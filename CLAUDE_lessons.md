# CLAUDE_lessons.md - Lessons Learned

> **Navigation**: [Main](CLAUDE.md) | [Safety](CLAUDE_safety.md) | [Workflows](CLAUDE_workflows.md) | [Subagents](CLAUDE_subagents.md) | **Lessons**

*(This section should be continuously updated with project-specific findings)*

---

## Key Learnings

### Oracle Philosophy
- **001-frequency-reveals-priority**: What you repeat frequently reveals what matters.
- **002-rules-are-starting-points**: Rules exist as starting points, not rigid constraints.

### Delegation & Token Efficiency
- **003-delegate-to-haiku**: Main agent should NOT read files directly for exploration. Use Haiku subagents. Cost ratio: Opus ~15x more.

---

## Common Mistakes to Avoid
- Jumping to workarounds before root cause analysis
- Reading files directly in Opus when Haiku can do it cheaper
- Forgetting to create retrospective at session end

---

**See also**: [CLAUDE.md](CLAUDE.md) for quick reference
