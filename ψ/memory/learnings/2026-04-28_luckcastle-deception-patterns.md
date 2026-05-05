# LuckCastle Deception Patterns

**Date**: 2026-04-28
**Source**: rrr: casual-game (LuckCastle round logic)

## Score Display Architecture

```
displayScores  →  shown during Choosing phase (may be fake)
shuffledScores →  shown during Reveal phase (always real)
```

## Deception Modes Implemented

| Deception | Display | Real | Key Mechanic |
|-----------|---------|------|-------------|
| `none` | = real | shuffled | No trick |
| `reverse` (LC-005) | descending [50,30,10,0] | ascending [0,10,30,50] | Fixed flip, deterministic |
| `reverse_with_hint` (LC-008) | shuffled normally | lowest-display zone → best score, rest random | Semi-predictable |
| `one_truth` (LC-006) | 1 real + 3 shuffled fakes | real scores | `truthZoneIndex` tracks unchanged zone |
| `maybe_lie` (LC-007) | 50% real, 50% shifted | real scores | Binary gamble |

## UI Patterns

- `int.MinValue` sentinel → UI hides that score slot (`gameObject.SetActive(false)`)
- `isReveal` parameter → controls score text color (white during choosing, ranked colors during reveal)
- `truthZoneIndex` → computed post-hoc by comparing `displayScores[i] == shuffledScores[i]`
- Risk mode → `revealScores[1] = int.MinValue` hides silver on reveal

## Design Principle

LC-005 (reverse) is deterministic — player who listens to hint can always win.
LC-008 (reverse_with_hint) is semi-random — only minimum→maximum is guaranteed. Harder to exploit.
This distinction creates difficulty progression within the deception category (Group B).
