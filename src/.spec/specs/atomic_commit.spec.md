# Atomic Commit and Directive Outbox

```spec-meta
id: agent_wasm.atomic_commit
kind: workflow
status: active
summary: Atomic snapshot, journal, lifecycle, and outbox commit with conflict recovery.
surface:
  - "lib/agent_wasm/atomic_commit/**/*.ex"
  - "test/agent_wasm/atomic_commit/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.host_owned_authority
```

## Source Traceability

- [Atomic State, Journal, and Directive-Outbox Commits](../../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)

## Requirements

```spec-requirements
- id: agent_wasm.atomic_commit.unit
  statement: Snapshot, journal, directive outbox, and lifecycle changes shall commit as one compare-and-commit unit against the expected revision.
  priority: must
  stability: stable
- id: agent_wasm.atomic_commit.outbox
  statement: No directive shall dispatch before its transition commits, and every outbox payload shall retain stable identity, hash, target, attempt, and state.
  priority: must
  stability: stable
- id: agent_wasm.atomic_commit.ambiguity
  statement: Ambiguous commit outcomes shall be resolved from durable revision, journal, and outbox identity without duplicate authoritative state.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.atomic_commit.implementation_frontier
  covers:
    - agent_wasm.atomic_commit.unit
    - agent_wasm.atomic_commit.outbox
    - agent_wasm.atomic_commit.ambiguity
  reason: Atomic commit and outbox storage are not implemented.
```
