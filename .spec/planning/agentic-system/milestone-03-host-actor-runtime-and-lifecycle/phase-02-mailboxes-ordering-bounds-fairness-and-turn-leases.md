# Phase 2 - Mailboxes Ordering Bounds Fairness And Turn Leases

Back to milestone: [README](./README.md)

- [x] 2 Phase - Provide one-at-a-time committed turns per agent while bounding queued work and making overload behavior explicit.

  This phase is complete only when its contracts, behavior, failure semantics,
  and integration evidence are reviewable without relying on a host-language
  implementation detail.

## 2.1 Section - Contract And Data Model

- [x] 2.1 Section - Establish contract and data model for mailboxes ordering bounds fairness and turn leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.1.1 Task - Complete the contract and data model work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.1.1.1 Subtask - Define mailbox entries as authenticated signal references with tenant, agent, priority class, enqueue time, deadline, and delivery metadata.
    - [x] 2.1.1.2 Subtask - Define deterministic ordering within priority classes and explicit fairness between classes.
    - [x] 2.1.1.3 Subtask - Define mailbox count, byte, age, per-source, and per-tenant bounds.

## 2.2 Section - Behavior And Integration

- [x] 2.2 Section - Establish behavior and integration for mailboxes ordering bounds fairness and turn leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.2.1 Task - Complete the behavior and integration work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.2.1.1 Subtask - Define reject, defer, coalesce, supersede, or dead-letter behavior by signal class when a bound is reached.
    - [x] 2.2.1.2 Subtask - Define per-agent turn leases with owner, revision, expiry, renewal, fencing token, and release behavior.
    - [x] 2.2.1.3 Subtask - Define duplicate workers, expired leases, stale fencing tokens, cancellation races, and host shutdown outcomes.

## 2.3 Section - Failure Evidence And Operational Notes

- [x] 2.3 Section - Establish failure evidence and operational notes for mailboxes ordering bounds fairness and turn leases.

  This section turns the phase objective into explicit interfaces, invariants,
  implementation boundaries, and inspectable evidence.

  - [x] 2.3.1 Task - Complete the failure evidence and operational notes work.

    This task is the section-sized implementation and commit boundary.

    - [x] 2.3.1.1 Subtask - Define malformed, incompatible, conflicting, unauthorized, exhausted, and unavailable outcomes relevant to mailboxes ordering bounds fairness and turn leases.
    - [x] 2.3.1.2 Subtask - Emit bounded diagnostics and evidence that identify the phase contract, profile, and failed boundary without exposing secrets.
    - [x] 2.3.1.3 Subtask - Document implementation-defined choices, deferred work, and any result that would invalidate an earlier milestone assumption.

## 2.4 Section - Phase 2 Integration Tests

- [x] 2.4 Section - Verify mailboxes ordering bounds fairness and turn leases across its real dependency boundaries.

  This section proves the phase works as an integrated behavior and preserves
  reproducible evidence for later milestone and release gates.

  - [x] 2.4.1 Task - Run the phase integration scenarios.

    The scenarios must exercise observable contracts rather than private
    implementation structure.

    - [x] 2.4.1.1 Subtask - Verify the canonical successful flow and retained evidence for mailboxes ordering bounds fairness and turn leases.
    - [x] 2.4.1.2 Subtask - Verify malformed, incompatible, stale, duplicate, and boundary-limit inputs fail with stable diagnostics where applicable.
    - [x] 2.4.1.3 Subtask - Verify timeout, cancellation, unavailable dependency, and retry behavior leave no unauthorized or partial state.
    - [x] 2.4.1.4 Subtask - Run all earlier milestone fixtures affected by this phase and record regressions or approved variability.

