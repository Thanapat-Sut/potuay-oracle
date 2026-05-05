# Onset Detection vs BPM Generation — Density Mismatch

**Date**: 2026-04-29
**Source**: rrr: bt-oracle (BeatStomp session)
**Status**: Learned, system reverted pending senior review

## Core Lesson

Audio onset detection (RMS energy spike analysis) finds **every transient** in a music track — kicks, snares, hi-hats, vocal attacks, synth stabs. A 60-second pop track can produce 400-800+ onsets. BPM-based procedural generation at 120 BPM produces ~120 evenly-spaced beats for the same duration.

When switching from BPM-based to onset-based chart generation, **density must be recalibrated downward** (e.g., from 0.50-0.90 to 0.15-0.40) to maintain playable note counts.

## AudioManager Naming Convention

BeatStomp AudioManager uses constructed names: `{prefix}{index}BGM`
- Easy: `Rhythm_Easy1BGM`, `Rhythm_Easy2BGM`, `Rhythm_Easy3BGM`
- Normal: `Rhythm_Meduim1BGM` (note: typo is intentional/legacy)
- Hard: `Rhythm_Hard1BGM`, `Rhythm_Hard2BGM`, `Rhythm_Hard3BGM`

AudioClip filenames (e.g., `Rhythm Stomp - Easy BGM 2`) do NOT match. Any system using clip-derived names must map to AudioManager names explicitly.

## Principle

Game design parameters (density, difficulty curves) need designer sign-off. Developer intuition alone is insufficient for player experience tuning.
