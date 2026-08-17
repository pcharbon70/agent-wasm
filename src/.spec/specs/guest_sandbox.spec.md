# Synchronous Host Functions, WASI, and Tenant Isolation

```spec-meta
id: agent_wasm.guest_sandbox
kind: contract
status: active
summary: Bounded synchronous host functions, import namespaces, default-no-WASI, instance modes, and residue checks.
surface:
  - "lib/agent_wasm/guest_sandbox/**/*.ex"
  - "test/agent_wasm/guest_sandbox/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.least_authority_credential_custody
  - agent_wasm.decision.portable_guest_protocol
```

## Source Traceability

- [Synchronous Host Functions, WASI Restrictions, and Tenant Isolation](../../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)

## Requirements

```spec-requirements
- id: agent_wasm.guest_sandbox.host_functions
  statement: Synchronous host functions shall be deterministic, bounded, cancellable, retry-safe, typed, capability-gated, and tenant-aware.
  priority: must
  stability: stable
- id: agent_wasm.guest_sandbox.wasi
  statement: WASI shall be disabled by default and enabled only by an approved per-module request intersected with host policy.
  priority: must
  stability: stable
- id: agent_wasm.guest_sandbox.isolation
  statement: Fresh, reset, pooled, and agent-pinned modes shall preserve memory, state, capability, resource, and residue isolation at least as strongly as fresh execution.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.guest_sandbox.implementation_frontier
  covers:
    - agent_wasm.guest_sandbox.host_functions
    - agent_wasm.guest_sandbox.wasi
    - agent_wasm.guest_sandbox.isolation
  reason: Host-function registration, WASI policy, optimized instances, and residue testing are not implemented.
```
