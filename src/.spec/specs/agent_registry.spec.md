# Agent Registry and Lifecycle

```spec-meta
id: agent_wasm.agent_registry
kind: module
status: active
summary: Logical agent records, activation, cancellation, completion, and disposable live projections.
surface:
  - "lib/agent_wasm/agent_registry/**/*.ex"
  - "test/agent_wasm/agent_registry/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Agent Registry, Activation, Cancellation, and Completion](../../../60-specification/22-agent-registry-activation-cancellation-and-completion.md)

## Requirements

```spec-requirements
- id: agent_wasm.agent_registry.logical_record
  statement: The registry shall own tenant-scoped logical identity, artifact, lifecycle policy, revision, and activation state independently of live execution.
  priority: must
  stability: stable
- id: agent_wasm.agent_registry.lifecycle
  statement: Create, resolve, activate, initialize, suspend, hibernate, thaw, cancel, complete, terminate, and inspect behavior shall enforce valid transitions.
  priority: must
  stability: stable
- id: agent_wasm.agent_registry.disposable_projection
  statement: Processes, Wasm instances, workers, sockets, and Port handles shall remain disposable and non-authoritative.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.agent_registry.implementation_frontier
  covers:
    - agent_wasm.agent_registry.logical_record
    - agent_wasm.agent_registry.lifecycle
    - agent_wasm.agent_registry.disposable_projection
  reason: Registry records, lifecycle transitions, and activation supervision are not implemented.
```
