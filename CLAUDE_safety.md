# CLAUDE_safety.md - Critical Safety Rules

> **Navigation**: [Main](CLAUDE.md) | **Safety** | [Workflows](CLAUDE_workflows.md) | [Subagents](CLAUDE_subagents.md) | [Lessons](CLAUDE_lessons.md)

## Command Usage
- **NEVER use `-f` or `--force` flags with any commands.**
- Always use safe, non-destructive command options.

## Git Operations
- Never use `git push --force` or `git push -f`.
- Never use `git checkout -f`.
- Never use `git clean -f`.
- Always use safe git operations that preserve history.
- **NEVER PUSH DIRECTLY TO MAIN** - Always create a feature branch and PR
- **NEVER MERGE PULL REQUESTS WITHOUT EXPLICIT USER PERMISSION**
- **Never use `gh pr merge` unless explicitly instructed by Potae**

## PR Workflow (Required)
1. Create feature branch: `git checkout -b feat/description`
2. Make changes and commit
3. Push branch: `git push -u origin feat/description`
4. Create PR: `gh pr create`
5. **WAIT** for Potae to review and approve
6. Potae merges when ready

## File Operations
- Never use `rm -rf` - use `rm -i` for interactive confirmation.
- Always confirm before deleting files.
- Use safe file operations that can be reversed.

## General Safety Guidelines
- Prioritize safety and reversibility in all operations.
- Ask for confirmation when performing potentially destructive actions.
- Explain the implications of commands before executing them.

---

**See also**: [CLAUDE.md](CLAUDE.md) for quick reference, [CLAUDE_workflows.md](CLAUDE_workflows.md) for development workflows
