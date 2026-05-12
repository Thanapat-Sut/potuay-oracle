#!/usr/bin/env python3
"""Scan recent Claude Code transcripts and tally tool calls."""
import json
import os
import sys
import glob
from collections import Counter

projects = [
    os.path.expanduser("~/.claude/projects/D--Claude"),
    os.path.expanduser("~/.claude/projects/D--Claude-izu-oracle"),
]

files = []
for p in projects:
    files.extend(glob.glob(os.path.join(p, "*.jsonl")))

files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
files = files[:50]

bash_counter = Counter()
mcp_counter = Counter()

def first_token(cmd):
    """Extract first command token from a shell string."""
    if not cmd:
        return None
    cmd = cmd.strip()
    # Strip common prefixes
    while cmd.startswith(("sudo ", "timeout ", "env ")):
        cmd = cmd.split(" ", 1)[1].strip() if " " in cmd else ""
    # Handle env var assignments like FOO=bar cmd
    parts = cmd.split()
    while parts and "=" in parts[0] and not parts[0].startswith("="):
        parts = parts[1:]
    if not parts:
        return None
    cmd0 = parts[0]
    cmd1 = parts[1] if len(parts) > 1 else ""
    # Drop redirections
    if cmd1.startswith((">", "<", "|", "&", ";")):
        cmd1 = ""
    return (cmd0, cmd1)

for f in files:
    try:
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                msg = obj.get("message", {})
                if not isinstance(msg, dict):
                    continue
                content = msg.get("content")
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") != "tool_use":
                        continue
                    name = c.get("name", "")
                    inp = c.get("input", {}) or {}
                    if name == "Bash":
                        cmd = inp.get("command", "")
                        # Split on && and | to get individual commands
                        chunks = []
                        for sep in ["&&", "||", ";", "|"]:
                            if sep in cmd and not chunks:
                                chunks = [c.strip() for c in cmd.split(sep)]
                        if not chunks:
                            chunks = [cmd]
                        for chunk in chunks:
                            tok = first_token(chunk)
                            if tok:
                                bash_counter[tok] += 1
                    elif name.startswith("mcp__"):
                        mcp_counter[name] += 1
    except Exception as e:
        print(f"err {f}: {e}", file=sys.stderr)

print("=== BASH (top 60) ===")
for (cmd0, cmd1), n in bash_counter.most_common(60):
    print(f"{n}\t{cmd0} {cmd1}".rstrip())

print()
print("=== MCP (top 30) ===")
for name, n in mcp_counter.most_common(30):
    print(f"{n}\t{name}")
