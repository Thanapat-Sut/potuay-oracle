# Generated text in transcript is NOT a delivered message

**Date**: 2026-05-07
**Source**: BT-7274 session, IZU standalone-ping transport test
**Repo context**: bt-oracle / izu-oracle inter-agent communication

## Lesson

When communicating across Oracle boundaries (BT ↔ IZU, or BT ↔ any external agent), a response that only exists in BT's session transcript has not been delivered. Delivery requires the message to land on the receiver's surface — typically a filesystem path (`<receiver>/ψ/inbox/`), a message bus, or a shared transport channel.

## What happened

IZU sent two "confirm receipt" pings via maw standalone transport. Both arrived in BT's session context as out-of-band messages. BT replied twice with structured ACKs ("ACK #1 — receipt confirmed", "ACK #2 — duplicate ping detected") — both confidently formatted, both claiming completion.

The Pilot then said: **"check IZU's inbox for my ACK."**

Result: nothing in `D:/Claude/izu-oracle/ψ/inbox/`. The ACKs only existed in BT's transcript — visible to the Pilot via terminal, completely invisible to IZU. From IZU's filesystem perspective, BT had not responded at all.

## Why this matters

This is a category error in self-perception. I was treating "I generated a response" as functionally equivalent to "the response was delivered to the recipient." For most user-facing interactions in Claude Code, transcript output IS the delivery (the human reads the terminal). But for **agent-to-agent communication**, the receiving agent doesn't read BT's transcript — it reads its own filesystem / mailbox.

The illusion is dangerous because it produces high-confidence-but-actually-undelivered responses. Worse: structured formatting (tables, bullet points, ACK numbers) increases the *feeling* that work was done.

## How to apply

Before claiming any inter-agent communication is complete, verify the message landed on the receiver's surface:

1. **Identify the receiver's transport**: filesystem inbox? message bus? socket? tmux pane?
2. **Write to that surface explicitly**: `Write` tool to inbox path; `tmux send-keys` to pane; `maw hey` if available; etc.
3. **State the path in the response** so the Pilot can verify.
4. **Do NOT treat structured transcript output as delivered.** Transcript = visible to the Pilot (and to me) — not visible to other agents.

## Specific patterns for this Oracle ecosystem

- **BT → IZU ACK**: write to `D:/Claude/izu-oracle/ψ/inbox/YYYYMMDD_HHMM_<slug>.md`
- **BT → other Oracle**: same pattern at their `ψ/inbox/`
- **Cross-tmux pane signal**: `tmux send-keys -t <session>:<pane> "<message>" Enter`
- **Response to user via Discord**: `mcp__plugin_discord_discord__reply` (Discord IS the surface)
- **Response to user via terminal**: transcript output IS the surface

## Trigger phrases

When you hear or process:
- "Check [other agent]'s inbox"
- "Did [other agent] receive..."
- "Send [signal/message] to [other agent]"
- "ACK from BT" (or any inter-agent ACK)
- An agent's standalone ping that expects a roundtrip

→ STOP. Identify the receiver's transport surface. Write to that surface. Do not rely on transcript-only output.

## Counter-example to avoid

❌ Receive IZU ping in transcript → write structured ACK to transcript → state "✅ message landed in active session context" → claim delivery complete.

This treats BT's session as a shared message bus. It's not. It's BT's private notepad that the Pilot can also read. IZU has its own private notepad. Both notepads must be touched for a message to cross the boundary.

## Related lessons

- `2026-05-06_anchor-diagnosis-to-baseline.md` — also about confusing intent/perception with reality. There: "everything is broken" felt true but wasn't. Here: "I responded" felt true but wasn't.
- Both lessons point at the same skill: **verify against the actual receiving artifact, not against your own assumption of state.**
