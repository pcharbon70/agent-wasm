---
title: "Phase 1 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-01
  - implementation
  - integration-tests
  - successful-flows
  - failure-handling
  - timeout-and-cancellation
  - cross-milestone-compatibility
aliases:
  - "M7-P1-1.4 Implementation"
---

# Phase 1 Integration Tests Implementation

## Overview

This note documents the implementation of Section 1.4 (Phase 1 Integration Tests) from
[Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md)
which defines the integration tests that verify provider-neutral model
requests, responses, streaming, and usage across its real dependency
boundaries.

## Subtask 1.4.1.1: Successful Flow Tests

### Model request creation flow tests (P1-SF-001 to P1-SF-010)

| Test ID | Description |
|---------|-------------|
| `P1-SF-001` | Create a model request with a valid provider, model, and messages and verify that the request is admitted. |
| `P1-SF-002` | Create a model request with a deterministic `request_id` and verify that two identical requests produce the same `request_id`. |
| `P1-SF-003` | Create a model request with structured output schema and verify that the schema is recorded. |
| `P1-SF-004` | Create a model request with tool definitions and verify that the tools are available to the model. |
| `P1-SF-005` | Create a model request with sampling controls and verify that the controls are passed to the provider. |
| `P1-SF-006` | Create a model request with a deadline and verify that the deadline is recorded. |
| `P1-SF-007` | Create a model request with a budget and verify that the budget is deducted from the agent's remaining budget. |
| `P1-SF-008` | Create a model request with trace context and verify that the context is passed to the provider. |
| `P1-SF-009` | Create a model request and verify that a `model.request.created` signal is emitted. |
| `P1-SF-010` | Create a model request and verify that the request is recorded in the durable journal. |

### Streaming response flow tests (P1-SF-011 to P1-SF-015)

| Test ID | Description |
|---------|-------------|
| `P1-SF-011` | Create a model request and verify that streaming events are emitted for each text delta. |
| `P1-SF-012` | Create a model request with tool definitions and verify that streaming events are emitted for each tool request delta. |
| `P1-SF-013` | Create a model request and verify that a finish event is emitted when the response is complete. |
| `P1-SF-014` | Create a model request and verify that a `model.response.completed` signal is emitted when the response is finalized. |
| `P1-SF-015` | Create a model request and verify that usage is recorded after the response is finalized. |

### Cancellation flow tests (P1-SF-016 to P1-SF-020)

| Test ID | Description |
|---------|-------------|
| `P1-SF-016` | Create a model request and cancel it before the response is finalized and verify that a `model.request.cancelled` signal is emitted. |
| `P1-SF-017` | Create a model request and cancel it after the response is finalized and verify that the cancellation is ignored. |
| `P1-SF-018` | Create two model requests and cancel one and verify that the other continues. |
| `P1-SF-019` | Create a model request with a deadline and cancel it before the deadline expires and verify that the cancellation is processed. |
| `P1-SF-020` | Create a model request with a deadline and cancel it after the deadline expires and verify that the cancellation is ignored. |

### Design decisions

1. **Observable behavior**: Tests verify observable behavior (signals,
   durable journal entries) rather than private implementation structure.
   This ensures that the tests remain valid even if the implementation
   changes.

2. **Deterministic `request_id`**: Test `P1-SF-002` verifies that the
   `request_id` is deterministic by creating two identical requests and
   checking that they produce the same `request_id`. This validates the
   idempotent retry design.

3. **Budget deduction**: Test `P1-SF-007` verifies that the budget is
   deducted from the agent's remaining budget when a request is created.
   This validates the budget enforcement mechanism.

4. **Signal emission**: Tests `P1-SF-009`, `P1-SF-014`, and `P1-SF-016`
   verify that the expected signals are emitted at the appropriate times.
   This validates the signal conversion layer.

5. **Durable journal recording**: Test `P1-SF-010` verifies that the
   request is recorded in the durable journal. This validates the
   atomic commit protocol.

## Subtask 1.4.1.2: Failure Handling Tests

### Malformed input tests (P1-FH-001 to P1-FH-009)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-001` | Model request with missing `provider` field. | `model.request.malformed` |
| `P1-FH-002` | Model request with missing `model` field. | `model.request.malformed` |
| `P1-FH-003` | Model request with empty `messages` list. | `model.request.malformed-messages` |
| `P1-FH-004` | Model request with invalid `sampling` controls. | `model.request.malformed-sampling` |
| `P1-FH-005` | Model request with invalid `deadline` timestamp. | `model.request.malformed-deadline` |
| `P1-FH-006` | Model request with invalid `budget` value. | `model.request.malformed-budget` |
| `P1-FH-007` | Response with invalid `text` field. | `model.response.malformed-text` |
| `P1-FH-008` | Response with invalid `structured_value` field. | `model.response.malformed-structured` |
| `P1-FH-009` | Response with invalid `usage` metrics. | `model.response.malformed-usage` |

### Incompatible input tests (P1-FH-010 to P1-FH-013)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-010` | Model request with unregistered `provider`. | `model.request.unavailable_provider` |
| `P1-FH-011` | Model request with unavailable `model`. | `model.request.unavailable_model` |
| `P1-FH-012` | Response with tool requests that do not match `tool_definitions`. | `model.request.tool_call_mismatch` |
| `P1-FH-013` | Response with `structured_value` that does not conform to `structured_output_schema`. | `model.request.invalid_structured_output` |

### Conflicting input tests (P1-FH-014 to P1-FH-015)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-014` | Two model requests with the same `request_id` submitted concurrently. | `model.request.duplicate-id` for the second request. |
| `P1-FH-015` | Two cancellation requests for the same `request_id` submitted concurrently. | `model.request.conflicting-cancellation` for the second cancellation. |

### Unauthorized input tests (P1-FH-016 to P1-FH-018)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-016` | Model request whose `agent_address` does not have the `model.request.create` capability. | `model.request.unauthorized` |
| `P1-FH-017` | Model request that grants cross-tenant tool access. | `model.request.cross-tenant-tool` |
| `P1-FH-018` | Model request that grants cross-tenant result sharing. | `model.request.cross-tenant-result` |

### Exhausted input tests (P1-FH-019 to P1-FH-020)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-019` | Model request that would exceed the implementation-defined maximum number of concurrent requests. | `model.request.exhausted-concurrency` |
| `P1-FH-020` | Model request that would exceed the implementation-defined maximum number of concurrent streams. | `model.request.exhausted-stream` |

### Unavailable input tests (P1-FH-021 to P1-FH-022)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-021` | Model request whose `provider` is not active in the adapter registry. | `model.request.unavailable-provider` |
| `P1-FH-022` | Model request whose `model` is not available from the provider. | `model.request.unavailable-model` |

### Design decisions

1. **State invariants**: Each failure test verifies that the host does
   NOT create partial request or response state. This validates the
   atomic rejection design.

2. **Stable diagnostics**: Each failure test verifies that the expected
   diagnostic is emitted. This validates the diagnostic format and
   consistency.

3. **Coverage**: The tests cover all failure outcome categories defined
   in section 41.3: malformed, incompatible, conflicting, unauthorized,
   exhausted, and unavailable.

## Subtask 1.4.1.3: Timeout And Cancellation Tests

### Model request timeout tests (P1-TO-001 to P1-TO-005)

| Test ID | Description |
|---------|-------------|
| `P1-TO-001` | Create a model request and verify that the request is completed before the implementation-defined timeout expires. |
| `P1-TO-002` | Create a model request and verify that the request is cancelled with `model.request.timeout` if it exceeds the implementation-defined timeout. |
| `P1-TO-003` | Create a model request with a deadline and verify that the request is completed before the deadline. |
| `P1-TO-004` | Create a model request with a deadline and verify that the request is accepted with `model.request.late-response` if it exceeds the deadline. |
| `P1-TO-005` | Create a model request with a deadline and verify that the request is cancelled with `model.request.timeout` if it exceeds the implementation-defined timeout. |

### Cancellation tests (P1-CA-001 to P1-CA-004)

| Test ID | Description |
|---------|-------------|
| `P1-CA-001` | Cancel a model request and verify that the cancellation is processed. |
| `P1-CA-002` | Cancel a model request after the response is finalized and verify that the cancellation is ignored. |
| `P1-CA-003` | Cancel two model requests concurrently and verify that only one cancellation is processed. |
| `P1-CA-004` | Verify that a `model.request.cancelled` signal is emitted when a model request is cancelled. |

### Design decisions

1. **Timeout scenarios**: The tests cover both the implementation-defined
   timeout and the agent-specified deadline, validating both timeout
   mechanisms.

2. **Cancellation timing**: The tests verify cancellation behavior at
   different points in the request lifecycle (before completion, after
   completion, with deadline).

3. **Concurrent cancellation**: Test `P1-CA-003` verifies that concurrent
   cancellation requests are handled correctly (only one is processed).
   This validates the conflict resolution mechanism.

4. **No partial state**: All timeout and cancellation tests verify that
   no partial state is left in the durable journal.

## Subtask 1.4.1.4: Cross-Milestone Compatibility Tests

### Affected earlier milestone fixtures

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 7 Phase 1 | Model requests, responses, streaming, and usage | All fixtures continue to pass; model requests are correctly processed. |
| Milestone 6 Phase 1 | Signal envelopes, causality routing, and delivery | All fixtures continue to pass; model request signals are correctly routed through the signal envelope mechanism. |
| Milestone 6 Phase 2 | Actions, instructions, validation, plans, and results | All fixtures continue to pass; model request validation is consistent with the actions validation flow. |
| Milestone 6 Phase 3 | State operations, patches, revisions, and conflicts | All fixtures continue to pass; model request state is correctly managed through the state operations mechanism. |
| Milestone 6 Phase 4 | Directives, strategies, continuations, and terminal states | All fixtures continue to pass; model request terminal states are consistent with the directive terminal states. |
| Milestone 6 Phase 5 | Deterministic reducer semantics and milestone acceptance | All fixtures continue to pass; model request results are correctly processed by the deterministic reducer. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; model request grants are consistent with the threat model. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; model request grant attenuation is consistent with the capability policy. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; model request adapters are consistent with the framework plugin model. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; model request adapters are subject to the same WASI restrictions. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; model request evidence is correctly signed and audited. |

### Design decisions

1. **Comprehensive scope**: The tests cover 11 fixture scopes from 6
   milestones, validating that Phase 1 does not introduce regressions
   in earlier milestones.

2. **Indirect effects**: The scope accounts for indirect effects through
   shared subsystems (such as the agent registry, mailboxes, and durable
   journal), not just direct integration points.

3. **Baseline comparison**: Each fixture is compared against a baseline
   to detect regressions. Any deviations are documented as approved
   variability.

4. **Revision protocol**: If any fixture fails, the Phase 1 implementation
   MUST be revised and the affected milestone MUST be re-validated
   according to the cross-milestone revision protocol defined in
   [Specification Authority](../SPECIFICATION-AUTHORITY.md).

## Integration Test Evidence Requirements

### Evidence items

The following evidence items MUST be recorded for each test scenario:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P1-SF-001`). | String |
| `test_objective` | The test objective this scenario addresses. | String |
| `setup` | The test setup description (input data, preconditions). | Structured text |
| `expected_outcome` | The expected observable behavior. | Structured text |
| `actual_outcome` | The actual observable behavior. | Structured text |
| `result` | `pass`, `fail`, or `blocked`. | Enum |
| `evidence_digest` | A deterministic hash of the evidence record. | Hash digest |
| `timestamp` | The ISO 8601 timestamp of test execution. | ISO 8601 string |
| `regression` | For cross-milestone tests, whether the test previously passed. | Boolean |
| `approved_variability` | For cross-milestone tests, any approved variability from the baseline. | Structured text |

### Promotion criteria

Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 1 integration tests as defined above.
2. A passing run of all cross-milestone compatibility tests as defined
   above.
3. All evidence records for the passing run, signed and stored in the
   durable evidence log.
4. A written report summarizing the test run, including any approved
   variability, regressions, or deviations from the baseline.

### Design decisions

1. **Tamper-evident evidence**: The `evidence_digest` field enables
   downstream systems to verify that the evidence record has not been
   tampered with after creation.

2. **Signed evidence**: All evidence records are signed according to the
   provenance and audit mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

3. **Reproducible**: The evidence format enables reproducible test runs
   that can be verified independently.

4. **Narrative context**: The written report provides context and narrative
   that structured evidence records cannot capture, such as explanations
   of approved variability or deviations from the baseline.

## Cross-references

- Section 41.4: [Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md)
- Section 41.1: [Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- Section 41.2: [Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
- Section 41.3: [Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md)
- Atomic commit protocol: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Provenance and audit: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Specification authority: [Specification Authority](../SPECIFICATION-AUTHORITY.md)

## Open questions

1. Should the test evidence include the full input/output data or just
   a hash? The current design includes the full data in the evidence
   record, but this may expose sensitive data.

2. Should cross-milestone tests run automatically or manually? The current
   design does not specify, but automated testing would be more reliable.

3. Should the evidence record include timing information (e.g., test
   duration)? This would be useful for performance analysis but adds
   overhead to the evidence format.
