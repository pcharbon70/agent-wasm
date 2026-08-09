---
title: "Retry Timer Recovery Replay Hibernate And Migration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-04
  - durable-state
  - retry
  - timer
  - recovery
  - replay
  - hibernate
  - migration
aliases:
  - "M4-P4 Retry Timer Recovery Replay Hibernate And Migration"
---

# Retry Timer Recovery Replay Hibernate And Migration

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-04-retry-timer-recovery-replay-hibernate-and-migration.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It makes delayed work, runtime deactivation, state reconstruction, and schema
evolution explicit durable operations.

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
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

## 4.1 Contract And Data Model

### Retry classification

> **Normative definition.**
A retry is a durable operation that re-attempts a failed directive dispatch
after a bounded number of attempts with exponential backoff and jitter.
The host MUST classify retries into the following categories:

1. **Transient**: The failure is likely to resolve on retry (e.g., network error).
2. **Permanent**: The failure will not resolve on retry (e.g., invalid payload).
3. **Operator-intervention**: The failure requires human intervention (e.g.,
   approval timeout).

> **Normative definition.**

```
RetryRecord {
  attempt_id: AttemptId,
  tenant_id: TenantId,
  agent_id: AgentId,
  retry_number: u32,
  max_retries: u32,
  backoff_ms: u64,
  jitter_ms: u64,
  next_retry_at: UnixTimestamp,
  deadline: UnixTimestamp?,
  classification: RetryClassification,
  state: RetryState,
  metadata: JsonObject
}

RetryClassification = Transient | Permanent | OperatorIntervention
RetryState = Pending | InProgress | Completed | Expired | TerminalFailed
```

`AttemptId`, `TenantId`, and `AgentId` are defined in
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `attempt_id` | AttemptId | Yes | Attempt this retry is for |
| `tenant_id` | TenantId | Yes | Tenant this retry belongs to |
| `agent_id` | AgentId | Yes | Agent this retry belongs to |
| `retry_number` | u32 | Yes | Current retry number (starts at 1) |
| `max_retries` | u32 | Yes | Maximum number of retries |
| `backoff_ms` | u64 | Yes | Base backoff duration in milliseconds |
| `jitter_ms` | u64 | Yes | Additional random jitter in milliseconds |
| `next_retry_at` | UnixTimestamp | Yes | Next retry time |
| `deadline` | UnixTimestamp? | No | Deadline for all retries (null if no deadline) |
| `classification` | RetryClassification | Yes | Retry classification |
| `state` | RetryState | Yes | Current retry state |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `retry_number` field is incremented on each retry attempt.
The host MUST NOT allow `retry_number` to exceed `max_retries`.
If `retry_number` exceeds `max_retries`, the host MUST mark the retry as
`TerminalFailed` with `retry.max_retries_exceeded`.

> **Normative definition.**
The `next_retry_at` field is computed as
`current_time + backoff_ms * 2^retry_number + random(jitter_ms)`.
The host MUST use the computed `next_retry_at` for scheduling retries.

> **Normative definition.**
The `deadline` field is optional.
If set, the host MUST mark all pending retries for the attempt as `Expired`
with `retry.deadline_exceeded` when the deadline passes.

### Timer persistence

> **Normative definition.**
A timer is a durable record of a delayed signal that the host must fire at a
specific time.
The host MUST persist timers independently of live schedulers.
If the host crashes, the host MUST recover timers from the durable store on
restart.

> **Normative definition.**

```
TimerRecord {
  timer_id: TimerId,
  tenant_id: TenantId,
  agent_id: AgentId,
  signal: SignalEnvelope,
  fire_at: UnixTimestamp,
  repeat_interval: u64?,
  repeat_count: u32?,
  state: TimerState,
  metadata: JsonObject
}

TimerId = string
SignalEnvelope = Defined in [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
TimerState = Pending | Fired | Cancelled | Expired
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `timer_id` | TimerId | Yes | Unique timer identifier |
| `tenant_id` | TenantId | Yes | Tenant this timer belongs to |
| `agent_id` | AgentId | Yes | Agent this timer belongs to |
| `signal` | SignalEnvelope | Yes | Signal to fire |
| `fire_at` | UnixTimestamp | Yes | Time to fire the timer |
| `repeat_interval` | u64? | No | Repeat interval in milliseconds (null if one-shot) |
| `repeat_count` | u32? | No | Number of repeats (null if unlimited) |
| `state` | TimerState | Yes | Current timer state |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST persist timers atomically with the commit unit that created them.
If a commit unit is rolled back, the host MUST delete the corresponding timers.

> **Normative definition.**
The host MUST recover timers from the durable store on restart.
The host MUST fire timers that have not yet fired and have not expired.
The host MUST mark timers that have expired as `Expired` with `timer.expired`.

### Missed-fire policy

> **Normative definition.**
The host MUST define a missed-fire policy for timers that fail to fire at the
scheduled time.
The host MUST support the following missed-fire policies:

1. **Fire immediately**: Fire the timer as soon as possible after the host
   restarts.
2. **Skip**: Skip the timer and do not fire it.
3. **Retry**: Retry the timer according to the retry policy.

> **Normative definition.**
The missed-fire policy is configured per timer and is stored in the `metadata`
field of the `TimerRecord`.

### Replay

> **Normative definition.**
Replay is the process of reconstructing agent state from the journal and
snapshots.
The host MUST support replay from the journal/checkpoint with artifact, schema,
policy, and nondeterministic-result references.

> **Normative definition.**

```
ReplayRecord {
  replay_id: ReplayId,
  tenant_id: TenantId,
  agent_id: AgentId,
  start_revision: u64,
  end_revision: u64,
  artifact_version: string,
  state_schema_version: string,
  policy_version: string,
  state: ReplayState,
  nondeterministic_results: NondeterministicResult[],
  metadata: JsonObject
}

ReplayId = string
ReplayState = Pending | InProgress | Completed | Failed
NondeterministicResult {
  revision: u64,
  result_hash: Bytes,
  reference: String?
}
```

`TenantId`, `AgentId`, and `u64` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `replay_id` | ReplayId | Yes | Unique replay identifier |
| `tenant_id` | TenantId | Yes | Tenant this replay belongs to |
| `agent_id` | AgentId | Yes | Agent this replay belongs to |
| `start_revision` | u64 | Yes | Start revision for the replay |
| `end_revision` | u64 | Yes | End revision for the replay |
| `artifact_version` | string | Yes | Artifact version used for the replay |
| `state_schema_version` | string | Yes | State schema version used for the replay |
| `policy_version` | string | Yes | Policy version used for the replay |
| `state` | ReplayState | Yes | Current replay state |
| `nondeterministic_results` | NondeterministicResult[] | Yes | Nondeterministic results from the replay |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The host MUST replay the journal from `start_revision` to `end_revision`.
The host MUST reconstruct the agent state at `end_revision`.
The host MUST verify the reconstructed state matches the snapshot at
`end_revision` (if available).

> **Normative definition.**
The `nondeterministic_results` field records results that are nondeterministic
(e.g., random numbers, timestamps).
The host MUST reference the original nondeterministic results for replay
consistency.
