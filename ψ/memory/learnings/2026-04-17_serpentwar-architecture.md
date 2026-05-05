# SerpentWar Architecture Notes

**Date**: 2026-04-17
**Source**: rrr: char-oracle

## Directory

- `Assets/Scripts/SerpentWar/` = active, refactored version (uses BaseGridManager, BaseGameUI)
- `Assets/Scripts/SnakeWars/` = old prototype (standalone, NOT in use)
- Always work in SerpentWar, not SnakeWars

## Key Files

| File | Role |
|------|------|
| SerpentWarManager | Game state, input routing, game tick |
| SerpentWarGridManager | Floor LED grid (extends BaseGridManager) |
| SerpentWarBoardRenderer | Projector display — UI-based (RectTransform/Image), NOT Texture2D |
| SerpentWarUI | Screen UI — extends BaseGameUI, has countdown, video, panels |
| SerpentWarConfig | ScriptableObject with all game settings |

## BoardRenderer

- Uses RectTransform containers with Image components
- Snake rendering: pooled body Image objects as children of per-player root
- Fruit: single Image object
- Shrink walls: 4 RectTransform panels
- Countdown: TextMeshProUGUI overlay (added 2026-04-17)

## Countdown Flow

```
Manager.CountdownCoroutine()
  → yield UI.StartCountdown()
    → plays intro video
    → CountdownRoutine() from BaseGameUI
      → grid.RenderDigitOnGrid() + boardRenderer.RenderCountdownDigit()
      → grid.RenderGoOnGrid() + boardRenderer.RenderGo()
      → grid.SetAllTilesBlack() + boardRenderer.HideCountdown()
  → StartGame()
```
