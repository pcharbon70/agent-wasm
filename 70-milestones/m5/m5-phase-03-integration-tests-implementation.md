---
title: "Phase 3 Integration Tests Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-03
  - implementation
  - integration-tests
  - plugin-testing
  - composition-testing
  - lifecycle-testing
aliases:
  - "M5-P3-3.4 Implementation"
---

# Phase 3 Integration Tests Implementation

## Overview

This note documents the implementation of Section 3.4 (Phase 3 Integration Tests) from
[Phase 3 - Framework Plugin Manifests Composition And Lifecycle Hooks](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-03-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[32-framework-plugin-manifests-composition-and-lifecycle-hooks.md](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
which defines the integration test objectives, scenarios, evidence
requirements, and cross-milestone compatibility checks for framework plugin
manifests composition and lifecycle hooks.

## Subtask 3.4.1.1: Verify canonical successful flow

### Implementation

Defined test objectives for the canonical successful flow:

**Test objectives:**
1. **Canonical successful flow**: Every lifecycle operation completes
   end-to-end without error when manifest, artifacts, grants, and
   dependencies are all valid and available.
2. **Failure handling**: Every failure outcome defined in failure semantics
   is detected, classified, and reported with a stable diagnostic when
   the triggering condition is present.
3. **Lifecycle enforcement**: The lifecycle transition graph is enforced,
   and no unauthorized or partially-loaded state persists after any failure.
4. **Trust-tier separation**: Every trust tier rule is enforced at runtime,
   and no artifact is loaded outside its declared tier.
5. **Cross-milestone compatibility**: All fixtures from earlier milestones
   that interact with the plugin registry remain functional after this
   phase is integrated.

**Successful flow tests:**
Each lifecycle operation (install, validate, approve, enable, disable,
upgrade, migrate, rollback, remove) MUST be tested end-to-end. Tests
MUST capture observable outcomes (registry state, audit log entries,
diagnostics) as evidence.

### Design decisions

1. **Tests verify observable contracts, not private structure**: Tests
   are defined in terms of external behavior (registry state, audit log,
   diagnostics) rather than internal implementation details. This ensures
   tests remain valid across implementation changes.

2. **All lifecycle operations are tested**: The nine lifecycle operations
   form a DAG, and tests verify that each operation completes successfully
   when preconditions are satisfied.

3. **Evidence is structured and machine-readable**: Required evidence
   includes registry state, audit log entries, and diagnostics. This
   enables automated comparison and regression detection.

## Subtask 3.4.1.2: Verify failure handling

### Implementation

Defined failure handling tests for all twelve failure outcomes:

| Failure | Test Trigger | Expected Diagnostic |
|---------|-------------|-------------------|
| Malformed manifest | Invalid manifest schema | `plugin.malformed_manifest` |
| Incompatible version | Unsupported manifest version | `plugin.incompatible_version` |
| Name conflict | Two plugins share resolved name | `plugin.name_conflict` |
| Route conflict | Two routes match same pattern at same priority | `plugin.route_conflict` |
| Namespace conflict | Two plugins declare same namespace | `plugin.namespace_conflict` |
| Schema conflict | Conflicting schemas with same id | `plugin.schema_conflict` |
| Migration conflict | Incompatible migrations on same namespace | `plugin.migration_conflict` |
| Capability conflict | Trust model cannot satisfy all grants | `plugin.capability_conflict` |
| Lifecycle conflict | Publisher-owned claims conflict | `plugin.lifecycle_conflict` |
| Unauthorized | Caller lacks trust class | `plugin.unauthorized` |
| Exhausted | Resources exhausted | `plugin.exhausted` |
| Unavailable | Dependency unavailable | `plugin.unavailable` |

Additional failure tests:
- `plugin.missing_dependency`: Referenced artifact or capability missing
- `plugin.version_conflict`: Requested version conflicts with installed
- `plugin.circular_dependency`: Circular dependency among plugins
- `plugin.ambiguous_route`: Two routes match same pattern at same priority
- `plugin.orphaned_state`: Active state references after removal
- `plugin.revoked_publisher`: Publisher's trust class revoked

Each test MUST verify that error code and diagnostic message match expected values.

### Design decisions

1. **Tests cover all failure outcomes**: The twelve primary failure
   outcomes plus six additional outcomes are all tested, ensuring
   comprehensive coverage of the failure domain.

2. **Error codes and diagnostics are verified together**: Tests verify
   both the error code and the diagnostic message, ensuring that
   implementations provide meaningful error information.

3. **Bounded diagnostics are verified**: Tests verify that diagnostics
   do not expose secrets, internal implementation details, or
   cross-plugin information.

## Subtask 3.4.1.3: Verify lifecycle enforcement and trust-tier separation

### Implementation

Defined tests for lifecycle enforcement and trust-tier separation:

**Lifecycle enforcement tests:**
- Verify that invalid lifecycle transitions are rejected (e.g., enable
  without install)
- Verify that no unauthorized or partially-loaded state persists after
  any failure
- Verify that each completed transition is recorded in lifecycle audit log

**Trust-tier separation tests:**
- Verify that `untrusted-guest` artifacts are sandboxed within Extism
  invocation boundary
- Verify that `reviewed-preparation` artifacts require review evidence
  before execution
- Verify that `privileged-host` artifacts are restricted to approved
  operations and cannot modify manifest or elevate trust tier
- Verify that no artifact is loaded outside its declared tier

Each test MUST verify that no unauthorized or partial state is left
after the test.

### Design decisions

1. **Lifecycle transitions are tested for invalid cases**: Tests verify
   that invalid transitions (e.g., enable without install) are rejected,
   which is the primary defense against unauthorized code execution.

2. **Trust tiers are tested at runtime**: Tests verify that artifacts
   are actually restricted to their declared trust tier at runtime,
   not just in manifest validation.

3. **Post-test state is verified**: Each test checks for residual
   unauthorized state, ensuring that security controls do not leave
   the system in a vulnerable condition.

## Subtask 3.4.1.4: Run cross-milestone compatibility tests

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
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks Contract And Data Model](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.2: [Framework Plugin Manifests Composition And Lifecycle Hooks Behavior And Integration](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 32.3: [Framework Plugin Manifests Composition And Lifecycle Hooks Failure Evidence And Operational Notes](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Guest SDK: [Guest SDK Contracts Fixtures And Milestone Acceptance](../../60-specification/05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Open questions

1. Should integration tests include performance benchmarks? The spec
   defines functional tests but does not address performance requirements
   for composition latency or lifecycle operation overhead.

2. How should test evidence be stored and retrieved? The spec requires
   recording test evidence but does not specify the storage format or
   retrieval mechanism for test reports.

3. Can integration tests be run in parallel? The spec does not address
   whether the successful flow tests can be run in parallel or must
   be run sequentially.
