---
title: "Phase 1 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-01
  - implementation
  - failure-evidence
  - diagnostics
  - evidence-emission
  - implementation-defined-choices
aliases:
  - "M7-P1-1.3 Implementation"
---

# Phase 1 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 1.3 (Failure Evidence And Operational Notes) from
[Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md)
which establishes the failure evidence and operational notes for
provider-neutral model requests, responses, streaming, and usage.

## Subtask 1.3.1.1: Failure Outcomes

### Malformed outcomes

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

### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable_provider` | Model request with unregistered `provider`. | Reject request; do NOT create partial request state. |
| `model.request.unavailable_model` | Model request with unavailable `model`. | Reject request; do NOT create partial request state. |
| `model.request.tool_call_mismatch` | Response with tool requests that do not match `tool_definitions`. | Reject response; do NOT create partial response state. |
| `model.request.invalid_structured_output` | Response with `structured_value` that does not conform to `structured_output_schema`. | Reject response; do NOT create partial response state. |

### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.duplicate-id` | Two model requests with the same `request_id` submitted concurrently. | Reject second request; do NOT create partial request state. |
| `model.request.conflicting-cancellation` | Two cancellation requests for the same `request_id` submitted concurrently. | Reject second cancellation; do NOT create partial request state. |

### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unauthorized` | Model request whose `agent_address` does not have the `model.request.create` capability. | Reject request; do NOT create partial request state. |
| `model.request.cross-tenant-tool` | Model request that grants cross-tenant tool access. | Reject request; do NOT create partial request state. |
| `model.request.cross-tenant-result` | Model request that grants cross-tenant result sharing. | Reject request; do NOT create partial request state. |

### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.quota_exhausted` | Agent's budget is insufficient to cover the request. | Reject request; do NOT create partial request state. |
| `model.request.exhausted-concurrency` | Host would exceed the implementation-defined maximum number of concurrent model requests. | Reject request; do NOT create partial request state. |
| `model.request.exhausted-stream` | Host would exceed the implementation-defined maximum number of concurrent streaming responses. | Reject request; do NOT create partial request state. |

### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.unavailable-provider` | Provider adapter is not active in the adapter registry. | Reject request; do NOT create partial request state. |
| `model.request.unavailable-model` | Model is not available from the provider. | Reject request; do NOT create partial request state. |
| `model.request.timeout` | Request exceeded the implementation-defined timeout. | Cancel request; do NOT create partial response state. |
| `model.request.late-response` | Response arrived after the `deadline`. | Accept response but mark as late in diagnostics. |

### Safety outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `model.request.safety_refused` | Provider refused the request due to safety filters. | Reject response; emit safety metadata in diagnostics. |
| `model.request.content_filter` | Response text was filtered by the provider's content filters. | Accept response but mark as filtered in diagnostics. |

### Design decisions

1. **Atomic rejection**: Every failure outcome MUST reject without creating
   partial request or response state. This is consistent with the atomic
   commit protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md).

2. **Consistent diagnostic format**: All diagnostics follow a consistent
   naming convention (`model.request.*` and `model.response.*`) and include
   the same set of fields, enabling consistent handling by downstream
   components.

3. **Cross-tenant rejection**: Cross-tenant tool access and result sharing
   are rejected outright to prevent authority leaks. This is consistent
   with the threat model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

4. **Safety metadata emission**: Safety-related diagnostics emit safety
   metadata in diagnostics to enable downstream filtering and auditing.

## Subtask 1.3.1.2: Bounded Diagnostics and Evidence

### Diagnostic fields

Every diagnostic MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic` | The failure diagnostic code (e.g., `model.request.malformed`). | Host runtime |
| `phase` | The phase that produced the diagnostic (`Phase 1`). | Host runtime |
| `section` | The section that produced the diagnostic (e.g., `41.3`). | Host runtime |
| `contract` | The contract that produced the diagnostic (e.g., `Provider-Neutral Model Requests Responses Streaming And Usage`). | Host runtime |
| `profile` | The conformance profile that produced the diagnostic. | Host runtime |
| `failed_boundary` | The failed boundary (e.g., `model.request.create`, `model.request.stream`, `model.request.cancel`). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of diagnostic emission. | Host clock |
| `message` | A human-readable description of the failure. | Host runtime |

### Evidence record fields

Every evidence record MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_type` | The evidence type (`model.request.created`, `model.request.completed`, `model.request.failed`, `model.request.cancelled`, `model.response.text_delta`, `model.response.tool_request_delta`, `model.usage.recorded`). | Host runtime |
| `request_id` | The `request_id` of the model request. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Host runtime |
| `provider` | The provider adapter identifier. | Host runtime |
| `model` | The model identifier. | Host runtime |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime |

### Design decisions

1. **Bounded diagnostics**: Diagnostics identify the phase contract, profile,
   and failed boundary without exposing secrets. This is consistent with
   the security requirements defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

2. **Tamper-evident evidence**: The `evidence_digest` field enables
   downstream systems to verify that the evidence record has not been
   tampered with after creation.

3. **Causal evidence types**: The evidence types follow a causal chain:
   `model.request.created` -> `model.request.streaming` ->
   `model.response.text_delta` / `model.response.tool_request_delta` ->
   `model.response.completed` / `model.response.failed` ->
   `model.usage.recorded` (or `model.request.cancelled`).

## Subtask 1.3.1.3: Implementation-Defined Choices and Deferred Work

### Implementation-defined choices

| Choice | Description | Constraint |
|--------|-------------|------------|
| Maximum concurrent requests | The maximum number of concurrent model requests. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent streams | The maximum number of concurrent streaming responses. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Request timeout | The maximum duration of a model request before timeout. | Must be longer than the maximum expected model response duration. Must be documented in the conformance profile. |
| Streaming buffer size | The maximum size of the streaming response buffer. | Must be at least 1 KB and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Usage recording interval | The interval between usage recordings (for long-running streams). | Must be at least 1 second and at most the implementation-defined maximum. Must be documented in the conformance profile. |

### Deferred work

The following work is deferred to future phases or milestones:

1. **Multi-model parallelism**: Running multiple model requests in
   parallel across different providers is deferred to Milestone 8.

2. **Model routing**: Routing model requests to the optimal provider
   based on cost, latency, and quality is deferred to Milestone 8.

3. **Model caching**: Caching model responses for repeated requests is
   deferred to Milestone 8.

4. **Model fallback**: Automatically falling back to a different model
   or provider on failure is deferred to Milestone 8.

### Design decisions

1. **Documented constraints**: Implementation-defined choices are documented
   in the conformance profile to ensure they are auditable and
   transparent.

2. **Deferred work**: The deferred work items are not within the scope
   of Phase 1 but may be addressed in future phases. Implementations
   MUST NOT implement deferred work without evidence from the
   corresponding future phase.

## Cross-references

- Section 41.3: [Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md)
- Section 41.1: [Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- Section 41.2: [Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
- Atomic commit protocol: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Threat model: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Security and audit: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Profile boundaries: [Profile Vocabulary And Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)

## Open questions

1. Should the diagnostic format include the full stack trace or just the
   failed boundary? The current design includes only the failed boundary
   to avoid exposing implementation details, but this may make debugging
   harder.

2. Should the evidence record include the full request/response payload or
   just a hash? The current design includes only the hash (via
   `evidence_digest`), but this may make it harder to reconstruct the
   full context of a failure.

3. Should implementation-defined choices have default values or be required?
   The current design requires them to be documented, but this may be
   burdensome for simple deployments.
