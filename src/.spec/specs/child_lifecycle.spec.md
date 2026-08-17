# Child Lifecycle, Cancellation, Monitoring, and Restart

```spec-meta
id: agent_wasm.child_lifecycle
kind: workflow
status: active
summary: Durable child creation, lifecycle events, monitoring, cancellation propagation, hard stop, and restart policy.
surface:
  - "lib/agent_wasm/child_lifecycle/**/*.ex"
  - "test/agent_wasm/child_lifecycle/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Child Lifecycle, Cancellation, Monitoring, and Restart Policy](../../../60-specification/36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)

## Requirements

```spec-requirements
- id: agent_wasm.child_lifecycle.creation
  statement: Child admission shall atomically record logical identity, relationships, lifecycle policy, attenuated grants, journal intent, mailbox event, and evidence before activation.
  priority: must
  stability: stable
- id: agent_wasm.child_lifecycle.monitoring
  statement: Lifecycle events and monitor subscriptions shall be durable, ordered, replayable, bounded, and independent of live watch handles.
  priority: must
  stability: stable
- id: agent_wasm.child_lifecycle.cancellation_restart
  statement: Cancellation propagation, acknowledgement, hard stop, grant revocation, orphaning, and restart policy shall remain explicit and bounded.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.child_lifecycle.implementation_frontier
  covers:
    - agent_wasm.child_lifecycle.creation
    - agent_wasm.child_lifecycle.monitoring
    - agent_wasm.child_lifecycle.cancellation_restart
  reason: Child directives, monitoring, cancellation, hard stop, and restart supervision are not implemented.
```
