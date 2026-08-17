# Threads, Checkpoints, Memory, Human Control, Quotas, and Credential Use

```spec-meta
id: agent_wasm.context_and_control
kind: contract
status: active
summary: Durable threads, projections, memory, approvals, quotas, use-only leases, custodians, and receipts.
surface:
  - "lib/agent_wasm/context_and_control/**/*.ex"
  - "test/agent_wasm/context_and_control/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.least_authority_credential_custody
  - agent_wasm.decision.user_owned_external_bindings
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md)
- [Phase 4 Integration Tests](../../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.context_and_control.context
  statement: Threads, messages, checkpoints, and working, episodic, semantic, and retrieved memory shall remain tenant-scoped projections with provenance, visibility, redaction, retention, and validation.
  priority: must
  stability: stable
- id: agent_wasm.context_and_control.human_resources
  statement: Approval routing, decisions, expiry, escalation, quota reservation, consumption, release, windows, burst, and reconciliation shall be durable and policy controlled.
  priority: must
  stability: stable
- id: agent_wasm.context_and_control.credential_use
  statement: Credential leases shall authorize typed use only, keep handles and credentials non-exportable, require independent custodian checks, and verify correlated receipts before result admission.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.context_and_control.implementation_frontier
  covers:
    - agent_wasm.context_and_control.context
    - agent_wasm.context_and_control.human_resources
    - agent_wasm.context_and_control.credential_use
  reason: Threads, checkpoints, memory, approvals, quotas, custodians, leases, and receipts are not implemented.
```
