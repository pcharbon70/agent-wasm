---
title: "Mailboxes Ordering Bounds Fairness And Turn Leases"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
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

This chapter is a normative specification produced by
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

## 2.1 Contract And Data Model

### Mailbox entries

> **Normative definition.**
A mailbox entry is a reference to one persisted `AcceptedSignalEnvelope` with
tenant, recorded target agent, priority class, enqueue time, and deadline. It
does not copy host-owned ingress context or carry retry state.

> **Normative definition.**

```
MailboxEntry {
  accepted_delivery_id: string,
  tenant_id: TenantId,
  agent_id: AgentId,
  priority_class: PriorityClass,
  enqueue_time: UnixTimestamp,
  deadline: UnixTimestamp?
}

TenantId = string
AgentId = string

PriorityClass = "realtime" | "high" | "normal" | "low" | "background"
```

`accepted_delivery_id` MUST equal the `delivery_id` inside exactly one
persisted `AcceptedSignalEnvelope` defined by
[Signal fields](10-signals-causality-routing-and-delivery.md#signal-fields).

`UnixTimestamp` is defined in
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `accepted_delivery_id` | string | Yes | Lookup key for the immutable accepted-ingress record |
| `tenant_id` | TenantId | Yes | Tenant this entry belongs to |
| `agent_id` | AgentId | Yes | Agent this entry is for |
| `priority_class` | PriorityClass | Yes | Priority class for ordering |
| `enqueue_time` | UnixTimestamp | Yes | Time the entry was enqueued |
| `deadline` | UnixTimestamp? | No | Absolute deadline for delivery |

> **Normative definition.**
The `priority_class` field determines an entry's share of the fixed service
cycle defined below. Higher-priority classes receive a larger service share.
Within the same priority class, entries MUST be delivered in FIFO order.

> **Normative definition.**
The `deadline` field is optional.
If present, it participates in the effective deadline rule under
[Mailbox bounds](#mailbox-bounds).

### Deterministic ordering

> **Normative definition.**
The host MUST order mailbox entries deterministically within priority classes.
The ordering MUST be stable: if two entries have the same priority class and
enqueue time, they MUST be ordered by their `delivery_id` (lexicographically).
Here `delivery_id` means the entry's `accepted_delivery_id`.

> **Normative definition.**
The host MUST schedule non-empty priority classes using a repeated 31-slot
service cycle containing, in order, 16 `realtime` slots, 8 `high` slots,
4 `normal` slots, 2 `low` slots, and 1 `background` slot. A new mailbox starts
at the first slot. For each dequeue, the host scans forward cyclically, skips
empty classes, delivers the FIFO head from the first non-empty class, and
places the cursor after the slot used. Enqueueing an entry MUST NOT reset the
cursor. This schedule is the required fairness policy and MUST NOT starve a
continuously non-empty class while dequeues continue.

### Mailbox bounds

> **Normative definition.**
The host MUST enforce the following mailbox bounds:

1. **Count bound**: The maximum number of entries in the mailbox.
2. **Byte bound**: The maximum total size of all entries in the mailbox.
3. **Age bound**: The maximum age of an entry before it is rejected.
4. **Per-source bound**: The maximum number of entries from a single source.
5. **Per-tenant bound**: The maximum number of entries for a single tenant.
6. **Delivery deadline**: The maximum time an entry may remain undelivered. Entries past their deadline are rejected with `mailbox.delivery.expired`.

> **Normative definition.**

```
MailboxBounds {
  max_entries: u64,
  max_bytes: u64,
  max_age_ms: u64,
  max_entries_per_source: u64,
  max_entries_per_tenant: u64,
  delivery_deadline_ms: u64?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `max_entries` | u64 | Yes | Maximum number of entries in the mailbox |
| `max_bytes` | u64 | Yes | Maximum total size of all entries in bytes |
| `max_age_ms` | u64 | Yes | Maximum age of an entry in milliseconds |
| `max_entries_per_source` | u64 | Yes | Maximum number of entries from a single source |
| `max_entries_per_tenant` | u64 | Yes | Maximum number of entries for a single tenant |
| `delivery_deadline_ms` | u64? | No | Maximum delivery time in milliseconds. Null means no delivery deadline. |

> **Normative definition.**
The host MUST reject a new entry that would exceed a count, byte, per-source,
or per-tenant admission bound according to
[Overload behavior](#overload-behavior). It MUST reject an entry that exceeds
the age bound with `mailbox.bounds.age_exceeded`.

> **Normative definition.**
The host MUST provide configuration for the mailbox bounds.
The bounds MUST be documented in the conformance profile.

> **Normative definition.**
An entry's effective delivery deadline is the earlier of its explicit
`deadline` and `enqueue_time + delivery_deadline_ms` when both are present. If
only one is present, that value is the effective deadline; if neither is
present, the entry has no delivery deadline. At or after an effective deadline,
the host MUST reject the entry with `mailbox.delivery.expired`.

## 2.2 Behavior And Integration

### Overload behavior

> **Normative definition.**
When admitting a new entry would exceed the count, byte, per-source, or
per-tenant bound, the host MUST reject that entry without changing an existing
entry. The primary error MUST be the applicable `mailbox.bounds.*_exceeded`
code, and the host MUST also emit `mailbox.overload.rejected` identifying the
bound. Deferral, coalescing, supersession, and dead-letter admission are not
part of this mailbox contract.

> **Normative definition.**
The host MUST emit the overload diagnostic for every bound rejection. The
diagnostic MUST identify the bound and the fixed rejection disposition.

### Per-agent turn leases

> **Normative definition.**
The host MUST enforce one-at-a-time committed turns per agent using turn leases.

> **Normative definition.**

```
TurnLease {
  agent_id: AgentId,
  owner: HostInstanceId,
  revision: u64,
  issued_at: UnixTimestamp,
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
| `revision` | u64 | Yes | State revision this lease covers |
| `issued_at` | UnixTimestamp | Yes | Time this lease interval began |
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
The lease duration is `expiry - issued_at` and MUST be positive. During a
long-running turn, the host MUST renew the lease no later than the midpoint of
its current duration. Renewal sets `issued_at` to the renewal time and sets
`expiry` one unchanged lease duration later. If the lease expires without a
successful renewal, the host MUST terminate the turn with
`mailbox.turn_lease.expired`.

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

1. **Duplicate workers**: The host MUST use fencing tokens to ensure only one worker processes the agent. The worker with the highest fencing token wins. If two workers attempt to acquire a lease for the same agent simultaneously, the host MUST emit `mailbox.turn_lease.conflict` for the losing worker.

2. **Expired leases**: The host MUST terminate the turn and release the lease. The next turn request for the agent MUST acquire a new lease.

3. **Stale fencing tokens**: The host MUST reject the turn request with `mailbox.turn_lease.stale_token`. The caller MUST retry with a fresh lease.

4. **Cancellation races**: The host MUST use the cancellation token to terminate the turn. The turn MUST be rolled back if possible.

5. **Host shutdown**: The host MUST release the lease and mark the turn as failed. The next turn request for the agent MUST acquire a new lease.

## 2.3 Failure Evidence And Operational Notes

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
| Exhausted | Mailbox bounds exceeded | Count, byte, age, per-source, or per-tenant bound reached | `mailbox.bounds.count_exceeded`, `mailbox.bounds.byte_exceeded`, `mailbox.bounds.age_exceeded`, `mailbox.bounds.per_source_exceeded`, `mailbox.bounds.per_tenant_exceeded` |
| Unavailable | Mailbox or lease unavailable | Mailbox not found or lease not acquired | `mailbox.entry.unavailable` |
| DeliveryExpired | Entry delivery deadline passed | Entry not delivered before deadline | `mailbox.delivery.expired` |
| Overload | Mailbox overload | Admission bound reached | `mailbox.overload.rejected` plus the applicable `mailbox.bounds.*_exceeded` code |
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
| `mailbox.delivery` | Mailbox delivery failures | `expired` |
| `mailbox.overload` | Mailbox overload failures | `rejected` |
| `mailbox.turn_lease` | Turn lease failures | `missing`, `expired`, `stale_token`, `revoked`, `conflict` |

### Internal mechanisms and fixed behavior

> **Normative definition.**
Mailbox storage, readiness notification, and lease-renewal triggering are
internal mechanisms. Every such mechanism MUST be observationally equivalent
with respect to the 31-slot dequeue sequence, FIFO tie-breaking, bound and
deadline rejection, overload diagnostics, fencing, lease expiry, and committed
turn results. The mechanism MUST NOT introduce an overflow or dead-letter queue
at this boundary.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Mailbox persistence**: A formal mailbox persistence strategy will be implemented in future milestones. The protocol is language-neutral and does not require mailbox persistence for base conformance.

2. **Multi-tenant isolation**: Enhanced multi-tenant isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

3. **Lease recovery**: A formal lease recovery mechanism will be implemented in future milestones. The protocol is language-neutral and does not require lease recovery for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 2.4 Phase 2 Integration Tests

### Canonical successful flow

> **Normative conformance criterion.**
The canonical successful flow integration test validates that a valid mailbox
entry is processed successfully through the full mailbox and lease pipeline.

Expected behavior:

- Input: valid mailbox entry with authenticated context, priority class, and agent ID.
- Expected output: TurnResult with state_patch, directives, diagnostics, and lease release.
- Expected error: null.

### Negative: malformed entry

> **Normative conformance criterion.**
The negative malformed entry test validates that invalid mailbox entries are rejected.

Expected behavior:

- Input: mailbox entry with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `mailbox.entry.malformed`.

### Negative: incompatible signal class

> **Normative conformance criterion.**
The negative incompatible signal class test validates that incompatible signal classes are rejected.

Expected behavior:

- Input: mailbox entry with signal class that does not match the mailbox policy.
- Expected output: null.
- Expected error: `mailbox.entry.incompatible`.

### Negative: unauthorized

> **Normative conformance criterion.**
The negative unauthorized test validates that missing capabilities are rejected.

Expected behavior:

- Input: mailbox entry with missing required capability.
- Expected output: null.
- Expected error: `mailbox.entry.unauthorized`.

### Negative: count bound exceeded

> **Normative conformance criterion.**
The negative count bound exceeded test validates that count bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum count bound.
- Expected output: null.
- Expected error: `mailbox.bounds.count_exceeded`.

### Negative: byte bound exceeded

> **Normative conformance criterion.**
The negative byte bound exceeded test validates that byte bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum byte bound.
- Expected output: null.
- Expected error: `mailbox.bounds.byte_exceeded`.

### Negative: age bound exceeded

> **Normative conformance criterion.**
The negative age bound exceeded test validates that age bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum age bound.
- Expected output: null.
- Expected error: `mailbox.bounds.age_exceeded`.

### Negative: per-source bound exceeded

> **Normative conformance criterion.**
The negative per-source bound exceeded test validates that per-source bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum per-source bound.
- Expected output: null.
- Expected error: `mailbox.bounds.per_source_exceeded`.

### Negative: per-tenant bound exceeded

> **Normative conformance criterion.**
The negative per-tenant bound exceeded test validates that per-tenant bounds are enforced.

Expected behavior:

- Input: mailbox entry that exceeds the maximum per-tenant bound.
- Expected output: null.
- Expected error: `mailbox.bounds.per_tenant_exceeded`.

### Negative: missing turn lease

> **Normative conformance criterion.**
The negative missing turn lease test validates that missing turn leases are rejected.

Expected behavior:

- Input: turn request without an active turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.missing`.

### Negative: expired turn lease

> **Normative conformance criterion.**
The negative expired turn lease test validates that expired turn leases are handled correctly.

Expected behavior:

- Input: turn request with an expired turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.expired`.

### Negative: stale fencing token

> **Normative conformance criterion.**
The negative stale fencing token test validates that stale fencing tokens are rejected.

Expected behavior:

- Input: turn request with a fencing token that does not match the current lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.stale_token`.

### Negative: revoked turn lease

> **Normative conformance criterion.**
The negative revoked turn lease test validates that revoked turn leases are rejected.

Expected behavior:

- Input: turn request for an agent with a revoked turn lease.
- Expected output: null.
- Expected error: `mailbox.turn_lease.revoked`.

### Negative: delivery expired

> **Normative conformance criterion.**
The negative delivery expired test validates that entries past their deadline are rejected.

Expected behavior:

- Input: mailbox entry with deadline that has passed.
- Expected output: null.
- Expected error: `mailbox.delivery.expired`.

### Fixed scheduling, overload, and renewal

> **Normative conformance criterion.**
The Phase 2 integration tests MUST additionally verify:

1. With every priority class continuously non-empty, the first service cycle
   delivers 16 `realtime`, 8 `high`, 4 `normal`, 2 `low`, and 1 `background`
   entry in that order, preserving FIFO order within each class.
2. Each count, byte, per-source, and per-tenant overflow rejects only the new
   entry, preserves existing entries, returns the bound-specific primary error,
   and emits `mailbox.overload.rejected`.
3. A lease is renewed no later than its midpoint with an unchanged duration,
   while a missed renewal terminates the turn at expiry.
4. An entry with neither an explicit deadline nor a configured delivery
   deadline remains eligible subject to the independent age bound; an entry
   with both uses the earlier deadline.

### Cross-milestone fixture regression

> **Normative conformance criterion.**
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

The register summarizes fixed behavior, disclosed limits, and internal
mechanisms. It does not independently license variation.

| Clause | Type | Selection | Constraint |
|--------|------|-----------|------------|
| Mailbox entry structure | Required | Fields fixed by this chapter | Validate before admission |
| Priority classes | Required | `realtime`, `high`, `normal`, `low`, `background` | Closed set |
| [Cross-class scheduling](#deterministic-ordering) | Required | Fixed 16:8:4:2:1 service cycle | Preserve FIFO order within each class |
| [Mailbox bounds](#mailbox-bounds) | Implementation limits | Positive configured values disclosed in the conformance profile | Reject with the bound-specific diagnostic |
| [Overload behavior](#overload-behavior) | Required | Reject only the new entry | Emit `mailbox.overload.rejected`; do not mutate existing entries |
| [Delivery deadline](#mailbox-bounds) | Required | Earlier configured or entry deadline; none only when both are absent | Reject at or after the effective deadline |
| Turn lease structure | Required | Fields fixed by this chapter | Positive duration and fencing token validation |
| [Lease renewal](#per-agent-turn-leases) | Required | No later than the lease midpoint | Preserve duration or terminate at expiry |
| Mailbox and renewal machinery | Internal mechanism | No profile selection | Preserve all dequeue, rejection, diagnostic, and lease observations |

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
