---
title: "2026-08-09 Phase 3 Implementation"
kind: journal
created: "2026-08-09"
tags:
  - milestone-07
  - phase-03
  - implementation
  - journal
aliases:
  - "M7-P3 Journal 2026-08-09"
---

# 2026-08-09 Phase 3 Implementation

## Overview

This journal entry documents the implementation of Phase 3 of Milestone 7:
**Direct FSM Tool-Loop And Planning Strategies**.

## Work performed

### Branch creation

Created and pushed branch `milestone-07-phase-03-direct-fsm-tool-loop-and-planning-strategies` from main.

### Implementation notes created

Created four implementation notes documenting each section of Phase 3:

1. **[Phase 3 Contract And Data Model Implementation](../70-milestones/m7/m7-phase-03-contract-and-data-model-implementation.md)**
   - Documents Subtask 3.1.1.1: Direct strategy behavior for one validated action and result without hidden continuation state (8 fields including strategy kind, action ID, result ID, continuation, iteration, budget remaining)
   - Documents Subtask 3.1.1.2: FSM strategy states (7 states), events (24 events), snapshot schema (10 fields), and migration rules (5 rules)
   - Documents Subtask 3.1.1.3: Bounded tool-loop state (10 states), tool selection strategy (4 rules), iteration budgets (6 budget types), and termination conditions (9 conditions)

2. **[Phase 3 Behavior And Integration Implementation](../70-milestones/m7/m7-phase-03-behavior-and-integration-implementation.md)**
   - Documents Subtask 3.2.1.1: Planning strategy outputs (9 plan state fields, 8-step flow, 5 reviewability requirements)
   - Documents Subtask 3.2.1.2: Budget enforcement (6 budget types, 6 enforcement points, 6 exhaustion diagnostics)
   - Documents Subtask 3.2.1.3: Failure behavior (7 failure types: invalid snapshot, non-progress loop, repeated tool request, contradictory plan, missing result, model drift, forced termination)

3. **[Phase 3 Failure Evidence And Operational Notes Implementation](../70-milestones/m7/m7-phase-03-failure-evidence-and-operational-notes-implementation.md)**
   - Documents Subtask 3.3.1.1: Failure outcomes (26 diagnostics across 6 categories: malformed, incompatible, conflicting, unauthorized, exhausted, unavailable)
   - Documents Subtask 3.3.1.2: Bounded diagnostics (10 fields) and evidence emission (11 fields, 9 evidence types)
   - Documents Subtask 3.3.1.3: Implementation-defined choices (8 choices), deferred work (10 items), and milestone assumption validation (none yet)

4. **[Phase 3 Integration Tests Implementation](../70-milestones/m7/m7-phase-03-integration-tests-implementation.md)**
   - Documents Subtask 3.4.1.1: Successful flow tests (32 tests: 5 direct strategy, 8 FSM transitions, 6 tool-loop, 4 plan submission, 3 budget tracking, 2 snapshot restoration, 3 evidence emission)
   - Documents Subtask 3.4.1.2: Failure handling tests (32 tests: 6 malformed, 3 incompatible, 2 conflicting, 3 unauthorized, 5 budget exhaustion, 3 unavailable, 2 invalid snapshot, 1 non-progress loop, 1 repeated tool request, 1 contradictory plan, 1 missing result, 1 model drift)
   - Documents Subtask 3.4.1.3: Timeout and cancellation tests (14 tests: 4 timeout, 4 cancellation, 3 unavailable dependency, 3 retry)
   - Documents Subtask 3.4.1.4: Cross-milestone compatibility tests (18 fixture scopes from 6 milestones)

## Key design decisions

### Contract and data model

1. **Deterministic FSM**: The FSM is deterministic and fully specified by its states, events, guards, and transitions. There is no hidden state.

2. **Bounded iteration**: The tool-loop is bounded by iteration counters and budgets to prevent infinite loops.

3. **Snapshot-based state**: The FSM state is serialized as a snapshot and can be restored, migrated, or rolled back.

4. **Plan-driven execution**: The tool-loop executes a plan (sequence of steps) rather than unbounded private reasoning.

5. **Budget enforcement at host level**: Budget enforcement is done at the host level, not in the strategy, to prevent bypass.

6. **Diagnostic evidence**: Every state transition emits bounded diagnostics and evidence for observability.

7. **Migration versioning**: Snapshots are versioned and migrated explicitly to support schema evolution.

8. **Tool selection strategy**: Tools are selected based on a priority queue that considers urgency, cost, and capability requirements.

9. **Human-in-the-loop**: The FSM supports human approval and rejection of plans.

10. **Non-progress detection**: The FSM detects and terminates non-progress loops, repeated tool requests, and contradictory plans.

### Behavior and integration

1. **Reviewable plans**: Plans are reviewable and auditable, not hidden private reasoning traces.

2. **Host-enforced budgets**: Budgets are enforced at the host level, not in the strategy, to prevent bypass.

3. **Explicit failure detection**: Failure detection is explicit and documented, not implicit or hidden.

4. **Bounded history**: The FSM maintains a bounded history of state transitions for non-progress detection.

5. **No recovery from critical failures**: The FSM does not attempt to recover from critical failures (invalid snapshot, non-progress loop, etc.).

6. **Evidence emission**: Every failure emits bounded evidence for observability and debugging.

7. **Plan adaptation**: The planning strategy can adapt the plan based on new information or failures.

8. **Step-level visibility**: Each step in the plan is visible and can be inspected.

9. **Decision auditing**: The decisions made by the planning strategy are visible and can be audited.

10. **Forced termination**: The FSM supports forced termination by human cancellation, budget exhaustion, or critical failure.

### Failure evidence and operational notes

1. **Bounded diagnostics**: Diagnostics are bounded and do not expose secrets.

2. **Evidence emission**: Every failure emits bounded evidence for observability and debugging.

3. **Implementation-defined choices**: Implementation-defined choices are documented in host configuration.

4. **Deferred work**: Deferred work is tracked with priority and description.

5. **Milestone assumption validation**: Results that invalidate earlier milestone assumptions are tracked and documented.

6. **Diagnostic codes**: Diagnostic codes are standardized and consistent across phases.

7. **Evidence types**: Evidence types are standardized and consistent across phases.

8. **Contract identification**: Diagnostics and evidence identify the contract and section that failed.

9. **Boundary identification**: Diagnostics and evidence identify the failed boundary.

10. **Profile identification**: Diagnostics and evidence identify the profile (if applicable).

### Integration tests

1. **Comprehensive test coverage**: Tests cover all aspects of Phase 3 (successful flow, failure handling, timeout/cancellation/retry, cross-milestone compatibility).

2. **Stable diagnostics**: Failure tests verify that failures produce stable diagnostics.

3. **No partial state**: Timeout, cancellation, and retry tests verify that no unauthorized or partial state remains.

4. **Cross-milestone compatibility**: Cross-milestone tests verify that Phase 3 does not break earlier milestones.

5. **Evidence retention**: Successful flow tests verify that evidence is retained for observability.

6. **Budget enforcement**: Budget tests verify that budgets are enforced correctly.

7. **Snapshot migration**: Snapshot tests verify that snapshots can be restored correctly.

8. **FSM state transitions**: FSM tests verify that state transitions are correct.

9. **Tool-loop execution**: Tool-loop tests verify that tool-loop execution is correct.

10. **Plan submission**: Plan tests verify that plans are submitted correctly.

## Cross-references

### Specification chapters

- [43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-contract-and-data-model.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-behavior-and-integration.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-failure-evidence-and-operational-notes.md)
- [43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md](../60-specification/43-direct-fsm-tool-loop-and-planning-strategies-phase-3-integration-tests.md)

### Earlier chapters

- [10-signals-causality-routing-and-delivery.md](../60-specification/10-signals-causality-routing-and-delivery.md)
- [11-actions-instructions-validation-plans-and-results.md](../60-specification/11-actions-instructions-validation-plans-and-results.md)
- [12-state-operations-patches-revisions-and-conflicts.md](../60-specification/12-state-operations-patches-revisions-and-conflicts.md)
- [13-directives-strategies-continuations-and-terminal-states.md](../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- [26-atomic-state-journal-and-directive-outbox-commits.md](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- [27-effect-handlers-attempts-idempotency-and-result-signals.md](../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

## Open questions

1. Should the FSM support parallel execution of multiple steps in a plan?

2. Should the budget enforcement be strict (hard limits) or soft (warnings)?

3. Should the planning strategy support preemption (interrupting a step execution)?

4. Should the FSM support checkpointing to external storage (e.g., S3)?

5. Should the non-progress detection threshold be configurable?

6. Should the repeated tool request detection threshold be configurable?

7. Should the model drift detection be based on statistical analysis or rule-based?

8. Should the FSM support hot-swapping the planning strategy at runtime?

9. Should the plan adaptation support rollback (undoing adaptations)?

10. Should the budget exhaustion trigger human approval or automatic termination?

11. Should the FSM support multiple human approvers (e.g., for critical operations)?

12. Should the forced termination trigger cleanup of in-progress external requests (e.g., HTTP calls)?

## Next steps

1. Push the implementation notes and specification chapters to the remote branch.
2. Create a single PR for all Phase 3 work.
3. Review and merge the PR.
4. Proceed to Phase 4 implementation.
