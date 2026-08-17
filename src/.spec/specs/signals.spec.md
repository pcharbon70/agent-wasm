# Signals, Causality, Routing, and Delivery

```spec-meta
id: agent_wasm.signals
kind: contract
status: active
summary: Immutable signal envelopes, causality, authorization, routing, delivery, and deduplication.
surface:
  - "lib/agent_wasm/signals/**/*.ex"
  - "test/agent_wasm/signals/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.portable_guest_protocol
```

## Source Traceability

- [Signal Envelopes, Causality, Routing, and Delivery](../../../60-specification/10-signals-causality-routing-and-delivery.md)

## Requirements

```spec-requirements
- id: agent_wasm.signals.envelope
  statement: Signals shall be immutable tenant-scoped envelopes with stable source, subject, correlation, causation, delivery, trace, and timestamp data.
  priority: must
  stability: stable
- id: agent_wasm.signals.admission
  statement: The host shall authenticate, authorize, validate, deduplicate, and deterministically route signals before delivery.
  priority: must
  stability: stable
- id: agent_wasm.signals.delivery
  statement: Accepted, rejected, deferred, delivered, redelivered, coalesced, and dead-lettered outcomes shall remain explicit and bounded.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.signals.implementation_frontier
  covers:
    - agent_wasm.signals.envelope
    - agent_wasm.signals.admission
    - agent_wasm.signals.delivery
  reason: Signal schemas, routing, deduplication, and delivery tracking are not implemented.
```
