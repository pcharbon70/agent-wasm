---
title: "Phase 1 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-01
  - implementation
  - behavior-and-integration
  - provider-adapters
  - streaming
  - cancellation
  - retry
  - signal-conversion
aliases:
  - "M7-P1-1.2 Implementation"
---

# Phase 1 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 1.2 (Behavior And Integration) from
[Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
which establishes the behavior and integration rules for provider-neutral
model requests, responses, streaming, and usage.

## Subtask 1.2.1.1: Provider Adapter Registration and Capability Mapping

### Implementation

#### Provider adapter capabilities

Every provider adapter MUST include the following capabilities:

| Capability | Description |
|------------|-------------|
| `create_request` | Create a provider-specific request from the neutral request |
| `stream_response` | Stream the provider-specific response as normalized events |
| `cancel_request` | Cancel an in-flight request |
| `check_status` | Check the status of an in-flight request |

#### Agent grants to adapter capabilities mapping

| Agent Grant | Adapter Capability |
|-------------|-------------------|
| `model.request.create` | `create_request` |
| `model.request.stream` | `stream_response` |
| `model.request.cancel` | `cancel_request` |
| `model.request.status` | `check_status` |
| `model.usage.read` | `record_usage` |

### Provider adapter behavior

When the host receives a model request, it MUST:

1. **Validate the request**: Validate the request against the schema
   defined in section 41.1. Invalid requests MUST be rejected with
   the appropriate diagnostic.
2. **Resolve the provider**: Resolve the `provider` field to a registered
   adapter. Unregistered providers MUST be rejected with
   `model.request.unavailable_provider`.
3. **Check the budget**: Check that the agent's remaining budget is
   sufficient to cover the request. Insufficient budget MUST be rejected
   with `model.request.quota_exhausted`.
4. **Create the adapter request**: Call the adapter's `create_request`
   capability to create a provider-specific request.
5. **Start streaming**: Call the adapter's `stream_response` capability
   to start streaming the response.
6. **Normalize events**: Normalize each streaming event and emit a
   signal for each event.
7. **Finalize the response**: When the adapter signals completion or
   failure, finalize the response and emit a signal.
8. **Record usage**: Record usage for the request and update the agent's
   budget.

### Design decisions

1. **Framework plugin model**: Provider adapters behave as framework
   plugins: they are isolated in their own tenant, subject to the
   capability policy, and communicate with the host through well-defined
   interfaces.

2. **Fault-tolerant behavior**: If an adapter crashes or becomes
   unresponsive, the host MUST cancel the in-flight request and retry
   with a different adapter if available.

3. **Capability mapping**: Ensures that adapters only have access to the
   resources that the agent has been granted. Consistent with the
   capability policy defined in
   [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md).

## Subtask 1.2.1.2: Model Resolution, Streaming Normalization, and Signal Conversion

### Model resolution

The host MUST resolve the `model` field of a model request to a
provider-specific model identifier:

1. The host checks the adapter's registered models for a match.
2. If no match is found, the host returns `model.request.unavailable_model`.
3. If a match is found, the host returns the provider-specific model
   identifier.

### Streaming normalization

Streaming normalization converts provider-specific streaming events
into a common format:

| Provider Event | Normalized Event |
|----------------|------------------|
| `text_delta` | `text_delta` |
| `tool_call_delta` | `tool_request_delta` |
| `finish` | `finish` |
| `error` | `finish` (with `finish_reason: error`) |

### Signal conversion

The host MUST convert final success or failure into causally linked
signals. Partial stream events are treated as bounded observations and
do NOT create durable effects until the response is finalized.

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

### Design decisions

1. **Portable model names**: Agents can use portable model names
   (e.g., `gpt-4o`, `claude-3-5-sonnet`) without knowing the
   provider-specific identifiers.

2. **Bounded observations**: Streaming events are not durable until
   the response is finalized, which prevents partial state from
   polluting the durable journal.

3. **Causal signal chain**: Each signal is causally linked to the
   previous signal, enabling downstream components to reason about
   the request lifecycle.

## Subtask 1.2.1.3: Cancellation, Retry, and Outcome Definitions

### Cancellation behavior

When a model request is cancelled, the host MUST:

1. Call the adapter's `cancel_request` capability.
2. Mark the request as `cancelled` in the durable journal.
3. Emit a `model.request.cancelled` signal.
4. Release any resources associated with the request.

### Retry classification

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

### Outcome definitions

#### Unavailable model

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable_model` | The requested model is not available from the provider. | Reject request; do NOT create partial request state. |

#### Quota exhaustion

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.quota_exhausted` | The agent's budget is insufficient to cover the request. | Reject request; do NOT create partial request state. |

#### Malformed structured output

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.invalid_structured_output` | The response's structured value does not conform to the `structured_output_schema`. | Reject response; emit `model.response.failed` signal. |

#### Tool-call mismatch

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.tool_call_mismatch` | The model returns tool requests that do not match the `tool_definitions`. | Reject response; emit `model.response.failed` signal. |

#### Safety refusal

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.safety_refused` | The provider refused the request due to safety filters. | Reject response; emit `model.response.failed` signal with safety metadata. |

#### Timeout

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.timeout` | The request exceeded the implementation-defined timeout. | Cancel the request; emit `model.response.failed` signal. |

#### Late response

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.late_response` | The response arrived after the `deadline`. | Accept the response but mark it as late in diagnostics. |

#### Ambiguous billing

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.ambiguous_billing` | The provider's usage report is inconsistent with the host's calculation. | Accept the response but use the host's calculation for budget enforcement. |

### Design decisions

1. **Best-effort cancellation**: If the adapter does not support
   cancellation, the host MUST wait for the request to complete or
   timeout. This is consistent with the cancellation behavior defined
   in [Agent Registry Activation Cancellation And Completion](../60-specification/22-agent-registry-activation-cancellation-and-completion.md).

2. **Retry classification**: The host does not retry failures that are
   unlikely to succeed. Retryable failures are those where the agent
   can take corrective action (e.g., update tool definitions, fix schema).

3. **Late response acceptance**: Late responses are accepted but marked
   as late in diagnostics to avoid losing work while still providing
   visibility into performance issues.

4. **Host-calculated billing**: In case of ambiguous billing, the host
   uses its own calculation to ensure consistency. This prevents
   discrepancies between the provider's and host's usage tracking.

## Cross-references

- Section 41.2: [Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
- Section 41.1: [Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- Framework plugin model: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Cancellation: [Agent Registry Activation Cancellation And Completion](../60-specification/22-agent-registry-activation-cancellation-and-completion.md)
- Retry mechanism: [Retry Timer Recovery Replay Hibernate And Migration](../60-specification/28-retry-timer-recovery-replay-hibernate-and-migration.md)
- Signal envelopes: [Signal Envelopes Causality Routing And Delivery](../60-specification/10-signals-causality-routing-and-delivery.md)

## Open questions

1. Should the host retry on `adapter.error` immediately or wait for the
   agent to signal readiness? The current design retries immediately,
   but this may cause unnecessary load if the adapter is in a degraded
   state.

2. How should the host handle provider-specific error codes? The current
   design normalizes them into generic diagnostics, but this may lose
   important debugging information.

3. Should late responses be retried or accepted? The current design
   accepts late responses, but this may be unacceptable for time-sensitive
   use cases.
