# MirrorDance: Scoring Inversion + Center Line

**Date**: 2026-04-27
**Source**: Senior review feedback
**Game**: MirrorDance (casual-game)

## Scoring Inversion Pattern

**Before**: DEF fail → `ApplyScore(defender, -50)` (punish defender)
**After**: DEF fail → `ApplyScore(attacker, +50)` (reward attacker)

This applies to both:
- `HandleDefendStep` — wrong tile order (immediate fail)
- `RoundLoopRoutine` — timeout (phase timer expired)

**Design principle**: Reward the offensive player for creating a difficult pattern, don't punish the defensive player for failing. Better incentive structure.

## Center Line

- `RenderCenterLine()` in GridManager — draws 1-tile-wide line at team boundary
- CrossLane mode: vertical line at `visCols / 2`
- SingleLane mode: horizontal line at `visRows / 2`
- Must be called after every `SetAllFloor()` (fragile pattern — 3 call sites)
- Active area tiles override center line tiles when they overlap

## Player Color Removal

- `SetPlayerOccupied` no longer changes tile color
- `SetTileState` no longer has `_hasPlayer` early return
- Tiles always show game state (ActiveArea, AttackSelected, DefendTarget, etc.)
- `_hasPlayer` bool still tracked but purely for logic, not visuals
