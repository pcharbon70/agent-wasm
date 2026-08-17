# Sensors, Schedules, Timers, and Signal Ingress

```spec-meta
id: agent_wasm.ingress
kind: module
status: active
summary: Authenticated external event sources, schedules, timers, deduplication, and mailbox admission.
surface:
  - "lib/agent_wasm/ingress/**/*.ex"
  - "test/agent_wasm/ingress/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Sensors, Schedules, Timers, and External Signal Ingress](../../../60-specification/23-sensors-schedules-timers-and-external-signal-ingress.md)

## Requirements

```spec-requirements
- id: agent_wasm.ingress.unified_boundary
  statement: User, transport, sensor, schedule, and timer events shall pass authentication, resolution, schema validation, deduplication, and mailbox admission.
  priority: must
  stability: stable
- id: agent_wasm.ingress.scheduling
  statement: Schedule timezone, misfire, and jitter behavior shall be validated and deterministic for a schedule and fire time.
  priority: must
  stability: stable
- id: agent_wasm.ingress.timer
  statement: Timer identities shall be tenant scoped and timer signals shall not be admitted before their absolute due time.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.ingress.implementation_frontier
  covers:
    - agent_wasm.ingress.unified_boundary
    - agent_wasm.ingress.scheduling
    - agent_wasm.ingress.timer
  reason: Source adapters, schedule evaluation, timers, and ingress admission are not implemented.
```
