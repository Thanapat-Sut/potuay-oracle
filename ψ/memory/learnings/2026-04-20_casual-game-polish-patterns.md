# casual-game Polish Patterns — 2026-04-20

## AudioManager DontDestroyOnLoad + MergeClips

When multiple scenes have their own AudioManager prefab, the singleton pattern with DontDestroyOnLoad means the first-loaded instance survives and destroys all later ones. Problem: scene-specific clips on the destroyed instances are lost.

**Solution**: In Awake(), before Destroy, call `Instance.MergeClips(musicClips, sfxClips)` to hand off clips to the survivor. Only adds clips that don't already exist (by name).

## BGM Fade Standard

All 11 casual games follow this flow:
- **Start()**: `PlayMusic("GameBGM")`
- **Countdown**: `FadeOutMusic(0.5f)`
- **BeginPlaying**: `FadeInMusic("GameBGM", 1f)`
- **EndGame**: nothing (BGM keeps playing)
- **ExitToSetup**: `FadeInMusic("GameBGM", 1f)`

## SFX Standard

- **CountdownSFX**: Single 4-second clip (3-2-1-GO sounds). Play once before countdown loop, NOT per digit.
- **ClickSFX**: Used only for button presses (StartGame, HandleGameOverButton). NOT for in-game scoring.

## /hm Humanization Conventions

| Original | Humanized |
|----------|-----------|
| `_gameLoopCoroutine` | `_loopCo` |
| `_gameTimerCo` | `_timerCo` |
| `StopCo(ref co)` / `StopAndClear` | `Kill(ref co)` |
| `StopAllGameCoroutines()` | `StopGameCo()` / `StopAllCo()` |
| `_setupGridReady` | `_gridReady` |
| `_isCountingDown` | `_countingDown` |
| `_lastDamageTime` | `_lastDmgTime` |
| `visualCols/visualRows` | `cols/rows` |
| `nextCol/nextRow` | `nx/ny` |
| XML `<summary>` docs | Short `//` or removed |

Don't rename: public API, serialized fields, event names.
