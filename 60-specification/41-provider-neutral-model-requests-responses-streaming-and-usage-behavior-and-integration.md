---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration"
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
  - behavior
  - integration
aliases:
  - "M7-P1 Behavior And Integration"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for provider-neutral
model requests, responses, streaming, and usage, including provider
adapter behavior, signal conversion, and outcome definitions.

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
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md).

## 41.2 Behavior And Integration

### Provider adapter behavior

> **Normative definition.**
Provider adapters behave as framework plugins: they are isolated in
their own tenant, subject to the capability policy, and communicate
with the host through well-defined interfaces.

> **Normative definition.**
When the host receives a model request, it MUST:

1. **Validate the request**: The host MUST validate the request against
   the schema defined in section 41.1. Invalid requests MUST be rejected
   with the appropriate diagnostic.
2. **Resolve the provider**: The host MUST resolve the `provider` field
   to a registered adapter. Unregistered providers MUST be rejected with
   `model.request.unavailable_provider`.
3. **Check the budget**: The host MUST check that the agent's remaining
   budget is sufficient to cover the request. Insufficient budget MUST
   be rejected with `model.request.quota_exhausted`.
4. **Create the adapter request**: The host MUST call the adapter's
   `create_request` capability to create a provider-specific request.
5. **Start streaming**: The host MUST call the adapter's `stream_response`
   capability to start streaming the response.
6. **Normalize events**: The host MUST normalize each streaming event
   and emit a signal for each event.
7. **Finalize the response**: When the adapter signals completion or
   failure, the host MUST finalize the response and emit a signal.
8. **Record usage**: The host MUST record usage for the request and
   update the agent's budget.

> **Non-normative note.**
Provider adapter behavior is designed to be fault-tolerant: if an adapter
crashes or becomes unresponsive, the host MUST cancel the in-flight
request and retry with a different adapter if available.
This is consistent with the retry mechanism defined in
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).

### Capability mapping

> **Normative definition.**
Provider adapters are granted capabilities by the host based on the
agent's grants and the request's `budget`.
The host MUST map the agent's grants to adapter capabilities using the
following rules:

| Agent Grant | Adapter Capability |
|-------------|-------------------|
| `model.request.create` | `create_request` |
| `model.request.stream` | `stream_response` |
| `model.request.cancel` | `cancel_request` |
| `model.request.status` | `check_status` |
| `model.usage.read` | `record_usage` |

> **Non-normative note.**
Capability mapping ensures that adapters only have access to the
resources that the agent has been granted.
This is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Model resolution

> **Normative definition.**
The host MUST resolve the `model` field of a model request to a
provider-specific model identifier.
The resolution process is:

1. The host checks the adapter's registered models for a match.
2. If no match is found, the host returns `model.request.unavailable_model`.
3. If a match is found, the host returns the provider-specific model
   identifier.

> **Non-normative note.**
Model resolution allows the host to abstract provider-specific model
identifiers.
Agents can use portable model names (e.g., `gpt-4o`, `claude-3-5-sonnet`)
without knowing the provider-specific identifiers.
This is consistent with the provider adapter model defined in section 41.1.

### Streaming normalization

> **Normative definition.**
Streaming normalization converts provider-specific streaming events
into a common format.
The host MUST normalize the following event types:

| Provider Event | Normalized Event |
|----------------|------------------|
| `text_delta` | `text_delta` |
| `tool_call_delta` | `tool_request_delta` |
| `finish` | `finish` |
| `error` | `finish` (with `finish_reason: error`) |

> **Non-normative note.**
Streaming normalization ensures that downstream components can work with
provider-neutral streaming data.
This is consistent with the response normalization defined in section 41.1.

### Cancellation behavior

> **Normative definition.**
When a model request is cancelled, the host MUST:

1. Call the adapter's `cancel_request` capability.
2. Mark the request as `cancelled` in the durable journal.
3. Emit a `model.request.cancelled` signal.
4. Release any resources associated with the request.

> **Non-normative note.**
Cancellation is best-effort: if the adapter does not support cancellation,
the host MUST wait for the request to complete or timeout.
This is consistent with the cancellation behavior defined in
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).

### Retry classification

> **Normative definition.**
The host MUST classify failures into retryable and non-retryable categories:

| Failure Type | Retryable |
|--------------|-----------|
| `model.request.unavailable_provider` | No |
| `model.request.unavailable_model` | No |
| `model.request.quota_exhausted` | No |
| `model.request.tool_call_mismatch` | Yes (after agent updates tool definitions) |
| `model.request.invalid_structured_output` | Yes (after agent updates schema) |
| `model.request.safety_refused` | No |
| `model.request.timeout` | Yes |
| `model.request.late_response` | Yes |
| `adapter.error` | Yes |
| `network.error` | Yes |

> **Non-normative note.**
Retry classification ensures that the host does not retry failures
that are unlikely to succeed.
This is consistent with the retry mechanism defined in
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md).

### Signal conversion

> **Normative definition.**
The host MUST convert final success or failure into causally linked
signals.
Partial stream events are treated as bounded observations and do NOT
create durable effects until the response is finalized.

> **Normative definition.**
The host MUST emit the following signals:

| Event | Signal |
|-------|--------|
| Request created | `model.request.created` |
| Streaming started | `model.request.streaming` |
| Text delta received | `model.response.text_delta` |
| Tool request delta received | `model.response.tool_request_delta` |
| Response finalized (success) | `model.response.completed` |
| Response finalized (failure) | `model.response.failed` |
| Request cancelled | `model.request.cancelled` |
| Usage recorded | `model.usage.recorded` |

> **Non-normative note.**
Signal conversion ensures that downstream components can react to model
requests and responses through the signal envelope mechanism defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

### Outcome definitions

> **Normative definition.**
The following outcomes are defined for provider-neutral model requests:

#### Unavailable model

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable_model` | The requested model is not available from the provider. | Reject request; do NOT create partial request state. |

> **Non-normative note.**
Unavailable model is caused by the provider not supporting the requested
model.
The agent MUST update the request to use an available model and retry.

#### Quota exhaustion

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.quota_exhausted` | The agent's budget is insufficient to cover the request. | Reject request; do NOT create partial request state. |

> **Non-normative note.**
Quota exhaustion is caused by the agent exceeding its budget.
The agent MUST request additional budget from the topology owner and
retry.

#### Malformed structured output

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.invalid_structured_output` | The response's structured value does not conform to the `structured_output_schema`. | Reject response; emit `model.response.failed` signal. |

> **Non-normative note.**
Malformed structured output is caused by the model returning invalid
JSON or values that do not match the schema.
The agent MUST update the schema or sampling and retry.

#### Tool-call mismatch

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.tool_call_mismatch` | The model returns tool requests that do not match the `tool_definitions`. | Reject response; emit `model.response.failed` signal. |

> **Non-normative note.**
Tool-call mismatch is caused by the model using tools that were not
explicitly granted.
The agent MUST update the tool definitions and retry.

#### Safety refusal

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.safety_refused` | The provider refused the request due to safety filters. | Reject response; emit `model.response.failed` signal with safety metadata. |

> **Non-normative note.**
Safety refusal is caused by the provider's content filters.
The agent MUST update the prompt to avoid triggering the filters.

#### Timeout

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.timeout` | The request exceeded the implementation-defined timeout. | Cancel the request; emit `model.response.failed` signal. |

> **Non-normative note.**
Timeout is caused by the request taking longer than expected.
The agent MAY retry with different sampling or a simpler prompt.

#### Late response

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.late_response` | The response arrived after the `deadline`. | Accept the response but mark it as late in diagnostics. |

> **Non-normative note.**
Late response is caused by the provider being slow.
The host MUST accept the response but emit a warning in diagnostics.

#### Ambiguous billing

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.ambiguous_billing` | The provider's usage report is inconsistent with the host's calculation. | Accept the response but use the host's calculation for budget enforcement. |

> **Non-normative note.**
Ambiguous billing is caused by discrepancies between the provider's
and host's usage tracking.
The host MUST use its own calculation for budget enforcement to ensure
consistency.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 1 behavior and integration would invalidate
an earlier milestone assumption:

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

### Cross-references and precedence

> **Non-normative note.**
This section's behavior and integration integrate with the following
earlier chapters:

1. For provider adapter behavior: this section takes precedence over
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
   for questions of model-specific adapter behavior.
2. For streaming normalization: this section takes precedence over
   [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md)
   for questions of model-specific signal conversion.
3. For cancellation: this section takes precedence over
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md)
   for questions of model-specific cancellation.
4. For retry: this section takes precedence over
   [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md)
   for questions of model-specific retry classification.
5. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of model-specific capability mapping.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
