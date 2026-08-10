# Milestone 3 - Host Actor Runtime And Lifecycle

Construct the host-owned live actor cell that serializes turns, invokes Extism reducers, manages lifecycle, and converts external events into signals.

Current status: phase 1-5 complete; milestone 3 complete.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for host actor runtime and lifecycle.

## Dependencies And Entry Gate

- Milestone 2 reducer semantics and conformance vectors pass in a local reference harness.
- The first Extism runtime profile is available to the host.

## Phase Order

1. [Phase 1 - Extism Invocation Boundary Instances And Output Validation](phase-01-extism-invocation-boundary-instances-and-output-validation.md)
2. [Phase 2 - Mailboxes Ordering Bounds Fairness And Turn Leases](phase-02-mailboxes-ordering-bounds-fairness-and-turn-leases.md)
3. [Phase 3 - Agent Registry Activation Cancellation And Completion](phase-03-agent-registry-activation-cancellation-and-completion.md)
4. [Phase 4 - Sensors Schedules Timers And External Signal Ingress](phase-04-sensors-schedules-timers-and-external-signal-ingress.md)
5. [Phase 5 - Single-Agent Host Flow And Milestone Acceptance](phase-05-single-agent-host-flow-and-milestone-acceptance.md)

## Planned Artifacts

- Host invocation and instance lifecycle interfaces
- Mailbox, registry, lifecycle, sensor, and scheduling interfaces
- Single-agent runtime acceptance scenarios

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- Each agent commits at most one turn at a time.
- Fresh instances define reference isolation behavior.
- Single-node operation is the first durability and lifecycle target.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Extism Invocation Boundary Instances And Output Validation](phase-01-extism-invocation-boundary-instances-and-output-validation.md) — implements and verifies this ordered phase.
- [Phase 2 - Mailboxes Ordering Bounds Fairness And Turn Leases](phase-02-mailboxes-ordering-bounds-fairness-and-turn-leases.md) — implements and verifies this ordered phase.
- [Phase 3 - Agent Registry Activation Cancellation And Completion](phase-03-agent-registry-activation-cancellation-and-completion.md) — implements and verifies this ordered phase.
- [Phase 4 - Sensors Schedules Timers And External Signal Ingress](phase-04-sensors-schedules-timers-and-external-signal-ingress.md) — implements and verifies this ordered phase.
- [Phase 5 - Single-Agent Host Flow And Milestone Acceptance](phase-05-single-agent-host-flow-and-milestone-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
