---
title: "Phase 1 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-01
  - implementation
  - contract-and-data-model
  - model-requests
  - responses
  - streaming
  - usage
aliases:
  - "M7-P1-1.1 Implementation"
---

# Phase 1 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 1.1 (Contract And Data Model) from
[Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](../../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md](../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
which establishes the contract and data model for provider-neutral model
requests, responses, streaming, and usage.

## Subtask 1.1.1.1: Model Request Identity and Provider Constraints

### Implementation

Defined the following fields for model requests:

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | Deterministic request identity derived from agent address, turn sequence, and request payload hash | Host runtime |
| `agent_address` | `TenantQualifiedAgentAddress` of the agent that originated the request | Agent |
| `provider` | Provider adapter identifier (e.g., `openai`, `anthropic`, `local`) | Agent |
| `model` | Model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet`) | Agent |
| `messages` | List of conversation messages (system, user, assistant) | Agent |
| `structured_output_schema` | JSON Schema for expected structured output, if applicable | Agent |
| `tool_definitions` | List of tool definitions available to the model | Agent |
| `sampling` | Sampling controls: `temperature`, `top_p`, `max_tokens`, `frequency_penalty`, `presence_penalty` | Agent |
| `deadline` | ISO 8601 deadline by which the response MUST be received | Agent |
| `budget` | Maximum cost (in implementation-defined units) for this request | Agent |
| `trace_context` | Distributed tracing context for observability | Host runtime |
| `created_at` | ISO 8601 timestamp of request creation | Host clock |
| `status` | Current status: `pending`, `streaming`, `completed`, `failed`, `cancelled` | Host runtime |

### Design decisions

1. **Deterministic `request_id`**: Enables idempotent retry by producing the
   same `request_id` for identical request payloads. Consistent with the
   deterministic reducer semantics defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md).

2. **Agent-originated fields vs. host-originated fields**: Separation of
   concerns between agent-provided data (provider, model, messages, etc.)
   and host-managed data (request_id, created_at, status, trace_context).

3. **Provider adapter identifiers**: Use string identifiers (e.g., `openai`,
   `anthropic`, `local`) rather than full adapter paths to keep requests
   portable across different deployment configurations.

## Subtask 1.1.1.2: Response Normalization

### Implementation

Defined the following fields for normalized responses:

| Field | Content | Source |
|-------|---------|--------|
| `response_id` | Deterministic response identity derived from `request_id` and response sequence number | Host runtime |
| `request_id` | `request_id` of the associated model request | Normalized from provider |
| `text` | Response text, if any | Normalized from provider |
| `structured_value` | Structured value (parsed from `structured_output_schema`), if applicable | Normalized from provider |
| `tool_requests` | List of tool requests made by the model | Normalized from provider |
| `finish_reason` | Finish reason: `stop`, `length`, `content_filter`, `tool_calls`, `error` | Normalized from provider |
| `usage` | Usage metrics: `prompt_tokens`, `completion_tokens`, `total_tokens` | Normalized from provider |
| `provider_response_id` | Provider-specific response identifier (for debugging) | Normalized from provider |
| `provider_error` | Provider-specific error, if any | Normalized from provider |
| `safety_metadata` | Safety metadata: `content_filter_results`, `safety_categories` | Normalized from provider |
| `diagnostics` | Diagnostics: `latency_ms`, `retry_count` | Host runtime |
| `created_at` | ISO 8601 timestamp of response creation | Host clock |

### Design decisions

1. **Response normalization**: Provider-specific responses are normalized
   into a common format before being recorded as durable effects. This
   ensures that downstream components (such as tool handlers and structured
   output validators) can work with provider-neutral data without knowing
   the provider-specific format.

2. **Provider-specific debugging**: Include `provider_response_id` and
   `provider_error` for debugging while keeping the primary fields
   provider-neutral.

3. **Safety metadata**: Capture safety-related information separately to
   enable downstream filtering and auditing without exposing sensitive
   content.

## Subtask 1.1.1.3: Streaming Normalization and Usage Tracking

### Implementation

Defined the following fields for streaming events:

| Field | Content | Source |
|-------|---------|--------|
| `event_id` | Deterministic event identity derived from `request_id` and event sequence number | Host runtime |
| `request_id` | `request_id` of the associated model request | Normalized from provider |
| `event_type` | Event type: `text_delta`, `tool_request_delta`, `finish` | Normalized from provider |
| `text_delta` | Text delta (for `text_delta` events), if applicable | Normalized from provider |
| `tool_request_delta` | Tool request delta (for `tool_request_delta` events), if applicable | Normalized from provider |
| `finish_reason` | Finish reason (for `finish` events), if applicable | Normalized from provider |
| `usage` | Cumulative usage (for `finish` events), if applicable | Normalized from provider |
| `created_at` | ISO 8601 timestamp of event creation | Host clock |

### Usage tracking fields

| Field | Content | Source |
|-------|---------|--------|
| `usage_id` | Deterministic usage identity derived from `request_id` | Host runtime |
| `request_id` | `request_id` of the associated model request | Normalized from provider |
| `agent_address` | `TenantQualifiedAgentAddress` of the agent that originated the request | Host runtime |
| `provider` | Provider adapter identifier | Host runtime |
| `model` | Model identifier | Host runtime |
| `prompt_tokens` | Number of prompt tokens used | Normalized from provider |
| `completion_tokens` | Number of completion tokens used | Normalized from provider |
| `total_tokens` | Total number of tokens used | Normalized from provider |
| `cost` | Cost in implementation-defined units | Host runtime |
| `currency` | Currency (e.g., `USD`) | Host runtime |
| `created_at` | ISO 8601 timestamp of usage recording | Host clock |

### Design decisions

1. **Streaming events are bounded observations**: Streaming events do NOT
   create durable effects until the response is finalized. This ensures
   that partial streaming data does not pollute the durable journal and
   can be discarded on cancellation or failure.

2. **Budget enforcement**: Usage tracking records the token counts and
   cost for each model request. The host MUST enforce the `budget`
   constraint by rejecting requests that would exceed the agent's
   remaining budget.

3. **Usage records are stored in the durable journal**: Consistent with
   the storage contract defined in
   [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md).

## Cross-references

- Section 41.1: [Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](../../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- Deterministic reducer semantics: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- Framework plugin model: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Security and audit: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

## Open questions

1. Should streaming events be recorded in the durable journal even though
   they are bounded observations? This would enable replay but at the cost
   of storage overhead.
2. How should cross-tenant tool access be validated? The current design
   rejects cross-tenant tool access outright, but this may need to be
   configurable for multi-tenant deployments.
3. What is the implementation-defined maximum cost unit? The spec uses
   "implementation-defined units" which leaves this to the host
   implementation. This is intentional to allow different billing models.
