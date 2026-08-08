---
title: "Deterministic Reducer Semantics And Milestone Acceptance"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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
The reducer MUST process turns in the following order:

1. **Signal validation**: Validate each signal's structure and required fields. See [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).
2. **Signal routing**: Route signals to appropriate actions or strategy transitions.
3. **Action/strategy execution**: Execute actions or apply strategy transitions. See [Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md) and [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).
4. **Patch production**: Collect state operations from action results or strategy transitions.
5. **Patch validation**: Validate the combined patch against current state revision. See [State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md#patch-validation).
6. **Patch application**: Apply the validated patch to produce new state revision.
7. **Directive production**: Collect directives from action results. See [Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md#directive-processing).
8. **Result construction**: Assemble turn result with state, directives, and diagnostics. See [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#turnresult-fields).

> **Normative definition.**
Each step MUST complete before the next step begins.
If any step fails, the reducer MUST emit a diagnostic and terminate the turn.
No partial state changes are permitted.

### Determinism requirement

> **Normative definition.**
The reducer MUST satisfy the following determinism requirement:

Given identical canonical inputs (signals, state, instructions) and profile,
the reducer MUST produce canonically equivalent results.

> **Normative definition.**
The Reducer's `state_schema_version` constrains which Patch `state_schema_version`
values are accepted.
If a Patch specifies a `state_schema_version` that does not match the Reducer's
`state_schema_version`, the patch MUST be rejected with `state.schema.version_mismatch`.

> **Normative definition.**
"Canonically equivalent" means:

- State patches are byte-identical after canonical JSON encoding.
- Directives are byte-identical after canonical JSON encoding.
- Diagnostics are byte-identical after canonical JSON encoding.
- State revision sequence numbers are identical.

> **Normative definition.**
The following `TurnResult` fields are excluded from equivalence checks:

- `invocation_id`: Per-invocation identifier, not deterministic across replays.
- `protocol_version`: May vary between protocol versions.
- `timestamp`: Wall-clock time, not deterministic.

The following `TurnResult` fields MUST be byte-identical for equivalence:

- `domain_status`
- `state` (after canonical encoding)
- `directives` (after canonical encoding)
- `diagnostics` (after canonical encoding)
- `strategy_snapshot` (if present, after canonical encoding)

> **Normative implementation-defined choice.**
Implementation-defined choices (e.g., hash algorithm, conflict resolution)
MUST be documented in the conformance profile.
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
Implementations MAY define additional reducer types as long as they satisfy
the determinism requirement and turn resolution order.

## 5.2 Behavior And Integration

### Metamorphic cases

> **Normative definition.**
The following metamorphic cases verify deterministic behavior:

1. **Irrelevant field ordering**: Signals with fields in different orders MUST produce identical results.
2. **Canonical re-encoding**: Re-encoding the turn request via canonical JSON MUST produce identical results.
3. **Replay from same revision**: Replaying a turn from the same state revision MUST produce identical results.

> **Normative definition.**
Each metamorphic case MUST be verified by the Phase 5 integration tests.
If any case fails, the reducer is non-conformant.

### Negative cases

> **Normative definition.**
The following negative cases verify failure handling:

1. **Stale state**: Turn with state revision older than current MUST be rejected with `state.revision.stale`.
2. **Ambiguous route**: Signal with no matching action or strategy transition MUST be rejected with `signal.routing.ambiguous`.
3. **Invalid patch**: Patch that fails validation MUST be rejected with appropriate diagnostic.
4. **Unauthorized directive**: Directive requiring ungranted capability MUST be rejected with `directive.missing.missing_capability`.
5. **Corrupt strategy snapshot**: Snapshot that fails validation MUST be rejected with `strategy.snapshot.corruption`.

> **Normative definition.**
Each negative case MUST be verified by the Phase 5 integration tests.
The reducer MUST emit a diagnostic identifying the failed boundary.

### Milestone 2 exit report

> **Normative definition.**
The Milestone 2 exit report MUST include:

1. **Semantic clauses**: Summary of normative requirements satisfied.
2. **Fixtures**: List of all integration tests with pass/fail status.
3. **Replay results**: Evidence that canonical re-encoding and replay produce identical results.
4. **Unresolved variability**: Any implementation-defined choices not yet documented.

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
| `reducer.resolution` | Turn resolution failures | `signal_invalid`, `routing_ambiguous`, `patch_rejected` |
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

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Canonical encoding**: The host MAY choose the canonical JSON encoding algorithm. The algorithm MUST produce byte-identical output for canonically equivalent inputs.

2. **Hash algorithm**: The host MAY choose the hash algorithm for state and revision computation. The algorithm MUST be documented in the conformance profile.

3. **Conflict resolution**: The host MAY implement conflict resolution strategies. The strategy is implementation-defined.

4. **Reducer loading**: The host MAY choose how to load and validate reducers. The loading mechanism is implementation-defined.

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
- Expected output: TurnResult with state_patch, directives, diagnostics.
- Expected error: null.

### Metamorphic: field ordering

> **Normative definition.**
The metamorphic field ordering test validates that signal field ordering
does not affect the result.

Expected behavior:

- Input: two turns with signals in different field orders.
- Expected output: canonically equivalent TurnResults.
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
- Expected output: byte-identical TurnResults.
- Expected error: null.

### Negative: stale state

> **Normative definition.**
The negative stale state test validates that a turn with stale state is rejected.

Expected behavior:

- Input: turn with state revision older than current.
- Expected output: null.
- Expected error: `state.revision.stale`.

### Negative: ambiguous route

> **Normative definition.**
The negative ambiguous route test validates that a signal with no matching
action or strategy is rejected.

Expected behavior:

- Input: signal with no matching reducer or transition.
- Expected output: null.
- Expected error: `signal.routing.ambiguous`.

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
- Expected output: null.
- Expected error: `directive.missing.missing_capability`.

### Negative: corrupt strategy snapshot

> **Normative definition.**
The negative corrupt strategy snapshot test validates that a corrupt snapshot
is rejected.

Expected behavior:

- Input: turn with strategy snapshot that fails validation.
- Expected output: null.
- Expected error: `strategy.snapshot.corruption`.

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

| Clause | Type | Selection |
|--------|------|-----------|
| Reducer structure | Required | Fields fixed by this chapter |
| Turn resolution order | Required | 8-step order fixed by this chapter |
| Determinism requirement | Required | Canonically equivalent results fixed by this chapter |
| Canonical encoding | Implementation-defined | Documented in conformance profile |
| Hash algorithm | Implementation-defined | Documented in conformance profile |
| Conflict resolution | Implementation-defined | Documented in conformance profile |
| Reducer loading | Implementation-defined | Documented in conformance profile |

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

- Verification that implementation-defined choices do not affect results.
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
