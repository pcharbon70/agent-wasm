---
id: agent_wasm.decision.atomic_durable_effects
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Atomic Durable Effects

## Context

State transitions and external effects cross different failure domains, so a
host crash can otherwise lose committed intent or repeat an unrecorded effect.

## Decision

Authoritative state, journal facts, lifecycle changes, and directive outbox
entries are committed atomically before external dispatch. Effect attempts,
idempotency, retries, timers, result signals, and recovery are durable host
records. External exactly-once behavior is not assumed.

## Consequences

Every external operation is traceable to committed intent and may be delivered
at least once under a stable idempotency identity. Result admission occurs as a
new signal rather than direct mutation of an already committed turn.
