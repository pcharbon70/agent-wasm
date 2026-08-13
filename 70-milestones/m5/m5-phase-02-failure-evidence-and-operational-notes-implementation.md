---
title: "Phase 2 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-02
  - implementation
  - failure-evidence-and-operational-notes
  - policy-diagnostics
  - error-codes
  - attenuation-violations
aliases:
  - "M5-P2-2.3 Implementation"
---

# Phase 2 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 2.3 (Failure Evidence And Operational Notes) from
[Phase 2 - Capability Policy Attenuation Limits And Enforcement](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-02-capability-policy-attenuation-limits-and-enforcement.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[31-capability-policy-attenuation-limits-and-enforcement.md](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
which defines failure outcomes, error codes, bounded diagnostics, and
implementation-defined choices for capability policy attenuation, limits,
and enforcement.

## Subtask 2.3.1.1: Define failure outcomes

### Implementation

Defined nine failure outcomes for capability policy:

| Outcome | Description | Error Code Prefix |
|---------|-------------|-------------------|
| Malformed | Input does not conform to expected schema | `policy.malformed_input` |
| Incompatible | Data incompatible with current policy version | `policy.incompatible_version` |
| Conflicting | Multiple policy rules produce conflicting decisions | `policy.conflicting_rules` |
| Unauthorized | Caller lacks permission to evaluate policy | `policy.unauthorized` |
| Exhausted | Policy engine out of resources | `policy.exhausted` |
| Unavailable | Policy engine unavailable | `policy.unavailable` |
| Approval deadline exceeded | Approval deadline expired without approval | `policy.approval_deadline_exceeded` |
| Attenuation violation | Runtime attenuation restriction violated | `policy.attenuation_violation` |
| Policy version mismatch | Policy version in input does not match active version | `policy.policy_version_mismatch` |

Additional grant-related error codes reference [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md):
`policy.grant_absent`, `policy.grant_expired`, `policy.grant_revoked`,
`policy.grant_scoped`, `policy.tenant_mismatch`, `policy.trust_class_insufficient`,
`policy.artifact_untrusted`, `policy.plugin_untrusted`, `policy.resource_locked`,
`policy.rate_limit_exceeded`, `policy.quota_exhausted`, `policy.capability_disabled`,
`policy.capability_unavailable`.

Limit enforcement error codes:
`policy.byte_count_exceeded`, `policy.duration_exceeded`, `policy.budget_exceeded`.

### Design decisions

1. **Error codes are namespaced by `policy.*`**: This distinguishes policy
   failures from authentication failures (`auth.*`) and trust-class failures
   (`trust.*`) defined in Phase 1. Operators can filter diagnostics by domain.

2. **Limit enforcement errors are distinct from policy errors**: The
   `byte_count_exceeded`, `duration_exceeded`, and `budget_exceeded`
   errors are runtime enforcement failures, not policy evaluation failures.
   This distinction helps operators diagnose whether a failure is a
   policy decision issue or a runtime enforcement issue.

3. **Grant-related errors reference Phase 1**: The grant error codes
   (`grant_absent`, `grant_expired`, etc.) are defined in Phase 1 but
   referenced here to avoid duplication. This ensures consistent error
   code usage across phases.

## Subtask 2.3.1.2: Define bounded diagnostics

### Implementation

Defined bounded diagnostics for policy failures. Each diagnostic MUST include:

1. **Error code**: Specific error code from the error code table
2. **Context**: Operation that failed (signal admission, action resolution, etc.)
3. **Entity identifiers**: Tenant ID, agent ID, or principal ID (sanitized)
4. **Timestamp**: Time of error
5. **Retryable**: Whether operation can be retried

Prohibited content: internal implementation details, secrets, sensitive data.

### Design decisions

1. **Context identifies the policy boundary**: The diagnostic includes
   the specific turn lifecycle boundary where policy was evaluated
   (e.g., "signal admission", "guest invocation"). This enables operators
   to identify which phase of the turn lifecycle is failing.

2. **Retryable is derived from error code**: The spec implies that
   retryability can be determined from the error code category. For
   example, `policy.grant_absent` is retryable (grant may be obtained),
   while `policy.attenuation_violation` is not (execution must stop).

3. **Diagnostics are consistent with Phase 1**: The bounded diagnostic
   format is consistent with Phase 1's approach, ensuring operators can
   parse diagnostics from both phases with the same tooling.

## Subtask 2.3.1.3: Document implementation-defined choices

### Implementation

**Implementation-defined choices**:
1. Policy engine (OPA, custom, etc.)
2. Grant storage (in-memory, database, etc.)
3. Policy caching strategy
4. Audit log retention
5. Approval notification mechanism
6. Attenuation enforcement mechanism

**Deferred work**:
1. Dynamic policy adaptation: Runtime policy adjustment based on behavior
2. Policy simulation: Simulating policy decisions before applying
3. Policy versioning automation: Automated policy versioning and deployment
4. Policy analytics: Policy usage and effectiveness analytics

**Results invalidating earlier milestones**:
1. Policy evaluation latency exceeding turn timeout
2. Grant storage exceeding capacity planned in earlier milestones
3. Audit log size exceeding capacity planned in earlier milestones

### Design decisions

1. **Policy engine is implementation-defined**: The spec does not mandate
   a specific policy engine (OPA, custom, etc.). This allows
   implementations to choose the engine that best fits their deployment
   environment while maintaining normative conformance.

2. **Attenuation enforcement mechanism is implementation-defined**: The
   spec does not specify how attenuation is enforced at runtime (proxy,
   wrapper, native enforcement). This allows implementations to optimize
   for their specific architecture.

3. **Deferred work is clearly scoped**: The four deferred items are
   explicitly non-normative. This prevents scope creep and makes it
   clear what is required for M5 promotion.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement Contract And Data Model](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.2: [Capability Policy Attenuation Limits And Enforcement Behavior And Integration](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.4: [Capability Policy Attenuation Limits And Enforcement Phase 2 Integration Tests](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin composition: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)

## Open questions

1. Should the policy engine support rule versioning? The spec defines
   policy versioning at the host level but does not address whether
   individual policy rules can be versioned independently.

2. How should attenuation enforcement overhead be measured? The spec
   requires runtime enforcement but does not define how to measure
   the performance overhead of attenuation checks.

3. Can policy decisions be pre-computed for known inputs? The spec
   allows caching but does not address whether known policy inputs
   (e.g., repeated invocations with the same context) can be
   pre-evaluated to reduce latency.
