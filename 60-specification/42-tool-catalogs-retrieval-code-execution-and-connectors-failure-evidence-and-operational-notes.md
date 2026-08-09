---
title: "Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-02
  - tool-catalogs
  - retrieval
  - code-execution
  - connectors
  - failure-evidence
  - diagnostics
  - implementation-defined-choices
aliases:
  - "M7-P2 Failure Evidence And Operational Notes"
---

# Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for tool catalogs,
retrieval, code execution, and connectors, including failure outcomes,
bounded diagnostics, evidence emission, and implementation-defined choices.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
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
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md),
[Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes](38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md),
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
[Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests](42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md).

## 42.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The following failure outcomes are normative invariants that every
host implementation MUST handle correctly for tool catalogs, retrieval,
code execution, and connectors.
Each outcome describes a specific failure condition and the expected
host behavior.

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.request.malformed` | Tool execution request with missing required fields. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-tool_id` | Tool execution request with invalid `tool_id` format. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-input` | Tool execution request with invalid `input` data. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-language` | Code execution request with invalid `language` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-code` | Code execution request with invalid `code` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-environment` | Code execution request with invalid `environment` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-query` | Retrieval request with missing or invalid `query` field. | Reject request; do NOT create partial execution state. |
| `tool.result.malformed-output` | Tool result with invalid `output` data. | Reject result; do NOT create partial result state. |
| `tool.result.malformed-usage` | Tool result with invalid `resource_usage` metrics. | Reject result; do NOT create partial result state. |

> **Non-normative note.**
Malformed outcomes are caused by invalid input data.
The host MUST reject malformed input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unknown_tool` | Tool execution request with unknown `tool_id`. | Reject request; do NOT create partial execution state. |
| `tool.execution.schema_mismatch` | Tool execution request input does not conform to the tool's `input_schema`. | Reject request; do NOT create partial execution state. |
| `tool.execution.result_schema_mismatch` | Tool result does not conform to the tool's `output_schema`. | Reject result; do NOT create partial result state. |
| `tool.execution.stale_catalog` | Tool descriptor version does not match the cached catalog version. | Reject request; do NOT create partial execution state. |

> **Non-normative note.**
Incompatible outcomes are caused by input data that is structurally valid
but semantically inconsistent with the tool or catalog.
The host MUST reject incompatible input without creating partial state,
which is consistent with the validation rules defined in
[Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md).

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.duplicate-id` | Two tool execution requests with the same `request_id` submitted concurrently. | Reject second request; do NOT create partial execution state. |
| `tool.execution.conflicting-cancellation` | Two cancellation requests for the same `request_id` submitted concurrently. | Reject second cancellation; do NOT create partial execution state. |

> **Non-normative note.**
Conflicting outcomes are caused by concurrent or duplicate requests.
The host MUST reject conflicting input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.denied_capability` | Tool execution request whose `agent_address` does not have the required capability. | Reject request; do NOT create partial execution state. |
| `tool.execution.cross-tenant-data` | Tool execution request that accesses cross-tenant data. | Reject request; do NOT create partial execution state. |
| `tool.execution.unauthorized_connector` | Tool execution request using an unauthorized connector. | Reject request; do NOT create partial execution state. |

> **Non-normative note.**
Unauthorized outcomes are caused by principals that lack the required
capabilities.
The host MUST reject unauthorized requests without creating partial
state, which is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.quota_exhausted` | Agent's capability budget is insufficient to cover the request. | Reject request; do NOT create partial execution state. |
| `tool.execution.exhausted-concurrency` | Host would exceed the implementation-defined maximum number of concurrent tool executions. | Reject request; do NOT create partial execution state. |
| `tool.execution.exhausted-code` | Host would exceed the implementation-defined maximum number of concurrent code executions. | Reject request; do NOT create partial execution state. |
| `tool.execution.timeout` | Tool execution exceeded the `timeout_ms` limit. | Cancel execution; do NOT create partial result state. |

> **Non-normative note.**
Exhausted outcomes are caused by resource limits.
The host MUST reject exhausted requests without creating partial state,
which is consistent with the resource limits defined in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unavailable_tool` | Tool is not active in the framework plugin registry. | Reject request; do NOT create partial execution state. |
| `tool.execution.unavailable_connector` | Connector is not active in the connector registry. | Reject request; do NOT create partial execution state. |
| `tool.execution.sandbox_failure` | Code execution failed due to sandbox restrictions. | Cancel execution; do NOT create partial result state. |
| `tool.execution.connector_failure` | Connector failed to execute the tool. | Cancel execution; do NOT create partial result state. |

> **Non-normative note.**
Unavailable outcomes are caused by tools or connectors that are not active
or not available.
The host MUST reject unavailable requests without creating partial
state, which is consistent with the framework plugin contract defined
in [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).

#### Safety outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unsafe_output` | Tool result contains content that fails the safety filter. | Reject result; emit safety metadata in diagnostics. |
| `tool.execution.provenance_loss` | Tool result is missing required provenance evidence. | Reject result; emit provenance warning in diagnostics. |

> **Non-normative note.**
Safety outcomes are caused by the tool returning content that violates
safety policies or missing required provenance evidence.
The host MUST reject the result and emit safety metadata or provenance
warnings in diagnostics.

### Bounded diagnostics and evidence

> **Normative definition.**
The host MUST emit bounded diagnostics and evidence for every failure
outcome.
Diagnostics identify the phase contract, profile, and failed boundary
without exposing secrets.
Evidence is recorded in the durable audit log as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Every diagnostic MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic` | The failure diagnostic code (e.g., `tool.execution.malformed`). | Host runtime |
| `phase` | The phase that produced the diagnostic (`Phase 2`). | Host runtime |
| `section` | The section that produced the diagnostic (e.g., `42.3`). | Host runtime |
| `contract` | The contract that produced the diagnostic (e.g., `Tool Catalogs Retrieval Code Execution And Connectors`). | Host runtime |
| `profile` | The conformance profile that produced the diagnostic. | Host runtime |
| `failed_boundary` | The failed boundary (e.g., `tool.execution.create`, `tool.execution.execute`, `tool.execution.cancel`). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of diagnostic emission. | Host clock |
| `message` | A human-readable description of the failure. | Host runtime |

> **Non-normative note.**
The bounded diagnostic format ensures that diagnostics are consistent,
auditable, and actionable.
The `phase`, `section`, `contract`, `profile`, and `failed_boundary`
fields enable operators to quickly identify the source and context
of a failure.
The `message` field provides a human-readable description that enables
operators to understand the failure and take corrective action.

> **Normative definition.**
Every evidence record MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_type` | The evidence type (`tool.execution.requested`, `tool.execution.completed`, `tool.execution.failed`, `tool.execution.cancelled`, `tool.execution.result`, `retrieval.requested`, `retrieval.completed`, `retrieval.failed`, `code.requested`, `code.completed`, `code.failed`, `code.cancelled`). | Host runtime |
| `request_id` | The `request_id` of the tool/retrieval/code execution request. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Host runtime |
| `tool_id` | The `tool_id` of the tool executed (for tool executions). | Host runtime |
| `language` | The `language` of the code executed (for code executions). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime |

> **Non-normative note.**
The evidence record format ensures that all tool/retrieval/code execution
events are auditable and tamper-evident.
The `evidence_digest` field enables downstream systems to verify that
the evidence record has not been tampered with after creation.
This is consistent with the provenance and audit contract defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Implementation-defined choices

> **Normative definition.**
The following implementation-defined choices are documented by this section.
Host implementations MUST document these choices in the conformance
profile.

| Choice | Description | Constraint |
|--------|-------------|------------|
| Maximum concurrent tool executions | The maximum number of concurrent tool executions. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent code executions | The maximum number of concurrent code executions. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent retrieval requests | The maximum number of concurrent retrieval requests. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Tool execution timeout | The default maximum duration of a tool execution before timeout. | Must be longer than the maximum expected tool execution duration. Must be documented in the conformance profile. |
| Code execution timeout | The default maximum duration of a code execution before timeout. | Must be longer than the maximum expected code execution duration. Must be documented in the conformance profile. |
| Retrieval timeout | The default maximum duration of a retrieval request before timeout. | Must be longer than the maximum expected retrieval duration. Must be documented in the conformance profile. |
| Sandbox memory limit | The maximum memory for code execution sandboxes. | Must be at least 64 MB and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Sandbox network access | Whether code execution sandboxes have network access. | Must be configurable per tool or globally. Must be documented in the conformance profile. |

> **Non-normative note.**
The implementation-defined choices above provide flexibility for
different deployment scenarios while ensuring that constraints are
documented and auditable.
Host implementations MUST document these choices in the conformance
profile so that operators can understand the system's behavior.

### Deferred work

> **Normative definition.**
The following work is deferred to future phases or milestones:

1. **Tool composition**: Composing multiple tools into a single compound
   tool is deferred to Milestone 8.
2. **Tool versioning**: Automatic tool version upgrades and rollback is
   deferred to Milestone 8.
3. **Tool marketplace**: A marketplace for third-party tools is deferred
   to Milestone 9.
4. **Tool analytics**: Analytics and metrics for tool usage is deferred
   to Milestone 9.
5. **Connector authentication caching**: Caching connector authentication
   tokens is deferred to Milestone 8.

> **Non-normative note.**
The deferred work items are not within the scope of Phase 2 but may
be addressed in future phases.
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 2 would invalidate an earlier milestone
assumption:

1. **Tools bypass the durable journal**: If tools bypass the durable
   journal, this would invalidate the assumption defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   that all state transitions are durable across host restarts.
2. **Tools bypass the atomic commit protocol**: If tools bypass the
   atomic commit protocol, this would invalidate the assumption defined
   in [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   that all state transitions are atomic.
3. **Tools allow cross-tenant authority leaks**: If tools allow cross-tenant
   data access or result sharing, this would invalidate the assumption defined
   in [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant.
4. **Tools require shared mutable guest state**: If tools require shared
   mutable guest state, this would invalidate the assumption defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   that all state transitions are deterministic and replayable.

> **Non-normative note.**
These results would indicate a design flaw in Phase 2 and would require
a revision of the Phase 2 contracts before promotion to `status:
normative`.
Implementations MUST NOT deviate from the contracts defined in this
chapter without evidence from a corresponding revision.

### Cross-references and precedence

> **Non-normative note.**
This section's failure evidence and operational notes integrate with the
following earlier chapters:

1. For failure diagnostics: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of tool-specific diagnostic format.
2. For evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of tool-specific evidence record format.
3. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of tool-specific capability enforcement.
4. For resource limits: this section takes precedence over
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   for questions of tool-specific resource limits.
5. For framework plugins: this section takes precedence over
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
   for questions of tool-specific plugin behavior.
6. Where both sections are applicable and agree, they are mutually
    reinforcing.

## Variability register

The following table lists every implementation-defined choice,
non-normative disposition, and permitted presentation documented in this
chapter.

| Item | Location | Nature | Constraint |
|------|----------|--------|------------|
| Maximum concurrent tool executions | Section 42.3 | MAY | Must be at least 1 and at most the implementation-defined maximum. Documented in conformance profile. |
| Maximum concurrent code executions | Section 42.3 | MAY | Must be at least 1 and at most the implementation-defined maximum. Documented in conformance profile. |
| Maximum concurrent retrieval requests | Section 42.3 | MAY | Must be at least 1 and at most the implementation-defined maximum. Documented in conformance profile. |
| Tool execution timeout | Section 42.3 | MAY | Must be at least the minimum execution duration. Documented in conformance profile. |
| Code execution timeout | Section 42.3 | MAY | Must be at least the minimum execution duration. Documented in conformance profile. |
| Retrieval timeout | Section 42.3 | MAY | Must be at least the minimum execution duration. Documented in conformance profile. |
| Sandbox memory limit | Section 42.3 | MAY | Must be at least 64 MB and at most the implementation-defined maximum. Documented in conformance profile. |
| Sandbox network access | Section 42.3 | MAY | Must be configurable per tool or globally. Documented in conformance profile. |
| Diagnostic message format | Section 42.3 | MAY | Must include all required fields. Free-text portion is informational. |
| Evidence record field order | Section 42.3 | SHOULD | Must include all required fields. Order is informational. |
| Evidence record hash algorithm | Section 42.3 | MAY | Must be deterministic. Documented in conformance profile. |
| Integration test ordering | Section 42.4 | MAY | Must cover all required scenarios. Order is informational. |
| Cross-milestone fixture selection | Section 42.4 | MUST | Must include all fixtures listed in section 42.4.4. |
