# Stable Identities, Versions, Errors, and Limits

```spec-meta
id: agent_wasm.identities
kind: contract
status: active
summary: Canonical identities, compatibility negotiation, diagnostics, and implementation limits.
surface:
  - "lib/agent_wasm/identities/**/*.ex"
  - "test/agent_wasm/identities/**/*_test.exs"
decisions:
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Stable Identities, Versions, Errors, and Limits](../../../60-specification/02-stable-identities-versions-errors-and-limits.md)

## Requirements

```spec-requirements
- id: agent_wasm.identities.canonical
  statement: Tenant, principal, agent, artifact, invocation, signal, directive, attempt, and trace identities shall use their canonical stable representations and equality rules.
  priority: must
  stability: stable
- id: agent_wasm.identities.compatibility
  statement: Version negotiation shall enforce compatible major, minor, and patch behavior with stable incompatibility diagnostics.
  priority: must
  stability: stable
- id: agent_wasm.identities.limits
  statement: Resource-limit exhaustion shall be distinct from malformed input and shall disclose the applicable configured limit safely.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.identities.implementation_frontier
  covers:
    - agent_wasm.identities.canonical
    - agent_wasm.identities.compatibility
    - agent_wasm.identities.limits
  reason: Canonical identity, version, diagnostic, and limit modules are not implemented.
```
