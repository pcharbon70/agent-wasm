# Phase 3 - Direct FSM Tool-Loop And Planning Strategies

Back to milestone: [README](./README.md)

- [ ] 3 Phase - Implement representative reasoning policies as replaceable, bounded state transitions over explicit inputs.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 3.1 Section - Contract And Data Model

- [ ] 3.1 Section - Establish contract and data model for direct fsm tool-loop and planning strategies.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.1.1.1 Subtask - Define direct strategy behavior for one validated action and result without hidden continuation state.
    - [ ] 3.1.1.2 Subtask - Define FSM strategy states, events, guards, transitions, waiting points, snapshot schema, and migration.
    - [ ] 3.1.1.3 Subtask - Define bounded tool-loop state for model request, tool selection, tool result, next-step decision, termination, and iteration budget.

## 3.2 Section - Behavior And Integration

- [ ] 3.2 Section - Establish behavior and integration for direct fsm tool-loop and planning strategies.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.2.1.1 Subtask - Define planning strategy outputs as reviewable plan state and directives rather than unbounded private reasoning traces.
    - [ ] 3.2.1.2 Subtask - Enforce turn, token, tool, cost, time, and recursion budgets in host policy and strategy inputs.
    - [ ] 3.2.1.3 Subtask - Define invalid snapshot, nonprogress loop, repeated tool request, contradictory plan, missing result, model drift, and forced termination behavior.

## 3.3 Section - Failure Evidence And Operational Notes

- [ ] 3.3 Section - Establish failure evidence and operational notes for direct fsm tool-loop and planning strategies.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [ ] 3.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [ ] 3.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to direct fsm tool-loop and planning strategies.
    - [ ] 3.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [ ] 3.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 3.4 Section - Phase 3 Integration Tests

- [ ] 3.4 Section - Verify direct fsm tool-loop and planning strategies across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [ ] 3.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [ ] 3.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for direct fsm tool-loop and planning strategies.
    - [ ] 3.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [ ] 3.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [ ] 3.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

