---
name: game-checklist
description: "Show game feature checklist table. Use when user says 'checklist', 'game checklist', 'game list', 'progress', or wants to see which games have a feature implemented."
---

# /game-checklist

Show the current implementation status of all casual games.

## Behavior

1. Read the checklist data from `D:/Claude/.claude/skills/game-checklist/data.md`
2. Display the table as-is
3. If the user asks to update a game's status or note, edit `data.md` accordingly

## Status Icons

- ✅ = done
- 🔧 = in progress
- ❌ = not done

## Update Rules

- When updating status, only change the specific row requested
- Keep the table aligned and formatted
- Always preserve existing notes unless asked to change them
