---
title: "Sensors Schedules Timers And External Signal Ingress"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-03
  - phase-04
  - sensor
  - schedule
  - timer
  - signal-ingress
aliases:
  - "M3-P4 Sensors Schedules Timers And External Signal Ingress"
---

# Sensors Schedules Timers And External Signal Ingress

## Status and authority

This chapter is a normative specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/phase-04-sensors-schedules-timers-and-external-signal-ingress.md)
of
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
--
Host Actor Runtime And Lifecycle.
It converts external events and time into validated signals without granting
event sources direct access to agent state.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

## 4.1 Contract And Data Model

### Sensor descriptor

> **Normative definition.**
A sensor descriptor defines the identity, source configuration reference,
emitted signal schemas, grants, lifecycle, and checkpoint data for a sensor.

> **Normative definition.**

```
SensorDescriptor {
  sensor_id: SensorId,
  tenant_id: TenantId,
  agent_id: AgentId?,
  source_config: SourceConfigRef,
  signal_schemas: SignalSchema[],
  grants: Grant[],
  lifecycle: SensorLifecycle,
  checkpoint: SensorCheckpoint?
}

SensorId = string

SourceConfigRef {
  type: SourceType,
  config_id: string,
  version: string,
  authentication: SourceAuthentication
}

SourceType = "http" | "websocket" | "file" | "queue" | "custom"

SourceAuthentication {
  kind: SourceAuthenticationKind,
  credential_ref: string
}

SourceAuthenticationKind = "api-key" | "oauth2" | "mtls"

SignalSchema {
  type: string,
  version: string,
  data_schema: SchemaRef
}

SchemaRef {
  name: string,
  version: string
}

SensorLifecycle {
  enabled: bool,
  max_events_per_minute: u64,
  max_queue_size: u64,
  retry_policy: RetryPolicy
}

RetryPolicy {
  max_attempts: u64,
  backoff_ms: u64,
  jitter_ms: u64?
}

SensorCheckpoint {
  last_event_id: string,
  last_timestamp: UnixTimestamp,
  last_sequence: u64
}
```

`TenantId`, `AgentId`, and `UnixTimestamp` are defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).
`Grant` is defined in
[Grants](04-turn-lifecycle-protocols-and-canonical-encoding.md#grants).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `sensor_id` | SensorId | Yes | Unique sensor identifier |
| `tenant_id` | TenantId | Yes | Tenant this sensor belongs to |
| `agent_id` | AgentId? | No | Optional authenticated target constraint; null imposes none |
| `source_config` | SourceConfigRef | Yes | Source configuration reference |
| `signal_schemas` | SignalSchema[] | Yes | Schemas for signals emitted by this sensor |
| `grants` | Grant[] | Yes | Grants for this sensor |
| `lifecycle` | SensorLifecycle | Yes | Sensor lifecycle configuration |
| `checkpoint` | SensorCheckpoint? | No | Last processed event checkpoint |

> **Normative definition.**
The `agent_id` field is optional.
If null, the sensor imposes no target-instance constraint and Chapter 10 still
selects exactly one target for each submission. If present, the selected route
MUST resolve to that agent or admission fails with
`signal.ingress.resolution_failed`; the field never bypasses canonical route
or selector evaluation. Fan-out requires separate submissions with distinct
logical signal identities and is not implicit when this field is null.

> **Normative definition.**
The `signal_schemas` field defines the signal schemas that this sensor
can emit.
The host MUST validate emitted signals against these schemas.

> **Normative definition.**
`source_config.authentication.kind` MUST be one of `api-key`, `oauth2`, or
`mtls`, and `credential_ref` MUST identify host-custodied credential material.
The descriptor MUST NOT contain the credential material itself. An unknown
authentication kind or unresolved credential reference is malformed and MUST
be rejected with `signal.ingress.malformed` before the source is enabled.

> **Normative definition.**
`SensorLifecycle.retry_policy.jitter_ms` MUST be absent or zero. A non-zero
value is malformed and MUST be rejected with `signal.ingress.malformed`.

### Schedule expression

> **Normative definition.**
A schedule expression defines the timing, timezone, misfire behavior, jitter,
next-fire calculation, and cancellation for a schedule.

> **Normative definition.**

```
ScheduleExpression {
  expression: string,
  timezone: string,
  misfire_policy: MisfirePolicy,
  jitter_ms: u64?,
  next_fire_calculation: NextFireCalculation
}

MisfirePolicy = "skip" | "execute_immediately" | "execute_at_next_interval"

NextFireCalculation = "from_last_fire" | "from_schedule_start"
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `expression` | string | Yes | Cron-like schedule expression |
| `timezone` | string | Yes | IANA timezone identifier |
| `misfire_policy` | MisfirePolicy | Yes | Behavior when a fire is missed |
| `jitter_ms` | u64? | No | Maximum deterministic jitter in milliseconds |
| `next_fire_calculation` | NextFireCalculation | Yes | How to calculate next fire time |

> **Normative definition.**
The `expression` field consists of exactly five fields in the order
`minute hour day-of-month month day-of-week`, separated by one or more ASCII
spaces. Each field is either `*` or a canonical unsigned decimal integer in
these inclusive ranges: minute `0..59`, hour `0..23`, day-of-month `1..31`,
month `1..12`, and day-of-week `0..6` with Sunday equal to `0`. A canonical
integer has no leading zero unless it is `0`. Lists, ranges, steps, names, and
all other forms are invalid. When both day fields are integers, both MUST
match. The host MUST reject any other syntax with
`schedule.expression.invalid`.

> **Normative definition.**
The `timezone` field uses IANA timezone identifiers (e.g., "America/New_York").
The host MUST validate the timezone identifier.
Invalid timezones MUST be rejected with `schedule.timezone.invalid`.

> **Normative definition.**
The `misfire_policy` field defines the behavior when a scheduled fire is missed:
- **skip**: Skip the missed fire.
- **execute_immediately**: Execute the missed fire immediately.
- **execute_at_next_interval**: Execute the missed fire at the next interval.

> **Normative definition.**
The `jitter_ms` field is optional.
If present, the host MUST add the following deterministic offset between zero
and `jitter_ms` to the unjittered fire time. Let `H` be the unsigned big-endian
integer represented by the first eight bytes of SHA-256 over the canonical JSON
encoding defined by
[Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding)
of `[expression, timezone, unjittered_fire_time]`, where
`unjittered_fire_time` is its canonical UTC `UnixTimestamp`. The offset is `H`
when `jitter_ms` is `18446744073709551615`; otherwise it is
`H mod (jitter_ms + 1)`. No other jitter calculation is conforming.

### Durable timer directive

> **Normative definition.**
A durable timer directive defines a stable identity, due time, completion
policy, and causation for a timer.

> **Normative definition.**

```
DurableTimer {
  timer_id: TimerId,
  tenant_id: TenantId,
  agent_id: AgentId,
  due_time: UnixTimestamp,
  completion_policy: TimerCompletionPolicy,
  causation_id: String
}

TimerId = string

TimerCompletionPolicy {
  kind: CompletionKind,
  on_complete: CompleteBehavior
}

CompleteBehavior = "emit_signal" | "cancel_timer" | "noop"
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `timer_id` | TimerId | Yes | Unique timer identifier |
| `tenant_id` | TenantId | Yes | Tenant this timer belongs to |
| `agent_id` | AgentId | Yes | Agent this timer is for |
| `due_time` | UnixTimestamp | Yes | Absolute due time for the timer |
| `completion_policy` | TimerCompletionPolicy | Yes | Behavior when the timer completes |
| `causation_id` | String | Yes | Causation ID for the timer signal |

> **Normative definition.**
The `timer_id` is unique per `(tenant_id, agent_id)` tuple.
The host MUST reject duplicate timer IDs with `timer.duplicate`.

> **Normative definition.**
The `due_time` field is an absolute timestamp.
The host MUST fire the timer at or after the `due_time`.
The host MUST NOT fire the timer before the `due_time`.

## 4.2 Behavior And Integration

### Signal admission boundary

> **Normative definition.**
The host MUST normalize sensor events, timer fires, user requests, and
transport deliveries through one signal admission boundary.

> **Normative definition.**
The signal admission boundary performs the following steps:

1. **Source authentication**: Authenticate the event source and establish the
   host-owned tenant and principal context.
2. **Source resolution**: Resolve the sensor, timer, user transport, or other
   source configuration without selecting a target agent instance.
3. **Source-event schema validation**: For a sensor event, validate the source
   payload against its declared `SignalSchema` before constructing a signal.
   This validates source normalization, not the generic Chapter 10 `data`
   field against a runtime-selected signal schema.
4. **Submission construction**: Construct one canonical `SignalSubmission`
   containing only sender-owned fields.
5. **Canonical signal admission**: Run the complete ordered evaluation in
   [Submission evaluation order](10-signals-causality-routing-and-delivery.md#submission-evaluation-order),
   including TTL, duplicate detection, route resolution, authorization,
   candidate selection, delivery identity, and atomic accepted-record
   persistence.
6. **Mailbox admission**: Enqueue a reference to the persisted
   `AcceptedSignalEnvelope` for its recorded target.

> **Normative definition.**
If any step fails, the host MUST reject the event with the appropriate diagnostic.
The host MUST NOT admit invalid events to the mailbox.

### Source authentication

> **Normative definition.**
The host MUST authenticate each event source using the exact mechanism selected
by `source_config.authentication.kind`: an API key for `api-key`, an OAuth 2.0
token for `oauth2`, or a client certificate authenticated by mutual TLS for
`mtls`. Authentication backend and credential-storage layout MUST NOT change
which credential reference, token, key, or certificate is accepted.

> **Normative definition.**
The host MUST reject unauthenticated sources with `signal.ingress.unauthenticated`.

### Tenant and target-constraint resolution

> **Normative definition.**
The host MUST resolve the tenant and any optional target constraint for each
event using the following mechanisms:

1. **Tenant header**: Resolve the tenant from the `X-Tenant-ID` header.
2. **Agent header**: Treat an authenticated `X-Agent-ID` as a target constraint.
3. **Sensor resolution**: Treat a sensor descriptor's `agent_id` as a target constraint.
4. **Timer resolution**: Treat the timer directive's agent as a target constraint.

> **Normative definition.**
The host MUST reject events with missing or invalid tenant resolution, or
whose Chapter 10 selected target does not satisfy an authenticated target
constraint, with `signal.ingress.resolution_failed`. Constraint resolution
MUST NOT itself choose an instance or advance selector state.

### Schema validation

> **Normative definition.**
Each `SignalSchema.data_schema` MUST resolve to a JSON Schema Draft 2020-12
schema. The host MUST validate the event against that exact schema and MUST
reject an unresolved schema reference as `signal.ingress.schema_invalid`.
The host MUST reject events that fail schema validation with `signal.ingress.schema_invalid`.

### Deduplication

> **Normative definition.**
The host MUST compute and retain the logical identity through Chapter 10's
canonical admission transaction. After first acceptance, a second event with
the same logical identity is rejected with `signal.duplicate`. The host MUST
preserve each accepted logical identity indefinitely across host restart.
There is no time-based deduplication window.

### Mailbox admission

> **Normative definition.**
The host MUST admit events to the mailbox using the following mechanisms:

1. **Priority class**: Assign a priority class to the event.
2. **Mailbox bounds**: Enforce mailbox bounds on the event.
3. **Overload rejection**: Apply the fixed rejection behavior when a bound is
   reached.

> **Normative definition.**
The host MUST admit events to the mailbox with the appropriate priority class.
The host MUST enforce mailbox bounds on all events.

### Signal outcomes

> **Normative definition.**
The host MUST handle the following signal outcomes:

1. **Skipped**: The signal was skipped due to misfire policy.
2. **Replayed**: The signal was replayed from a checkpoint.
3. **Late**: The signal arrived after its deadline.
4. **Duplicate**: The signal was rejected as a duplicate.
5. **Disabled**: The sensor was disabled.
6. **Failed source**: The source failed to emit the signal.

> **Normative definition.**

```
SignalOutcome {
  kind: OutcomeKind,
  message: String,
  diagnostic_code: String
}

OutcomeKind {
  Skipped,
  Replayed,
  Late,
  Duplicate,
  Disabled,
  FailedSource
}
```

| Kind | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| `Skipped` | Signal skipped | Misfire policy is skip | `signal.ingress.skipped` |
| `Replayed` | Signal replayed | Sensor checkpoint replay | `signal.ingress.replayed` |
| `Late` | Signal late | Signal arrived after deadline | `signal.ingress.late` |
| `Duplicate` | Signal duplicate | Duplicate event detected | `signal.duplicate` |
| `Disabled` | Sensor disabled | Sensor is disabled | `signal.ingress.disabled` |
| `FailedSource` | Source failed | Source failed to emit signal | `signal.ingress.failed_source` |

## 4.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to sensors, schedules, timers, and
external signal ingress:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid sensor/schedule/timer structure | Failed JSON parsing or schema validation | `signal.ingress.malformed` |
| Incompatible | Sensor incompatible with signal | Signal schema mismatch | `signal.ingress.incompatible` |
| Conflicting | Duplicate timer ID | Two timers with same ID | `timer.duplicate` |
| Unauthorized | Missing capability for signal ingress | Required capability not granted | `signal.ingress.unauthorized` |
| Exhausted | Resource limits exceeded | Maximum sensors per tenant reached | `sensor.capacity.exhausted` |
| Unavailable | Sensor or timer unavailable | Sensor not found or timer not fired | `signal.ingress.unavailable` |
| Unauthenticated | Source unauthenticated | Source authentication failed | `signal.ingress.unauthenticated` |
| ResolutionFailed | Tenant/agent resolution failed | Tenant or agent not resolved | `signal.ingress.resolution_failed` |
| SchemaInvalid | Event schema invalid | Event failed schema validation | `signal.ingress.schema_invalid` |
| ScheduleInvalid | Schedule expression invalid | Invalid schedule expression | `schedule.expression.invalid` |
| TimezoneInvalid | Timezone invalid | Invalid timezone identifier | `schedule.timezone.invalid` |

> **Normative definition.**
All failure modes MUST produce a diagnostic and terminate the operation without
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
| `signal.ingress` | Source normalization failures | `malformed`, `incompatible`, `unauthorized`, `unavailable`, `unauthenticated`, `resolution_failed`, `schema_invalid`, `skipped`, `replayed`, `late`, `disabled`, `failed_source` |
| `signal.duplicate` | Canonical logical-signal duplicate | `identity_matches` |
| `sensor` | Sensor failures | `capacity.exhausted` |
| `timer` | Timer failures | `duplicate` |
| `schedule` | Schedule failures | `expression.invalid`, `timezone.invalid` |

### Internal mechanisms and fixed behavior

> **Normative definition.**
Credential storage, duplicate-identity indexing, schedule evaluation, and timer
storage are internal mechanisms. Every such mechanism MUST be observationally
equivalent with respect to source acceptance, logical signal identity,
indefinite duplicate rejection, schedule acceptance,
calculated jitter, fire time, mailbox admission, and diagnostics. Runtime configuration
selects a source's authentication kind; it is not a host-release semantic
selection.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Sensor replication**: A formal sensor replication strategy will be implemented in future milestones. The protocol is language-neutral and does not require sensor replication for base conformance.

2. **Multi-tenant signal isolation**: Enhanced multi-tenant signal isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

3. **Timer persistence**: A formal timer persistence mechanism will be implemented in future milestones. The protocol is language-neutral and does not require timer persistence for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 4.4 Phase 4 Integration Tests

### Canonical successful flow

> **Normative conformance criterion.**
The canonical successful flow integration test validates that a valid sensor
event is processed successfully through the full signal ingress pipeline.

Expected behavior:

- Input: valid sensor event with authenticated source, resolved tenant/agent, and valid schema.
- Expected output: one persisted `AcceptedSignalEnvelope` whose reference is
  admitted to the mailbox for its recorded target.
- Expected error: null.

### Negative: malformed event

> **Normative conformance criterion.**
The negative malformed event test validates that invalid events are rejected.

Expected behavior:

- Input: event with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `signal.ingress.malformed`.

### Negative: unauthenticated source

> **Normative conformance criterion.**
The negative unauthenticated source test validates that unauthenticated sources are rejected.

Expected behavior:

- Input: event with missing or invalid authentication.
- Expected output: null.
- Expected error: `signal.ingress.unauthenticated`.

### Negative: resolution failed

> **Normative conformance criterion.**
The negative resolution failed test validates that failed tenant/agent resolution is rejected.

Expected behavior:

- Input: event with missing or invalid tenant/agent.
- Expected output: null.
- Expected error: `signal.ingress.resolution_failed`.

### Negative: schema invalid

> **Normative conformance criterion.**
The negative schema invalid test validates that schema-invalid events are rejected.

Expected behavior:

- Input: event that fails schema validation.
- Expected output: null.
- Expected error: `signal.ingress.schema_invalid`.

### Negative: duplicate event

> **Normative conformance criterion.**
The negative duplicate event test validates that duplicate events are rejected.

Expected behavior:

- Input: event with the same logical signal identity as an earlier accepted
  event, including after host restart.
- Expected output: null.
- Expected error: `signal.duplicate`.

### Negative: late event

> **Normative conformance criterion.**
The negative late event test validates that late events are rejected.

Expected behavior:

- Input: event that arrived after its deadline.
- Expected output: null.
- Expected error: `signal.ingress.late`.

### Negative: disabled sensor

> **Normative conformance criterion.**
The negative disabled sensor test validates that events from disabled sensors are rejected.

Expected behavior:

- Input: event from a disabled sensor.
- Expected output: null.
- Expected error: `signal.ingress.disabled`.

### Negative: failed source

> **Normative conformance criterion.**
The negative failed source test validates that failed sources are handled correctly.

Expected behavior:

- Input: source that failed to emit signal.
- Expected output: null.
- Expected error: `signal.ingress.failed_source`.

### Negative: duplicate timer

> **Normative conformance criterion.**
The negative duplicate timer test validates that duplicate timers are rejected.

Expected behavior:

- Input: timer with duplicate timer ID.
- Expected output: null.
- Expected error: `timer.duplicate`.

### Negative: invalid schedule expression

> **Normative conformance criterion.**
The negative invalid schedule expression test validates that invalid schedule expressions are rejected.

Expected behavior:

- Input: schedule with invalid cron expression.
- Expected output: null.
- Expected error: `schedule.expression.invalid`.

### Negative: invalid timezone

> **Normative conformance criterion.**
The negative invalid timezone test validates that invalid timezones are rejected.

Expected behavior:

- Input: schedule with invalid timezone.
- Expected output: null.
- Expected error: `schedule.timezone.invalid`.

### Fixed authentication, identity, schedule, and jitter behavior

> **Normative conformance criterion.**
The Phase 4 integration tests MUST additionally verify:

1. Each of `api-key`, `oauth2`, and `mtls` accepts only credentials validated
   through the descriptor's `credential_ref`; an unknown kind or unresolved
   reference fails before source enablement.
2. Duplicate detection uses the Chapter 10 logical identity and remains active
   indefinitely across host restart, independent of the identity index
   implementation.
3. A valid five-field expression accepts each boundary integer, while a list,
   range, step, name, leading-zero integer, or out-of-range integer fails with
   `schedule.expression.invalid`.
4. Repeated evaluation of the same expression, timezone, and unjittered UTC
   fire time produces the exact SHA-256-derived offset specified above.
5. A non-zero sensor retry jitter fails with `signal.ingress.malformed`.

### Cross-milestone fixture regression

> **Normative conformance criterion.**
All earlier milestone fixtures MUST be re-run after Phase 4 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Phase 3 fixtures: PASS.
- All Phase 4 fixtures: PASS.
- All Phase 5 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.
- All Milestone 2 Phase 3 fixtures: PASS.
- All Milestone 2 Phase 4 fixtures: PASS.
- All Milestone 2 Phase 5 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 3 exit report.

## Variability register

The register summarizes fixed behavior, runtime record selections, and internal
mechanisms. It does not independently license variation.

| Clause | Type | Selection | Constraint |
|--------|------|-----------|------------|
| Sensor descriptor structure | Required | Fields fixed by this chapter | Reject malformed descriptors before enablement |
| [Source authentication](#source-authentication) | Runtime configuration | `api-key`, `oauth2`, or `mtls` | Use the descriptor's host-custodied `credential_ref` |
| [Duplicate detection](#deduplication) | Required | Chapter 10 logical signal identity | Retain indefinitely across restart and reject before mailbox admission |
| [Event schema validation](#schema-validation) | Required | JSON Schema Draft 2020-12 | Resolve and apply the exact referenced schema |
| [Schedule expression](#schedule-expression) | Required | Fixed five-field integer-or-wildcard grammar | Reject every other form |
| [Schedule jitter](#schedule-expression) | Required | Fixed SHA-256 calculation | Offset remains in `0..jitter_ms` |
| Sensor retry jitter | Required | Absent or zero | Reject non-zero values as malformed |
| Durable timer structure | Required | Fields fixed by this chapter | Preserve timer identity and causation |
| Signal admission boundary | Required | Six steps fixed by this chapter | Source normalization feeds the complete Chapter 10 admission transaction before Chapter 21 mailbox admission |
| Credential, identity-index, schedule, and timer machinery | Internal mechanism | No profile selection | Preserve all acceptance, identity, timing, admission, and diagnostic observations |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The signal ingress provides:

- One admission boundary for all external signals.
- Source authentication and tenant/agent resolution.
- Schema validation and deduplication.

The sensors provide:

- Flexible event sourcing (HTTP, WebSocket, file, queue, custom).
- Checkpoint-based replay.
- Rate limiting and retry policies.

The schedules provide:

- Cron-like schedule expressions.
- Timezone-aware scheduling.
- Misfire handling and jitter.

The timers provide:

- Durable timer directives.
- Stable identities and causation.
- Completion policies.

The failure modes provide:

- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.
- Evidence that failures are handled correctly.

The integration tests provide:

- Verification that the canonical flow works end-to-end.
- Evidence that all failure modes are handled correctly.
- Foundation for cross-implementation conformance testing.
