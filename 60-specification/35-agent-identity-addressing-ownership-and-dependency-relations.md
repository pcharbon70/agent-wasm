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
