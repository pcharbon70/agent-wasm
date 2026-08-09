---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model"
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
aliases:
  - "M7-P1 Contract And Data Model"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the contract and data model for provider-neutral model
requests, responses, streaming, and usage, including durable request
records, response normalization, and usage tracking.

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
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-phase-5-integration-tests.md).

## 41.1 Contract And Data Model

### Model request identity and provider constraints

> **Normative definition.**
A model request is a durable effect that represents a provider-neutral
request to an AI model.
The request captures the agent's intent, the model's constraints, and
the expected response format without exposing provider-specific details.

> **Normative definition.**
Every model request MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | A deterministic request identity derived from the agent address, turn sequence, and request payload hash. | Host runtime. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Agent. |
| `provider` | The provider adapter identifier (e.g., `openai`, `anthropic`, `local`). | Agent. |
| `model` | The model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet`). | Agent. |
| `messages` | A list of conversation messages (system, user, assistant). | Agent. |
| `structured_output_schema` | The JSON Schema for the expected structured output, if applicable. | Agent. |
| `tool_definitions` | The list of tool definitions available to the model. | Agent. |
| `sampling` | Sampling controls: `temperature`, `top_p`, `max_tokens`, `frequency_penalty`, `presence_penalty`. | Agent. |
| `deadline` | The ISO 8601 deadline by which the response MUST be received. | Agent. |
| `budget` | The maximum cost (in implementation-defined units) for this request. | Agent. |
| `trace_context` | The distributed tracing context for observability. | Host runtime. |
| `created_at` | The ISO 8601 timestamp of request creation. | Host clock. |
| `status` | The current status: `pending`, `streaming`, `completed`, `failed`, `cancelled`. | Host runtime. |

> **Non-normative note.**
The `request_id` is deterministic to enable idempotent retry: if the same
agent submits the same request payload, the host MUST produce the same
`request_id`.
This is consistent with the deterministic reducer semantics defined in
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

### Provider adapter registration and model resolution

> **Normative definition.**
Provider adapters are registered with the host and expose a common
interface for model requests.
The host resolves the `provider` and `model` fields of a model request
to a registered adapter.

> **Normative definition.**
Every provider adapter MUST include the following capabilities:

| Capability | Description |
|------------|-------------|
| `create_request` | Create a provider-specific request from the neutral request. |
| `stream_response` | Stream the provider-specific response as normalized events. |
| `cancel_request` | Cancel an in-flight request. |
| `check_status` | Check the status of an in-flight request. |

> **Non-normative note.**
Provider adapters are implemented as framework plugins as defined in
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).
Each adapter is isolated in its own tenant and subject to the capability
policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Response normalization

> **Normative definition.**
Provider-specific responses are normalized into a common format before
being recorded as durable effects.
The normalized response captures the response text, structured value,
tool requests, finish reason, usage, provider references, safety
metadata, and diagnostics.

> **Normative definition.**
Every normalized response MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `response_id` | A deterministic response identity derived from the `request_id` and response sequence number. | Host runtime. |
| `request_id` | The `request_id` of the associated model request. | Normalized from provider. |
| `text` | The response text, if any. | Normalized from provider. |
| `structured_value` | The structured value (parsed from `structured_output_schema`), if applicable. | Normalized from provider. |
| `tool_requests` | The list of tool requests made by the model. | Normalized from provider. |
| `finish_reason` | The finish reason: `stop`, `length`, `content_filter`, `tool_calls`, `error`. | Normalized from provider. |
| `usage` | The usage metrics: `prompt_tokens`, `completion_tokens`, `total_tokens`. | Normalized from provider. |
| `provider_response_id` | The provider-specific response identifier (for debugging). | Normalized from provider. |
| `provider_error` | The provider-specific error, if any. | Normalized from provider. |
| `safety_metadata` | Safety metadata: `content_filter_results`, `safety_categories`. | Normalized from provider. |
| `diagnostics` | Diagnostics: `latency_ms`, `retry_count`. | Host runtime. |
| `created_at` | The ISO 8601 timestamp of response creation. | Host clock. |

> **Non-normative note.**
Response normalization ensures that downstream components (such as
tool handlers and structured output validators) can work with provider-neutral
data without knowing the provider-specific format.
This is consistent with the framework plugin model defined in
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).

### Streaming normalization

> **Normative definition.**
Streaming responses are normalized into a sequence of events that include
the response text delta, tool request deltas, and finish event.
The host MUST emit a signal for each normalized streaming event.

> **Normative definition.**
Every streaming event MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `event_id` | A deterministic event identity derived from the `request_id` and event sequence number. | Host runtime. |
| `request_id` | The `request_id` of the associated model request. | Normalized from provider. |
| `event_type` | The event type: `text_delta`, `tool_request_delta`, `finish`. | Normalized from provider. |
| `text_delta` | The text delta (for `text_delta` events), if applicable. | Normalized from provider. |
| `tool_request_delta` | The tool request delta (for `tool_request_delta` events), if applicable. | Normalized from provider. |
| `finish_reason` | The finish reason (for `finish` events), if applicable. | Normalized from provider. |
| `usage` | The cumulative usage (for `finish` events), if applicable. | Normalized from provider. |
| `created_at` | The ISO 8601 timestamp of event creation. | Host clock. |

> **Non-normative note.**
Streaming events are bounded observations: they do NOT create durable
effects until the response is finalized.
This ensures that partial streaming data does not pollute the durable
journal and can be discarded on cancellation or failure.

### Usage tracking and budget enforcement

> **Normative definition.**
Usage tracking records the token counts and cost for each model request.
The host MUST enforce the `budget` constraint by rejecting requests
that would exceed the agent's remaining budget.

> **Normative definition.**
Every usage record MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `usage_id` | A deterministic usage identity derived from the `request_id`. | Host runtime. |
| `request_id` | The `request_id` of the associated model request. | Normalized from provider. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Host runtime. |
| `provider` | The provider adapter identifier. | Host runtime. |
| `model` | The model identifier. | Host runtime. |
| `prompt_tokens` | The number of prompt tokens used. | Normalized from provider. |
| `completion_tokens` | The number of completion tokens used. | Normalized from provider. |
| `total_tokens` | The total number of tokens used. | Normalized from provider. |
| `cost` | The cost in implementation-defined units. | Host runtime. |
| `currency` | The currency (e.g., `USD`). | Host runtime. |
| `created_at` | The ISO 8601 timestamp of usage recording. | Host clock. |

> **Non-normative note.**
Usage records are stored in the durable journal as defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
Budget enforcement is performed by the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Durable request and result records

> **Normative definition.**
Durable model request and result records are stored in the durable
journal.
The prompt and content payloads are stored separately with redacted
references to protect sensitive data.

> **Normative definition.**
The durable request record includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | The `request_id` of the model request. | Host runtime. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Agent. |
| `provider` | The provider adapter identifier. | Agent. |
| `model` | The model identifier. | Agent. |
| `messages` | The conversation messages (redacted reference). | Agent. |
| `structured_output_schema` | The JSON Schema for the expected structured output, if applicable. | Agent. |
| `tool_definitions` | The list of tool definitions available to the model. | Agent. |
| `sampling` | Sampling controls. | Agent. |
| `deadline` | The ISO 8601 deadline. | Agent. |
| `budget` | The maximum cost. | Agent. |
| `trace_context` | The distributed tracing context. | Host runtime. |
| `created_at` | The ISO 8601 timestamp of request creation. | Host clock. |
| `status` | The current status. | Host runtime. |

> **Normative definition.**
The durable result record includes the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `response_id` | The `response_id` of the normalized response. | Host runtime. |
| `request_id` | The `request_id` of the associated model request. | Host runtime. |
| `text` | The response text (redacted reference). | Normalized from provider. |
| `structured_value` | The structured value, if applicable. | Normalized from provider. |
| `tool_requests` | The list of tool requests made by the model. | Normalized from provider. |
| `finish_reason` | The finish reason. | Normalized from provider. |
| `usage` | The usage metrics. | Normalized from provider. |
| `provider_error` | The provider-specific error, if any. | Normalized from provider. |
| `safety_metadata` | Safety metadata. | Normalized from provider. |
| `diagnostics` | Diagnostics. | Host runtime. |
| `created_at` | The ISO 8601 timestamp of response creation. | Host clock. |

> **Non-normative note.**
Prompt and content payloads are stored with redacted references to
protect sensitive data.
The actual payloads are stored in a separate, access-controlled storage
layer as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
This ensures that durable records do not expose sensitive data to
unauthorized principals.

### Tool call mismatch handling

> **Normative definition.**
If the model returns tool requests that do not match the `tool_definitions`
provided in the request, the host MUST reject the response with
`model.request.tool_call_mismatch`.
The agent MUST be notified to update the tool definitions and retry.

> **Non-normative note.**
Tool call mismatch handling prevents the model from executing tools
that were not explicitly granted.
This is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Structured output validation

> **Normative definition.**
If a `structured_output_schema` is provided, the host MUST validate
the response's `structured_value` against the schema.
Invalid structured output MUST be rejected with `model.request.invalid_structured_output`.
The agent MUST be notified to fix the schema or retry with different sampling.

> **Non-normative note.**
Structured output validation ensures that the response conforms to
the expected format.
This is consistent with the schema validation defined in
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md).

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
This section's contract and data model integrate with the following
earlier chapters:

1. For model request validation: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of model-specific validation.
2. For durable storage: this section takes precedence over
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   for questions of model-specific storage.
3. For atomic commits: this section takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of model-specific atomic commits.
4. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of model-specific capability enforcement.
5. For security and audit: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of model-specific security.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
