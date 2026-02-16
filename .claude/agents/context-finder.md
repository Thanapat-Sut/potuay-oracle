# context-finder

**Fast search through git history, retrospectives, issues, and codebase**

## Usage

Task tool with subagent_type='context-finder'

## Model

**haiku** (fast, cost-effective)

## Behavior

- Searches git log, file system, retrospectives, and learnings
- Returns file paths + excerpts for main agent to read
- Scores results by recency + type + impact

## Scoring

| Score | Level | Meaning |
|-------|-------|---------|
| 6+ | Critical | Read immediately |
| 4-5 | Important | Review soon |
| 2-3 | Notable | Background context |
| 0-1 | Background | Low priority |

## Output Format

Compact table with scored results:

```
| Score | When | File | What |
|-------|------|------|------|
| 6+ | 5m | src/index.ts | New feature |
| 4 | 1h | .claude/x.md | Config change |
```
