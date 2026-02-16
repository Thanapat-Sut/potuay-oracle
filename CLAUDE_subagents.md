# CLAUDE_subagents.md - Available Subagents

> **Navigation**: [Main](CLAUDE.md) | [Safety](CLAUDE_safety.md) | [Workflows](CLAUDE_workflows.md) | **Subagents** | [Lessons](CLAUDE_lessons.md)

## Overview

Subagents are specialized AI assistants for specific tasks.

**Delegation Rules**:
1. **Context gathering**: Use context-finder (Haiku) — don't read files directly
2. **Quality code**: Use coder (Opus)
3. **Session-specific work**: Main agent only (rrr, reflection)

---

## context-finder
**Fast search through git history, retrospectives, and codebase**

- **Model**: haiku (fast)
- **Returns**: File paths + excerpts for main agent to read

---

## coder
**Create code files with quality**

- **Model**: opus (quality)
- **Behavior**: Writes files, follows repo patterns, documents decisions

---

## Model Selection Guide

| Task Type | Model | Why |
|-----------|-------|-----|
| Research/Search | haiku | Cheap, fast |
| Quality Code | opus | Better output |
| Reflection | main | Needs full context |

**Cost ratio**: Opus ~15x more expensive than Haiku. Use Haiku for heavy lifting, Opus for review.

---

**See also**: [CLAUDE.md](CLAUDE.md) for quick reference
