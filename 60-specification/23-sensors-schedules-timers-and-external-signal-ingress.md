---
title: "Sensors Schedules Timers And External Signal Ingress"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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

## 3.1 Contract And Data Model

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
  version: string
}

SourceType = "http" | "websocket" | "file" | "queue" | "custom"

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

`TenantId`, `AgentId`, `Grant`, and `UnixTimestamp` are defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `sensor_id` | SensorId | Yes | Unique sensor identifier |
| `tenant_id` | TenantId | Yes | Tenant this sensor belongs to |
| `agent_id` | AgentId? | No | Agent this sensor is for. Null means global. |
| `source_config` | SourceConfigRef | Yes | Source configuration reference |
| `signal_schemas` | SignalSchema[] | Yes | Schemas for signals emitted by this sensor |
| `grants` | Grant[] | Yes | Grants for this sensor |
| `lifecycle` | SensorLifecycle | Yes | Sensor lifecycle configuration |
| `checkpoint` | SensorCheckpoint? | No | Last processed event checkpoint |

> **Normative definition.**
The `agent_id` field is optional.
If null, the sensor emits signals to all agents in the tenant.
If present, the sensor emits signals only to the specified agent.

> **Normative definition.**
The `signal_schemas` field defines the signal schemas that this sensor
can emit.
The host MUST validate emitted signals against these schemas.

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
| `jitter_ms` | u64? | No | Random jitter in milliseconds |
| `next_fire_calculation` | NextFireCalculation | Yes | How to calculate next fire time |

> **Normative definition.**
The `expression` field uses a cron-like syntax: `minute hour day-of-month month day-of-week`.
The host MUST validate the expression syntax.
Invalid expressions MUST be rejected with `schedule.expression.invalid`.

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
If present, the host MUST add a random jitter between 0 and `jitter_ms`
to the scheduled fire time.
The jitter MUST be deterministic for a given schedule expression and fire time.

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

## 3.2 Behavior And Integration

### Signal admission boundary

> **Normative definition.**
The host MUST normalize sensor events, timer fires, user requests, and
transport deliveries through one signal admission boundary.

> **Normative definition.**
The signal admission boundary performs the following steps:

1. **Source authentication**: Authenticate the event source.
2. **Tenant/agent resolution**: Resolve the tenant and agent for the event.
3. **Schema validation**: Validate the event against the expected schema.
4. **Deduplication**: Detect and reject duplicate events.
5. **Mailbox admission**: Admit the event to the mailbox.

> **Normative definition.**
If any step fails, the host MUST reject the event with the appropriate diagnostic.
The host MUST NOT admit invalid events to the mailbox.

### Source authentication

> **Normative definition.**
The host MUST authenticate event sources using the following mechanisms:

1. **API key**: Authenticate using an API key.
2. **OAuth 2.0**: Authenticate using OAuth 2.0 tokens.
3. **mTLS**: Authenticate using mutual TLS.
4. **Custom**: Authenticate using a custom mechanism.

> **Normative definition.**
The host MUST document the authentication mechanism for each source in
the conformance profile.

> **Normative definition.**
The host MUST reject unauthenticated sources with `signal.ingress.unauthenticated`.

### Tenant/agent resolution

> **Normative definition.**
The host MUST resolve the tenant and agent for each event using the following mechanisms:

1. **Tenant header**: Resolve the tenant from the `X-Tenant-ID` header.
2. **Agent header**: Resolve the agent from the `X-Agent-ID` header.
3. **Sensor resolution**: Resolve the agent from the sensor descriptor.
4. **Timer resolution**: Resolve the agent from the timer directive.

> **Normative definition.**
The host MUST reject events with missing or invalid tenant/agent resolution
with `signal.ingress.resolution_failed`.

### Schema validation

> **Normative definition.**
The host MUST validate events against the expected schema using the following mechanisms:

1. **JSON Schema**: Validate against a JSON Schema.
2. **Custom schema**: Validate against a custom schema.

> **Normative definition.**
The host MUST reject events that fail schema validation with `signal.ingress.schema_invalid`.

### Deduplication

> **Normative definition.**
The host MUST detect and reject duplicate events using the following mechanisms:

1. **Event ID**: Reject events with duplicate event IDs.
2. **Event signature**: Reject events with duplicate signatures.

> **Normative definition.**
The host MUST reject duplicate events with `signal.ingress.duplicate`.

### Mailbox admission

> **Normative definition.**
The host MUST admit events to the mailbox using the following mechanisms:

1. **Priority class**: Assign a priority class to the event.
2. **Mailbox bounds**: Enforce mailbox bounds on the event.
3. **Overload policy**: Apply the overload policy when bounds are reached.

> **Normative definition.**
The host MUST admit events to the mailbox with the appropriate priority class.
The host MUST enforce mailbox bounds on all events.

### Signal outcomes

> **Normative definition.**
The host MUST handle the following signal outcomes:

1. **Skipped**: The signal was skipped due to misfire policy.
2. **Coalesced**: The signal was coalesced with another signal.
3. **Replayed**: The signal was replayed from a checkpoint.
4. **Late**: The signal arrived after its deadline.
5. **Duplicate**: The signal was rejected as a duplicate.
6. **Disabled**: The sensor was disabled.
7. **Failed source**: The source failed to emit the signal.

> **Normative definition.**

```
SignalOutcome {
  kind: OutcomeKind,
  message: String,
  diagnostic_code: String
}

OutcomeKind {
  Skipped,
  Coalesced,
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
| `Coalesced` | Signal coalesced | Overload policy is coalesce | `signal.ingress.coalesced` |
| `Replayed` | Signal replayed | Sensor checkpoint replay | `signal.ingress.replayed` |
| `Late` | Signal late | Signal arrived after deadline | `signal.ingress.late` |
| `Duplicate` | Signal duplicate | Duplicate event detected | `signal.ingress.duplicate` |
| `Disabled` | Sensor disabled | Sensor is disabled | `signal.ingress.disabled` |
| `FailedSource` | Source failed | Source failed to emit signal | `signal.ingress.failed_source` |

## 3.3 Failure Evidence And Operational Notes

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
| `signal.ingress` | Signal ingress failures | `malformed`, `incompatible`, `unauthorized`, `unavailable`, `unauthenticated`, `resolution_failed`, `schema_invalid`, `skipped`, `coalesced`, `replayed`, `late`, `duplicate`, `disabled`, `failed_source` |
| `sensor` | Sensor failures | `capacity.exhausted` |
| `timer` | Timer failures | `duplicate` |
| `schedule` | Schedule failures | `expression.invalid`, `timezone.invalid` |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Source authentication mechanism**: The host MAY choose the source authentication mechanism. The mechanism MUST be documented in the conformance profile.

2. **Deduplication window**: The host MAY choose the deduplication window. The window MUST be documented in the conformance profile.

3. **Jitter determinism**: The host MAY choose how to make jitter deterministic. The method MUST be documented in the conformance profile.

4. **Schedule expression syntax**: The host MAY choose the schedule expression syntax. The syntax MUST be documented in the conformance profile.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Sensor replication**: A formal sensor replication strategy will be implemented in future milestones. The protocol is language-neutral and does not require sensor replication for base conformance.

2. **Multi-tenant signal isolation**: Enhanced multi-tenant signal isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

3. **Timer persistence**: A formal timer persistence mechanism will be implemented in future milestones. The protocol is language-neutral and does not require timer persistence for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 3.4 Phase 4 Integration Tests

### Canonical successful flow

> **Normative conformance criterion.**
The canonical successful flow integration test validates that a valid sensor
event is processed successfully through the full signal ingress pipeline.

Expected behavior:

- Input: valid sensor event with authenticated source, resolved tenant/agent, and valid schema.
- Expected output: SignalEnvelope admitted to mailbox.
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

- Input: event with duplicate event ID.
- Expected output: null.
- Expected error: `signal.ingress.duplicate`.

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

| Clause | Type | Selection |
|--------|------|-----------|
| Sensor descriptor structure | Required | Fields fixed by this chapter |
| Schedule expression structure | Required | Fields fixed by this chapter |
| Durable timer structure | Required | Fields fixed by this chapter |
| Signal admission boundary | Required | 5 steps fixed by this chapter |
| Source authentication | Implementation-defined | Documented in conformance profile |
| Deduplication window | Implementation-defined | Documented in conformance profile |
| Jitter determinism | Implementation-defined | Documented in conformance profile |
| Schedule expression syntax | Implementation-defined | Documented in conformance profile |

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
