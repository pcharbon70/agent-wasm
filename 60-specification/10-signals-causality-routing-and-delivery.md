---
title: "Signal Envelopes Causality Routing And Delivery Vocabulary"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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
The signal envelope carries the transport, identity, causality,
and delivery metadata required for deterministic routing and processing.

> **Normative definition.**
This SignalEnvelope extends the definition in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#signal-envelope)
with host-injected fields for multi-tenant isolation, authorization,
and distributed tracing.

> **Normative definition.**

```
SignalEnvelope {
  type: string,
  source: string,
  subject: string,
  correlation_id: string,
  causation_id: string?,
  timestamp: ISO 8601 UTC,
  data: JsonObject?,
  tenant_id: string,
  principal_id: string?,
  delivery_id: string,
  trace_context: TraceContext
}
```

| Field | Type | Required | Source | Purpose |
|-------|------|----------|--------|---------|
| `type` | string | Yes | Sender | Signal category and schema key |
| `source` | string | Yes | Sender | Origin of the signal |
| `subject` | string | Yes | Sender | Target recipient or resource |
| `correlation_id` | string | Yes | Sender | Grouping identifier for related signals |
| `causation_id` | string? | No | Sender | Parent signal or instruction identifier |
| `timestamp` | ISO 8601 UTC | Yes | Sender | Event time at origin |
| `data` | JsonObject? | No | Sender | Signal payload |
| `tenant_id` | string | Yes | Host | Multi-tenant isolation |
| `principal_id` | string? | No | Host | Calling principal for authorization |
| `delivery_id` | string | Yes | Host | Per-delivery identity for deduplication |
| `trace_context` | TraceContext | Yes | Host | Distributed tracing metadata |

### Transport identity

> **Normative definition.**
The `delivery_id` is the transport identity assigned by the host at delivery time.
It is unique per delivery attempt and survives retries.
The host MUST assign `delivery_id` before invoking the reduce export.

### Signal identity

> **Normative definition.**
The tuple `(type, source, subject, correlation_id, timestamp)` identifies
a logical signal.
Two signals with the same identity are considered duplicates.
The host MUST detect duplicates and reject them with a `signal.duplicate` diagnostic.

### Delivery attempt

> **Normative definition.**
Each delivery attempt has a unique `delivery_id` even if the signal is a duplicate.
The host MAY retry delivery based on the delivery policy.
The guest MUST NOT rely on `delivery_id` stability across retries.

### Causal parent

> **Normative definition.**
The `causation_id` references the `delivery_id` of the parent signal or
the `invocation_id` of the parent turn.
It establishes the causal chain for distributed debugging and replay.
The `causation_id` MAY be null for root signals.

## 1.1 Section - Contract And Data Model

### Signal type naming

> **Normative definition.**
Signal types follow the naming convention `<domain>.<subject>.<event>`.

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
Each signal type MAY have an associated JSON schema defining the `data` field.
Schema registration is implementation-defined and does not create
conformance obligations for the base protocol.

The host MAY validate `data` against the registered schema before delivery.
Validation failures MUST be rejected with a `signal.schema` diagnostic.

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
The artifact manifest declares routing rules that map signal types to
reducer entry points.
The host uses these rules to route signals to the correct agent instance
and turn state.

> **Normative definition.**

```
RouteDeclaration {
  match: RouteMatch,
  target: RouteTarget,
  priority: int,
  fallback: RouteDeclaration?
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
  match: "first" | "round-robin" | "sticky",
  filter: JsonObject?
}
```

| Match type | Description | Example |
|------------|-------------|---------|
| `exact` | Exact match on signal type or subject | `type: "api.request"` |
| `prefix` | Match on signal type or subject prefix | `type: "effect."` |
| `type` | Match on signal type only | `type: "sensor.*"` |
| `subject` | Match on signal subject only | `subject: "chatbot.*"` |
| `fallback` | Default route when no other matches | `type: "fallback"` |

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
| Expired | Signal timestamp is older than the configured TTL | `signal.expired` |
| Duplicate | Signal identity matches a previously delivered signal | `signal.duplicate` |
| Malformed | Signal fails schema or canonicalization validation | `signal.malformed` |

## Delivery vocabulary

> **Normative definition.**
The delivery vocabulary describes the lifecycle of a signal from
submission to final disposition.

| State | Description | Transition |
|-------|-------------|------------|
| Accepted | Signal passes validation and is queued for delivery | Malformed -> Accepted |
| Rejected | Signal fails validation and is discarded | Accepted -> Rejected |
| Deferred | Signal is queued for later delivery (e.g., backoff) | Accepted -> Deferred |
| Delivered | Signal is delivered to the guest | Deferred -> Delivered |
| Redelivered | Signal is delivered again after a previous failure | Rejected -> Redelivered |
| Coalesced | Multiple signals are merged into one delivery | Accepted -> Coalesced |
| Dead-lettered | Signal exceeds retry limits and is moved to dead-letter queue | Rejected -> Dead-lettered |

### Acceptance criteria

> **Normative definition.**
A signal is accepted if:

- It passes schema validation.
- It passes canonicalization validation.
- It passes size bounds validation.
- A route matches.
- The signal is not a duplicate.
- The signal source is authorized.
- The signal is not expired.

### Rejection criteria

> **Normative definition.**
A signal is rejected if:

- It fails schema validation.
- It fails canonicalization validation.
- It exceeds size bounds.
- No route matches.
- It is a duplicate.
- The signal source is unauthorized.
- The signal is expired.

### Deferral criteria

> **Normative definition.**
A signal is deferred if:

- The target agent instance is busy (backoff policy).
- The target agent instance is shutting down.
- A resource limit is temporarily exceeded.

### Delivery criteria

> **Normative definition.**
A signal is delivered if:

- It is accepted.
- The target agent instance is available.
- The delivery attempt has not exceeded the retry limit.

### Redelivery criteria

> **Normative definition.**
A signal is redelivered if:

- The previous delivery failed.
- The retry limit has not been exceeded.
- The backoff period has elapsed.

### Coalescing criteria

> **Normative definition.**
Signals are coalesced if:

- They have the same correlation_id.
- They are delivered within the configured coalescing window.
- They target the same agent instance.

### Dead-letter criteria

> **Normative definition.**
A signal is dead-lettered if:

- The retry limit is exceeded.
- The signal is permanently invalid.

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
| `signal.malformed` | Signal validation failures | `invalid_type`, `invalid_source`, `invalid_subject` |
| `signal.schema` | Schema validation failures | `type_mismatch`, `required_field_missing` |
| `signal.oversized` | Size bounds violations | `data_too_large` |
| `signal.unmatched` | Routing failures | `no_route` |
| `signal.ambiguous` | Ambiguous routing | `multiple_matches` |
| `signal.unauthorized` | Authorization failures | `principal_not_allowed` |
| `signal.expired` | TTL violations | `timestamp_too_old` |
| `signal.duplicate` | Duplicate detection | `identity_matches` |
| `signal.dead_letter` | Dead-letter queue | `retry_exhausted` |
| `signal.timeout` | Turn deadline exceeded | `deadline_exceeded` |

## Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Schema registration**: The host MAY implement schema registration for
   signal types. The registration API and storage are implementation-defined.

2. **Coalescing window**: The host MAY implement signal coalescing.
   The coalescing window and algorithm are implementation-defined.

3. **Dead-letter storage**: The host MAY implement dead-letter queue storage.
   The storage backend and retention policy are implementation-defined.

4. **Retry policy**: The host MAY implement retry policies for failed
   deliveries. The policy parameters (max_retries, backoff_strategy) are
   implementation-defined.

5. **Route priority**: The host MAY allow dynamic route priority adjustment.
   The adjustment API and rules are implementation-defined.

## Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Schema registry**: A formal schema registry will be implemented in
   future milestones. The protocol is language-neutral and does not require
   schema registration for base conformance.

2. **Coalescing algorithm**: A formal coalescing algorithm will be implemented
   in future milestones. The protocol is language-neutral and does not require
   coalescing for base conformance.

3. **Dead-letter API**: A formal dead-letter queue API will be implemented
   in future milestones. The protocol is language-neutral and does not require
   dead-letter queues for base conformance.

4. **Route priority API**: A formal route priority adjustment API will be
   implemented in future milestones. The protocol is language-neutral and
   does not require dynamic priority adjustment for base conformance.

## 1.4 Section - Phase 1 Integration Tests

### Successful routing

> **Normative definition.**
The successful routing integration test validates that a valid signal is
routed to the correct agent instance and delivered successfully.

Expected behavior:

- Input: valid signal with matching route.
- Expected output: signal delivered to guest.
- Expected error: null.

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
The expired signal integration test validates that a signal older than the
configured TTL is rejected with a `signal.expired` diagnostic.

Expected behavior:

- Input: valid signal with timestamp older than TTL.
- Expected output: null.
- Expected error: `signal.expired`.

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
The malformed signal integration test validates that a signal with invalid
schema or non-canonical data is rejected with a `signal.malformed` diagnostic.

Expected behavior:

- Input: valid signal with non-canonical data.
- Expected output: null.
- Expected error: `signal.malformed`.

### Timeout and cancellation

> **Normative definition.**
The timeout and cancellation integration test validates that the host
handles delivery timeouts and cancellation requests correctly.

Expected behavior:

- Input: signal delivery that exceeds deadline_ms.
- Expected output: null.
- Expected error: `signal.timeout`.

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

| Clause | Type | Selection |
|--------|------|-----------|
| Signal type naming | Required | Pattern fixed by this chapter |
| Signal size bounds | Required | 1 MiB maximum |
| Canonicalization | Required | Rules fixed by this chapter |
| Routing precedence | Required | Order fixed by this chapter |
| Schema registration | Implementation-defined | Documented in conformance profile |
| Coalescing window | Implementation-defined | Documented in conformance profile |
| Dead-letter storage | Implementation-defined | Documented in conformance profile |
| Retry policy | Implementation-defined | Documented in conformance profile |
| Route priority | Implementation-defined | Documented in conformance profile |

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