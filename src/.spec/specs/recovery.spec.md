# Retry, Timer Recovery, Replay, Hibernate, and Migration

```spec-meta
id: agent_wasm.recovery
kind: workflow
status: active
summary: Durable retry and timer scheduling, replay, hibernation, thaw, migration, and rollback.
surface:
  - "lib/agent_wasm/recovery/**/*.ex"
  - "test/agent_wasm/recovery/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Retry, Timer, Recovery, Replay, Hibernate, and Migration](../../../60-specification/28-retry-timer-recovery-replay-hibernate-and-migration.md)

## Requirements

```spec-requirements
- id: agent_wasm.recovery.delayed_work
  statement: Retry and timer records shall be durable, bounded, independently recoverable, and classified for transient, permanent, or operator intervention outcomes.
  priority: must
  stability: stable
- id: agent_wasm.recovery.replay_hibernate
  statement: Replay shall reconstruct pinned history without external effects, and hibernation shall deactivate only after verified snapshot and checkpoint durability.
  priority: must
  stability: stable
- id: agent_wasm.recovery.migration
  statement: Migration shall require authorization, compatible path, checkpoint, rollback state, atomic audit evidence, and safe failure behavior.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.recovery.implementation_frontier
  covers:
    - agent_wasm.recovery.delayed_work
    - agent_wasm.recovery.replay_hibernate
    - agent_wasm.recovery.migration
  reason: Durable retry, timers, replay, hibernation, and migration are not implemented.
```
