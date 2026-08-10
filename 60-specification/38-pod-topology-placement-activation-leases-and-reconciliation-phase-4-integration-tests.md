---
title: "Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-04
  - pod-topology
  - placement
  - activation-leases
  - reconciliation
  - integration-tests
aliases:
  - "M6-P4 Phase 4 Integration Tests"
---

# Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-04-pod-topology-placement-activation-leases-and-reconciliation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It defines the integration tests that verify pod topology placement
activation leases and reconciliation across its real dependency boundaries.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
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
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md).

## 38.4 Phase 4 Integration Tests

### Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes pod topology
placement activation leases and reconciliation under normal operating
conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Topology directive creation flow

| Test ID | Description |
|---------|-------------|
| `P4-SF-001` | Create a topology directive with a valid topology directive and verify that all required validation rules pass (topology owner resolution, node list non-empty, node agent resolution, dependency validation, activation mode validation, lifecycle policy validation). |
| `P4-SF-002` | Create a topology directive with a deterministic `topology_identity` and verify that two identical directives produce the same `topology_identity`. |
| `P4-SF-003` | Create a topology directive with all three activation modes (`durable`, `ephemeral`, `manual`) and verify that each mode is correctly recorded in the topology directive. |
| `P4-SF-004` | Create a topology directive with attenuated delegation grants and verify that the topology nodes' grants are strictly a subset of the topology owner's grants as defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). |
| `P4-SF-005` | Create a topology directive with a valid `nodes` list and verify that the nodes are recorded in the evidence emission. |

> **Non-normative note.**
Tests `P4-SF-001` through `P4-SF-005` exercise the full topology directive
creation flow defined in section 38.1.
Test `P4-SF-001` is the primary creation test and MUST verify the complete
validation sequence defined in section 38.2.

#### Reconciliation flow

| Test ID | Description |
|---------|-------------|
| `P4-SF-006` | Verify that reconciliation correctly creates live agent instances for `missing` nodes according to the node's `activation_mode`. |
| `P4-SF-007` | Verify that reconciliation correctly terminates live agent instances for `extra` nodes. |
| `P4-SF-008` | Verify that reconciliation correctly applies the node's `lifecycle_policy` for `failed` nodes. |
| `P4-SF-009` | Verify that reconciliation correctly marks `stale` nodes and applies the node's `lifecycle_policy`. |
| `P4-SF-010` | Verify that reconciliation correctly defers creation of `dependency-blocked` nodes until dependencies are resolved. |

> **Non-normative note.**
Tests `P4-SF-006` through `P4-SF-010` validate the full reconciliation
flow defined in section 38.2.
Each test validates one of the seven reconciliation rules and verifies
that the host behaves correctly according to the rule.

#### Activation lease flow

| Test ID | Description |
|---------|-------------|
| `P4-SF-011` | Verify that an activation lease is correctly issued for a reconciliation pass and that the lease includes all required fields. |
| `P4-SF-012` | Verify that an activation lease with a lower `fence_token` than the current fence token is rejected with `topology.lease.expired-fence`. |
| `P4-SF-013` | Verify that an activation lease with a past `expires_at` timestamp is rejected with `topology.lease.expired-timeout`. |
| `P4-SF-014` | Verify that an activation lease is correctly renewed before expiration and that the renewed lease extends the `expires_at` timestamp. |
| `P4-SF-015` | Verify that an activation lease is correctly transferred to another host and that the new host's lease has an incremented `fence_token`. |

> **Non-normative note.**
Tests `P4-SF-011` through `P4-SF-015` exercise the full activation lease
flow defined in section 38.2.
Each test validates one of the five lease operations and verifies that
the host behaves correctly according to the operation.

#### Topology versioning flow

| Test ID | Description |
|---------|-------------|
| `P4-SF-016` | Create a topology directive with `topology_version: 1` and verify that the version is recorded in the durable journal. |
| `P4-SF-017` | Create a topology directive with `topology_version: 2` and verify that the version is greater than `topology_version: 1`. |
| `P4-SF-018` | Create a topology directive with `topology_version: 1` (duplicate) and verify that the directive is rejected with `topology.directive.duplicate-version`. |
| `P4-SF-019` | Roll back to `topology_version: 1` by creating a new directive that copies version 1's nodes and verify that the rollback is recorded in the durable journal. |
| `P4-SF-020` | Verify that topology evidence is emitted for every topology directive admission, rejection, and reconciliation pass. |

> **Non-normative note.**
Tests `P4-SF-016` through `P4-SF-020` validate the full topology versioning
flow defined in section 38.2.
Each test validates one of the five versioning operations and verifies
that the host behaves correctly according to the operation.

### Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-001` | Topology directive with missing `topology_owner` field. | `topology.directive.malformed` |
| `P4-FH-002` | Topology directive with empty `nodes` list. | `topology.directive.malformed-nodes` |
| `P4-FH-003` | Topology directive with invalid `node_id` format. | `topology.directive.malformed-node-id` |
| `P4-FH-004` | Topology directive with invalid `agent_address` format. | `topology.directive.malformed-agent-address` |
| `P4-FH-005` | Topology directive with unknown `role` value. | `topology.directive.malformed-role` |
| `P4-FH-006` | Topology directive with unknown `activation_mode` value. | `topology.directive.malformed-activation-mode` |
| `P4-FH-007` | Topology directive with unknown `lifecycle_policy` value. | `topology.directive.malformed-lifecycle-policy` |
| `P4-FH-008` | Topology node with missing required fields. | `topology.node.malformed` |
| `P4-FH-009` | Topology node with invalid `dependencies` list. | `topology.node.malformed-dependencies` |
| `P4-FH-010` | Activation lease with missing required fields. | `topology.lease.malformed` |
| `P4-FH-011` | Activation lease with past `expires_at` timestamp. | `topology.lease.malformed-expiry` |

> **Normative definition.**
Each malformed input test MUST verify that the host: (1) rejects the
directive with the specified diagnostic, (2) does NOT create a partial
registry entry or journal record, and (3) does NOT leave any live actor
instance in an indeterminate state.

> **Non-normative note.**
The malformed input tests validate the schema validation layer that guards
the atomic commit protocol.
Without these tests, a malformed directive could cause inconsistent state
or leave partial state in the durable journal, violating the atomicity
guarantees defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

#### Incompatible input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-012` | Topology directive whose `agent_address` does not resolve to an active agent. | `topology.directive.incompatible-agent` |
| `P4-FH-013` | Topology node whose `agent_address` does not resolve to an active agent. | `topology.node.incompatible-agent` |
| `P4-FH-014` | Topology node whose `dependencies` reference non-existent `node_id` values. | `topology.node.incompatible-dependency` |
| `P4-FH-015` | Topology directive whose `nodes` list contains a circular dependency. | `topology.node.incompatible-circular-dependency` |

> **Non-normative note.**
The incompatible input tests validate the semantic validation layer that
guards the atomic commit protocol.
Without these tests, an incompatible directive could cause inconsistent
state or leave partial state in the durable journal.

#### Conflicting input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-016` | Two topology directives with the same `topology_version` submitted concurrently. | `topology.directive.duplicate-version` for the second directive. |
| `P4-FH-017` | Two topology directives with the same `node_id` submitted concurrently. | `topology.node.duplicate-node-id` for the second directive. |
| `P4-FH-018` | Two activation leases with lower `fence_token` than the current fence token for the same `node_id`. | `topology.lease.expired-fence` for the second lease. |
| `P4-FH-019` | Two activation leases with past `expires_at` timestamp. | `topology.lease.expired-timeout` for the second lease. |
| `P4-FH-020` | Two reconciliation passes attempt to modify the same `node_id` concurrently. | `topology.reconciliation.conflict` for the second pass. |

> **Non-normative note.**
The conflicting input tests validate the deduplication and conflict
resolution layer that guards the atomic commit protocol.
Without these tests, conflicting directives could cause inconsistent
state or leave partial state in the durable journal.

#### Unauthorized input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-021` | Topology directive whose `topology_owner` does not have the `topology.directive.create` capability. | `topology.directive.unauthorized` |
| `P4-FH-022` | Topology node whose `owner` does not have the `topology.node.create` capability. | `topology.node.unauthorized` |
| `P4-FH-023` | Activation lease whose `host_id` does not have the `topology.lease.acquire` capability. | `topology.lease.unauthorized` |

> **Non-normative note.**
The unauthorized input tests validate the capability enforcement layer
that guards the atomic commit protocol.
Without these tests, unauthorized directives could bypass the capability
policy and compromise system security.

#### Exhausted input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-024` | Topology directive that would exceed the implementation-defined maximum number of nodes per topology. | `topology.directive.exhausted-nodes` |
| `P4-FH-025` | Topology node that would exceed the implementation-defined maximum concurrency per topology. | `topology.node.exhausted-concurrency` |
| `P4-FH-026` | Host that would exceed the implementation-defined maximum number of concurrent leases. | `topology.lease.exhausted-concurrency` |

> **Non-normative note.**
The exhausted input tests validate the resource limit enforcement layer
that guards the atomic commit protocol.
Without these tests, exhausted directives could cause resource exhaustion
and compromise system stability.

#### Unavailable input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P4-FH-027` | Topology directive whose `topology_owner` is not active in the durable registry. | `topology.directive.unavailable` |
| `P4-FH-028` | Topology node whose `agent_address` is not active in the durable registry. | `topology.node.unavailable-agent` |
| `P4-FH-029` | Activation lease whose `host_id` is not active in the host registry. | `topology.lease.unavailable-host` |

> **Non-normative note.**
The unavailable input tests validate the agent registry lookup layer
that guards the atomic commit protocol.
Without these tests, unavailable directives could bypass the agent
registry and compromise system consistency.

### Timeout and cancellation tests

> **Normative definition.**
Timeout and cancellation tests verify that the host correctly handles
topology directive timeout, reconciliation cancellation, and node
cancellation under various `lifecycle_policy` settings.

#### Topology directive timeout tests

| Test ID | Description |
|---------|-------------|
| `P4-TO-001` | Create a topology directive and verify that the directive is accepted before the implementation-defined timeout expires. |
| `P4-TO-002` | Create a topology directive and verify that the directive is rejected with `topology.directive.timeout` if it exceeds the implementation-defined timeout. |
| `P4-TO-003` | Create a topology directive with `lifecycle_policy: terminate-on-topology-revoke` and verify that the directive is terminated when the topology is revoked. |
| `P4-TO-004` | Create a topology directive with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that the directive is allowed to complete before being terminated. |
| `P4-TO-005` | Create a topology directive with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that the directive is allowed to continue but its results are excluded from aggregation. |

> **Non-normative note.**
Tests `P4-TO-001` through `P4-TO-005` validate the topology directive
timeout behavior defined in section 38.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Reconciliation cancellation tests

| Test ID | Description |
|---------|-------------|
| `P4-CA-001` | Cancel a reconciliation pass with `lifecycle_policy: terminate-on-topology-revoke` and verify that all live agent instances are terminated. |
| `P4-CA-002` | Cancel a reconciliation pass with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that live agent instances are allowed to complete before being terminated. |
| `P4-CA-003` | Cancel a reconciliation pass with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that live agent instances are allowed to complete but their results are excluded from aggregation. |
| `P4-CA-004` | Verify that a `topology.reconciliation.cancelled` event is emitted when a reconciliation pass is cancelled. |

> **Non-normative note.**
Tests `P4-CA-001` through `P4-CA-004` validate the reconciliation
cancellation behavior defined in section 38.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Node cancellation tests

| Test ID | Description |
|---------|-------------|
| `P4-NA-001` | Cancel a topology node with `lifecycle_policy: terminate-on-topology-revoke` and verify that the live agent instance is terminated. |
| `P4-NA-002` | Cancel a topology node with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that the live agent instance is allowed to complete before being terminated. |
| `P4-NA-003` | Cancel a topology node with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that the live agent instance is allowed to complete but its results are excluded from aggregation. |
| `P4-NA-004` | Verify that a `topology.node.cancelled` event is emitted when a topology node is cancelled. |

> **Non-normative note.**
Tests `P4-NA-001` through `P4-NA-004` validate the node cancellation
behavior defined in section 38.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

### Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 4 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 4 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 4
contracts interact with many earlier milestones (see the cross-reference
summary in section 38.1).
Without these tests, a Phase 4 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 4
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 6 Phase 1 | Signal envelopes, causality routing, and delivery | All fixtures continue to pass; topology node signals are correctly routed through the signal envelope mechanism. |
| Milestone 6 Phase 1 | Actions, instructions, validation, plans, and results | All fixtures continue to pass; topology directive validation is consistent with the actions validation flow. |
| Milestone 6 Phase 1 | State operations, patches, revisions, and conflicts | All fixtures continue to pass; topology node state is correctly managed through the state operations mechanism. |
| Milestone 6 Phase 1 | Directives, strategies, continuations, and terminal states | All fixtures continue to pass; topology directive terminal states are consistent with the directive terminal states. |
| Milestone 6 Phase 1 | Deterministic reducer semantics and milestone acceptance | All fixtures continue to pass; topology node results are correctly processed by the deterministic reducer. |
| Milestone 6 Phase 1 | Extism invocation boundary instances and output validation | All fixtures continue to pass; topology node live agents are subject to the same Extism invocation boundary. |
| Milestone 6 Phase 1 | Mailboxes, ordering, bounds, fairness, and turn leases | All fixtures continue to pass; topology node lifecycle events are correctly delivered through mailboxes. |
| Milestone 6 Phase 1 | Agent registry, activation, cancellation, and completion | All fixtures continue to pass; topology node registry entries are consistent with the agent registry contract. |
| Milestone 6 Phase 1 | Sensors, schedules, timers, and external signal ingress | All fixtures continue to pass; topology node notifications are correctly delivered through the sensor mechanism. |
| Milestone 6 Phase 1 | Single-agent host flow and milestone acceptance | All fixtures continue to pass; topology node lifecycle is consistent with the single-agent host flow. |
| Milestone 6 Phase 1 | Revisioned snapshots, journals, history, and storage contracts | All fixtures continue to pass; topology node snapshots are correctly captured and journaled. |
| Milestone 6 Phase 1 | Atomic state journal and directive-outbox commits | All fixtures continue to pass; topology directive atomic commits are consistent with the journal protocol. |
| Milestone 6 Phase 1 | Effect handlers, attempts, idempotency, and result signals | All fixtures continue to pass; topology node lifecycle events are correctly processed as effect handlers. |
| Milestone 6 Phase 1 | Retry, timer, recovery, replay, hibernate, and migration | All fixtures continue to pass; topology node restart policy does not conflict with the retry mechanism. |
| Milestone 6 Phase 1 | Crash injection, durable effects, and milestone acceptance | All fixtures continue to pass; topology node lifecycle events are durable across crashes. |
| Milestone 6 Phase 2 | Child lifecycle, cancellation, monitoring, and restart policy | All fixtures continue to pass; topology node child agents are consistent with the child lifecycle contract. |
| Milestone 6 Phase 3 | Fan-out fan-in delegation and result aggregation | All fixtures continue to pass; topology node fan-out coordination is consistent with the fan-out contract. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; topology node grants are consistent with the threat model. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; topology node grant attenuation is consistent with the capability policy. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; topology node live agents are consistent with the framework plugin model. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; topology node live agents are subject to the same WASI restrictions. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; topology node lifecycle evidence is correctly signed and audited. |
| Milestone 5 | Agent identity, addressing, ownership, and dependency relations | All fixtures continue to pass; topology node addresses and relationships are consistent with the identity model. |

> **Normative definition.**
A cross-milestone compatibility test passes if and only if: (1) every
fixture listed in the table above continues to produce the same expected
output as before the Phase 4 contracts were active, and (2) no new
regressions are introduced.
If any fixture fails, the Phase 4 implementation MUST be revised and the
affected milestone MUST be re-validated according to the cross-milestone
revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).

> **Non-normative note.**
The table above lists 23 fixture scopes from 7 milestones that are affected
by the Phase 4 contracts.
This is consistent with the cross-reference summary in section 38.1, which
identifies 12 direct integration points with earlier chapters.
The broader fixture scope accounts for indirect effects through shared
subsystems (such as the agent registry, mailboxes, and durable journal).

### Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 4
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: draft` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 38.4.1 through 38.4.5:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P4-SF-001`). | String. |
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
A run of all Phase 4 integration tests passes if and only if:

1. Every test scenario defined in sections 38.4.1 through 38.4.5 produces
   a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 38.4.6
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 4 integration tests as defined above.
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

### Cross-reference summary

> **Non-normative note.**
This section's integration tests integrate with the following earlier
chapters:

1. For topology directive and node validation: this section takes
   precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of topology-specific validation tests.
2. For topology directive and node atomic commits: this section takes
   precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of topology-specific atomic commit tests.
3. For topology directive and node evidence emission: this section takes
   precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of topology-specific evidence tests.
4. For topology node live agent lifecycle: this section takes precedence
   over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of topology node-specific lifecycle tests.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.
