---
title: "Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-02
  - tool-catalogs
  - retrieval
  - code-execution
  - connectors
  - integration-tests
  - credential-custody
aliases:
  - "M7-P2 Phase 2 Integration Tests"
---

# Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It defines the integration tests that verify tool catalogs, retrieval,
code execution, and connectors across their real dependency boundaries.

Version `0.2.0` adds authenticated-connector fixtures proving that the same
use-only custodian boundary applies to connector credentials and refresh
tokens, not only model-provider credentials.

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
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md),
[Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md),
[Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md),
[Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md).

## 42.4 Phase 2 Integration Tests

The harness MUST include an authenticated connector, a user-controlled
custodian containing a unique sentinel credential and refresh token, a fake
external service, and inspection of guest I/O, host and Port memory, durable
stores, journals, logs, traces, diagnostics, evidence, crash artifacts,
network destinations, and support bundles. The sentinel values MUST exist only
inside the custodian fixture.

### 42.4.1 Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes tool
catalogs, retrieval, code execution, and connectors under normal
operating conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Tool catalog and execution flow tests

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

> **Non-normative note.**
Tests `P2-SF-001` through `P2-SF-010` exercise the full tool catalog
and execution flow defined in section 42.2.

#### Retrieval flow tests

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

> **Non-normative note.**
Tests `P2-SF-011` through `P2-SF-018` validate the full retrieval flow
defined in section 42.2.
Each test validates one of the eight retrieval operations and verifies
that the host behaves correctly according to the operation.

#### Code execution flow tests

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

> **Non-normative note.**
Tests `P2-SF-019` through `P2-SF-026` validate the full code execution
flow defined in section 42.2.
Each test validates one of the eight code execution operations and verifies
that the host behaves correctly according to the operation.

#### Connector flow tests

| Test ID | Description |
| --- | --- |
| `P2-SF-027` | User binds an authenticated connector to a registered custodian and executes one typed tool operation; verify a valid result and receipt. |
| `P2-SF-028` | Rotate or refresh connector authority inside the custodian and execute again; verify no plugin, host, or Port configuration receives a token. |
| `P2-SF-029` | Execute an unauthenticated connector through its approved direct handler; verify that no credential-use request is created. |

### 42.4.2 Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

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

> **Normative definition.**
Each malformed input test MUST verify that the host: (1) rejects the
request or result with the specified diagnostic, (2) does NOT create a
partial execution or result state, and (3) does NOT leave any live actor
instance in an indeterminate state.

> **Non-normative note.**
The malformed input tests validate the schema validation layer that guards
the atomic commit protocol.
Without these tests, a malformed request could cause inconsistent state
or leave partial state in the durable journal, violating the atomicity
guarantees defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-010` | Tool execution request with unknown `tool_id`. | `tool.execution.unknown_tool` |
| `P2-FH-011` | Tool execution request with input that does not conform to `input_schema`. | `tool.execution.schema_mismatch` |
| `P2-FH-012` | Tool result with output that does not conform to `output_schema`. | `tool.execution.result_schema_mismatch` |
| `P2-FH-013` | Tool execution request with stale catalog version. | `tool.execution.stale_catalog` |

> **Non-normative note.**
The incompatible input tests validate the semantic validation layer that
guards the atomic commit protocol.
Without these tests, an incompatible request could cause inconsistent
state or leave partial state in the durable journal.

#### Conflicting input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-014` | Two tool execution requests with the same `request_id` submitted concurrently. | `tool.execution.duplicate-id` for the second request. |
| `P2-FH-015` | Two cancellation requests for the same `request_id` submitted concurrently. | `tool.execution.conflicting-cancellation` for the second cancellation. |

> **Non-normative note.**
The conflicting input tests validate the deduplication and conflict
resolution layer that guards the atomic commit protocol.
Without these tests, conflicting requests could cause inconsistent
state or leave partial state in the durable journal.

#### Unauthorized input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-016` | Tool execution request whose `agent_address` does not have the required capability. | `tool.execution.denied_capability` |
| `P2-FH-017` | Tool execution request that accesses cross-tenant data. | `tool.execution.cross-tenant-data` |
| `P2-FH-018` | Tool execution request using an unauthorized connector. | `tool.execution.unauthorized_connector` |

> **Non-normative note.**
The unauthorized input tests validate the capability enforcement layer
that guards the atomic commit protocol.
Without these tests, unauthorized requests could bypass the capability
policy and compromise system security.

#### Exhausted input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-019` | Tool execution request that would exceed the implementation-defined maximum number of concurrent tool executions. | `tool.execution.exhausted-concurrency` |
| `P2-FH-020` | Code execution request that would exceed the implementation-defined maximum number of concurrent code executions. | `tool.execution.exhausted-code` |
| `P2-FH-021` | Tool execution request that would exceed the agent's capability budget. | `tool.execution.quota_exhausted` |

> **Non-normative note.**
The exhausted input tests validate the resource limit enforcement layer
that guards the atomic commit protocol.
Without these tests, exhausted requests could cause resource exhaustion
and compromise system stability.

#### Unavailable input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-022` | Tool execution request for a tool that is not active in the framework plugin registry. | `tool.execution.unavailable_tool` |
| `P2-FH-023` | Tool execution request for a connector that is not active in the connector registry. | `tool.execution.unavailable_connector` |
| `P2-FH-024` | Code execution request that exceeds sandbox memory limits. | `tool.execution.sandbox_failure` |

> **Non-normative note.**
The unavailable input tests validate the framework plugin and connector
lookup layers that guard the atomic commit protocol.
Without these tests, unavailable requests could bypass the registries
and compromise system consistency.

#### Credential custody tests

| Test ID | Description | Expected diagnostic or invariant |
| --- | --- | --- |
| `P2-FH-025` | Agent has connector capability but effect worker lacks `CredentialUse`. | `credential.use.unauthorized` |
| `P2-FH-026` | Typed request changes binding, operation, resource, digest, deadline, nonce, or budget. | `credential.use.scope_mismatch` |
| `P2-FH-027` | Connector asks for a credential, refresh token, authentication header, or bearer token. | `credential.use.export_forbidden` |
| `P2-FH-028` | Accepted connector-use nonce is replayed. | `credential.use.replay` |
| `P2-FH-029` | Pinned connector custodian is unavailable. | `credential.custodian.unavailable` |
| `P2-FH-030` | Connector receipt has invalid correlation, digest, signature, or transport proof. | `credential.receipt.invalid`; result is not admitted |
| `P2-FH-031` | Connector binding is absent, stale, cross-tenant, or unapproved. | Operation is rejected before custodian or external-service contact |

#### Credential non-exposure and egress tests

| Test ID | Security scenario | Expected invariant |
| --- | --- | --- |
| `P2-SEC-001` | Complete successful, denied, failed, cancelled, and crashed connector uses. | Sentinel credential and refresh token, including common encodings, are absent from every inspected product boundary. |
| `P2-SEC-002` | Inspect guest, connector adapter, operator, audit, and support interfaces. | No opaque handle or authentication header is observable. |
| `P2-SEC-003` | Compromised connector changes origin, method, headers, operation, resource, or payload digest. | Custodian rejects the request and the external service is not contacted. |
| `P2-SEC-004` | Host or Port attempts direct authenticated external-service egress. | Network policy denies the operation and emits `credential.egress.bypass`. |
| `P2-SEC-005` | Reuse a connector binding or handle reference across tenant, agent, artifact, or operation. | Sender and scope validation reject the use. |
| `P2-SEC-006` | Retry after an uncertain outcome. | Status is reconciled; binding, custodian, operation, resource, digest, and budget stay pinned; nonce is fresh. |
| `P2-SEC-007` | Enable host-local connector authentication without warning and approval. | Activation fails and separated-custody conformance is not claimed. |

The harness MUST prove both non-transmission and zero sentinel occurrences.
Redaction-only evidence is insufficient.

### 42.4.3 Timeout and cancellation tests

> **Normative definition.**
Timeout and cancellation tests verify that the host correctly handles
tool execution, retrieval, and code execution timeout, cancellation,
and retry under various scenarios.

#### Tool execution timeout tests

| Test ID | Description |
|---------|-------------|
| `P2-TO-001` | Execute a tool and verify that the tool completes before the implementation-defined timeout expires. |
| `P2-TO-002` | Execute a tool and verify that the tool is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-003` | Execute a tool with a custom timeout and verify that the tool completes before the custom timeout. |
| `P2-TO-004` | Execute a tool with a custom timeout and verify that the tool is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-005` | Execute a tool and verify that cancellation leaves no partial state in the durable journal. |

> **Non-normative note.**
Tests `P2-TO-001` through `P2-TO-005` validate the tool execution timeout
behavior defined in section 42.3.

#### Retrieval timeout tests

| Test ID | Description |
|---------|-------------|
| `P2-TO-006` | Execute a retrieval request and verify that the retrieval completes before the implementation-defined timeout expires. |
| `P2-TO-007` | Execute a retrieval request and verify that the retrieval is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-008` | Execute a retrieval request with a custom timeout and verify that the retrieval completes before the custom timeout. |
| `P2-TO-009` | Execute a retrieval request with a custom timeout and verify that the retrieval is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-010` | Execute a retrieval request and verify that cancellation leaves no partial state in the durable journal. |

> **Non-normative note.**
Tests `P2-TO-006` through `P2-TO-010` validate the retrieval timeout
behavior defined in section 42.3.

#### Code execution timeout tests

| Test ID | Description |
|---------|-------------|
| `P2-TO-011` | Execute a code execution request and verify that the code completes before the implementation-defined timeout expires. |
| `P2-TO-012` | Execute a code execution request and verify that the code is cancelled with `tool.execution.timeout` if it exceeds the implementation-defined timeout. |
| `P2-TO-013` | Execute a code execution request with a custom timeout and verify that the code completes before the custom timeout. |
| `P2-TO-014` | Execute a code execution request with a custom timeout and verify that the code is cancelled with `tool.execution.timeout` if it exceeds the custom timeout. |
| `P2-TO-015` | Execute a code execution request and verify that cancellation leaves no partial state in the durable journal. |

> **Non-normative note.**
Tests `P2-TO-011` through `P2-TO-015` validate the code execution timeout
behavior defined in section 42.3.

#### Cancellation tests

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

> **Non-normative note.**
Tests `P2-CA-001` through `P2-CA-008` validate the cancellation behavior
defined in section 42.2.
Each test validates one of the eight cancellation scenarios and verifies
that the host behaves correctly according to the scenario.

### 42.4.4 Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 2 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 2 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 2
contracts interact with many earlier milestones (see the cross-reference
summary in section 42.1).
Without these tests, a Phase 2 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 2
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 7 Phase 1 | Model requests, responses, streaming, and usage | All fixtures continue to pass; model requests can call tools. |
| Milestone 7 Phase 2 | Tool catalogs, retrieval, code execution, and connectors | All fixtures continue to pass; tools are correctly resolved and executed. |
| Milestone 7 Phase 4 | Credential custodians, leases, handles, and receipts | Authenticated connector use preserves typed scope, non-exposure, revocation, and receipt semantics. |
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

> **Normative definition.**
A cross-milestone compatibility test passes if and only if: (1) every
fixture listed in the table above continues to produce the same expected
output as before the Phase 2 contracts were active, and (2) no new
regressions are introduced.
If any fixture fails, the Phase 2 implementation MUST be revised and the
affected milestone MUST be re-validated according to the cross-milestone
revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).

> **Non-normative note.**
The table above includes direct model, connector-custody, policy, plugin,
isolation, provenance, and durable-execution boundaries. Its broader fixture
scope also covers indirect effects through shared subsystems such as the agent
registry, mailboxes, and durable journal.

### 42.4.5 Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 2
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: draft` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 42.4.1 through 42.4.4:

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
| `connector_binding_revision` | Pinned authentication binding revision, if applicable. | Integer or null |
| `credential_use_count` | Number of custodian use requests. | Integer |
| `external_call_count` | Number of fake external-service operations. | Integer |
| `sentinel_scan_result` | Non-exposure scan result, if applicable. | Structured text or null |

> **Non-normative note.**
The evidence format above is consistent with the evidence record format
defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
The `evidence_digest` field enables downstream systems to verify that the
evidence record has not been tampered with after creation.
The `approved_variability` field enables operators to document and
retroactively approve intentional deviations from the baseline, which
is important for cross-milestone compatibility testing where some
variations are acceptable (such as implementation-defined bounded times).

> **Normative definition.**
A run of all Phase 2 integration tests passes if and only if:

1. Every test scenario defined in sections 42.4.1 through 42.4.4 produces
    a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 42.4.4
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 2 integration tests as defined above.
2. A passing run of all cross-milestone compatibility tests as defined
   above.
3. All evidence records for the passing run, signed and stored in the
   durable evidence log.
4. A written report summarizing the test run, including any approved
   variability, regressions, or deviations from the baseline.

> **Non-normative note.**
The evidence requirements above ensure that promotion to `status: normative`
is based on reproducible, auditable evidence rather than subjective
assessment.
The signed evidence records provide a tamper-evident trail that
downstream consumers (such as the provenance and audit layer) can
verify independently.
The written report provides context and narrative that structured
evidence records cannot capture, such as explanations of approved
variability or deviations from the baseline.

### 42.4.6 Cross-reference summary

> **Non-normative note.**
This section's integration tests integrate with the following earlier
chapters:

1. For tool execution validation: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of tool-specific validation tests.
2. For tool execution atomic commits: this section takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of tool-specific atomic commit tests.
3. For tool execution evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of tool-specific evidence tests.
4. For tool execution capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of tool-specific capability tests.
5. Where both sections are applicable and agree, they are mutually
    reinforcing.

## Variability register

The following table lists every implementation-defined choice,
non-normative disposition, and permitted presentation documented in this
chapter.

| Item | Location | Nature | Constraint |
|------|----------|--------|------------|
| Test execution order | Section 42.4 | MAY | Must cover all required scenarios. Order is informational. |
| Test isolation strategy | Section 42.4 | MAY | May run tests in parallel or sequentially. Must not leave partial state. |
| Evidence record hash algorithm | Section 42.4 | MAY | Must be deterministic. Documented in conformance profile. |
| Evidence record signature algorithm | Section 42.4 | MAY | Must be cryptographically secure. Documented in conformance profile. |
| Cross-milestone fixture execution order | Section 42.4 | MAY | Must include all fixtures listed in section 42.4.4. Order is informational. |
| Approved variability documentation format | Section 42.4 | MAY | Must include scenario, deviation, rationale. Format is informational. |
| Regression baseline selection | Section 42.4 | MAY | Must use most recent normative baseline. Documented in conformance profile. |
| Custodian fixture transport | Section 42.4 | MAY | Must exercise the product's real authenticated custody boundary. |
| Sentinel encoding scan | Section 42.4 | MUST | Must cover raw, base64, hex, URL-encoded, and structured forms and accompany the non-transmission proof. |
