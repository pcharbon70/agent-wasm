# Framework Plugins and Lifecycle

```spec-meta
id: agent_wasm.plugins
kind: contract
status: active
summary: Plugin manifests, deterministic composition, user configuration, approvals, lifecycle, and trust tiers.
surface:
  - "lib/agent_wasm/plugins/**/*.ex"
  - "test/agent_wasm/plugins/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.user_owned_external_bindings
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Framework Plugin Manifests, Composition, and Lifecycle Hooks](../../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)

## Requirements

```spec-requirements
- id: agent_wasm.plugins.manifest
  statement: Plugin manifests shall declare immutable artifacts, actions, routes, namespaces, schemas, strategies, logical requirements, grants, and lifecycle ownership.
  priority: must
  stability: stable
- id: agent_wasm.plugins.composition
  statement: Composition shall use deterministic plugin ordering and reject name, route, namespace, schema, migration, capability, and lifecycle conflicts atomically.
  priority: must
  stability: stable
- id: agent_wasm.plugins.lifecycle
  statement: Install, validate, configure, approve, enable, disable, upgrade, migrate, rollback, and remove shall preserve user bindings, trust, and review gates.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.plugins.implementation_frontier
  covers:
    - agent_wasm.plugins.manifest
    - agent_wasm.plugins.composition
    - agent_wasm.plugins.lifecycle
  reason: Plugin registries, composition, configuration, approval, and lifecycle behavior are not implemented.
```
