# BGM Fade Pattern for casual-game

**Date**: 2026-04-19
**Source**: rrr: casual-game
**Tags**: audio, bgm, fade, unity, casual-game

## Pattern

Every game Manager follows this music flow:

```
Start()           → PlayMusic("XXX_BGM")         // immediate, full volume
Countdown start   → FadeOutMusic(0.5f)            // quick fade out
BeginPlaying()    → FadeInMusic("XXX_BGM", 1f)    // restart from beginning, 1s fade in
EndGame()         → FadeOutMusic(1.5f)             // slow fade out
ExitToSetup()     → FadeInMusic("XXX_BGM", 1f)    // restart music for menu
```

## BGM Names per Game

| Game | BGM Name |
|---|---|
| ChromaHunt | ColorBGM |
| ColorHunt | ColorBGM |
| DungeonRace | DungeonBGM |
| GhostBuster | GhostBGM |
| IceLand | IceBGM |
| LavaEscape | LavaBGM |
| SparkStep | LightBGM |
| MemoryMaze | MazeBGM |
| ShadowDodge | DodgeBGM |
| PixelPong | PongBGM |
| SerpentWar | SnakeBGM |
| TerritoryWars | WarBGM |

## Key Notes

- Music calls go in **Manager**, not UI
- Pilot prefers **direct calls** over AppState event-driven approach
- AudioManager is DontDestroyOnLoad singleton — music clips must be configured per scene
- `FadeInMusic` always restarts from time 0 (not resume)
- Sound names must match Inspector's Sound.name field exactly
