---
title: "Phase 2 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-02
  - implementation
  - integration-tests
  - successful-flows
  - failure-handling
  - timeout-and-cancellation
  - cross-milestone-compatibility
aliases:
  - "M7-P2-2.4 Implementation"
---

# Phase 2 Integration Tests Implementation

## Overview

This note documents the implementation of Section 2.4 (Phase 2 Integration Tests) from
[Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](../../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md](../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md)
which defines the integration tests that verify tool catalogs, retrieval,
code execution, and connectors across their real dependency boundaries.

## Subtask 2.4.1.1: Successful Flow Tests

### Tool catalog and execution flow tests (P2-SF-001 to P2-SF-010)

| Test ID | Description |
|---------|-------------|
| `P2-SF-001` | Create a framework plugin with a tool descriptor and verify that the tool is added to the catalog. |
| `P2-SF-002` | Query the tool catalog and verify that the tool is visible to agents with the required capability. |
| `P2-SF-003` | Query the tool catalog and verify that the tool is NOT visible to agents without the required capability. |
| `P2-SF-004` | Execute a tool with valid input and verify that the tool executes successfully. |
| `P2-SF-005` | Execute a tool with valid input and verify that a `tool.execution.result` signal is emitted. |
| `P2-SF-006` | Execute a tool with valid input and verify that the execution is recorded in the durable journal. |
| `P2-SF-007` | Execute a tool with idempotent=true and verify that retrying produces the same result. |
| `P2-SF-008` | Execute a tool with a timeout and verify that the execution completes before the timeout. |
| `P2-SF-009` | Execute a tool with a resource budget and verify that the resource usage is recorded. |
| `P2-SF-010` | Execute a tool with provenance_required=true and verify that provenance evidence is captured. |

### Retrieval flow tests (P2-SF-011 to P2-SF-018)

| Test ID | Description |
|---------|-------------|
| `P2-SF-011` | Execute a retrieval request with a valid query and verify that results are returned. |
| `P2-SF-012` | Execute a retrieval request with tenant_scope=self and verify that only self-scoped results are returned. |
| `P2-SF-013` | Execute a retrieval request with filters and verify that filtered results are returned. |
| `P2-SF-014` | Execute a retrieval request and verify that a `retrieval.completed` signal is emitted. |
| `P2-SF-015` | Execute a retrieval request and verify that the request is recorded in the durable journal. |
| `P2-SF-016` | Execute a retrieval request with max_results=5 and verify that at most 5 results are returned. |
| `P2-SF-017` | Execute a retrieval request with ranking=relevance and verify that results are ranked by relevance. |
| `P2-SF-018` | Execute a retrieval request and verify that content references are included for deduplication. |

### Code execution flow tests (P2-SF-019 to P2-SF-026)

| Test ID | Description |
|---------|-------------|
| `P2-SF-019` | Execute a code execution request with valid code and verify that the code executes successfully. |
| `P2-SF-020` | Execute a code execution request with valid code and verify that a `code.completed` signal is emitted. |
| `P2-SF-021` | Execute a code execution request with valid code and verify that the execution is recorded in the durable journal. |
| `P2-SF-022` | Execute a code execution request with isolation_class=isolated and verify that the code runs in isolation. |
| `P2-SF-023` | Execute a code execution request with a resource budget and verify that the resource usage is recorded. |
| `P2-SF-024` | Execute a code execution request with a timeout and verify that the execution completes before the timeout. |
| `P2-SF-025` | Execute a code execution request with artifacts=true and verify that output artifacts are captured. |
| `P2-SF-026` | Execute a code execution request with a sandbox and verify that sandbox restrictions are enforced. |

### Design decisions

1. **Observable behavior**: Tests verify observable behavior (signals,
   durable journal entries) rather than private implementation structure.
   This ensures that the tests remain valid even if the implementation
   changes.

2. **Capability visibility**: Test `P2-SF-002` and `P2-SF-003` verify
   that tools are visible only to agents with the required capability.
   This validates the capability-based catalog filtering.

3. **Idempotent execution**: Test `P2-SF-007` verifies that idempotent
   tools produce the same result on retry. This validates the idempotency
   design.

4. **Resource tracking**: Tests `P2-SF-009` and `P2-SF-023` verify that
   resource usage is recorded. This validates the resource budgeting
   mechanism.

5. **Provenance capture**: Test `P2-SF-010` verifies that provenance
   evidence is captured for tools that require it. This validates the
   provenance mechanism.

6. **Tenant scope**: Test `P2-SF-012` verifies that tenant scope filters
   are enforced. This validates the tenant isolation design.

7. **Content deduplication**: Test `P2-SF-018` verifies that content
   references are included for deduplication. This validates the storage
   optimization.

8. **Sandbox enforcement**: Test `P2-SF-026` verifies that sandbox
   restrictions are enforced. This validates the isolation design.

## Subtask 2.4.1.2: Failure Handling Tests

### Malformed input tests (P2-FH-001 to P2-FH-009)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-001` | Tool execution request with missing `tool_id` field. | `tool.request.malformed` |
| `P2-FH-002` | Tool execution request with invalid `tool_id` format. | `tool.request.malformed-tool_id` |
| `P2-FH-003` | Tool execution request with invalid `input` data. | `tool.request.malformed-input` |
| `P2-FH-004` | Code execution request with invalid `language` field. | `tool.request.malformed-language` |
| `P2-FH-005` | Code execution request with invalid `code` field. | `tool.request.malformed-code` |
| `P2-FH-006` | Code execution request with invalid `environment` field. | `tool.request.malformed-environment` |
| `P2-FH-007` | Retrieval request with missing `query` field. | `tool.request.malformed-query` |
| `P2-FH-008` | Tool result with invalid `output` data. | `tool.result.malformed-output` |
| `P2-FH-009` | Tool result with invalid `resource_usage` metrics. | `tool.result.malformed-usage` |

### Incompatible input tests (P2-FH-010 to P2-FH-013)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-010` | Tool execution request with unknown `tool_id`. | `tool.execution.unknown_tool` |
| `P2-FH-011` | Tool execution request with input that does not conform to `input_schema`. | `tool.execution.schema_mismatch` |
| `P2-FH-012` | Tool result with output that does not conform to `output_schema`. | `tool.execution.result_schema_mismatch` |
| `P2-FH-013` | Tool execution request with stale catalog version. | `tool.execution.stale_catalog` |

### Conflicting input tests (P2-FH-014 to P2-FH-015)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-014` | Two tool execution requests with the same `request_id` submitted concurrently. | `tool.execution.duplicate-id` for the second request. |
| `P2-FH-015` | Two cancellation requests for the same `request_id` submitted concurrently. | `tool.execution.conflicting-cancellation` for the second cancellation. |

### Unauthorized input tests (P2-FH-016 to P2-FH-018)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-016` | Tool execution request whose `agent_address` does not have the required capability. | `tool.execution.denied_capability` |
| `P2-FH-017` | Tool execution request that accesses cross-tenant data. | `tool.execution.cross-tenant-data` |
| `P2-FH-018` | Tool execution request using an unauthorized connector. | `tool.execution.unauthorized_connector` |

### Exhausted input tests (P2-FH-019 to P2-FH-021)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-019` | Tool execution request that would exceed the implementation-defined maximum number of concurrent tool executions. | `tool.execution.exhausted-concurrency` |
| `P2-FH-020` | Code execution request that would exceed the implementation-defined maximum number of concurrent code executions. | `tool.execution.exhausted-code` |
| `P2-FH-021` | Tool execution request that would exceed the agent's capability budget. | `tool.execution.quota_exhausted` |

### Unavailable input tests (P2-FH-022 to P2-FH-024)

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-022` | Tool execution request for a tool that is not active in the framework plugin registry. | `tool.execution.unavailable_tool` |
| `P2-FH-023` | Tool execution request for a connector that is not active in the connector registry. | `tool.execution.unavailable_connector` |
| `P2-FH-024` | Code execution request that exceeds sandbox memory limits. | `tool.execution.sandbox_failure` |

### Design decisions

1. **State invariants**: Each failure test verifies that the host does
   NOT create partial execution or result state. This validates the
   atomic rejection design.

2. **Stable diagnostics**: Each failure test verifies that the expected
   diagnostic is emitted. This validates the diagnostic format and
   consistency.

3. **Comprehensive failure coverage**: The tests cover all failure outcome
   categories defined in section 42.3: malformed, incompatible, conflicting,
   unauthorized, exhausted, and unavailable.

## Subtask 2.4.1.3: Timeout And Cancellation Tests

### Tool execution timeout tests (P2-TO-001 to P2-TO-005)

| Test ID | Description |
|---------|-------------|
| `P2-TO-001` | Execute a tool and verify that the tool completes before the implementation-defined timeout expires. |
| `P2-TO-002` | Execute a tool and verify that the tool is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-003` | Execute a tool with a custom timeout and verify that the tool completes before the custom timeout. |
| `P2-TO-004` | Execute a tool with a custom timeout and verify that the tool is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-005` | Execute a tool and verify that cancellation leaves no partial state in the durable journal. |

### Retrieval timeout tests (P2-TO-006 to P2-TO-010)

| Test ID | Description |
|---------|-------------|
| `P2-TO-006` | Execute a retrieval request and verify that the retrieval completes before the implementation-defined timeout expires. |
| `P2-TO-007` | Execute a retrieval request and verify that the retrieval is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-008` | Execute a retrieval request with a custom timeout and verify that the retrieval completes before the custom timeout. |
| `P2-TO-009` | Execute a retrieval request with a custom timeout and verify that the retrieval is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-010` | Execute a retrieval request and verify that cancellation leaves no partial state in the durable journal. |

### Code execution timeout tests (P2-TO-011 to P2-TO-015)

| Test ID | Description |
|---------|-------------|
| `P2-TO-011` | Execute a code execution request and verify that the code completes before the implementation-defined timeout expires. |
| `P2-TO-012` | Execute a code execution request and verify that the code is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-013` | Execute a code execution request with a custom timeout and verify that the code completes before the custom timeout. |
| `P2-TO-014` | Execute a code execution request with a custom timeout and verify that the code is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-015` | Execute a code execution request and verify that cancellation leaves no partial state in the durable journal. |

### Cancellation tests (P2-CA-001 to P2-CA-008)

| Test ID | Description |
|---------|-------------|
| `P2-CA-001` | Cancel a tool execution request and verify that the cancellation is processed. |
| `P2-CA-002` | Cancel a retrieval request and verify that the cancellation is processed. |
| `P2-CA-003` | Cancel a code execution request and verify that the cancellation is processed. |
| `P2-CA-004` | Cancel a tool execution request after the execution is completed and verify that the cancellation is ignored. |
| `P2-CA-005` | Cancel a retrieval request after the retrieval is completed and verify that the cancellation is ignored. |
| `P2-CA-006` | Cancel a code execution request after the code is completed and verify that the cancellation is ignored. |
| `P2-CA-007` | Cancel two tool execution requests concurrently and verify that only one cancellation is processed. |
| `P2-CA-008` | Verify that a `tool.execution.cancelled` signal is emitted when a tool execution request is cancelled. |

### Design decisions

1. **Timeout scenarios**: The tests cover both the implementation-defined
   timeout and the agent-specified custom timeout for tool, retrieval,
   and code execution.

2. **Cancellation timing**: The tests verify cancellation behavior at
   different points in the lifecycle (during execution, after completion).

3. **Concurrent cancellation**: Test `P2-CA-007` verifies that concurrent
   cancellation requests are handled correctly (only one is processed).
   This validates the conflict resolution mechanism.

4. **No partial state**: All timeout and cancellation tests verify that
   no partial state is left in the durable journal.

## Subtask 2.4.1.4: Cross-Milestone Compatibility Tests

### Affected earlier milestone fixtures

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 7 Phase 1 | Model requests, responses, streaming, and usage | All fixtures continue to pass; model requests can call tools. |
| Milestone 7 Phase 2 | Tool catalogs, retrieval, code execution, and connectors | All fixtures continue to pass; tools are correctly resolved and executed. |
| Milestone 6 Phase 1 | Signal envelopes, causality routing, and delivery | All fixtures continue to pass; tool execution signals are correctly routed. |
| Milestone 6 Phase 2 | Actions, instructions, validation, plans, and results | All fixtures continue to pass; tool execution results are consistent with action results. |
| Milestone 6 Phase 3 | State operations, patches, revisions, and conflicts | All fixtures continue to pass; tool execution state is correctly managed. |
| Milestone 6 Phase 4 | Directives, strategies, continuations, and terminal states | All fixtures continue to pass; tool execution directives are consistent. |
| Milestone 6 Phase 5 | Deterministic reducer semantics and milestone acceptance | All fixtures continue to pass; tool execution results are correctly processed. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; tool execution grants are consistent. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; tool execution capability enforcement is consistent. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; tool execution framework plugins are consistent. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; tool execution isolation is consistent. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; tool execution provenance is consistent. |

### Design decisions

1. **Comprehensive scope**: The tests cover 12 fixture scopes from 6
   milestones, validating that Phase 2 does not introduce regressions
   in earlier milestones.

2. **Indirect effects**: The scope accounts for indirect effects through
   shared subsystems (such as the agent registry, mailboxes, and durable
   journal), not just direct integration points.

3. **Baseline comparison**: Each fixture is compared against a baseline
   to detect regressions. Any deviations are documented as approved
   variability.

4. **Revision protocol**: If any fixture fails, the Phase 2 implementation
   MUST be revised and the affected milestone MUST be re-validated
   according to the cross-milestone revision protocol defined in
   [Specification Authority](../../SPECIFICATION-AUTHORITY.md).

## Integration Test Evidence Requirements

### Evidence items

The following evidence items MUST be recorded for each test scenario:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P2-SF-001`). | String |
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

1. A passing run of all Phase 2 integration tests as defined above.
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
   [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

3. **Reproducible**: The evidence format enables reproducible test runs
   that can be verified independently.

4. **Narrative context**: The written report provides context and narrative
   that structured evidence records cannot capture, such as explanations
   of approved variability or deviations from the baseline.

## Cross-references

- Section 42.4: [Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests](../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md)
- Section 42.1: [Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- Section 42.2: [Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md)
- Section 42.3: [Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](../../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md)
- Atomic commit protocol: [Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Provenance and audit: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Specification authority: [Specification Authority](../../SPECIFICATION-AUTHORITY.md)

## Open questions

1. Should the test evidence include the full input/output data or just
   a hash? The current design includes the full data in the evidence
   record, but this may expose sensitive data.

2. Should cross-milestone tests run automatically or manually? The current
   design does not specify, but automated testing would be more reliable.

3. Should the evidence record include timing information (e.g., test
   duration)? This would be useful for performance analysis but adds
   overhead to the evidence format.

4. Should sandbox memory limits be configurable per tool or only globally?
   The current design allows global configuration, but per-tool limits
   may be more flexible.
