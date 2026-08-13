---
title: "Phase 4 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-04
  - implementation
  - integration-tests
  - host-function-testing
  - wasi-testing
  - tenant-isolation-testing
  - residue-testing
aliases:
  - "M5-P4-4.4 Implementation"
---

# Phase 4 Integration Tests Implementation

## Overview

This note documents the implementation of Section 4.4 (Phase 4 Integration Tests) from
[Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
which defines the integration test objectives, scenarios, evidence
requirements, and cross-milestone compatibility checks for synchronous
host functions, WASI restrictions, and tenant isolation.

## Subtask 4.4.1.1: Verify canonical successful flow

### Implementation

Defined test objectives for the canonical successful flow:

**Test objectives:**
1. **Canonical flow**: Host function evaluation, WASI profile enforcement,
   and instance creation modes operate successfully when all preconditions
   defined in Contract And Data Model and Behavior And Integration are
   satisfied.
2. **Failure handling**: Malformed, incompatible, stale, duplicate, and
   boundary-limit inputs produce stable, bounded diagnostics and leave
   no unauthorized residue.
3. **Instance mode enforcement**: Every instance creation mode preserves
   the `fresh` oracle on every isolation invariant, including under
   concurrent cross-tenant load.
4. **Tenant isolation**: Memory, state, capability, and resource separation
   hold under adversarial scenarios, including deliberate violation attempts.

**Successful flow tests:**
Tests MUST exercise at least one host function, at least one WASI-enabled
guest, and at least one instance creation mode per mode defined in
[Instance modes](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

Test scenarios:
- **Host function evaluation**: Register eligible host function; verify
  successful invocation with correct output
- **WASI profile enforcement**: Enable WASI interfaces through guest
  profile and host policy; verify interfaces are bound to instance
- **Instance mode enforcement**: Create instances in each mode; verify
  isolation invariants hold

### Design decisions

1. **Tests verify observable contracts, not private structure**: Tests
   are defined in terms of external behavior (output, isolation invariants)
   rather than internal implementation details. This ensures tests remain
   valid across implementation changes.

2. **All instance modes are tested**: The four instance modes (fresh,
   reset, pooled, agent-pinned) are all tested, ensuring that each mode
   preserves the `fresh` oracle on isolation invariants.

3. **WASI enablement is tested end-to-end**: Tests verify that WASI
   interfaces are enabled through both guest profile and host policy,
   and that interfaces are correctly bound to instances.

## Subtask 4.4.1.2: Verify failure handling

### Implementation

Defined failure handling tests for all failure outcomes:

| Failure | Test Trigger | Expected Diagnostic |
|---------|-------------|-------------------|
| Malformed | Invalid host function record or invocation context | `host-function.malformed` |
| Ineligible | Function fails eligibility criteria | `host-function.ineligible` |
| Unresolved import | Guest module declares unresolvable import | `import.unresolved` |
| Namespace collision | Imports collide between namespaces | `import.namespace-collision` |
| Policy denied | Guest profile requests interface host policy denies | `wasi.policy-denied` |
| Interface unknown | Guest profile requests interface not in closed list | `wasi.interface-unknown` |
| Tenant validation failed | Missing or invalid tenant identifier | `tenant.validation-failed` |
| Isolation violation | Cross-tenant access attempt | `isolation.violation` |
| Bound exceeded | Function exceeds declared resource bound | `bound.exceeded` |
| Cancellation timeout | Function does not respond to cancellation | `cancellation.timeout` |
| Context missing | Required field in invocation context missing | `invocation.context-missing` |
| Deadline exceeded | Invocation exceeds `deadline_ms` | `invocation.deadline-exceeded` |
| Output limit exceeded | Invocation exceeds `output_limit_bytes` | `invocation.output-limit` |
| Grant missing | Invocation lacks capability grant | `invocation.grant-missing` |
| Mode isolation violation | Instance mode relaxes isolation invariant | `instance.mode-isolation-violation` |
| Reset leakage detected | State leaks into `reset` instance | `instance.reset-leakage-detected` |
| Residue violation | Observable residue persists after invocation | `residue.violation` |

Each test MUST verify that error code and diagnostic message match expected values.

### Design decisions

1. **Tests cover all failure outcomes**: The seventeen failure outcomes
   are all tested, ensuring comprehensive coverage of the failure domain.

2. **Error codes and diagnostics are verified together**: Tests verify
   both the error code and the diagnostic message, ensuring that
   implementations provide meaningful error information.

3. **Bounded diagnostics are verified**: Tests verify that diagnostics
   do not expose secrets, internal implementation details, or
   tenant-specific state beyond `tenant_id`.

## Subtask 4.4.1.3: Verify timeout, cancellation, unavailable dependency, and retry behavior

### Implementation

Defined tests for timeout, cancellation, unavailable dependency, and retry
behavior. Tests MUST verify that these scenarios leave no unauthorized or
partial state.

Test scenarios:
- **Timeout**: Trigger invocation timeout; verify all effects rolled back,
  `invocation.deadline-exceeded` emitted, no residue persists
- **Cancellation**: Trigger invocation cancellation; verify all effects
  rolled back, `invocation.cancelled` emitted, no residue persists
- **Unavailable dependency**: Make host function dependency unavailable;
  verify `host-function.unavailable` emitted, no unauthorized state left
- **Retry**: Trigger retry of failed invocation; verify idempotency or
  structured partial result handling, no duplicated effects

Each test MUST verify that no unauthorized or partial state is left after
the test.

### Design decisions

1. **Timeout and cancellation always roll back**: Tests verify that
   timeout and cancellation result in full rollback of all effects.
   This ensures that partial state never persists.

2. **Retry is tested for idempotency**: Tests verify that retries do
   not duplicate effects. This is critical for reliability and
   correctness.

3. **Unavailable dependency is tested**: Tests verify that when a
   dependency is unavailable, the host function fails gracefully with
   appropriate diagnostic and no unauthorized state.

## Subtask 4.4.1.4: Run cross-milestone compatibility tests

### Implementation

Defined four cross-milestone compatibility tests:

| Milestone | Fixture Source | Regression Check |
|-----------|---------------|-----------------|
| 1 | [Guest SDK Contracts Fixtures And Milestone Acceptance](../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md) | All M1 fixtures pass |
| 2 | Phase 1-5 plans under [Milestone 2](../../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/) | All M2 fixtures pass |
| 3 | Phase 1-5 plans under [Milestone 3](../../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/) | All M3 fixtures pass |
| 4 | Phase 1-5 plans under [Milestone 4](../../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/) | All M4 fixtures pass |

If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Design decisions

1. **Cross-milestone tests are mandatory**: The phase cannot be promoted
   to `status: normative` without passing cross-milestone fixtures.
   This ensures M5 does not introduce regressions in earlier milestones.

2. **Regressions trigger mandatory revision**: If a regression is
   detected, the affected milestone MUST be revised and re-validated.
   This prevents accumulating technical debt.

3. **Fixture sources are explicitly documented**: Each milestone's
   fixtures are traced to their source chapter or planning directory.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Contract And Data Model](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.2: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Behavior And Integration](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.3: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Failure Evidence And Operational Notes](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Guest SDK: [Guest SDK Contracts Fixtures And Milestone Acceptance](../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should integration tests include performance benchmarks? The spec
   defines functional tests but does not address performance requirements
   for host function evaluation latency or instance creation overhead.

2. How should test evidence be stored and retrieved? The spec requires
   recording test evidence but does not specify the storage format or
   retrieval mechanism for test reports.

3. Can integration tests be run in parallel? The spec does not address
   whether the successful flow tests can be run in parallel or must
   be run sequentially.
