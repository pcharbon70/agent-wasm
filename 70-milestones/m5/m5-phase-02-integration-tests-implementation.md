---
title: "Phase 2 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-02
  - implementation
  - integration-tests
  - policy-testing
  - attenuation-testing
  - approval-workflow
aliases:
  - "M5-P2-2.4 Implementation"
---

# Phase 2 Integration Tests Implementation

## Overview

This note documents the implementation of Section 2.4 (Phase 2 Integration Tests) from
[Phase 2 - Capability Policy Attenuation Limits And Enforcement](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-02-capability-policy-attenuation-limits-and-enforcement.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[31-capability-policy-attenuation-limits-and-enforcement.md](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
which defines the integration test objectives, scenarios, and evidence
requirements for capability policy attenuation, limits, and enforcement.

## Subtask 2.4.1.1: Verify canonical successful flow

### Implementation

Defined five tests for the canonical successful flow:

| Test | Verification |
|------|-------------|
| Policy evaluation | Evaluate policy input; verify decision is `allow` or `attenuated` |
| Attenuation enforcement | Apply attenuation restrictions; verify capability executes within granted boundaries |
| Approval workflow | Trigger `approval-required`; verify workflow suspends execution until approval |
| Policy caching | Verify policy decisions are cached and invalidated when input changes |
| Revocation | Revoke grant; verify cached decisions invalidated and new invocations denied |

Each test MUST record: input data, expected output, actual output, pass/fail status.

### Design decisions

1. **Tests cover the full decision surface**: The five tests cover allow,
   attenuated, approval-required, caching, and revocation, ensuring that
   all major policy outcomes are verified.

2. **Approval workflow is tested as a suspension mechanism**: The test
   verifies that execution is suspended until approval is received,
   which is the primary security property of the approval workflow.

3. **Policy caching is tested for correctness and invalidation**: The test
   verifies both that caching works (performance) and that invalidation
   occurs on input changes (correctness).

## Subtask 2.4.1.2: Verify failure handling

### Implementation

Defined ten failure handling tests:

| Test | Trigger | Expected Error Code |
|------|---------|-------------------|
| Malformed input | Malformed policy input | `policy.malformed_input` |
| Grant absence | No valid grant | `policy.grant_absent` |
| Grant expiry | Expired grant | `policy.grant_expired` |
| Grant revocation | Revoked grant | `policy.grant_revoked` |
| Trust class insufficient | Insufficient trust class | `policy.trust_class_insufficient` |
| Artifact untrusted | Untrusted artifact | `policy.artifact_untrusted` |
| Byte count exceeded | Attenuated capability exceeds byte limit | `policy.byte_count_exceeded` |
| Duration exceeded | Attenuated capability exceeds duration | `policy.duration_exceeded` |
| Budget exceeded | Attenuated capability exceeds budget | `policy.budget_exceeded` |
| Approval deadline exceeded | Approval deadline expires without approval | `policy.approval_deadline_exceeded` |

Each test MUST verify that error code and diagnostic message match expected values.

### Design decisions

1. **Tests cover all limit enforcement scenarios**: The three limit
   enforcement tests (byte count, duration, budget) verify that runtime
   enforcement works correctly, which is distinct from policy evaluation.

2. **Approval deadline is tested as a failure mode**: The test verifies
   that approval deadlines are enforced and that missing approval results
   in denial, preventing operational deadlocks.

3. **Error codes and diagnostics are verified together**: Tests verify
   both the error code and the diagnostic message, ensuring that
   implementations provide meaningful error information.

## Subtask 2.4.1.3: Verify security enforcement

### Implementation

Defined five security enforcement tests:

| Test | Verification |
|------|-------------|
| Tenant isolation | Tenant cannot access another tenant's data through policy decisions |
| Attenuation enforcement | Attenuated capabilities execute within granted boundaries |
| Policy versioning | Decisions invalidated when policy version changes |
| Revocation | Revoked grants prevent new invocations |
| Audit logging | All policy decisions and violations logged |

Each test MUST verify that no unauthorized or partial state is left after the test.

### Design decisions

1. **Tenant isolation is tested through policy**: The test verifies that
   policy decisions respect tenant boundaries, which is the primary
   defense against cross-tenant data access.

2. **Attenuation enforcement is tested at runtime**: The test verifies
   that attenuated capabilities are actually restricted at runtime, not
   just in policy evaluation. This ensures that enforcement works as
   designed.

3. **Policy versioning is tested for cache invalidation**: The test
   verifies that cached decisions are invalidated when policy version
   changes, preventing stale policy from being applied.

## Subtask 2.4.1.4: Run cross-milestone compatibility tests

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
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement Contract And Data Model](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.2: [Capability Policy Attenuation Limits And Enforcement Behavior And Integration](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.3: [Capability Policy Attenuation Limits And Enforcement Failure Evidence And Operational Notes](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin composition: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Guest SDK: [Guest SDK Contracts Fixtures And Milestone Acceptance](../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Open questions

1. Should integration tests include performance benchmarks? The spec
   defines functional tests but does not address performance requirements
   for policy evaluation latency or attenuation enforcement overhead.

2. How should test evidence be stored and retrieved? The spec requires
   recording test evidence but does not specify the storage format or
   retrieval mechanism for test reports.

3. Can integration tests be run in parallel? The spec does not address
   whether the five successful flow tests can be run in parallel or
   must be run sequentially.
