---
title: "Atomic State Journal And Directive-Outbox Commits"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-02
  - durable-state
  - journal
  - outbox
  - commit
aliases:
  - "M4-P2 Atomic State Journal And Directive-Outbox Commits"
---

# Atomic State Journal And Directive-Outbox Commits

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-02-atomic-state-journal-and-directive-outbox-commits.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It closes the crash gap between accepting a state transition and making its
external requests durable.

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
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
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
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

## 2.1 Contract And Data Model

### Commit unit

> **Normative definition.**
A commit unit is the atomic transaction boundary that groups state, journal,
outbox, and lifecycle changes.
The host MUST write all components of a commit unit in a single transaction.
If any component fails to write, the host MUST abort the entire transaction.

> **Normative definition.**

```
CommitUnit {
  expected_revision: u64,
  next_revision: u64,
  snapshot: AgentSnapshot?,
  journal_facts: JournalEntry[],
  directive_outbox_entries: OutboxEntry[],
  lifecycle_changes: LifecycleChange[]
}

LifecycleChange {
  agent_id: AgentId,
  from_state: LifecycleState,
  to_state: LifecycleState,
  timestamp: UnixTimestamp,
  reason: String
}
```

`AgentSnapshot` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`JournalEntry` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`LifecycleState` is defined in
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `expected_revision` | u64 | Yes | The revision the host expects to see before commit |
| `next_revision` | u64 | Yes | The revision after the commit |
| `snapshot` | AgentSnapshot? | No | New snapshot or patch result (null if no state change) |
| `journal_facts` | JournalEntry[] | Yes | Journal entries for this turn |
| `directive_outbox_entries` | OutboxEntry[] | Yes | Directives to be dispatched |
| `lifecycle_changes` | LifecycleChange[] | Yes | Lifecycle state changes |

> **Normative definition.**
The `expected_revision` field is used for optimistic concurrency control.
If the current revision does not match `expected_revision`, the host MUST reject
the commit with `commit.conflict`.

> **Normative definition.**
The `next_revision` field MUST be `expected_revision + 1`.
The host MUST NOT allow `next_revision` to be less than or equal to the current
revision.

### Directive outbox entry

> **Normative definition.**
A directive outbox entry is a durable record of a directive that the host
must dispatch to its target.
The host MUST write outbox entries atomically with the state journal.

> **Normative definition.**

```
OutboxEntry {
  entry_id: EntryId,
  agent_id: AgentId,
  directive_id: DirectiveId,
  payload_hash: Bytes,
  target: DirectiveTarget,
  attempt_number: u32,
  state: OutboxState,
  created_at: UnixTimestamp,
  metadata: JsonObject
}

DirectiveId = string
DirectiveTarget {
  type: Effect | Signal | Timer | Internal,
  address: String,
  idempotency_key: String?
}

OutboxState {
  Pending,
  Leased,
  Completed,
  TerminalFailed,
  Cancelled,
  Superseded
}
```

`EntryId` and `DirectiveId` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `entry_id` | EntryId | Yes | Unique outbox entry identifier |
| `agent_id` | AgentId | Yes | Agent this outbox entry belongs to |
| `directive_id` | DirectiveId | Yes | Directive this outbox entry represents |
| `payload_hash` | Bytes | Yes | Hash of the directive payload (computed before commit) |
| `target` | DirectiveTarget | Yes | Target to dispatch to |
| `attempt_number` | u32 | Yes | Number of dispatch attempts (starts at 1) |
| `state` | OutboxState | Yes | Current outbox state |
| `created_at` | UnixTimestamp | Yes | Outbox entry creation time |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `payload_hash` field is computed from the directive payload before the
commit is written.
The host MUST NOT allow outbox entries with missing or invalid `payload_hash`.

> **Normative definition.**
The `attempt_number` field is incremented on each dispatch attempt.
The host MUST NOT allow `attempt_number` to be decremented or reset.

> **Normative definition.**
The `state` field follows the outbox state machine defined in
[Behavior And Integration](#22-behavior-and-integration).

### Directive identity and payload hash

> **Normative definition.**
The host MUST determine the directive identity and payload hash before writing
the commit unit.
The host MUST NOT write commit units with unresolved directive identities or
payload hashes.

> **Normative definition.**
The directive identity is derived from the directive type, target, and payload.
The host MUST use a deterministic function to compute the directive identity.

> **Normative definition.**
The payload hash is a hash of the directive payload (e.g., SHA-256).
The host MUST compute the payload hash before writing the commit unit.

### Compare-and-commit semantics

> **Normative definition.**
The host MUST use compare-and-commit semantics for all commit units.
The host MUST verify the `expected_revision` matches the current revision before
writing the commit unit.

> **Normative definition.**
The host MUST fence concurrent commit attempts with a monotonically advancing
revision.
If two commit attempts race, only the one with the higher revision succeeds.

> **Normative definition.**
The host MUST reject commit attempts with stale `expected_revision` with
`commit.conflict`.
The host MUST NOT silently overwrite committed data.

> **Normative definition.**
The host MUST support retry logic for transient conflicts.
The host MUST limit the number of retries to prevent infinite loops.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Hash algorithm for payload hashes | Use any cryptographically secure hash | SHA-256 or stronger | Must be constant within a deployment |
| Outbox dispatch strategy | Implementation-defined | At-least-once with idempotency | Must prevent dispatch without commit |
| Ambiguous commit resolution timeout | Implementation-defined | Document in conformance profile | Must not block agent turns indefinitely |
| Outbox entry retention | Implementation-defined | Document retention policy | Must preserve audit journal for cancelled/completed agents |
