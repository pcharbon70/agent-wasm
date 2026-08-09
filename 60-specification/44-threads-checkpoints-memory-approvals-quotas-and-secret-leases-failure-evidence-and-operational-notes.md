---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-04
  - threads
  - checkpoints
  - memory
  - approvals
  - quotas
  - secret-leases
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
aliases:
  - "M7-P4 Failure Evidence And Operational Notes"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for threads,
checkpoints, memory, approvals, quotas, and secret leases, including failure
outcomes, bounded diagnostics, evidence emission, implementation-defined
choices, deferred work, and results that would invalidate earlier milestone
assumptions.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md),
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md),
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md),
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md),
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md),
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md),
[Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md),
[Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model](37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md),
[Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration](37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md),
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md),
[Fan-Out Fan-In Delegation And Result Aggregation Phase 3 Integration Tests](37-fan-out-fan-in-delegation-and-result-aggregation-phase-3-integration-tests.md),
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md),
[Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes](38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md),
[Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests](38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Failure Evidence And Operational Notes](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-failure-evidence-and-operational-notes.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-phase-5-integration-tests.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests](41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md),
[Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md),
[Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md),
[Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md),
[Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests](42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md),
[Direct FSM Tool-Loop And Planning Strategies Contract And Data Model](43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md),
[Direct FSM Tool-Loop And Planning Strategies Behavior And Integration](43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md),
[Direct FSM Tool-Loop And Planning Strategies Failure Evidence And Operational Notes](43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md),
[Direct FSM Tool-Loop And Planning Strategies Phase 3 Integration Tests](43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md).

## 44.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST classify failure outcomes for threads, checkpoints, memory,
approvals, quotas, and secret leases into the following categories:

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_thread_input` | The thread input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_thread_input` diagnostic. |
| `malformed_message_input` | The message input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_message_input` diagnostic. |
| `malformed_checkpoint_input` | The checkpoint input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_checkpoint_input` diagnostic. |
| `malformed_memory_input` | The memory input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_memory_input` diagnostic. |
| `malformed_approval_input` | The approval input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_approval_input` diagnostic. |
| `malformed_quota_input` | The quota input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_quota_input` diagnostic. |
| `malformed_lease_input` | The lease input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_lease_input` diagnostic. |

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_thread_version` | The thread version is incompatible with the host version. | Reject the input and emit an `incompatible_thread_version` diagnostic. |
| `incompatible_checkpoint_version` | The checkpoint version is incompatible with the host version. | Reject the input and emit an `incompatible_checkpoint_version` diagnostic. |
| `incompatible_memory_version` | The memory version is incompatible with the host version. | Reject the input and emit an `incompatible_memory_version` diagnostic. |

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_thread_visibility` | The thread visibility is conflicting with the current visibility. | Reject the input and emit a `conflicting_thread_visibility` diagnostic. |
| `conflicting_quota_limit` | The quota limit is conflicting with the current limit. | Reject the input and emit a `conflicting_quota_limit` diagnostic. |
| `conflicting_lease_expiry` | The lease expiry is conflicting with the current expiry. | Reject the input and emit a `conflicting_lease_expiry` diagnostic. |

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_thread_access` | The agent is not authorized to access the thread. | Reject the request and emit an `unauthorized_thread_access` diagnostic. |
| `unauthorized_checkpoint_access` | The agent is not authorized to access the checkpoint. | Reject the request and emit an `unauthorized_checkpoint_access` diagnostic. |
| `unauthorized_memory_access` | The agent is not authorized to access the memory. | Reject the request and emit an `unauthorized_memory_access` diagnostic. |
| `unauthorized_approval_access` | The agent is not authorized to access the approval. | Reject the request and emit an `unauthorized_approval_access` diagnostic. |
| `unauthorized_quota_access` | The agent is not authorized to access the quota. | Reject the request and emit an `unauthorized_quota_access` diagnostic. |
| `unauthorized_lease_access` | The agent is not authorized to access the lease. | Reject the request and emit an `unauthorized_lease_access` diagnostic. |

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `quota_exhausted` | The quota is exhausted. | Reject the request and emit a `quota_exhausted` diagnostic. |
| `approval_expired` | The approval request has expired. | Reject the request and emit an `approval_expired` diagnostic. |
| `lease_expired` | The secret lease has expired. | Reject the request and emit a `lease_expired` diagnostic. |

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `thread_store_unavailable` | The thread store is unavailable. | Retry the request or reject and emit a `thread_store_unavailable` diagnostic. |
| `checkpoint_store_unavailable` | The checkpoint store is unavailable. | Retry the request or reject and emit a `checkpoint_store_unavailable` diagnostic. |
| `memory_store_unavailable` | The memory store is unavailable. | Retry the request or reject and emit a `memory_store_unavailable` diagnostic. |
| `approval_store_unavailable` | The approval store is unavailable. | Retry the request or reject and emit an `approval_store_unavailable` diagnostic. |
| `quota_store_unavailable` | The quota store is unavailable. | Retry the request or reject and emit a `quota_store_unavailable` diagnostic. |
| `lease_store_unavailable` | The lease store is unavailable. | Retry the request or reject and emit a `lease_store_unavailable` diagnostic. |

### Bounded diagnostics

> **Normative definition.**
Every diagnostic MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic_id` | The `DiagnosticId` of the diagnostic. | Host runtime |
| `diagnostic_code` | The diagnostic code (e.g., `malformed_thread_input`, `quota_exhausted`). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-04`). | Host runtime |
| `section` | The section identifier (`4.1`, `4.2`, `4.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `thread.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `profile` | The profile identifier (if applicable). | Host runtime |
| `message` | A human-readable message describing the diagnostic. | Host runtime |
| `details` | Additional details about the diagnostic (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the diagnostic. | Host clock |

> **Normative definition.**
Diagnostics MUST be bounded. They MUST NOT expose:
- Secrets or secret references.
- Internal host implementation details.
- Other agents' data or state.

> **Normative definition.**
The host MUST identify the phase, section, contract, and failed boundary in
every diagnostic.

### Evidence emission

> **Normative definition.**
Every significant event related to threads, checkpoints, memory, approvals,
quotas, and secret leases MUST emit bounded evidence.

> **Normative definition.**
Every evidence entry MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_id` | The `EvidenceId` of the evidence. | Host runtime |
| `evidence_type` | The evidence type (e.g., `thread.created`, `quota.reserved`). | Host runtime |
| `thread_id` | The `ThreadId` of the thread (if applicable). | Host runtime |
| `checkpoint_id` | The `CheckpointId` of the checkpoint (if applicable). | Host runtime |
| `memory_id` | The `MemoryId` of the memory (if applicable). | Host runtime |
| `approval_id` | The `ApprovalId` of the approval (if applicable). | Host runtime |
| `quota_id` | The `QuotaId` of the quota (if applicable). | Host runtime |
| `lease_id` | The `LeaseId` of the lease (if applicable). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-04`). | Host runtime |
| `section` | The section identifier (`4.1`, `4.2`, `4.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `thread.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `details` | Additional details about the evidence (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the evidence. | Host clock |

> **Normative definition.**
Evidence types for threads, checkpoints, memory, approvals, quotas, and secret
leases are defined as follows:

| Evidence type | Description |
|---------------|-------------|
| `thread.created` | Emitted when a thread is created. |
| `thread.archived` | Emitted when a thread is archived. |
| `thread.deleted` | Emitted when a thread is deleted. |
| `thread.message_added` | Emitted when a message is added to a thread. |
| `thread.participant_added` | Emitted when a participant is added to a thread. |
| `thread.participant_left` | Emitted when a participant leaves a thread. |
| `checkpoint.created` | Emitted when a checkpoint is created. |
| `checkpoint.archived` | Emitted when a checkpoint is archived. |
| `checkpoint.restored` | Emitted when a checkpoint is restored. |
| `checkpoint.deleted` | Emitted when a checkpoint is deleted. |
| `memory.created` | Emitted when memory is created. |
| `memory.archived` | Emitted when memory is archived. |
| `memory.promoted` | Emitted when memory is promoted. |
| `memory.deleted` | Emitted when memory is deleted. |
| `approval.requested` | Emitted when an approval is requested. |
| `approval.approved` | Emitted when an approval is approved. |
| `approval.rejected` | Emitted when an approval is rejected. |
| `approval.modified` | Emitted when an approval is modified. |
| `approval.delegated` | Emitted when an approval is delegated. |
| `approval.expired` | Emitted when an approval expires. |
| `approval.cancelled` | Emitted when an approval is cancelled. |
| `quota.reserved` | Emitted when quota is reserved. |
| `quota.consumed` | Emitted when quota is consumed. |
| `quota.released` | Emitted when quota is released. |
| `quota.reconciled` | Emitted when quota is reconciled. |
| `quota.exhausted` | Emitted when quota is exhausted. |
| `quota.suspended` | Emitted when quota is suspended. |
| `quota.deleted` | Emitted when quota is deleted. |
| `lease.created` | Emitted when a secret lease is created. |
| `lease.accessed` | Emitted when a secret lease is accessed. |
| `lease.renewed` | Emitted when a secret lease is renewed. |
| `lease.expired` | Emitted when a secret lease expires. |
| `lease.revoked` | Emitted when a secret lease is revoked. |
| `lease.deleted` | Emitted when a secret lease is deleted. |

> **Normative definition.**
Evidence MUST be bounded. It MUST NOT expose:
- Secrets or secret references.
- Internal host implementation details.
- Other agents' data or state.

### Implementation-defined choices

> **Normative definition.**
The following implementation-defined choices MUST be documented by the host:

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Thread visibility default | `private` | MUST be documented in host configuration. |
| Memory confidence defaults | As stated in Section 44.1 | MUST be documented in host configuration. |
| Checkpoint schema migration | Forward migration only | MUST be documented in host configuration. |
| Approval routing strategy | `any` | MUST be documented in host configuration. |
| Quota reconciliation interval | 1 hour | MUST be documented in host configuration. |
| Secret lease non-exportability | `true` | MUST be documented in host configuration. |
| Approval expiry default | 24 hours | MUST be documented in host configuration. |
| Memory retention default | `permanent` | MUST be documented in host configuration. |

### Deferred work

> **Normative definition.**
The following work is deferred and MUST be tracked with priority and description:

| Item | Description | Priority |
|------|-------------|----------|
| Parallel approvals | Support parallel approvals (e.g., require N out of M approvers). | Medium |
| Quota burst allowance | Support burst allowances (temporary overages). | Low |
| Secret lease rotation | Support secret rotation without invalidating leases. | Medium |
| Memory predictive promotion | Support predictive promotion based on usage patterns. | Low |
| Approval conditional decisions | Support conditional decisions (e.g., "approve if X"). | Medium |
| Quota predictive scaling | Support predictive scaling based on usage patterns. | Low |
| Secret lease auto-renewal | Support automatic renewal of secret leases. | Low |
| Approval auto-approval | Support auto-approval for low-risk requests. | Medium |
| Memory hierarchical scoping | Support hierarchical scoping for memory references. | Low |
| Quota shared pools | Support shared quota pools for multiple agents. | Medium |

### Results that would invalidate earlier milestone assumptions

> **Normative definition.**
No results have been identified that invalidate earlier milestone assumptions.
If any result is identified, it MUST be documented and reported to the
milestone maintainer.

## Variability register

### 44.3.1 Diagnostic detail level

- **Permission**: The host MAY configure the level of detail in diagnostics.
- **Recommendation**: The host SHOULD provide sufficient detail for debugging.
- **Permitted presentation**: The host MAY present the configured detail level to the operator.
- **Limit**: The host MUST not expose secrets or other agents' data.

### 44.3.2 Evidence retention

- **Permission**: The host MAY configure the retention period for evidence.
- **Recommendation**: The host SHOULD retain evidence for at least 30 days.
- **Permitted presentation**: The host MAY present the configured retention period to the operator.
- **Limit**: The host MUST enforce tenant data isolation for evidence.
