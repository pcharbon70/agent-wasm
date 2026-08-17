---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.2.0"
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
  - credential-custody
aliases:
  - "M7-P4 Behavior And Integration"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration

## Status and authority

This chapter is a normative specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for threads, checkpoints,
memory, approvals, quotas, and credential leases, including approval requests,
quota enforcement, use-only credential dispatch, and receipt admission.

Version `0.2.0` replaces secret access through a host-held lease with typed,
use-only credential dispatch through a user-controlled custodian. Raw
credential access is not part of the lease lifecycle.

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
2. Emit an `approval_expired` diagnostic.
3. Emit an `approval.expired` evidence entry.
4. Apply the escalation policy (if configured).

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
2. Emit a `quota_exhausted` diagnostic.
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
The host MUST manage credential leases according to this metadata and use
lifecycle:

1. **Custodian registration**: The user registers an authenticated custodian
   and approved typed operation catalog. No provider or external-service
   credential is sent to the host.
2. **Handle enrollment**: The custodian issues a sender-constrained opaque
   handle reference and non-authority-bearing fingerprint.
3. **Lease creation**: The host records tenant, principal, purpose, operation,
   resource, expiry, custodian, and handle fingerprint metadata.
4. **Use authorization**: The host independently authorizes the originating
   domain capability and the effect worker's `CredentialUse`.
5. **Typed use**: The custodian validates and executes the scoped operation.
6. **Receipt admission**: The host verifies the custodian receipt before
   admitting the external result and usage.
7. **Renewal or rotation**: Lease metadata may be renewed; credential rotation
   remains inside the custodian.
8. **Expiry, suspension, revocation, or deletion**: New uses are denied and
   in-flight work is reconciled.

> **Normative definition.**
The host MUST enforce the following secret lease behaviors:

| Behavior | Description |
|----------|-------------|
| `active` | The lease may authorize a scoped typed use. |
| `suspended` | New uses are denied pending user or operator action. |
| `expired` | New uses are denied after the expiry time. |
| `revoked` | New uses are permanently denied. |
| `deleted` | Metadata is tombstoned subject to evidence retention. |

> **Normative definition.**
`non_exportable` is always `true`. The host and custodian MUST reject secret
read, reveal, unwrap, decrypt-for-caller, copy, export, bearer-token minting,
and authentication-header return operations with
`credential.use.export_forbidden`.
The host MUST NOT offer an API that returns the opaque handle to a guest,
plugin, adapter, log reader, or support operator.

> **Normative definition.**
Before accepting a `CredentialUseRequest`, the host MUST validate the lease
state and policy, and the custodian MUST independently validate:

- authenticated caller and tenant;
- principal, agent, and artifact digest;
- exactly one model or connector binding id and revision when present;
- handle, operation, and resource scope;
- canonical request digest;
- deadline and unique nonce;
- per-use and cumulative budget.

The custodian MUST reject any arbitrary origin, method, authentication header,
provider, model, connector, or resource substitution, digest change, replay,
or scope expansion.

> **Normative definition.**
For a valid use, the host MUST:

1. Atomically record the external effect before dispatch.
2. Emit `credential.use.requested` without handle or credential material.
3. Send the typed request through authenticated custodian transport.
4. Normalize bounded stream or result data.
5. Verify receipt correlation, digest, and signature or transport proof.
6. Emit `credential.use.completed` or `credential.use.denied`.
7. Admit the external result only after receipt verification.

> **Normative definition.**
When a credential lease is revoked, the host MUST:
1. Mark the lease as `revoked`.
2. Invalidate cached policy decisions and reject uses not yet dispatched.
3. Request cancellation or reconciliation of in-flight uses.
4. Emit `credential.lease.revoked` evidence.
5. Ensure that a later retry does not silently use another handle or custodian.

> **Normative definition.**
When a credential lease expires, the host MUST:
1. Mark the lease as `expired`.
2. Reject new uses with `credential.handle.expired`.
3. Reconcile any already-dispatched operation.
4. Emit `credential.lease.expired` evidence.

> **Normative definition.**
When a credential lease is deleted, the host MUST:
1. Mark the lease as `deleted`.
2. Reject new uses.
3. Retain a bounded tombstone for revocation and evidence consistency.
4. Emit `credential.lease.deleted` evidence.

> **Normative definition.**
In the `separated-credential-custody` profile, the host MUST route every
authenticated provider or connector operation through an `external-broker` or
`provider-workload-identity` custodian. Direct authenticated provider or
external-service egress from the host and Port processes MUST be denied. A `host-local` connection
MAY be used only after explicit user or operator opt-in and warning, and the
resulting deployment MUST NOT claim separated-custody conformance.

### Cross-chapter diagnostic precedence

For approval, quota, lease, handle, credential-use, receipt, custody-mode, and
credential-egress failures, the diagnostic codes in Section 44.3 are
canonical and take precedence over workflow or adapter wrappers. Dotted names
such as `approval.expired`, `quota.exhausted`, and
`credential.use.completed` are evidence types only and MUST NOT be emitted as
diagnostic codes unless Section 44.3 separately defines the same dotted code.

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

### 44.2.3 Credential custody mode

- **Permission**: The host MAY expose an explicitly opted-in `host-local`
  compatibility mode.
- **Recommendation**: End-user distributions SHOULD use
  `external-broker` or `provider-workload-identity`.
- **Permitted presentation**: The host MAY present custody mode, custodian
  health, and bounded receipt status to the authorized user.
- **Limit**: Credential leases are always non-exportable; `host-local` MUST
  NOT claim separated-custody conformance.

### 44.2.4 Quota reconciliation interval

- **Permission**: The host MAY configure the quota reconciliation interval.
- **Recommendation**: The host SHOULD reconcile quotas at least once per hour.
- **Permitted presentation**: The host MAY present the configured interval to the operator.
- **Limit**: The host MUST document the configured interval.

### 44.2.5 Custodian retry and reconciliation

> **Non-normative note.**

- **Internal mechanism**: Retry scheduling, backoff calculation, and
  receipt-reconciliation transport may vary only when they produce the same
  retry eligibility, timeout, receipt, and terminal outcomes.
- **Recommendation**: The host SHOULD reconcile uncertain outcomes before
  retry.
- **Permitted presentation**: The host MAY present bounded attempt and receipt
  summaries.
- **Limit**: Retry MUST preserve the original operation, resource, binding,
  handle, request digest, and budget while using a fresh nonce.

### 44.2.6 Diagnostic and evidence namespaces

- **Requirement**: Diagnostics use the exact Section 44.3 code; lifecycle
  evidence uses the exact dotted evidence type.
- **Permitted presentation**: The host MAY display both values together.
- **Limit**: Presentation MUST NOT translate one namespace into the other.
