---
title: "Deterministic Reducer Semantics And Milestone Acceptance"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-02
  - phase-05
  - reducer
  - deterministic
  - acceptance
aliases:
  - "M2-P5 Deterministic Reducer"
---

# Deterministic Reducer Semantics And Milestone Acceptance

## Status and authority

This chapter is a normative specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/phase-05-deterministic-reducer-semantics-and-milestone-acceptance.md)
of
[Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/README.md)
--
Signals, Actions, State, And Strategies.
It assembles signals, actions, state operations, directives, and strategies
into one replayable decision kernel.

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
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md),
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

## 5.1 Contract And Data Model

### Reducer

> **Normative definition.**
A reducer is the deterministic decision kernel that processes a turn.
It resolves signals, executes actions or strategies, produces state patches
and directives, and returns a deterministic result.

> **Normative definition.**

```
Reducer {
  id: string,
  kind: ReducerKind,
  profile: ProfileRef,
  state_schema_version: string,
  execute: (TurnRequest) -> TurnResult
}

TurnRequest, TurnResult: Defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

ReducerKind = "direct" | "fsm" | "terminal_workflow" | "bounded_loop"

ProfileRef {
  name: string,
  version: string
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | Yes | Reducer identifier |
| `kind` | ReducerKind | Yes | Reducer type |
| `profile` | ProfileRef | Yes | Profile this reducer conforms to |
| `state_schema_version` | string | Yes | Required state schema version |
| `execute` | function | Yes | Turn execution function |

### Turn resolution order

> **Normative definition.**
The host-coordinated reducer boundary MUST process turns in the following
order. The reducer calculates candidate outputs; only the host validates and
commits authoritative state:

1. **Accepted-signal validation**: Validate the persisted accepted-ingress
   projection, required signal fields, delivery identity, host context, and
   selected target. TTL and instance selection have already completed and
   MUST NOT be reevaluated here. See
   [Guest-wire projection](10-signals-causality-routing-and-delivery.md#guest-wire-projection).
2. **Intra-agent dispatch**: Resolve the already-targeted signal to an action
   or strategy transition. This step MUST NOT select a different agent
   instance or advance an instance-selector cursor.
3. **Action/strategy execution**: Execute actions or apply strategy transitions. See [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md) and [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).
4. **Output production**: Collect state operations and directives from action results or strategy transitions.
5. **Patch validation**: Validate the combined patch against current state revision. See [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md#patch-validation).
6. **Directive validation**: Validate every directive, deterministic id,
   capability, resource, destination, retry class, and result contract. See
   [Directive processing](13-directives-strategies-continuations-and-terminal-states.md#directive-processing).
7. **Result construction**: Assemble and canonically validate the turn result
   with its patch, directives, and diagnostics. See
   [TurnResult fields](04-turn-lifecycle-protocols-and-canonical-encoding.md#turnresult-fields).
8. **Host atomic commit**: Apply the validated patch and atomically commit the new
   state revision, journal facts, and every validated directive outbox entry
   before publishing the successful result.

> **Normative definition.**
Each step MUST complete before the next step begins.
If guest execution fails, the reducer reports its diagnostic in the returned
result or error buffer. If a host-owned validation or commit step fails, the
host emits the governing diagnostic; reducer code may not have run. Every
failure terminates the turn and permits no partial state change.

### Determinism requirement

> **Normative definition.**
The reducer MUST satisfy the following determinism requirement:

Given identical canonical `TurnRequest` values and profile,
the reducer MUST produce canonically equivalent results.

> **Normative definition.**
The Reducer's `state_schema_version` constrains which Patch `state_schema_version`
values are accepted.
If a Patch specifies a `state_schema_version` that does not match the Reducer's
`state_schema_version`, the patch MUST be rejected with `state.schema.version_mismatch`.

> **Normative definition.**
"Canonically equivalent" means the complete `TurnResult` is byte-identical
after the one Canonical JSON encoding defined by chapter 04. This includes
`protocol_version`, `invocation_id`, `expected_state_revision`, `state_patch`,
`directives`, `strategy_snapshot`, `domain_status`, and `diagnostics`.

A request with a different invocation identity is not an identical input and
is outside this equivalence judgment. Reducer output MUST NOT contain a host
wall-clock value. Strategy snapshot timestamps are derived from input signal
timestamps under
[Strategy lifecycle](13-directives-strategies-continuations-and-terminal-states.md#strategy-lifecycle).

> **Normative definition.**
Every required profile selection imported from a governing chapter MUST be
documented in the conformance profile. Concurrent state requests use fixed
mailbox and turn-lease serialization and are not a profile selection.
Different implementations with the same profile MUST produce equivalent results.

### Representative reducers

> **Normative definition.**
The following representative reducers illustrate the contract:

1. **Direct action reducer**: Executes a single action and returns the result.
2. **FSM continuation reducer**: Applies strategy transitions based on signals.
3. **Terminal workflow reducer**: Executes a sequence of actions to completion.
4. **Bounded tool-request loop reducer**: Repeats action execution up to iteration limit.

> **Non-normative note.**
These reducers are illustrative.
Additional reducer kinds require an explicit versioned extension; the base
profile contains only the four `ReducerKind` values above.

## 5.2 Behavior And Integration

### Metamorphic cases

> **Normative definition.**
The following metamorphic cases verify deterministic behavior:

1. **Irrelevant construction order**: In-memory signals constructed with
   fields inserted in different orders MUST canonicalize to identical request
   bytes and produce identical results. Non-canonical wire input remains
   invalid.
2. **Canonical re-encoding**: Re-encoding the turn request via canonical JSON MUST produce identical results.
3. **Replay from same revision**: Replaying a turn from the same state revision MUST produce identical results.
4. **Accepted-envelope projection**: Reconstructing a request from the same
   persisted accepted-ingress record MUST produce identical request bytes and
   MUST NOT reevaluate TTL or instance selection.

Metamorphic replay runs the pure reducer in an isolated conformance harness
with the original snapshot restored and without committing either run. It is
not a second submission of the same invocation to a live host and therefore
does not bypass duplicate-invocation rejection.

> **Normative definition.**
Each metamorphic case MUST be verified by the Phase 5 integration tests.
If any case fails, the reducer is non-conformant.

### Negative cases

> **Normative definition.**
The following negative cases verify failure handling:

1. **Stale state**: Turn with state revision older than current MUST be rejected with `state.revision.stale`.
2. **Unmatched route**: A signal with no matching action or strategy transition MUST be rejected with `signal.unmatched` as defined by [Routing outcomes](10-signals-causality-routing-and-delivery.md#routing-outcomes).
3. **Invalid patch**: Patch that fails validation MUST be rejected with appropriate diagnostic.
4. **Unauthorized directive**: Directive requiring ungranted capability MUST be rejected with `directive.missing.missing_capability`.
5. **Corrupt strategy snapshot**: Snapshot that fails validation MUST be rejected with `strategy.snapshot.corruption`.
6. **Delivery identity mismatch**: A signal whose `delivery_id` does not match
   its accepted tenant-scoped identity MUST be rejected with
   `protocol.semantic.delivery_identity_invalid`.
7. **Projection mismatch**: A request whose tenant, principal, trace context,
   target agent type, or target instance differs from its accepted record MUST be rejected with
   `protocol.semantic.context_projection_invalid` before reducer execution.

> **Normative definition.**
Each negative case MUST be verified by the Phase 5 integration tests.
The reducer MUST emit a diagnostic identifying the failed boundary.

### Milestone 2 exit report

> **Normative definition.**
The Milestone 2 exit report MUST include:

1. **Semantic clauses**: Summary of normative requirements satisfied.
2. **Fixtures**: List of all integration tests with pass/fail status.
3. **Replay results**: Evidence that canonical re-encoding and replay produce identical results.
4. **Unresolved variability**: Any required profile selections not yet documented.

> **Normative definition.**
The exit report MUST be signed off by the milestone owner before Milestone 2 is considered complete.

## 5.3 Failure Evidence And Operational Notes

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
| `reducer.resolution` | Reducer loading and output failures | `signal_invalid`, `patch_rejected`, `not_found`, `invalid_descriptor` |
| `reducer.determinism` | Determinism violations | `result_mismatch`, `encoding_mismatch` |
| `reducer.replay` | Replay failures | `stale_revision`, `corrupt_snapshot` |
| `acceptance.exit` | Exit report issues | `fixture_failed`, `variability_unresolved` |

### Failure modes

| Mode | Description | Conditions |
|------|-------------|------------|
| Malformed | Invalid turn request structure | Failed JSON parsing or schema validation |
| Incompatible | Reducer profile incompatible with turn | Profile version mismatch |
| Conflicting | Concurrent turns on same revision | Same state revision targeted |
| Unauthorized | Missing capability for directive | Required capability not granted |
| Exhausted | Resource limits exceeded | Timeout, memory, or iteration limit |
| Unavailable | Reducer or strategy unavailable | Reducer not found or strategy corrupt |

### Governing fixed semantics and internal mechanisms

1. **Canonical encoding**: Reducer inputs and outputs MUST use
   [Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).
   No alternate encoding algorithm is permitted.

2. **Hash algorithm**: State and revision hashes MUST use the SHA-256
   calculations in
   [Next-revision calculation](12-state-operations-patches-revisions-and-conflicts.md#next-revision-calculation).

3. **Concurrent state requests**: Ordinary turns load state only after lease
   acquisition; the current turn lease and FIFO maintenance queue serialize
   all patch commits under
   [Conflict detection](12-state-operations-patches-revisions-and-conflicts.md#conflict-detection).

4. **Reducer loading**: The host MUST load the reducer identified by `id`,
   `kind`, `profile`, and `state_schema_version` from the admitted artifact and
   validate it before turn processing. The host MAY use any internal loading
   backend only if it returns byte-identical reducer bytes and identical
   validation, result, and diagnostic observations. A missing reducer MUST
   fail with `reducer.resolution.not_found`; an invalid reducer descriptor MUST
   fail with `reducer.resolution.invalid_descriptor`. Neither failure may
   execute reducer code or publish partial state.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Reducer composition API**: A formal reducer composition API will be implemented in future milestones. The protocol is language-neutral and does not require reducer composition for base conformance.

2. **Reducer debugging API**: A formal reducer debugging API will be implemented in future milestones. The protocol is language-neutral and does not require reducer debugging for base conformance.

3. **Reducer monitoring API**: A formal reducer monitoring API will be implemented in future milestones. The protocol is language-neutral and does not require reducer monitoring for base conformance.

4. **Milestone 3 planning**: Future milestones will build on Milestone 2 contracts and may introduce additional phases and chapters.

## 5.4 Phase 5 Integration Tests

### Canonical successful flow

> **Normative definition.**
The canonical successful flow integration test validates that a valid turn
is processed successfully through the full resolution order.

Expected behavior:

- Input: valid turn with signal, action, and state.
- Expected output: TurnResult with state_patch, directives, and diagnostics,
  published only after atomic state, journal, and outbox commit.
- Expected evidence: the request matches its durable accepted-ingress record
  and the accepted target and selector state remain unchanged by reducer
  dispatch.
- Expected error: null.

### Metamorphic: field ordering

> **Normative definition.**
The metamorphic field ordering test validates that signal field ordering
does not affect the result.

Expected behavior:

- Input: two in-memory turn values whose signal fields were inserted in
  different orders, each canonically encoded before invocation.
- Expected output: identical canonical request bytes and byte-identical
  TurnResults.
- Expected error: null.

### Metamorphic: canonical re-encoding

> **Normative definition.**
The metamorphic canonical re-encoding test validates that re-encoding
the turn request produces identical results.

Expected behavior:

- Input: turn request encoded via canonical JSON, then re-encoded.
- Expected output: byte-identical TurnResults.
- Expected error: null.

### Metamorphic: replay from same revision

> **Normative definition.**
The metamorphic replay test validates that replaying a turn from the same
revision produces identical results.

Expected behavior:

- Input: same turn request replayed from same state revision.
- Expected output: byte-identical TurnResults from two isolated, noncommitting
  reducer runs.
- Expected error: null.

### Metamorphic: accepted-envelope projection

> **Normative definition.**
The accepted-envelope projection test reconstructs a request twice from the
same persisted `AcceptedSignalEnvelope`, once after advancing the host wall
clock and perturbing registry enumeration order.

Expected behavior:

- Expected request: byte-identical canonical `TurnRequest` values.
- Expected target: the target recorded in the accepted envelope.
- Expected selector effect: no cursor read or advancement during either
  reconstruction.
- Expected output: byte-identical TurnResults from isolated, noncommitting
  reducer runs.

### Negative: stale state

> **Normative definition.**
The negative stale state test validates that a turn with stale state is rejected.

Expected behavior:

- Input: turn with state revision older than current.
- Expected output: null.
- Expected error: `state.revision.stale`.

### Negative: unmatched route

> **Normative definition.**
The negative unmatched-route test validates that a signal with no matching
action or strategy is rejected.

Expected behavior:

- Input: signal with no matching reducer or transition.
- Expected output: null.
- Expected error: `signal.unmatched`.

### Negative: invalid patch

> **Normative definition.**
The negative invalid patch test validates that an invalid patch is rejected.

Expected behavior:

- Input: turn producing patch that fails validation.
- Expected output: null.
- Expected error: `state.patch.malformed`, `state.patch.incompatible`, or other `state.patch.*` diagnostic per [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md).

### Negative: unauthorized directive

> **Normative definition.**
The negative unauthorized directive test validates that a directive requiring
an ungranted capability is rejected.

Expected behavior:

- Input: turn producing directive requiring ungranted capability.
- Expected output: null; no state, journal, or outbox entry commits.
- Expected error: `directive.missing.missing_capability`.

### Negative: corrupt strategy snapshot

> **Normative definition.**
The negative corrupt strategy snapshot test validates that a corrupt snapshot
is rejected.

Expected behavior:

- Input: turn with strategy snapshot that fails validation.
- Expected output: null.
- Expected error: `strategy.snapshot.corruption`.

### Negative: delivery identity mismatch

> **Normative definition.**
The negative delivery-identity test mutates one hexadecimal digit in the
accepted signal's `delivery_id`.

Expected behavior:

- Expected output: null; reducer code is not invoked.
- Expected error: `protocol.semantic.delivery_identity_invalid`.

### Negative: accepted-context projection mismatch

> **Normative definition.**
The negative projection test separately changes the runtime tenant, principal,
trace context, target agent type, and target instance relative to the persisted
accepted record.

Expected behavior:

- Expected output: null; reducer code is not invoked.
- Expected error: `protocol.semantic.context_projection_invalid` for every
  mutation.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 5 to verify
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

Any approved variability MUST be documented in the Milestone 2 exit report.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
|--------|------|-----------|
| Reducer structure | Required | Fields fixed by this chapter |
| Turn resolution order | Required | 8-step order fixed by this chapter |
| Determinism requirement | Required | Canonically equivalent results fixed by this chapter |
| [Accepted-signal validation](#turn-resolution-order) | Required | Validate recorded delivery identity, host context, and target without reevaluating TTL or selection |
| [Accepted-envelope replay](#metamorphic-accepted-envelope-projection) | Required | Reuse the durable projection and target; selector state is untouched |
| [Canonical encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding) | Required | Rules fixed by the canonical JSON contract |
| [Hash algorithm](12-state-operations-patches-revisions-and-conflicts.md#next-revision-calculation) | Required | SHA-256 over canonical JSON |
| [Concurrent state requests](12-state-operations-patches-revisions-and-conflicts.md#conflict-detection) | Required | Ordinary turns load after lease acquisition; FIFO maintenance serialization makes later prebuilt same-base patches stale |
| [Reducer loading](#governing-fixed-semantics-and-internal-mechanisms) | MAY (internal backend) | Byte-identical reducer and outcome equivalence required |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The reducer model provides:

- A deterministic decision kernel that processes turns.
- A clear resolution order from signal validation through result construction.
- A determinism requirement that enables replay and verification.

The metamorphic cases provide:

- Verification that fixed mailbox and lease ordering does not affect replay
  equivalence.
- Evidence that canonical encoding is stable.
- Foundation for cross-implementation conformance testing.

The negative cases provide:

- Verification that failures are handled correctly.
- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.

The exit report provides:

- A structured summary of Milestone 2 completion.
- Evidence that all fixtures pass and determinism is verified.
- Documentation of any unresolved variability.
