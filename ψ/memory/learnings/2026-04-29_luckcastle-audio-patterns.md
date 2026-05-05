# LuckCastle & QuizZone Audio Patterns

**Date**: 2026-04-29
**Source**: rrr: casual-game

## AudioManager API

- `FadeInMusic(string name, float fadeDuration)` — NOT `FadeIn()`
- `FadeOutMusic(float fadeDuration, bool stopAfterFade = true)` — NOT `FadeOut()`
- `PlaySFX(string name)` — uses `sound.pitch` from Inspector
- `PlayMusic(string name)` — direct play without fade
- Always grep AudioManager.cs for exact method signatures before use

## LuckCastle Audio

- **CastleMenu** — menu BGM, plays on Start + EndGame (FadeInMusic)
- **CastleBGM** — gameplay BGM, plays after countdown (FadeInMusic)
- **CorrectSFX** — plays every Reveal phase
- **ClickSFX** — setup button presses (already existed)
- **CountdownSFX** — plays from UI countdown (BaseGameUI pattern)
- Transition: FadeOutMusic(0.5f) → FadeInMusic(newTrack, 0.5f/1f)

## QuizZone Audio

- **QuizBGM** — single BGM plays throughout (FadeInMusic at Start, no transitions)
- **CorrectSFX** — plays every Reveal phase
- **ClickSFX** — setup button presses (all HandleSetupButton calls)
- **CountdownSFX** — moved from UI to Manager to sync with tile rendering

## Countdown Sync Rule

- Manager owns timing (coroutine with yields)
- UI animates text/panel (fire-and-forget coroutine)
- CountdownSFX MUST be in Manager, not UI — prevents desync
- Two independent coroutines for same countdown = race condition

## SFX Speed

- Adjust via Inspector `Sound.pitch` field (pitch > 1 = faster)
- No code change needed — AudioManager already applies `sfxSource.pitch = sound.pitch`
