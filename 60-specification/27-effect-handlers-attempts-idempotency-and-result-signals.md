---
title: "Effect Handlers Attempts Idempotency And Result Signals"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-03
  - durable-state
  - effect-handler
  - attempt
  - idempotency
  - result-signal
aliases:
  - "M4-P3 Effect Handlers Attempts Idempotency And Result Signals"
---

# Effect Handlers Attempts Idempotency And Result Signals

## Status and authority

This chapter is a normative specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-03-effect-handlers-attempts-idempotency-and-result-signals.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It interprets committed directives through typed handlers while retaining every
attempt and returning results as new signals.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
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
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

## 3.1 Contract And Data Model

### Effect handler registration

> **Normative definition.**
An effect handler is a typed component that interprets a specific directive kind
and dispatches to an external target.
The host MUST register effect handlers by directive kind, schema version, trust
class, capability, and retry policy.

> **Normative definition.**

```
EffectHandlerRegistration {
  handler_id: HandlerId,
  directive_kind: DirectiveKindName,
  schema_version: string,
  trust_class: TrustClass,
  capability: HandlerCapability,
  retry_policy: RetryPolicy
}

HandlerId = string
TrustClass = Untrusted | Confined | Privileged
HandlerCapability {
  effects: Set<EffectKind>,
  signals: Set<SignalKind>,
  timers: Set<TimerKind>,
  child_lifecycle: ChildLifecyclePermission
}
ChildLifecyclePermission = None | Suspend | Cancel | Terminate
```

`DirectiveKindName` is defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).
`RetryPolicy` is defined in
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md).
`SignalKind`, `EffectKind`, and `TimerKind` are defined in
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `handler_id` | HandlerId | Yes | Unique handler identifier |
| `directive_kind` | DirectiveKindName | Yes | Directive kind this handler interprets |
| `schema_version` | string | Yes | Schema version for payload validation |
| `trust_class` | TrustClass | Yes | Trust class for the handler |
| `capability` | HandlerCapability | Yes | Capabilities granted to the handler |
| `retry_policy` | RetryPolicy | Yes | Retry policy for this handler |

> **Normative definition.**
The `trust_class` field determines the handler's trust level:
- **Untrusted**: Handler runs in a sandbox with no external access.
- **Confined**: Handler runs in a sandbox with limited external access.
- **Privileged**: Handler runs with full external access.

> **Normative definition.**
The `capability` field determines what the handler can do:
- `effects`: Set of effect kinds the handler can dispatch.
- `signals`: Set of signal kinds the handler can emit.
- `timers`: Set of timer kinds the handler can create.
- `child_lifecycle`: Permission to suspend, cancel, or terminate child agents.

> **Normative definition.**
The host MUST validate the handler's trust class and capability against the
agent's manifest before dispatching.
If the handler exceeds its trust class or capability, the host MUST reject the
dispatch with `handler.trust_violation`.

### Effect attempt

> **Normative definition.**
An effect attempt is a durable record of a single dispatch attempt for an
effect handler.
The host MUST retain every attempt for audit purposes.

> **Normative definition.**

```
EffectAttempt {
  attempt_id: AttemptId,
  tenant_id: TenantId,
  agent_id: AgentId,
  outbox_entry_id: EntryId,
  directive_id: DirectiveId,
  handler_id: HandlerId,
  lease: AttemptLease,
  handler_version: string,
  request_hash: Bytes,
  created_at: UnixTimestamp,
  dispatched_at: UnixTimestamp?,
  completed_at: UnixTimestamp?,
  outcome: AttemptOutcome,
  external_reference: String?,
  metadata: JsonObject
}

AttemptId = string
AttemptLease {
  lease_id: String,
  acquired_at: UnixTimestamp,
  expires_at: UnixTimestamp
}
AttemptOutcome {
  status: AttemptStatus,
  result: AttemptResult?
}
AttemptStatus = Pending | Dispatched | Completed | Failed | Cancelled
AttemptResult {
  status: DispatchStatus,
  response_hash: Bytes?,
  diagnostics: Diagnostics?
}
DispatchStatus = Success | DomainFailure | InfrastructureFailure | Timeout
Diagnostics {
  kind: DiagnosticsKind,
  message: String,
  code: String
}
DiagnosticsKind = Internal | External
```

`EntryId` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`DirectiveId` is defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).
`TenantId` and `AgentId` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `attempt_id` | AttemptId | Yes | Unique attempt identifier |
| `tenant_id` | TenantId | Yes | Tenant this attempt belongs to |
| `agent_id` | AgentId | Yes | Agent this attempt belongs to |
| `outbox_entry_id` | EntryId | Yes | Outbox entry this attempt is for |
| `directive_id` | DirectiveId | Yes | Directive this attempt is for |
| `handler_id` | HandlerId | Yes | Handler this attempt is dispatched to |
| `lease` | AttemptLease | Yes | Lease for this attempt |
| `handler_version` | string | Yes | Handler version used for this attempt |
| `request_hash` | Bytes | Yes | Hash of the dispatch request |
| `created_at` | UnixTimestamp | Yes | Attempt creation time |
| `dispatched_at` | UnixTimestamp? | No | Dispatch time (null if not yet dispatched) |
| `completed_at` | UnixTimestamp? | No | Completion time (null if not yet completed) |
| `outcome` | AttemptOutcome | Yes | Attempt outcome |
| `external_reference` | String? | No | External provider reference (if any) |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `lease` field is used to prevent concurrent dispatch of the same attempt.
The host MUST acquire a lease before dispatching an attempt.
If the lease expires, the host MUST mark the attempt as `Failed` with
`attempt.lease_expired` and MUST NOT dispatch it again until a new lease is
acquired.

> **Normative definition.**
The `request_hash` field is a hash of the dispatch request (e.g., SHA-256).
The host MUST compute the request hash before dispatching the attempt.
The host MUST verify the request hash on every retry to prevent request
mutation.

> **Normative definition.**
The `external_reference` field is set by the external provider when the
dispatch succeeds.
The host MUST store the external reference for audit purposes.

### Stable idempotency keys

> **Normative definition.**
The host MUST support stable idempotency keys to prevent duplicate dispatch
to external providers.
Idempotency keys are separate from attempt and external provider identities.

> **Normative definition.**

```
IdempotencyKey {
  key: String,
  scope: IdempotencyScope,
  expires_at: UnixTimestamp?
}

IdempotencyScope = Tenant | Agent | Directive | Global
```

> **Normative definition.**
The `scope` field determines the scope of the idempotency key:
- **Tenant**: The key is unique per tenant.
- **Agent**: The key is unique per agent within a tenant.
- **Directive**: The key is unique per directive within an agent.
- **Global**: The key is unique across all tenants and agents.

> **Normative definition.**
The host MUST check the idempotency key before dispatching an attempt.
If the key has already been used, the host MUST return the previous result
without dispatching again.
If the key has expired, the host MUST reject the attempt with
`handler.idempotency_key_expired`.

> **Normative definition.**
The host MUST NOT use the `attempt_id` or `external_reference` as the
idempotency key.
The idempotency key is determined by the directive payload and MUST be
deterministic for the same payload.

## 3.2 Behavior And Integration

### Pre-dispatch validation

> **Normative definition.**
The host MUST validate the handler policy and payload immediately before
dispatching an attempt.
The host MUST NOT dispatch attempts that fail pre-dispatch validation.

> **Normative definition.**
Pre-dispatch validation includes:
1. **Handler registration**: The handler is registered and active.
2. **Trust class**: The handler's trust class is sufficient for the dispatch.
3. **Capability**: The handler has the required capability for the dispatch.
4. **Schema version**: The payload matches the handler's schema version.
5. **Idempotency key**: The idempotency key has not expired or been used.
6. **Payload bounds**: The payload is within the size limit.

> **Normative definition.**
The host MUST bound the response bytes, duration, and diagnostics for each
dispatch:
- **Response bytes**: The response MUST NOT exceed `handler.response_bytes_limit`
  bytes.
- **Duration**: The dispatch MUST NOT exceed `handler.duration_limit`
  milliseconds.
- **Diagnostics**: The diagnostics MUST be bounded to `handler.diagnostics_limit`
  bytes.

> **Normative definition.**
If pre-dispatch validation fails, the host MUST reject the attempt with the
appropriate error code:
- `handler.not_registered`: Handler is not registered.
- `handler.trust_violation`: Handler trust class is insufficient.
- `handler.capability_violation`: Handler lacks required capability.
- `handler.schema_mismatch`: Payload schema version does not match.
- `handler.idempotency_key_expired`: Idempotency key has expired.
- `handler.payload_too_large`: Payload exceeds size limit.
- `handler.response_too_large`: Response exceeds byte limit.
- `handler.duration_exceeded`: Dispatch exceeded duration limit.
- `handler.diagnostics_too_large`: Diagnostics exceed byte limit.

### Outcome translation

> **Normative definition.**
The host MUST translate effect handler outcomes into causally linked result
signals for the agent turn.

> **Normative definition.**
The host MUST translate the following outcomes:

1. **Success**: The external provider returned successfully. The host MUST
   create a result signal with `signal.type = effect_result` and
   `signal.data` containing the provider's response.
2. **Domain failure**: The external provider returned a domain error. The host
   MUST create a result signal with `signal.type = effect_result` and
   `signal.data` containing the error details.
3. **Infrastructure failure**: The external provider is unavailable or
   encountered an infrastructure error. The host MUST create a result signal
   with `signal.type = infrastructure_failure` and `signal.data` containing
   the error details.
4. **Timeout**: The external provider did not respond within the duration
   limit. The host MUST create a result signal with `signal.type = timeout`
   and `signal.data` containing the timeout details.
5. **Cancellation**: The turn was cancelled before the dispatch completed.
   The host MUST create a result signal with `signal.type = cancellation`
   and `signal.data` containing the cancellation details.
6. **Approval**: The directive requires user approval. The host MUST create a
   result signal with `signal.type = approval_required` and `signal.data`
   containing the approval request details.

> **Normative definition.**
Each result signal MUST set the following causality fields from
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md):
- `signal.correlation_id`: Set to the attempt ID to group all attempts for the
  same directive.
- `signal.causation_id`: Set to the turn ID that produced the result signal.

### Failure behavior

> **Normative definition.**
The host MUST define the following failure behavior for effect handlers:

1. **Handler crash**: If the handler crashes during dispatch, the host MUST
   mark the attempt as `Failed` with `attempt.handler_crashed` and MUST
   retry the attempt according to the retry policy.
2. **Lease expiry**: If the attempt lease expires during dispatch, the host
   MUST mark the attempt as `Failed` with `attempt.lease_expired` and MUST
   retry the attempt according to the retry policy.
3. **Late response**: If the external provider responds after the attempt is
   marked as `Failed`, the host MUST discard the response and MUST NOT
   update the attempt outcome.
4. **Duplicate response**: If the external provider responds multiple times
   for the same attempt, the host MUST discard all responses after the first
   and MUST NOT update the attempt outcome multiple times.
5. **Conflicting replay**: If a replayed attempt produces a different result
   than the original attempt, the host MUST mark the replayed attempt as
   `Failed` with `attempt.conflicting_replay` and MUST log the conflict for
   audit purposes.
6. **Unsupported idempotency**: If the external provider does not support
   idempotency keys, the host MUST log a warning and MUST dispatch the
   attempt without idempotency protection.

> **Normative definition.**
The host MUST retry failed attempts according to the `RetryPolicy` defined in
the effect handler registration.
The `RetryPolicy` type is defined in
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md)
and includes:
- `max_attempts`: The maximum number of dispatch attempts (including the
  original).
- `backoff_ms`: The base backoff duration in milliseconds.
- `jitter_ms`: Optional shared-schema field that MUST be absent or zero for an
  effect-handler retry policy.

> **Normative definition.**
An effect-handler `RetryPolicy` MUST conform to the fixed directive retry
semantics in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md#fixed-directive-and-strategy-policy):
`max_attempts` is at least 1 and counts the initial attempt, `backoff_ms` is the
exact constant delay before every subsequent attempt, and `jitter_ms` is absent
or zero. A policy requesting exponential or linear growth, non-zero jitter, or
another delay transformation MUST be rejected with `handler.retry_policy_invalid`
before the handler registration becomes active.

## 3.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for effect handlers
attempts idempotency and result signals:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current schema version or
   handler version.
3. **Conflicting**: Multiple writers attempt to write to the same attempt
   (optimistic concurrency conflict).
4. **Unauthorized**: The caller does not have permission to perform the operation.
5. **Exhausted**: The system is out of resources (e.g., storage capacity, retry
   budget).
6. **Unavailable**: The storage backend is unavailable.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for effect handlers attempts
idempotency and result signals:

| Error Code | Description |
|------------|-------------|
| `handler.not_registered` | Handler is not registered |
| `handler.trust_violation` | Handler trust class is insufficient |
| `handler.capability_violation` | Handler lacks required capability |
| `handler.schema_mismatch` | Payload schema version does not match |
| `handler.idempotency_key_expired` | Idempotency key has expired |
| `handler.payload_too_large` | Payload exceeds size limit |
| `handler.response_too_large` | Response exceeds byte limit |
| `handler.duration_exceeded` | Dispatch exceeded duration limit |
| `handler.diagnostics_too_large` | Diagnostics exceed byte limit |
| `handler.retry_policy_invalid` | Retry policy requests an invalid attempt count, delay transformation, or non-zero jitter |
| `attempt.handler_crashed` | Handler crashed during dispatch |
| `attempt.lease_expired` | Attempt lease expired |
| `attempt.conflicting_replay` | Replayed attempt produced different result |
| `attempt.max_retries_exceeded` | Maximum retry attempts exceeded |
| `commit.conflict` | Optimistic concurrency conflict (see [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)) |
| `storage.snapshot.duplicate` | Snapshot ID already exists (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.unavailable` | Storage backend unavailable (see [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome using exactly
the Chapter 04 `Diagnostic` top-level structure. The domain error is `code`,
`severity` is `error`, and `details` contains `phase`, `contract`, `profile`,
`failed_boundary`, `context`, `entity_identifiers`, `timestamp`, and
`retryable`.

| Family | Domain codes |
|--------|--------------|
| `identity.validation.effect_handler` | `handler.schema_mismatch`, `handler.retry_policy_invalid` |
| `identity.authorization.effect_handler` | `handler.trust_violation`, `handler.capability_violation` |
| `identity.conflict.effect_handler` | `attempt.conflicting_replay`, `commit.conflict`, `storage.snapshot.duplicate` |
| `identity.limit.effect_handler` | `handler.idempotency_key_expired`, `handler.payload_too_large`, `handler.response_too_large`, `handler.duration_exceeded`, `handler.diagnostics_too_large`, `attempt.max_retries_exceeded` |
| `identity.effect.effect_handler` | `handler.not_registered`, `attempt.handler_crashed`, `attempt.lease_expired` |
| `identity.storage.effect_handler` | `storage.unavailable` |

No additional top-level diagnostic member is permitted.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:
Each selection is one of the alternatives or finite positive limit domains
stated below. Observable response-limit rejections and dispatch timeout timing
may differ according to the recorded selections; handler results and durable
effect semantics MUST NOT differ.

1. **Handler registry**: An in-memory registry backed by a durable snapshot or a
   transactional database registry.
2. **Idempotency key storage**: A transactional database table or an
   append-only durable key log.
3. **Response size limit**: The default response size limit for effect
   handlers.
4. **Duration limit**: The default duration limit for effect handler
   dispatches.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Handler versioning**: The handler versioning strategy (canary, blue-green,
   etc.).
2. **Handler hot-reload**: The handler hot-reload strategy.
3. **Effect handler metrics**: The effect handler metrics and monitoring.
4. **Effect handler tracing**: The effect handler tracing and debugging.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 3 MAY invalidate earlier milestone assumptions:

1. **Handler registry**: If the handler registry implementation exceeds the
   capacity planned in earlier milestones, the capacity plan MUST be revised.
2. **Retry policy**: If the retry policy exceeds the turn timeout, the timeout
   or retry policy MUST be revised.
3. **Idempotency key storage**: If the idempotency key storage exceeds the
   capacity planned in earlier milestones, the capacity plan MUST be revised.

> **Non-normative note.**
If any result from Phase 3 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## Variability register

The register below indexes profile selections and other variability governed by
the linked clauses. It does not independently license variation.

> **Non-normative note.**

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| [Handler registry implementation](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must support hot-reload |
| [Retry policy](#failure-behavior) | Required | Explicit `max_attempts`, constant `backoff_ms`, and absent or zero `jitter_ms` | Must not exceed the turn timeout |
| [Idempotency key storage](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must support tenant/agent/directive/global scopes |
| [Response size limit](#pre-dispatch-validation) | Implementation-defined | Document in conformance profile | Must be bounded |
| [Duration limit](#pre-dispatch-validation) | Implementation-defined | Document in conformance profile | Must be bounded |
| [Backoff strategy](#failure-behavior) | Required | Exact constant `backoff_ms` | No growth algorithm or non-zero jitter |
| [Handler trust classes](#effect-handler-registration) | Required | Use the closed trust-class set | Must enforce trust boundaries |

## 3.4 Phase 3 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 3 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host dispatches effect handlers, retains
   every attempt, and returns results as new signals.
2. **Failure handling**: The host handles malformed, incompatible, stale,
   duplicate, and boundary-limit inputs correctly.
3. **Transient failure recovery**: The host recovers from timeout, cancellation,
   unavailable dependency, and retry behavior without leaving unauthorized or
   partial state.
4. **Cross-milestone compatibility**: The phase does not introduce regressions
   in earlier milestones.

> **Normative definition.**
Each integration test MUST exercise observable contracts rather than private
implementation structure.

### Successful flow tests

> **Normative definition.**
The following tests MUST verify the canonical successful flow:

1. **Handler registration**: Register an effect handler and verify it is
   registered correctly.
2. **Attempt creation**: Create an effect attempt and verify it is created
   correctly.
3. **Pre-dispatch validation**: Validate the handler policy and payload before
   dispatch and verify the validation passes.
4. **Dispatch**: Dispatch the effect handler and verify the attempt state
   transitions from `Pending` to `Dispatched` to `Completed`.
5. **Result signal creation**: Create a result signal for the successful
   dispatch and verify the signal is causally linked.
6. **Idempotency key check**: Check the idempotency key before dispatch and
   verify the key has not been used.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Handler not registered**: Attempt to dispatch an unregistered handler and
   verify the `handler.not_registered` error code.
2. **Trust violation**: Attempt to dispatch a handler with insufficient trust
   class and verify the `handler.trust_violation` error code.
3. **Capability violation**: Attempt to dispatch a handler with insufficient
   capability and verify the `handler.capability_violation` error code.
4. **Schema mismatch**: Attempt to dispatch a handler with a mismatched schema
   version and verify the `handler.schema_mismatch` error code.
5. **Idempotency key expired**: Attempt to dispatch with an expired idempotency
   key and verify the `handler.idempotency_key_expired` error code.
6. **Payload too large**: Attempt to dispatch with a payload that exceeds the
   size limit and verify the `handler.payload_too_large` error code.
7. **Response too large**: Simulate a response that exceeds the byte limit and
   verify the `handler.response_too_large` error code.
8. **Duration exceeded**: Simulate a dispatch that exceeds the duration limit
   and verify the `handler.duration_exceeded` error code.
9. **Invalid retry policy**: Register a handler with non-zero jitter or a delay
   growth algorithm and verify `handler.retry_policy_invalid` and that the
   registration does not become active.

> **Normative definition.**
Each test MUST verify the exact Chapter 04 diagnostic shape, assigned family,
domain `code`, `severity: "error"`, message, and required bounded details.

### Transient failure recovery tests

> **Normative definition.**
The following tests MUST verify transient failure recovery:

1. **Handler crash**: Simulate a handler crash during dispatch and verify the
   attempt is marked as `Failed` with `attempt.handler_crashed` and the attempt
   is retried.
2. **Lease expiry**: Simulate a lease expiry during dispatch and verify the
   attempt is marked as `Failed` with `attempt.lease_expired` and the attempt
   is retried.
3. **Late response**: Simulate a late response from the external provider and
   verify the response is discarded.
4. **Duplicate response**: Simulate a duplicate response from the external
   provider and verify all responses after the first are discarded.
5. **Conflicting replay**: Simulate a conflicting replay and verify the
   replayed attempt is marked as `Failed` with `attempt.conflicting_replay`.
6. **Max retries exceeded**: Simulate exceeding the maximum retry attempts and
   verify the attempt is marked as `Failed` with `attempt.max_retries_exceeded`.
7. **Constant retry delay**: Fail at least three attempts and verify every
   subsequent dispatch starts after exactly the registered `backoff_ms`, with
   no exponential growth and no jitter, including across host recovery.

> **Normative definition.**
Each test MUST verify that no unauthorized or partial state is left after the
failure.

### Cross-milestone compatibility tests

> **Normative definition.**
The following tests MUST verify cross-milestone compatibility:

1. **Milestone 1 fixtures**: Run all Milestone 1 fixtures and verify no
   regressions. Milestone 1 fixtures are defined in
   [Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md).
2. **Milestone 2 fixtures**: Run all Milestone 2 fixtures and verify no
   regressions. Milestone 2 fixtures are defined in the Phase 1-5 plans under
   [Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/).
3. **Milestone 3 fixtures**: Run all Milestone 3 fixtures and verify no
   regressions. Milestone 3 fixtures are defined in the Phase 1-5 plans under
   [Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/).

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 3 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Handler registration evidence**: Evidence that effect handlers are
   registered correctly.
3. **Attempt retention evidence**: Evidence that every attempt is retained for
   audit purposes.
4. **Result signal evidence**: Evidence that results are returned as new
   signals with correct causality metadata.
5. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
6. **Recovery evidence**: Evidence that transient failures are recovered from
   correctly.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.
