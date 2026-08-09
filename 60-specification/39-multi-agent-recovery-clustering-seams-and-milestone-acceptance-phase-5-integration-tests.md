---
title: "Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-05
  - recovery
  - clustering
  - seams
  - milestone-acceptance
  - integration-tests
aliases:
  - "M6-P5 Phase 5 Integration Tests"
---

# Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-05-multi-agent-recovery-clustering-seams-and-milestone-acceptance.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It defines the integration tests that verify multi-agent recovery clustering
seams and milestone acceptance across its real dependency boundaries.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
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
[Pod Topology Placement Activation Leases And Reconciliation Phase 4 Integration Tests](38-pod-topology-placement-activation-leases-and-reconciliation-phase-4-integration-tests.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md).

## 39.4 Phase 5 Integration Tests

### 39.4.1 Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes multi-agent
recovery clustering seams and milestone acceptance under normal operating
conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Parent/child creation and lifecycle flow

| Test ID | Description |
|---------|-------------|
| `P5-SF-001` | Create a parent agent and verify that child agents are correctly spawned with the expected lifecycle policies. |
| `P5-SF-002` | Create a topology with multiple child agents and verify that all children are created and running. |
| `P5-SF-003` | Cancel a parent agent and verify that all child agents are cancelled. |
| `P5-SF-004` | Restart a child agent and verify that the restart is recorded in the durable journal. |
| `P5-SF-005` | Delegate work from a parent agent to a child agent and verify that the delegation is recorded. |
| `P5-SF-006` | Fan-out work to multiple child agents and verify that all children are created. |
| `P5-SF-007` | Fan-in results from multiple child agents and verify that results are aggregated. |
| `P5-SF-008` | Trigger a terminal state for a topology and verify that all child agents are terminated. |
| `P5-SF-009` | Create a topology with a child agent and verify that the child's lifecycle events are observable. |

> **Non-normative note.**
Tests `P5-SF-001` through `P5-SF-009` exercise the full parent/child
creation, monitoring, cancellation, restart, delegation, fan-out, fan-in,
and terminal aggregation flow defined in section 39.2.

#### Restart and recovery flow

| Test ID | Description |
|---------|-------------|
| `P5-SF-010` | Simulate a host restart and verify that live placement is correctly reconstructed from durable topology. |
| `P5-SF-011` | Simulate a host restart with an in-flight coordination and verify that the coordination is retained. |
| `P5-SF-012` | Simulate a host restart with an expired activation lease and verify that the node is marked as stale. |
| `P5-SF-013` | Simulate a host restart with a failed live agent and verify that the node is restarted according to its lifecycle policy. |
| `P5-SF-014` | Simulate a host restart with a duplicate topology version and verify that the duplicate is rejected. |
| `P5-SF-015` | Simulate a host restart with delayed lifecycle events and verify that the events are processed correctly. |

> **Non-normative note.**
Tests `P5-SF-010` through `P5-SF-015` validate the recovery from clean
state flow defined in section 39.2.
Each test simulates a different failure scenario and verifies that the
host correctly recovers from durable topology.

#### Activation lease flow

| Test ID | Description |
|---------|-------------|
| `P5-SF-016` | Verify that an activation lease is correctly issued for a reconciliation pass and that the lease includes all required fields. |
| `P5-SF-017` | Verify that an activation lease with a lower `fence_token` than the current fence token is rejected with `topology.lease.expired-fence`. |
| `P5-SF-018` | Verify that an activation lease with a past `expires_at` timestamp is rejected with `topology.lease.expired-timeout`. |
| `P5-SF-019` | Verify that an activation lease is correctly renewed before expiration and that the renewed lease extends the `expires_at` timestamp. |
| `P5-SF-020` | Verify that an activation lease is correctly expired and that the node is marked as stale. |

> **Non-normative note.**
Tests `P5-SF-016` through `P5-SF-020` exercise the full activation lease
flow defined in section 39.1.
Each test validates one of the five lease operations and verifies that
the host behaves correctly according to the operation.

### 39.4.2 Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P5-FH-001` | Topology directive with missing `topology_owner` field. | `topology.directive.malformed` |
| `P5-FH-002` | Topology directive with empty `nodes` list. | `topology.directive.malformed-nodes` |
| `P5-FH-003` | Topology directive with invalid `node_id` format. | `topology.directive.malformed-node-id` |
| `P5-FH-004` | Topology directive with invalid `agent_address` format. | `topology.directive.malformed-agent-address` |
| `P5-FH-005` | Topology directive with unknown `role` value. | `topology.directive.malformed-role` |
| `P5-FH-006` | Topology directive with unknown `activation_mode` value. | `topology.directive.malformed-activation-mode` |
| `P5-FH-007` | Topology directive with unknown `lifecycle_policy` value. | `topology.directive.malformed-lifecycle-policy` |
| `P5-FH-008` | Topology node with missing required fields. | `topology.node.malformed` |
| `P5-FH-009` | Topology node with invalid `dependencies` list. | `topology.node.malformed-dependencies` |
| `P5-FH-010` | Activation lease with missing required fields. | `topology.lease.malformed` |
| `P5-FH-011` | Activation lease with past `expires_at` timestamp. | `topology.lease.malformed-expiry` |

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
| `P5-FH-012` | Topology directive whose `agent_address` does not resolve to an active agent. | `topology.directive.incompatible-agent` |
| `P5-FH-013` | Topology node whose `agent_address` does not resolve to an active agent. | `topology.node.incompatible-agent` |
| `P5-FH-014` | Topology node whose `dependencies` reference non-existent `node_id` values. | `topology.node.incompatible-dependency` |
| `P5-FH-015` | Topology directive whose `nodes` list contains a circular dependency. | `topology.node.incompatible-circular-dependency` |

> **Non-normative note.**
The incompatible input tests validate the semantic validation layer that
guards the atomic commit protocol.
Without these tests, an incompatible directive could cause inconsistent
state or leave partial state in the durable journal.

#### Conflicting input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P5-FH-016` | Two topology directives with the same `topology_version` submitted concurrently. | `topology.directive.duplicate-version` for the second directive. |
| `P5-FH-017` | Two topology directives with the same `node_id` submitted concurrently. | `topology.node.duplicate-node-id` for the second directive. |
| `P5-FH-018` | Two activation leases with lower `fence_token` than the current fence token for the same `node_id`. | `topology.lease.expired-fence` for the second lease. |
| `P5-FH-019` | Two activation leases with past `expires_at` timestamp. | `topology.lease.expired-timeout` for the second lease. |
| `P5-FH-020` | Two reconciliation passes attempt to modify the same `node_id` concurrently. | `topology.reconciliation.conflict` for the second pass. |

> **Non-normative note.**
The conflicting input tests validate the deduplication and conflict
resolution layer that guards the atomic commit protocol.
Without these tests, conflicting directives could cause inconsistent
state or leave partial state in the durable journal.

#### Unauthorized input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P5-FH-021` | Topology directive whose `topology_owner` does not have the `topology.directive.create` capability. | `topology.directive.unauthorized` |
| `P5-FH-022` | Topology node whose `owner` does not have the `topology.node.create` capability. | `topology.node.unauthorized` |
| `P5-FH-023` | Activation lease whose `host_id` does not have the `topology.lease.acquire` capability. | `topology.lease.unauthorized` |
| `P5-FH-024` | Topology directive that grants cross-tenant routing access. | `topology.directive.cross-tenant-route` |
| `P5-FH-025` | Topology directive that grants cross-tenant relationship access. | `topology.directive.cross-tenant-relationship` |
| `P5-FH-026` | Topology directive that grants cross-tenant grant access. | `topology.directive.cross-tenant-grant` |
| `P5-FH-027` | Topology directive that grants cross-tenant result access. | `topology.directive.cross-tenant-result` |

> **Non-normative note.**
The unauthorized input tests validate the capability enforcement layer
that guards the atomic commit protocol.
Without these tests, unauthorized directives could bypass the capability
policy and compromise system security.

#### Exhausted input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P5-FH-028` | Topology directive that would exceed the implementation-defined maximum number of nodes per topology. | `topology.directive.exhausted-nodes` |
| `P5-FH-029` | Topology node that would exceed the implementation-defined maximum concurrency per topology. | `topology.node.exhausted-concurrency` |
| `P5-FH-030` | Host that would exceed the implementation-defined maximum number of concurrent leases. | `topology.lease.exhausted-concurrency` |
| `P5-FH-031` | Live agent mailbox queue that exceeds the implementation-defined maximum. | `topology.mailbox.exhausted-queue` |
| `P5-FH-032` | Topology node that exceeds the implementation-defined maximum retries. | `topology.retry.exhausted` |

> **Non-normative note.**
The exhausted input tests validate the resource limit enforcement layer
that guards the atomic commit protocol.
Without these tests, exhausted directives could cause resource exhaustion
and compromise system stability.

#### Unavailable input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P5-FH-033` | Topology directive whose `topology_owner` is not active in the durable registry. | `topology.directive.unavailable` |
| `P5-FH-034` | Topology node whose `agent_address` is not active in the durable registry. | `topology.node.unavailable-agent` |
| `P5-FH-035` | Activation lease whose `host_id` is not active in the host registry. | `topology.lease.unavailable-host` |

> **Non-normative note.**
The unavailable input tests validate the agent registry lookup layer
that guards the atomic commit protocol.
Without these tests, unavailable directives could bypass the agent
registry and compromise system consistency.

### 39.4.3 Timeout and cancellation tests

> **Normative definition.**
Timeout and cancellation tests verify that the host correctly handles
topology directive timeout, reconciliation cancellation, and node
cancellation under various `lifecycle_policy` settings.

#### Topology directive timeout tests

| Test ID | Description |
|---------|-------------|
| `P5-TO-001` | Create a topology directive and verify that the directive is accepted before the implementation-defined timeout expires. |
| `P5-TO-002` | Create a topology directive and verify that the directive is rejected with `topology.directive.timeout` if it exceeds the implementation-defined timeout. |
| `P5-TO-003` | Create a topology directive with `lifecycle_policy: terminate-on-topology-revoke` and verify that the directive is terminated when the topology is revoked. |
| `P5-TO-004` | Create a topology directive with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that the directive is allowed to complete before being terminated. |
| `P5-TO-005` | Create a topology directive with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that the directive is allowed to continue but its results are excluded from aggregation. |

> **Non-normative note.**
Tests `P5-TO-001` through `P5-TO-005` validate the topology directive
timeout behavior defined in section 39.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Reconciliation cancellation tests

| Test ID | Description |
|---------|-------------|
| `P5-CA-001` | Cancel a reconciliation pass with `lifecycle_policy: terminate-on-topology-revoke` and verify that all live agent instances are terminated. |
| `P5-CA-002` | Cancel a reconciliation pass with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that live agent instances are allowed to complete before being terminated. |
| `P5-CA-003` | Cancel a reconciliation pass with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that live agent instances are allowed to complete but their results are excluded from aggregation. |
| `P5-CA-004` | Verify that a `topology.reconciliation.cancelled` event is emitted when a reconciliation pass is cancelled. |

> **Non-normative note.**
Tests `P5-CA-001` through `P5-CA-004` validate the reconciliation
cancellation behavior defined in section 39.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

#### Node cancellation tests

| Test ID | Description |
|---------|-------------|
| `P5-NA-001` | Cancel a topology node with `lifecycle_policy: terminate-on-topology-revoke` and verify that the live agent instance is terminated. |
| `P5-NA-002` | Cancel a topology node with `lifecycle_policy: wait-completion-on-topology-revoke` and verify that the live agent instance is allowed to complete before being terminated. |
| `P5-NA-003` | Cancel a topology node with `lifecycle_policy: allow-partial-on-topology-revoke` and verify that the live agent instance is allowed to complete but its results are excluded from aggregation. |
| `P5-NA-004` | Verify that a `topology.node.cancelled` event is emitted when a topology node is cancelled. |

> **Non-normative note.**
Tests `P5-NA-001` through `P5-NA-004` validate the node cancellation
behavior defined in section 39.2.
Each test validates one of the three `lifecycle_policy` settings and
verifies that the host behaves correctly according to the policy.

### 39.4.4 Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 5 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 5 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 5
contracts interact with many earlier milestones (see the cross-reference
summary in section 39.1).
Without these tests, a Phase 5 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 5
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 6 Phase 1 | Agent identity, addressing, ownership, and dependency relations | All fixtures continue to pass; topology nodes are correctly addressed and related. |
| Milestone 6 Phase 2 | Child lifecycle, cancellation, monitoring, and restart policy | All fixtures continue to pass; topology nodes' child agents are consistent with the child lifecycle contract. |
| Milestone 6 Phase 3 | Fan-out fan-in delegation and result aggregation | All fixtures continue to pass; topology nodes' fan-out coordination is consistent with the fan-out contract. |
| Milestone 6 Phase 4 | Pod topology placement, activation leases, and reconciliation | All fixtures continue to pass; topology nodes' placement is consistent with the Phase 4 contract. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; topology nodes' grants are consistent with the threat model. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; topology nodes' grant attenuation is consistent with the capability policy. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; topology nodes' live agents are consistent with the framework plugin model. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; topology nodes' live agents are subject to the same WASI restrictions. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; topology nodes' lifecycle evidence is correctly signed and audited. |

> **Normative definition.**
A cross-milestone compatibility test passes if and only if: (1) every
fixture listed in the table above continues to produce the same expected
output as before the Phase 5 contracts were active, and (2) no new
regressions are introduced.
If any fixture fails, the Phase 5 implementation MUST be revised and the
affected milestone MUST be re-validated according to the cross-milestone
revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).

> **Non-normative note.**
The table above lists 9 fixture scopes from 5 milestones that are affected
by the Phase 5 contracts.
This is consistent with the cross-reference summary in section 39.1, which
identifies 5 direct integration points with earlier chapters.
The broader fixture scope accounts for indirect effects through shared
subsystems (such as the agent registry, mailboxes, and durable journal).

### 39.4.5 Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 5
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: draft` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 39.4.1 through 39.4.5:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P5-SF-001`). | String. |
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
A run of all Phase 5 integration tests passes if and only if:

1. Every test scenario defined in sections 39.4.1 through 39.4.5 produces
   a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 39.4.4
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: draft` to `status: normative` requires:

1. A passing run of all Phase 5 integration tests as defined above.
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

### 39.4.6 Cross-reference summary

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
5. For recovery from clean state: this section takes precedence over
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md)
   for questions of topology-specific recovery tests.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
