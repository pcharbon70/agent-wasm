# Provider-Neutral Model Gateway

```spec-meta
id: agent_wasm.model_gateway
kind: workflow
status: active
summary: Logical model intent, user-owned bindings, pinned requests, streaming, usage, custody, and receipts.
surface:
  - "lib/agent_wasm/model_gateway/**/*.ex"
  - "test/agent_wasm/model_gateway/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.least_authority_credential_custody
  - agent_wasm.decision.user_owned_external_bindings
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md)
- [Phase 1 Integration Tests](../../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.model_gateway.intent_binding
  statement: Agents shall emit provider-neutral model intents while users own versioned concrete connection, provider, model, and custodian bindings outside artifacts.
  priority: must
  stability: stable
- id: agent_wasm.model_gateway.pinned_request
  statement: The host shall atomically materialize and pin request identity, binding revision, provider, model, digest, budget, quota, outbox, and idempotency across retry and replay.
  priority: must
  stability: stable
- id: agent_wasm.model_gateway.streaming_custody
  statement: Streaming, final response, usage, cancellation, credential use, and receipt admission shall remain bounded, normalized, tenant-safe, and credential-free.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.model_gateway.implementation_frontier
  covers:
    - agent_wasm.model_gateway.intent_binding
    - agent_wasm.model_gateway.pinned_request
    - agent_wasm.model_gateway.streaming_custody
  reason: Model catalogs, bindings, request materialization, adapters, custody dispatch, streaming, and fixtures are not implemented.
```
