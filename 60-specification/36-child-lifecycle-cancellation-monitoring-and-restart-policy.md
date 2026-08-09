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

## 36.2 Behavior And Integration

### Monitor subscriptions and durable lifecycle notifications

> **Normative definition.**
A monitor subscription is a durable, address-bound declaration by which a
parent agent, a peer agent, or an operator agent declares an interest in
observing child lifecycle events without requiring a live connection to
the host's lifecycle monitor or holding a reference to a live actor
instance.
Monitor subscriptions are the sole mechanism through which external
principals observe child lifecycle events over the agent's lifetime,
including across host restarts, agent migrations, and engine instance
failures.

> **Normative definition.**
A monitor subscription MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `subscriber_address` | The `TenantQualifiedAgentAddress` of the subscribing principal (parent, peer, or operator). | Subscription request. |
| `target_child` | The `TenantQualifiedAgentAddress` of the child to observe, or `null` to observe all children of the subscriber's tenant. | Subscription request. |
| `event_types` | A subset of the eight child lifecycle event types defined in section 36.1, or `all` to observe every event type. | Subscription request. |
| `subscription_id` | A deterministic identifier derived from the subscriber address, target child address, event types set, and a monotonic sequence counter. | Subscription construction. |
| `created_at` | The ISO 8601 timestamp of subscription creation. | Subscription construction. |

> **Normative definition.**
The host MUST NOT persist live monitor handles, active watch descriptors,
or runtime-specific connection objects in durable storage as part of a
monitor subscription.
A monitor subscription is a declarative record, not an active connection.
The host's lifecycle monitor is responsible for evaluating active
subscriptions at the time an event is emitted and routing the event
to the appropriate subscriber mailbox.
This design ensures that monitor subscriptions survive host restarts
without requiring re-registration, and that subscribers do not hold
resources that could leak if the host process crashes.

> **Normative implementation-defined choice.**
The mechanism by which the host evaluates active subscriptions against
emitted events is implementation-defined.
Acceptable mechanisms include: in-memory subscription tables evaluated
at event emission time with durable subscription records for persistence
across restarts, a subscription-aware event bus that fans events to
matching subscribers, or a polling mechanism where subscribers query a
durable event log for events matching their subscription criteria.
The implementation MUST document its subscription evaluation mechanism
in the conformance profile.

> **Non-normative note.**
The prohibition on persisting live monitor handles is a deliberate
design choice that prevents resource leaks and subscription staleness.
A host that persists live handles would require explicit cleanup when
a subscriber is deleted or when a child reaches a terminal status,
introducing additional failure modes.
By treating subscriptions as declarative records, the host can
determine subscription validity at event emission time based solely
on the current state of the durable registry.

> **Normative definition.**
When a child reaches a terminal status (cancelled, terminated, completed,
or orphaned-and-deleted), the host MUST automatically close any open
monitor subscriptions for that child by emitting a `subscription.closed`
evidence record and removing the subscription from the active table.
Closed subscriptions are NOT removed from the durable subscription log
and MAY be replayed by subscribers that missed earlier events.

> **Normative definition.**
Every child lifecycle event emitted into the child's mailbox MUST also
be evaluated against all active monitor subscriptions.
An event matches a subscription if the subscription's `target_child`
is `null` (observe all children) or matches the event's `child_address`,
AND the subscription's `event_types` includes the event's type or is
set to `all`.
A matching event is delivered to the subscriber's mailbox as a
`child.lifecycle.observed` signal that includes a copy of the original
lifecycle event fields plus the `subscription_id` that matched.

> **Non-normative note.**
The `child.lifecycle.observed` signal is distinct from the original
lifecycle event to prevent confusion between events received by the
child's live actor (which drive the child's state machine) and events
received by subscribers (which are purely observational).
Subscribers have no authority to affect the child's lifecycle by
processing `child.lifecycle.observed` signals; they are read-only
notifications.
This separation is consistent with the capability model defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
where observation rights do not imply modification rights.

> **Normative definition.**
Monitor subscriptions are subject to the following lifecycle rules:

1. A subscription is created when the host admits the subscription
   request through the atomic commit protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
2. A subscription is active while the target child exists in the
   durable registry with a non-terminal status.
3. A subscription is closed when the target child reaches a terminal
   status, when the subscriber agent is deleted, or when the
   subscriber explicitly cancels the subscription.
4. A subscription is invalid if the subscriber's grants do not include
   the `observe.child.lifecycle` capability for the target child.

> **Non-normative note.**
The grant-based access control on subscriptions is a critical security
property.
Without it, any agent in the tenant could subscribe to observe the
lifecycle of any other agent, enabling surveillance of agent behavior
without authorization.
The `observe.child.lifecycle` capability is defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
and is attenuated when granted to child agents.

### Restart policies

> **Normative definition.**
A restart policy is a normative behavioral class that determines whether
and how a child agent is restarted after a lifecycle termination event
that is not a graceful cancellation.
Restart policies are selected at child creation time via the
`lifecycle_policy` field of the child-create directive and are immutable
for the lifetime of the child.
The following four restart policies are defined by this chapter.

> **Normative definition.**
The `never` restart policy is the default and most restrictive policy.
A child with the `never` policy is terminated upon its first non-graceful
termination and is NEVER restarted by the host.
The `never` policy is appropriate for one-shot child agents whose failure
is considered a terminal condition, such as batch processing tasks,
one-time computations, or children whose sole purpose is to produce a
single result.

> **Normative implementation-defined choice.**
The host MUST document the circumstances under which a `never` policy
child is eligible for restart.
Under no circumstances MAY the host restart a `never` policy child as
a consequence of its own lifecycle policy evaluation.
A `never` policy child MAY be restarted only if an operator issues an
explicit restart directive through a mechanism outside the scope of this
chapter, which is not a conformance requirement.

> **Normative definition.**
The `bounded-retry` restart policy is the most commonly used policy for
long-running child agents that are expected to be resilient to transient
failures.
A child with the `bounded-retry` policy is restarted up to a maximum
number of attempts, with an increasing backoff between attempts, when
the child terminates due to a failure that the policy classifies as
restartable.
The following parameters define the `bounded-retry` policy:

| Parameter | Content | Default |
|-----------|---------|---------|
| `max_attempts` | The maximum number of restart attempts. | 3 |
| `initial_delay` | The delay before the first restart attempt. | 1 second |
| `max_delay` | The maximum delay between restart attempts. | 60 seconds |
| `backoff_multiplier` | The multiplier applied to the delay after each attempt. | 2 |
| `restartable_failure_codes` | A list of failure codes for which the child is restartable. | `transient-engine-error`, `transient-resource-exhaustion` |
| `non_restartable_failure_codes` | A list of failure codes for which the child is NOT restartable. | `policy-violation`, `malformed-state`, `unauthorized` |

> **Normative definition.**
The `bounded-retry` policy evaluates the child's failure code at each
termination event.
If the failure code is in the `non_restartable_failure_codes` list,
the child is NOT restarted and transitions directly to terminal status.
If the failure code is in the `restartable_failure_codes` list, the child
is restarted after the current backoff delay, up to `max_attempts` total.
If the failure code is in neither list, the host MUST treat it as a
non-restartable failure and transition the child to terminal status.

> **Normative definition.**
The host MUST compute the backoff delay between restart attempts using
exponential backoff with a ceiling, as defined by the formula
`delay(n) = min(initial_delay * (backoff_multiplier ** n), max_delay)`
where `n` is the zero-indexed attempt number.
The host MUST pause the child's live actor during the delay period and
MUST NOT emit any lifecycle events other than the periodic `child.lifecycle.retrying`
heartbeat (see the event types section below).

> **Non-normative note.**
The formula above illustrates the exponential backoff computation
used by the `bounded-retry` restart policy.
It is provided for clarity and does not impose a specific implementation
requirement beyond the bounded-time behavior defined in the surrounding
normative text.

> **Non-normative note.**
The exponential backoff with a ceiling prevents both immediate retry
storms and unbounded waiting.
A `max_attempts` of 3 with `initial_delay` of 1 second and
`backoff_multiplier` of 2 produces delays of 1s, 2s, and 4s before
each retry attempt, which is sufficient to allow most transient
infrastructure issues to resolve while limiting total restart time
to under 10 seconds.

> **Normative definition.**
The `restart-on-infrastructure-failure` restart policy is a middle ground
between `never` and `bounded-retry`.
A child with the `restart-on-infrastructure-failure` policy is restarted
only when the termination event's reason code is one of the
infrastructure failure codes defined below.
All other termination reasons result in a terminal child status with
NO restart attempt.

| Reason code | Is infrastructure failure | Is restartable |
|------------|--------------------------|---------------|
| `infrastructure-failure` | Yes | Yes |
| `engine-instance-crash` | Yes | Yes |
| `node-network-partition` | Yes | Yes |
| `resource-exhaustion-host-level` | Yes | Yes |
| `transient-engine-error` | No | No |
| `policy-violation` | No | No |
| `operator-requested` | No | No |
| `parent-requested` | No | No |
| `child-requested` | No | No |

> **Non-normative note.**
The `restart-on-infrastructure-failure` policy is appropriate for child
agents that perform critical work where infrastructure failures should
be transparent to the operator but application-level failures (such as
policy violations or operator requests) should NOT be silently retried.
This policy ensures that the child is restarted when the host is
experiencing infrastructure issues but that the child is NOT restarted
when the failure is attributable to the child's own behavior or to
explicit human decisions.

> **Normative definition.**
The `operator-approved` restart policy requires explicit operator approval
before any restart attempt is made.
When a child with the `operator-approved` policy terminates due to a
non-graceful reason, the host MUST:

1. Transition the child to `suspended-pending-operator-approval` status.
2. Emit a `child.lifecycle.pending-operator-approval` event into the
   operator's mailbox (as defined in
   [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md)).
3. Hold the child in the `suspended-pending-operator-approval` status
   until the operator issues an explicit restart directive or the child
   is explicitly terminated by the operator.

> **Normative implementation-defined choice.**
The mechanism by which the host notifies the operator of a
`suspended-pending-operator-approval` child is implementation-defined.
Acceptable mechanisms include: emitting a signal into the operator's
mailbox, sending an out-of-band notification (email, webhook,
messaging system), or setting a flag in the operator's dashboard.
The implementation MUST document its operator notification mechanism
in the conformance profile.

> **Normative definition.**
An operator restart directive for a `operator-approved` policy child
MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `operator_address` | The `TenantQualifiedAgentAddress` of the operator issuing the directive. | Operator request. |
| `target_child` | The `TenantQualifiedAgentAddress` of the child to restart. | Operator request. |
| `restart_nonce` | A random value that prevents replay of operator directives. | Operator request. |
| `approved_at` | The ISO 8601 timestamp of operator approval. | Operator request. |

> **Non-normative note.**
The `restart_nonce` field prevents replay attacks where an adversary
captures a previous operator approval and re-issues it to restart a
child that the operator no longer wishes to restart.
The nonce is recorded in the durable audit log and MUST be unique
across all restart directives for the same child.

> **Non-normative note.**
The `operator-approved` policy is appropriate for child agents that
perform sensitive operations (such as financial transactions,
user-modifying actions, or system-level configuration changes) where
automatic restart could amplify the impact of a failure.
This policy ensures that a human operator reviews and explicitly
approves each restart decision.

### Failure scenarios

> **Normative definition.**
The following six failure scenarios are normative invariants that every
host implementation MUST handle correctly for child agents under any
of the four restart policies.
Each scenario describes a specific race condition, edge case, or
interaction between subsystems that, if handled incorrectly, could
lead to resource leaks, inconsistent state, or security violations.

#### Create/terminate races

> **Normative definition.**
A create/terminate race occurs when a child-create directive and a
termination directive (cancellation, hard stop, or infrastructure
termination) are issued concurrently for the same child address.
The host MUST handle create/terminate races according to the following
rules:

1. If the child-create directive is admitted before the termination
   directive, the child enters the `pending` status and the termination
   directive is applied to the child in its current status.
2. If the termination directive is admitted before the child-create
   directive, the child-create directive MUST be rejected with the
   diagnostic `child.create.terminated-before-created` and the child
   address MUST be reserved for the duration of the termination
   processing to prevent a race-condition-based address reuse attack.
3. If both directives are admitted in the same journal commit, the
   child-create directive takes precedence and the termination
   directive is queued for application after the child reaches a
   non-pending status.

> **Non-normative note.**
Rule 2 is a security invariant.
Without address reservation, an adversary could issue a termination
directive for an address, then issue a child-create directive for the
same address, causing the newly created child to inherit the terminated
status and potentially bypass lifecycle policy evaluation.
The reservation duration must be documented in the conformance profile
and MUST be at least as long as the maximum termination processing time.

#### Parent loss

> **Normative definition.**
Parent loss occurs when a child's parent agent is deleted, terminated,
or becomes unresolvable in the durable registry while the child is
still active.
The host MUST handle parent loss according to the following rules:

1. When the host detects parent loss (via the orphan detection mechanism
   defined in section 36.1), the host MUST emit a
   `child.lifecycle.orphaned` event into the child's mailbox.
2. The host MUST evaluate the child's restart policy to determine
   whether the child should be restarted, held in suspended status,
   or terminated.
3. For the `never` policy: the child is NOT restarted and is held in
   `suspended-parent-loss` status pending operator intervention.
4. For the `bounded-retry` policy: the child is restarted according
   to the standard `bounded-retry` schedule if the termination reason
   is in the `restartable_failure_codes` list.
5. For the `restart-on-infrastructure-failure` policy: the child is
   NOT restarted because parent loss is not an infrastructure failure.
6. For the `operator-approved` policy: the child transitions to
   `suspended-pending-operator-approval` status and the operator
   is notified via the mechanism defined in the restart-on-infrastructure-failure section.

> **Non-normative note.**
The differential handling of parent loss by restart policy reflects the
expected operational intent of each policy.
A `never` policy child is a one-shot task; its parent's loss means
there is no one to orchestrate it, so it should not be restarted.
A `bounded-retry` policy child is expected to be resilient; if the
parent loss is coincident with a transient infrastructure issue,
restarting the child is appropriate.
A `restart-on-infrastructure-failure` policy child is only restarted
for infrastructure failures; parent loss is not an infrastructure
failure, so the child is not restarted.
An `operator-approved` policy child requires explicit approval for
any restart, which is appropriate for sensitive operations.

#### Initialization failure

> **Normative definition.**
Initialization failure occurs when a child's live actor fails to
complete initialization (the `child.lifecycle.activated` event is
emitted but the `child.lifecycle.initialized` event is not emitted
within the bounded initialization timeout) or fails during initialization
due to an invalid initial state, missing capability, or host-level error.
The host MUST handle initialization failure according to the following
rules:

1. If the child does not emit `child.lifecycle.initialized` within the
   bounded initialization timeout (documented in the conformance
   profile), the host MUST emit a `child.lifecycle.failed` event with
   failure code `initialization-timeout` and apply the child's restart
   policy to determine whether the child is restarted.
2. If the child emits a `child.lifecycle.failed` event during
   initialization with a failure code in the `non_restartable_failure_codes`
   list of the child's restart policy, the child is NOT restarted.
3. If the child emits a `child.lifecycle.failed` event during
   initialization with a failure code in the `restartable_failure_codes`
   list of the child's restart policy, the child is restarted according
   to the standard restart schedule.
4. If the child's initial state is structurally invalid against the
   manifest's input schema, the child-create directive is rejected at
   admission time (see section 36.1) and the child is never activated.

> **Non-normative note.**
The bounded initialization timeout prevents children from being stuck
in the `pending` status indefinitely due to a hung initialization.
The timeout must be documented in the conformance profile and MUST be
longer than the maximum expected initialization time for any valid
manifest, with headroom for infrastructure latency.
The differentiation between restartable and non-restartable initialization
failures is consistent with the `bounded-retry` policy's treatment of
other failure codes: transient initialization issues (such as missing
capabilities that are being provisioned) are retryable, while
structural issues (such as invalid initial state) are not.

#### Restart exhaustion

> **Normative definition.**
Restart exhaustion occurs when a child with the `bounded-retry` policy
has been restarted the maximum number of times (`max_attempts`) and
has failed again, or when a child with the `operator-approved` policy
has been terminated and the operator has not issued a restart directive
within a reasonable time.
The host MUST handle restart exhaustion according to the following rules:

1. For the `bounded-retry` policy: when the child has been restarted
   `max_attempts` times and has failed again, the host MUST transition
   the child to `terminated-restart-exhausted` status and emit a
   `child.lifecycle.failed` event with reason code `restart-exhausted`.
2. For the `operator-approved` policy: the child remains in
   `suspended-pending-operator-approval` status indefinitely until the
   operator issues a restart directive or a termination directive.
   The host MUST periodically (at intervals documented in the conformance
   profile) emit a `child.lifecycle.pending-operator-approval` reminder
   into the operator's mailbox until the operator acts.

> **Non-normative note.**
Restart exhaustion is a terminal condition for `bounded-retry` children
because the host has exhausted its budget for automatic recovery.
The `restart-exhausted` reason code is one of the immediate escalation
reasons in the cancellation taxonomy defined in section 36.1, which
means that if a cancellation is in progress when restart exhaustion
occurs, the host MUST escalate to termination immediately.
For `operator-approved` children, the indefinite suspension is intentional:
the operator is expected to act on the child's lifecycle, and the host
should not make that decision on the operator's behalf.

#### Duplicate lifecycle events

> **Normative definition.**
Duplicate lifecycle events occur when the same lifecycle event is
delivered to the child's mailbox more than once, either due to
network retries, host restarts, or subscription evaluation races.
The host MUST handle duplicate lifecycle events according to the following
rules:

1. Every child lifecycle event includes a `sequence_number` that is
   monotonically incremented for each event emitted into the child's
   mailbox (see section 36.1).
2. The child's live actor MUST track the highest `sequence_number`
   it has processed and MUST discard any event with a `sequence_number`
   less than or equal to the highest processed `sequence_number`.
3. If a duplicate event is discarded, the host MUST record the discard
   in the evidence log with the original `sequence_number` to enable
   operators to detect and diagnose duplicate event delivery.

> **Non-normative note.**
The `sequence_number` field enables at-least-once delivery semantics
with duplicate detection at the child agent level.
Without this field, the child's live actor would have no way to
distinguish a legitimate new event from a duplicate, leading to
potential state corruption (e.g., processing a `child.lifecycle.accepted`
event twice could cause the child to initialize twice).
The evidence log recording of discarded duplicates provides operators
with visibility into delivery reliability without adding overhead to
the normal event processing path.

> **Normative definition.**
Duplicate detection is performed by the child's live actor, not by the
host.
The host is responsible for ensuring that the `sequence_number` field
is correctly assigned and monotonically incremented.
The child's live actor is responsible for implementing the duplicate
detection logic using the `sequence_number` field.
This separation of responsibilities is consistent with the
single-agent host flow defined in
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
where the host provides the signal envelope and the live actor processes
the signal content.

#### Grant revocation

> **Normative definition.**
Grant revocation occurs when a child agent's grants are revoked as a
consequence of cancellation, termination, or lifecycle policy evaluation.
Grant revocation MUST be performed according to the following rules:

1. When a child is cancelled, the host MUST revoke all grants associated
   with the child according to the `grant_revocation_scope` specified
   in the cancellation directive (see section 36.1).
2. When a child is terminated (non-gracefully), the host MUST revoke
   all grants associated with the child with `grant_revocation_scope: all`,
   regardless of the termination reason.
3. When a child is completed, the host MUST revoke all grants associated
   with the child with `grant_revocation_scope: derived-only`, revoking
   only grants that were derived from the child (not the grants that
   were inherited from the parent).
4. Grant revocation is recorded in the evidence log with the `child_address`,
   the `grant_revocation_scope`, and the `termination_id` or
   `cancellation_id` that triggered the revocation.

> **Non-normative note.**
The differential grant revocation by lifecycle outcome reflects the
principle of least privilege.
A cancelled child's grants are revoked according to the cancelling
principal's specification because the cancellation was a deliberate
action.
A terminated child's grants are always fully revoked because termination
is a host-level safety action that assumes the child may have been
compromised or misbehaving.
A completed child's grants are only partially revoked because completion
is a normal, expected outcome and the child's derived grants (grants
obtained during execution that were not part of the original grant scope)
should be revoked, but the child's original inherited grants should
remain available for the child's parent.
This is consistent with the grant scope attenuation model defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Cross-reference summary

> **Normative definition.**
The behavior and integration defined in this section integrate with the
following existing chapters:

1. **Monitor subscriptions**: Subscription admission is governed by
   the atomic commit protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
   Subscription access control is governed by the capability model
   defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
   Subscription delivery routes events to subscriber mailboxes as
   defined in
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
2. **Restart policies**: The `bounded-retry` backoff schedule is
   implemented by the host's scheduler as defined in
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).
   The `operator-approved` operator notification is delivered via the
   signal ingress mechanism defined in
   [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md).
   Restart policy selection is recorded as evidence in the format
   defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
3. **Failure scenarios**: Create/terminate race address reservation
   is enforced by the agent registry defined in
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).
   Parent loss orphan detection is performed by the lifecycle monitor
   as defined in
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).
   Initialization failure timeout is bounded by the turn lease limits
   defined in
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
   Duplicate event detection uses the sequence number model defined in
   [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
   Grant revocation is enforced by the capability policy engine as
   defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

> **Non-normative note.**
The nine integration points above demonstrate that behavior and integration
is the connective tissue between the contract and data model (section 36.1)
and the failure evidence and operational notes (section 36.3).
Every subsystem that interacts with child lifecycle events must be
aware of the subscription model, restart policy semantics, and failure
scenario invariants defined in this section.

> **Normative definition.**
When this section and another section of this specification appear to
conflict on a behavior question, the following precedence rules apply:

1. For monitor subscription lifecycle: this section takes precedence
   over
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   for questions of subscription delivery timing and duplicate handling.
2. For restart policy evaluation: this section takes precedence over
   [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md)
   for questions of child-specific restart semantics.
3. For grant revocation scope: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of child-specific grant revocation behavior.
4. For operator notification: this section takes precedence over
   [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md)
   for questions of operator approval notification content and timing.

## Variability and limits

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
| 36.2 Monitor subscriptions | Normative implementation-defined choice | The mechanism by which the host evaluates active subscriptions against emitted events (in-memory tables, subscription-aware event bus, or polling). Must be documented in the conformance profile. |
| 36.2 Monitor subscriptions | Normative implementation-defined choice | The maximum number of active monitor subscriptions per subscriber. Must be at least 100 and documented in the conformance profile. |
| 36.2 Monitor subscriptions | Normative implementation-defined choice | The retention period for closed monitor subscriptions in the durable subscription log. Must be at least 24 hours and documented in the conformance profile. |
| 36.2 Restart policies | Normative implementation-defined choice | The default parameter values for the `bounded-retry` restart policy (max_attempts, initial_delay, max_delay, backoff_multiplier, restartable_failure_codes, non_restartable_failure_codes). Must be documented in the conformance profile. |
| 36.2 Restart policies | Normative implementation-defined choice | The mechanism by which the host notifies the operator of a `suspended-pending-operator-approval` child (mailbox signal, webhook, email, dashboard flag). Must be documented in the conformance profile. |
| 36.2 Restart policies | Normative implementation-defined choice | The maximum restart_nonce entropy (in bits) for operator-approved restart directives. Must be at least 128 bits and documented in the conformance profile. |
| 36.2 Failure scenarios | Normative implementation-defined choice | The address reservation duration for create/terminate races, in seconds. Must be at least 30 seconds and documented in the conformance profile. |
| 36.2 Failure scenarios | Normative implementation-defined choice | The bounded initialization timeout for child live actors, in seconds. Must be at least 60 seconds and documented in the conformance profile. |
| 36.2 Failure scenarios | Normative implementation-defined choice | The periodic reminder interval for `operator-approved` children in `suspended-pending-operator-approval` status, in seconds. Must be at most 3600 seconds (1 hour) and documented in the conformance profile. |

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
| Maximum active monitor subscriptions per subscriber | 100 | Consistent with mailbox turn lease limits. |
| Maximum operator restart_nonce entropy | 128 bits | Prevents replay attacks. |
| Maximum subscription closed-log retention | Unbounded by default | Hosts MAY impose local limits; must be at least 24 hours. |

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

## 36.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for child lifecycle
cancellation monitoring and restart policy:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current lifecycle policy
   version or artifact version.
3. **Conflicting**: Multiple principals attempt to control the same child
   concurrently (optimistic concurrency conflict).
4. **Unauthorized**: The caller does not have permission to perform the
   operation on the target child.
5. **Exhausted**: The system is out of resources (e.g., restart budget,
   monitor subscription quota, grant scope).
6. **Unavailable**: The child agent, the host's lifecycle monitor, or a
   required dependency is unavailable.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.
The error codes defined below are the normative set for child lifecycle
cancellation monitoring and restart policy.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for child lifecycle cancellation
monitoring and restart policy:

| Error Code | Description |
|------------|-------------|
| `child.create.malformed` | Child-create directive fails schema validation |
| `child.create.manifest-artifact-mismatch` | Manifest does not declare the artifact (see [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md)) |
| `child.create.duplicate-directive-id` | Directive ID matches already-admitted directive |
| `child.create.unauthorized` | Owner address not active in durable registry (see [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md)) |
| `child.create.incompatible` | Lifecycle policy reference does not name a defined policy |
| `child.create.exhausted` | Restart budget or subscription quota exhausted (see [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md)) |
| `child.create.unavailable` | Agent registry or manifest registry unavailable |
| `child.lifecycle.unauthorized` | Subscriber lacks `observe.child.lifecycle` capability (see [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)) |
| `child.lifecycle.subscription.conflict` | Multiple subscription requests for same child and event set concurrently |
| `child.lifecycle.grant_revocation.unauthorized` | Cancelling principal lacks grant revocation capability |
| `child.lifecycle.restart.exhausted` | `bounded-retry` policy `max_attempts` reached |
| `child.lifecycle.restart.policy-violation` | Non-restartable failure code encountered |
| `child.lifecycle.parent-loss.unauthorized` | Operator lacks parent-loss resolution capability |
| `child.cancellation.unauthorized` | Cancelling principal lacks cancellation capability for target child |
| `child.cancellation.conflict` | Cancellation conflicts with in-flight restart or lifecycle transition |
| `child.cancellation.unavailable` | Child live actor or mailbox unavailable during cancellation |
| `child.hard_stop.exhausted` | Hard stop exceeds bounded time |
| `child.acknowledgement.timeout` | Cancellation acknowledgement timeout (see [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)) |
| `child.monitor.unavailable` | Lifecycle monitor or subscription evaluation unavailable |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome.
The diagnostics MUST include:

1. **Error code**: The specific error code from the table above.
2. **Context**: The operation that failed (e.g., child-create admission,
   cancellation propagation, restart evaluation, subscription delivery).
3. **Entity identifiers**: The `child_address`, `directive_id`,
   `cancellation_id`, `subscription_id`, or `subscriber_address` involved
   (without exposing sensitive data).
4. **Timestamp**: The time the error occurred.
5. **Retryable**: Whether the operation can be retried.
6. **Restart policy impact**: If the failure interacts with a restart
   policy, the diagnostic MUST indicate whether the failure is restartable
   or terminal per the policy definition.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

> **Non-normative note.**
The `Restart policy impact` field is a critical differentiator for this
chapter's diagnostics.
Because child lifecycle failures are evaluated against restart policies,
an operator MUST be able to distinguish from the diagnostic alone whether
a failure will trigger a restart or transition the child to terminal status.
This is consistent with the bounded-diagnostic requirement defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

### Bounded evidence requirements

> **Normative definition.**
The host MUST record the following evidence for each failure outcome:

1. **Error code and diagnostic**: As defined in the diagnostics section.
2. **Child address**: The `TenantQualifiedAgentAddress` of the affected child.
3. **Directive identity** (if applicable): The `directive_id` or
   `cancellation_id` associated with the failed operation.
4. **Snapshot at failure**: The child's snapshot at the time of failure,
   recorded as defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
5. **Restart policy state**: The current restart policy state (attempt
   count, next backoff delay, remaining budget) at the time of failure.
6. **Timestamp**: The time the evidence was recorded.
7. **Evidence digest**: A deterministic hash of the evidence record,
   as defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Non-normative note.**
The evidence record provides operators with a durable, auditable trail of
every failure outcome that affects a child agent.
The `evidence_digest` field enables downstream systems (such as the
provenance and audit layer) to verify that the evidence record has not
been tampered with after creation.
The `restart_policy_state` field is specific to child lifecycle and
enables operators to reconstruct the full restart sequence for a failed
child without consulting additional subsystem logs.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:

1. **Error code taxonomy extension**: Hosts MAY define additional error
   codes beyond the table above for implementation-specific observations.
   Additional codes MUST not conflict with the existing codes and MUST be
   documented in the conformance profile.
2. **Diagnostic format**: The exact format of diagnostic messages is
   implementation-defined, provided they satisfy the bounded-diagnostic
   requirements above.
3. **Evidence retention**: The retention period for failure evidence records
   is implementation-defined, provided it is at least as long as the
   maximum restart budget (e.g., `max_attempts` for `bounded-retry`) plus
   the operator-approved suspension period.
4. **Diagnostic delivery**: The mechanism by which diagnostics are delivered
   to operators (log file, structured output, external monitoring system)
   is implementation-defined.
5. **Restart policy state sampling**: The granularity of restart policy
   state recording (e.g., every attempt boundary vs. continuous state) is
   implementation-defined.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Cross-process failure correlation**: Correlation of child lifecycle
   failures across multiple host processes in a distributed deployment.
   The protocol is language-neutral and does not require distributed
   correlation for base conformance.
2. **Failure pattern analysis**: Automated analysis of failure patterns
   across children with the same restart policy or artifact to identify
   systemic issues.
   This is planned for future milestones.
3. **Dynamic restart policy adjustment**: The ability to change a child's
   restart policy after creation is deferred.
   The policy is currently immutable for the lifetime of the child.
4. **Operator-approved restart deadline**: A default deadline after which
   an unapproved `operator-approved` policy child transitions to terminal
   status.
   The current specification holds indefinitely.
5. **Failure evidence export API**: A formal API for exporting failure
   evidence records to external systems.
   The protocol is language-neutral and does not require an export API
   for base conformance.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 2 MAY invalidate earlier milestone
assumptions:

1. **Restart budget exhaustion rate**: If the rate of restart budget
   exhaustion exceeds the capacity planned in earlier milestones, the
   capacity plan MUST be revised.
2. **Subscription evaluation overhead**: If subscription evaluation overhead
   exceeds the turn timeout, the timeout or subscription model MUST be
   revised.
3. **Evidence record size**: If evidence record size exceeds storage
   capacity planned in earlier milestones, the storage plan MUST be
   revised.
4. **Cancellation acknowledgement latency**: If cancellation acknowledgement
   latency exceeds the `deadline`, the deadline or cancellation flow MUST
   be revised.
5. **Hard stop bounded time**: If hard stop exceeds the bounded time
   documented in the conformance profile, the Extism invocation boundary
   MUST be revised to support faster termination.
6. **Duplicate event frequency**: If duplicate event delivery frequency is
   higher than expected, the mailbox ordering and delivery guarantees
   defined in
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
   MUST be revised.

> **Non-normative note.**
If any result from Phase 2 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.
This is consistent with the cross-milestone revision protocol defined in
[Specification Authority](../SPECIFICATION-AUTHORITY.md).
