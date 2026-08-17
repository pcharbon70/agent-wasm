---
title: "Signal Envelopes Causality Routing And Delivery Vocabulary"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-02
  - phase-01
  - signal
  - causality
  - routing
  - delivery
aliases:
  - "M2-P1 Signal Envelopes"
---

# Signal Envelopes Causality Routing And Delivery Vocabulary

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/phase-01-signal-envelopes-causality-routing-and-delivery-vocabulary.md)
of
[Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/README.md)
--
Signals, Actions, State, And Strategies.
It defines the event fabric through which users, effects, timers, sensors,
and agents enter deterministic turns.

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
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

## Signal fields

> **Normative definition.**
A signal is an immutable event that enters an agent turn.
The sender supplies signal content; the host authenticates ingress metadata,
selects one target, and persists one accepted-ingress record before invoking a
guest.

> **Normative definition.**
`SignalEnvelope` is exclusively the guest-wire type defined by
[Signal envelope](04-turn-lifecycle-protocols-and-canonical-encoding.md#signal-envelope).
This chapter does not extend that type. It defines the sender submission and a
host-owned wrapper that maps to the existing `TurnRequest` fields.

> **Normative definition.**

```
SignalSubmission {
  type: string,
  source: string,
  subject: string,
  correlation_id: string,
  causation_id: string?,
  timestamp: ISO 8601 UTC,
  data: JsonObject?
}

AcceptedSignalEnvelope {
  signal: SignalEnvelope,
  tenant_id: string,
  principal_id: string?,
  trace_context: TraceContext,
  received_at: ISO 8601 UTC,
  route_id: string,
  target_agent_type: string,
  target_instance_id: string
}
```

| Field | Type | Required | Source | Purpose |
|-------|------|----------|--------|---------|
| `SignalSubmission.*` | fields above | Yes except nullable fields | Sender | Immutable event content |
| `signal` | SignalEnvelope | Yes | Host | Exact guest-wire projection, including derived `delivery_id` |
| `tenant_id` | string | Yes | Host | Multi-tenant isolation |
| `principal_id` | string? | No | Host | Calling principal for authorization |
| `trace_context` | TraceContext | Yes | Host | Distributed tracing metadata |
| `received_at` | ISO 8601 UTC | Yes | Host | Immutable timestamp used for TTL evaluation |
| `route_id` | string | Yes | Host | Canonical identity of the selected route declaration |
| `target_agent_type` | string | Yes | Host | Agent type fixed by the selected route |
| `target_instance_id` | string | Yes | Host | Target fixed before the record becomes accepted |

The host MUST derive `tenant_id`, `principal_id`, and `trace_context` from the
authenticated transport context. Sender-supplied values for those fields have
no authority and MUST be rejected with `signal.malformed.host_field_supplied`.
The host MUST record `received_at` once, at complete receipt, before validating
event content. It MUST NOT change that value during retry-free delivery,
recovery, audit, or replay.

### Guest-wire projection

> **Normative definition.**
After validation and target selection, the host constructs `signal` by copying
the seven `SignalSubmission` fields unchanged and adding the derived
`delivery_id`. It then constructs `TurnRequest` using the exact mapping in
[Signal envelope](04-turn-lifecycle-protocols-and-canonical-encoding.md#signal-envelope).

The host MUST persist `AcceptedSignalEnvelope` before guest invocation. Replay
MUST use its recorded signal, authentication context, trace context, route,
and target. Replay MUST NOT reevaluate TTL, rerun instance selection, or
advance a round-robin cursor.

### Transport identity

> **Normative definition.**
The `delivery_id` is the transport identity assigned by the host after a
logical signal passes duplicate detection and before persisting the accepted
record. It is:

`delivery:` followed by the lowercase hexadecimal SHA-256 digest of canonical
JSON encoding of
`[tenant_id, type, source, subject, correlation_id, timestamp]`.

The canonical logical-signal identity uses the same digest in
`signal:sha256:<hex-digest>` as defined by
[Canonical text representations](02-stable-identities-versions-errors-and-limits.md#canonical-text-representations).
The same accepted logical signal therefore has one deterministic delivery
identity. Duplicate submissions are rejected and MUST NOT create another
delivery identity or attempt.

### Signal identity

> **Normative definition.**
The tuple `(tenant_id, type, source, subject, correlation_id, timestamp)`
identifies a logical signal, consistent with the tenant-scoped identity rule
in
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md#identity-types).
Two signals with the same identity are considered duplicates.
The host MUST detect duplicates and reject them with a `signal.duplicate` diagnostic.

### Fixed TTL

> **Normative definition.**
The base signal TTL is exactly 300,000 milliseconds. It is not configurable
and a conformance profile MUST NOT replace it. Let:

> **Normative definition.**

```
age_ms = unix_time_ms(received_at) - unix_time_ms(submission.timestamp)
```

Both values are interpreted at exact millisecond precision after canonical
timestamp validation. If `age_ms < 0`, the host MUST reject the submission with
`signal.malformed.timestamp_future`. If `age_ms > 300000`, the host MUST reject
it with `signal.expired.timestamp_too_old`. An age of exactly `300000` is
accepted. The host MUST perform this check against the immutable `received_at`
recorded for that submission, never against a later wall clock. Recovery
and replay use the recorded acceptance outcome and do not reevaluate age.

### Delivery attempt

> **Normative definition.**
An accepted logical signal has exactly one delivery attempt using its one
`delivery_id`. The base protocol has no automatic retry, redelivery, alternate
delivery identity, or duplicate attempt.

### Causal parent

> **Normative definition.**
The `causation_id` references the `delivery_id` of the parent signal or
the `invocation_id` of the parent turn.
It establishes the causal chain for distributed debugging and replay.
The `causation_id` MAY be null for root signals.

## 1.1 Section - Contract And Data Model

### Signal type naming

> **Normative definition.**
Signal types contain two or more lowercase segments separated by dots. The
first segment identifies the domain; later segments identify the event within
that domain.

| Prefix | Domain | Examples |
|--------|--------|----------|
| `api` | User or service requests | `api.request`, `api.cancel` |
| `effect` | Host-managed side effects | `effect.result`, `effect.error` |
| `timer` | Scheduled events | `timer.expired`, `timer.snoozed` |
| `sensor` | External system events | `sensor.data`, `sensor.alert` |
| `agent` | Inter-agent communication | `agent.request`, `agent.response` |
| `system` | Runtime events | `system.boot`, `system.shutdown` |

> **Normative definition.**
The `type` field MUST match the pattern `^[a-z]+(\.[a-z]+)+$`.
The host MUST reject signals with invalid type names.

## Signal data schema

> **Normative definition.**
The base protocol defines no separately registered schema for signal `data`.
The host MUST NOT consult a runtime-specific schema when deciding whether to
accept a signal. At this boundary, the host validates only the
`SignalSubmission` structure, canonical encoding, size, routing, identity,
authorization, and expiry rules defined by this chapter.

## Signal size bounds

> **Normative definition.**
The host MUST enforce a maximum signal size of 1 MiB (1,048,576 bytes).
Signals exceeding this limit MUST be rejected with a `signal.oversized` diagnostic.

The guest MAY request smaller limits via the artifact manifest.
The host MUST honor the smaller limit if declared.

## Canonicalization

> **Normative definition.**
Signal `data` MUST be canonical JSON as defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).
The host MUST reject signals with non-canonical `data`.

## 1.2 Section - Behavior And Integration

### Routing declarations

> **Normative definition.**
The host composes an admitted ingress route table from authenticated deployment
policy, the agent registry, and artifact manifest routes. The ingress table
selects an agent type and instance; it is distinct from the artifact `Route`
that dispatches an already-targeted signal to an action or strategy under
[Route definition](03-agent-manifests-artifacts-schemas-and-registries.md#route-definition).

> **Normative definition.**

```
IngressRouteDeclaration {
  match: RouteMatch,
  target: RouteTarget,
  priority: int,
  fallback: IngressRouteDeclaration?
}

RouteMatch {
  type: "exact" | "prefix" | "type" | "subject" | "fallback",
  value: string
}

RouteTarget {
  agent_type: string,
  instance_selector: InstanceSelector?
}

InstanceSelector {
  match: "first" | "round-robin" | "sticky"
}
```

| Match type | Description | Example |
|------------|-------------|---------|
| `exact` | Exact match on signal type or subject | `type: "api.request"` |
| `prefix` | Match on signal type or subject prefix | `type: "effect."` |
| `type` | Match on signal type only | `type: "sensor.*"` |
| `subject` | Match on signal subject only | `subject: "chatbot.*"` |
| `fallback` | Default route when no other matches | `type: "fallback"` |

Unknown fields in `IngressRouteDeclaration`, `RouteTarget`, or
`InstanceSelector` are invalid. In particular, the base profile has no
selector `filter` field. The host MUST reject an ingress route table containing
an unknown selector mode or field with `signal.selector.invalid` before
activating that table.

### Canonical route identity

> **Normative definition.**
Each admitted declaration has the following identity, where every value is the
validated declaration value and `null` represents an absent optional field:

> **Normative definition.**

```
route_id = "route:sha256:" + lowercase_hex(SHA-256(canonical_json([
  match,
  target,
  priority,
  fallback
])))
```

The route identity changes whenever any declaration field changes. Replacing
a route table with a byte-identical declaration retains the same identity and
round-robin cursor; any changed declaration has a new identity and a cursor
initialized to zero.

### Candidate snapshot

> **Normative definition.**
After selecting exactly one route declaration, the host MUST take one
immutable candidate snapshot. It contains every instance that belongs to the
authenticated submission's tenant, has the route target's exact `agent_type`, and is
registered as accepting a turn at snapshot time. Candidate ids are sorted by
their canonical UTF-8 bytes in ascending lexicographic order.

The snapshot is fixed for this selection. A membership or availability change
affects only a later signal. An empty snapshot rejects the signal with
`signal.delivery.unavailable`; the host MUST NOT defer it or select an instance
from another tenant or agent type.

An absent `instance_selector` is exactly equivalent to `{match: "first"}`.
The three selector modes are fixed as follows:

1. **`first`** selects candidate index zero.
2. **`round-robin`** uses the durable cursor algorithm below.
3. **`sticky`** uses the rendezvous-hash algorithm below.

### Round-robin selection

> **Normative definition.**
The host maintains one unsigned 64-bit cursor for each `(tenant_id, route_id)`.
A missing cursor is zero. The host MUST serialize and read the cursor inside
the durable acceptance transaction. For a sorted candidate snapshot of length
`n`, the selected index is `cursor mod n`. In the same transaction that creates
the accepted-ingress record, the host advances the cursor to
`(cursor + 1) mod 2^64` exactly once.

Signals rejected before acceptance do not advance the cursor. Delivery failure
after acceptance does not roll it back. Concurrent selections for the same
cursor key MUST serialize in accepted-record commit order. If the cursor
cannot be read or atomically advanced, the signal is rejected with
`signal.selector.cursor_unavailable`; no accepted record or delivery attempt
is created.

### Sticky selection

> **Normative definition.**
For each candidate id, the host computes:

> **Normative definition.**

```
score(candidate_id) = SHA-256(canonical_json([
  tenant_id,
  route_id,
  submission.correlation_id,
  candidate_id
]))
```

The digest is interpreted as an unsigned 256-bit big-endian integer. The host
selects the candidate with the greatest score. A digest collision is broken by
the lexicographically smallest candidate id. Sticky selection changes no
cursor. The same tenant, route, correlation id, and candidate snapshot MUST
therefore select the same instance regardless of registry enumeration order.

## Routing precedence

> **Normative definition.**
The host MUST evaluate route declarations in the following order:

1. `exact` matches on signal type (highest priority)
2. `exact` matches on signal subject
3. `prefix` matches on signal type
4. `prefix` matches on signal subject
5. `type` matches on signal type
6. `subject` matches on signal subject
7. `fallback` matches (lowest priority)

Within the same match type, declarations with lower `priority` values
are evaluated first.

The admitted route table and every declaration's `priority` value are
immutable while routing a signal. A replacement route table affects only
signals accepted after that replacement becomes active. The host MUST NOT
dynamically adjust priority values.

> **Normative definition.**
If no route matches, the host MUST reject the signal with a
`signal.unmatched` diagnostic.

## Routing outcomes

| Outcome | Condition | Diagnostic |
|---------|-----------|------------|
| Matched | A route declaration matches | None |
| Unmatched | No route declaration matches | `signal.unmatched` |
| Ambiguous | Multiple routes match with same priority | `signal.ambiguous` |
| Unauthorized | Signal source is not authorized for the target | `signal.unauthorized` |
| Expired | Signal age is greater than the fixed 300,000 ms TTL | `signal.expired.timestamp_too_old` |
| Duplicate | Signal identity matches a previously accepted signal | `signal.duplicate` |
| Malformed | Submission fails structure, canonicalization, or future-timestamp validation | `signal.malformed` |
| Selector unavailable | Durable round-robin selection cannot commit | `signal.selector.cursor_unavailable` |
| Target unavailable | Candidate snapshot is empty or the accepted target cannot take its attempt | `signal.delivery.unavailable` |

### Submission evaluation order

> **Normative definition.**
The host MUST evaluate a submission in this order and emit the diagnostic from
the first failing step:

1. Record authenticated host context and immutable `received_at`.
2. Validate submission structure, canonical encoding, type, and size.
3. Apply the fixed future-timestamp and TTL rules.
4. Compute logical identity and reject a previously accepted duplicate.
5. Resolve exactly one route under the fixed precedence rules.
6. Authorize the source for that route and target agent type.
7. Build the immutable candidate snapshot and run the selected algorithm.
8. Derive `delivery_id` and atomically persist `AcceptedSignalEnvelope`,
   including any round-robin cursor advance.

No failed step creates an accepted record or delivery attempt. Only step 8 may
advance a cursor.

## Delivery vocabulary

> **Normative definition.**
The delivery vocabulary describes the lifecycle of a signal from
submission to final disposition.

| State | Description | Transition |
|-------|-------------|------------|
| Accepted | Signal passes validation and is queued for one delivery attempt | Submitted -> Accepted |
| Rejected | Signal fails validation or its single delivery attempt fails | Submitted or Accepted -> Rejected |
| Deferred | Reserved; unreachable in the base protocol | None |
| Delivered | The one guest delivery attempt completes successfully | Accepted -> Delivered |
| Redelivered | Reserved; unreachable in the base protocol | None |
| Coalesced | Reserved; unreachable in the base protocol | None |
| Dead-lettered | Reserved; unreachable in the base protocol | None |

### Acceptance criteria

> **Normative definition.**
A signal is accepted only after all ordered submission checks succeed and:

- Its submission structure is valid.
- It passes canonicalization validation.
- It passes size bounds validation.
- A route matches.
- The signal is not a duplicate.
- The signal source is authorized.
- The signal is not expired.
- One target is selected and the accepted-ingress record is durable.

### Rejection criteria

> **Normative definition.**
A signal is rejected if:

- Its submission structure is invalid.
- It fails canonicalization validation.
- It exceeds size bounds.
- Its timestamp is in the future or exceeds the fixed TTL.
- No route matches.
- It is a duplicate.
- The signal source is unauthorized.
- Selector state is unavailable.
- The target is unavailable or the one delivery attempt fails.

### Deferral criteria

> **Normative definition.**
The host MUST NOT defer an accepted signal in the base protocol. If the target
is unavailable when the one delivery attempt is due, the signal transitions to
`Rejected` and emits `signal.delivery.unavailable`.

### Delivery criteria

> **Normative definition.**
A signal is delivered if:

- It is accepted.
- The target agent instance is available.
- No delivery attempt has previously been made for the logical signal identity.
- The resulting turn completes successfully.

### Redelivery criteria

> **Normative definition.**
The host MUST NOT redeliver a signal automatically. A failed delivery attempt
transitions the signal to `Rejected` and emits `signal.delivery.failed`.

### Coalescing criteria

> **Normative definition.**
The host MUST NOT coalesce accepted signals. Distinct non-duplicate signal
identities are delivered independently even when they share a
`correlation_id` and target.

### Dead-letter criteria

> **Normative definition.**
The host MUST NOT move signals to a dead-letter queue in the base protocol.
Invalid signals and failed delivery attempts terminate in `Rejected` with
their governing diagnostic.

## 1.3 Section - Failure Evidence And Operational Notes

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
| `signal.malformed` | Signal validation failures | `invalid_type`, `invalid_source`, `invalid_subject`, `unknown_field`, `host_field_supplied`, `timestamp_future` |
| `signal.schema` | Reserved; not emitted by the base protocol | `type_mismatch`, `required_field_missing` |
| `signal.oversized` | Size bounds violations | `data_too_large` |
| `signal.unmatched` | Routing failures | `no_route` |
| `signal.ambiguous` | Ambiguous routing | `multiple_matches` |
| `signal.unauthorized` | Authorization failures | `principal_not_allowed` |
| `signal.expired` | TTL violations | `timestamp_too_old` |
| `signal.duplicate` | Duplicate detection | `identity_matches` |
| `signal.selector` | Instance-selector failures | `invalid`, `cursor_unavailable` |
| `signal.delivery` | Delivery-attempt failures | `failed`, `unavailable` |
| `signal.dead_letter` | Reserved; not emitted by the base protocol | `retry_exhausted` |
| `identity.limit` | Turn-duration implementation limit | `time.turn_ms` |

## Fixed optional-feature policy

1. **Schema registration**: The schema-registration disposition is governed by
   [Signal data schema](#signal-data-schema).

2. **Coalescing**: Coalescing is prohibited by
   [Coalescing criteria](#coalescing-criteria).

3. **Dead-letter storage**: Dead-lettering and dead-letter storage are
   prohibited by [Dead-letter criteria](#dead-letter-criteria).

4. **Retry policy**: Automatic retry is prohibited by
   [Redelivery criteria](#redelivery-criteria).

5. **Route priority**: Priorities are immutable for the active route-table
   snapshot under [Routing precedence](#routing-precedence).

6. **Signal TTL**: The TTL and boundary arithmetic are fixed by
   [Fixed TTL](#fixed-ttl); no profile selection or override is permitted.

7. **Instance selection**: Candidate ordering, cursor handling, and sticky
   hashing are fixed by [Candidate snapshot](#candidate-snapshot),
   [Round-robin selection](#round-robin-selection), and
   [Sticky selection](#sticky-selection).

## Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Schema registry**: A future versioned extension may define a formal signal
   data-schema registry. The base protocol does not consult one.

2. **Coalescing algorithm**: A future versioned extension may define a formal
   coalescing algorithm. The base protocol prohibits coalescing.

3. **Dead-letter API**: A future versioned extension may define a formal
   dead-letter API. The base protocol prohibits dead-lettering.

4. **Route priority API**: A future versioned extension may define route-table
   replacement. The base protocol prohibits dynamic priority adjustment within
   an active table.

## 1.4 Section - Phase 1 Integration Tests

### Successful routing

> **Normative definition.**
The successful routing integration test validates that a valid signal is
routed to the correct agent instance and delivered successfully.

Expected behavior:

- Input: valid signal with matching route.
- Expected output: one durable `AcceptedSignalEnvelope` and one `TurnRequest`
  whose signal, tenant, principal, trace, and target fields match the fixed
  projection.
- Expected error: null.

### Accepted-envelope projection

> **Normative definition.**
The accepted-envelope projection test validates that host metadata is not
duplicated inside the guest signal and cannot diverge during projection.

Expected behavior:

- Input: one accepted record with known signal, tenant, principal, trace,
  route, and target values.
- Expected output: byte-identical `TurnRequest.signal` and trace context plus
  matching runtime tenant/principal, agent type, and agent instance.
- Expected error: null.
- Mutation: change each projected host-owned value in turn.
- Mutation error: `protocol.semantic.context_projection_invalid` before guest
  invocation.

### Unmatched signal

> **Normative definition.**
The unmatched signal integration test validates that a signal with no
matching route is rejected with a `signal.unmatched` diagnostic.

Expected behavior:

- Input: valid signal with no matching route.
- Expected output: null.
- Expected error: `signal.unmatched`.

### Ambiguous routing

> **Normative definition.**
The ambiguous routing integration test validates that a signal with multiple
matching routes at the same priority is rejected with a `signal.ambiguous`
diagnostic.

Expected behavior:

- Input: valid signal with multiple matching routes at same priority.
- Expected output: null.
- Expected error: `signal.ambiguous`.

### First-instance selection

> **Normative definition.**
The first-instance test supplies the candidates `u-3`, `u-1`, and `u-2` in
each possible registry enumeration order.

Expected behavior:

- Expected target: `u-1` for every enumeration order.
- Expected cursor change: none.
- Expected error: null.

### Round-robin selection

> **Normative definition.**
The round-robin test uses sorted candidates `u-1`, `u-2`, and `u-3`, a new
route cursor, four accepted signals, one rejected submission, and replay of
the second accepted record.

Expected behavior:

- Accepted targets in commit order: `u-1`, `u-2`, `u-3`, `u-1`.
- The rejected submission does not advance the cursor.
- Replay uses its recorded `u-2` target and does not advance the cursor.
- A simulated failure to atomically advance the cursor rejects with
  `signal.selector.cursor_unavailable` and creates no accepted record.

### Sticky selection

> **Normative definition.**
The sticky test evaluates the fixed rendezvous score for one tenant, route,
and correlation id against at least three candidates, then repeats with every
candidate enumeration order.

Expected behavior:

- Expected target: the candidate with the greatest specified score, or the
  lexicographically smallest candidate on a score collision.
- Every enumeration order selects the same target.
- Repeated signals with the same correlation id and candidate snapshot select
  the same target and do not mutate a cursor.

### Selector rejection

> **Normative definition.**
Selector rejection tests validate conservative failure behavior.

Expected behavior:

- An unknown selector mode or field rejects route-table admission with
  `signal.selector.invalid`.
- An empty candidate snapshot rejects the signal with
  `signal.delivery.unavailable` and creates no accepted record.
- No selector failure falls back to another tenant, agent type, or selector.

### Unauthorized signal

> **Normative definition.**
The unauthorized signal integration test validates that a signal from an
unauthorized source is rejected with a `signal.unauthorized` diagnostic.

Expected behavior:

- Input: valid signal from unauthorized source.
- Expected output: null.
- Expected error: `signal.unauthorized`.

### Expired signal

> **Normative definition.**
The TTL integration test validates the exact fixed boundary and recorded-time
behavior.

Expected behavior:

- Input A: `received_at - timestamp = 300000 ms`.
- Expected A: accepted.
- Input B: `received_at - timestamp = 300001 ms`.
- Expected B: rejected with `signal.expired.timestamp_too_old`.
- Input C: `timestamp - received_at = 1 ms`.
- Expected C: rejected with `signal.malformed.timestamp_future`.
- Replay: advance the wall clock beyond the TTL and replay Input A's accepted
  record.
- Replay result: recorded acceptance and target are reused without TTL
  reevaluation.

### Duplicate signal

> **Normative definition.**
The duplicate signal integration test validates that a signal with a
duplicate identity is rejected with a `signal.duplicate` diagnostic.

Expected behavior:

- Input: valid signal with duplicate identity.
- Expected output: null.
- Expected error: `signal.duplicate`.

### Oversized signal

> **Normative definition.**
The oversized signal integration test validates that a signal exceeding
the size limit is rejected with a `signal.oversized` diagnostic.

Expected behavior:

- Input: valid signal with data exceeding 1 MiB.
- Expected output: null.
- Expected error: `signal.oversized`.

### Malformed signal

> **Normative definition.**
The malformed signal integration test validates that a submission with an
invalid structure or non-canonical data is rejected with a `signal.malformed`
diagnostic.

Expected behavior:

- Input: valid signal with non-canonical data.
- Expected output: null.
- Expected error: `signal.malformed`.
- Input mutation: sender supplies `tenant_id`, `principal_id`, `trace_context`,
  or another unknown field.
- Mutation error: `signal.malformed.host_field_supplied` for a host-owned field
  and `signal.malformed.unknown_field` for any other unknown field.

### Timeout and cancellation

> **Normative definition.**
The timeout and cancellation integration test validates that the host
handles delivery timeouts and cancellation requests correctly.

Expected behavior:

- Input: signal delivery that exceeds deadline_ms.
- Expected output: null.
- Expected error: `identity.limit.time.turn_ms`.

The host MUST NOT leave unauthorized or partial state after a timeout.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 1 to verify
no regressions.

Expected behavior:

- All Milestone 1 fixtures: PASS.
- All earlier Milestone 2 Phase 1 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
|--------|------|-----------|
| Signal type naming | Required | Pattern fixed by this chapter |
| [Ingress and guest-wire mapping](#guest-wire-projection) | Required | Host wrapper maps to one Chapter 04 `SignalEnvelope`; tenant, principal, and trace are not duplicated |
| [Recorded receive time](#fixed-ttl) | Required | Assigned once at complete receipt and reused for recovery and replay |
| [Signal TTL](#fixed-ttl) | Required | Exactly 300,000 ms; future timestamps rejected; no override |
| Signal size bounds | Required | 1 MiB maximum |
| [Smaller artifact signal limit](#signal-size-bounds) | MAY | Guest may request a smaller ceiling, which the host must honor |
| Canonicalization | Required | Rules fixed by this chapter |
| Routing precedence | Required | Order fixed by this chapter |
| [Schema registration](#signal-data-schema) | Required | No separately registered schemas in the base protocol |
| [Coalescing](#coalescing-criteria) | Required | Prohibited; distinct signals are delivered independently |
| [Dead-letter storage](#dead-letter-criteria) | Required | Prohibited; failures terminate in `Rejected` |
| [Retry policy](#redelivery-criteria) | Required | One delivery attempt; no automatic redelivery |
| [Route priority](#routing-precedence) | Required | Immutable within the active route-table snapshot |
| [Route identity](#canonical-route-identity) | Required | SHA-256 over the canonical declaration fields |
| [Candidate snapshot](#candidate-snapshot) | Required | Tenant/type constrained and lexicographically sorted; no selector filters |
| [First selector](#candidate-snapshot) | Required | Candidate index zero; also the absent-selector default |
| [Round-robin selector](#round-robin-selection) | Required | Durable serialized cursor advanced atomically once per accepted record |
| [Sticky selector](#sticky-selection) | Required | Greatest rendezvous SHA-256 score with lexical collision tie-break |
| [Delivery identity](#transport-identity) | Required | Deterministic SHA-256 derivation from the tenant-scoped logical signal identity |
| [Deferral](#deferral-criteria) | Required | Prohibited; unavailable targets reject the one attempt |
| [Root-signal causation](#causal-parent) | MAY | Root signals may use null causation; non-root signals cite their parent |

## Rationale and evidence (non-normative)

This chapter derives from the turn protocol requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The signal envelope model provides:

- A uniform event structure for all signal types.
- Clear separation between transport, identity, and causality metadata.
- Deterministic routing based on declared rules.

The routing precedence model provides:

- Predictable signal delivery for deterministic turns.
- Flexible routing for diverse signal types.
- Clear error reporting for ambiguous or unmatched signals.

The delivery vocabulary provides:

- Stable signal lifecycle tracking.
- Bounded diagnostics for failures.
- Clear separation between transient and permanent failures.
