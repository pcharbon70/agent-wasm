---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-01
  - model-requests
  - responses
  - streaming
  - usage
  - provider-neutral
  - failure-evidence
aliases:
  - "M7-P1 Failure Evidence And Operational Notes"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the failure evidence and operational notes for provider-neutral
model requests, responses, streaming, and usage, including failure outcomes,
bounded diagnostics, evidence emission, and implementation-defined choices.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
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
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md).

## 41.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The following failure outcomes are normative invariants that every
host implementation MUST handle correctly for provider-neutral model
requests, responses, streaming, and usage.
Each outcome describes a specific failure condition and the expected
host behavior.

#### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.malformed` | Model request with missing required fields. | Reject request; do NOT create partial request state. |
| `model.request.malformed-messages` | Model request with empty or invalid `messages` list. | Reject request; do NOT create partial request state. |
| `model.request.malformed-provider` | Model request with invalid `provider` format. | Reject request; do NOT create partial request state. |
| `model.request.malformed-model` | Model request with invalid `model` format. | Reject request; do NOT create partial request state. |
| `model.request.malformed-sampling` | Model request with invalid `sampling` controls. | Reject request; do NOT create partial request state. |
| `model.request.malformed-deadline` | Model request with invalid `deadline` timestamp. | Reject request; do NOT create partial request state. |
| `model.request.malformed-budget` | Model request with invalid `budget` value. | Reject request; do NOT create partial request state. |
| `model.response.malformed-text` | Response with invalid `text` field. | Reject response; do NOT create partial response state. |
| `model.response.malformed-structured` | Response with invalid `structured_value` field. | Reject response; do NOT create partial response state. |
| `model.response.malformed-usage` | Response with invalid `usage` metrics. | Reject response; do NOT create partial response state. |

> **Non-normative note.**
Malformed outcomes are caused by invalid input data.
The host MUST reject malformed input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable_provider` | Model request with unregistered `provider`. | Reject request; do NOT create partial request state. |
| `model.request.unavailable_model` | Model request with unavailable `model`. | Reject request; do NOT create partial request state. |
| `model.request.tool_call_mismatch` | Response with tool requests that do not match `tool_definitions`. | Reject response; do NOT create partial response state. |
| `model.request.invalid_structured_output` | Response with `structured_value` that does not conform to `structured_output_schema`. | Reject response; do NOT create partial response state. |

> **Non-normative note.**
Incompatible outcomes are caused by input data that is structurally valid
but semantically inconsistent with the model or provider.
The host MUST reject incompatible input without creating partial state,
which is consistent with the validation rules defined in
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md).

#### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.duplicate-id` | Two model requests with the same `request_id` submitted concurrently. | Reject second request; do NOT create partial request state. |
| `model.request.conflicting-cancellation` | Two cancellation requests for the same `request_id` submitted concurrently. | Reject second cancellation; do NOT create partial request state. |

> **Non-normative note.**
Conflicting outcomes are caused by concurrent or duplicate requests.
The host MUST reject conflicting input without creating partial state,
which is consistent with the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unauthorized` | Model request whose `agent_address` does not have the `model.request.create` capability. | Reject request; do NOT create partial request state. |
| `model.request.cross-tenant-tool` | Model request that grants cross-tenant tool access. | Reject request; do NOT create partial request state. |
| `model.request.cross-tenant-result` | Model request that grants cross-tenant result sharing. | Reject request; do NOT create partial request state. |

> **Non-normative note.**
Unauthorized outcomes are caused by principals that lack the required
capabilities.
The host MUST reject unauthorized requests without creating partial
state, which is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

#### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.quota_exhausted` | Agent's budget is insufficient to cover the request. | Reject request; do NOT create partial request state. |
| `model.request.exhausted-concurrency` | Host would exceed the implementation-defined maximum number of concurrent model requests. | Reject request; do NOT create partial request state. |
| `model.request.exhausted-stream` | Host would exceed the implementation-defined maximum number of concurrent streaming responses. | Reject request; do NOT create partial request state. |

> **Non-normative note.**
Exhausted outcomes are caused by resource limits.
The host MUST reject exhausted requests without creating partial state,
which is consistent with the resource limits defined in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md).

#### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable-provider` | Provider adapter is not active in the adapter registry. | Reject request; do NOT create partial request state. |
| `model.request.unavailable-model` | Model is not available from the provider. | Reject request; do NOT create partial request state. |
| `model.request.timeout` | Request exceeded the implementation-defined timeout. | Cancel request; do NOT create partial response state. |
| `model.request.late-response` | Response arrived after the `deadline`. | Accept response but mark as late in diagnostics. |

> **Non-normative note.**
Unavailable outcomes are caused by providers or models that are not active
or not available.
The host MUST reject unavailable requests without creating partial
state, which is consistent with the provider adapter contract defined in
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).

#### Safety outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.safety_refused` | Provider refused the request due to safety filters. | Reject response; emit safety metadata in diagnostics. |
| `model.request.content_filter` | Response text was filtered by the provider's content filters. | Accept response but mark as filtered in diagnostics. |

> **Non-normative note.**
Safety outcomes are caused by the provider's content filters.
The host MUST reject or accept the response based on the filter result
and emit safety metadata in diagnostics.

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
| `diagnostic` | The failure diagnostic code (e.g., `model.request.malformed`). | Host runtime. |
| `phase` | The phase that produced the diagnostic (`Phase 1`). | Host runtime. |
| `section` | The section that produced the diagnostic (e.g., `41.3`). | Host runtime. |
| `contract` | The contract that produced the diagnostic (e.g., `Provider-Neutral Model Requests Responses Streaming And Usage`). | Host runtime. |
| `profile` | The conformance profile that produced the diagnostic. | Host runtime. |
| `failed_boundary` | The failed boundary (e.g., `model.request.create`, `model.request.stream`, `model.request.cancel`). | Host runtime. |
| `timestamp` | The ISO 8601 timestamp of diagnostic emission. | Host clock. |
| `message` | A human-readable description of the failure. | Host runtime. |

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
| `evidence_type` | The evidence type (`model.request.created`, `model.request.completed`, `model.request.failed`, `model.request.cancelled`, `model.response.text_delta`, `model.response.tool_request_delta`, `model.usage.recorded`). | Host runtime. |
| `request_id` | The `request_id` of the model request. | Host runtime. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Host runtime. |
| `provider` | The provider adapter identifier. | Host runtime. |
| `model` | The model identifier. | Host runtime. |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock. |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime. |

> **Non-normative note.**
The evidence record format ensures that all model request events are auditable
and tamper-evident.
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
| Maximum concurrent requests | The maximum number of concurrent model requests. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent streams | The maximum number of concurrent streaming responses. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Request timeout | The maximum duration of a model request before timeout. | Must be longer than the maximum expected model response duration. Must be documented in the conformance profile. |
| Streaming buffer size | The maximum size of the streaming response buffer. | Must be at least 1 KB and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Usage recording interval | The interval between usage recordings (for long-running streams). | Must be at least 1 second and at most the implementation-defined maximum. Must be documented in the conformance profile. |

> **Non-normative note.**
The implementation-defined choices above provide flexibility for
different deployment scenarios while ensuring that constraints are
documented and auditable.
Host implementations MUST document these choices in the conformance
profile so that operators can understand the system's behavior.

### Deferred work

> **Normative definition.**
The following work is deferred to future phases or milestones:

1. **Multi-model parallelism**: Running multiple model requests in
   parallel across different providers is deferred to Milestone 8.
2. **Model routing**: Routing model requests to the optimal provider
   based on cost, latency, and quality is deferred to Milestone 8.
3. **Model caching**: Caching model responses for repeated requests is
   deferred to Milestone 8.
4. **Model fallback**: Automatically falling back to a different model
   or provider on failure is deferred to Milestone 8.

> **Non-normative note.**
The deferred work above is not within the scope of Phase 1 but may
be addressed in future phases.
Implementations MUST NOT implement deferred work without evidence from
the corresponding future phase.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 1 would invalidate an earlier milestone
assumption:

1. **Model requests bypass the durable journal**: If model requests
   bypass the durable journal, this would invalidate the assumption
   defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   that all state transitions are durable across host restarts.
2. **Model requests bypass the atomic commit protocol**: If model requests
   bypass the atomic commit protocol, this would invalidate the assumption
   defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   that all state transitions are atomic.
3. **Model requests allow cross-tenant authority leaks**: If model requests
   allow cross-tenant tool access or result sharing, this would invalidate
   the assumption defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant.
4. **Model requests require shared mutable guest state**: If model requests
   require shared mutable guest state, this would invalidate the assumption
   defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   that all state transitions are deterministic and replayable.

> **Non-normative note.**
These results would indicate a design flaw in Phase 1 and would require
a revision of the Phase 1 contracts before promotion to `status:
normative`.
Implementations MUST NOT deviate from the contracts defined in this
chapter without evidence from a corresponding revision.

### Cross-references and precedence

> **Non-normative note.**
This section's failure evidence and operational notes integrate with the
following earlier chapters:

1. For failure diagnostics: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of model-specific diagnostic format.
2. For evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of model-specific evidence record format.
3. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of model-specific capability enforcement.
4. For resource limits: this section takes precedence over
   [Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
   for questions of model-specific resource limits.
5. For provider adapters: this section takes precedence over
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
   for questions of model-specific adapter behavior.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
