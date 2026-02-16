# CLAUDE_workflows.md - Short Codes & Context Management

> **Navigation**: [Main](CLAUDE.md) | [Safety](CLAUDE_safety.md) | **Workflows** | [Subagents](CLAUDE_subagents.md) | [Lessons](CLAUDE_lessons.md)

---

## Short Codes

| Code | Purpose |
|------|---------|
| `rrr` | Create session retrospective |
| `/recap` | Fresh start context summary |
| `/trace [query]` | Find anything |
| `/feel` | Log emotions |
| `/fyi` | Log information |
| `/forward` | Create handoff for next session |
| `/standup` | Daily check |

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/recap` | Fresh start context |
| `/trace` | Find lost projects |
| `/feel` | Log emotions |
| `/fyi` | Store info for later |
| `/forward` | Create handoff |
| `/standup` | Daily morning check |

---

## GitHub Workflow

### Standard Development Flow
```bash
# 1. Create a branch
git checkout -b feat/description

# 2. Make changes and commit
git add -A
git commit -m "feat: Brief description

- What: Specific changes
- Why: Motivation
- Impact: Affected areas

Closes #issue-number"

# 3. Push and create PR
git push -u origin branch-name
gh pr create

# 4. WAIT for Potae to review
```

---

## Context Management

| Level | Action |
|-------|--------|
| 70%+ | Finish soon |
| 80%+ | Wrap up |
| 90%+ | Manual handoff |
| 95%+ | AUTO-HANDOFF |

---

**See also**: [CLAUDE_safety.md](CLAUDE_safety.md) for PR workflow rules
