---
title: "Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model"
kind: specification
created: "2026-08-09"
status: normative
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

This chapter is a normative specification produced by
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
live actor as a child of an existing parent agent, establishing durable paired
`child` and `parent` relationships, allocating an address in the
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
and binding the child to a deterministic request identity, lifecycle policy,
grant scope, and initial state.

> **Normative definition.**
Every child-create directive MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `directive_id` | A deterministic request identity derived from parent address, artifact digest, manifest digest, initial state hash, owner address, lifecycle policy reference, grant scope hash, and a monotonic sequence number. | Directive construction. |
| `directive_sequence` | The monotonic per-parent `u64` sequence reserved for this distinct directive. | Parent directive construction. |
| `parent_address` | The `TenantQualifiedAgentAddress` of the existing parent agent. | Authenticated directive context. |
| `child_address` | The canonical `TenantQualifiedAgentAddress` reserved for the prospective child before consent is signed. | Host address allocator. |
| `artifact` | The WASM artifact digest and selection that the child's live actor will execute. | [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md). |
| `manifest` | The reviewed manifest record that declares the artifact's declared capabilities, input schema, output schema, and trust tier. | [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md). |
| `initial_state` | The serialized initial state document that becomes the child's first snapshot revision. | [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md). |
| `owner` | The `TenantQualifiedAgentAddress` of the parent agent that created the child. | [Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md). |
| `lifecycle_policy` | A reference to one of the restart policies defined in section 36.1, selecting the behavioral class for this child. | This chapter. |
| `grants` | The attenuated grant scope inherited from the parent, subject to the limits defined in [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). | [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). |
| `parent_consent` | The existing parent's ordinary signed target-consent record for the `parent` relationship from child to parent. | Parent agent principal. |
| `bootstrap_consent` | The one-use `ChildBootstrapConsent` that authorizes the prospective child to become the target of the paired `child` relationship. | Authorized user or operator. |
| `request_context` | Optional tenant-qualified metadata describing the originating user request or upstream directive that triggered the creation. | Host runtime. |

> **Normative definition.**

```
ChildBootstrapConsent {
  directive_id: string,
  parent_address: TenantQualifiedAgentAddress,
  prospective_child_address: TenantQualifiedAgentAddress,
  artifact_digest: ArtifactDigest,
  manifest_digest: string,
  relationships: ["child:parent-to-child", "parent:child-to-parent"],
  issued_by: PrincipalAddress,
  issued_at: ISO8601,
  expires_at: ISO8601,
  nonce: string,
  signature: bytes
}
```

`issued_by.kind` MUST be `user` or `operator`. The signature MUST be Ed25519
over the SHA-256 digest of the Canonical JSON encoding of the record with
`signature` omitted. The authorizer MUST be authenticated, authorized to create
the exact child, and in the same tenant unless an explicit cross-tenant grant
authorizes the creation. `relationships` has the exact order and values shown.

> **Normative definition.**
The `directive_id` is the lowercase hexadecimal SHA-256 digest of a canonical
byte sequence. In the order listed below, each of the first seven UTF-8
components is encoded as an unsigned 64-bit big-endian byte length followed by
exactly that many bytes:

1. parent agent address;
2. artifact digest;
3. manifest digest;
4. initial state hash;
5. owner address;
6. lifecycle policy reference;
7. grant scope hash; and
8. the unsigned 64-bit big-endian value of `directive_sequence`, a monotonic per-parent sequence
   counter, appended as exactly eight bytes without a length prefix.

The parent and owner components are their canonical address strings from
Chapter 35. The artifact and manifest components are their exact canonical
digest strings from Chapter 03. The initial-state and grant-scope components
are lowercase hexadecimal SHA-256 digests of their Canonical JSON encodings
under [Chapter 04](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).
The lifecycle-policy component is the exact lowercase policy name from this
chapter. `directive_sequence` starts at 1, increases by one for each distinct
directive constructed by that parent, and MUST NOT be reused. A retransmission
MUST reuse the original `directive_sequence` and `directive_id` rather than
construct a new directive. Zero or reuse for a distinct directive is malformed
and MUST be rejected with `child.create.malformed`.
The per-parent sequence allocator and the mapping from reserved sequence to
`directive_id` MUST be durable and reserved atomically before directive
emission.

No separator, alternate hash algorithm, alternate component order, or wider
counter scope is permitted.
The resulting `directive_id` MUST contain exactly 64 lowercase hexadecimal
characters; any other representation is malformed and MUST be rejected with
`child.create.malformed`.
The `directive_id` is deterministic: the same inputs in the same order
always produce the same `directive_id`, regardless of the host process,
engine instance, or physical node on which the directive is evaluated.

> **Normative definition.**
Deterministic `directive_id` values serve three purposes: (1) they enable
exact deduplication of retransmissions of the same constructed directive while
keeping distinct same-content directives unique through the per-parent
counter; (2) they provide a stable reference for lifecycle
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
   declared input schema and MUST NOT exceed 65536 bytes. Exceeding this fixed
   limit MUST be rejected with `child.create.initial-state-limit`.
5. The `lifecycle_policy` reference MUST name a policy defined by this
   chapter's normative policy table.
6. The `grants` scope MUST not exceed the parent's current grant scope.
7. `parent_address` MUST be the authenticated parent constructing the directive,
   `owner` MUST equal `parent_address`, and `child_address` MUST equal the
   uncommitted address reservation named by both relationship records.
8. `parent_consent` MUST be valid ordinary target consent for the `parent`
   relationship from `child_address` to `parent_address`.
9. `bootstrap_consent` MUST satisfy the fixed child-consent bootstrap in
   Chapter 35, bind `directive_id`, `parent_address`, `child_address`, the two
   fixed relationship directions, artifact and manifest digests, and remain
   unused and unexpired. Through `directive_id`, it also binds initial state,
   owner, lifecycle policy, grants, and `directive_sequence` without a circular
   signature dependency.
10. `directive_id` MUST equal the fixed SHA-256 construction above for the
    directive fields and `directive_sequence`; a mismatch MUST be rejected with
    `child.create.malformed`.
11. A child-create directive whose `directive_id` matches an already-admitted
   directive (recorded in the durable state journal) MUST be rejected with
   the diagnostic `child.create.duplicate-directive-id`.
12. The canonical string representation of the parent, owner, and allocated
   child address MUST NOT exceed 256 characters. Exceeding this fixed
   child-lifecycle address bound MUST be rejected with
   `child.create.address-limit` before any registry entry is created.

> **Non-normative note.**
The twelve validation rules above ensure that child creation is a
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

1. Write the child agent's registry entry with `status: pending` and the
   directive's reserved `child_address`.
2. Create the `child` relationship from parent to child and the `parent`
   relationship from child to parent, consuming the validated
   `parent_consent` and `bootstrap_consent` in the same commit.
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

> **Normative definition.**
`maximum_child_failure_message_bytes` is a named implementation limit. It MUST
be a finite integer of at least 1024 and MUST be disclosed in the conformance
profile; the default is 4096 bytes. A longer `failure_message` MUST be truncated
at a valid UTF-8 boundary, and the host MUST emit
`child.lifecycle.failure-message-truncated` with the original byte count and a
SHA-256 digest of the untruncated message.

> **Normative definition.**
The canonical encoded payload of a child lifecycle event MUST NOT exceed 65536
bytes. An event-causing request that would exceed this fixed bound MUST be
rejected before state mutation with `child.lifecycle.event-payload-limit`.
For child lifecycle events, this narrower bound and diagnostic explicitly
replace the general 1 MiB `signal.oversized` rule in
[Signal size bounds](10-signals-causality-routing-and-delivery.md#signal-size-bounds).

> **Non-normative note.**
The eight event types above cover the complete set of lifecycle transitions
that a child agent can experience from creation through final resolution.
Operational notification signals such as `child.lifecycle.retrying` and
`child.lifecycle.pending-operator-approval` are not lifecycle event types and
MUST NOT be accepted in a monitor subscription's `event_types` set.
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
The host MUST record the child's last completed durable revision as
`snapshot_at_termination` in the evidence record defined
in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

> **Normative definition.**
The `child.lifecycle.orphaned` event is emitted when the host detects
that a child's parent agent is no longer resolvable in the durable
registry or has reached a terminal status.
The host's lifecycle monitor MUST evaluate orphan status at least once every
60 seconds. Its scheduling mechanism is internal, but for the same registry
history it MUST emit the same orphan event no later than 60 seconds after the
parent becomes terminal or unresolvable.
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
The canonical `cancellation_id` MUST NOT exceed 256 characters. An otherwise
valid cancellation with a longer identifier MUST be rejected with
`child.cancellation.id-limit` without emitting an event or changing child
state.

> **Normative definition.**
The `deadline` field is required; there is no default. It MUST be no earlier
than receipt of the cancellation and no later than 600 seconds after receipt.
A missing deadline or a deadline before receipt MUST be rejected with
`child.cancellation.malformed`. A deadline more than 600 seconds after receipt
MUST be rejected with `child.cancellation.deadline-limit` without emitting a
cancellation event or changing child state. Deadline detection is internal, but
every mechanism MUST make the same acknowledgement-versus-timeout decision at
the specified instant.

The optional human-readable cancellation-reason message MUST NOT exceed 1024
characters. A longer message MUST be rejected with
`child.cancellation.reason-limit` without changing child state.

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
3. The host MUST record the child's last completed durable revision as
   `snapshot_at_termination` in the evidence log. Mid-turn memory MUST NOT be
   used as a recovery snapshot.
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
The snapshot captured at hard stop is the last completed durable revision.
Volatile mid-turn memory MAY be retained only as redacted evidence and MUST NOT
be used to reactivate the child.

> **Normative definition.**
The mechanism used to issue hard stop is internal. Every mechanism MUST prevent
all further guest execution and signal processing, revoke grants, record the
same last-completed snapshot and lifecycle event, and complete within 30
seconds. Failure to complete within 30 seconds MUST emit
`child.hard_stop.exhausted`, quarantine the instance, and leave the child in
`terminated` state.

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
| `subscriber_address` | The `AddressablePrincipal` of the subscriber. Parents and peers use `TenantQualifiedAgentAddress`; users and operators use `PrincipalAddress`. | Subscription request. |
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

> **Normative definition.**
The mechanism used to evaluate active subscriptions is internal. For the same
durable subscriptions and ordered lifecycle events, every mechanism MUST
deliver the same `child.lifecycle.observed` signals in the same order, without
duplicates beyond the specified at-least-once delivery behavior and without
holding a durable live handle.

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
for 24 hours and MAY be replayed by subscribers that missed earlier events
during that period. At 24 hours the host MUST remove the closed subscription
from the log and record a `subscription.retention-expired` evidence event.

> **Normative definition.**
`maximum_active_monitor_subscriptions_per_subscriber` is a named implementation
limit. It MUST be a finite integer of at least 100 and MUST be disclosed in the
conformance profile; the default is 100. An otherwise valid subscription that
would exceed the disclosed limit MUST be rejected with
`child.monitor.subscription-limit` without creating a durable record.

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

Under no circumstances MAY the host restart a `never` policy child as
a consequence of its own lifecycle policy evaluation.
An operator-issued restart mechanism is outside this chapter's scope and
does not alter the `never` lifecycle policy.

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
`maximum_restart_attempts` is a named implementation limit. It MUST be a finite
integer of at least 3 and MUST be disclosed in the conformance profile; the
default is 3. A `bounded-retry` policy whose `max_attempts` exceeds the
disclosed limit MUST be rejected with `child.lifecycle.restart.limit-exceeded`
before child creation or policy replacement changes durable state.

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
MUST NOT emit any lifecycle event during that period. It MUST emit a periodic
`child.lifecycle.retrying` operational notification signal containing
`child_address`, `attempt_number`, `next_retry_at`, and `remaining_attempts`.
This signal is not a lifecycle event and does not participate in lifecycle
event sequencing or monitor-subscription matching.

> **Non-normative note.**
The formula above defines the observable exponential backoff computation
used by the `bounded-retry` restart policy. Implementations may vary internally,
but MUST produce the exact delays required by the formula.

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
2. Emit a `child.lifecycle.pending-operator-approval` operational notification
   signal into the
   operator's mailbox (as defined in
   [Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md)).
3. Hold the child in the `suspended-pending-operator-approval` status
   until the operator issues an explicit restart directive or the child
   is explicitly terminated by the operator.

> **Normative definition.**
The host MUST notify the operator by emitting the
`child.lifecycle.pending-operator-approval` operational notification signal,
containing `child_address`, `operator_address`, `suspended_at`, and
`reminder_number`, into the operator's mailbox. This signal is not a lifecycle
event and does not participate in lifecycle event sequencing or
monitor-subscription matching.
Out-of-band email, webhook, or dashboard notifications MAY mirror that signal,
but they MUST NOT replace it or alter restart authorization or timing.

> **Normative definition.**
An operator restart directive for a `operator-approved` policy child
MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `operator_address` | The `PrincipalAddress` with `kind: "operator"` of the operator issuing the directive. | Operator request. |
| `target_child` | The `TenantQualifiedAgentAddress` of the child to restart. | Operator request. |
| `restart_nonce` | A random value that prevents replay of operator directives. | Operator request. |
| `approved_at` | The ISO 8601 timestamp of operator approval. | Operator request. |

> **Non-normative note.**
The `restart_nonce` field prevents replay attacks where an adversary
captures a previous operator approval and re-issues it to restart a
child that the operator no longer wishes to restart.
The nonce is recorded in the durable audit log and MUST be unique
across all restart directives for the same child.

> **Normative definition.**
The `restart_nonce` MUST contain at least 128 bits of entropy from a
cryptographically secure random source. A nonce with less entropy or a reused
nonce MUST be rejected with `child.lifecycle.restart.nonce-invalid` before any
restart state transition.

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
   address MUST be reserved for exactly 30 seconds after termination admission
   to prevent a race-condition-based address reuse attack.
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
The fixed 30-second reservation equals the hard-stop completion deadline.

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
   is notified as defined in [Restart policies](#restart-policies).

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
   fixed 60-second initialization timeout, the host MUST emit a
   `child.lifecycle.failed` event with
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
The timeout is 60 seconds from emission of `child.lifecycle.activated`.
The differentiation between restartable and non-restartable initialization
failures is consistent with the `bounded-retry` policy's treatment of
other failure codes: transient initialization issues (such as missing
capabilities that are being provisioned) are retryable, while
structural issues (such as invalid initial state) are not.

#### Restart exhaustion

> **Normative definition.**
Restart exhaustion occurs when a child with the `bounded-retry` policy
has been restarted the maximum number of times (`max_attempts`) and
has failed again. An `operator-approved` child does not exhaust while waiting;
it remains suspended indefinitely as defined below.
The host MUST handle restart exhaustion according to the following rules:

1. For the `bounded-retry` policy: when the child has been restarted
   `max_attempts` times and has failed again, the host MUST transition
   the child to `terminated-restart-exhausted` status and emit a
   `child.lifecycle.failed` event with reason code `restart-exhausted`.
2. For the `operator-approved` policy: the child remains in
   `suspended-pending-operator-approval` status indefinitely until the
   operator issues a restart directive or a termination directive.
   The host MUST emit a `child.lifecycle.pending-operator-approval` operational
   reminder signal
   every 3600 seconds
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

## Variability register

The register below summarizes fixed behavior, internal mechanisms, named
implementation limits, and permitted variations governed by the linked
clauses. It does not independently license variation.

> **Non-normative note.**

| Clause | Variability class | Selection |
|--------|------------------|-----------|
| [36.1 Child-create directives](#child-create-directives) | Required | Length-prefixed canonical input, SHA-256, and a per-parent `u64` sequence counter. |
| [36.1 Child relationship bootstrap consent](#child-create-directives) | Required | One-use Ed25519 consent over the exact prospective child creation; consume atomically with correctly directed `child` and `parent` relationships. |
| [36.1 Child lifecycle events](#child-event-types) | Named implementation limit | `maximum_child_failure_message_bytes`, at least 1024 bytes; default 4096. |
| [36.1 Child address bound](#child-create-directives) | Required fixed limit | 256 canonical characters; use `child.create.address-limit`. |
| [36.1 Initial-state bound](#child-create-directives) | Required fixed limit | 65536 bytes; use `child.create.initial-state-limit`. |
| [36.1 Lifecycle-event bound](#child-event-types) | Required fixed limit | 65536 canonical bytes; use `child.lifecycle.event-payload-limit` instead of the general signal-size diagnostic. |
| [36.1 Cancellation scope and propagation](#cancellation-scope-reason-deadline-and-propagation) | Required | `deadline` is required and must be between receipt time and receipt plus 600 seconds. |
| [36.1 Cancellation identifier bound](#cancellation-scope-reason-deadline-and-propagation) | Required fixed limit | 256 canonical characters; use `child.cancellation.id-limit`. |
| [36.1 Cancellation reason bound](#cancellation-scope-reason-deadline-and-propagation) | Required fixed limit | 1024 characters; use `child.cancellation.reason-limit`. |
| [36.1 Cancellation deadline detection](#cancellation-scope-reason-deadline-and-propagation) | Internal mechanism | Must make the same decision at the specified deadline instant. |
| [36.1 Hard-stop behavior](#hard-stop-behavior) | Internal mechanism | Must preserve termination, grant-revocation, snapshot, event, and diagnostic outcomes. |
| [36.1 Hard-stop deadline](#hard-stop-behavior) | Required | Complete within 30 seconds or emit `child.hard_stop.exhausted`. |
| [36.1 Hard-stop snapshot](#hard-stop-behavior) | Required | Record the last completed durable revision; never recover from mid-turn memory. |
| [36.1 Orphan detection](#child-event-types) | Required | Evaluate at least every 60 seconds. |
| [36.2 Operator-approved orphan handling](#failure-scenarios) | Required | Hold indefinitely until an operator restart or termination directive. |
| [36.2 Monitor subscription evaluation](#monitor-subscriptions-and-durable-lifecycle-notifications) | Internal mechanism | Preserve matching, ordering, delivery, and duplicate behavior. |
| [36.2 Active monitor subscriptions](#monitor-subscriptions-and-durable-lifecycle-notifications) | Named implementation limit | `maximum_active_monitor_subscriptions_per_subscriber`, at least 100; default 100. |
| [36.2 Subscriber and operator addressing](#monitor-subscriptions-and-durable-lifecycle-notifications) | Required | Agents use `TenantQualifiedAgentAddress`; non-agent users and operators use canonical `PrincipalAddress`. |
| [36.2 Closed subscription retention](#monitor-subscriptions-and-durable-lifecycle-notifications) | Required | Retain for 24 hours, then remove with evidence. |
| [36.2 Bounded-retry defaults](#restart-policies) | Required | Use the fixed parameter table in the governing clause. |
| [36.2 Restart attempts](#restart-policies) | Named implementation limit | `maximum_restart_attempts`, at least 3; default 3. |
| [36.2 Operator notification](#restart-policies) | Required | Deliver the mailbox signal; mirrors are optional and non-authoritative. |
| [36.2 Restart nonce](#restart-policies) | Required | At least 128 bits of cryptographic entropy and no reuse. |
| [36.2 Create/terminate reservation](#failure-scenarios) | Required | Reserve the address for 30 seconds. |
| [36.2 Initialization timeout](#failure-scenarios) | Required | 60 seconds after activation. |
| [36.2 Operator reminder](#failure-scenarios) | Required | Emit every 3600 seconds while approval is pending. |
| [36.3 Diagnostic format](#fixed-diagnostic-and-evidence-behavior) | Required | Canonical UTF-8 JSON using the exact Chapter 04 top-level structure and bounded child-lifecycle details. |
| [36.3 Evidence retention](#fixed-diagnostic-and-evidence-behavior) | Required | Retain while non-terminal and for 365 days after terminal resolution. |
| [36.3 Diagnostic delivery](#fixed-diagnostic-and-evidence-behavior) | Required | Return to requester, append to evidence, and notify operator mailbox when applicable. |
| [36.3 Restart-state sampling](#fixed-diagnostic-and-evidence-behavior) | Required | Record every attempt boundary and policy-state transition. |
| [36.1 Volatile hard-stop evidence](#hard-stop-behavior) | Optional | Retain only redacted evidence | Must never be used for reactivation. |
| [36.2 Closed-subscription replay](#monitor-subscriptions-and-durable-lifecycle-notifications) | Optional | Replay only during the fixed 24-hour retention period | Must preserve event order and at-least-once behavior. |
| [36.2 Operator notification mirrors](#restart-policies) | Optional | Mailbox delivery remains authoritative | Mirrors must not alter authorization or timing. |
| [36.3 Continuous restart-state sampling](#fixed-diagnostic-and-evidence-behavior) | Optional | Add to required boundary records | Must not replace a required record. |

### Fixed bounds and implementation limits

| Bound | Class | Required value or floor | Exhaustion behavior |
|-------|-------|-------------------------|---------------------|
| Child address | Fixed limit | 256 canonical characters | Reject with `child.create.address-limit`. |
| `directive_id` representation | Required formation rule | Exactly 64 lowercase hexadecimal characters | Reject malformed representations with `child.create.malformed`. |
| `cancellation_id` | Fixed limit | 256 canonical characters | Reject with `child.cancellation.id-limit`. |
| Child `initial_state` | Fixed limit | 65536 bytes | Reject with `child.create.initial-state-limit`. |
| Lifecycle event payload | Fixed limit | 65536 canonical bytes | Reject with `child.lifecycle.event-payload-limit`. |
| Cancellation reason message | Fixed limit | 1024 characters | Reject with `child.cancellation.reason-limit`. |
| `maximum_child_failure_message_bytes` | Named implementation limit | At least 1024 bytes; default 4096 | Truncate at a UTF-8 boundary and emit `child.lifecycle.failure-message-truncated`. |
| `maximum_active_monitor_subscriptions_per_subscriber` | Named implementation limit | At least 100; default 100 | Reject with `child.monitor.subscription-limit`. |
| `maximum_restart_attempts` | Named implementation limit | At least 3; default 3 | Reject with `child.lifecycle.restart.limit-exceeded`. |

### Closed vocabularies

The cancellation reason taxonomy, the eight child lifecycle event types, and the
three propagation directions are closed. An unknown value is malformed and
MUST be rejected with `child.cancellation.malformed` or
`child.monitor.malformed`, as applicable. Adding a value requires a versioned
normative revision; a conformance profile cannot extend these vocabularies.

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
7. **Timeout**: A required acknowledgement or hard-stop operation exceeds its
   fixed deadline.

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
| `relationship.creation.unauthorized-consent` | Required parent consent or one-use prospective-child bootstrap consent is missing or invalid |
| `child.create.terminated-before-created` | Termination for the reserved child address was admitted before creation |
| `child.create.unauthorized` | Owner address not active in durable registry (see [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md)) |
| `child.create.incompatible` | Lifecycle policy reference does not name a defined policy |
| `child.create.exhausted` | Restart budget or subscription quota exhausted (see [Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md)) |
| `child.create.address-limit` | Parent, owner, or allocated child address exceeds 256 canonical characters |
| `child.create.initial-state-limit` | Child initial state exceeds 65536 bytes |
| `child.create.unavailable` | Agent registry or manifest registry unavailable |
| `child.lifecycle.unauthorized` | Subscriber lacks `observe.child.lifecycle` capability (see [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)) |
| `child.lifecycle.event-payload-limit` | Lifecycle event payload exceeds 65536 bytes |
| `child.lifecycle.subscription.conflict` | Multiple subscription requests for same child and event set concurrently |
| `child.lifecycle.failure-message-truncated` | Failure message exceeded the disclosed byte limit and was truncated with digest evidence |
| `child.lifecycle.grant_revocation.unauthorized` | Cancelling principal lacks grant revocation capability |
| `child.lifecycle.restart.exhausted` | `bounded-retry` policy `max_attempts` reached |
| `child.lifecycle.restart.limit-exceeded` | `max_attempts` exceeds `maximum_restart_attempts` |
| `child.lifecycle.restart.nonce-invalid` | Restart nonce has insufficient entropy or was already used |
| `child.lifecycle.restart.policy-violation` | Non-restartable failure code encountered |
| `child.lifecycle.parent-loss.unauthorized` | Operator lacks parent-loss resolution capability |
| `child.cancellation.unauthorized` | Cancelling principal lacks cancellation capability for target child |
| `child.cancellation.malformed` | Cancellation directive is missing a required field or has an invalid field shape |
| `child.cancellation.conflict` | Cancellation conflicts with in-flight restart or lifecycle transition |
| `child.cancellation.deadline-limit` | Cancellation deadline is more than 600 seconds after receipt |
| `child.cancellation.id-limit` | Cancellation identifier exceeds 256 canonical characters |
| `child.cancellation.reason-limit` | Cancellation reason exceeds 1024 characters |
| `child.cancellation.unavailable` | Child live actor or mailbox unavailable during cancellation |
| `child.hard_stop.exhausted` | Hard stop exceeds bounded time |
| `child.acknowledgement.timeout` | Cancellation acknowledgement timeout (see [Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)) |
| `child.monitor.malformed` | Monitor subscription uses an unknown lifecycle event type or invalid field shape |
| `child.monitor.subscription-limit` | Active monitor subscriptions exceed the disclosed per-subscriber limit |
| `child.monitor.unavailable` | Lifecycle monitor or subscription evaluation unavailable |

> **Normative definition.**
Each diagnostic uses one of the following stable Chapter 02 family codes:

| Family | Domain codes |
|--------|--------------|
| `identity.validation.child_lifecycle` | `child.create.malformed`, `child.lifecycle.restart.nonce-invalid`, `child.cancellation.malformed`, `child.monitor.malformed` |
| `identity.compatibility.child_lifecycle` | `child.create.manifest-artifact-mismatch`, `child.create.incompatible`, `child.lifecycle.restart.policy-violation` |
| `identity.conflict.child_lifecycle` | `child.create.duplicate-directive-id`, `child.create.terminated-before-created`, `child.lifecycle.subscription.conflict`, `child.cancellation.conflict` |
| `identity.authorization.child_lifecycle` | `child.create.unauthorized`, `relationship.creation.unauthorized-consent`, `child.lifecycle.unauthorized`, `child.lifecycle.grant_revocation.unauthorized`, `child.lifecycle.parent-loss.unauthorized`, `child.cancellation.unauthorized` |
| `identity.limit.child_lifecycle` | `child.create.exhausted`, `child.create.address-limit`, `child.create.initial-state-limit`, `child.lifecycle.event-payload-limit`, `child.lifecycle.failure-message-truncated`, `child.lifecycle.restart.exhausted`, `child.lifecycle.restart.limit-exceeded`, `child.cancellation.deadline-limit`, `child.cancellation.id-limit`, `child.cancellation.reason-limit`, `child.hard_stop.exhausted`, `child.acknowledgement.timeout`, `child.monitor.subscription-limit` |
| `identity.resource.child_lifecycle` | `child.cancellation.unavailable`, `child.monitor.unavailable` |
| `identity.storage.child_lifecycle` | `child.create.unavailable` |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic's `details` MUST identify the phase contract, profile, and
failed boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome using the exact
top-level `Diagnostic` structure defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics):
`family`, `code`, `severity`, `message`, and `details`.
`family` MUST be the family assigned above and `code` MUST be the specific
closed-table domain code. `severity` MUST be `error`, except
`child.lifecycle.failure-message-truncated` uses `warning`. `message` MUST be a
human-readable description that does not expose secrets.

The `details` object MUST include `phase`, `contract`, `profile`,
`failed_boundary`, `context`, `entity_identifiers`, `timestamp`, and
`retryable`. `entity_identifiers` contains the applicable `child_address`,
`directive_id`, `cancellation_id`, `subscription_id`, or `subscriber_address`
without exposing sensitive data. If the failure interacts with a restart
policy, `details` MUST also include `restart_policy_impact` with value
`restartable` or `terminal`.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

> **Non-normative note.**
The `restart_policy_impact` detail is a critical differentiator for this
chapter's diagnostics.
Because child lifecycle failures are evaluated against restart policies,
an operator MUST be able to distinguish from the diagnostic alone whether
a failure will trigger a restart or transition the child to terminal status.
This is consistent with the bounded-diagnostic requirement defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

### Bounded evidence requirements

> **Normative definition.**
The host MUST record the following evidence for each failure outcome:

1. **Diagnostic family, code, and canonical diagnostic**: As defined in the
   diagnostics section.
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

### Fixed diagnostic and evidence behavior

> **Normative definition.**
The error-code table above is closed. A diagnostic MUST NOT use an unlisted
domain `code`. Diagnostics MUST be UTF-8 canonical JSON encodings of the exact
Chapter 04 top-level structure and MUST use the canonical member ordering defined by
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).

> **Normative definition.**
Failure evidence for a child that has not reached terminal status MUST be
retained while that status persists. After terminal resolution, the evidence
MUST be retained for 365 days and then deleted through an audited deletion.

> **Normative definition.**
A diagnostic MUST be returned to the requesting principal when a request is
active and MUST always be appended to the durable evidence log. A diagnostic
requiring operator action MUST also be emitted into the operator mailbox. Logs,
webhooks, and dashboards MAY mirror these deliveries but MUST NOT replace or
change them.

> **Normative definition.**
Restart policy state MUST be recorded at every attempt start, attempt
completion, attempt failure, backoff scheduling decision, approval decision,
and lifecycle-policy state transition. Continuous sampling MAY add evidence but
MUST NOT replace any required boundary record.

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
5. **Hard stop bounded time**: If hard stop exceeds the fixed 30-second
   deadline, the Extism invocation boundary
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

## 36.4 Phase 2 Integration Tests

### Test objectives

> **Normative definition.**
Phase 2 integration tests verify that the contracts defined in sections 36.1, 36.2,
and 36.3 of this chapter operate correctly when exercised against the real
dependency boundaries of the multi-agent coordination subsystem.
Integration tests MUST exercise observable contracts rather than private
implementation structure.
This section defines the canonical test scenarios that MUST be run before
this chapter may be promoted from `status: candidate` to `status: normative`.

> **Normative definition.**
The following test objectives are the normative goals for Phase 2 integration
testing.
Every test scenario defined in this section maps to at least one of these
objectives.

| Objective | Description |
|-----------|-------------|
| Canonical flow | The host correctly executes the full child lifecycle from creation through terminal status under normal conditions. |
| Failure handling | The host correctly rejects malformed, incompatible, stale, duplicate, and boundary-limit inputs with stable diagnostics. |
| Lifecycle enforcement | The host correctly applies restart policies, monitors subscriptions, and lifecycle transitions under all conditions. |
| Cancellation propagation | The host correctly propagates cancellations, handles acknowledgements, and escalates to hard stop when required. |
| Restart policy enforcement | The host correctly enforces all four restart policies including never, bounded-retry, infrastructure-failure, and operator-approved. |
| Cross-milestone compatibility | Earlier milestone fixtures continue to pass when the Phase 2 contracts are active. |

> **Non-normative note.**
These six objectives cover the full scope of the Phase 2 integration surface.
A host implementation that passes all test scenarios defined below demonstrates
conformance with this chapter's normative behavior under both normal and
adversarial conditions.
Promotion to `status: normative` requires evidence of a passing run of all
scenarios in this section, recorded in the evidence log as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Successful flow tests

> **Normative definition.**
Successful flow tests verify that the host correctly executes the full child
lifecycle under normal operating conditions.
Each test scenario below describes the test setup, the expected observable
behavior, and the retention requirements for test evidence.

#### Child creation flow

| Test ID | Description |
|---------|-------------|
| `P2-SF-001` | Create a child with a valid child-create directive and verify that all five atomic commit steps are executed (registry entry, parent/child relationships, directive journal entry, mailbox initialization, evidence emission). |
| `P2-SF-001A` | Verify the paired relationships are `child` from parent to child and `parent` from child to parent, the parent supplies ordinary target consent, and the prospective child's one-use bootstrap consent is consumed atomically. |
| `P2-SF-002` | Evaluate the identity construction twice from the same fixed component and `directive_sequence` test vector and verify the same `directive_id`; increment only the sequence and verify a different ID; restart the host and verify the per-parent allocator resumes without reuse. |
| `P2-SF-003` | Create a child with all four restart policy types and verify that each policy is correctly recorded in the registry entry. |
| `P2-SF-004` | Create a child with an attenuated grant scope and verify that the child's grants are strictly a subset of the parent's grants as defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). |
| `P2-SF-005` | Create a child with a valid `request_context` and verify that the context is recorded in the evidence emission. |

> **Normative definition.**
Test `P2-SF-001` is the primary creation test and MUST verify the complete
atomic commit sequence defined in section 36.1.
Each of the five steps MUST be observable as a separate entry in the
durable state journal as defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

> **Non-normative note.**
Test `P2-SF-002` validates the determinism invariant of `directive_id`
construction.
This is a critical property for replay and deduplication.
Without determinism, the same constructed directive and reserved counter could
produce different identities on different hosts, breaking the durable journal replay
guarantees defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

#### Lifecycle progression flow

| Test ID | Description |
|---------|-------------|
| `P2-SF-006` | Verify that a child transitions through the following lifecycle states in order: `pending`, `activated`, `initialized`, then `completed`, with each transition emitting the correct lifecycle event into the child's mailbox. |
| `P2-SF-007` | Verify that each lifecycle event includes the required fields defined in section 36.1 and that the `sequence_number` is monotonically incremented. |
| `P2-SF-008` | Verify that `child.lifecycle.accepted` is emitted before `child.lifecycle.activated` and that `child.lifecycle.activated` is emitted before `child.lifecycle.initialized`. |
| `P2-SF-009` | Verify that `child.lifecycle.completed` includes a valid `completion_status` and `result_summary` populated by the child's live actor. |
| `P2-SF-010` | Verify that `child.lifecycle.failed` is emitted with a valid `failure_code`, `failure_message`, and `snapshot_at_failure` when the child exits with an error. |

> **Non-normative note.**
The lifecycle ordering tests `P2-SF-006` through `P2-SF-008` validate the
state machine transitions defined by the eight lifecycle event types.
Test `P2-SF-010` exercises the failure path that is distinct from the
cancellation and termination paths.
These tests ensure that the child's live actor produces valid lifecycle
events under both success and failure conditions.

#### Monitor subscription flow

| Test ID | Description |
|---------|-------------|
| `P2-SF-011` | Create a monitor subscription for a child's lifecycle events and verify that the subscriber receives a `child.lifecycle.observed` signal for every matching event. |
| `P2-SF-012` | Create a tenant-wide monitor subscription with `target_child: null` and `event_types: all`; exercise separate children as needed and verify that the subscriber receives signals for all eight event types but does not receive operational notification signals. |
| `P2-SF-013` | Create a monitor subscription with a specific `event_types` subset and verify that the subscriber does NOT receive signals for events outside the subset. |
| `P2-SF-014` | Create a monitor subscription with `target_child: null` and verify that the subscriber receives signals for all children of the subscriber's tenant. |
| `P2-SF-015` | Delete a child and verify that the monitor subscription is automatically closed with a `subscription.closed` evidence record. |
| `P2-SF-016` | Delete the subscriber agent and verify that all active subscriptions for that subscriber are automatically closed. |
| `P2-SF-017` | Verify that a subscriber without the `observe.child.lifecycle` capability is rejected with the diagnostic `child.lifecycle.unauthorized`. |

> **Non-normative note.**
Tests `P2-SF-011` through `P2-SF-017` exercise the full monitor subscription
lifecycle defined in section 36.2.
The grant-based access control test `P2-SF-017` validates the security
invariant that observation rights do not imply modification rights,
consistent with the capability model defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

#### Cancellation flow

| Test ID | Description |
|---------|-------------|
| `P2-SF-018` | Issue a cancellation with `propagation_direction: top-down` and verify that the child acknowledges within the `deadline` and transitions to `cancelled` status. |
| `P2-SF-019` | Issue a cancellation with `propagation_direction: bottom-up` initiated by the child and verify that the parent acknowledges and the child transitions to `cancelled` status. |
| `P2-SF-020` | Issue a cancellation with `propagation_direction: bidirectional` for a subtree and verify that all children in the subtree acknowledge. |
| `P2-SF-021` | Issue a cancellation with `grant_revocation_scope: all` and verify that all child grants are revoked. |
| `P2-SF-022` | Issue a cancellation with `grant_revocation_scope: derived-only` and verify that only derived grants are revoked. |
| `P2-SF-023` | Issue a cancellation with `grant_revocation_scope: none` and verify that no grants are revoked. |
| `P2-SF-024` | Issue a cancellation with each of the eight reason codes and verify that the correct `child.lifecycle.cancelled` event is emitted. |

> **Non-normative note.**
Tests `P2-SF-018` through `P2-SF-024` exercise the full cancellation flow
defined in section 36.1.
The grant revocation scope tests `P2-SF-021` through `P2-SF-023` validate
the differential revocation behavior that reflects the principle of
least privilege as discussed in the grant revocation section.

#### Restart policy flow

| Test ID | Description |
|---------|-------------|
| `P2-SF-025` | Verify that a `never` policy child is terminated after its first non-graceful termination and is NEVER restarted by the host. |
| `P2-SF-026` | Verify that a `bounded-retry` policy child is restarted the correct number of times with the correct exponential backoff schedule. |
| `P2-SF-027` | Verify that a `bounded-retry` policy child with a non-restartable failure code is NOT restarted and transitions directly to terminal status. |
| `P2-SF-028` | Verify that a `restart-on-infrastructure-failure` policy child is restarted for infrastructure failure reasons but NOT restarted for application-level failure reasons. |
| `P2-SF-029` | Verify that an `operator-approved` policy child transitions to `suspended-pending-operator-approval` status and is restarted only after an explicit operator directive. |
| `P2-SF-030` | Verify that an `operator-approved` policy child with a valid operator restart directive is restarted and that the `restart_nonce` prevents replay. |
| `P2-SF-031` | Verify that a `bounded-retry` policy child that exhausts its restart budget transitions to `terminated-restart-exhausted` status and emits a `child.lifecycle.failed` event with reason code `restart-exhausted`. |

> **Non-normative note.**
Tests `P2-SF-025` through `P2-SF-031` exercise the full restart policy
behavior defined in section 36.2.
The nonce replay prevention test `P2-SF-030` validates the security
invariant that prevents replay attacks on operator-approved restart
directives.
The restart exhaustion test `P2-SF-031` validates the terminal condition
for `bounded-retry` children.

### Failure handling tests

> **Normative definition.**
Failure handling tests verify that the host correctly rejects invalid inputs
with stable diagnostics and without leaving unauthorized or partial state.
Each test scenario below describes the invalid input, the expected diagnostic,
and the state invariants that MUST hold after the failure.

#### Malformed input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-001` | Child-create directive with missing `artifact` field. | `child.create.malformed` |
| `P2-FH-002` | Child-create directive with `artifact` field that is not a valid digest. | `child.create.malformed` |
| `P2-FH-003` | Child-create directive with `initial_state` that is not valid JSON. | `child.create.malformed` |
| `P2-FH-003A` | Child-create directive with missing, expired, reused, incorrectly scoped, or invalidly signed `parent_consent` or `bootstrap_consent`. | `relationship.creation.unauthorized-consent` |
| `P2-FH-004` | Cancellation directive with missing `cancellation_id` field. | `child.cancellation.malformed` |
| `P2-FH-005` | Monitor subscription with `event_types` containing an unknown event type. | `child.monitor.malformed` |

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
| `P2-FH-006` | Child-create directive with `lifecycle_policy` that does not name a defined policy. | `child.create.incompatible` |
| `P2-FH-007` | Child-create directive with `manifest` digest that does not correspond to `artifact` digest. | `child.create.manifest-artifact-mismatch` |
| `P2-FH-008` | Cancellation directive with `reason` code not in the cancellation reason taxonomy. | `child.cancellation.malformed` |

> **Normative definition.**
Each incompatible input test MUST verify that the host rejects the directive
before entering the deterministic reducer and does NOT commit any state
changes to the durable journal.

> **Non-normative note.**
The incompatible input tests validate the policy and schema conformance
layer.
Without these tests, a directive that is structurally valid but semantically
incompatible could enter the reducer and produce unpredictable behavior.

#### Stale input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-009` | Child-create directive whose `owner` address resolves to a deleted or terminated agent. | `child.create.unauthorized` |
| `P2-FH-010` | Cancellation directive whose `cancelling_principal` no longer has cancellation capability for the target child. | `child.cancellation.unauthorized` |
| `P2-FH-011` | Restart directive whose `operator_address` no longer has operator approval capability. | `child.lifecycle.parent-loss.unauthorized` |

> **Normative definition.**
Each stale input test MUST verify that the host checks the current state
of the durable registry (not a cached snapshot) before admitting the
directive and rejects the directive if the principal is no longer valid.

> **Non-normative note.**
The stale input tests validate the principal resolution layer.
Without these tests, a directive issued by a principal that was valid at
the time the directive was composed but is no longer valid at the time
of evaluation could be erroneously admitted, potentially bypassing
security controls.

#### Duplicate input tests

| Test ID | Description | Expected diagnostic |
|---------|-------------|---------------------|
| `P2-FH-012` | Two child-create directives with the same `directive_id` submitted concurrently. | `child.create.duplicate-directive-id` for the second directive. |
| `P2-FH-013` | Two monitor subscription requests for the same child and event set submitted concurrently. | `child.lifecycle.subscription.conflict` for the second request. |
| `P2-FH-014` | Two cancellation directives for the same child submitted concurrently. | `child.cancellation.conflict` for the second directive. |

> **Normative definition.**
Each duplicate input test MUST verify that exactly one directive is admitted
and the other is rejected with the specified diagnostic.
The host MUST NOT admit both directives, even under high concurrency.

> **Non-normative note.**
The duplicate input tests validate the deduplication layer.
Without these tests, concurrent duplicate directives could cause the host
to create multiple live actor instances for the same child, leading to
state corruption and resource leaks.

#### Boundary-limit input tests

| Test ID | Description | Expected behavior |
|---------|-------------|-------------------|
| `P2-FH-015` | Child-create directive with `initial_state` of exactly 65536 bytes. | Directive is admitted successfully if structurally valid. |
| `P2-FH-016` | Child-create directive with `initial_state` of 65537 bytes. | Directive is rejected with `child.create.initial-state-limit`. |
| `P2-FH-017` | Monitor subscription at `maximum_active_monitor_subscriptions_per_subscriber`. | Subscription is admitted successfully. |
| `P2-FH-018` | Monitor subscription at `maximum_active_monitor_subscriptions_per_subscriber + 1`. | Subscription is rejected with `child.monitor.subscription-limit`. |
| `P2-FH-019` | `bounded-retry` policy with `max_attempts` equal to the disclosed `maximum_restart_attempts` implementation limit. | Policy is applied correctly with the maximum number of restart attempts. |
| `P2-FH-020` | Cancellation with `deadline` exactly 600 seconds after receipt. | Cancellation is admitted and the deadline is enforced. |
| `P2-FH-021` | `bounded-retry` policy with `max_attempts` equal to `maximum_restart_attempts + 1`. | Policy is rejected with `child.lifecycle.restart.limit-exceeded`. |
| `P2-FH-022` | Cancellation with `deadline` 601 seconds after receipt. | Cancellation is rejected with `child.cancellation.deadline-limit`. |
| `P2-FH-023` | Canonical child address of exactly 256 characters. | Child creation proceeds if all other fields conform. |
| `P2-FH-024` | Canonical parent, owner, or allocated child address of 257 characters. | Child creation is rejected with `child.create.address-limit`. |
| `P2-FH-025` | `directive_id` that is not exactly 64 lowercase hexadecimal characters. | Child creation is rejected with `child.create.malformed`. |
| `P2-FH-025A` | Well-formed `directive_id` that does not equal the fixed construction for the directive fields and `directive_sequence`. | Child creation is rejected with `child.create.malformed`. |
| `P2-FH-025B` | `directive_sequence: 0` or reuse of a reserved sequence for a distinct directive. | Child creation is rejected with `child.create.malformed`. |
| `P2-FH-026` | `cancellation_id` of exactly 256 canonical characters. | Cancellation proceeds if all other fields conform. |
| `P2-FH-027` | `cancellation_id` of 257 canonical characters. | Cancellation is rejected with `child.cancellation.id-limit`. |
| `P2-FH-028` | Canonical lifecycle event payload of exactly 65536 bytes. | Event is emitted if all fields conform. |
| `P2-FH-029` | Canonical lifecycle event payload of 65537 bytes. | Event-causing request is rejected with `child.lifecycle.event-payload-limit`, not `signal.oversized`. |
| `P2-FH-030` | Cancellation reason message of exactly 1024 characters. | Cancellation proceeds if all other fields conform. |
| `P2-FH-031` | Cancellation reason message of 1025 characters. | Cancellation is rejected with `child.cancellation.reason-limit`. |
| `P2-FH-032` | `failure_message` exactly at `maximum_child_failure_message_bytes`. | Message is retained without truncation diagnostic. |
| `P2-FH-033` | `failure_message` one byte over `maximum_child_failure_message_bytes`. | Message is truncated at a UTF-8 boundary and `child.lifecycle.failure-message-truncated` contains the original byte count and SHA-256 digest. |
| `P2-FH-034` | Cancellation with a deadline before receipt. | Cancellation is rejected with `child.cancellation.malformed`. |
| `P2-FH-035` | Cancellation with an unknown `propagation_direction`. | Cancellation is rejected with `child.cancellation.malformed`. |
| `P2-FH-036` | Any failure case above. | Diagnostic has exactly the Chapter 04 top-level fields, the assigned `identity.*` family, the expected domain `code`, and all required bounded `details`. |

> **Normative definition.**
Each boundary-limit input test MUST verify that the host correctly enforces
the fixed bounds and named implementation limits defined in the
"Fixed bounds and implementation limits" table of this chapter without
crashing, panicking, or entering a state not defined by this specification.

> **Non-normative note.**
The boundary-limit input tests validate the capacity planning layer.
Without these tests, an adversary could intentionally submit boundary-limit
inputs to cause resource exhaustion, denial of service, or memory corruption.
Tests MUST use the disclosed values of named implementation limits. A host MUST
NOT enforce a lower ceiling than a required floor or a different fixed ceiling
than this chapter specifies.

### Cancellation tests

> **Normative definition.**
Cancellation tests verify that the host correctly executes the cancellation
flow including scope evaluation, propagation direction, acknowledgement
handling, and hard-stop escalation.
These tests exercise the interaction between the cancellation mechanism
and the child's lifecycle state machine.

#### Cancellation scope tests

| Test ID | Description |
|---------|-------------|
| `P2-CT-001` | Issue a cancellation with `grant_revocation_scope: all` and verify that ALL grants associated with the child (both inherited and derived) are revoked. |
| `P2-CT-002` | Issue a cancellation with `grant_revocation_scope: derived-only` and verify that only grants derived by the child during execution are revoked, while inherited grants remain available to the parent. |
| `P2-CT-003` | Issue a cancellation with `grant_revocation_scope: none` and verify that NO grants are revoked. |
| `P2-CT-004` | Verify that grant revocation is recorded in the evidence log with the correct `grant_revocation_scope`, `child_address`, and `cancellation_id`. |

> **Non-normative note.**
Tests `P2-CT-001` through `P2-CT-004` validate the differential grant
revocation behavior defined in the grant revocation section.
This behavior reflects the principle of least privilege and ensures that
grant revocation is proportional to the lifecycle outcome.

#### Cancellation propagation tests

| Test ID | Description |
|---------|-------------|
| `P2-CT-005` | Issue a `top-down` cancellation from parent to child and verify that the child receives the `child.lifecycle.cancelled` event in its mailbox. |
| `P2-CT-006` | Issue a `bottom-up` cancellation from child to parent and verify that the parent receives the acknowledgement signal. |
| `P2-CT-007` | Issue a `bidirectional` cancellation for a subtree of children and verify that all children in the subtree receive the event and acknowledgements flow back to the cancelling principal. |
| `P2-CT-008` | Verify that `propagation_direction` is recorded in the evidence log and can be correlated with the `cancellation_id`. |

> **Non-normative note.**
Tests `P2-CT-005` through `P2-CT-008` validate the propagation direction
model defined in section 36.1.
The bidirectional cancellation test `P2-CT-007` exercises the subtree
cancellation semantics that are critical for system-level operations.

#### Cancellation acknowledgement tests

| Test ID | Description |
|---------|-------------|
| `P2-CT-009` | Issue a cancellation with a reasonable `deadline` and verify that the child acknowledges within the deadline and the cancellation completes gracefully. |
| `P2-CT-010` | Issue a cancellation with a `deadline` and verify that the child does NOT acknowledge within the deadline and the host escalates to termination with reason `cancellation-timeout`. |
| `P2-CT-011` | Verify that the escalation from cancellation to termination is recorded in the evidence log with the original `cancellation_id`. |
| `P2-CT-012` | Issue a cancellation with an immediate-escalation reason code (`infrastructure-failure`, `restart-exhausted`, or `system-shutdown`) and verify that the child is terminated without waiting for acknowledgement. |

> **Non-normative note.**
Tests `P2-CT-009` through `P2-CT-012` validate the acknowledgement flow
and the escalation mechanism.
The timeout test `P2-CT-010` is particularly important because it validates
that the host does not hang indefinitely waiting for an unresponsive child.
The immediate-escalation test `P2-CT-012` validates that the host correctly
distinguishes between cancellation reasons that require acknowledgement
and those that do not.

#### Hard-stop tests

| Test ID | Description |
|---------|-------------|
| `P2-CT-013` | Issue a hard stop (via escalation from cancellation timeout) and verify that the child's live actor is immediately stopped without processing additional signals. |
| `P2-CT-014` | Verify that the child's last completed durable revision is recorded as `snapshot_at_termination` and that mid-turn memory is not used for recovery. |
| `P2-CT-015` | Verify that the hard stop completes within 30 seconds. |
| `P2-CT-016` | Verify that the `child.lifecycle.terminated` event is emitted with reason `hard-stop` and that no further lifecycle events are emitted for the child after hard stop. |

> **Non-normative note.**
Tests `P2-CT-013` through `P2-CT-016` validate the hard-stop behavior
defined in section 36.1.
The bounded-time test `P2-CT-015` is critical because a hard stop that
takes too long defeats the purpose of hard stop as an immediate,
unconditional stop mechanism.
The snapshot test `P2-CT-014` validates that recovery evidence identifies the
last completed durable revision without treating volatile mid-turn state as a
recoverable snapshot.

### Restart policy tests

> **Normative definition.**
Restart policy tests verify that the host correctly enforces all four
restart policies under both normal and failure conditions.
These tests exercise the interaction between the restart policy and the
child's lifecycle state machine, including the backoff schedule, failure
code evaluation, and operator approval flow.

#### Never policy tests

| Test ID | Description |
|---------|-------------|
| `P2-RT-001` | Create a child with `lifecycle_policy: never` and verify that after a non-graceful termination, the child is NOT restarted. |
| `P2-RT-002` | Create a child with `lifecycle_policy: never` and verify that the host does NOT restart the child even when the termination reason is a transient infrastructure failure. |
| `P2-RT-003` | Verify that a `never` policy child transitions to terminal status immediately after its first non-graceful termination. |

> **Non-normative note.**
The `never` policy tests validate the most restrictive restart policy.
Test `P2-RT-002` is particularly important because it validates that the
host does NOT restart a `never` policy child even under conditions where
other policies would retry.
This confirms the immutability of the restart policy selection at child
creation time.

#### Bounded-retry policy tests

| Test ID | Description |
|---------|-------------|
| `P2-RT-004` | Create a child with `lifecycle_policy: bounded-retry`, `max_attempts: 3`, and verify that the child is restarted exactly 3 times before transitioning to `terminated-restart-exhausted` status. |
| `P2-RT-005` | Verify that the backoff delay between restart attempts follows the exponential backoff formula `delay(n) = min(initial_delay * (backoff_multiplier ** n), max_delay)`. |
| `P2-RT-006` | Create a child with `lifecycle_policy: bounded-retry` and a failure code in `restartable_failure_codes` and verify that the child IS restarted. |
| `P2-RT-007` | Create a child with `lifecycle_policy: bounded-retry` and a failure code in `non_restartable_failure_codes` and verify that the child is NOT restarted and transitions directly to terminal status. |
| `P2-RT-008` | Create a child with `lifecycle_policy: bounded-retry` and a failure code in neither list and verify that the host treats it as non-restartable and transitions the child to terminal status. |
| `P2-RT-009` | Verify that the `child.lifecycle.retrying` operational notification signal is emitted during the backoff delay period, is not assigned a lifecycle `sequence_number`, and no lifecycle events are emitted. |
| `P2-RT-010` | Create a child with `lifecycle_policy: bounded-retry` and verify that the restart policy state (attempt count, next backoff delay, remaining budget) is correctly tracked and recorded in evidence. |

> **Non-normative note.**
The `bounded-retry` policy tests are the most complex restart policy tests
because they exercise the backoff schedule, failure code evaluation, and
restart budget tracking.
Test `P2-RT-005` validates the exponential backoff computation, which is
critical for preventing retry storms and unbounded waiting.
Test `P2-RT-008` validates the default behavior for unknown failure codes,
which should be conservative (no restart) to prevent unexpected retries.

#### Infrastructure-failure policy tests

| Test ID | Description |
|---------|-------------|
| `P2-RT-011` | Create a child with `lifecycle_policy: restart-on-infrastructure-failure` and verify that the child IS restarted when the termination reason is `infrastructure-failure`. |
| `P2-RT-012` | Create a child with `lifecycle_policy: restart-on-infrastructure-failure` and verify that the child IS restarted when the termination reason is `engine-instance-crash`. |
| `P2-RT-013` | Create a child with `lifecycle_policy: restart-on-infrastructure-failure` and verify that the child IS NOT restarted when the termination reason is `policy-violation`. |
| `P2-RT-014` | Create a child with `lifecycle_policy: restart-on-infrastructure-failure` and verify that the child IS NOT restarted when the termination reason is `operator-requested`. |
| `P2-RT-015` | Verify that the restart on infrastructure failure is a single restart (not a bounded retry) and that the child transitions to terminal status after the single restart if it fails again. |

> **Non-normative note.**
The `restart-on-infrastructure-failure` policy tests validate the middle
ground between `never` and `bounded-retry`.
Test `P2-RT-015` is particularly important because it validates that the
policy performs at most one restart (not a bounded retry), which is the
key differentiator from `bounded-retry`.

#### Operator-approved policy tests

| Test ID | Description |
|---------|-------------|
| `P2-RT-016` | Create a child with `lifecycle_policy: operator-approved` and verify that after a non-graceful termination, the child transitions to `suspended-pending-operator-approval` status and is NOT restarted. |
| `P2-RT-017` | Verify that the operator receives a `child.lifecycle.pending-operator-approval` operational notification signal in their mailbox after the child transitions to suspended status and that it is not treated as a lifecycle event. |
| `P2-RT-018` | Issue a valid operator restart directive for a `operator-approved` policy child and verify that the child is restarted. |
| `P2-RT-019` | Issue an operator restart directive with a previously-used `restart_nonce` and verify that the directive is rejected with `child.lifecycle.restart.nonce-invalid`. |
| `P2-RT-020` | Verify that periodic operational reminder signals are emitted every 3600 seconds while the child is in `suspended-pending-operator-approval` status. |
| `P2-RT-021` | Verify that an operator termination directive for a `operator-approved` policy child transitions the child to terminal status without restart. |

> **Non-normative note.**
The `operator-approved` policy tests validate the human-in-the-loop
restart flow.
Test `P2-RT-019` validates the nonce-based replay prevention, which is
critical for preventing replay attacks on operator approval directives.
Test `P2-RT-020` validates the operator notification mechanism, which
must be reliable to ensure that operators are aware of children requiring
approval.

### Cross-milestone compatibility tests

> **Normative definition.**
Cross-milestone compatibility tests verify that the Phase 2 contracts do
not introduce regressions in earlier milestones.
These tests run the integration fixtures from earlier milestones with the
Phase 2 contracts active and verify that all previously-passing scenarios
continue to pass.

> **Non-normative note.**
Cross-milestone compatibility testing is essential because the Phase 2
contracts interact with many earlier milestones (see the cross-reference
summary in section 36.1).
Without these tests, a Phase 2 change that appears correct in isolation
could break the behavior of earlier milestones, leading to inconsistent
or unpredictable system behavior.

#### Affected earlier milestone fixtures

The following earlier milestone fixtures are affected by the Phase 2
contracts and MUST be re-run as part of cross-milestone compatibility
testing.

| Milestone | Fixture scope | Expected behavior |
|-----------|--------------|-------------------|
| Milestone 6 Phase 1 | Signal envelopes, causality routing, and delivery | All fixtures continue to pass; child lifecycle events are correctly routed through the signal envelope mechanism. |
| Milestone 6 Phase 1 | Actions, instructions, validation, plans, and results | All fixtures continue to pass; child-create directives are correctly validated through the actions validation flow. |
| Milestone 6 Phase 1 | State operations, patches, revisions, and conflicts | All fixtures continue to pass; child initial state is correctly managed through the state operations mechanism. |
| Milestone 6 Phase 1 | Directives, strategies, continuations, and terminal states | All fixtures continue to pass; child lifecycle terminal states are consistent with the directive terminal states. |
| Milestone 6 Phase 1 | Deterministic reducer semantics and milestone acceptance | All fixtures continue to pass; child's first turn is correctly processed by the deterministic reducer. |
| Milestone 6 Phase 1 | Extism invocation boundary instances and output validation | All fixtures continue to pass; hard stop correctly terminates Extism instances. |
| Milestone 6 Phase 1 | Mailboxes, ordering, bounds, fairness, and turn leases | All fixtures continue to pass; child lifecycle events are correctly delivered through mailboxes. |
| Milestone 6 Phase 1 | Agent registry, activation, cancellation, and completion | All fixtures continue to pass; child registry entries are consistent with the agent registry contract. |
| Milestone 6 Phase 1 | Sensors, schedules, timers, and external signal ingress | All fixtures continue to pass; operator notifications are correctly delivered through the sensor mechanism. |
| Milestone 6 Phase 1 | Single-agent host flow and milestone acceptance | All fixtures continue to pass; child lifecycle is consistent with the single-agent host flow. |
| Milestone 6 Phase 1 | Revisioned snapshots, journals, history, and storage contracts | All fixtures continue to pass; child snapshots are correctly captured and journaled. |
| Milestone 6 Phase 1 | Atomic state journal and directive-outbox commits | All fixtures continue to pass; child-create atomic commits are consistent with the journal protocol. |
| Milestone 6 Phase 1 | Effect handlers, attempts, idempotency, and result signals | All fixtures continue to pass; child lifecycle events are correctly processed as effect handlers. |
| Milestone 6 Phase 1 | Retry, timer, recovery, replay, hibernate, and migration | All fixtures continue to pass; child restart policy does not conflict with the retry mechanism. |
| Milestone 6 Phase 1 | Crash injection, durable effects, and milestone acceptance | All fixtures continue to pass; child lifecycle events are durable across crashes. |
| Milestone 5 | Threat model, principals, trust classes, and grant vocabulary | All fixtures continue to pass; child grants are consistent with the threat model. |
| Milestone 5 | Capability policy, attenuation, limits, and enforcement | All fixtures continue to pass; child grant attenuation is consistent with the capability policy. |
| Milestone 5 | Framework plugin manifests, composition, and lifecycle hooks | All fixtures continue to pass; child live actors are consistent with the framework plugin model. |
| Milestone 5 | Synchronous host functions, WASI restrictions, and tenant isolation | All fixtures continue to pass; child live actors are subject to the same WASI restrictions. |
| Milestone 5 | Provenance signing, audit, security, and milestone acceptance | All fixtures continue to pass; child lifecycle evidence is correctly signed and audited. |
| Milestone 5 | Agent identity, addressing, ownership, and dependency relations | All fixtures continue to pass; child addresses and relationships are consistent with the identity model. |

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
The table above lists 21 fixture scopes from 6 milestones that are affected
by the Phase 2 contracts.
This is consistent with the cross-reference summary in section 36.1, which
identifies 10 direct integration points with earlier chapters.
The broader fixture scope accounts for indirect effects through shared
subsystems (such as the agent registry, mailboxes, and durable journal).

### Integration test evidence requirements

> **Normative definition.**
Integration test evidence is the durable, auditable record that the Phase 2
integration tests were executed and the results.
Evidence is the primary input for promotion from `status: candidate` to
`status: normative`.

> **Normative definition.**
The following evidence items MUST be recorded for each test scenario
defined in sections 36.4.1 through 36.4.5:

| Evidence item | Content | Format |
|---------------|---------|--------|
| `test_id` | The test identifier (e.g., `P2-SF-001`). | String. |
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
A run of all Phase 2 integration tests passes if and only if:

1. Every test scenario defined in sections 36.4.1 through 36.4.5 produces
   a `result` of `pass`.
2. Every cross-milestone compatibility test defined in section 36.4.6
   produces a `result` of `pass` and no new regressions are introduced.
3. Every evidence record is complete (all required fields are present
   and non-null) and has a valid `evidence_digest`.
4. All evidence records are signed according to the provenance and audit
   mechanism defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
Promotion from `status: candidate` to `status: normative` requires:

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

### Cross-reference summary

> **Normative definition.**
The integration tests defined in this section integrate with the following
existing chapters:

1. **Test evidence and provenance**: All test evidence is recorded in the
   format defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
2. **Durable state**: Test preconditions and postconditions may interact
   with the durable state journal as defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   and
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
3. **Cross-milestone revision**: If cross-milestone compatibility tests
   fail, the affected milestones must be revised according to the protocol
   defined in
   [Specification Authority](../SPECIFICATION-AUTHORITY.md).
4. **Conformance vocabulary**: Test result classification (pass/fail/blocked)
   follows the behavior classes defined in
   [Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

> **Non-normative note.**
The four integration points above demonstrate that Phase 2 integration
testing is not an isolated activity but is deeply woven into the
specification authority, conformance, and evidence layers.
Every test evidence record is a first-class artifact in the archive,
subject to the same provenance and audit guarantees as other durable
knowledge documents.
