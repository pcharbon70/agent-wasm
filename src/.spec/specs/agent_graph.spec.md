# Agent Identity and Relationship Graph

```spec-meta
id: agent_wasm.agent_graph
kind: contract
status: active
summary: Tenant-qualified identity, relationships, ownership, dependency, visibility, and signal provenance.
surface:
  - "lib/agent_wasm/agent_graph/**/*.ex"
  - "test/agent_wasm/agent_graph/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Agent Identity, Addressing, Ownership, and Dependency Relations](../../../60-specification/35-agent-identity-addressing-ownership-and-dependency-relations.md)

## Requirements

```spec-requirements
- id: agent_wasm.agent_graph.addresses
  statement: External agent references shall use stable tenant-qualified logical addresses independent of process, engine, worker, socket, and node identity.
  priority: must
  stability: stable
- id: agent_wasm.agent_graph.relationships
  statement: Parent, child, owner, member, dependency, observer, delegate, and result-recipient relations shall enforce direction, consent, lifecycle, cardinality, and visibility.
  priority: must
  stability: stable
- id: agent_wasm.agent_graph.provenance
  statement: Relayed signals shall preserve validated origin, principal, correlation, causation, delegation chain, and return-address provenance within bounded depth.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.agent_graph.implementation_frontier
  covers:
    - agent_wasm.agent_graph.addresses
    - agent_wasm.agent_graph.relationships
    - agent_wasm.agent_graph.provenance
  reason: Agent address resolution, relationship storage, visibility, and provenance validation are not implemented.
```
