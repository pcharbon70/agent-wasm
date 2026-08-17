# Threat Model, Principals, Trust, and Grants

```spec-meta
id: agent_wasm.threat_model
kind: policy
status: active
summary: Threat actors, protected assets, principal kinds, trust classes, grants, and separated custody.
surface:
  - "lib/agent_wasm/security/**/*.ex"
  - "test/agent_wasm/security/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Threat Model, Principals, Trust Classes, and Grant Vocabulary](../../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)

## Requirements

```spec-requirements
- id: agent_wasm.threat_model.assets
  statement: Security controls shall address the specified malicious guests, compromised components, confused deputies, tenants, dependencies, operators, co-tenants, and host threats.
  priority: must
  stability: stable
- id: agent_wasm.threat_model.principals_trust
  statement: Authentication shall bind the closed principal kinds and assign trust only through provenance, authorization, and tenant isolation.
  priority: must
  stability: stable
- id: agent_wasm.threat_model.grants
  statement: Grants shall independently bind principal, tenant, capability, resource, purpose, operation, constraints, expiry, and delegation without ambient authority.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.threat_model.implementation_frontier
  covers:
    - agent_wasm.threat_model.assets
    - agent_wasm.threat_model.principals_trust
    - agent_wasm.threat_model.grants
  reason: Principal authentication, trust assignment, grants, and threat controls are not implemented.
```
