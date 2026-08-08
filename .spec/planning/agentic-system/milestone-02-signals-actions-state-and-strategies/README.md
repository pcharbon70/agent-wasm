# Milestone 2 - Signals, Actions, State, And Strategies

Implement the portable Jido-inspired decision vocabulary and deterministic reducer semantics independently of host scheduling and external effects.

Current status: planned; all phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for signals, actions, state, and strategies.

## Dependencies And Entry Gate

- Milestone 1 protocol, manifest, identity, and schema contracts are approved.
- Positive and negative turn fixtures can be decoded consistently.

## Phase Order

1. [Phase 1 - Signal Envelopes Causality Routing And Delivery Vocabulary](phase-01-signal-envelopes-causality-routing-and-delivery-vocabulary.md)
2. [Phase 2 - Actions Instructions Validation Plans And Results](phase-02-actions-instructions-validation-plans-and-results.md)
3. [Phase 3 - State Operations Patches Revisions And Conflicts](phase-03-state-operations-patches-revisions-and-conflicts.md)
4. [Phase 4 - Directives Strategies Continuations And Terminal States](phase-04-directives-strategies-continuations-and-terminal-states.md)
5. [Phase 5 - Deterministic Reducer Semantics And Milestone Acceptance](phase-05-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Planned Artifacts

- Signal and routing semantic model
- Action, instruction, state-operation, directive, and strategy contracts
- Direct and FSM reducer conformance corpus

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- The reducer is deterministic over explicit inputs.
- State changes are expressed as validated patches against an expected revision.
- External authority is requested through directives rather than exercised by the reducer.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Signal Envelopes Causality Routing And Delivery Vocabulary](phase-01-signal-envelopes-causality-routing-and-delivery-vocabulary.md) — implements and verifies this ordered phase.
- [Phase 2 - Actions Instructions Validation Plans And Results](phase-02-actions-instructions-validation-plans-and-results.md) — implements and verifies this ordered phase.
- [Phase 3 - State Operations Patches Revisions And Conflicts](phase-03-state-operations-patches-revisions-and-conflicts.md) — implements and verifies this ordered phase.
- [Phase 4 - Directives Strategies Continuations And Terminal States](phase-04-directives-strategies-continuations-and-terminal-states.md) — implements and verifies this ordered phase.
- [Phase 5 - Deterministic Reducer Semantics And Milestone Acceptance](phase-05-deterministic-reducer-semantics-and-milestone-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
