---
title: "Agentic Workflows Provenance Safety And Milestone Acceptance Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-05
  - workflows
  - safety
  - provenance
  - milestone-acceptance
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
  - model-bindings
  - credential-custody
aliases:
  - "M7-P5 Failure Evidence And Operational Notes"
---

# Agentic Workflows Provenance Safety And Milestone Acceptance Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-05-agentic-workflows-provenance-safety-and-milestone-acceptance.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for agentic
workflows, provenance, safety, and milestone acceptance, including failure
outcomes, bounded diagnostics, evidence emission, implementation-defined
choices, deferred work, and results that would invalidate earlier milestone
assumptions.

Version `0.2.0` aligns workflow failures and evidence with logical model
bindings and canonical `credential.*` custody failures. It supersedes
workflow-level secret-access diagnostics.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
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
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md),
[Agentic Workflows Provenance Safety And Milestone Acceptance Contract And Data Model](45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md),
[Agentic Workflows Provenance Safety And Milestone Acceptance Behavior And Integration](45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md).

## 45.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST classify failure outcomes for agentic workflows, provenance,
safety, and milestone acceptance into the following categories:

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `malformed_workflow_input` | The workflow input is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_workflow_input` diagnostic. |
| `malformed_provenance_reference` | The provenance reference is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_provenance_reference` diagnostic. |
| `malformed_approval_request` | The approval request is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_approval_request` diagnostic. |
| `malformed_quota_request` | The quota request is malformed (invalid JSON, missing required fields, invalid field values). | Reject the input and emit a `malformed_quota_request` diagnostic. |
| `credential.lease.malformed` | Credential lease or handle metadata is malformed. | Reject without creating use state. |

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `incompatible_workflow_version` | The workflow version is incompatible with the host version. | Reject the input and emit an `incompatible_workflow_version` diagnostic. |
| `incompatible_provenance_reference_version` | The provenance reference version is incompatible with the host version. | Reject the input and emit an `incompatible_provenance_reference_version` diagnostic. |

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `conflicting_workflow_status` | The workflow status is conflicting with the current status. | Reject the input and emit a `conflicting_workflow_status` diagnostic. |
| `conflicting_provenance_reference` | The provenance reference is conflicting with existing references. | Reject the input and emit a `conflicting_provenance_reference` diagnostic. |
| `conflicting_approval_status` | The approval status is conflicting with the current status. | Reject the input and emit a `conflicting_approval_status` diagnostic. |
| `conflicting_quota_limit` | The quota limit is conflicting with the current limit. | Reject the input and emit a `conflicting_quota_limit` diagnostic. |
| `credential.lease.conflicting_expiry` | Credential lease revision or expiry conflicts. | Reject and require revision reload. |

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `unauthorized_workflow_access` | The agent is not authorized to access the workflow. | Reject the request and emit an `unauthorized_workflow_access` diagnostic. |
| `unauthorized_provenance_reference_access` | The agent is not authorized to access the provenance reference. | Reject the request and emit an `unauthorized_provenance_reference_access` diagnostic. |
| `unauthorized_approval_access` | The agent is not authorized to access the approval. | Reject the request and emit an `unauthorized_approval_access` diagnostic. |
| `unauthorized_quota_access` | The agent is not authorized to access the quota. | Reject the request and emit an `unauthorized_quota_access` diagnostic. |
| `credential.use.unauthorized` | Agent domain authority or effect-worker `CredentialUse` authority is absent. | Reject before custodian dispatch. |
| `model.request.unauthorized` | The agent is not authorized to use its logical model slot. | Reject before model dispatch. |
| `unauthorized_tool_access` | The agent is not authorized to access the tool. | Reject the request and emit an `unauthorized_tool_access` diagnostic. |

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `workflow_budget_exhausted` | The workflow budget is exhausted. | Terminate the workflow and emit a `workflow_budget_exhausted` diagnostic. |
| `quota_exhausted` | The quota is exhausted. | Reject the request and emit a `quota_exhausted` diagnostic. |
| `approval_expired` | The approval request has expired. | Reject the request and emit an `approval_expired` diagnostic. |
| `credential.handle.expired` | Credential lease or handle has expired. | Reject new use and reconcile in-flight work. |
| `model_stream_cancelled` | The model stream has been cancelled. | Terminate the model stream and emit a `model_stream_cancelled` diagnostic. |

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `workflow_store_unavailable` | The workflow store is unavailable. | Retry the request or reject and emit a `workflow_store_unavailable` diagnostic. |
| `provenance_reference_store_unavailable` | The provenance reference store is unavailable. | Retry the request or reject and emit a `provenance_reference_store_unavailable` diagnostic. |
| `approval_store_unavailable` | The approval store is unavailable. | Retry the request or reject and emit an `approval_store_unavailable` diagnostic. |
| `quota_store_unavailable` | The quota store is unavailable. | Retry the request or reject and emit a `quota_store_unavailable` diagnostic. |
| `credential.custodian.unavailable` | Pinned credential custodian is unavailable. | Retry only the same pinned workflow operation under bounded policy. |
| `model.connection.unavailable` | The pinned model connection is unavailable. | Retry only the same pinned workflow operation or require user reconfiguration. |
| `tool_unavailable` | The tool is unavailable. | Retry the request or reject and emit a `tool_unavailable` diagnostic. |

Model and credential failures MUST preserve the canonical diagnostic from
Sections 41 and 44. The workflow layer MUST NOT translate a binding, scope,
export, replay, receipt, or custodian failure into a generic workflow,
network, or tool error.

### Bounded diagnostics

> **Normative definition.**
Every diagnostic MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic_id` | The `DiagnosticId` of the diagnostic. | Host runtime |
| `diagnostic_code` | The diagnostic code (e.g., `malformed_workflow_input`, `workflow_budget_exhausted`). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-05`). | Host runtime |
| `section` | The section identifier (`5.1`, `5.2`, `5.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `workflow.input`, `quota.check`, `lease.expiry`). | Host runtime |
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
Every significant event related to agentic workflows, provenance, safety,
and milestone acceptance MUST emit bounded evidence.

> **Normative definition.**
Every evidence entry MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_id` | The `EvidenceId` of the evidence. | Host runtime |
| `evidence_type` | The evidence type (e.g., `workflow.created`, `workflow.budget_exhausted`, `hostile_output.detected`). | Host runtime |
| `workflow_id` | The `WorkflowId` of the workflow (if applicable). | Host runtime |
| `provenance_reference_id` | The `ReferenceId` of the provenance reference (if applicable). | Host runtime |
| `approval_id` | The `ApprovalId` of the approval (if applicable). | Host runtime |
| `quota_id` | The `QuotaId` of the quota (if applicable). | Host runtime |
| `lease_fingerprint` | Non-authority-bearing credential lease fingerprint (if applicable). | Host runtime |
| `credential_use_fingerprint` | Non-authority-bearing credential-use fingerprint (if applicable). | Host runtime |
| `model_binding_id` | Pinned model binding identity (if applicable). | Host runtime |
| `model_binding_revision` | Pinned model binding revision (if applicable). | Host runtime |
| `model_id` | The `ModelId` of the model (if applicable). | Host runtime |
| `tool_id` | The `ToolId` of the tool (if applicable). | Host runtime |
| `phase` | The phase identifier (`milestone-07`, `phase-05`). | Host runtime |
| `section` | The section identifier (`5.1`, `5.2`, `5.3`). | Host runtime |
| `contract` | The contract identifier (e.g., `45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model`). | Host runtime |
| `boundary` | The failed boundary (e.g., `workflow.input`, `quota.check`, `lease.expiry`). | Host runtime |
| `details` | Additional details about the evidence (bounded, no secrets). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the evidence. | Host clock |

> **Normative definition.**
Evidence types for agentic workflows, provenance, safety, and milestone
acceptance are defined as follows:

| Evidence type | Description |
|---------------|-------------|
| `workflow.created` | Emitted when a workflow is created. |
| `workflow.completed` | Emitted when a workflow is completed. |
| `workflow.failed` | Emitted when a workflow fails. |
| `workflow.cancelled` | Emitted when a workflow is cancelled. |
| `workflow.budget_exhausted` | Emitted when a workflow budget is exhausted. |
| `provenance_reference.created` | Emitted when a provenance reference is created. |
| `hostile_output.detected` | Emitted when hostile output is detected. |
| `hostile_output.rejected` | Emitted when hostile output is rejected. |
| `hostile_output.sanitized` | Emitted when hostile output is sanitized. |
| `hostile_output.admitted` | Emitted when hostile output is admitted. |
| `approval.requested` | Emitted when an approval is requested. |
| `approval.approved` | Emitted when an approval is approved. |
| `approval.rejected` | Emitted when an approval is rejected. |
| `approval.expired` | Emitted when an approval expires. |
| `quota.reserved` | Emitted when quota is reserved. |
| `quota.consumed` | Emitted when quota is consumed. |
| `quota.exhausted` | Emitted when quota is exhausted. |
| `credential.lease.created` | Emitted when a use-only credential lease is created. |
| `credential.lease.revoked` | Emitted when a credential lease is revoked. |
| `credential.lease.expired` | Emitted when a credential lease expires. |
| `credential.use.requested` | Emitted before typed custodian dispatch. |
| `credential.use.completed` | Emitted after valid receipt admission. |
| `credential.use.denied` | Emitted when policy or custodian denies a use. |
| `model_stream.started` | Emitted when a model stream starts. |
| `model_stream.completed` | Emitted when a model stream completes. |
| `model_stream.cancelled` | Emitted when a model stream is cancelled. |
| `model_stream.failed` | Emitted when a model stream fails. |
| `tool.invocation.started` | Emitted when a tool invocation starts. |
| `tool.invocation.completed` | Emitted when a tool invocation completes. |
| `tool.invocation.failed` | Emitted when a tool invocation fails. |

> **Normative definition.**
Evidence MUST be bounded. It MUST NOT expose:
- Credentials, authentication headers, opaque handle references, or
  transferable bearer values.
- Custodian endpoint or transport internals.
- Internal host implementation details.
- Other agents' data or state.

### Implementation-defined choices

> **Normative definition.**
The following implementation-defined choices MUST be documented by the host:

| Choice | Default | Documentation requirement |
|--------|---------|---------------------------|
| Workflow budget defaults | As stated in Section 45.2 | MUST be documented in host configuration. |
| Hostile output validation rules | Built-in rules only | MUST be documented in host configuration. |
| Deterministic resume behavior | Resume from last snapshot | MUST be documented in host configuration. |
| Provenance reference deduplication | Enabled | MUST be documented in host configuration. |
| Safety boundary configurability | Tenant-level | MUST be documented in host configuration. |
| Cost tracking granularity | Per workflow, per tenant, per agent | MUST be documented in host configuration. |
| Residual limitation reporting | Empirical data only | MUST be documented in host configuration. |

### Deferred work

> **Normative definition.**
The following work is deferred and MUST be tracked with priority and description. Items marked as "rejected" are not deferred — they were explicitly decided against based on the design rationale.

| Item | Description | Status | Rationale |
|------|-------------|--------|-----------|
| Custom workflow types | Support custom workflow types beyond the six defined (direct-model-response, structured-response, model-to-tool-continuation, retrieval-grounded-answer, code-execution, multi-agent-delegation). | Deferred (Medium) | Workflow types are internal implementation categories, not security boundaries. Six types cover the main agentic patterns. |
| Custom validation rules | Support a host-configurable declarative validation pipeline beyond built-in rules (schema, length, content filters). Rules should be expressed declaratively (regex patterns, schema extensions, policy scripts). | Deferred (Medium) | Built-in rules cover common cases. Custom rules require tenant-specific requirements (e.g., HIPAA, PII redaction). |
| Partial results on resume | Support partial results on deterministic resume, gated by workflow author opt-in (`partial_results_allowed: true/false`). | Deferred (Low) | Opt-in mechanism needed to avoid surfacing incomplete/misleading data. Financial workflows should not return partial results. |
| Quantified residual limitations | Quantify residual model-quality limitations (e.g., hallucination rate) and expose in operator dashboards as host-reported data. | Deferred (Low) | Quantified metrics are operational data, not normative thresholds. Framework cannot enforce model quality. |
| ML-based hostile output detection | Use ML-based approaches (e.g., toxicity classifiers) as advisory signals only. ML-flagged content should go to a review queue, not auto-block. | Deferred (Medium) | ML classifiers are probabilistic — false positives/negatives. Rule-based detection is deterministic and auditable. ML should be advisory, not enforcement. |
| External storage checkpointing | Support checkpointing to external storage (e.g., S3, GCS) for long-running workflows (multi-minute/hour-scale). | Deferred (Low) | Most workflows complete in seconds to minutes. External storage adds complexity (network calls, costs, consistency). Add as optional host feature, gated by config flag. |
| Budget grace periods | Support budget grace periods (allow in-progress operations to complete after exhaustion). | Rejected | Budget exhaustion is a hard stop for safety. Grace periods let tenants exceed quotas, defeating quota enforcement. Use approval workflow for resource increases. |
| Provenance reference cleanup | Support automatic cleanup of provenance references when answers are deleted. | Rejected | Provenance is audit evidence, not garbage. Deleting provenance breaks the audit chain. Implement tiered storage (hot vs. cold) with retention policies instead. |
| Benchmark workflows | Include benchmark workflows (e.g., standard test cases) in the workflow corpus for regression testing and performance measurement. | Deferred (Medium) | Useful for CI/CD and performance baselines. |
| Quantified provenance coverage | Quantify provenance coverage (e.g., "95% of answers have full provenance"). | Rejected | Provenance coverage is an operational metric, not a spec requirement. Mandating thresholds creates perverse incentives (skip provenance for edge cases to hit numbers). |

### Results that would invalidate earlier milestone assumptions

> **Normative definition.**
No results have been identified that invalidate earlier milestone assumptions.
If any result is identified, it MUST be documented and reported to the
milestone maintainer.

## Variability register

### 45.3.1 Diagnostic detail level

- **Permission**: The host MAY configure the level of detail in diagnostics.
- **Recommendation**: The host SHOULD provide sufficient detail for debugging.
- **Permitted presentation**: The host MAY present the configured detail level to the operator.
- **Limit**: The host MUST not expose secrets or other agents' data.

### 45.3.2 Evidence retention

- **Permission**: The host MAY configure the retention period for evidence.
- **Recommendation**: The host SHOULD retain evidence for at least 30 days.
- **Permitted presentation**: The host MAY present the configured retention period to the operator.
- **Limit**: The host MUST enforce tenant data isolation for evidence.

### 45.3.3 Workflow budget configurability

- **Permission**: The host MAY configure workflow budgets per tenant, with per-agent override support. Tenants are the natural billing and trust boundary — they own their agents and should control spend. Per-agent override lets a tenant run a "sandbox" agent with tighter limits while a "power" agent gets the full amount. Per-workflow configuration is not supported. Budget exhaustion is a hard stop for safety — grace periods would let a tenant exceed their quota, defeating the purpose of quota enforcement. If a tenant needs more resources, they should request a quota increase through the approval workflow.
- **Recommendation**: The host SHOULD support tenant-level configuration by default.
- **Permitted presentation**: The host MAY present the configured budgets to the operator.
- **Limit**: Budgets MUST be enforced at all times. Budget exhaustion is a hard stop, not a soft target.
