---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration"
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
  - behavior
  - integration
aliases:
  - "M7-P4 Behavior And Integration"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for threads, checkpoints,
memory, approvals, quotas, and secret leases, including approval requests,
quota enforcement, and secret lease lifecycle.

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
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md).

## 44.2 Behavior And Integration

### Approval requests

> **Normative definition.**
The host MUST handle approval requests according to the following flow:

1. **Request**: The agent submits an approval request.
2. **Validation**: The host validates the approval request.
3. **Routing**: The host routes the approval request to eligible approvers.
4. **Notification**: The host notifies eligible approvers.
5. **Decision**: The approver makes a decision.
6. **Signal**: The host emits a causally linked approval-result signal.
7. **Action**: The agent acts on the approval decision.

> **Normative definition.**
The host MUST validate the following approval request fields:

| Field | Validation |
|-------|------------|
| `request_type` | MUST be one of `action`, `plan`, `tool`, `code`, `memory`, `quota`. |
| `request_details` | MUST not be empty. |
| `eligible_approvers` | MUST contain at least one approver. |
| `decision_options` | MUST contain at least one option. |
| `expiry` | MUST be in the future (if specified). |

> **Normative definition.**
The host MUST route the approval request to all eligible approvers.
If multiple approvers are eligible, the host MAY use the following strategies:
- `any`: Any one approver can decide.
- `all`: All approvers must decide.
- `majority`: A majority of approvers must decide.

> **Normative definition.**
The host MUST notify eligible approvers of the approval request.
Notification MUST include:
- The approval request details.
- The decision options.
- The expiry timestamp.
- The escalation policy.

> **Normative definition.**
When an approver makes a decision, the host MUST emit a causally linked
approval-result signal.
The signal MUST include:
- `approval_id`: The `ApprovalId` of the approval request.
- `decision`: The decision made (`approve`, `reject`, `modify`, `delegate`).
- `decided_by`: The `TenantQualifiedAgentAddress` that decided.
- `decided_at`: The ISO 8601 timestamp of the decision.
- `causal_link`: The causal link to the approval request.

> **Normative definition.**
The host MUST handle the following approval behaviors:

| Behavior | Description |
|----------|-------------|
| `pending` | The approval request is pending a decision. |
| `approved` | The approval request is approved. |
| `rejected` | The approval request is rejected. |
| `modified` | The approval request is modified and resubmitted. |
| `delegated` | The approval request is delegated to another approver. |
| `expired` | The approval request has expired without a decision. |
| `cancelled` | The approval request is cancelled by the requester. |

> **Normative definition.**
If an approval request expires without a decision, the host MUST:
1. Mark the approval request as `expired`.
2. Emit an `approval.expired` diagnostic.
3. Apply the escalation policy (if configured).

### Quotas

> **Normative definition.**
The host MUST enforce quotas at the following points:

1. **Reservation**: Before reserving quota, the host checks if the quota has available capacity.
2. **Consumption**: Before consuming quota, the host checks if the quota has available capacity.
3. **Release**: After releasing quota, the host updates the quota usage.
4. **Reconciliation**: Periodically, the host reconciles quota usage.

> **Normative definition.**
The host MUST enforce the following quota behaviors:

| Behavior | Description |
|----------|-------------|
| `active` | The quota is active and can be used. |
| `exhausted` | The quota has reached its limit. |
| `suspended` | The quota is suspended (e.g., due to billing issues). |
| `deleted` | The quota is deleted. |

> **Normative definition.**
Quota windows are defined as follows:

| Window | Description |
|--------|-------------|
| `hourly` | Quota resets every hour. |
| `daily` | Quota resets every day. |
| `monthly` | Quota resets every month. |
| `lifetime` | Quota does not reset. |

> **Normative definition.**
When a quota is exhausted, the host MUST:
1. Mark the quota as `exhausted`.
2. Emit a `quota.exhausted` diagnostic.
3. Emit a `quota.exhausted` evidence entry.
4. Reject further reservations or consumption (unless burst allowance is configured).

> **Normative definition.**
When a quota is suspended, the host MUST:
1. Mark the quota as `suspended`.
2. Emit a `quota.suspended` evidence entry.
3. Reject further reservations or consumption.

> **Normative definition.**
When a quota is deleted, the host MUST:
1. Mark the quota as `deleted`.
2. Emit a `quota.deleted` evidence entry.
3. Invalidate any active reservations.

> **Normative definition.**
When a thread is archived, the host MUST emit a `thread.archived` evidence entry.

> **Normative definition.**
When a message is added to a thread, the host MUST emit a `thread.message_added` evidence entry.

> **Normative definition.**
When a participant is added to a thread, the host MUST emit a `thread.participant_added` evidence entry.

> **Normative definition.**
When a participant leaves a thread, the host MUST emit a `thread.participant_left` evidence entry.

> **Normative definition.**
When a checkpoint is archived, the host MUST emit a `checkpoint.archived` evidence entry.

> **Normative definition.**
When a checkpoint is deleted, the host MUST emit a `checkpoint.deleted` evidence entry.

> **Normative definition.**
When memory is archived, the host MUST emit a `memory.archived` evidence entry.

> **Normative definition.**
The host MUST perform periodic reconciliation of quota usage.
Reconciliation MUST:
- Compare expected usage with actual usage.
- Identify discrepancies.
- Log discrepancies for audit.
- Resolve discrepancies according to policy.

### Secret leases

> **Normative definition.**
The host MUST manage secret leases according to the following lifecycle:

1. **Creation**: The host creates a secret lease for a principal.
2. **Access**: The principal accesses the secret using the lease.
3. **Renewal**: The principal renews the lease before expiry.
4. **Expiry**: The lease expires and the principal loses access.
5. **Revocation**: The host revokes the lease before expiry.
6. **Deletion**: The lease is deleted.

> **Normative definition.**
The host MUST enforce the following secret lease behaviors:

| Behavior | Description |
|----------|-------------|
| `active` | The lease is active and the principal can access the secret. |
| `expired` | The lease has expired and the principal loses access. |
| `revoked` | The lease has been revoked and the principal loses access. |
| `deleted` | The lease is deleted. |

> **Normative definition.**
The host MUST enforce non-exportability for secret leases.
If `non_exportable` is true, the host MUST:
1. Prevent the secret from being exported from the host.
2. Log any export attempts.
3. Emit a `secret.export_attempt` diagnostic.

> **Normative definition.**
The host MUST log all secret lease operations for audit.
Operations include:
- Lease creation.
- Lease access.
- Lease renewal.
- Lease expiry.
- Lease revocation.
- Lease deletion.

> **Normative definition.**
When a secret lease is revoked, the host MUST:
1. Mark the lease as `revoked`.
2. Invalidate any active access using the lease.
3. Emit a `secret.lease_revoked` diagnostic.
4. Log the revocation for audit.

> **Normative definition.**
When a secret lease expires, the host MUST:
1. Mark the lease as `expired`.
2. Invalidate any active access using the lease.
3. Emit a `lease.expired` diagnostic.
4. Emit a `lease.expired` evidence entry.
5. Log the expiry for audit.

> **Normative definition.**
When a secret lease is deleted, the host MUST:
1. Mark the lease as `deleted`.
2. Invalidate any active access using the lease.
3. Emit a `lease.deleted` evidence entry.
4. Log the deletion for audit.

## Variability register

### 44.2.1 Approval routing strategy

- **Permission**: The host MAY configure the approval routing strategy.
- **Recommendation**: The host SHOULD support `any`, `all`, and `majority` strategies.
- **Permitted presentation**: The host MAY present the configured strategy to the operator.
- **Limit**: The host MUST document the configured strategy.

### 44.2.2 Quota burst allowance

- **Permission**: The host MAY configure burst allowance for quotas.
- **Recommendation**: The host SHOULD not configure burst allowance by default.
- **Permitted presentation**: The host MAY present the configured burst allowance to the operator.
- **Limit**: The host MUST document the configured burst allowance.

### 44.2.3 Secret lease non-exportability

- **Permission**: The host MAY configure non-exportability for secret leases.
- **Recommendation**: The host SHOULD default to `true` for non-exportability.
- **Permitted presentation**: The host MAY present the configured non-exportability to the operator.
- **Limit**: The host MUST document the configured non-exportability.

### 44.2.4 Quota reconciliation interval

- **Permission**: The host MAY configure the quota reconciliation interval.
- **Recommendation**: The host SHOULD reconcile quotas at least once per hour.
- **Permitted presentation**: The host MAY present the configured interval to the operator.
- **Limit**: The host MUST document the configured interval.
