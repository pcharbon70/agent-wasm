# Effect Handlers, Attempts, and Result Signals

```spec-meta
id: agent_wasm.effects
kind: workflow
status: active
summary: Typed effect dispatch, attempt leases, idempotency, retries, outcomes, and causal result signals.
surface:
  - "lib/agent_wasm/effects/**/*.ex"
  - "test/agent_wasm/effects/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Effect Handlers, Attempts, Idempotency, and Result Signals](../../../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)

## Requirements

```spec-requirements
- id: agent_wasm.effects.handler_gate
  statement: Dispatch shall validate handler registration, trust, capability, schema, idempotency, payload, duration, and result bounds.
  priority: must
  stability: stable
- id: agent_wasm.effects.attempts
  statement: Every external dispatch shall use a durable leased attempt with stable request hash, outcome, timestamps, and retained evidence.
  priority: must
  stability: stable
- id: agent_wasm.effects.result_signal
  statement: Effect outcomes shall return as causally linked signals and shall not directly mutate an already committed reducer transition.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.effects.implementation_frontier
  covers:
    - agent_wasm.effects.handler_gate
    - agent_wasm.effects.attempts
    - agent_wasm.effects.result_signal
  reason: Effect handlers, attempt leases, idempotency, and result ingress are not implemented.
```
