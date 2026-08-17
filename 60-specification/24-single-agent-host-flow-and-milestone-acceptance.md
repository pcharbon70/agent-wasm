---
title: "Single-Agent Host Flow And Milestone Acceptance"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-03
  - phase-05
  - host-flow
  - acceptance
  - single-agent
aliases:
  - "M3-P5 Single-Agent Host Flow And Milestone Acceptance"
---

# Single-Agent Host Flow And Milestone Acceptance

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/phase-05-single-agent-host-flow-and-milestone-acceptance.md)
of
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
--
Host Actor Runtime And Lifecycle.
It connects admission, mailbox, activation, Extism invocation, validation,
lifecycle, and observable results in one single-node runtime.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
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
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

## 5.1 Contract And Data Model

### Reference host flow

> **Normative definition.**
The host MUST implement the following reference flow from authenticated
submission through accepted-record routing, lease, snapshot load, reducer
call, result validation, atomic commit, and asynchronous effect scheduling:

1. **Signal admission**: Run Chapter 10's complete submission evaluation,
   atomically persist `AcceptedSignalEnvelope` and selector state, and enqueue
   a mailbox reference for the recorded target.
2. **Mailbox dequeue**: Dequeue the accepted-record reference under Chapter
   21's fixed priority schedule.
3. **Lease acquisition**: Acquire the recorded target agent's turn lease.
4. **Snapshot and request load**: Load the current state and strategy snapshot,
   then project and validate the accepted record as one `TurnRequest`.
5. **Reducer invocation**: Invoke `reduce` exactly once with the projected
   signal, snapshots, grants, and effective limits.
6. **Result validation**: Validate canonical output, expected revision, patch,
   strategy snapshot, every directive, and diagnostics.
7. **Atomic commit**: Commit the next state revision, journal facts, strategy
   snapshot, and all validated directive outbox entries as one unit.
8. **Turn completion**: Release the turn lease, record the delivery outcome,
   and publish the successful `TurnResult` to the caller.
9. **Asynchronous directive drain**: Schedule and execute committed outbox
   entries after turn completion. The turn caller MUST NOT wait for this step.

> **Normative definition.**
Failure before or during step 7 MUST publish no state revision, journal fact,
strategy snapshot, or outbox entry; if a lease was acquired, the host MUST
release it. Atomic-commit failure leaves the prior revision current. Failure
to release a lease after commit MUST be recorded and fenced, but MUST NOT undo
the commit or suppress the committed `TurnResult`; its lease diagnostic is
host-owned evidence rather than a mutation of deterministic reducer output. A
step 9 effect failure follows the directive retry and completion contract and
MUST NOT alter the committed turn or `TurnResult`.

### Host flow invariants

> **Normative definition.**
The host MUST enforce the following invariants:

1. **No state change after trap**: The host MUST NOT apply state changes after a reducer trap.
2. **No state change after timeout**: The host MUST NOT apply state changes after a reducer timeout.
3. **No state change after cancellation**: The host MUST NOT apply state changes after a reducer cancellation.
4. **No state change after invalid output**: The host MUST NOT apply state changes after invalid reducer output.
5. **No state change after stale revision**: The host MUST NOT apply state changes after a stale revision.
6. **No state change after policy rejection**: The host MUST NOT apply state changes after a policy rejection.

> **Normative definition.**
The host MUST return the appropriate diagnostic for each invariant violation.

### Representative flows

> **Normative definition.**
The host MUST support the following representative flows:

1. **Direct action**: Execute a single action and return the result.
2. **FSM waiting/resume**: Wait for a signal and resume when received.
3. **Timer-driven transition**: Transition on a timer fire.
4. **Sensor-driven transition**: Transition on a sensor event.
5. **Cancellation**: Cancel an active turn.
6. **Terminal completion**: Complete the agent lifecycle.

> **Normative definition.**
Each representative flow MUST be verified by the Phase 5 integration tests.

## 5.2 Behavior And Integration

### Failure scenarios

> **Normative definition.**
The host MUST handle the following failure scenarios:

1. **Overload**: Mailbox overload when bounds are reached.
2. **Duplicate delivery**: Duplicate signal delivery.
3. **Expired signal**: Signal past its deadline.
4. **Lease loss**: Turn lease lost (e.g., host restart).
5. **Shutdown**: Host shutdown during a turn.
6. **Reactivation**: Reactivation after suspension/hibernation.
7. **Initialization failure**: Reducer initialization failure.

> **Normative definition.**
Each failure scenario MUST be verified by the Phase 5 integration tests.

### Host-owned turn evidence

> **Normative definition.**
The host MUST record the following evidence for each turn:

1. **Identities**: Signal identity, agent identity, instance identity.
2. **Artifact/profile**: Artifact digest, profile version.
3. **Limits**: Memory limit, timeout, host function limit.
4. **Revisions**: Input revision, output revision.
5. **Route**: Signal route (action, strategy transition).
6. **Result**: Turn result (state patch, directives, diagnostics).
7. **Usage**: Invocation usage (input bytes, output bytes, host calls, duration).
8. **Failure disposition**: Failure diagnostic, if any.

> **Normative definition.**
The host MUST retain turn evidence for debugging and auditing purposes.
Ordinary turn evidence MUST remain available for exactly 90 days after the turn
completes and MUST then become unavailable. Evidence classified by another
applicable normative chapter as security evidence or an audit event MUST
instead follow the longer retention and authorized-deletion rules in
[Host-owned evidence recording](34-provenance-signing-audit-security-and-milestone-acceptance.md#host-owned-evidence-recording)
and
[Retention Policies](48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md#4818-retention-policies),
as applicable.

### Milestone 3 exit report

> **Normative definition.**
The Milestone 3 exit report MUST include:

1. **Semantic clauses**: Summary of normative requirements satisfied.
2. **Fixtures**: List of all integration tests with pass/fail status.
3. **Replay results**: Evidence that canonical re-encoding and replay produce identical results.
4. **Unresolved variability**: Any variability choices not yet documented.
5. **Durability gaps**: Precise durability gaps intentionally deferred to Milestone 4.

> **Normative definition.**
The exit report MUST be signed off by the milestone owner before Milestone 3
is considered complete.

### Durability gaps deferred to Milestone 4

> **Non-normative note.**
The following durability gaps are intentionally deferred to Milestone 4:

1. **State persistence**: State is in-memory only. Milestone 4 will add durable state storage.
2. **Mailbox persistence**: Mailbox is in-memory only. Milestone 4 will add durable mailbox storage.
3. **Registry persistence**: Registry is in-memory only. Milestone 4 will add durable registry storage.
4. **Sensor persistence**: Sensor state is in-memory only. Milestone 4 will add durable sensor state storage.
5. **Schedule persistence**: Schedule state is in-memory only. Milestone 4 will add durable schedule state storage.
6. **Timer persistence**: Timer state is in-memory only. Milestone 4 will add durable timer state storage.

> **Non-normative note.**
These durability gaps mean that a host restart will lose all state.
Milestone 4 will address these gaps.

## 5.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to single-agent host flow and
milestone acceptance:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid host flow request structure | Failed JSON parsing or schema validation | `host.flow.request.malformed` |
| Incompatible | Reducer incompatible with host flow | Profile version mismatch | `host.flow.request.incompatible` |
| Conflicting | Concurrent turns on same agent | Same agent targeted with multiple leases | `host.flow.turn_lease.conflict` |
| Unauthorized | Missing capability for host flow | Required capability not granted | `host.flow.request.unauthorized` |
| Exhausted | Resource limits exceeded | Maximum agents per tenant reached | `host.flow.capacity.exhausted` |
| Unavailable | Registry or artifact unavailable | Registry not found or artifact not cached | `host.flow.registry.unavailable`, `host.flow.artifact.unavailable` |
| Trap | Reducer trapped | Guest instance trapped | `host.flow.reducer.trap` |
| Timeout | Reducer duration limit | Effective turn-duration ceiling exceeded | `identity.limit.time.turn_ms` |
| Cancelled | Reducer cancelled | Cancellation requested | `host.flow.reducer.cancelled` |
| InvalidOutput | Invalid reducer output | Output validation failed | `host.flow.reducer.invalid_output` |
| StaleRevision | Stale revision | Input revision does not match current | `host.flow.state.stale_revision` |
| PolicyRejection | Policy rejection | Policy rejected the request | `host.flow.policy.rejected` |

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
| `host.flow.request` | Host flow request failures | `malformed`, `incompatible`, `unauthorized` |
| `host.flow.turn_lease` | Turn lease failures | `conflict` |
| `host.flow.capacity` | Capacity failures | `exhausted` |
| `host.flow.registry` | Registry failures | `unavailable` |
| `host.flow.artifact` | Artifact failures | `unavailable` |
| `host.flow.reducer` | Reducer failures independent of named limits | `trap`, `cancelled`, `invalid_output` |
| `identity.limit` | Named host-flow limit exhaustion | `time.turn_ms`, `memory.max_pages`, `input.max_bytes`, `output.max_bytes` |
| `host.flow.state` | State failures | `stale_revision` |
| `host.flow.policy` | Policy failures | `rejected` |

### Internal mechanisms and fixed behavior

> **Normative definition.**
Execution optimization, evidence storage, metrics collection, structured
logging, and tracing backends are internal mechanisms. Every mechanism MUST be
observationally equivalent with respect to the nine host-flow steps, operation
order, acceptance, diagnostics, committed state, directives, lifecycle state,
usage, and required turn evidence. A failed precommit host-flow step MUST NOT
be retried transparently: the host publishes no commit, releases any acquired
lease, and returns the specified diagnostic. Postcommit lease-release or
directive failures are recorded and fenced or retried under their governing
contracts without rolling back the committed turn. A later signal submission
is a new flow with a newly acquired lease.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Multi-agent coordination**: A formal multi-agent coordination mechanism will be implemented in future milestones. The protocol is language-neutral and does not require multi-agent coordination for base conformance.

2. **Durable state storage**: A formal durable state storage mechanism will be implemented in future milestones. The protocol is language-neutral and does not require durable state storage for base conformance.

3. **Production platform**: A formal production platform will be implemented in future milestones. The protocol is language-neutral and does not require production platform for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 5.4 Phase 5 Integration Tests

### Canonical successful flow

> **Normative conformance criterion.**
The canonical successful flow integration test validates that a valid signal
is processed successfully through the full host flow pipeline.

Expected behavior:

- Input: valid signal with authenticated source, resolved tenant/agent, and valid schema.
- Expected output: TurnResult with state_patch, directives, diagnostics.
- Expected error: null.

### Negative: malformed request

> **Normative conformance criterion.**
The negative malformed request test validates that invalid host flow requests are rejected.

Expected behavior:

- Input: host flow request with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `host.flow.request.malformed`.

### Negative: incompatible profile

> **Normative conformance criterion.**
The negative incompatible profile test validates that incompatible profiles are rejected.

Expected behavior:

- Input: host flow request with incompatible profile version.
- Expected output: null.
- Expected error: `host.flow.request.incompatible`.

### Negative: unauthorized

> **Normative conformance criterion.**
The negative unauthorized test validates that missing capabilities are rejected.

Expected behavior:

- Input: host flow request with missing required capability.
- Expected output: null.
- Expected error: `host.flow.request.unauthorized`.

### Negative: reducer trap

> **Normative conformance criterion.**
The negative reducer trap test validates that reducer traps are handled correctly.

Expected behavior:

- Input: reducer that traps during execution.
- Expected output: null.
- Expected error: `host.flow.reducer.trap`.

### Negative: reducer timeout

> **Normative conformance criterion.**
The negative reducer timeout test validates that reducer timeouts are handled correctly.

Expected behavior:

- Input: reducer that exceeds the execution timeout.
- Expected output: null.
- Expected error: `identity.limit.time.turn_ms`.

### Negative: reducer cancelled

> **Normative conformance criterion.**
The negative reducer cancelled test validates that reducer cancellations are handled correctly.

Expected behavior:

- Input: reducer that is cancelled during execution.
- Expected output: null.
- Expected error: `host.flow.reducer.cancelled`.

### Negative: invalid output

> **Normative conformance criterion.**
The negative invalid output test validates that invalid reducer output is rejected.

Expected behavior:

- Input: reducer that produces invalid output.
- Expected output: null.
- Expected error: `host.flow.reducer.invalid_output`.

### Negative: stale revision

> **Normative conformance criterion.**
The negative stale revision test validates that stale revisions are rejected.

Expected behavior:

- Input: host flow request with stale revision.
- Expected output: null.
- Expected error: `host.flow.state.stale_revision`.

### Negative: lease conflict

> **Normative conformance criterion.**
The negative lease conflict test validates that lease conflicts are handled correctly.

Expected behavior:

- Input: concurrent turns on the same agent.
- Expected output: null.
- Expected error: `host.flow.turn_lease.conflict`.

### Negative: capacity exhausted

> **Normative conformance criterion.**
The negative capacity exhausted test validates that capacity limits are enforced.

Expected behavior:

- Input: host flow request that exceeds the maximum agents per tenant.
- Expected output: null.
- Expected error: `host.flow.capacity.exhausted`.

### Representative flow: direct action

> **Normative conformance criterion.**
The representative direct action flow test validates that a direct action
is executed successfully.

Expected behavior:

- Input: signal that triggers a direct action.
- Expected output: TurnResult with state_patch, directives, diagnostics.
- Expected error: null.

### Representative flow: FSM waiting/resume

> **Normative conformance criterion.**
The representative FSM waiting/resume flow test validates that an FSM
waits for a signal and resumes when received.

Expected behavior:

- Input: signal that triggers an FSM waiting state.
- Expected output: TurnResult with no state_patch, directives for resume.
- Expected error: null.

### Representative flow: timer-driven transition

> **Normative conformance criterion.**
The representative timer-driven transition flow test validates that a
timer fire triggers a state transition.

Expected behavior:

- Input: timer fire signal.
- Expected output: TurnResult with state_patch for transition.
- Expected error: null.

### Representative flow: sensor-driven transition

> **Normative conformance criterion.**
The representative sensor-driven transition flow test validates that a
sensor event triggers a state transition.

Expected behavior:

- Input: sensor event signal.
- Expected output: TurnResult with state_patch for transition.
- Expected error: null.

### Representative flow: cancellation

> **Normative conformance criterion.**
The representative cancellation flow test validates that an active turn
can be cancelled.

Expected behavior:

- Input: cancellation signal for an active turn.
- Expected output: TurnResult with cancellation diagnostic.
- Expected error: null.

### Representative flow: terminal completion

> **Normative conformance criterion.**
The representative terminal completion flow test validates that an agent
can reach terminal completion.

Expected behavior:

- Input: signal that triggers terminal completion.
- Expected output: TurnResult with terminal completion diagnostic.
- Expected error: null.

### Fixed evidence, optimization, and failure behavior

> **Normative conformance criterion.**
The Phase 5 integration tests MUST additionally verify:

1. Every completed or failed turn records all eight required evidence groups,
   and ordinary turn evidence remains available before the 90-day boundary and
   becomes unavailable at that boundary.
2. Evidence subject to a longer security or audit retention rule remains
   available for that longer period.
3. An optimized execution path and the unoptimized reference path produce the
   same acceptance, diagnostics, state, directives, lifecycle state, usage
   fields, and turn evidence for the same input.
4. Failure at each precommit boundary through atomic commit publishes no
   partial state and releases any acquired lease without transparent retry.
   Simulated postcommit lease-release and directive failures preserve the
   committed turn and follow their fencing or retry contracts.

### Cross-milestone fixture regression

> **Normative conformance criterion.**
All earlier milestone fixtures MUST be re-run after Phase 5 to verify
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

The register summarizes fixed behavior and internal mechanisms. It does not
independently license variation.

| Clause | Type | Selection | Constraint |
|--------|------|-----------|------------|
| Host flow reference flow | Required | Nine steps fixed by this chapter | Preserve accepted-record admission, atomic commit, turn completion, and asynchronous directive drain order |
| Host flow invariants | Required | Six invariants fixed by this chapter | Never commit partial state |
| Representative flows | Required | Six flows fixed by this chapter | Verify each flow in Phase 5 |
| [Turn evidence recording](#host-owned-turn-evidence) | Required | Eight evidence groups | Record every completed or failed turn |
| [Ordinary turn-evidence retention](#host-owned-turn-evidence) | Required | Exactly 90 days | Apply longer security or audit rules when applicable |
| [Failure recovery](#internal-mechanisms-and-fixed-behavior) | Required | No transparent turn retry | Precommit failure publishes nothing; postcommit failure never rolls back the committed turn |
| Optimization and observability backends | Internal mechanism | No profile selection | Preserve host-flow, result, state, lifecycle, usage, and evidence observations |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The host flow provides:

- A complete reference flow from signal admission to state commit.
- Clear invariants for failure handling.
- Representative flows for common use cases.

The failure scenarios provide:

- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.
- Evidence that failures are handled correctly.

The turn evidence provides:

- Comprehensive debugging and auditing capabilities.
- Foundation for cross-implementation conformance testing.

The integration tests provide:

- Verification that the canonical flow works end-to-end.
- Evidence that all failure modes are handled correctly.
- Evidence that all representative flows work correctly.
- Foundation for cross-implementation conformance testing.
