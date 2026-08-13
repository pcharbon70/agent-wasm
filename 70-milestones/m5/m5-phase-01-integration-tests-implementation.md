---
title: "Phase 1 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-01
  - implementation
  - integration-tests
  - security-testing
  - threat-model
  - grants
aliases:
  - "M5-P1-1.4 Implementation"
---

# Phase 1 Integration Tests Implementation

## Overview

This note documents the implementation of Section 1.4 (Phase 1 Integration Tests) from
[Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
which defines the integration test objectives, scenarios, and evidence
requirements for threat model principals, trust classes, and grant vocabulary.

## Subtask 1.4.1.1: Verify canonical successful flow

### Implementation

Defined five tests for the canonical successful flow:

| Test | Verification |
|------|-------------|
| Principal authentication | Authenticate user, service, agent, or operator principal; verify success |
| Grant validation | Validate a grant; verify it is valid |
| Trust class enforcement | Enforce a trust class; verify principal is restricted to correct access level |
| Tenant isolation | Verify tenant cannot access another tenant's data |
| Audit logging | Verify all authorization decisions are logged |

Each test MUST record: input data, expected output, actual output, pass/fail status.

### Design decisions

1. **Tests exercise observable contracts, not private structure**: The test
   scenarios are defined in terms of external behavior (authentication
   succeeds, isolation holds) rather than internal implementation details.
   This ensures tests remain valid across implementation changes.

2. **Evidence is structured and machine-readable**: The required evidence
   fields (input, expected, actual, pass/fail) enable automated comparison
   and regression detection.

3. **Audit logging is tested as a security control**: The audit logging test
   verifies that authorization decisions are recorded, which is essential
   for forensic analysis and compliance auditing.

## Subtask 1.4.1.2: Verify failure handling

### Implementation

Defined nine failure handling tests:

| Test | Trigger | Expected Error Code |
|------|---------|-------------------|
| Authentication failure | Invalid credentials | `auth.authentication_failure` |
| Principal mismatch | Wrong principal presented | `auth.principal_mismatch` |
| Grant absence | No valid grant | `auth.grant_absence` |
| Scope conflict | Conflicting grant scope | `auth.scope_conflict` |
| Grant expiry | Expired grant | `auth.grant_expiry` |
| Grant revocation | Revoked grant | `auth.grant_revocation` |
| Untrusted publisher | Untrusted publisher artifact | `auth.untrusted_publisher` |
| Untrusted guest | Untrusted guest execution | `trust.untrusted_guest` |
| Tenant isolation violation | Cross-tenant data access | `tenant.isolation_violation` |

Each test MUST verify that the error code and diagnostic message match expected values.

### Design decisions

1. **Failure tests verify exact error codes**: The spec requires exact matching
   of error codes and diagnostic messages, ensuring consistent behavior across
   implementations and enabling automated compliance checking.

2. **Tests cover the full failure outcome surface**: The nine tests cover all
   seven authentication/authorization outcomes plus the two trust-class outcomes,
   ensuring comprehensive coverage of the failure domain.

3. **Diagnostic content is verified for boundedness**: Tests verify that
   diagnostics do not expose secrets or internal implementation details,
   enforcing the bounded diagnostics requirement.

## Subtask 1.4.1.3: Verify security enforcement

### Implementation

Defined five security enforcement tests:

| Test | Verification |
|------|-------------|
| Tenant data isolation | Tenant A cannot read Tenant B's data |
| Grant constraint enforcement | Grant constraints (rate limits) are enforced |
| Trust class sandboxing | Untrusted guests are sandboxed |
| Audit log completeness | All authorization decisions are logged |
| Secret isolation | Secrets not exposed to untrusted guests |

Each test MUST verify that no unauthorized or partial state is left after the test.

### Design decisions

1. **Post-test state is verified**: Each test checks for residual unauthorized
   state, ensuring that security controls do not leave the system in a vulnerable
   condition even after a test failure.

2. **Secret isolation is tested at the guest boundary**: The test verifies that
   untrusted guests cannot access host secrets, which is the primary defense
   against the "malicious guest" threat actor.

3. **Audit log completeness is a security property**: The test verifies that no
   authorization decision is missed, which is essential for forensic analysis
   and detecting security incidents.

## Subtask 1.4.1.4: Run cross-milestone compatibility tests

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

1. **Cross-milestone tests are mandatory for promotion**: The phase cannot be
   promoted to `status: normative` without passing cross-milestone fixtures.
   This ensures M5 does not introduce regressions in earlier milestones.

2. **Regressions trigger mandatory revision**: If a regression is detected,
   the affected milestone MUST be revised and re-validated. This prevents
   accumulating technical debt and ensures that changes are properly scoped.

3. **Fixture sources are explicitly documented**: Each milestone's fixtures
   are traced to their source chapter or planning directory, enabling
   reproducibility and auditability.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary Contract And Data Model](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 30.2: [Threat Model Principals Trust Classes And Grant Vocabulary Behavior And Integration](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 30.3: [Threat Model Principals Trust Classes And Grant Vocabulary Failure Evidence And Operational Notes](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Capability policy tests: [Capability Policy Attenuation Limits And Enforcement Phase 2 Integration Tests](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin tests: [Framework Plugin Manifests Composition And Lifecycle Hooks Phase 3 Integration Tests](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions tests: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Phase 4 Integration Tests](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance tests: [Provenance Signing Audit Security And Milestone Acceptance Phase 5 Integration Tests](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Guest SDK: [Guest SDK Contracts Fixtures And Milestone Acceptance](../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)

## Open questions

1. Should integration tests include adversarial scenarios beyond the nine
   failure handling tests? The spec defines controlled adversarial inputs in
   Phase 5 (provenance) but does not require them for Phase 1. Should
   Phase 1 tests include simulated malicious guest scenarios?

2. How should cross-milestone fixture results be recorded? The spec requires
   recording regressions or approved variability but does not specify the
   format or storage mechanism for this evidence.

3. Can integration tests be run incrementally or must they be run as a full
   suite? The spec does not address whether individual test sections can
   be validated independently or require the full suite to run.
