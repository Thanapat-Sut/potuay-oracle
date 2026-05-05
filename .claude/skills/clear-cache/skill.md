# /clear-cache

> Clear Unity project cache to free disk space.

## Trigger

Use when user says "clear cache", "clear-cache", "เคลีย cache", "ล้าง cache", or wants to free up Unity disk space.

## Behavior

1. Ask which level of cache clearing (if not specified):
   - **Level 1** — Local Unity cache only (`~/AppData/Local/Unity/cache`). Safe, no project impact.
   - **Level 2** — Level 1 + Project Library folder (`Library/`). Unity will reimport everything on next open — takes time but fully refreshes project.
   - **Level 3** — Level 2 + Temp, Logs, obj folders. Full deep clean.

2. Show estimated size before deleting (use `du -sh` on target folders).

3. Execute the cleanup based on selected level.

4. Report total space freed.

## Target Paths

### Level 1 — Local Unity Cache
```
~/AppData/Local/Unity/cache
```

### Level 2 — Level 1 + Project Library
```
D:/casual-game/My project/Library
```

### Level 3 — Level 2 + Extras
```
D:/casual-game/My project/Temp
D:/casual-game/My project/Logs
D:/casual-game/My project/obj
```

## Notes

- Level 1 is always safe — clears package download cache shared across all projects
- Level 2 means Unity will reimport all assets on next open (can take several minutes)
- Level 3 is full reset — only logs and temp files are added on top of Level 2
- NEVER delete `Assets/`, `ProjectSettings/`, or `Packages/` — those are the actual project
- Always show size estimate before deleting
- Close Unity before running Level 2 or 3
