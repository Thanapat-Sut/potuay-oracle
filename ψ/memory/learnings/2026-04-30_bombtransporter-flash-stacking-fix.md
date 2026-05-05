# Flash Coroutine Color Stacking Fix

**Date**: 2026-04-30
**Context**: BombTransporter FlashTeamSide causing permanent red tint after many explosions
**Source**: rrr: casual-game

## Problem

`BaseTileController.Flash()` captures `orig = _sr.color` at coroutine start, then lerps back to `orig` when done. When explosions happen rapidly:

1. Flash A starts, captures `orig = floorColor`
2. Flash A sets `_sr.color = explosionColor`
3. Flash B starts (kills A), captures `orig = explosionColor` (wrong!)
4. Flash B lerps back to `explosionColor` instead of `floorColor`
5. Each subsequent flash drifts further from true floor color

After 11 hits, the entire team side was permanently dark red.

## Fix

In `FlashTeamSide`, before calling `Flash()`:
1. Skip tiles that aren't `BombTileState.Floor` (let Bomb/Exploding handle their own visuals)
2. Force-reset `_sr.color` to true floor color so `Flash()` captures correct `orig`

```csharp
foreach (int i in tiles) {
    if (_allTiles[i] == null) continue;
    if (_allTiles[i].CurrentState != BombTileState.Floor) continue;
    _allTiles[i].SetColor(_allTiles[i].IsBorder ? config.borderColor : config.floorColor);
    _allTiles[i].Flash(config.explosionColor, duration);
}
```

## Principle

Same as IceLand input blocking: **block at source, don't compensate downstream**. Don't try to fix Flash() internals — just ensure it always receives clean state.

## Applicability

Any game using `BaseTileController.Flash()` with rapid repeated calls on the same tiles. Watch for:
- Score-based games with frequent team-side flashes
- Any Flash usage where the trigger rate > flash duration
