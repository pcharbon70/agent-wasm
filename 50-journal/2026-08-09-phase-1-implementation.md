---
title: "2026-08-09 Phase 1 Implementation"
kind: journal
created: "2026-08-09"
tags:
  - milestone-07
  - phase-01
  - implementation
  - journal
aliases:
  - "M7-P1 Journal 2026-08-09"
---

# 2026-08-09 Phase 1 Implementation

## Overview

This journal entry documents the implementation of Phase 1 of Milestone 7:
**Provider-Neutral Model Requests, Responses, Streaming, and Usage**.

## Work performed

### PR Merge

- Merged PR #26 (spec-41: Phase 1 - Provider-Neutral Model Requests Responses Streaming And Usage)
- Checked out main and synced with remote
- Created new branch `milestone-07-phase-01-implementation` for implementing Phase 1 section by section

### Implementation notes created

Created four implementation notes documenting each section of Phase 1:

1. **[Phase 1 Contract And Data Model Implementation](../20-notes/m7-phase-01-contract-and-data-model-implementation.md)**
   - Documents Subtask 1.1.1.1: Model request identity and provider constraints (13 fields)
   - Documents Subtask 1.1.1.2: Response normalization (12 fields)
   - Documents Subtask 1.1.1.3: Streaming normalization (8 fields) and usage tracking (11 fields)

2. **[Phase 1 Behavior And Integration Implementation](../20-notes/m7-phase-01-behavior-and-integration-implementation.md)**
   - Documents Subtask 1.2.1.1: Provider adapter registration and capability mapping (5 capabilities, 5 grants)
   - Documents Subtask 1.2.1.2: Model resolution, streaming normalization, and signal conversion (8 signals)
   - Documents Subtask 1.2.1.3: Cancellation, retry classification (10 failure types), and outcome definitions (8 outcomes)

3. **[Phase 1 Failure Evidence And Operational Notes Implementation](../20-notes/m7-phase-01-failure-evidence-and-operational-notes-implementation.md)**
   - Documents Subtask 1.3.1.1: Failure outcomes (28 diagnostics across 7 categories)
   - Documents Subtask 1.3.1.2: Bounded diagnostics (8 required fields) and evidence emission (7 evidence types)
   - Documents Subtask 1.3.1.3: Implementation-defined choices (5 choices) and deferred work (4 items)

4. **[Phase 1 Integration Tests Implementation](../20-notes/m7-phase-01-integration-tests-implementation.md)**
   - Documents Subtask 1.4.1.1: Successful flow tests (20 tests)
   - Documents Subtask 1.4.1.2: Failure handling tests (22 tests)
   - Documents Subtask 1.4.1.3: Timeout and cancellation tests (9 tests)
   - Documents Subtask 1.4.1.4: Cross-milestone compatibility tests (11 fixture scopes from 6 milestones)

## Key design decisions

### Contract and data model

1. **Deterministic `request_id`**: Enables idempotent retry by producing the same `request_id` for identical request payloads.

2. **Agent-originated vs. host-originated fields**: Separation of concerns between agent-provided data and host-managed data.

3. **Provider adapter identifiers**: Use string identifiers (e.g., `openai`, `anthropic`, `local`) rather than full adapter paths to keep requests portable.

4. **Response normalization**: Provider-specific responses are normalized into a common format before being recorded as durable effects.

5. **Bounded streaming observations**: Streaming events do NOT create durable effects until the response is finalized.

### Behavior and integration

1. **Framework plugin model**: Provider adapters behave as framework plugins: isolated in their own tenant, subject to capability policy.

2. **8-step request processing**: Validate -> Resolve provider -> Check budget -> Create adapter request -> Start streaming -> Normalize events -> Finalize response -> Record usage.

3. **Best-effort cancellation**: If the adapter does not support cancellation, the host MUST wait for the request to complete or timeout.

4. **Retry classification**: The host does not retry failures that are unlikely to succeed. Only failures where the agent can take corrective action are retryable.

5. **Late response acceptance**: Late responses are accepted but marked as late in diagnostics to avoid losing work while still providing visibility into performance issues.

### Failure evidence

1. **Atomic rejection**: Every failure outcome MUST reject without creating partial request or response state.

2. **Consistent diagnostic format**: All diagnostics follow a consistent naming convention (`model.request.*` and `model.response.*`).

3. **Cross-tenant rejection**: Cross-tenant tool access and result sharing are rejected outright to prevent authority leaks.

4. **Tamper-evident evidence**: The `evidence_digest` field enables downstream systems to verify that the evidence record has not been tampered with after creation.

### Integration tests

1. **Observable behavior**: Tests verify observable behavior (signals, durable journal entries) rather than private implementation structure.

2. **Comprehensive failure coverage**: Tests cover all failure outcome categories: malformed, incompatible, conflicting, unauthorized, exhausted, unavailable.

3. **Cross-milestone compatibility**: Tests cover 11 fixture scopes from 6 milestones to ensure Phase 1 does not introduce regressions.

4. **Signed evidence**: All evidence records are signed according to the provenance and audit mechanism.

## Cross-references

### Specification chapters

- [41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md)
- [41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md)
- [41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md)
- [41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md](../60-specification/41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md)

### Earlier chapters

- [14-deterministic-reducer-semantics-and-milestone-acceptance.md](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- [10-signals-causality-routing-and-delivery.md](../60-specification/10-signals-causality-routing-and-delivery.md)
- [26-atomic-state-journal-and-directive-outbox-commits.md](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- [32-framework-plugin-manifests-composition-and-lifecycle-hooks.md](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- [34-provenance-signing-audit-security-and-milestone-acceptance.md](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

## Open questions

1. Should streaming events be recorded in the durable journal even though they are bounded observations?

2. How should cross-tenant tool access be validated? The current design rejects cross-tenant tool access outright.

3. What is the implementation-defined maximum cost unit? The spec uses "implementation-defined units".

4. Should the host retry on `adapter.error` immediately or wait for the agent to signal readiness?

5. How should the host handle provider-specific error codes? The current design normalizes them into generic diagnostics.

6. Should implementation-defined choices have default values or be required?

## Next steps

1. Push the implementation notes to the remote branch.
2. Create a single PR for all implementation notes.
3. Review and merge the PR.
4. Proceed to Phase 2 implementation.
