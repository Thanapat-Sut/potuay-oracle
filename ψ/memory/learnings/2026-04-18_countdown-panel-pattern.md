# Lesson: Countdown Panel System Pattern

**Date**: 2026-04-18
**Source**: casual-game BaseGameUI refactor
**Tags**: Unity, UI, animation, countdown, BaseGameUI

## Pattern

BaseGameUI provides a shared countdown animation system:
- `countdownPanel` (GameObject) + `countdownText` (TMP, font size 348)
- Grid-based CountdownRoutine auto-syncs projector TMP with LED Floor
- Animated: ElasticOut punch → pulse hold → shrink fade (per digit), GO! has yellow→green flash
- `SetAsLastSibling()` on panel show to fix z-order
- Null-safe: games without panel assigned skip silently

## Intro Video → Waiting Tiles Pattern

Used in IceLand and TerritoryWars:
1. Manager calls `SetState(Waiting)` → UI shows gameplay panel (no tiles yet)
2. Manager yields `ui.PlayIntroAndWait()` — plays intro video, waits for clip length
3. After video: `gridManager.SetupWaitingCorners()` + `InitPlayerSlots()`
4. `ui.ShowWaitingStatus()` — shows "STEP ON YOUR POSITION"

## Key Techniques

- `ElasticOut(t)` easing: `Pow(2, -10t) * Sin((t - p/4) * 2PI/p) + 1` where p=0.3
- Fire-and-forget coroutine for animation alongside external timing
- `transform.SetAsLastSibling()` for runtime UI z-order control
