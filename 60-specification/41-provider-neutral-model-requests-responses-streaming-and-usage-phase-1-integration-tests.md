---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests"
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
  - integration-tests
aliases:
  - "M7-P1 Phase 1 Integration Tests"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It defines the integration tests that verify provider-neutral model
requests, responses, streaming, and usage across its real dependency
boundaries.

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

## 41.4 Phase 1 Integration Tests

### 41.4.1 Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes provider-neutral
model requests, responses, streaming, and usage under normal operating
conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Model request creation flow

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

> **Non-normative note.**
Tests `P1-SF-001` through `P1-SF-010` exercise the full model request
creation flow defined in section 41.2.

#### Streaming response flow

| Test ID | Description |
|---------|-------------|
| `P1-SF-011` | Create a model request and verify that streaming events are emitted for each text delta. |
| `P1-SF-012` | Create a model request with tool definitions and verify that streaming events are emitted for each tool request delta. |
| `P1-SF-013` | Create a model request and verify that a finish event is emitted when the response is complete. |
| `P1-SF-014` | Create a model request and verify that a `model.response.completed` signal is emitted when the response is finalized. |
| `P1-SF-015` | Create a model request and verify that usage is recorded after the response is finalized. |

> **Non-normative note.**
Tests `P1-SF-011` through `P1-SF-015` validate the full streaming response
flow defined in section 41.2.
Each test validates one of the five streaming operations and verifies
that the host behaves correctly according to the operation.

#### Cancellation flow

| Test ID | Description |
|---------|-------------|
| `P1-SF-016` | Create a model request and cancel it before the response is finalized and verify that a `model.request.cancelled` signal is emitted. |
| `P1-SF-017` | Create a model request and cancel it after the response is finalized and verify that the cancellation is ignored. |
| `P1-SF-018` | Create two model requests and cancel one and verify that the other continues. |
| `P1-SF-019` | Create a model request with a deadline and cancel it before the deadline expires and verify that the cancellation is processed. |
| `P1-SF-020` | Create a model request with a deadline and cancel it after the deadline expires and verify that the cancellation is ignored. |

> **Non-normative note.**
Tests `P1-SF-016` through `P1-SF-020` exercise the full cancellation flow
defined in section 41.2.
Each test validates one of the five cancellation scenarios and verifies
that the host behaves correctly according to the scenario.

### 41.4.2 Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

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

> **Normative definition.**
Each malformed input test MUST verify that the host: (1) rejects the
request or response with the specified diagnostic, (2) does NOT create a
partial request or response state, and (3) does NOT leave any live actor
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
| `P1-FH-010` | Model request with unregistered `provider`. | `model.request.unavailable_provider` |
| `P1-FH-011` | Model request with unavailable `model`. | `model.request.unavailable_model` |
| `P1-FH-012` | Response with tool requests that do not match `tool_definitions`. | `model.request.tool_call_mismatch` |
| `P1-FH-013` | Response with `structured_value` that does not conform to `structured_output_schema`. | `model.request.invalid_structured_output` |

> **Non-normative note.**
The incompatible input tests validate the semantic validation layer that
guards the atomic commit protocol.
Without these tests, an incompatible request could cause inconsistent
state or leave partial state in the durable journal.

#### Conflicting input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-014` | Two model requests with the same `request_id` submitted concurrently. | `model.request.duplicate-id` for the second request. |
| `P1-FH-015` | Two cancellation requests for the same `request_id` submitted concurrently. | `model.request.conflicting-cancellation` for the second cancellation. |

> **Non-normative note.**
The conflicting input tests validate the deduplication and conflict
resolution layer that guards the atomic commit protocol.
Without these tests, conflicting requests could cause inconsistent
state or leave partial state in the durable journal.

#### Unauthorized input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-016` | Model request whose `agent_address` does not have the `model.request.create` capability. | `model.request.unauthorized` |
| `P1-FH-017` | Model request that grants cross-tenant tool access. | `model.request.cross-tenant-tool` |
| `P1-FH-018` | Model request that grants cross-tenant result sharing. | `model.request.cross-tenant-result` |

> **Non-normative note.**
The unauthorized input tests validate the capability enforcement layer
that guards the atomic commit protocol.
Without these tests, unauthorized requests could bypass the capability
policy and compromise system security.

#### Exhausted input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-019` | Model request that would exceed the implementation-defined maximum number of concurrent requests. | `model.request.exhausted-concurrency` |
| `P1-FH-020` | Model request that would exceed the implementation-defined maximum number of concurrent streams. | `model.request.exhausted-stream` |

> **Non-normative note.**
The exhausted input tests validate the resource limit enforcement layer
that guards the atomic commit protocol.
Without these tests, exhausted requests could cause resource exhaustion
and compromise system stability.

#### Unavailable input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P1-FH-021` | Model request whose `provider` is not active in the adapter registry. | `model.request.unavailable-provider` |
| `P1-FH-022` | Model request whose `model` is not available from the provider. | `model.request.unavailable-model` |

> **Non-normative note.**
The unavailable input tests validate the provider adapter lookup layer
that guards the atomic commit protocol.
Without these tests, unavailable requests could bypass the adapter
registry and compromise system consistency.

### 41.4.3 Timeout and cancellation tests

> **Normative definition.**
Timeout and cancellation tests verify that the host correctly handles
model request timeout, cancellation, and late response under various
scenarios.

#### Model request timeout tests

| Test ID | Description |
|---------|-------------|
| `P1-TO-001` | Create a model request and verify that the request is completed before the implementation-defined timeout expires. |
| `P1-TO-002` | Create a model request and verify that the request is cancelled with `model.request.timeout` if it exceeds the implementation-defined timeout. |
| `P1-TO-003` | Create a model request with a deadline and verify that the request is completed before the deadline. |
| `P1-TO-004` | Create a model request with a deadline and verify that the request is accepted with `model.request.late-response` if it exceeds the deadline. |
| `P1-TO-005` | Create a model request with a deadline and verify that the request is cancelled with `model.request.timeout` if it exceeds the implementation-defined timeout. |

> **Non-normative note.**
Tests `P1-TO-001` through `P1-TO-005` validate the model request timeout
behavior defined in section 41.2.
Each test validates one of the five timeout scenarios and verifies
that the host behaves correctly according to the scenario.

#### Cancellation tests

| Test ID | Description |
|---------|-------------|
| `P1-CA-001` | Cancel a model request and verify that the cancellation is processed. |
| `P1-CA-002` | Cancel a model request after the response is finalized and verify that the cancellation is ignored. |
| `P1-CA-003` | Cancel two model requests concurrently and verify that only one cancellation is processed. |
| `P1-CA-004` | Verify that a `model.request.cancelled` signal is emitted when a model request is cancelled. |

> **Non-normative note.**
Tests `P1-CA-001` through `P1-CA-004` validate the model request
cancellation behavior defined in section 41.2.
Each test validates one of the four cancellation scenarios and verifies
that the host behaves correctly according to the scenario.

### 41.4.4 Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 1 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 1 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 1
contracts interact with many earlier milestones (see the cross-reference
summary in section 41.1).
Without these tests, a Phase 1 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 1
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

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

> **Normative definition.**
A cross-milestone compatibility test passes if and only if: (1) every
fixture listed in the table above continues to produce the same expected
output as before the Phase 1 contracts were active, and (2) no new
regressions are introduced.
If any fixture fails, the Phase 1 implementation MUST be revised and the
affected milestone MUST be re-validated according to the cross-milestone
revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).

> **Non-normative note.**
The table above lists 11 fixture scopes from 6 milestones that are affected
by the Phase 1 contracts.
This is consistent with the cross-reference summary in section 41.1, which
identifies 6 direct integration points with earlier chapters.
The broader fixture scope accounts for indirect effects through shared
subsystems (such as the agent registry, mailboxes, and durable journal).

### 41.4.5 Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 1
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: draft` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 41.4.1 through 41.4.5:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P1-SF-001`). | String. |
| `test_objective` | The test objective this scenario addresses. | String. |
| `setup` | The test setup description (input data, preconditions). | Structured text. |
| `expected_outcome` | The expected observable behavior. | Structured text. |
| `actual_outcome` | The actual observable behavior. | Structured text. |
| `result` | `pass`, `fail`, or `blocked`. | Enum. |
| `evidence_digest` | A deterministic hash of the evidence record. | Hash digest. |
| `timestamp` | The ISO 8601 timestamp of test execution. | ISO 8601 string. |
| `regression` | For cross-milestone tests, whether the test previously passed. | Boolean. |
| `approved_variability` | For cross-milestone tests, any approved variability from the baseline. | Structured text. |

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
A run of all Phase 1 integration tests passes if and only if:

1. Every test scenario defined in sections 41.4.1 through 41.4.5 produces
   a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 41.4.4
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 1 integration tests as defined above.
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

### 41.4.6 Cross-reference summary

> **Non-normative note.**
This section's integration tests integrate with the following earlier
chapters:

1. For model request validation: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of model-specific validation tests.
2. For model request atomic commits: this section takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of model-specific atomic commit tests.
3. For model request evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of model-specific evidence tests.
4. For model request capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of model-specific capability tests.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
