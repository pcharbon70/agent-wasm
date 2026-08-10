---
title: "Single-Agent Host Flow And Milestone Acceptance"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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
signal through routing, lease, snapshot load, reducer call, result validation,
and in-memory commit:

1. **Signal admission**: Authenticate the signal source, resolve tenant/agent, validate schema, deduplicate, and admit to mailbox.
2. **Mailbox dequeue**: Dequeue the signal from the mailbox in priority order.
3. **Lease acquisition**: Acquire a turn lease for the agent.
4. **Snapshot load**: Load the state snapshot for the agent.
5. **Reducer invocation**: Invoke the reducer with the signal, state snapshot, and grants.
6. **Result validation**: Validate the reducer result (state patch, directives, diagnostics).
7. **State commit**: Commit the state patch to the agent's state.
8. **Directive execution**: Execute the directives (emit, timer, effect, etc.).
9. **Lease release**: Release the turn lease.

> **Normative definition.**
If any step fails, the host MUST roll back the state change and release the
lease.
The host MUST NOT commit partial state changes.

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
The retention period MUST be documented in the conformance profile.

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
| Timeout | Reducer timeout | Execution timeout exceeded | `host.flow.reducer.timeout` |
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
| `host.flow.reducer` | Reducer failures | `trap`, `timeout`, `cancelled`, `invalid_output` |
| `host.flow.state` | State failures | `stale_revision` |
| `host.flow.policy` | Policy failures | `rejected` |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Turn evidence retention**: The host MAY choose how long to retain turn evidence. The retention period MUST be documented in the conformance profile.

2. **Host flow optimization**: The host MAY optimize the host flow for performance. The optimization MUST be documented in the conformance profile.

3. **Failure recovery**: The host MAY implement failure recovery strategies. The strategy MUST be documented in the conformance profile.

4. **Observability**: The host MAY choose the observability mechanisms (metrics, logging, tracing). The mechanisms MUST be documented in the conformance profile.

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
- Expected error: `host.flow.reducer.timeout`.

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

| Clause | Type | Selection |
|--------|------|-----------|
| Host flow reference flow | Required | 9 steps fixed by this chapter |
| Host flow invariants | Required | 6 invariants fixed by this chapter |
| Representative flows | Required | 6 flows fixed by this chapter |
| Turn evidence recording | Required | 8 evidence fields fixed by this chapter |

Other variability choices are documented in the section on host-defined selections.

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
