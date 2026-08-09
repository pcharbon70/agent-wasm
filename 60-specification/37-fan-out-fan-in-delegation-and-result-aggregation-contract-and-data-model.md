---
title: "Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-03
  - fan-out
  - fan-in
  - delegation
  - result-aggregation
aliases:
  - "M6-P3 Contract And Data Model"
---

# Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-03-fan-out-fan-in-delegation-and-result-aggregation.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the contract and data model for coordinating parallel child
work through durable directives and deterministic aggregation rather than
shared mutable guest state.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
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
[Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md).

## 37.1 Contract And Data Model

### Fan-out plan identity

> **Normative definition.**
A fan-out plan is the host-owned coordination structure that schedules a
set of child work items for parallel execution under a common deadline,
concurrency bound, and aggregation policy, then produces a single
aggregated result for the originating principal.
A fan-out plan is identified by a deterministic plan identity derived
from the delegating agent address, the plan payload hash, and a monotonic
sequence counter.

> **Normative definition.**
Every fan-out plan MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `plan_id` | A deterministic plan identity derived from delegating agent address, payload hash, and a monotonic per-agent sequence counter. | Fan-out plan construction. |
| `delegating_agent` | The `TenantQualifiedAgentAddress` of the agent that created the fan-out plan. | Fan-out plan directive. |
| `work_items` | A list of child work items to be executed in parallel, each referencing an artifact, manifest, and input data. | Fan-out plan directive. |
| `concurrency_bound` | The maximum number of child agents that may execute concurrently for this plan. | Fan-out plan directive. |
| `deadline` | An ISO 8601 timestamp after which the plan is considered expired and partial results MAY be aggregated. | Fan-out plan directive. |
| `cancellation_policy` | The policy for cancelling child agents when the plan is cancelled or expired: `cancel-all`, `wait-completion`, or `allow-partial`. | Fan-out plan directive. |
| `aggregation_policy` | The policy for aggregating child results: `all`, `quorum`, `first-success`, `best-effort`, or `ordered`. | Fan-out plan directive. |
| `quorum_threshold` | The minimum number of successful child results required for `quorum` aggregation. Only applicable when `aggregation_policy` is `quorum`. | Fan-out plan directive. |
| `result_contract` | The schema and field requirements that the aggregated result MUST satisfy. | Fan-out plan directive. |
| `delegation_grants` | The attenuated grant scope inherited by child agents from the delegating agent. | Fan-out plan directive. |

> **Normative definition.**
The `plan_id` is computed by hashing the concatenation of the delegating
agent address, payload hash, and a monotonic per-agent sequence counter,
then encoding the resulting digest in the canonical string representation
defined in
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
The `plan_id` is deterministic: the same inputs in the same order always
produce the same `plan_id`, regardless of the host process, engine
instance, or physical node on which the plan is evaluated.

> **Normative definition.**
Deterministic `plan_id` values serve three purposes: (1) they enable
exact deduplication of concurrent fan-out plan requests that carry the
same semantic content; (2) they provide a stable reference for result
correlation, allowing any aggregated result to be traced back to the
originating plan without requiring additional context; and (3) they
enable replay of the plan execution sequence from the durable state
journal defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
without depending on transient host memory.

> **Normative definition.**
A fan-out plan directive MUST be validated against the following rules
before admission:

1. The `delegating_agent` address MUST resolve to an active agent in the
   durable registry.
2. The `work_items` list MUST contain at least one work item and at
   least one work item MUST reference a valid artifact digest recorded
   in the manifest registry.
3. Each work item's artifact digest MUST pass the schema validation
   defined in
   [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).
4. Each work item's manifest digest MUST correspond to the work item's
    artifact digest; a manifest that does not declare the artifact MUST
    be rejected with the diagnostic `fanout.plan.incompatible-manifest-artifact`.
5. The `concurrency_bound` MUST be a positive integer and MUST not
   exceed the implementation-defined maximum concurrency per plan.
6. The `deadline` MUST be a future timestamp relative to the current
   host clock.
7. The `aggregation_policy` MUST name a policy defined by this chapter's
   normative policy table.
8. When `aggregation_policy` is `quorum`, the `quorum_threshold` MUST
   be a positive integer less than or equal to the number of work items.
9. A fan-out plan whose `plan_id` matches an already-admitted plan
   (recorded in the durable state journal) MUST be rejected with the
   diagnostic `fanout.plan.duplicate-plan-id`.

> **Non-normative note.**
The nine validation rules above ensure that fan-out plans are governed,
auditable, and replayable operations.
Each rule maps to a specific existing chapter's contract, and failure
at any rule prevents the plan from entering any observable state.
This is consistent with the single-agent host flow defined in
[Single-Agent Host And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
which requires that every external request passes validation before
entering the deterministic reducer.

> **Normative definition.**
The host MUST atomically commit the following state changes when admitting
a fan-out plan directive through the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md):

1. Write the fan-out plan's registry entry (status: `pending`, address:
   derived from the plan's deterministic construction).
2. Record the `plan_id` in the durable journal with status `admitted`.
3. Create child work items for each entry in `work_items`, each with a
   deterministic work item identity derived from the `plan_id`, the
   work item index, and the work item payload hash.
4. Initialize the fan-out plan's aggregation state in the durable journal
   with status `awaiting-results`.
5. Emit a `fanout.plan.admitted` evidence record in the format defined
   in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Non-normative note.**
Step 5 ensures that fan-out plan creation is fully auditable through the
provenance and evidence layer.
The evidence record includes the `plan_id`, the delegating agent address,
the number of work items, the aggregation policy, and the concurrency
bound, enabling operators to reconstruct any fan-out plan execution
sequence from the evidence log alone.

### Child work items

> **Normative definition.**
A child work item is a discrete unit of parallel work within a fan-out
plan.
Each child work item references an artifact, manifest, and input data,
and is executed by a child agent that is bound to the parent fan-out plan.
Child work items are the atomic units of parallel execution; the host
may schedule multiple child work items concurrently up to the plan's
`concurrency_bound`.

> **Normative definition.**
Every child work item MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `work_item_id` | A deterministic work item identity derived from `plan_id`, work item index, and input data hash. | Fan-out plan directive. |
| `plan_id` | The `plan_id` of the parent fan-out plan. | Fan-out plan directive. |
| `work_item_index` | The zero-indexed position of this work item in the parent plan's `work_items` list. | Fan-out plan directive. |
| `artifact` | The artifact digest and selection that the child agent will execute. | Fan-out plan directive. |
| `manifest` | The reviewed manifest record that declares the artifact's declared capabilities, input schema, output schema, and trust tier. | [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md). |
| `input_data` | The serialized input data for this work item, structured against the manifest's declared input schema. | Fan-out plan directive. |
| `delegation_grants` | The attenuated grant scope inherited by the child agent from the delegating agent, subject to the limits defined in [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). | Fan-out plan directive. |
| `purpose` | A human-readable description of the work item's purpose within the plan. | Fan-out plan directive. |

> **Normative definition.**
The `work_item_id` is computed by hashing the concatenation of the
`plan_id`, the `work_item_index`, and the input data hash, then encoding
the resulting digest in the canonical string representation defined in
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
The `work_item_id` is deterministic: the same inputs in the same order
always produce the same `work_item_id`, regardless of the host process,
engine instance, or physical node on which the work item is evaluated.

> **Normative definition.**
Child work items are bound to the parent fan-out plan through the
following invariants:

1. A child work item MUST be associated with exactly one parent fan-out
    plan; a work item whose `plan_id` does not resolve to an active plan
    MUST be rejected with the diagnostic `fanout.plan.incompatible-plan`.
2. A child work item MUST NOT be created with a `work_item_id` that matches
    an already-existing work item for the same plan; a duplicate work item
    submission MUST be rejected with the diagnostic
    `fanout.work-item.duplicate-work-item-id`.
3. A child work item MUST not exceed the parent plan's `concurrency_bound`;
   the host MUST schedule child agents such that at most
   `concurrency_bound` child agents are executing concurrently for a given
   plan.
4. A child work item MUST not outlive the parent fan-out plan's `deadline`;
   if a child agent has not completed its work item by the deadline, the
   host MUST apply the plan's `cancellation_policy` to determine whether
   to cancel, wait, or allow partial results.
5. A child work item's result MUST be aggregated according to the parent
   plan's `aggregation_policy`; results that do not satisfy the
   `result_contract` MUST be rejected with the diagnostic
   `fanout.result.incompatible-contract`.

> **Non-normative note.**
The five invariants above ensure that child work items are governed by
the parent plan's constraints and that the plan's aggregation policy
can be applied deterministically.
The `concurrency_bound` invariant prevents resource exhaustion by
limiting parallelism; the `deadline` invariant prevents indefinite
waiting for slow or hung children; the `result_contract` invariant
ensures that aggregated results are structurally valid.

### Delegated principal and attenuated grants

> **Normative definition.**
A delegated principal is the child agent that executes a child work item
within a fan-out plan.
Each delegated principal is bound to the parent fan-out plan through
a deterministic child relationship, attenuated grants, and a purpose
that restricts the child's capabilities to the work item's scope.

> **Normative definition.**
Every delegated principal MUST be granted the following attenuated
capabilities:

| Capability | Scope | Restriction |
|------------|-------|-------------|
| `fanout.work-item.execute` | The child's assigned work item only | The child MUST NOT execute work items assigned to other children in the same plan. |
| `fanout.result.submit` | The child's assigned work item only | The child MUST submit results through the result submission mechanism defined in this section. |
| `fanout.plan.observe` | The parent fan-out plan only | The child MAY observe the parent plan's status but MUST NOT modify it. |

> **Normative definition.**
The following capabilities are nondelegable and MUST NOT be granted to
delegated principals:

| Nondelegable capability | Rationale |
|------------------------|-----------|
| `fanout.plan.cancel` | Cancelling a plan affects all work items; only the delegating agent or operator MAY cancel. |
| `fanout.plan.modify` | Modifying a plan's structure affects all work items; only the delegating agent MAY modify. |
| `fanout.result.aggregate` | Aggregation is a host function; delegated principals MUST NOT aggregate results. |
| `fanout.work-item.modify` | Modifying a work item affects the plan's execution; only the delegating agent MAY modify. |

> **Non-normative note.**
The nondelegable capabilities ensure that delegated principals cannot
disrupt the plan's execution or aggregation.
The three granted capabilities ensure that delegated principals can
execute their assigned work, submit results, and observe the plan's
status without being able to modify the plan or other work items.

> **Normative definition.**
The attenuated grants granted to delegated principals are derived from
the delegating agent's current grant scope, subject to the limits defined
in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
The host MUST ensure that the attenuated grants are strictly a subset of
the delegating agent's grant scope and that the attenuation is recorded
in the durable journal.

### Child result identity and ordering

> **Normative definition.**
A child result is the output produced by a child agent's execution of a
child work item within a fan-out plan.
Each child result is identified by a deterministic result identity derived
from the `work_item_id`, a monotonic sequence counter, and the result
payload hash.

> **Normative definition.**
Every child result MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `result_id` | A deterministic result identity derived from `work_item_id`, sequence counter, and result payload hash. | Child agent. |
| `work_item_id` | The `work_item_id` of the parent work item. | Child agent. |
| `plan_id` | The `plan_id` of the parent fan-out plan. | Child agent. |
| `sequence_number` | A monotonic counter incremented for each result submitted by this child agent. | Child agent. |
| `result_data` | The serialized result data, structured against the `result_contract` of the parent plan. | Child agent. |
| `status` | The result status: `success`, `failure`, or `partial`. | Child agent. |
| `failure_code` | The failure code if `status` is `failure`; otherwise `null`. | Child agent. |
| `failure_message` | The human-readable failure message if `status` is `failure`; otherwise `null`. | Child agent. |
| `timestamp` | The ISO 8601 timestamp of result submission. | Child agent. |

> **Normative definition.**
The `result_id` is computed by hashing the concatenation of the
`work_item_id`, the `sequence_number`, and the result payload hash,
then encoding the resulting digest in the canonical string representation
defined in
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
The `result_id` is deterministic: the same inputs in the same order
always produce the same `result_id`, regardless of the host process,
engine instance, or physical node on which the result is submitted.

> **Normative definition.**
Child results are ordered within a fan-out plan according to the parent
plan's `aggregation_policy`:

- `all`: Results are aggregated in the order they are received; partial
  results are collected until the `deadline` expires.
- `quorum`: Results are aggregated in the order they are received;
  aggregation completes when `quorum_threshold` successful results are
  received.
- `first-success`: Aggregation completes when the first successful result
  is received; subsequent results are discarded.
- `best-effort`: Results are aggregated in the order they are received;
  the host selects the best result according to an implementation-defined
  quality metric.
- `ordered`: Results are aggregated in the order specified by the parent
  plan's `work_items` list, regardless of submission order.

### Partial completion and duplicate suppression

> **Normative definition.**
Partial completion occurs when a child agent completes its work item but
the result does not fully satisfy the parent plan's `result_contract`.
The host MUST classify partial results according to the parent plan's
`aggregation_policy`:

- `all`: Partial results are collected and included in the aggregated
  result; the host MUST NOT discard partial results unless the plan's
  `cancellation_policy` is `cancel-all` and the plan is cancelled.
- `quorum`: Partial results are aggregated in the order they are received
  until `quorum_threshold` successful results are received; subsequent
  successful results are discarded; failed results are included only if
  they are among the first `quorum_threshold` results by submission order.
- `first-success`: Partial results are discarded; only successful results
  are aggregated.
- `best-effort`: Partial results are included in the aggregated result
  if they are the best available according to the implementation-defined
  quality metric.
- `ordered`: Partial results are included in the aggregated result in
  their specified order; the host MUST NOT reorder partial results.

> **Non-normative note.**
Partial completion is a common outcome in distributed systems where
children may fail or produce incomplete results.
The aggregation policies above provide different tradeoffs between
completeness and timeliness; implementations SHOULD document their
partial result handling behavior in the conformance profile.

> **Normative definition.**
Duplicate suppression prevents the same child result from being aggregated
multiple times.
The host MUST suppress duplicate results according to the following rules:

1. A result whose `result_id` matches a previously-aggregated result
   MUST be rejected with the diagnostic `fanout.result.duplicate`.
2. A result whose `work_item_id` and `result_data` hash match a previously-
   aggregated result MUST be rejected with the diagnostic
   `fanout.result.duplicate-content`.
3. Duplicate suppression is applied before aggregation; rejected results
   are recorded in the durable journal with the diagnostic and the
   corresponding original result's `result_id`.

> **Non-normative note.**
The two duplicate suppression rules provide defense-in-depth: the first
rule prevents replay of the same result identity; the second rule
prevents replay of results with identical content but different identities.
Both rules are necessary because the `result_id` may be regenerated
across host restarts if the monotonic sequence counter is not durable,
while the `result_data` hash is always durable.

### Causal attachment

> **Normative definition.**
Causal attachment links child results back to the originating fan-out plan,
the delegating agent, and the original user request or directive that
triggered the plan.
Causal attachment is recorded through the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `plan_id` | The `plan_id` of the parent fan-out plan. | Child agent. |
| `work_item_id` | The `work_item_id` of the parent work item. | Child agent. |
| `delegating_agent` | The `TenantQualifiedAgentAddress` of the delegating agent. | Fan-out plan directive. |
| `originating_request_id` | The identifier of the original user request or directive that triggered the fan-out plan. | Fan-out plan directive. |
| `correlation_id` | A correlation identifier that groups all results from the same fan-out plan. | Fan-out plan directive. |

> **Non-normative note.**
Causal attachment ensures that aggregated results can be traced back to
the originating request, which is essential for audit, debugging, and
operator notification.
The `correlation_id` field enables downstream systems to group all
results from the same plan without requiring additional context.
The `originating_request_id` field enables operators to trace a plan
back to the user request that triggered it, which is essential for
provenance and compliance.

> **Normative definition.**
The host MUST record causal attachment metadata for every child result
in the durable journal and in the evidence record emitted through
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
Causal attachment metadata is immutable once recorded; modifications
to causal attachment after recording MUST be rejected with the
diagnostic `fanout.result.causal-attachment.immutable`.

> **Non-normative note.**
Immutable causal attachment prevents tampering with the provenance
trail.
If a child agent or operator needs to correct causal attachment metadata
after submission, the correction MUST be recorded as a separate
append-only evidence record rather than modifying the original record.

### Cross-references and precedence

> **Non-normative note.**
This section's contract and data model integrate with the following
earlier chapters:

1. For fan-out plan and child work item identity: this section takes
   precedence over
   [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md)
   for questions of plan-specific and work-item-specific identity
   construction and determinism.
2. For fan-out plan and child work item validation: this section takes
   precedence over
   [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md)
   for questions of fan-out plan-specific validation rules.
3. For fan-out plan and child work item atomic commits: this section
   takes precedence over
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   for questions of fan-out plan-specific atomic commit steps.
4. For fan-out plan and child work item evidence emission: this section
   takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of fan-out plan-specific evidence record format.
5. For child agent execution within a fan-out plan: this section takes
   precedence over
   [Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
   for questions of child agent lifecycle within a fan-out plan context.
6. For child result submission and aggregation: this section takes
   precedence over
   [Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md)
   for questions of fan-out plan-specific result submission semantics.
7. Where both sections are applicable and agree, they are mutually
   reinforcing.
