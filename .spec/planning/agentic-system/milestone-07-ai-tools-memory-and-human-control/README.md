# Milestone 7 - AI, Tools, Memory, And Human Control

Layer provider-neutral model access, tools, retrieval, reasoning strategies, memory projections, approvals, quotas, and secret leases above the stable agent runtime.

Current status: planned; all phases and tasks are unchecked.

## Purpose

Provide the ordered, section-sized implementation work and evidence needed to
satisfy this milestone without selecting language-specific internals.

## What belongs here

Only phase plans and milestone-wide assumptions for ai, tools, memory, and human control.

## Dependencies And Entry Gate

- Milestone 6 supports durable result-bearing coordination and lifecycle.
- Milestone 5 policy can authorize high-authority effects and human approvals.

## Phase Order

1. [Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
2. [Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
3. [Phase 3 - Direct FSM Tool-Loop And Planning Strategies](phase-03-direct-fsm-tool-loop-and-planning-strategies.md)
4. [Phase 4 - Threads Checkpoints Memory Approvals Quotas And Secret Leases](phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md)
5. [Phase 5 - Agentic Workflows Provenance Safety And Milestone Acceptance](phase-05-agentic-workflows-provenance-safety-and-milestone-acceptance.md)

## Planned Artifacts

- Model, tool, retrieval, and connector effect contracts
- Reasoning strategy and continuation catalog
- Conversation, memory, approval, provenance, and safety acceptance corpus

## Shared Conventions

- Phases use `N`; sections use `N.M`; tasks use `N.M.K`; subtasks use
  `N.M.K.L`.
- Every checklist item remains unchecked until implementation evidence exists.
- Every phase, section, and task has an immediate description.
- Every phase ends in a final integration-testing section.
- Implement and commit one section at a time.

## Shared Assumptions And Defaults

- LLM reasoning is a replaceable strategy, not the runtime kernel.
- Prompts, secrets, and large payloads use redacted or access-controlled evidence.
- Human decisions re-enter the system as causally linked signals.

## Exit Gate

All five phase integration sections pass together, their evidence is retained,
and no unresolved failure changes an earlier contract or trust assumption.

## Index

### Subdirectories

- None yet.

### Documents

- [Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage](phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md) — implements and verifies this ordered phase.
- [Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md) — implements and verifies this ordered phase.
- [Phase 3 - Direct FSM Tool-Loop And Planning Strategies](phase-03-direct-fsm-tool-loop-and-planning-strategies.md) — implements and verifies this ordered phase.
- [Phase 4 - Threads Checkpoints Memory Approvals Quotas And Secret Leases](phase-04-threads-checkpoints-memory-approvals-quotas-and-secret-leases.md) — implements and verifies this ordered phase.
- [Phase 5 - Agentic Workflows Provenance Safety And Milestone Acceptance](phase-05-agentic-workflows-provenance-safety-and-milestone-acceptance.md) — implements and verifies this ordered phase.

## Maintaining This Index

Keep phase numbering contiguous, preserve dependency order, and update the
master roadmap when milestone scope or exit criteria change.
