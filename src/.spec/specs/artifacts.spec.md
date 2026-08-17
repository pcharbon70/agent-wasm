# Artifacts, Manifests, Schemas, and Registries

```spec-meta
id: agent_wasm.artifacts
kind: contract
status: active
summary: Immutable artifact bundles, manifests, schemas, registry resolution, admission, and cache keys.
surface:
  - "lib/agent_wasm/artifacts/**/*.ex"
  - "test/agent_wasm/artifacts/**/*_test.exs"
decisions:
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.user_owned_external_bindings
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Agent Manifests, Artifacts, Schemas, and Registries](../../../60-specification/03-agent-manifests-artifacts-schemas-and-registries.md)

## Requirements

```spec-requirements
- id: agent_wasm.artifacts.immutable_bundle
  statement: Artifacts shall be immutable content-addressed Wasm bundles whose manifest, schemas, modules, provenance, and cache identity are verified.
  priority: must
  stability: stable
- id: agent_wasm.artifacts.portable_requirements
  statement: Manifests shall express logical model requirements without selecting providers, endpoints, connections, credentials, or custodians.
  priority: must
  stability: stable
- id: agent_wasm.artifacts.admission
  statement: Admission shall apply the specified integrity, digest, signature, feature, manifest, schema, and policy checks before availability.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.artifacts.implementation_frontier
  covers:
    - agent_wasm.artifacts.immutable_bundle
    - agent_wasm.artifacts.portable_requirements
    - agent_wasm.artifacts.admission
  reason: Artifact storage, admission, registry, and cache behavior are not implemented.
```
