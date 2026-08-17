# Telemetry, Audit, Redaction, Health, and Operator Actions

```spec-meta
id: agent_wasm.operations
kind: contract
status: active
summary: Metrics, tracing, structured logs, audit, redaction, sampling, retention, health, export, and operator controls.
surface:
  - "lib/agent_wasm/operations/**/*.ex"
  - "test/agent_wasm/operations/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.evidence_gated_conformance
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/48-telemetry-tracing-audit-redaction-health-and-operator-actions-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/48-telemetry-tracing-audit-redaction-health-and-operator-actions-failure-evidence-and-operational-notes.md)
- [Phase 3 Integration Tests](../../../60-specification/48-telemetry-tracing-audit-redaction-health-and-operator-actions-phase-3-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.operations.observability
  statement: Metrics, traces, structured logs, and audit records shall use bounded versioned schemas, causal correlation, controlled cardinality, retention, export, and tenant authorization.
  priority: must
  stability: stable
- id: agent_wasm.operations.redaction_health
  statement: Sensitive data shall be redacted before exposure, and liveness, readiness, dependencies, runtime profile, queue, storage, scheduler, and coordinator health shall remain accurate and bounded.
  priority: must
  stability: stable
- id: agent_wasm.operations.operator_actions
  statement: Drain, pause, resume, retry, cancel, quarantine, reconcile, rotate, and inspect actions shall be authorized, audited, idempotent, bounded, and safely observable.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.operations.implementation_frontier
  covers:
    - agent_wasm.operations.observability
    - agent_wasm.operations.redaction_health
    - agent_wasm.operations.operator_actions
  reason: Telemetry, audit, redaction, health, export, and operator-action systems are not implemented.
```
