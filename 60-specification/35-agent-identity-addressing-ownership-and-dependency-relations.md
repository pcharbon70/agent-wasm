---
title: "Agent Identity Addressing Ownership And Dependency Relations"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-06
  - phase-01
  - agent-identity
  - addressing
  - ownership
  - dependency-relations
aliases:
  - "M6-P1 Agent Identity Addressing Ownership And Dependency Relations"
---

# Agent Identity Addressing Ownership And Dependency Relations

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/phase-01-agent-identity-addressing-ownership-and-dependency-relations.md)
of
[Milestone 6](../.spec/planning/agentic-system/milestone-06-multi-agent-coordination-and-topology/README.md)
--
Multi-Agent Coordination And Topology.
It establishes the contract and data model for tenant-qualified agent addresses,
relationship types and their authority semantics, and signal provenance fields
that remain valid while live actors move, sleep, restart, or change runtime
instances.

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
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

## 6.1 Contract And Data Model

### Tenant-qualified agent addresses

> **Normative definition.**
A tenant-qualified agent address is the durable, logical identifier for an
agent that is independent of any specific process, socket, engine instance,
worker thread, or physical node on which the agent's live actors may execute.
An agent address is the stable reference point through which all inter-agent
communication, relationship resolution, and signal routing operate.

> **Normative definition.**
Agent addresses are tenant-qualified: the address space is partitioned by
tenant, and two agents in different tenants MAY share the same local name
without collision because their full addresses include the tenant component.
A tenant-qualified agent address uniquely identifies an agent within a
tenant and MUST NOT collide with any other tenant-qualified agent address
in the same tenant across the lifetime of that tenant's data.

> **Normative definition.**
An agent address is structurally composed of a tenant component and a
local component.
The tenant component identifies the tenant that owns or controls the agent.
The local component identifies the agent within that tenant's address space.
The combination is the full tenant-qualified agent address.

> **Normative definition.**

```
TenantQualifiedAgentAddress {
  tenant_id: TenantId,
  local_id: AgentLocalId
}

TenantId = string (non-empty, validated by
  [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md))

AgentLocalId = string (non-empty, unique within tenant_id,
  opaque to external consumers; format is implementation-defined)
```

> **Normative definition.**
The host MUST derive a canonical string representation of a
`TenantQualifiedAgentAddress` by concatenating the `tenant_id`, a
separator character, and the `local_id`, where the separator is an
implementation-defined character that does not appear in either component.
The canonical representation MUST be deterministic for the same address
and MUST NOT depend on the order of components (the tenant component is
always first).

> **Non-normative note.**
The separator character is typically `:` or `/`, consistent with URI-style
namespacing.
The constraint that the separator does not appear in either component
prevents ambiguity when parsing canonical representations.

> **Normative definition.**
An agent address is independent of process identity.
The same agent address MUST resolve to the agent regardless of which
process, container, or deployment unit is currently hosting the agent's
live actors.
Process identity MAY be used as a placement hint for routing, but it
MUST NOT be part of the agent address itself.

> **Normative definition.**
An agent address is independent of socket identity.
A socket (network endpoint, Unix domain socket, named pipe, or equivalent)
is a transient transport binding that MAY change between invocations,
restarts, or migrations.
An agent address MUST NOT encode or depend on any specific socket identity.
Signal routing MAY resolve an agent address to a current socket binding
at delivery time, but the address itself is stable across socket changes.

> **Normative definition.**
An agent address is independent of engine instance identity.
An engine instance is a specific instantiation of the agent runtime
host.
Agents MUST NOT be addressed through engine instance identifiers because
engine instances are ephemeral, replaceable, and may be scaled up or down
independently of agent lifecycle.

> **Normative definition.**
An agent address is independent of worker identity.
A worker is a thread, coroutine, or execution context within an engine
instance that processes a specific turn or signal.
Workers are short-lived and are not appropriate as address components.

> **Normative definition.**
An agent address is independent of physical node identity.
A physical node is a machine, container host, or cloud region in which
an engine instance runs.
Physical nodes are mutable: agents and engine instances may be migrated
across nodes for load balancing, failure recovery, or maintenance.
An agent address MUST NOT encode or depend on any physical node identity.

> **Non-normative note.**
The independence from process, socket, engine instance, worker, and physical
node is the core design property that enables agents to be addressed
durably while their runtime placement changes.
Without this property, every migration or restart would require updating
every relationship, signal route, and dependency that references the
agent, which is infeasible at scale.

> **Normative definition.**
The `local_id` component of an agent address is assigned by the host at
agent creation time and is opaque to external consumers.
External consumers MUST use the full `TenantQualifiedAgentAddress` (or
its canonical string representation) to refer to an agent.
The `local_id` alone is not a valid agent reference and MUST NOT be used
in signal headers, relationship records, or inter-agent communication.

> **Non-normative note.**
Making the `local_id` opaque prevents external agents from inferring
information about internal host topology, naming conventions, or tenant
structure.
It also allows the host to change its internal naming scheme without
breaking external contracts.

> **Normative definition.**
Agent address resolution is the process of mapping a `TenantQualifiedAgentAddress`
to the current runtime state of the corresponding agent.
Resolution returns the agent's status (active, inactive, pending, or
unknown), its current placement (engine instance, worker, socket) if any,
and any active relationship bindings.
Resolution does NOT create, modify, or terminate the agent; it is a
read-only observation of current state.

> **Normative definition.**
The agent address registry is the host-owned data structure that maps
agent addresses to their current resolution state.
The registry is the single authoritative source for agent address
resolution within a host instance.
Multiple host instances connected to a shared backend (database, service
discovery, or equivalent) MUST converge on the same resolution state for
any given agent address within a bounded time documented in the
conformance profile.

> **Normative definition.**
Agent address assignment MUST follow these rules:

1. **Uniqueness**: The host MUST NOT assign the same `local_id` to two
   agents within the same tenant.
   A duplicate assignment attempt MUST be rejected with the diagnostic
   `agent.address.duplicate-local-id`.
2. **Stability**: Once assigned, an agent's address MUST NOT change for
   the lifetime of the agent.
   If an agent is deleted and later recreated with the same logical
   identity, the new instance receives a new address.
3. **Non-guessability**: The `local_id` component MUST be generated using
   a method that prevents external actors from predicting valid addresses
   for other agents.
   UUID v4, cryptographically random identifiers, or monotonic counters
   with cryptographic obfuscation are acceptable methods.
4. **Tenant scoping**: The host MUST enforce tenant isolation on address
   assignment.
   A tenant MUST NOT be able to observe or infer the `local_id` values
   of agents in other tenants.

> **Normative definition.**

```
AgentAddressRegistry {
  entries: Map<TenantQualifiedAgentAddress, AgentRegistryEntry>,
  resolution_cache: Cache<TenantQualifiedAgentAddress, ResolutionState>
}

AgentRegistryEntry {
  address: TenantQualifiedAgentAddress,
  created_at: ISO8601,
  status: AgentStatus,
  metadata: Map<String, Value>
}

AgentStatus = "active" | "inactive" | "pending" | "deleted"

ResolutionState {
  address: TenantQualifiedAgentAddress,
  status: AgentStatus,
  placement: AgentPlacement?,
  relationships: RelationshipSnapshot,
  resolved_at: ISO8601
}

AgentPlacement {
  engine_instance_id: EngineInstanceId,
  worker_id: WorkerId?,
  socket: SocketBinding?,
  node_id: NodeId?
}

EngineInstanceId = string
WorkerId = string
SocketBinding = { protocol: String, endpoint: String }
NodeId = string
RelationshipSnapshot = Map<RelationshipId, RelationshipRecord>
```

> **Normative definition.**
The `placement` field of `ResolutionState` is optional because an agent
that is inactive, suspended, or in the process of migration may not have
a current placement.
When `placement` is absent, the agent address is still valid and
resolvable; it simply indicates that no live actor is currently
processing signals for that agent.
Signal delivery to an agent without a placement is governed by the
mailbox and delivery policies defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
and
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).

### Relationship types

> **Normative definition.**
A relationship is a directed, typed association between two agents (or
between an agent and a non-agent principal such as a user or system
service) that encodes a specific semantic role and carries defined
authority, lifecycle, and visibility semantics.
Relationships are the primary mechanism by which agents discover,
coordinate with, delegate to, and observe each other.

> **Normative definition.**
The following relationship types are defined by this specification.
Each type has a specific semantic meaning, creation rules, lifecycle
constraints, and visibility policy.

| Type | Semantic meaning | Direction | Authority model |
|------|-----------------|-----------|----------------|
| `parent` | The target agent oversees, supervises, or governs the source agent. | Source -> Target | Target has supervisory authority over source. |
| `child` | The target agent is governed by, reported to, or subordinate to the source agent. | Source -> Target | Source has governance authority over target. |
| `owner` | The target agent owns, controls, or is the primary beneficiary of the source agent's outputs. | Source -> Target | Target has ownership authority over source. |
| `member` | The source agent is a constituent part of a collective or team led by the target agent. | Source -> Target | Target has team-lead authority over source. |
| `dependency` | The source agent requires capabilities, data, or services provided by the target agent. | Source -> Target | Target has no obligation to serve; source has no entitlement. |
| `observer` | The source agent observes the state or outputs of the target agent without influencing them. | Source -> Target | Target has no obligation to support observers; source has no authority. |
| `delegate` | The source agent has delegated a specific task or authority to the target agent. | Source -> Target | Target acts on behalf of source within the delegation scope. |
| `result-recipient` | The target agent is the designated consumer of the source agent's results. | Source -> Target | Target is entitled to receive results; source is obligated to deliver. |

> **Non-normative note.**
Relationship types are intentionally asymmetric: `parent` and `child` are
distinct types, not two views of the same relationship.
This allows the host to apply different authority, visibility, and
lifecycle rules to each direction without requiring bidirectional
relationship records.

> **Non-normative note.**
The `owner` type is distinct from `parent` because ownership implies
benefit and control without necessarily implying ongoing supervision.
A parent agent is actively involved in governance; an owner agent may
be passive and only claim benefits when produced.

> **Non-normative note.**
The `delegate` type is scoped: a delegation record SHOULD include (or
reference) a description of the delegated scope, duration, and any
limitations on the delegate's authority.
This specification does not define the delegation scope schema; that is
an implementation-defined choice documented in the conformance profile.

> **Normative definition.**
Relationships are directed: a relationship from agent A to agent B with
type `child` is NOT equivalent to a relationship from agent B to agent A
with type `parent`.
Both directions SHOULD exist to represent a symmetric governance
relationship, but the host MUST NOT infer the existence of one from the
other.
Each direction is an independent relationship record with its own
lifecycle and authority semantics.

> **Normative definition.**
A self-relationship (where source and target are the same agent address)
is NOT a valid relationship and MUST be rejected at creation time with
the diagnostic `relationship.self-reference-invalid`.

> **Normative definition.**
A relationship between agents in different tenants is a cross-tenant
relationship.
Cross-tenant relationships are subject to the cross-tenant policies
defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
and
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
The host MUST validate cross-tenant relationship creation against these
policies before admitting the relationship.

> **Normative definition.**

```
RelationshipType = "parent" | "child" | "owner" | "member"
                 | "dependency" | "observer" | "delegate"
                 | "result-recipient"

RelationshipRecord {
  relationship_id: RelationshipId,
  type: RelationshipType,
  source: TenantQualifiedAgentAddress,
  target: TenantQualifiedAgentAddress,
  created_by: PrincipalId,
  created_at: ISO8601,
  status: RelationshipStatus,
  metadata: Map<String, Value>
}

RelationshipId = string (globally unique, stable for the relationship's lifetime)
PrincipalId = string (identity of the principal that created the relationship)
RelationshipStatus = "active" | "suspended" | "terminated"
```

> **Normative definition.**
Every relationship record MUST include the `relationship_id` field, which
is globally unique and stable for the relationship's lifetime.
The `relationship_id` is the primary key for relationship queries,
modifications, and deletions.
The format of `relationship_id` is implementation-defined but MUST be
opaque and non-guessable (same requirements as `AgentLocalId`).

### Relationship creation authority

> **Normative definition.**
Relationship creation authority is the permission to create a relationship
record of a given type between specific source and target agents.
Creation authority depends on the relationship type, the roles of the
source and target agents, and the creating principal's identity and
trust tier.

> **Normative definition.**
For `parent`, `child`, and `owner` relationships, the target agent MUST
explicitly consent to the relationship before it is admitted.
Consent is evidenced by the target agent's principal signing a consent
record that the host verifies before creating the relationship.
Without valid consent, the host MUST reject the relationship creation
request with the diagnostic `relationship.creation.unauthorized-consent`.

> **Normative definition.**
For `member` relationships, the target agent (acting as team lead) MUST
explicitly invite the source agent to join, OR the source agent MUST
submit a membership request that the target agent approves.
The host MUST record the invitation/approval as evidence and reject
membership creation without it.

> **Normative definition.**
For `dependency` relationships, the source agent MAY create the relationship
unilaterally to declare its dependency, but the relationship is NOT
operative (the target has no obligation to serve) until the target agent
confirms willingness to provide the dependency.
A `dependency` relationship in `active` status requires target confirmation;
in `pending` status it indicates a unilateral declaration awaiting target
response.

> **Normative definition.**
For `observer` relationships, the source agent MAY create the relationship
unilaterally, but the target agent MAY terminate observer relationships
at any time without cause.
The host MUST enforce the target's termination right and reject any
attempt by the source to prevent or delay termination.

> **Normative definition.**
For `delegate` relationships, the source agent (the delegator) MUST create
the relationship; the target agent (the delegate) does not need to consent
to creation, but the delegation scope and terms are binding on the source
and MUST be enforced by the host during execution.

> **Normative definition.**
For `result-recipient` relationships, the source agent MAY create the
relationship unilaterally to declare its intended result delivery target,
but the target agent MAY reject or ignore result delivery without
affecting the relationship's existence.

> **Non-normative note.**
The asymmetry in creation authority reflects the semantic weight of each
relationship type.
Governance and ownership relationships require mutual consent because
they confer authority over an agent.
Dependency, observer, and result-recipient relationships are declarations
by the source that do not obligate the target, so unilateral creation is
permitted (subject to the target's right to terminate or reject).
Delegation is special: the delegator unilaterally confers authority on
the delegate, so the delegate's consent is not required for creation, but
the scope of that authority is binding.

> **Normative definition.**
The creating principal MUST be authenticated and authorized at the trust
tier required by the relationship type.
The minimum trust tier for creation is:

| Relationship types | Minimum trust tier for creating principal |
|-------------------|------------------------------------------|
| `parent`, `child`, `owner` | `trusted` or higher |
| `member` | `semi-trusted` or higher |
| `dependency`, `observer`, `result-recipient` | `sandboxed` or higher |
| `delegate` | `trusted` or higher (delegator); no requirement for delegate |

> **Non-normative note.**
These trust tier requirements are minimums; hosts MAY enforce higher
tiers through local policy.
The trust tiers referenced here are defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

### Relationship lifecycle

> **Normative definition.**
Every relationship progresses through a defined lifecycle of states:

1. **Pending**: The relationship has been requested but is not yet
   operative.
   This state applies to relationships requiring consent or confirmation
   (parent, child, owner, member, dependency).
2. **Active**: The relationship is operative and enforces the authority,
   visibility, and routing semantics defined by its type.
3. **Suspended**: The relationship is temporarily inactive but preserved.
   suspended relationships do not enforce authority or routing semantics
   but are not deleted.
4. **Terminated**: The relationship is permanently concluded.
   Terminated relationships MUST NOT be reactivated; a new relationship
   record is required to re-establish the association.

> **Normative definition.**

```
Pending -> Active (on consent/confirmation)
Pending -> Terminated (on withdrawal or timeout)
Active -> Suspended (by either party, or by host policy)
Active -> Terminated (by either party, or by host policy)
Suspended -> Active (by the party that suspended, or by mutual agreement)
Suspended -> Terminated (by either party)
```

State transitions are constrained as defined above.

> **Normative definition.**
A relationship in `Pending` status that is not confirmed within a bounded
time documented in the conformance profile MUST be automatically
transitioned to `Terminated` by the host.
The transitioning principal that initiated the pending relationship (or
its successor after migration) is notified of the timeout.

> **Non-normative note.**
Automatic timeout of pending relationships prevents stale relationship
records from accumulating and confusing relationship queries.
The bounded time is implementation-defined but SHOULD be short enough
to be useful (typically seconds to minutes for consent-based transitions)
and long enough to tolerate normal network and processing latency.

> **Normative definition.**
Relationship suspension and termination are asymmetric with respect to
authority:

- For `parent`, `child`, `owner`: either party MAY suspend or terminate,
  but the host MUST log the action and notify the other party.
- For `member`: the target (team lead) MAY suspend or terminate unilaterally;
  the source MAY request termination but cannot force it (the team lead
  retains the right to keep the member).
- For `dependency`: the source MAY suspend or terminate unilaterally; the
  target has no authority to interfere.
- For `observer`: the target MAY terminate unilaterally at any time without
  cause; the source MAY suspend or terminate unilaterally.
- For `delegate`: the source (delegator) MAY terminate unilaterally at any
  time; the target MUST comply immediately.
- For `result-recipient`: the source MAY terminate or change the recipient
  unilaterally.

> **Normative definition.**
Relationship records are durable: they persist beyond the lifecycle of
any specific engine instance, worker, or process.
Relationship records are stored in the durable state layer defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
and are subject to the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
A relationship state transition is a state operation that MUST follow
the patch and revision semantics defined in
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md).

### Relationship cardinality

> **Normative definition.**
Relationship cardinality constrains the maximum number of relationships
of each type that an agent MAY have as source or target.
Cardinality limits prevent unbounded relationship growth, enforce
design intent, and bound the computational cost of relationship resolution.

> **Normative definition.**
The default cardinality limits are:

| Relationship type | Max as source | Max as target | Notes |
|-------------------|--------------|---------------|-------|
| `parent` | 1 | Unbounded | An agent has at most one parent. |
| `child` | Unbounded | 1 | An agent has at most one child-agents cluster. |
| `owner` | 1 | Unbounded | An agent has at most one owner. |
| `member` | Unbounded | 1 | An agent is a member of at most one team at a time. |
| `dependency` | Unbounded | Unbounded | No upper bound by default; hosts MAY impose local limits. |
| `observer` | Unbounded | Unbounded | No upper bound by default; hosts MAY impose local limits. |
| `delegate` | Unbounded | Unbounded | No upper bound by default; hosts MAY impose local limits. |
| `result-recipient` | 1 | Unbounded | An agent delivers results to at most one recipient. |

> **Non-normative note.**
The `parent` cardinality of 1 enforces a tree-like governance structure.
An agent has exactly one parent (or none), which prevents governance
ambiguity and simplifies escalation and accountability.
The `owner` cardinality of 1 enforces a clear line of benefit and control.
The `result-recipient` cardinality of 1 ensures that results have a
determinate delivery target.

> **Normative definition.**
Hosts MAY impose stricter cardinality limits than the defaults above
through local policy.
Hosts MAY NOT relax cardinality limits below the defaults (e.g., a host
MAY NOT allow an agent to have more than one parent if the default is 1,
because that would violate the specification).
Any host-local cardinality limits MUST be documented in the conformance
profile.

> **Normative definition.**
A relationship creation request that would violate cardinality limits
MUST be rejected with the diagnostic `relationship.cardinality-exceeded`.
The diagnostic MUST identify the relationship type, the agent, and the
current count.

### Relationship visibility

> **Normative definition.**
Relationship visibility determines which principals MAY observe a
relationship record and its metadata.
Visibility is enforced by the host at query time and is independent of
relationship creation authority.

> **Normative definition.**
The default visibility policy for relationship records is:

| Viewer | Visible fields |
|--------|---------------|
| Source agent | All fields |
| Target agent | All fields |
| Creating principal | All fields |
| Operators | All fields |
| Other agents in the same tenant | Type, source, target, status (no metadata) |
| Agents in other tenants | None (relationship is invisible) |

> **Normative definition.**
The `metadata` field of a relationship record is visible only to the
source agent, target agent, creating principal, and operators.
Metadata is the appropriate place to store scope descriptions,
delegation terms, consent records, and other sensitive details that
should not be exposed to other agents.

> **Non-normative note.**
Limiting cross-agent visibility to type, source, target, and status
enables agents to discover the topology of relationships without
exposing sensitive governance or delegation details.
The `observer` relationship type itself is a controlled mechanism for
agents that need broader visibility; they MUST still respect the
visibility policy of the relationships they observe.

> **Normative definition.**
Cross-tenant visibility: a relationship between agents in different
tenants is invisible to all principals outside both tenants.
Principals within one tenant but outside the other MAY see that a
cross-tenant relationship exists (type, source, target, status) but
MAY NOT see metadata or infer the nature of the cross-tenant association
beyond the fact of its existence.

> **Normative definition.**
Relationship visibility queries MUST be evaluated against the viewer's
access level and the relationship's cross-tenant status.
A query that would return visibility-violating data MUST be filtered
before the result is returned, OR the query MUST return an empty result
for relationships that the viewer has no visibility into.
The host MUST NOT leak information about the existence of relationships
that the viewer cannot see, even through timing or error-channel side
channels.

> **Non-normative note.**
The prohibition on information leakage through timing or error channels
is a security requirement derived from
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
Implementations MUST design their query interfaces to prevent such leaks.

### Relationship deletion behavior

> **Normative definition.**
Relationship deletion is the permanent removal of a relationship record
from the active relationship store.
Deletion is the final step in the relationship lifecycle and is only
permitted after the relationship has reached `Terminated` status.

> **Normative definition.**
A terminated relationship MAY be deleted by:

- Either the source or target agent,
- The creating principal,
- An operator.

Deletion requires the authorization of at least one of the above
principals.

> **Normative definition.**
Before deletion, the host MUST:

1. Verify that the relationship is in `Terminated` status.
2. Verify that the requesting principal has authorization to delete.
3. Archive the relationship record to the historical store defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   with a retention policy documented in the conformance profile.
4. Emit a `relationship.deleted` evidence record following the format
   defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
5. Release any resources (caches, indexes, routing entries) associated
   with the relationship.

> **Non-normative note.**
Archiving (rather than immediate permanent deletion) supports forensic
analysis, compliance audits, and dispute resolution.
The retention period for archived relationship records is
implementation-defined but SHOULD be at least as long as the retention
period for evidence records defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

> **Normative definition.**
A relationship creation request that references a relationship_id of an
already-deleted relationship MUST be rejected with the diagnostic
`relationship.id-reused-invalid`.
Relationship IDs are single-use: once a relationship is deleted, its ID
is permanently retired and MUST NOT be reassigned.

> **Normative definition.**
Relationship deletion does NOT automatically terminate dependent
relationships.
For example, deleting a `parent` relationship does not automatically
terminate `child` relationships from the perspective of other agents,
nor does it affect `dependency` or `delegate` relationships that may
have been established based on the now-deleted parent relationship.
Agents that depend on relationship topology MUST monitor for changes
and handle deletions explicitly.

> **Non-normative note.**
This design choice separates relationship lifecycle management from
topology-dependent logic.
If relationship deletion automatically terminated dependent
relationships, the system would have implicit cascading behavior that
is difficult to reason about and test.
Explicit handling by dependent agents is more transparent and controllable.

### Signal provenance fields

> **Normative definition.**
Signal provenance fields are structured metadata attached to every
signal that enables recipients to trace the signal's origin, causal
chain, and delegation path back to the originating principal.
Signal provenance fields are derived from agent addresses and
relationships, not from transport or process metadata.

> **Normative definition.**
Every signal MUST include the following provenance fields:

| Field | Content | Source |
|-------|---------|--------|
| `originating_agent` | The `TenantQualifiedAgentAddress` of the agent that originally created the signal. | Signal creation. |
| `originating_principal` | The `PrincipalId` of the principal that created the signal. | Signal creation. |
| `correlation_id` | A stable identifier that links related signals across the same logical interaction. | Signal creation or relay. |
| `causation_id` | The `relationship_id` of the relationship through which the signal was sent, or `null` if no relationship exists. | Signal routing. |
| `delegation_chain` | An ordered list of `RelationshipId` values tracing the delegation path from the originating agent to the current sender, or empty if no delegation occurred. | Signal routing. |
| `return_address` | The `TenantQualifiedAgentAddress` to which results SHOULD be delivered, or `null` if results should not be returned. | Signal creation. |

> **Normative definition.**
The `originating_agent` field is set at the moment the signal is created
by the originating agent and is NEVER modified by intermediate relays.
This field is the primary mechanism for tracing a signal back to its
true origin, regardless of how many agents, delegates, or routing
layers the signal passes through.

> **Normative definition.**
The `correlation_id` field groups signals that belong to the same
logical interaction (e.g., a single user request that generates multiple
agent-to-agent signals).
The `correlation_id` is set when the interaction begins and is inherited
by all signals generated within that interaction.

> **Normative definition.**
The `causation_id` field identifies the relationship through which the
signal was transmitted.
If a signal is sent directly between two agents without a relationship,
`causation_id` is `null`.
If a signal is sent through a `delegate` relationship, the
`causation_id` is the `relationship_id` of that delegation.

> **Normative definition.**
The `delegation_chain` field is an ordered list that traces the chain of
delegations from the originating agent to the current sender.
If the current sender is the originating agent, the list is empty.
If the signal passed through one delegation, the list has one element.
If the signal passed through multiple delegations, the list has one
element per delegation, in order from originating agent to current sender.

> **Non-normative note.**
The delegation chain enables recipients to verify that a signal was
transmitted through a valid delegation path and to detect delegation
loops or unauthorized delegation hops.
Without this field, a recipient cannot distinguish a signal that was
directly created by the claimed originating agent from one that was
relayed through an unauthorized chain.

> **Normative definition.**
The `return_address` field specifies where the recipient SHOULD deliver
results in response to this signal.
If `return_address` is `null`, the recipient MUST NOT deliver results
back to the sender (the signal is fire-and-forget from the sender's
perspective, even if the sender could theoretically receive results).
If `return_address` is present, the recipient MUST use it as the
destination for result signals, regardless of the sender's current
address or placement.

> **Normative definition.**
Signal provenance fields are immutable once set on a signal.
An intermediate relay MUST NOT modify `originating_agent`,
`originating_principal`, `correlation_id`, `causation_id`,
`delegation_chain`, or `return_address`.
A relay MAY add its own metadata (e.g., relay timestamp, relay identity)
in a separate, non-protected field, but MUST NOT alter the protected
provenance fields.

> **Normative definition.**
The host MUST validate signal provenance fields at reception time:

1. `originating_agent` MUST resolve to a known agent address in the
   registry.
   If it does not resolve, the signal MUST be rejected with the
   diagnostic `signal.provenance.originating-agent-unknown`.
2. `originating_principal` MUST be a valid, non-revoked principal
   identity.
   If it is not, the signal MUST be rejected with the diagnostic
   `signal.provenance.originating-principal-invalid`.
3. `delegation_chain` MUST form a valid chain: each delegation in the
   chain MUST be an active `delegate` relationship, and the target of
   each delegation MUST match the source of the next.
   A broken chain MUST be rejected with the diagnostic
   `signal.provenance.delegation-chain-invalid`.
4. `return_address`, if present, MUST resolve to a known agent address.
   If it does not, the signal MUST be rejected with the diagnostic
   `signal.provenance.return-address-unknown`.

> **Non-normative note.**
Provenance validation at reception prevents spoofed signals that claim
to originate from an agent or principal the sender is not authorized to
impersonate.
It also prevents signals from being delivered along invalid delegation
paths that might grant the sender authority it does not actually hold.

> **Normative definition.**
Signal provenance fields are recorded in the signal evidence logs defined
in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
and are subject to the same immutability, retention, and redaction rules.
The `originating_agent` and `originating_principal` fields are classified
as non-sensitive and are visible to all principals with signal access.
The `delegation_chain` field is classified as tenant-sensitive and is
visible only to principals within the tenant of the originating agent
and the recipient agent.

### Address-relationship coupling

> **Normative definition.**
Agent addresses and relationships are coupled: relationships reference
agent addresses, and agent address resolution returns relationship
snapshots.
This coupling enables consistent topology queries and ensures that
relationship state is always evaluated in the context of the current
agent identity and placement.

> **Normative definition.**
When an agent address is resolved, the resolution state includes a
snapshot of all active relationships in which the agent is the source
or target.
The snapshot is a point-in-time view and does NOT imply that the
relationships are stable or will persist until the next query.
Agents MUST not build long-lived state on the assumption that a
relationship observed at resolution time will still be active at
execution time.

> **Non-normative note.**
The point-in-time nature of relationship snapshots reflects the
asynchronous, distributed nature of multi-agent systems.
Relationships can be terminated between the moment of resolution and
the moment of use.
Agents that require strong consistency for relationship-dependent
operations SHOULD re-resolve immediately before the critical operation
or use the directive and effect handler protocols defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md)
and
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

> **Normative definition.**
When a relationship is created, modified, or terminated, the host MUST
invalidate any cached resolution state for the source and target agents.
Invalidation is asynchronous: the next resolution query returns the
updated state, but in-flight resolutions that completed before the
change are not retroactively updated.

> **Normative definition.**
Agent address migration (movement of an agent's live actors to a
different engine instance, worker, or node) does NOT trigger relationship
recreation or modification.
Relationships continue to reference the agent's stable address, and
address resolution returns the new placement without any change to the
relationship records.
This is the core property that makes agent addresses durable across
migration.

> **Non-normative note.**
Address migration is transparent to all relationship-dependent logic.
An agent that holds a `dependency` relationship on another agent does
not need to be notified when the target agent migrates; the host's
address resolution layer handles the routing update internally.
This transparency is what enables agents to be addressed durably while
their runtime placement changes freely.

### Cross-reference to signal envelope and causality

> **Normative definition.**
The signal provenance fields defined in this section are the address- and
relationship-layer component of the signal envelope defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
The signal envelope specification defines the complete signal structure,
delivery semantics, and causality model.
This section defines how the address and relationship layers populate
and validate the provenance fields within that envelope.
Where this section and the signal envelope specification agree, they are
mutually reinforcing.
Where they appear to conflict, the signal envelope specification takes
precedence for signal-structure questions, and this specification takes
precedence for address and relationship semantics.

> **Non-normative note.**
The separation between signal envelope (transport, delivery, causality)
and address/relationship (identity, topology, authority) is architectural.
The signal envelope is concerned with how signals move; the address/
relationship layer is concerned with who is moving them and why.
Both layers are necessary for a complete multi-agent coordination model.

## 6.2 Behavior And Integration

### Address resolution and placement projections

> **Normative definition.**
Address resolution is the observable behavior that maps a
`TenantQualifiedAgentAddress` to a `ResolutionState` produced by combining
two sources of information: (1) the durable agent registry entry that
records the agent's identity, creation time, and lifecycle status, and
(2) the current activation and placement projection that records the
engine instance, worker, socket binding, and physical node where the
agent's live actors are executing at the moment of the query.

> **Normative definition.**
The durable registry entry is the single source of truth for an agent's
identity and lifecycle status.
It is written through the durable state layer defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
and is subject to the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
The registry entry MUST persist across engine instance restarts, agent
migration, and host failure.

> **Normative definition.**
The activation and placement projection is a transient, in-memory or
cache-local view that reflects which engine instance, worker, socket, and
node are currently hosting the agent's live actors.
The projection is derived from the host's runtime scheduling and
placement logic and is updated asynchronously as agents start, stop,
migrate, or fail.
The projection is NOT durable and MUST NOT be treated as authoritative
for identity or lifecycle questions; it is purely a routing hint.

> **Non-normative note.**
The separation between durable registry state and transient placement
projection is what allows address resolution to remain correct even when
the host has no currently active placement for an agent (e.g., the agent
is inactive, suspended, or in the process of migration).
The registry tells the resolver that the agent still exists; the
projection tells the router where to send signals if the agent is live.
Both views must be combined to produce a complete `ResolutionState`.

> **Normative definition.**
Address resolution returns a `ResolutionState` that includes:

1. The agent's `status` from the durable registry entry.
2. The agent's current `placement` from the activation/placement
   projection, if any.
3. A point-in-time snapshot of the agent's active relationships,
   consistent with the relationship visibility policy defined in
   section 6.1.
4. A timestamp indicating when the resolution was computed.

The resolution operation MUST NOT create, modify, or terminate the agent.
It is a purely read-only observation of current state.

> **Non-normative note.**
Because the placement projection is asynchronous, two consecutive
resolution queries for the same agent MAY return different placement
values even though the agent's durable identity has not changed.
This is expected behavior and is consistent with the eventual
consistency model described in the conformance profile.

> **Normative implementation-defined choice.**
The mechanism by which the host combines the durable registry entry with
the activation/placement projection to produce a `ResolutionState` is
implementation-defined.
The implementation MUST document how it handles the case where the
registry entry is present but no placement is available, and how it
handles the case where the registry entry is absent but a stale
placement reference persists.

> **Normative definition.**
Address resolution for a `TenantQualifiedAgentAddress` that does not
exist in the durable registry MUST return a `ResolutionState` with
`status: "unknown"` and an absent `placement`.
The resolution MUST NOT fabricate a placement for an unknown agent,
even if the host has historical evidence of a previous agent with a
similar address.

> **Normative definition.**
Address resolution for a `TenantQualifiedAgentAddress` whose registry
entry exists but whose status is `"deleted"` MUST return a
`ResolutionState` with `status: "deleted"`.
Signal delivery to a deleted agent MUST be rejected with the diagnostic
`agent.resolution.deleted` by any component that receives the
resolution result and attempts delivery.

> **Normative definition.**
Address resolution for a `TenantQualifiedAgentAddress` whose registry
entry exists but whose status is `"pending"` MUST return a
`ResolutionState` with `status: "pending"` and an absent `placement`.
Signals delivered to a pending agent MUST be queued in the agent's
mailbox as defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
and delivered when the agent transitions to `"active"`.

### Signal provenance propagation

> **Normative definition.**
Signal provenance propagation is the set of rules that govern how the
provenance fields defined in section 6.1 are carried, preserved, and
validated as a signal traverses the multi-agent system from its
originating agent to its final recipient.
Propagation is governed by three invariants: origin preservation, chain
integrity, and return-address binding.

> **Normative definition.**
Origin preservation requires that the `originating_agent` and
`originating_principal` fields on a signal are immutable once set.
An intermediate agent that relays, delegates, or transforms a signal
MUST NOT modify these fields.
The originating agent is the agent that created the signal, not the
agent that last modified its content or the agent that is currently
forwarding it.
If a signal is received with an `originating_agent` that does not match
the agent that the signal claims to originate from, the signal MUST
be rejected with the diagnostic `signal.provenance.origin-mismatch`.

> **Non-normative note.**
Origin preservation is the primary defense against identity spoofing
and delegation abuse.
Without this invariant, any agent could claim to originate a signal
from a more authoritative agent, thereby bypassing the trust and
authority model defined by relationships.

> **Normative definition.**
Chain integrity requires that the `delegation_chain` field on a signal
is a valid, contiguous chain of active `delegate` relationship records.
Each element in the chain MUST correspond to an active delegate
relationship whose source matches the target of the preceding element
(in order from originating agent to current sender).
If the chain is empty, the current sender MUST be the originating agent.
If the chain is non-empty, each transition from one delegation to the
next MUST be through a valid relationship: the target of delegation
element N MUST be the source of delegation element N+1.

> **Normative definition.**
A broken delegation chain is a signal-level error.
If, at any point during signal processing, the recipient detects that
the `delegation_chain` does not form a valid contiguous chain of active
`delegate` relationships, the signal MUST be rejected with the
diagnostic `signal.provenance.delegation-chain-broken`.
The recipient MUST NOT process, forward, or act on a signal with a
broken delegation chain.

> **Normative definition.**
A cyclic delegation chain is a signal-level error.
If processing the `delegation_chain` reveals that the same
`RelationshipId` appears more than once, the signal MUST be rejected
with the diagnostic `signal.provenance.delegation-chain-cyclic`.
Cycles in the delegation chain indicate a misconfiguration or an
adversarial attempt to create an infinite signal relay loop.

> **Non-normative note.**
A cyclic delegation chain can arise in two scenarios: (1) an agent
A delegates to agent B, and agent B delegates back to agent A, creating
a cycle that allows an attacker to amplify signal visibility or bypass
authority checks by looping through the chain; (2) a legitimate
multi-hop delegation where the chain is incorrectly constructed with a
redundant back-edge.
Both scenarios are rejected because they are either security violations
or bugs, and neither can be distinguished from the signal alone.

> **Normative definition.**
Return-address binding requires that the `return_address` field on a
signal, if present, is honored by the recipient as the destination for
any result signals produced in response to this signal.
The recipient MUST NOT deliver results to any address other than the
`return_address`, even if the signal's current sender is at a different
address or placement.
If `return_address` is `null`, the recipient MUST NOT deliver results
back to the signal's sender or any other address.

> **Non-normative note.**
Return-address binding enables fire-and-forget signaling patterns where
the sender does not wish to receive results, and it also enables
multi-hop delegation where the original sender (at a different address
than the current sender) expects results to be returned.
Without this binding, a delegating agent that forwards a signal to a
delegate cannot control where results are delivered, which breaks the
delegation contract.

> **Normative definition.**
Correlation ID inheritance requires that all signals generated within
a single logical interaction share the same `correlation_id`.
The `correlation_id` is established at the start of the interaction
(by the initiating agent or principal) and is inherited by every
subsequent signal generated as part of that interaction.
An agent that generates multiple signals from a single incoming signal
MUST set the `correlation_id` of all derived signals to the same value
as the incoming signal.

> **Normative definition.**
Causation ID propagation requires that the `causation_id` field on a
signal records the relationship through which the signal was transmitted.
If a signal is forwarded through a `delegate` relationship, the
intermediate agent MUST update the `causation_id` to reflect the
relationship through which it is forwarding the signal.
If a signal is forwarded without any relationship (e.g., direct
delivery to an agent that is not in the sender's relationship graph),
the `causation_id` MUST be set to `null`.

> **Non-normative note.**
The distinction between `originating_agent` (immutable, set once at
creation) and `causation_id` (may change at each hop to reflect the
current transmission path) is intentional.
`originating_agent` answers "who created this?"; `causation_id` answers
"through what relationship was this last transmitted?".
Both are needed for complete provenance: one identifies the source of
intent, the other identifies the authority used to transmit.

> **Normative implementation-defined choice.**
The maximum length of the `delegation_chain` field is implementation-defined.
Implementations MUST document their maximum chain length and MUST
reject signals whose delegation chain exceeds the documented maximum
with the diagnostic `signal.provenance.delegation-chain-too-long`.
The maximum MUST be at least 128 elements and SHOULD be documented as a
bounded value in the conformance profile.

> **Non-normative note.**
A bounded delegation chain prevents unbounded signal propagation that
could lead to resource exhaustion or infinite relay loops in the event
of a misconfiguration.
The minimum of 128 elements is chosen to accommodate deep multi-agent
organizational hierarchies while remaining small enough to process
efficiently in memory.

### Relation outcome classifications

> **Normative definition.**
A relation outcome is the result returned by a relationship query or
operation when the requested relationship cannot be satisfied under the
specified conditions.
Relation outcomes are classified into the following categories:
unknown, ambiguous, moved, terminated, cross-tenant, cyclic, and
unauthorized.
Each category has a distinct diagnostic, semantic meaning, and
required handling behavior for the requesting principal.

> **Normative definition.**
The **unknown** relation outcome occurs when a relationship query
references an agent address that does not exist in the durable
registry.
The host MUST return the diagnostic `relationship.query.unknown-agent`
and the query MUST NOT return any partial or speculative data about the
unknown agent.
The requesting principal SHOULD re-resolve the agent address before
retrying the query.

> **Normative definition.**
The **ambiguous** relation outcome occurs when a relationship query
matches more than one relationship record and the query does not include
sufficient filtering criteria to disambiguate.
For example, an agent that has multiple active `dependency` relationships
with the same target agent but different relationship IDs would produce
an ambiguous result if the query does not specify which relationship
ID to retrieve.
The host MUST return the diagnostic `relationship.query.ambiguous` and
MUST include in the diagnostic the count of matching records and the
available filtering dimensions.
The requesting principal MUST refine the query with additional criteria
before retrying.

> **Non-normative note.**
Ambiguity is a query-shape error, not a data integrity error.
It indicates that the query is under-specified, not that the data is
corrupt.
The host helps the principal resolve the ambiguity by reporting the
count and available dimensions, rather than silently choosing one
result or returning all matches without explanation.

> **Normative definition.**
The **moved** relation outcome occurs when a relationship query references
a relationship record whose source or target agent has been migrated
to a different engine instance, worker, or node since the relationship
was created.
Because agent addresses are independent of placement (as defined in
section 6.1), the relationship record itself does NOT change when an
agent migrates.
The moved outcome is NOT an error: the relationship remains valid and
operative.
The moved outcome is a informational signal to the querying principal
that the agents involved in the relationship may currently be executing
on different runtime instances, which may affect latency, fault
tolerance, and delivery guarantees.
The host MUST NOT return a moved diagnostic for a relationship query
that succeeds normally.
The moved outcome is returned only when the query explicitly requests
placement information and the placement of one or both agents has
changed since the last resolution.

> **Non-normative note.**
The moved outcome is intentionally distinct from a broken or terminated
relationship.
A moved relationship is still active and valid; only the runtime
placement of one or both agents has changed.
This distinction matters because agents that depend on relationship
topology can continue to operate normally even when their targets have
migrated, as long as they handle the placement change gracefully (e.g.,
by adjusting expected latency or retry backoff).

> **Normative definition.**
The **terminated** relation outcome occurs when a relationship query
references a relationship record whose status is `terminated`.
The host MUST return the diagnostic `relationship.query.terminated`
and MUST NOT include the terminated relationship in the query result.
The requesting principal SHOULD treat a terminated relationship as if
it never existed for the purposes of authority, visibility, and routing
decisions.
A terminated relationship MAY still be present in historical archives
for audit and forensic purposes, but it MUST NOT be returned by
operational queries.

> **Normative definition.**
The **cross-tenant** relation outcome occurs when a relationship query
references a cross-tenant relationship and the requesting principal is
not a member of either tenant.
The host MUST return the diagnostic `relationship.query.cross-tenant-invisible`
and MUST NOT return any data about the cross-tenant relationship,
including its existence, type, source, target, or status.
If the requesting principal is a member of one but not the other
tenant, the host MAY return a restricted view (type, source, target,
status only, as defined in the visibility policy in section 6.1).

> **Non-normative note.**
The cross-tenant outcome enforces the tenant isolation boundary defined
in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
Cross-tenant relationships are the only relationships that can span
tenant boundaries, and they are subject to stricter visibility rules
than intra-tenant relationships.

> **Normative definition.**
The **cyclic** relation outcome occurs when a relationship operation
would create a cycle in the relationship graph.
For example, creating a `parent` relationship from agent A to agent B
would create a cycle if agent B already has a `parent` relationship
pointing to agent A (directly or through a chain of `parent`
relationships).
The host MUST reject the operation with the diagnostic
`relationship.operation.cyclic` and MUST NOT create the relationship.
The diagnostic MUST include the cycle path (the sequence of relationship
IDs that form the cycle) to enable the requesting principal to
understand and resolve the conflict.

> **Non-normative note.**
Cyclic relationships are rejected for governance and ownership types
(`parent`, `child`, `owner`) because cycles in these types create
accountability and escalation ambiguity.
For non-governance types (`dependency`, `delegate`, `observer`), cycles
are permitted but subject to the cycle-detection rules in the
delegation-chain propagation section above.

> **Normative definition.**
The **unauthorized** relation outcome occurs when a relationship
operation is attempted by a principal that lacks the required creation
authority for the requested relationship type.
The host MUST reject the operation with the diagnostic
`relationship.operation.unauthorized` and MUST NOT create, modify, or
terminate the relationship.
The diagnostic MUST identify the relationship type, the requesting
principal, and the required trust tier or consent condition.

> **Non-normative note.**
The unauthorized outcome is the primary enforcement mechanism for the
relationship creation authority model defined in section 6.1.
Without this outcome, principals could create or modify relationships
without proper authority, undermining the trust and governance model.

### Integration with existing contracts

> **Normative definition.**
Address resolution, signal provenance propagation, and relation outcome
classifications are integrated with the following existing contracts
in this specification:

1. **Signal envelopes**: The provenance fields defined in this section
   are the address-and-relationship-layer component of the signal
   envelope defined in
   [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
   Signal envelope delivery semantics govern how signals are routed
   after provenance validation succeeds.
2. **Agent registry**: Address resolution is backed by the agent
   registry defined in
   [Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).
   Registry state transitions (activation, cancellation, completion)
   update the durable entry that address resolution reads.
3. **Mailboxes**: Signal delivery to agents without current placement
   is governed by the mailbox and delivery policies defined in
   [Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
   Provenance validation occurs before signal admission to the mailbox.
4. **Threat model**: Cross-tenant relationship enforcement, trust tier
   requirements for relationship creation, and information leakage
   prevention are governed by the threat model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
5. **Capability policy**: Relationship creation authority and visibility
   enforcement are governed by the capability policy defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
6. **Provenance and audit**: Signal provenance fields are recorded in
   the evidence logs defined in
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
   Relationship lifecycle events are also recorded as evidence.

> **Non-normative note.**
This integration ensures that agent identity, addressing, ownership, and
dependency relations are not an isolated subsystem but are deeply
woven into the multi-agent coordination fabric.
Every other chapter that deals with inter-agent communication,
authority, or lifecycle interacts with this chapter's contracts in
well-defined ways.
The cross-references above are the primary integration points.

> **Normative definition.**
When this section and another section of this specification appear to
conflict on a behavior question, the following precedence rules apply:

1. For signal provenance and provenance validation: this section takes
   precedence over the signal envelope specification for questions of
   field immutability, validation rules, and origin preservation.
2. For relationship authority and lifecycle: this section takes
   precedence over the directive and effect handler specifications for
   questions of creation authority, consent requirements, and lifecycle
   transitions.
3. For address resolution: this section takes precedence over the
   mailbox and delivery specifications for questions of what state is
   returned by resolution (status, placement, relationships).
4. Where both sections are applicable and agree, they are mutually
   reinforcing.

> **Non-normative note.**
The precedence rules above are narrowly scoped: they resolve conflicts
only within the specific behavioral domains identified.
They do NOT establish blanket precedence of this section over any other
section.
For example, the signal envelope specification still governs signal
delivery semantics, fault tolerance, and retry behavior; this section
only governs how the provenance fields within those signals are
populated and validated.

## 6.3 Failure Evidence And Operational Notes

### Failure outcome taxonomy

> **Normative definition.**
A failure outcome is the structured diagnostic returned when a
contract, boundary, or invariant defined in this chapter is violated
or cannot be satisfied.
Failure outcomes are classified into six categories, each with a distinct
diagnostic prefix, semantic meaning, and required downstream handling.
The categories are: malformed, incompatible, conflicting, unauthorized,
exhausted, and unavailable.

> **Normative definition.**
The **malformed** failure outcome occurs when a request, signal,
relationship record, or address component fails structural validation
at the boundary of this chapter's contract.
Malformed inputs are rejected before any state mutation or relationship
resolution occurs.
The diagnostic prefix for malformed failures is `agent.identity.malformed`.
The diagnostic MUST identify the specific structural element that failed
validation (e.g., `agent.identity.malformed.address-invalid-tenant`,
`agent.identity.malformed.address-empty-local-id`,
`relationship.record.invalid-type`, `signal.provenance.malformed-field`).

> **Normative definition.**
The **incompatible** failure outcome occurs when a request is structurally
valid but semantically inconsistent with the state or constraints of the
system.
Incompatible inputs are not rejected as malformed because their shape is
correct; they are rejected because they cannot coexist with existing
state or with the invariants defined in this chapter.
The diagnostic prefix for incompatible failures is `agent.identity.incompatible`.
The diagnostic MUST identify the conflicting constraint and the state
that conflicts with it (e.g., `agent.identity.incompatible.address-tenant-mismatch`,
`relationship.lifecycle.incompatible-state-transition`).

> **Normative definition.**
The **conflicting** failure outcome occurs when two or more concurrent
or near-concurrent operations on the same relationship, agent address, or
address-resolution cache produce an inconsistent state that cannot be
resolved through normal conflict-resolution semantics.
Conflicting outcomes are distinct from incompatible outcomes: an
incompatible outcome is a static inconsistency with existing state,
while a conflicting outcome is a dynamic inconsistency arising from
concurrent operations.
The diagnostic prefix for conflicting failures is `agent.identity.conflict`.
The diagnostic MUST include the conflicting operation identifiers and
the conflict-resolution action taken (e.g., `agent.identity.conflict.address-assignment-latest-wins`,
`relationship.operation.conflict-rejected-second`).

> **Normative definition.**
The **unauthorized** failure outcome occurs when a principal attempts an
operation without the required creation authority, consent, or trust
tier defined in section 6.1.
Unauthorized outcomes are the primary enforcement mechanism for the
governance and authority model.
The diagnostic prefix for unauthorized failures is `agent.identity.unauthorized`.
The diagnostic MUST identify the relationship type or operation, the
requesting principal, and the required authority (e.g.,
`agent.identity.unauthorized.relationship-creation-no-consent`,
`agent.identity.unauthorized.relationship-creation-trust-tier-too-low`).

> **Normative definition.**
The **exhausted** failure outcome occurs when a system resource or limit
defined by this chapter is reached and the requested operation cannot
proceed.
Exhausted outcomes are distinct from malformed, incompatible, conflicting,
and unauthorized outcomes because they indicate a capacity or cardinality
limit rather than a correctness or authority problem.
The diagnostic prefix for exhausted failures is `agent.identity.exhausted`.
The diagnostic MUST identify the exhausted resource or limit
(e.g., `agent.identity.exhausted.cardinality-parent-limit`,
`agent.identity.exhausted.delegation-chain-max-length`,
`agent.identity.exhausted.pending-relationship-timeout`).

> **Normative definition.**
The **unavailable** failure outcome occurs when the agent, relationship,
or resolution subsystem required to complete the operation is currently
unable to serve the request due to migration, suspension, host failure,
or other transient conditions.
Unavailable outcomes are distinguished from other failure categories by
their transience: they MAY succeed on retry, whereas malformed,
incompatible, conflicting, unauthorized, and exhausted outcomes
typically require corrective action before retry is meaningful.
The diagnostic prefix for unavailable outcomes is `agent.identity.unavailable`.
The diagnostic SHOULD include the estimated or known recovery time or
action required (e.g., `agent.identity.unavailable.agent-migration-in-progress`,
`relationship.operation.unavailable-target-suspended`).

> **Non-normative note.**
The six-category taxonomy separates concerns: malformed is structural,
incompatible is semantic, conflicting is concurrent, unauthorized is
authority-based, exhausted is capacity-based, and unavailable is
transience-based.
This separation enables operators and agents to select the appropriate
recovery action for each failure type without needing to inspect
implementation-specific error codes.

### Failure outcome reference

> **Normative definition.**
The following table summarizes the six failure outcome categories and
their primary diagnostic prefixes:

| Category | Diagnostic prefix | Trigger condition | Recovery action |
|----------|------------------|-------------------|----------------|
| Malformed | `agent.identity.malformed.*` | Structural validation failure | Correct the input and retry. |
| Incompatible | `agent.identity.incompatible.*` | Semantic inconsistency with state | Revise the request to align with existing state. |
| Conflicting | `agent.identity.conflict.*` | Concurrent operation inconsistency | Retry after conflict resolution, or resolve the conflict explicitly. |
| Unauthorized | `agent.identity.unauthorized.*` | Insufficient authority or consent | Obtain the required authority, consent, or trust tier. |
| Exhausted | `agent.identity.exhausted.*` | Resource or cardinality limit reached | Reduce the scope of the request or wait for resource release. |
| Unavailable | `agent.identity.unavailable.*` | Transient inability to serve | Retry after the estimated recovery time, or take the indicated recovery action. |

> **Non-normative note.**
The recovery actions above are guidelines, not obligations.
Agents and operators SHOULD select recovery actions appropriate to the
specific diagnostic and the operational context.
The taxonomy's purpose is to make the failure mode identifiable at a
glance, not to prescribe a single recovery path.

### Bounded diagnostics

> **Normative definition.**
A bounded diagnostic is a structured failure report that identifies the
phase contract, profile, and failed boundary without exposing secrets,
internal topology, or information that violates the cross-tenant
isolation policy defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
Bounded diagnostics are the contractually observable surface through
which agents and operators learn about failure outcomes.

> **Normative definition.**
Every diagnostic emitted by this chapter's contracts MUST include:

1. The failure outcome category (malformed, incompatible, conflicting,
   unauthorized, exhausted, unavailable).
2. The diagnostic code from the category's prefix.
3. The affected agent addresses or relationship IDs (if any), subject
   to the visibility policy in section 6.1.
4. A human-readable message that describes the failure in domain terms.

> **Normative definition.**
Bounded diagnostics MUST NOT include:

1. The internal implementation of validation logic, including specific
   regex patterns, hash functions, or comparison algorithms.
2. Information about agents, relationships, or principals that the
   requesting principal has no visibility into under the policy in
   section 6.1.
3. Timing information that could be used to infer the existence or
   state of resources the principal cannot observe (timing side
   channel prevention, as required by
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)).
4. Stack traces, internal error codes, or memory addresses.
5. The internal resolution of conflicts (e.g., which of two concurrent
   operations won); the diagnostic SHOULD state that a conflict occurred
   and the adopted resolution strategy, but MUST NOT reveal the losing
   operation's identity to principals who could not observe it.

> **Non-normative note.**
The prohibition on timing side channels is derived from the threat model.
A diagnostic that takes longer to return for an unknown agent address
than for a known one leaks information about the agent's existence.
Implementations MUST design their diagnostic paths to have constant
latency with respect to observable input, or to use sampling or padding
to prevent timing-based inference.

> **Normative definition.**
Diagnostics are emitted as evidence records in the format defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).
The evidence record for a diagnostic MUST include the same fields as
the bounded diagnostic above, plus the standard provenance metadata
(originating agent, originating principal, correlation ID, timestamp).
Evidence records for diagnostics are subject to the same retention and
redaction rules as other evidence records in that chapter.

> **Normative implementation-defined choice.**
The format of the human-readable message field is implementation-defined.
Implementations MUST ensure the message is intelligible to a human
operator without requiring access to internal documentation, and MUST
not include implementation-specific jargon that would prevent an
operator from understanding the failure without additional context.

> **Normative implementation-defined choice.**
The mechanism by which diagnostics are delivered to the requesting
principal (synchronous return value, asynchronous event, log entry, or
combination) is implementation-defined.
The implementation MUST document its delivery mechanism in the
conformance profile and MUST ensure that the diagnostic is observable
by the requesting principal within a bounded time documented in the
conformance profile.

### Evidence requirements

> **Normative definition.**
Evidence for failure outcomes is the inspectable record that enables
auditors, operators, and agents to verify that failures were handled
correctly and that no unauthorized or partial state persists after a
failure.
Evidence requirements are bounded: they record what is necessary to
establish conformance, not every internal step that led to the failure.

> **Normative definition.**
The following evidence is required for each failure outcome category:

| Category | Required evidence fields |
|----------|-------------------------|
| Malformed | Diagnostic code, malformed field, structural validation rule violated. |
| Incompatible | Diagnostic code, conflicting constraint, current state that conflicts. |
| Conflicting | Diagnostic code, operation identifiers involved, resolution strategy adopted. |
| Unauthorized | Diagnostic code, requesting principal, required authority, relationship type or operation. |
| Exhausted | Diagnostic code, exhausted resource or limit, current count or usage. |
| Unavailable | Diagnostic code, affected subsystem, estimated recovery time or required action. |

> **Normative definition.**
All evidence records MUST be written through the durable state layer
defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
and MUST be subject to the atomic commit protocol defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
A failure that leaves partial state MUST not be recorded as successful
until the partial state is resolved or rolled back.

> **Non-normative note.**
The evidence requirements above are minimal.
Implementations MAY record additional evidence for operational
diagnostics, performance monitoring, or compliance requirements, but
the fields listed in the table are the minimum that MUST be recorded
to establish conformance with this specification.

> **Non-normative note.**
Evidence for unauthorized failures is particularly important for audit
and compliance.
The combination of requesting principal, required authority, and
relationship type enables auditors to reconstruct every unauthorized
attempt and verify that it was correctly rejected.

### Implementation-defined operational choices

> **Normative definition.**
The following choices are implementation-defined within this chapter.
Each choice MUST be documented in the conformance profile and MUST
not change the observable failure outcomes or diagnostic structure.

> **Normative implementation-defined choice.**
The maximum number of failure evidence records retained per agent
or per relationship is implementation-defined.
Implementations MUST retain evidence for at least as long as the
evidence retention period documented in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
and MUST document the retention period in the conformance profile.

> **Normative implementation-defined choice.**
The mechanism by which the host detects and reports conflicting
operations on the same relationship or agent address is
implementation-defined.
Implementations MUST use a conflict-resolution strategy that is
documented in the conformance profile and MUST ensure that the
conflict is resolved within a bounded time documented in the conformance
profile.
Acceptable strategies include last-writer-wins, first-writer-wins,
optimistic concurrency with retry, or application-defined resolution.

> **Normative implementation-defined choice.**
The threshold for classifying a transient unavailability as a permanent
failure (i.e., when to transition from `unavailable` to a different
failure category or to abort the operation entirely) is
implementation-defined.
Implementations MUST document the threshold and MUST not transition
from `unavailable` to a non-transient category without explicit
operator or policy intervention.

> **Normative implementation-defined choice.**
The level of detail included in the `conflicting` diagnostic's
resolution description is implementation-defined, subject to the
constraint that the description MUST not reveal the identity of
operations or principals that the requesting principal has no
visibility into (as defined in the bounded diagnostics section above).

> **Non-normative note.**
These implementation-defined choices give hosts flexibility to optimize
for their specific deployment scenarios (e.g., high-throughput
multi-tenant systems versus single-tenant embedded systems) while
keeping the observable failure contract stable.

### Deferred work

> **Non-normative note.**
The following items are deferred from this chapter.
They are identified here so that future phases or extensions can
address them without requiring changes to the contracts defined in
this chapter.
Deferred items do NOT create conformance obligations for this chapter.

> **Non-normative note.**
The cross-tenant conflict resolution protocol is deferred.
When agents in different tenants attempt concurrent operations that
affect shared infrastructure (e.g., a shared agent registry backend),
the protocol for resolving conflicts across tenant boundaries is not
defined in this chapter.
This is deferred because cross-tenant operations require the full
cross-tenant policy framework defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
and
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
to be normative before a conflict resolution protocol can be specified
safely.

> **Non-normative note.**
The distributed consensus protocol for address resolution across
multiple host instances is deferred.
This chapter defines that multiple host instances connected to a shared
backend MUST converge on the same resolution state within a bounded
time (as stated in section 6.1), but the specific consensus protocol
(paxos, raft, causal broadcast, or other) is not defined here.
This is deferred because the consensus protocol depends on the
deployment topology and failure model, which are implementation-defined
choices documented in the conformance profile.

> **Non-normative note.**
The relationship graph cycle-detection algorithm for non-governance
types (`dependency`, `delegate`, `observer`) is not fully specified.
This chapter defines that cycles in governance types (`parent`,
`child`, `owner`) are rejected (see section 6.2), but does not define
the specific algorithm for detecting cycles in non-governance types
beyond the signal-level delegation-chain cycle detection.
This is deferred because the cycle-detection requirements for
non-governance types depend on the cardinality and operational semantics
of those types, which are implementation-defined.

> **Non-normative note.**
The evidence correlation protocol for multi-step failures (e.g., a
malformed signal that triggers an unauthorized relationship operation
attempt) is deferred.
This chapter records evidence for each failure outcome independently
but does not define how correlated evidence records should be linked
for audit and forensic analysis.
This is deferred because the correlation protocol depends on the
evidence storage and query infrastructure, which is defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
and is not yet normative.

> **Non-normative note.**
The operational dashboard and alerting schema for failure outcomes is
deferred.
This chapter defines the failure outcomes and diagnostics but does not
define the schema for operational dashboards, alerting rules, or
SLO/SLA definitions based on failure rates.
This is deferred because operational concerns are outside the scope
of this specification chapter and belong in a separate operations
guide or conformance profile supplement.

### Results that could invalidate earlier milestones

> **Non-normative note.**
The following results from this phase, if realized, would invalidate
assumptions made in earlier milestones.
These are identified here so that reviewers can assess whether the
assumptions are valid and, if not, update the earlier milestones before
this phase is promoted to normative.

> **Non-normative note.**
The tenant-qualified agent address model assumes that a single durable
identity can outlive any number of runtime instance changes.
If integration tests reveal that address resolution cannot converge
across host instances within the bounded time documented in the
conformance profile, then the address stability assumption in
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
(through
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md))
would need revision.
Specifically, Milestones 1 through 5 assume that an agent's address is
stable enough to be used as a foreign key in signals, directives,
state patches, and relationship records.
If addresses are not stable, those foreign keys would need to be
replaced with indirection layers, which would affect every chapter
that references agent addresses.

> **Non-normative note.**
The relationship authority model assumes that relationship records are
the sole source of authority for inter-agent operations.
If integration tests reveal that authority can be bypassed through
signal provenance manipulation despite the validation rules in this
chapter, then the authority assumptions in
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
and
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
would need revision.
Specifically, those milestones assume that the signal provenance and
relationship layers, taken together, provide a complete authority
model.
If the provenance validation in this chapter has gaps that allow
authority bypass, the authority model in those milestones is
incomplete.

> **Non-normative note.**
The cross-tenant relationship invisibility assumption assumes that
cross-tenant relationships are fully invisible to principals outside
both tenants.
If integration tests reveal that cross-tenant relationships can be
inferred through side channels (timing, error messages, or resource
usage patterns), then the tenant isolation assumptions in
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
(through
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md))
would need revision.
Specifically, those milestones assume tenant isolation at the
infrastructure level; if the relationship layer leaks cross-tenant
information, the isolation guarantee is weakened.

> **Non-normative note.**
The bounded delegation chain assumption assumes that delegation chains
are bounded in length (maximum 128 elements, as stated in section 6.2).
If integration tests reveal that delegation chains longer than 128
elements are required for legitimate operational patterns, or that
the 128-element limit causes legitimate operations to fail, then the
delegation chain length limit and the related assumptions in
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
would need revision.
Specifically, that milestone assumes that delegation chains are short
enough to be processed efficiently in memory during signal routing.
If chains must be longer, the routing performance model needs
recalibration.

> **Non-normative note.**
The pending relationship timeout assumption assumes that a bounded
timeout (currently documented as 60 seconds by default) is sufficient
for consent-based relationship transitions.
If integration tests reveal that legitimate consent workflows require
longer timeouts (e.g., due to human-in-the-loop approval steps or
slow cross-tenant policy evaluation), then the timeout and the related
assumptions in
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
(regarding relationship lifecycle) would need revision.
Specifically, that milestone assumes that relationship state
transitions complete within bounded time; if consent workflows are
inherently unbounded (e.g., awaiting human approval that may never come),
the lifecycle model needs a new state or a different timeout strategy.

## Variability register

The following table enumerates every implementation-defined choice,
MAY permission, permitted variation, and limit defined in this section.
Each entry references the rule or definition it modifies and states the
required documentation obligation.

| ID | Rule / Definition reference | Variability | Required documentation | Default |
|----|---------------------------|-------------|----------------------|---------|
| V-6.1-01 | Canonical address representation (separator character) | The separator character used to concatenate `tenant_id` and `local_id` in the canonical string representation of `TenantQualifiedAgentAddress`. | Conformance profile. | `:` |
| V-6.1-02 | `local_id` generation method | The method used to generate `local_id` values (UUID v4, cryptographic random, monotonic counter with obfuscation, or other). | Conformance profile. | UUID v4 |
| V-6.1-03 | Pending relationship timeout | The bounded time after which a pending relationship is automatically terminated. | Conformance profile. | 60 seconds |
| V-6.1-04 | Stricter cardinality limits | Host-local cardinality limits that are stricter than the defaults in the cardinality table. | Conformance profile. | None (use defaults) |
| V-6.1-05 | Delegation scope schema | The schema used to describe delegation scope, duration, and limitations in `delegate` relationship metadata. | Conformance profile. | Implementation-defined |
| V-6.1-06 | Archived relationship retention | The retention period for archived (deleted) relationship records. | Conformance profile. | Same as evidence retention |
| V-6.1-07 | Cross-tenant relationship policy | The specific cross-tenant policies applied to relationship creation, visibility, and resolution. | Conformance profile; must reference
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
and
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md). | Deny by default |
| V-6.1-08 | Relationship snapshot consistency model | Whether resolution returns a strong-consistency snapshot or a eventually-consistent snapshot of relationship state. | Conformance profile. | Strong consistency |
| V-6.1-09 | Resolution cache invalidation mechanism | The mechanism used to invalidate resolution cache entries on relationship state changes (immediate, event-driven, TTL-based, or hybrid). | Conformance profile. | Event-driven |
| V-6.1-10 | Signal provenance validation strictness | Whether provenance validation at reception is hard-fail (reject signal) or soft-fail (log warning, allow signal). | Conformance profile. | Hard-fail |
| V-6.2-01 | Address resolution combination mechanism | How the host combines the durable registry entry with the activation/placement projection to produce a `ResolutionState`, including handling of missing placement and stale references. | Conformance profile. | Registry-first with placement overlay |
| V-6.2-02 | Maximum delegation chain length | The maximum number of elements permitted in the `delegation_chain` field before the signal is rejected. | Conformance profile. | 128 |
| V-6.2-03 | Moved outcome delivery mechanism | How the host signals that an agent's placement has changed since the last resolution (informational diagnostic, explicit placement field, or separate notification). | Conformance profile. | Informational diagnostic on placement-request |
