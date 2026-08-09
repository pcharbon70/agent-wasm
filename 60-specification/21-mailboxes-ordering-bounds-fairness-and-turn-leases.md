---
title: "Mailboxes Ordering Bounds Fairness And Turn Leases"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-03
  - phase-02
  - mailbox
  - ordering
  - fairness
  - turn-lease
aliases:
  - "M3-P2 Mailboxes And Turn Leases"
---

# Mailboxes Ordering Bounds Fairness And Turn Leases

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/phase-02-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
of
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
--
Host Actor Runtime And Lifecycle.
It provides one-at-a-time committed turns per agent while bounding queued work
and making overload behavior explicit.

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
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

## 3.1 Contract And Data Model

### Mailbox entries

> **Normative definition.**
A mailbox entry is an authenticated signal reference with tenant, agent,
priority class, enqueue time, deadline, and delivery metadata.

> **Normative definition.**

```
MailboxEntry {
  signal: SignalEnvelope,
  tenant_id: TenantId,
  agent_id: AgentId,
  priority_class: PriorityClass,
  enqueue_time: UnixTimestamp,
  deadline: UnixTimestamp?,
  delivery_metadata: DeliveryMetadata
}

TenantId = string
AgentId = string

PriorityClass = "realtime" | "high" | "normal" | "low" | "background"

DeliveryMetadata {
  attempt_count: u64,
  last_attempt_at: UnixTimestamp?,
  next_attempt_at: UnixTimestamp?,
  backoff_ms: u64
}
```

`SignalEnvelope` is defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md#signal-fields).

`UnixTimestamp` is defined in
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `signal` | SignalEnvelope | Yes | The signal to deliver |
| `tenant_id` | TenantId | Yes | Tenant this entry belongs to |
| `agent_id` | AgentId | Yes | Agent this entry is for |
| `priority_class` | PriorityClass | Yes | Priority class for ordering |
| `enqueue_time` | UnixTimestamp | Yes | Time the entry was enqueued |
| `deadline` | UnixTimestamp? | No | Absolute deadline for delivery |
| `delivery_metadata` | DeliveryMetadata | Yes | Delivery attempt metadata |

> **Normative definition.**
The `priority_class` field determines the ordering within the mailbox.
Entries with higher priority MUST be delivered before entries with lower priority.
Within the same priority class, entries MUST be delivered in FIFO order.

> **Normative definition.**
The `deadline` field is optional.
If present, the host MUST reject entries that have not been delivered by the deadline
with `mailbox.delivery.expired`.

### Deterministic ordering

> **Normative definition.**
The host MUST order mailbox entries deterministically within priority classes.
The ordering MUST be stable: if two entries have the same priority class and
enqueue time, they MUST be ordered by their `delivery_id` (lexicographically).

> **Normative definition.**
The host MUST provide explicit fairness between priority classes.
The host MUST NOT starve lower-priority entries indefinitely.

> **Normative definition.**
The host MAY implement fairness using the following policies:

1. **Strict priority**: Higher-priority entries are always delivered before lower-priority entries. Lower-priority entries may be starved.

2. **Weighted fair queuing**: Each priority class receives a weighted share of delivery capacity. The weights MUST be documented in the conformance profile.

3. **Round-robin with priority**: Entries are delivered in round-robin fashion, but higher-priority classes are visited more frequently. The frequency MUST be documented in the conformance profile.

> **Normative definition.**
The host MUST document the chosen fairness policy in the conformance profile.

### Mailbox bounds

> **Normative definition.**
The host MUST enforce the following mailbox bounds:

1. **Count bound**: The maximum number of entries in the mailbox.
2. **Byte bound**: The maximum total size of all entries in the mailbox.
3. **Age bound**: The maximum age of an entry before it is rejected.
4. **Per-source bound**: The maximum number of entries from a single source.
5. **Per-tenant bound**: The maximum number of entries for a single tenant.

> **Normative definition.**

```
MailboxBounds {
  max_entries: u64,
  max_bytes: u64,
  max_age_ms: u64,
  max_entries_per_source: u64,
  max_entries_per_tenant: u64
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `max_entries` | u64 | Yes | Maximum number of entries in the mailbox |
| `max_bytes` | u64 | Yes | Maximum total size of all entries in bytes |
| `max_age_ms` | u64 | Yes | Maximum age of an entry in milliseconds |
| `max_entries_per_source` | u64 | Yes | Maximum number of entries from a single source |
| `max_entries_per_tenant` | u64 | Yes | Maximum number of entries for a single tenant |

> **Normative definition.**
The host MUST reject new entries when any bound is reached, according to the
overload policy defined in section 3.2.

> **Normative definition.**
The host MUST provide configuration for the mailbox bounds.
The bounds MUST be documented in the conformance profile.

## 3.2 Behavior And Integration

### Overload behavior

> **Normative definition.**
When a mailbox bound is reached, the host MUST apply the following behavior
by signal class:

1. **Reject**: Reject the new entry immediately with `mailbox.overload.rejected`.
2. **Defer**: Queue the new entry in a separate overflow queue with `mailbox.overload.deferred`.
3. **Coalesce**: Merge the new entry with an existing entry of the same type and source with `mailbox.overload.coalesced`.
4. **Supersede**: Replace an existing entry of the same type and source with the new entry with `mailbox.overload.superseded`.
5. **Dead-letter**: Move the new entry to a dead-letter queue with `mailbox.overload.dead_lettered`.

> **Normative definition.**
The host MUST document the overload policy for each signal class in the
conformance profile.

> **Normative definition.**
The host MUST emit a diagnostic when any overload action is taken.
The diagnostic MUST identify the bound that was reached and the action taken.

### Per-agent turn leases

> **Normative definition.**
The host MUST enforce one-at-a-time committed turns per agent using turn leases.

> **Normative definition.**

```
TurnLease {
  agent_id: AgentId,
  owner: HostInstanceId,
  revision: int,
  expiry: UnixTimestamp,
  fencing_token: u64,
  status: LeaseStatus
}

HostInstanceId = string

LeaseStatus {
  Active,
  Expired,
  Revoked
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `agent_id` | AgentId | Yes | Agent this lease is for |
| `owner` | HostInstanceId | Yes | Host instance that owns the lease |
| `revision` | int | Yes | State revision this lease covers |
| `expiry` | UnixTimestamp | Yes | Absolute expiry time for the lease |
| `fencing_token` | u64 | Yes | Fencing token for lease validation |
| `status` | LeaseStatus | Yes | Current lease status |

> **Normative definition.**
The host MUST acquire a turn lease before invoking the reducer for an agent.
The host MUST release the turn lease after the reducer completes, whether successfully
or with a trap.

> **Normative definition.**
The host MUST reject turn requests when no active lease exists for the agent.
The host MUST reject with `mailbox.turn_lease.missing`.

> **Normative definition.**
The host MUST validate the fencing token before processing a turn request.
If the fencing token does not match the current lease, the host MUST reject
with `mailbox.turn_lease.stale_token`.

> **Normative definition.**
The host MUST renew the turn lease periodically during long-running turns.
If the lease expires and is not renewed, the host MUST terminate the turn
with `mailbox.turn_lease.expired`.

> **Normative definition.**
The host MUST revoke the turn lease when the agent is cancelled or completed.
The host MUST reject subsequent turn requests for the revoked agent with
`mailbox.turn_lease.revoked`.

### Failure outcomes

> **Normative definition.**
The following failure outcomes are relevant to mailboxes, ordering, bounds,
fairness, and turn leases:

1. **Duplicate workers**: Multiple host instances attempt to process the same agent.
2. **Expired leases**: A turn lease expires before the turn completes.
3. **Stale fencing tokens**: A turn request uses an outdated fencing token.
4. **Cancellation races**: A cancellation occurs while a turn is in progress.
5. **Host shutdown**: A host instance shuts down while processing a turn.

> **Normative definition.**
The host MUST handle each failure outcome as follows:

1. **Duplicate workers**: The host MUST use fencing tokens to ensure only one worker processes the agent. The worker with the highest fencing token wins.

2. **Expired leases**: The host MUST terminate the turn and release the lease. The next turn request for the agent MUST acquire a new lease.

3. **Stale fencing tokens**: The host MUST reject the turn request with `mailbox.turn_lease.stale_token`. The caller MUST retry with a fresh lease.

4. **Cancellation races**: The host MUST use the cancellation token to terminate the turn. The turn MUST be rolled back if possible.

5. **Host shutdown**: The host MUST release the lease and mark the turn as failed. The next turn request for the agent MUST acquire a new lease.

## 3.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to mailboxes, ordering, bounds,
fairness, and turn leases:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid mailbox entry structure | Failed JSON parsing or schema validation | `mailbox.entry.malformed` |
| Incompatible | Mailbox policy incompatible with signal | Priority class or signal class mismatch | `mailbox.entry.incompatible` |
| Conflicting | Concurrent turns on same agent | Same agent targeted with multiple leases | `mailbox.turn_lease.conflict` |
| Unauthorized | Missing capability for mailbox operation | Required capability not granted | `mailbox.entry.unauthorized` |
| Exhausted | Mailbox bounds exceeded | Count, byte, age, per-source, or per-tenant bound reached | `mailbox.bounds.exhausted` |
| Unavailable | Mailbox or lease unavailable | Mailbox not found or lease not acquired | `mailbox.entry.unavailable` |
| Overload | Mailbox overload | Bound reached, overload policy triggered | `mailbox.overload.*` |
| LeaseExpired | Turn lease expired | Lease expiry time passed without renewal | `mailbox.turn_lease.expired` |
| StaleToken | Stale fencing token | Fencing token does not match current lease | `mailbox.turn_lease.stale_token` |
| LeaseRevoked | Turn lease revoked | Lease revoked due to cancellation or completion | `mailbox.turn_lease.revoked` |

> **Normative definition.**
All failure modes MUST produce a diagnostic and terminate the turn without
partial state changes.
The host MUST NOT expose implementation details in diagnostics.

### Diagnostics

> **Normative definition.**
All diagnostics emitted by the host MUST conform to the `Diagnostic` type
defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics).

Diagnostics MUST identify the phase contract, profile, and failed boundary
without exposing secrets or implementation internal state.

### Diagnostic families

| Family | Purpose | Example codes |
|--------|---------|---------------|
| `mailbox.entry` | Mailbox entry failures | `malformed`, `incompatible`, `unauthorized`, `unavailable` |
| `mailbox.bounds` | Mailbox bound failures | `count_exceeded`, `byte_exceeded`, `age_exceeded`, `per_source_exceeded`, `per_tenant_exceeded` |
| `mailbox.overload` | Mailbox overload failures | `rejected`, `deferred`, `coalesced`, `superseded`, `dead_lettered` |
| `mailbox.turn_lease` | Turn lease failures | `missing`, `expired`, `stale_token`, `revoked`, `conflict` |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Fairness policy**: The host MAY choose the fairness policy between priority classes. The policy MUST be documented in the conformance profile.

2. **Overload policy**: The host MAY choose the overload policy for each signal class. The policy MUST be documented in the conformance profile.

3. **Lease renewal interval**: The host MAY choose how frequently to renew turn leases. The interval MUST be documented in the conformance profile.

4. **Dead-letter retention**: The host MAY choose how long to retain dead-lettered entries. The retention period MUST be documented in the conformance profile.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Mailbox persistence**: A formal mailbox persistence strategy will be implemented in future milestones. The protocol is language-neutral and does not require mailbox persistence for base conformance.

2. **Multi-tenant isolation**: Enhanced multi-tenant isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

3. **Lease recovery**: A formal lease recovery mechanism will be implemented in future milestones. The protocol is language-neutral and does not require lease recovery for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 3.4 Phase 2 Integration Tests

### Canonical successful flow

> **Normative definition.**
The canonical successful flow integration test validates that a valid mailbox
entry is processed successfully through the full mailbox and lease pipeline.

Expected behavior:

- Input: valid mailbox entry with authenticated context, priority class, and agent ID.
- Expected output: TurnResult with state_patch, directives, diagnostics, and lease release.
- Expected error: null.

### Negative: malformed entry

> **Normative definition.**
The negative malformed entry test validates that invalid mailbox entries are rejected.

Expected behavior:

- Input: mailbox entry with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `mailbox.entry.malformed`.

### Negative: incompatible signal class

> **Normative definition.**
The negative incompatible signal class test validates that incompatible signal classes are rejected.

Expected behavior:

- Input: mailbox entry with signal class that does not match the mailbox policy.
- Expected output: null.
- Expected error: `mailbox.entry.incompatible`.

### Negative: unauthorized

> **Normative definition.**
The negative unauthorized test validates that missing capabilities are rejected.

Expected behavior:

- Input: mailbox entry with missing required capability.
- Expected output: null.
- Expected error: `mailbox.entry.unauthorized`.

### Negative: count bound exceeded

> **Normative definition.**
The negative count bound exceeded test validates that count bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum count bound.
- Expected output: null.
- Expected error: `mailbox.bounds.count_exceeded`.

### Negative: byte bound exceeded

> **Normative definition.**
The negative byte bound exceeded test validates that byte bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum byte bound.
- Expected output: null.
- Expected error: `mailbox.bounds.byte_exceeded`.

### Negative: age bound exceeded

> **Normative definition.**
The negative age bound exceeded test validates that age bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum age bound.
- Expected output: null.
- Expected error: `mailbox.bounds.age_exceeded`.

### Negative: per-source bound exceeded

> **Normative definition.**
The negative per-source bound exceeded test validates that per-source bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum per-source bound.
- Expected output: null.
- Expected error: `mailbox.bounds.per_source_exceeded`.

### Negative: per-tenant bound exceeded

> **Normative definition.**
The negative per-tenant bound exceeded test validates that per-tenant bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum per-tenant bound.
- Expected output: null.
- Expected error: `mailbox.bounds.per_tenant_exceeded`.

### Negative: missing turn lease

> **Normative definition.**
The negative missing turn lease test validates that missing turn leases are rejected.

Expected behavior:

- Input: turn request without an active turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.missing`.

### Negative: expired turn lease

> **Normative definition.**
The negative expired turn lease test validates that expired turn leases are handled correctly.

Expected behavior:

- Input: turn request with an expired turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.expired`.

### Negative: stale fencing token

> **Normative definition.**
The negative stale fencing token test validates that stale fencing tokens are rejected.

Expected behavior:

- Input: turn request with a fencing token that does not match the current lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.stale_token`.

### Negative: revoked turn lease

> **Normative definition.**
The negative revoked turn lease test validates that revoked turn leases are rejected.

Expected behavior:

- Input: turn request for an agent with a revoked turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.revoked`.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 2 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Phase 3 fixtures: PASS.
- All Phase 4 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.
- All Milestone 2 Phase 3 fixtures: PASS.
- All Milestone 2 Phase 4 fixtures: PASS.
- All Milestone 2 Phase 5 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 3 exit report.

## Variability register

| Clause | Type | Selection |
|--------|------|-----------|
| Mailbox entry structure | Required | Fields fixed by this chapter |
| Priority classes | Required | realtime, high, normal, low, background, fixed by this chapter |
| Deterministic ordering | Required | Stable FIFO within priority class, fixed by this chapter |
| Mailbox bounds | Required | Count, byte, age, per-source, per-tenant, fixed by this chapter |
| Turn lease structure | Required | Fields fixed by this chapter |
| Fairness policy | Implementation-defined | Documented in conformance profile |
| Overload policy | Implementation-defined | Documented in conformance profile |
| Lease renewal interval | Implementation-defined | Documented in conformance profile |
| Dead-letter retention | Implementation-defined | Documented in conformance profile |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The mailbox provides:

- One-at-a-time committed turns per agent.
- Deterministic ordering within priority classes.
- Explicit fairness between priority classes.
- Bounded queued work with clear overload behavior.

The turn lease provides:

- Exclusive access to an agent for one turn at a time.
- Fencing tokens for lease validation.
- Clear failure handling for expired, stale, and revoked leases.

The failure modes provide:

- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.
- Evidence that failures are handled correctly.

The integration tests provide:

- Verification that the canonical flow works end-to-end.
- Evidence that all failure modes are handled correctly.
- Foundation for cross-implementation conformance testing.
