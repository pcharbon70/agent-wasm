---
title: "Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes"
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
  - failure-evidence
  - diagnostics
  - credential-custody
aliases:
  - "M7-P4 Failure Evidence And Operational Notes"
---

# Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for threads,
checkpoints, memory, approvals, quotas, and secret leases, including failure
outcomes, bounded diagnostics, evidence emission, profiled configuration,
deferred work, and results that would invalidate earlier milestone
assumptions.

Version `0.2.0` replaces host-held secret-access failures with credential
custodian, use-only scope, replay, receipt, and egress-boundary failures.
Legacy `malformed_lease_input`, `unauthorized_lease_access`,
`lease_expired`, and `lease_store_unavailable` codes are superseded by
the `credential.*` codes below.

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
| `credential.lease.malformed` | Lease or opaque-handle metadata is malformed. | Reject without creating lease or use state. |

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
| `credential.lease.conflicting_expiry` | Lease update races or conflicts with its current revision. | Reject and require revision reload. |

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_thread_access` | The agent is not authorized to access the thread. | Reject the request and emit an `unauthorized_thread_access` diagnostic. |
| `unauthorized_checkpoint_access` | The agent is not authorized to access the checkpoint. | Reject the request and emit an `unauthorized_checkpoint_access` diagnostic. |
| `unauthorized_memory_access` | The agent is not authorized to access the memory. | Reject the request and emit an `unauthorized_memory_access` diagnostic. |
| `unauthorized_approval_access` | The agent is not authorized to access the approval. | Reject the request and emit an `unauthorized_approval_access` diagnostic. |
| `unauthorized_quota_access` | The agent is not authorized to access the quota. | Reject the request and emit an `unauthorized_quota_access` diagnostic. |
| `credential.use.unauthorized` | Agent domain authority or effect-worker `CredentialUse` authority is absent. | Reject before custodian dispatch. |

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `quota_exhausted` | The quota is exhausted. | Reject the request and emit a `quota_exhausted` diagnostic. |
| `approval_expired` | The approval request has expired. | Reject the request and emit an `approval_expired` diagnostic. |
| `credential.handle.expired` | The credential lease or handle has expired. | Reject new use and reconcile in-flight work. |

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `thread_store_unavailable` | The thread store is unavailable. | Retry the request or reject and emit a `thread_store_unavailable` diagnostic. |
| `checkpoint_store_unavailable` | The checkpoint store is unavailable. | Retry the request or reject and emit a `checkpoint_store_unavailable` diagnostic. |
| `memory_store_unavailable` | The memory store is unavailable. | Retry the request or reject and emit a `memory_store_unavailable` diagnostic. |
| `approval_store_unavailable` | The approval store is unavailable. | Retry the request or reject and emit an `approval_store_unavailable` diagnostic. |
| `quota_store_unavailable` | The quota store is unavailable. | Retry the request or reject and emit a `quota_store_unavailable` diagnostic. |
| `credential.lease_store.unavailable` | Versioned lease metadata is unavailable. | Do not dispatch; retry under bounded policy. |

#### Credential custody outcomes

| Diagnostic | Cause | Host behavior |
| --- | --- | --- |
| `credential.handle.malformed` | Handle reference or fingerprint fails structural validation. | Reject before policy evaluation. |
| `credential.handle.revoked` | Lease or handle was revoked. | Reject new use and invalidate cached decisions. |
| `credential.custodian.unavailable` | Registered custodian cannot serve the request. | Preserve durable effect for bounded retry or fail by policy. |
| `credential.use.scope_mismatch` | Custodian, tenant, principal, agent, artifact, binding, operation, resource, digest, deadline, or budget differs from authorization. | Reject and emit security evidence. |
| `credential.use.export_forbidden` | Caller requests credential read, reveal, unwrap, export, bearer conversion, or authentication headers. | Reject as non-retryable security failure. |
| `credential.use.replay` | Nonce or completed use identity is replayed. | Reject without external dispatch. |
| `credential.receipt.invalid` | Receipt correlation, digest, signature, or transport proof is invalid. | Reject result admission and reconcile. |
| `credential.mode.host_local_unapproved` | Host-local custody is selected without explicit approval and warning. | Refuse activation. |
| `credential.egress.bypass` | Host or Port attempts authenticated provider or external-service egress outside the custodian. | Deny network operation and emit critical evidence. |

The underscore codes `approval_expired` and `quota_exhausted` are diagnostics.
The dotted names `approval.expired` and `quota.exhausted` are evidence types.
The host MUST preserve that distinction in APIs, logs, tests, and wrappers.

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
- Credentials, authentication headers, opaque handle references, or
  transferable bearer values.
- Custodian endpoint or transport internals.
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
| `lease_fingerprint` | Non-authority-bearing lease correlation fingerprint (if applicable). | Host runtime |
| `credential_use_fingerprint` | Non-authority-bearing use correlation fingerprint (if applicable). | Host runtime |
| `custodian_id` | Registered custodian identity (if applicable). | Host runtime |
| `model_binding_id` | Model binding identity (if applicable). | Host runtime |
| `model_binding_revision` | Model binding revision (if applicable). | Host runtime |
| `connector_binding_id` | Connector authentication binding identity (if applicable). | Host runtime |
| `connector_binding_revision` | Connector authentication binding revision (if applicable). | Host runtime |
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
| `credential.custodian.registered` | Emitted when a user registers a custodian connection. |
| `credential.lease.created` | Emitted when a use-only credential lease is created. |
| `credential.lease.renewed` | Emitted when lease metadata is renewed. |
| `credential.lease.expired` | Emitted when a credential lease expires. |
| `credential.lease.revoked` | Emitted when a credential lease is revoked. |
| `credential.lease.deleted` | Emitted when credential lease metadata is tombstoned. |
| `credential.use.requested` | Emitted before a typed request is sent to the custodian. |
| `credential.use.completed` | Emitted after a valid completion receipt is admitted. |
| `credential.use.denied` | Emitted when policy or custodian denies a use. |
| `credential.use.failed` | Emitted when a use fails or cannot be reconciled. |

> **Normative definition.**
Evidence MUST be bounded. It MUST NOT expose:
- Credentials, authentication headers, opaque handle references, or
  transferable bearer values.
- Custodian endpoint or transport internals.
- Internal host implementation details.
- Other agents' data or state.

### Configuration requirements

> **Normative definition.**
The following required defaults and deployment selections MUST be documented
in the conformance profile:

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Thread visibility default | `private` | MUST be documented in host configuration. |
| Memory confidence defaults | As stated in Section 44.1 | MUST be documented in host configuration. |
| Checkpoint schema migration | Forward migration only | MUST be documented in host configuration. |
| Approval routing strategy | `any` | MUST be documented in host configuration. |
| Quota reconciliation interval | 1 hour | MUST be documented in host configuration. |
| Credential custody mode | `external-broker` for end-user distribution | MUST document custody mode and conformance claim. |
| Approval expiry default | 24 hours | MUST be documented in host configuration. |
| Memory retention default | `permanent` | MUST be documented in host configuration. |

### Internal custodian mechanisms (non-normative)

Custodian transport identity, receipt proof, retry scheduling, and evidence
storage are internal mechanisms. They may vary only when they preserve sender
constraints, private-material boundaries, correlation, digest and scope
verification, replay rejection, tenant isolation, and every diagnostic and
terminal outcome specified by this chapter.

### Deferred work

> **Normative definition.**
The following work is deferred and MUST be tracked with priority and description:

| Item | Description | Priority |
|------|-------------|----------|
| Parallel approvals | Support parallel approvals (e.g., require N out of M approvers). | Medium |
| Quota burst allowance | Support burst allowances (temporary overages). | Low |
| Multi-custodian failover | Support explicit user-approved failover without runtime model or credential substitution. | Medium |
| Memory predictive promotion | Support predictive promotion based on usage patterns. | Low |
| Approval conditional decisions | Support conditional decisions (e.g., "approve if X"). | Medium |
| Quota predictive scaling | Support predictive scaling based on usage patterns. | Low |
| Secret lease auto-renewal | Support automatic renewal of secret leases. | Low |
| Approval auto-approval | Support auto-approval for low-risk requests. | Medium |
| Memory hierarchical scoping | Support hierarchical scoping for memory references. | Low |
| Quota shared pools | Support shared quota pools for multiple agents. | Medium |

### Results that would invalidate earlier milestone assumptions

> **Normative definition.**
Evidence that raw credentials must enter host or Port process memory for a
deployment claiming `separated-credential-custody` invalidates that claim and
requires a contract revision before promotion. Evidence that sender
constraints, scope checks, nonces, receipts, or direct-egress denial cannot be
enforced independently by the custodian also requires revision of the threat
model and this contract. Every such result MUST be reported to the milestone
maintainer.

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

### 44.3.3 Custodian and receipt detail

> **Non-normative note.**

- **Permission**: The host MAY present custodian identity, custody mode,
  binding revision, outcome, usage, and non-authority-bearing receipt
  fingerprints to the authorized user.
- **Recommendation**: The host SHOULD expose enough receipt detail for the user
  to reconcile external-service use independently.
- **Internal presentation**: Diagnostic and evidence field ordering, encoding,
  and layout may vary only when authorized users observe the same bounded
  fields, values, redactions, and receipt correlations.
- **Limit**: Presentation MUST NOT include credentials, opaque handles,
  authentication headers, external request bodies, or custodian transport
  internals.

### 44.3.4 Diagnostic and evidence namespaces

- **Requirement**: Use canonical underscore diagnostics and dotted lifecycle
  evidence exactly as defined above.
- **Permitted presentation**: A diagnostic MAY link to its resulting evidence
  entry by identity.
- **Limit**: Linking MUST NOT change either stable code.
