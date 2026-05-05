#!/usr/bin/env python3
"""
LINE Chat Export Parser
Splits a LINE .txt export into daily files and generates a timeline summary.

Supports two LINE export formats:

Format A (Desktop / tab-separated):
  [LINE] ประวัติการแชทกับ GroupName
  บันทึกวันที่ 2024/01/15 10:30
  <blank>
  2024/01/15 จันทร์
  10:30\tUserA\tMessage text
  10:31\tUserB\tAnother message

Format B (Mobile / space-separated):
  2025.12.20 วันเสาร์
  22:31 UserA รูป
  22:31 UserB สวัสดีครับ
"""

import re
import sys
import os
import json
from pathlib import Path
from collections import defaultdict, Counter

# --- Format detection ---

# Date headers
DATE_SLASH_RE = re.compile(r'^(\d{4}/\d{2}/\d{2})\s+\S+')       # 2024/01/15 จันทร์
DATE_DOT_RE = re.compile(r'^(\d{4}\.\d{2}\.\d{2})\s+\S+')        # 2025.12.20 วันเสาร์

# Message patterns
MSG_TAB_RE = re.compile(r'^(\d{1,2}:\d{2})\t(.+?)\t(.*)$')       # HH:MM\tSender\tMsg
MSG_SPACE_RE = re.compile(r'^(\d{1,2}:\d{2})\s+(.+)$')           # HH:MM Sender Msg


def detect_format(lines: list[str]) -> str:
    """Detect whether the file uses tab-separated or space-separated format."""
    for line in lines[:50]:
        line = line.rstrip('\n\r')
        if MSG_TAB_RE.match(line):
            return 'tab'
        if DATE_DOT_RE.match(line):
            return 'space'
    # Fallback: check if any line has tabs
    for line in lines[:100]:
        if '\t' in line:
            return 'tab'
    return 'space'


def identify_senders_space_format(lines: list[str]) -> set[str]:
    """
    For space-separated format, identify sender names by frequency analysis.

    Strategy: after HH:MM, the text is 'SenderName Message'.
    We collect all candidate prefixes and find the ones that appear as
    consistent sender names across multiple messages.
    """
    # Collect all text after HH:MM
    time_re = re.compile(r'^(\d{1,2}:\d{2})\s+(.+)$')
    after_time = []

    for line in lines:
        line = line.rstrip('\n\r')
        m = time_re.match(line)
        if m:
            after_time.append(m.group(2))

    if not after_time:
        return set()

    # Strategy: try splitting each "after_time" text at each space position.
    # The part before the space is a candidate sender name.
    # Real sender names will appear many times.
    candidate_counts = Counter()

    for text in after_time:
        # Try each possible split point (1st space, 2nd space, etc.)
        parts = text.split(' ')
        for i in range(1, len(parts)):
            candidate = ' '.join(parts[:i])
            candidate_counts[candidate] += 1

    # A sender name should appear at least twice (or be the only pattern)
    # Pick candidates that appear frequently relative to total messages
    total = len(after_time)
    senders = set()

    # Sort by count descending, then by length descending (prefer longer matches)
    sorted_candidates = sorted(candidate_counts.items(), key=lambda x: (-x[1], -len(x[0])))

    covered = [False] * total

    for candidate, count in sorted_candidates:
        if count < 2 and total > 2:
            continue
        # Check: does this candidate cover uncovered messages?
        new_covers = 0
        for idx, text in enumerate(after_time):
            if not covered[idx] and text.startswith(candidate + ' ') or text == candidate:
                new_covers += 1

        if new_covers > 0 and count >= max(2, total * 0.05):
            senders.add(candidate)
            for idx, text in enumerate(after_time):
                if text.startswith(candidate + ' ') or text == candidate:
                    covered[idx] = True

    # If we still have uncovered lines, try single-occurrence senders
    if not all(covered):
        for idx, text in enumerate(after_time):
            if not covered[idx]:
                # The whole text might be "SenderName Message" with a new sender
                # Take the first word as sender
                parts = text.split(' ', 1)
                if len(parts) >= 1:
                    senders.add(parts[0])

    return senders


def parse_space_message(text: str, senders: set[str]) -> tuple[str, str]:
    """
    Given text after 'HH:MM ', split into (sender, message).
    Tries longest matching sender name first.
    """
    # Sort senders by length descending to match longest first
    for sender in sorted(senders, key=len, reverse=True):
        if text.startswith(sender + ' '):
            return sender, text[len(sender) + 1:]
        if text == sender:
            return sender, ''

    # Fallback: first word is sender
    parts = text.split(' ', 1)
    return parts[0], parts[1] if len(parts) > 1 else ''


def normalize_date(date_str: str) -> str:
    """Normalize date to YYYY/MM/DD format."""
    return date_str.replace('.', '/')


def parse_line_export(filepath: str, encoding: str = 'utf-8') -> dict:
    """Parse a LINE .txt export file. Returns {header, days: {date: [messages]}}."""
    with open(filepath, 'r', encoding=encoding) as f:
        lines = f.readlines()

    fmt = detect_format(lines)
    date_re = DATE_DOT_RE if fmt == 'space' else DATE_SLASH_RE

    # For space format, identify senders first
    senders = set()
    if fmt == 'space':
        senders = identify_senders_space_format(lines)

    days = {}
    current_date = None
    current_messages = []
    header_lines = []

    i = 0
    # Collect header lines (before first date)
    while i < len(lines):
        line = lines[i].rstrip('\n\r')
        if date_re.match(line):
            break
        header_lines.append(line)
        i += 1

    # Parse messages by date
    while i < len(lines):
        line = lines[i].rstrip('\n\r')

        date_match = date_re.match(line)
        if date_match:
            if current_date and current_messages:
                days[current_date] = current_messages
            current_date = normalize_date(date_match.group(1))
            current_messages = []
            i += 1
            continue

        if fmt == 'tab':
            msg_match = MSG_TAB_RE.match(line)
            if msg_match:
                time_str, sender, text = msg_match.groups()
                current_messages.append({
                    'time': time_str,
                    'sender': sender,
                    'text': text
                })
                i += 1
                continue
        else:
            msg_match = MSG_SPACE_RE.match(line)
            if msg_match:
                time_str = msg_match.group(1)
                rest = msg_match.group(2)
                sender, text = parse_space_message(rest, senders)
                current_messages.append({
                    'time': time_str,
                    'sender': sender,
                    'text': text
                })
                i += 1
                continue

        # Continuation line or blank
        if line.strip() and current_messages:
            current_messages[-1]['text'] += '\n' + line
        i += 1

    # Save last day
    if current_date and current_messages:
        days[current_date] = current_messages

    return {
        'header': '\n'.join(header_lines).strip(),
        'days': days,
        'format': fmt,
        'detected_senders': sorted(senders) if senders else [],
    }


def write_daily_files(parsed: dict, output_dir: str) -> list:
    """Write individual daily chat files. Returns list of created files."""
    os.makedirs(output_dir, exist_ok=True)
    created = []

    for date_str, messages in sorted(parsed['days'].items()):
        safe_date = date_str.replace('/', '-')
        filename = f"{safe_date}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {date_str}\n")
            if parsed['header']:
                f.write(f"# {parsed['header'].splitlines()[0]}\n")
            f.write(f"# Messages: {len(messages)}\n\n")

            for msg in messages:
                f.write(f"[{msg['time']}] {msg['sender']}: {msg['text']}\n")

        created.append(filepath)

    return created


def generate_timeline(parsed: dict, output_dir: str) -> str:
    """Generate a timeline summary markdown file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, '_timeline.md')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# LINE Chat Timeline\n\n")
        if parsed['header']:
            f.write(f"> {parsed['header'].splitlines()[0]}\n\n")

        total_msgs = sum(len(msgs) for msgs in parsed['days'].values())
        all_senders = set()
        for msgs in parsed['days'].values():
            for m in msgs:
                all_senders.add(m['sender'])

        f.write(f"**Days:** {len(parsed['days'])}  \n")
        f.write(f"**Total messages:** {total_msgs}  \n")
        f.write(f"**Participants:** {', '.join(sorted(all_senders))}  \n\n")
        f.write("---\n\n")

        for date_str in sorted(parsed['days'].keys()):
            messages = parsed['days'][date_str]
            safe_date = date_str.replace('/', '-')

            sender_counts = defaultdict(int)
            for m in messages:
                sender_counts[m['sender']] += 1

            f.write(f"## {date_str}\n\n")
            f.write(f"**{len(messages)} messages** | ")
            f.write(' | '.join(f"{s}: {c}" for s, c in sorted(sender_counts.items())))
            f.write("  \n")
            f.write(f"See: [{safe_date}.txt]({safe_date}.txt)\n\n")

            if messages:
                first = messages[0]
                last = messages[-1]
                f.write(f"- `{first['time']}` **{first['sender']}**: {_truncate(first['text'])}\n")
                if len(messages) > 1:
                    f.write("- ...\n")
                    f.write(f"- `{last['time']}` **{last['sender']}**: {_truncate(last['text'])}\n")
            f.write("\n")

    return filepath


def _truncate(text: str, max_len: int = 80) -> str:
    """Truncate text for summary display."""
    first_line = text.split('\n')[0]
    if len(first_line) > max_len:
        return first_line[:max_len] + '...'
    return first_line


def generate_stats_json(parsed: dict, output_dir: str) -> str:
    """Generate a stats JSON for Claude to read."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, '_stats.json')

    all_senders = defaultdict(int)
    daily_stats = {}

    for date_str, messages in sorted(parsed['days'].items()):
        sender_counts = defaultdict(int)
        for m in messages:
            sender_counts[m['sender']] += 1
            all_senders[m['sender']] += 1
        daily_stats[date_str] = {
            'message_count': len(messages),
            'senders': dict(sender_counts),
            'first_message_time': messages[0]['time'] if messages else None,
            'last_message_time': messages[-1]['time'] if messages else None,
        }

    stats = {
        'header': parsed['header'],
        'format_detected': parsed.get('format', 'unknown'),
        'senders_detected': parsed.get('detected_senders', []),
        'total_days': len(parsed['days']),
        'total_messages': sum(len(m) for m in parsed['days'].values()),
        'participants': dict(all_senders),
        'daily': daily_stats,
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    return filepath


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_line_chat.py <chat.txt> [output_dir] [--encoding=utf-8]")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    base = Path(input_file).stem
    default_out = os.path.join(os.path.dirname(input_file) or '.', f"{base}_daily")
    output_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else default_out

    encoding = 'utf-8'
    for arg in sys.argv:
        if arg.startswith('--encoding='):
            encoding = arg.split('=', 1)[1]

    print(f"Parsing: {input_file}")
    print(f"Output:  {output_dir}")
    print(f"Encoding: {encoding}")
    print()

    try:
        parsed = parse_line_export(input_file, encoding=encoding)
    except UnicodeDecodeError:
        print("UTF-8 failed, trying utf-8-sig...")
        try:
            parsed = parse_line_export(input_file, encoding='utf-8-sig')
        except UnicodeDecodeError:
            print("Trying cp874 (Thai Windows)...")
            parsed = parse_line_export(input_file, encoding='cp874')

    if not parsed['days']:
        print("Error: No chat days found. Check file format.")
        sys.exit(1)

    print(f"Format:  {parsed.get('format', 'unknown')}")
    if parsed.get('detected_senders'):
        print(f"Senders: {parsed['detected_senders']}")
    if parsed['header']:
        print(f"Header:  {parsed['header'][:100]}")
    print(f"Days:    {len(parsed['days'])}")
    total = sum(len(m) for m in parsed['days'].values())
    print(f"Messages:{total}")
    print()

    daily_files = write_daily_files(parsed, output_dir)
    print(f"Created {len(daily_files)} daily files:")
    for f in daily_files:
        print(f"  {f}")

    timeline = generate_timeline(parsed, output_dir)
    print(f"\nTimeline: {timeline}")

    stats = generate_stats_json(parsed, output_dir)
    print(f"Stats:    {stats}")

    print("\nDone!")


if __name__ == '__main__':
    main()
