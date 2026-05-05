---
name: line-chat
description: Read LINE chat exports (.txt) and summarize as daily timeline. Use when user says "line chat", "read line", "สรุปแชท", "อ่านแชท LINE", "line export", shares a LINE .txt file, or asks to analyze/summarize LINE messages.
---

# /line-chat

> Parse LINE exported chat (.txt) → split by day → timeline summary

## Usage

```
/line-chat <path-to-line-export.txt> [output_dir]
```

**Examples:**
```
/line-chat ~/Downloads/line-chat.txt
/line-chat D:/chats/group.txt D:/chats/output
/line-chat chat.txt --encoding=cp874
```

## How It Works

1. **Parse** the LINE .txt export using the Python parser
2. **Split** into one file per day (`YYYY-MM-DD.txt`)
3. **Generate** `_timeline.md` (overview + first/last messages per day)
4. **Generate** `_stats.json` (message counts, participants, daily breakdown)

## Execution

Run the parser script:

```bash
python3 /d/Claude/.claude/skills/line-chat/parse_line_chat.py "<input_file>" [output_dir] [--encoding=utf-8]
```

If the file is on the user's machine, ask for the path. The script auto-detects encoding (tries utf-8 → utf-8-sig → cp874).

**Default output directory:** `<filename>_daily/` next to the input file.

## After Parsing

Once the script finishes:

1. **Read `_stats.json`** to understand the chat structure
2. **Read `_timeline.md`** to get the overview
3. **Present the summary in Thai** (or match user's language):
   - จำนวนวันทั้งหมด / ข้อความทั้งหมด
   - ผู้เข้าร่วมสนทนา
   - สรุป timeline แต่ละวัน (ใครพูดอะไร, กี่ข้อความ)
4. If the user wants detail on a specific day, **read that day's `.txt` file** and summarize

## Supported Formats

LINE exports messages as `.txt` in this structure:

```
[LINE] ประวัติการแชทกับ GroupName
บันทึกวันที่ 2024/01/15 10:30

2024/01/15 จันทร์
10:30	UserA	สวัสดีครับ
10:31	UserB	สวัสดี!

2024/01/16 อังคาร
09:00	UserC	อรุณสวัสดิ์
```

English variant:
```
[LINE] Chat history with GroupName
Save date: 2024/01/15 10:30
```

## Encoding

- Default: `utf-8`
- LINE on Windows/Thai may use: `cp874`, `utf-8-sig`, `utf-16`
- Pass `--encoding=cp874` if utf-8 fails

## Output Structure

```
<filename>_daily/
├── _timeline.md       ← overview + daily first/last messages
├── _stats.json        ← structured data for analysis
├── 2024-01-15.txt     ← all messages from that day
├── 2024-01-16.txt
└── ...
```
