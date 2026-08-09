---
title: "Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-02
  - child-lifecycle
  - cancellation
  - restart-policy
  - monitoring
aliases:
  - "M6-P2 Contract And Data Model"
---

# Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-02-child-lifecycle-cancellation-monitoring-and-restart-policy.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the contract and data model for host-owned child agent spawning,
lifecycle event observability, cancellation propagation, and restart policy
selection without relying on host-language implementation details.

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
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).

## 36.1 Contract And Data Model

### Child-create directives

> **Normative definition.**
A child-create directive is the host-owned instruction that spawns a new
live actor as a child of an existing parent agent, establishing a durable
`child` relationship, allocating an address in the
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
and binding the child to a deterministic request identity, lifecycle policy,
grant scope, and initial state.

> **Normative definition.**
Every child-create directive MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `directive_id` | A deterministic request identity derived from parent address, artifact digest, manifest digest, initial state hash, owner address, lifecycle policy reference, grant scope hash, and a monotonic sequence number. | Directive construction. |
| `artifact` | The WASM artifact digest and selection that the child's live actor will execute. | Agent Manifests Artifacts Schemas And Registries](30-threat-model-principals-trust-classes-and-grant-vocabulary.md). |
| `manifest` | The reviewed manifest record that declares the artifact's declared capabilities, input schema, output schema, and trust tier. | [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md). |
| `initial_state` | The serialized initial state document that becomes the child's first snapshot revision. | [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md). |
| `owner` | The `TenantQualifiedAgentAddress` of the parent agent that created the child. | [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md). |
| `lifecycle_policy` | A reference to one of the restart policies defined in section 36.1, selecting the behavioral class for this child. | This chapter. |
| `grants` | The attenuated grant scope inherited from the parent, subject to the limits defined in [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). | [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). |
| `request_context` | Optional tenant-qualified metadata describing the originating user request or upstream directive that triggered the creation. | Host runtime. |

> **Normative definition.**
The `directive_id` is computed by hashing the concatenation of the parent
agent address, artifact digest, manifest digest, initial state hash,
owner address, lifecycle policy reference, grant scope hash, and a
monotonic per-parent sequence counter, then encoding the resulting digest
in the canonical string representation defined in
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
The `directive_id` is deterministic: the same inputs in the same order
always produce the same `directive_id`, regardless of the host process,
engine instance, or physical node on which the directive is evaluated.

> **Normative definition.**
Deterministic `directive_id` values serve three purposes: (1) they enable
exact deduplication of concurrent child-create requests that carry the
same semantic content; (2) they provide a stable reference for lifecycle
event correlation, allowing any `child.lifecycle.*` event to be traced
back to the originating directive without requiring additional context;
and (3) they enable replay of the child creation sequence from the durable
state journal defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
without depending on transient host memory.

> **Normative definition.**
A child-create directive MUST be validated against the following rules
before admission:

1. The `owner` address MUST resolve to an active agent in the durable
   registry.
2. The `artifact` digest MUST reference an artifact recorded in the
   manifest registry and MUST pass the schema validation defined in
   [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).
3. The `manifest` digest MUST correspond to the `artifact` digest; a
   manifest that does not declare the artifact MUST be rejected with
   the diagnostic `child.create.manifest-artifact-mismatch`.
4. The `initial_state` MUST be structurally valid against the manifest's
   declared input schema.
5. The `lifecycle_policy` reference MUST name a policy defined by this
   chapter's normative policy table.
6. The `grants` scope MUST not exceed the parent's current grant scope.
7. A child-create directive whose `directive_id` matches an already-admitted
   directive (recorded in the durable state journal) MUST be rejected with
   the diagnostic `child.create.duplicate-directive-id`.

> **Non-normative note.**
The seven validation rules above ensure that child creation is a
governed, auditable, and replayable operation.
Each rule maps to a specific existing chapter's contract, and failure
at any rule prevents the child from entering any observable state.
This is consistent with the single-agent host flow defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
which requires that every external request passes validation before
entering the deterministic reducer.

> **Normative definition.**
The host MUST atomically commit the following state changes when admitting
a child-create directive through the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md):

1. Write the child agent's registry entry (status: `pending`, address:
   derived from the directive's deterministic construction).
2. Create the `parent` relationship from parent to child and the
   `child` relationship from child to parent.
3. Record the `directive_id` in the durable journal with status
   `admitted`.
4. Initialize the child's mailbox with the `child.lifecycle.accepted`
   event (see the event types section below).
5. Emit a `child.create.admitted` evidence record in the format defined
   in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Non-normative note.**
Step 5 ensures that child creation is fully auditable through the
provenance and evidence layer.
The evidence record includes the `directive_id`, the parent address,
the artifact digest, the lifecycle policy selected, and the grant
scope hash, enabling operators to reconstruct any child creation
sequence from the evidence log alone.

### Child event types

> **Normative definition.**
A child lifecycle event is a structured notification emitted by the host
into the child agent's mailbox that records a transition in the child's
lifecycle state.
Child lifecycle events are the sole mechanism through which parent agents,
monitor agents, and operators observe child state changes without
persisting live monitor handles or holding references to live actor
instances.

> **Normative definition.**
The following child lifecycle event types are defined by this chapter.
Each event type has a specific emission condition, required fields,
and semantic meaning.

| Event type | Emission condition | Required fields |
|-----------|-------------------|-----------------|
| `child.lifecycle.accepted` | A child-create directive is admitted through validation. | `directive_id`, `child_address`, `parent_address`, `lifecycle_policy`. |
| `child.lifecycle.activated` | The child's live actor begins processing its first turn. | `child_address`, `activation_id`, `engine_instance_id`. |
| `child.lifecycle.initialized` | The child's live actor completes initialization and is ready to process signals. | `child_address`, `initial_state_revision`. |
| `child.lifecycle.completed` | The child's live actor completes its assigned work and exits cleanly. | `child_address`, `completion_status`, `result_summary`. |
| `child.lifecycle.failed` | The child's live actor exits with an error that is not a cancellation or termination. | `child_address`, `failure_code`, `failure_message`, `snapshot_at_failure`. |
| `child.lifecycle.cancelled` | A cancellation directive propagates to the child and the child acknowledges receipt. | `child_address`, `cancellation_id`, `reason`, `acknowledged_at`. |
| `child.lifecycle.terminated` | The child's live actor is forcibly stopped by the host without a graceful cancellation flow. | `child_address`, `termination_id`, `reason`, `snapshot_at_termination`. |
| `child.lifecycle.orphaned` | The parent agent that created the child is deleted, terminated, or becomes unresolvable while the child is still active. | `child_address`, `former_parent_address`, `orphan_reason`. |

> **Non-normative note.**
The eight event types above cover the complete set of lifecycle transitions
that a child agent can experience from creation through final resolution.
The separation between `cancelled` and `terminated` is intentional:
`cancelled` indicates a graceful, acknowledged cancellation initiated by
a directive; `terminated` indicates a forceful stop by the host, such as
during infrastructure failure, resource exhaustion, or operator override.
The separation between `failed` and `terminated` is also intentional:
`failed` indicates that the child's live actor exited with an error during
normal operation; `terminated` indicates that the host stopped the live
actor regardless of the actor's internal state.

> **Normative definition.**
Every child lifecycle event MUST be emitted into the child agent's mailbox
as defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
Events are delivered in the order they are emitted.
The host MUST NOT batch, merge, or reorder child lifecycle events.
Each event is a discrete, observable signal that the child's live actor
processes as part of its turn.

> **Normative definition.**
Every child lifecycle event MUST include the following standard fields:

| Field | Content | Source |
|-------|---------|--------|
| `event_type` | The child lifecycle event type (one of the eight defined above). | Event emission. |
| `child_address` | The `TenantQualifiedAgentAddress` of the affected child agent. | Event emission. |
| `timestamp` | The ISO 8601 timestamp of event emission. | Host clock. |
| `correlation_id` | The `directive_id` of the child-create directive that created this child, linking the event to its origin. | Directive admission. |
| `sequence_number` | A monotonic counter incremented for each event emitted into the child's mailbox. | Host runtime. |

> **Non-normative note.**
The `correlation_id` field is the primary mechanism for tracing any child
lifecycle event back to the originating child-create directive.
Without this field, an operator would need to maintain an external mapping
between child addresses and their originating directives, which is fragile
and incompatible with agent migration and host restart.
The `sequence_number` field enables detection of duplicate or out-of-order
event delivery at the child agent level.

> **Normative definition.**
The `child.lifecycle.accepted` event is the first event in a child's
lifecycle.
It is emitted immediately after the child-create directive is admitted
and before the child's live actor is activated.
The `child.lifecycle.activated` event is emitted when the child's live
actor begins processing its first turn.
Between `accepted` and `activated`, the child's live actor is in the
host's scheduling queue but not yet executing.

> **Normative definition.**
The `child.lifecycle.terminated` event is emitted when the host forcibly
stops the child's live actor for any reason that is not a graceful
cancellation or a normal completion.
Common causes include: engine instance failure, physical node failure,
resource exhaustion (memory, CPU, storage), operator override, or
infrastructure-level cancellation that cannot be propagated through the
graceful cancellation flow defined below.
The host MUST capture the child's snapshot at the moment of termination
and record it as `snapshot_at_termination` in the evidence record defined
in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

> **Normative definition.**
The `child.lifecycle.orphaned` event is emitted when the host detects
that a child's parent agent is no longer resolvable in the durable
registry or has reached a terminal status.
Orphan detection is performed by the host's lifecycle monitor at
intervals documented in the conformance profile.
When an orphan is detected, the host MUST evaluate the child's lifecycle
policy to determine whether the child should be restarted, terminated,
or held in a suspended state pending operator intervention.

> **Non-normative note.**
The orphan detection mechanism is intentionally decoupled from the
child's live actor.
The live actor has no knowledge of its parent's lifecycle status.
Orphan detection is a host-level observation that triggers a lifecycle
event into the child's mailbox, which the child's live actor then
processes as part of its normal signal processing.

### Cancellation scope, reason, deadline, and propagation

> **Normative definition.**
A cancellation is a host-owned directive that requests the graceful
shutdown of a child agent's live actor, its associated mailbox, and its
durable state.
Cancellation is distinct from termination: cancellation follows a
graceful flow with acknowledgement, whereas termination is immediate
and does not require acknowledgement.

> **Normative definition.**
Every cancellation MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `cancellation_id` | A deterministic identifier derived from the cancelling principal's address, the target child address, the reason code, and a monotonic sequence counter. | Cancellation construction. |
| `cancelling_principal` | The address of the principal that issued the cancellation (parent agent, operator, or system principal). | Cancellation request. |
| `target_child` | The `TenantQualifiedAgentAddress` of the child to be cancelled. | Cancellation request. |
| `reason` | A code from the cancellation reason taxonomy defined below, plus an optional human-readable message. | Cancellation request. |
| `deadline` | An ISO 8601 timestamp after which the cancellation MUST be escalated to termination if acknowledgement has not been received. | Cancellation request. |
| `propagation_direction` | The direction of cancellation propagation: `top-down` (from parent to child), `bottom-up` (from child to parent), or `bidirectional` (both directions). | Cancellation request. |
| `grant_revocation_scope` | The scope of grants to revoke: `all`, `derived-only`, or `none`. | Cancellation request. |

> **Normative definition.**
The cancellation reason taxonomy is:

| Reason code | Meaning | Escalation to termination |
|------------|---------|--------------------------|
| `operator-requested` | An operator explicitly requested cancellation. | After `deadline`. |
| `parent-requested` | The parent agent requested cancellation of the child. | After `deadline`. |
| `child-requested` | The child agent requested its own cancellation. | After `deadline`. |
| `infrastructure-failure` | An infrastructure-level failure (engine instance, node, network partition) makes continuation impossible. | Immediately. |
| `policy-violation` | The child violated a grant, policy, or capability limit. | After `deadline`. |
| `orphan-resolution` | The child was orphaned and the lifecycle policy resolved to cancellation. | After `deadline`. |
| `restart-exhausted` | The child's restart policy was exhausted and the child is no longer restartable. | Immediately. |
| `system-shutdown` | The host is shutting down and cannot continue any live actors. | Immediately. |

> **Non-normative note.**
The immediate escalation reasons (`infrastructure-failure`,
`restart-exhausted`, `system-shutdown`) are cases where waiting for
acknowledgement is either impossible (the host is failing) or pointless
(the child has no more restart budget).
For all other reasons, the `deadline` field provides a bounded window
for the child to acknowledge the cancellation before the host escalates
to termination.

> **Normative definition.**
Cancellation propagation direction determines which agents receive the
cancellation signal and in what order:

- `top-down`: The cancelling principal issues the cancellation to the
  parent, which propagates it to the child.
  This is the default direction for parent-initiated cancellations.
- `bottom-up`: The child initiates the cancellation and propagates it
  to the parent for acknowledgement.
  This is the default direction for child-initiated cancellations.
- `bidirectional`: The cancellation propagates in both directions
  simultaneously.
  This is used for system-level cancellations that affect entire
  subtrees of the agent hierarchy.

> **Non-normative note.**
The propagation direction model enables fine-grained control over
cancellation semantics.
A parent that wants to cancel a single child uses `top-down`.
A child that wants to cancel itself uses `bottom-up`.
A system-level operation that wants to cancel an entire subtree of
children uses `bidirectional`, which ensures that all children in the
subtree receive the cancellation signal and acknowledgement flows back
to the cancelling principal.

> **Normative definition.**
The acknowledgement flow for a cancellation proceeds as follows:

1. The cancelling principal issues the cancellation directive to the
   host.
2. The host emits a `child.lifecycle.cancelled` event into the child's
   mailbox.
3. The child's live actor processes the event and, within the bounded
   time defined by the `deadline`, emits a `child.lifecycle.cancelled`
   acknowledgement signal back to the cancelling principal.
4. The host records the acknowledgement and transitions the child to
   `cancelled` status.

> **Normative definition.**
If the child does not acknowledge the cancellation within the `deadline`,
the host MUST escalate the cancellation to termination by emitting a
`child.lifecycle.terminated` event with reason `cancellation-timeout`.
The termination is immediate and does not require further acknowledgement.
The host MUST record the timeout in the evidence log with the original
`cancellation_id` to enable operators to correlate the escalation.

> **Non-normative note.**
The acknowledgement-based cancellation flow ensures that the child has
an opportunity to perform graceful shutdown (flushing state, releasing
resources, notifying dependents) before being forcibly stopped.
The `deadline` field bounds the maximum time the cancelling principal
must wait for acknowledgement, preventing indefinite hangs.
The escalation to termination on timeout ensures that the cancellation
is not blocked by a misbehaving or unresponsive child.

### Hard-stop behavior

> **Normative definition.**
Hard stop is the host's immediate, unconditional stop of a child's live
actor without waiting for acknowledgement, graceful shutdown, or signal
processing completion.
Hard stop is the behavior that occurs when the `deadline` has passed
without acknowledgement and the host escalates from cancellation to
termination, OR when the cancellation reason is one of the immediate
escalation reasons.

> **Normative definition.**
Hard stop behaviour is defined by the following invariants:

1. The host MUST stop the child's live actor immediately upon
   escalation to termination.
2. The host MUST NOT process additional signals for the child after
   hard stop.
3. The host MUST capture the child's snapshot at the moment of hard
   stop and record it as `snapshot_at_termination` in the evidence log.
4. The host MUST emit a `child.lifecycle.terminated` event into the
   child's mailbox with reason `hard-stop`.
5. The host MUST revoke all grants associated with the child according
   to the `grant_revocation_scope` specified in the original cancellation.
6. The host MUST transition the child to `terminated` status in the
   durable registry.

> **Non-normative note.**
Hard stop is the most disruptive lifecycle transition because it does
not give the child an opportunity to clean up.
It is reserved for cases where graceful shutdown is either impossible
(infrastructure failure, system shutdown) or undesirable (policy
violation, restart exhaustion).
For all other cancellation reasons, the acknowledgement-based flow
provides the child with an opportunity to perform graceful shutdown.

> **Normative definition.**
Hard stop is consistent with the Extism invocation boundary defined in
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md).
The Extism host MUST support immediate termination of a running instance
without waiting for the guest to complete its current turn.
The snapshot captured at hard stop is the guest's memory state at the
moment the host issues the termination command, which may be mid-turn.
This is acceptable because the snapshot is recorded as evidence and
the child's next activation (if any) will start from a fresh initial
state or from the last completed revision, as defined by the
lifecycle policy.

> **Normative implementation-defined choice.**
The mechanism by which the host issues hard stop to the Extism instance
is implementation-defined.
Acceptable mechanisms include: sending a SIGKILL-equivalent signal to
the guest process, invoking an Extism-native termination function, or
using a host-level timeout that aborts the turn at its boundary.
The implementation MUST document its hard stop mechanism in the
conformance profile and MUST ensure that hard stop completes within a
bounded time documented in the conformance profile.

> **Non-normative note.**
The bounded-time requirement for hard stop is important because a host
that takes minutes to stop a live actor defeats the purpose of hard
stop as an immediate, unconditional stop mechanism.
Implementations SHOULD target hard stop completion within seconds,
consistent with the bounded-time requirements for other host operations
defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).

### Cross-reference summary

> **Normative definition.**
The contract and data model defined in this section integrate with the
following existing chapters:

1. **Agent addresses and relationships**: Child-create directives establish
   `parent`/`child` relationships as defined in
   [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md).
   The deterministic `directive_id` construction uses the same
   tenant-qualified address model.
2. **Agent registry**: Child creation writes a registry entry with
   `status: pending` as defined in
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).
3. **State operations**: The `initial_state` field of child-create
   directives is validated against the manifest's input schema using
   the patch and revision semantics defined in
   [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md).
4. **Deterministic reducer**: The child's first turn is processed by the
   deterministic reducer as defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).
5. **Mailboxes**: Child lifecycle events are emitted into the child's
   mailbox as defined in
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
6. **Capability policy**: Grant scope attenuation for child agents is
   governed by
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
7. **Framework plugins**: The child's live actor executes as a framework
   plugin instance as defined in
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).
8. **Synchronous host functions**: The child's live actor is subject to
   the WASI restrictions and tenant isolation defined in
   [Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).
9. **Provenance and audit**: All child lifecycle events and cancellations
   are recorded as evidence in the format defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
10. **Durable state**: The child's state journal, snapshot capture at
    termination, and atomic commit protocol are defined in
    [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
    and
    [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

> **Non-normative note.**
The ten integration points above demonstrate that child lifecycle
cancellation monitoring and restart policy is not an isolated subsystem
but is deeply woven into the multi-agent coordination fabric.
Every chapter that deals with agent lifecycle, state, grants, or
provenance interacts with this chapter's contracts in well-defined ways.
The cross-references above are the primary integration points.

> **Normative definition.**
When this section and another section of this specification appear to
conflict on a behavior question, the following precedence rules apply:

1. For child address and relationship semantics: this section takes
   precedence over
   [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md)
   for questions of child-specific relationship lifecycle and cancellation
   propagation.
2. For child lifecycle event ordering and mailbox delivery: this section
   takes precedence over
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   for questions of child event emission order and acknowledgement
   requirements.
3. For child grant scope and policy enforcement: this section takes
   precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of grant revocation scope and inheritance.
4. For hard stop mechanism and bounded time: this section takes precedence
   over
   [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)
   for questions of immediate instance termination.
5. Where both sections are applicable and agree, they are mutually
   reinforcing.

## Variability and limits

### Normative variability register

The following table enumerates every `MAY`, `SHOULD`, `SHOULD NOT`,
implementation-defined choice, implementation limit, and permitted
variation in this section, synchronized with the specification area's
variability register.

| Clause | Variability class | Selection |
|--------|------------------|-----------|
| 36.1 Child-create directives | Normative implementation-defined choice | The separator character used in the deterministic `directive_id` hash input. Must not collide with any component of the parent address, artifact digest, manifest digest, initial state hash, owner address, lifecycle policy reference, or grant scope hash. |
| 36.1 Child-create directives | Normative implementation-defined choice | The exact hash function (SHA-256, SHA-3, BLAKE2s, or equivalent) used to compute the `directive_id`. Must produce a collision-resistant digest of at least 256 bits. |
| 36.1 Child-create directives | Normative implementation-defined choice | The monotonic sequence counter scope: per-parent, per-tenant, or global. Must be documented in the conformance profile. |
| 36.1 Child lifecycle events | Normative implementation-defined choice | The maximum size of the `failure_message` field in `child.lifecycle.failed` events, in bytes. Must be at least 1024 bytes and documented in the conformance profile. |
| 36.1 Cancellation scope and propagation | Normative implementation-defined choice | The default `deadline` duration for cancellations not explicitly specifying a deadline. Must be at least 30 seconds and documented in the conformance profile. |
| 36.1 Cancellation scope and propagation | Normative implementation-defined choice | The maximum `deadline` duration. Must be at least 600 seconds (10 minutes) and documented in the conformance profile. |
| 36.1 Cancellation scope and propagation | Normative implementation-defined choice | The mechanism by which the host detects that a child has not acknowledged a cancellation within the `deadline`. Must be documented in the conformance profile. |
| 36.1 Hard-stop behavior | Normative implementation-defined choice | The mechanism by which the host issues hard stop to the Extism instance (SIGKILL-equivalent signal, Extism-native termination function, or host-level turn boundary timeout). Must be documented in the conformance profile. |
| 36.1 Hard-stop behavior | Normative implementation-defined choice | The bounded time within which hard stop must complete. Must be at most 30 seconds and documented in the conformance profile. |
| 36.1 Hard-stop behavior | Normative implementation-defined choice | The snapshot capture granularity at hard stop: full memory snapshot, last-completed-turn snapshot, or partial-turn snapshot. Must be documented in the conformance profile. |
| 36.1 Orphan detection | Normative implementation-defined choice | The interval at which the host's lifecycle monitor performs orphan detection. Must be at most 60 seconds and documented in the conformance profile. |
| 36.1 Orphan detection | Normative implementation-defined choice | The resolution strategy for orphaned children whose lifecycle policy is `operator-approved` and no operator is available: hold indefinitely, terminate, or migrate to a default owner. Must be documented in the conformance profile. |

### Implementation limits

| Limit | Minimum value | Notes |
|-------|--------------|-------|
| Maximum child address length | 256 characters | Consistent with
  [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md). |
| Maximum `directive_id` length | 256 characters | Deterministic hash digest encoding. |
| Maximum `cancellation_id` length | 256 characters | Deterministic hash digest encoding. |
| Maximum lifecycle event payload size | 64 KB | Consistent with
  [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md). |
| Maximum cancellation reason message length | 1024 characters | Human-readable message field. |
| Maximum grant revocation scope list | Unbounded by default | Hosts MAY impose local limits through policy. |

### Permitted variations

The following variations are permitted by this specification and MUST
be documented in the conformance profile when selected:

1. **Additional cancellation reason codes**: Hosts MAY define additional
   cancellation reason codes beyond the taxonomy defined in this section,
   provided they do not conflict with the existing codes and are documented
   in the conformance profile.
2. **Additional child lifecycle event types**: Hosts MAY define additional
   child lifecycle event types for implementation-specific observations
   (e.g., `child.lifecycle.migration-started`), provided they do not
   conflict with the existing event types and are documented in the
   conformance profile.
3. **Additional propagation directions**: Hosts MAY define additional
   propagation directions beyond `top-down`, `bottom-up`, and
   `bidirectional`, provided they are documented in the conformance profile
   and do not violate the acknowledgement flow defined in this section.

### Exclusions

The following items are NOT within the scope of this section:

1. The specific implementation of the Extism instance termination function
   (covered by
   [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)).
2. The specific implementation of the durable state journal write protocol
   (covered by
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   and
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)).
3. The specific implementation of the lifecycle monitor's orphan detection
   algorithm (covered by
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md)).
4. The specific implementation of the grant revocation mechanism (covered
   by
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)).
