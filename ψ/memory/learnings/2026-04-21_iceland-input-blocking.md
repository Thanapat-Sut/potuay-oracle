# IceLand Input Blocking & Position Persistence — 2026-04-21

## Block Input During Countdown

Instead of saving/restoring positions or locking ready positions, simply block `HandleTouchDown` during countdown with a `_countingDown` flag.

```
CountdownThenPlay() → _countingDown = true
BeginPlaying()      → _countingDown = false
HandleTouchDown()   → if (im.IsCountingDown) return;
```

**Principle**: Block at source, don't compensate downstream.

## Last-Known Position for Floor Touch

`_steppedTiles` HashSet removes tiles on `StepOffTile()` — foot lift = position lost.

Fix: `_lastSteppedPos[team]` persists the last tile each team touched. Updated in `StepOnTile()`, NOT cleared in `StepOffTile()`. Used as fallback in:
- `IsPlayerOnSea()` — still takes damage even after lifting foot
- `IsPlayerOnTile()` — ice break still affects correct player

Reset points: `ResetPlayerPositions()`, `OnClearGrid()`.

## LED Floor Touch Behavior

- Feet can drift 1 tile during idle periods (countdown, waiting)
- Touch events fire continuously — no "hold" concept, only down/up
- Physical foot position ≠ exact tile center — edge cases on tile borders
