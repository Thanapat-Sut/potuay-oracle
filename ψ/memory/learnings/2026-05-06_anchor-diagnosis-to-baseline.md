# Anchor diagnosis to the user's baseline-working artifact

**Date**: 2026-05-06
**Source**: BT-7274 session, LED Player Pro 3.1.1 controller-2 debug
**Repo context**: bt-oracle / casual-game ecosystem

## Lesson

When a user reports "X doesn't work", the first move is **not** to enumerate everything that could be wrong with X. The first move is to identify what *similar thing* is working — the baseline — and use that to subtract layers from the suspect list.

## What happened

Pilot reported: "I want to add controller-2 in LED Player Pro 3.1.1, but it doesn't show up." Sent screenshot showing both controllers Offline.

My first reply: a 6-point network-layer checklist (PC subnet match, NIC adapter selection, link LEDs, ping test, ARP cache, switch loop).

Pilot's actual context, revealed in the next message: "controller-1 works normally; I'm just trying to add controller-2."

That single fact eliminated 4 of my 6 checklist items. The real suspect list was narrow: cable, switch port, PoE, IP conflict, controller-2 initial config. I should have arrived there in one reply, not two.

## Why this matters

A generic checklist is cheap to write but expensive in context. Each turn spent on the wrong layer:
- Burns the user's attention on irrelevant checks
- Risks the user actually doing the wrong checks (untrust your real adapter, change static IPs, etc.)
- Delays the actual diagnosis

## How to apply

When a user reports a problem with one of N similar artifacts:

1. **Ask first**: "Is the equivalent working right now? Has it ever worked?"
2. **If something works**: subtract everything that the working artifact already proves OK (network, software config, PC, account, etc.). The remaining suspects are specific to the failing artifact.
3. **Only after** subtraction → give the focused checklist.

## Counter-example to avoid

❌ Receive screenshot showing both X1 and X2 offline → assume "both broken = shared cause" → checklist for shared infrastructure.

This treats the screenshot as the steady state. It's a snapshot. The user's mental model (which artifact normally works) is the steady state.

## Trigger phrases

When you hear:
- "I'm trying to add a NEW [thing]"
- "Yesterday it was fine"
- "[Other thing] works"

→ STOP. Anchor to the working baseline before generating any checklist.
