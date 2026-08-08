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

ReducerKind = "direct" | "fsm" | "bounded_loop"

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

1. **Signal validation**: Validate each signal's structure and required fields.
2. **Signal routing**: Route signals to appropriate actions or strategy transitions.
3. **Action/strategy execution**: Execute actions or apply strategy transitions.
4. **Patch production**: Collect state operations from action results or strategy transitions.
5. **Patch validation**: Validate the combined patch against current state revision.
6. **Patch application**: Apply the validated patch to produce new state revision.
7. **Directive production**: Collect directives from action results.
8. **Result construction**: Assemble turn result with state, directives, and diagnostics.

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
"Canonically equivalent" means:

- State patches are byte-identical after canonical JSON encoding.
- Directives are byte-identical after canonical JSON encoding.
- Diagnostics are byte-identical after canonical JSON encoding.
- State revision sequence numbers are identical.

> **Non-normative note.**
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
