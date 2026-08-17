# Tool, Retrieval, Code, and Connector Runtime

```spec-meta
id: agent_wasm.tool_runtime
kind: workflow
status: active
summary: Tool catalogs, retrieval, sandboxed code, connectors, durable attempts, authenticated custody, and results.
surface:
  - "lib/agent_wasm/tool_runtime/**/*.ex"
  - "test/agent_wasm/tool_runtime/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.least_authority_credential_custody
  - agent_wasm.decision.user_owned_external_bindings
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md)
- [Phase 2 Integration Tests](../../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.tool_runtime.catalog
  statement: Tool descriptors and catalog queries shall validate schemas, provenance, capability, side-effect class, tenant scope, status, timeout, and result limits.
  priority: must
  stability: stable
- id: agent_wasm.tool_runtime.execution
  statement: Retrieval, code, and tool operations shall execute through bounded durable attempts with tenant isolation, provenance, cancellation, and normalized result signals.
  priority: must
  stability: stable
- id: agent_wasm.tool_runtime.connectors
  statement: Authenticated connector operations shall use user-owned bindings, independent credential-use authority, typed custodian dispatch, receipt verification, and direct-egress denial.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.tool_runtime.implementation_frontier
  covers:
    - agent_wasm.tool_runtime.catalog
    - agent_wasm.tool_runtime.execution
    - agent_wasm.tool_runtime.connectors
  reason: Tool catalog, retrieval, code sandbox, connector, custody, and result behavior are not implemented.
```
