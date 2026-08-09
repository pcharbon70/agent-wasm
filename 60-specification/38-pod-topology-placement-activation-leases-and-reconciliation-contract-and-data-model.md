---
title: "Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model"
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
aliases:
  - "M6-P4 Contract And Data Model"
---

# Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-04-pod-topology-placement-activation-leases-and-reconciliation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the contract and data model for pod-like topology nodes,
activation leases that fence live placement, and deterministic reconciliation
that turns desired topology into disposable live agents on one or more hosts.

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
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md).

## 38.1 Contract And Data Model

### Pod-like topology nodes

> **Normative definition.**
A pod topology node is the durable, logical description of a desired
agent placement.
Each node captures the agent's identity, its role within a topology graph,
its dependencies, its ownership, its activation mode, its placement
constraints, its resource class, and its lifecycle policy.
A node is the authoritative desired state; live placement is ephemeral and
derived from it through reconciliation.

> **Normative definition.**
Every pod topology node MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `node_id` | A deterministic node identity derived from the topology version and the node's position in the topology graph. | Topology directive. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that this node describes. | Topology directive. |
| `role` | The agent's role within the topology (e.g., `orchestrator`, `worker`, `coordinator`, `observer`). | Topology directive. |
| `dependencies` | A list of `node_id` values for nodes that this node depends on; empty list means no dependencies. | Topology directive. |
| `dependents` | A list of `node_id` values for nodes that depend on this node; computed from dependency declarations, not stored. | Derived. |
| `owner` | The `TenantQualifiedAgentAddress` of the principal that owns or controls this node. | Topology directive. |
| `activation_mode` | The activation mode: `durable`, `ephemeral`, or `manual`. | Topology directive. |
| `placement_constraints` | A set of constraints that describe where the node MAY be placed (e.g., `resource_class`, `topology_region`). | Topology directive. |
| `resource_class` | The implementation-defined resource class that describes the node's expected resource footprint. | Topology directive. |
| `lifecycle_policy` | The lifecycle policy for this node's live placement: `terminate-on-topology-revoke`, `wait-completion-on-topology-revoke`, or `allow-partial-on-topology-revoke`. | Topology directive. |
| `topology_version` | The monotonic version of the topology that this node belongs to. | Topology directive. |
| `created_at` | The ISO 8601 timestamp of node creation. | Topology directive. |
| `purpose` | A human-readable description of the node's purpose within the topology. | Topology directive. |

> **Normative definition.**
The `node_id` is computed by hashing the concatenation of the
`topology_version`, the node's role, the `agent_address`, and a
deterministic position index, then encoding the resulting digest in the
canonical string representation defined in
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
The `node_id` is deterministic: the same inputs in the same order always
produce the same `node_id`, regardless of the host process, engine
instance, or physical node on which the topology is evaluated.

> **Non-normative note.**
Deterministic `node_id` values serve three purposes: (1) they enable exact
deduplication of concurrent topology directives that carry the same
semantic content; (2) they provide a stable reference for dependency
resolution, allowing any node to be traced back to its position in the
topology graph without requiring additional context; and (3) they enable
replay of the topology execution sequence from the durable state journal
defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
without depending on transient host memory.

### Desired topology, observed status, and live placement

> **Normative definition.**
The pod topology model separates three distinct concerns:

1. **Desired topology**: The durable, authoritative description of what
   the system SHOULD look like.
   This is stored in the durable journal and is the source of truth for
   reconciliation.
   Desired topology is immutable once recorded; modifications are expressed
   as new topology versions.

2. **Observed status**: The durable record of what the system ACTUALLY
   looks like, as observed by the host.
   This is stored in the durable journal and includes the current
   reconciliation status, any observed deviations from desired topology,
   and the results of the last reconciliation pass.

3. **Live placement**: The ephemeral, disposable state of agents that
   are currently executing on one or more hosts.
   Live placement is NOT stored durably; it is derived from desired
   topology through reconciliation and is lost on host restart (recovered
   from desired topology on restart).

> **Non-normative note.**
This separation ensures that desired topology remains the source of truth,
observed status provides auditability and debugging information, and live
placement remains disposable so that hosts can be restarted, migrated, or
replaced without losing authoritative state.
The durable journal defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
stores desired topology and observed status; live placement is held in
memory only.

> **Normative definition.**
Desired topology is identified by a deterministic topology identity
derived from the topology version, the topology owner address, and a
monotonic per-tenant sequence counter.
The topology identity is stored in the durable journal and is used to
correlate topology directives, node states, and reconciliation events.

> **Normative definition.**
Observed status is identified by the topology identity and includes:

| Field | Content | Source |
|-------|---------|--------|
| `topology_identity` | The deterministic topology identity. | Topology directive. |
| `reconciliation_status` | The current reconciliation status: `pending`, `reconciling`, `reconciled`, `failed`, or `rollback`. | Host runtime. |
| `nodes_observed` | A list of `node_id` values for nodes that the host has observed in the current topology version. | Host runtime. |
| `nodes_missing` | A list of `node_id` values for nodes in desired topology that are NOT present in live placement. | Host runtime. |
| `nodes_extra` | A list of `node_id` values for nodes in live placement that are NOT present in desired topology. | Host runtime. |
| `nodes_failed` | A list of `node_id` values for nodes in live placement that have failed. | Host runtime. |
| `nodes_stale` | A list of `node_id` values for nodes in live placement whose live state has not been refreshed within the implementation-defined stale timeout. | Host runtime. |
| `reconciliation_timestamp` | The ISO 8601 timestamp of the last reconciliation pass. | Host runtime. |
| `reconciliation_result` | The result of the last reconciliation pass: `success`, `partial`, or `failed`. | Host runtime. |

> **Non-normative note.**
Observed status provides operators with visibility into the reconciliation
process.
The `nodes_missing`, `nodes_extra`, `nodes_failed`, and `nodes_stale`
fields enable operators to identify deviations from desired topology and
take corrective action.
The `reconciliation_result` field indicates whether the last reconciliation
pass completed successfully, partially, or failed.

### Single-node placement first

> **Normative definition.**
Single-node placement is the simplest placement mode, in which all desired
topology nodes are placed on a single host.
Single-node placement is implemented before multi-node coordination
adapters because it provides a complete, self-contained test of the
reconciliation loop without requiring distributed consensus or network
coordination.

> **Normative definition.**
In single-node placement, the host MUST:

1. Resolve all desired topology nodes to the local host.
2. For each node in `pending` or `missing` state, create a live agent
   instance according to the node's `activation_mode`:
   - `durable`: Create a live agent instance that persists across host
     restarts (recovered from desired topology on restart).
   - `ephemeral`: Create a live agent instance that does NOT persist
     across host restarts (lost on restart, recreated from desired
     topology on restart).
   - `manual`: Do NOT create a live agent instance; the operator MUST
     manually create and register the live agent instance.
3. For each node in `extra` state, terminate the corresponding live agent
   instance.
4. For each node in `failed` state, apply the node's `lifecycle_policy`
   to determine whether to restart, wait, or allow partial results.
5. Emit reconciliation evidence for each state transition.

> **Non-normative note.**
Single-node placement is appropriate for development, testing, and
small-scale deployments.
Multi-node placement (deferred to Milestone 7) is required for production
deployments that need horizontal scaling, fault tolerance, or geographic
distribution.

> **Normative definition.**
A replaceable activation coordinator handles the reconciliation loop for
single-node placement.
The activation coordinator is a host-owned, stateless function that
takes desired topology and observed status as input and produces live
placement updates as output.
The activation coordinator is replaceable: the host MAY swap activation
coordinator implementations without changing the desired topology or
observed status contracts.

> **Non-normative note.**
The replaceable activation coordinator pattern ensures that the
reconciliation loop is decoupled from the host's internal architecture.
This enables implementations to evolve their reconciliation strategy
without breaking the durable topology contracts.

### Cross-references and precedence

> **Non-normative note.**
This section's contract and data model integrate with the following
earlier chapters:

1. For topology node identity: this section takes precedence over
   [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md)
   for questions of topology-specific identity construction and determinism.
2. For topology node validation: this section takes precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of topology directive-specific validation rules.
3. For topology node atomic commits: this section takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of topology directive-specific atomic commit steps.
4. For topology node evidence emission: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of topology directive-specific evidence record format.
5. For live agent lifecycle within topology nodes: this section takes
   precedence over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of live agent lifecycle within a topology node context.
6. For live agent fan-out coordination: this section takes precedence over
   [Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model](37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md)
   for questions of topology node-specific fan-out coordination.
7. Where both sections are applicable and agree, they are mutually
   reinforcing.
