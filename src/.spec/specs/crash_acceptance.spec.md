# Crash Injection and Durable Effects Acceptance

```spec-meta
id: agent_wasm.crash_acceptance
kind: workflow
status: active
summary: Crash-boundary invariants, restart reconstruction, ambiguous success, and Milestone 4 acceptance.
surface:
  - "test/agent_wasm/crash_acceptance/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Crash Injection, Durable Effects, and Milestone Acceptance](../../../60-specification/29-crash-injection-durable-effects-and-milestone-acceptance.md)

## Requirements

```spec-requirements
- id: agent_wasm.crash_acceptance.commit_invariant
  statement: No directive from an uncommitted turn shall dispatch and every eligible committed directive shall retain a recoverable outbox record.
  priority: must
  stability: stable
- id: agent_wasm.crash_acceptance.restart
  statement: Restart shall verify snapshots, replay journals, and restore outbox, timers, retries, hibernation, and migration state before normal work.
  priority: must
  stability: stable
- id: agent_wasm.crash_acceptance.matrix
  statement: Fault tests shall retain a crash matrix for every specified commit, dispatch, acknowledgement, and result-ingress boundary.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.crash_acceptance.implementation_frontier
  covers:
    - agent_wasm.crash_acceptance.commit_invariant
    - agent_wasm.crash_acceptance.restart
    - agent_wasm.crash_acceptance.matrix
  reason: Durable runtime and crash-injection infrastructure do not exist.
```
