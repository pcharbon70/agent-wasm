---
title: "Phase 1 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-01
  - implementation
  - failure-evidence-and-operational-notes
  - diagnostics
  - error-codes
  - bounded-diagnostics
aliases:
  - "M5-P1-1.3 Implementation"
---

# Phase 1 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 1.3 (Failure Evidence And Operational Notes) from
[Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
which defines failure outcomes, error codes, bounded diagnostics, and
implementation-defined choices for the threat model, principals, trust classes,
and grant vocabulary.

## Subtask 1.3.1.1: Define failure outcomes

### Implementation

Defined six primary failure outcomes relevant to threat model principals, trust
classes, and grant vocabulary:

| Outcome | Description | Relevant Error Codes |
|---------|-------------|---------------------|
| Malformed | Input data does not conform to expected schema | `storage.snapshot.duplicate`, `commit.conflict` |
| Incompatible | Data incompatible with current schema or handler version | `trust.unreviewed_plugin` |
| Conflicting | Multiple writers attempt to write to same record | `commit.conflict` |
| Unauthorized | Caller lacks permission to perform operation | `auth.authentication_failure`, `auth.grant_absence`, `auth.principal_mismatch` |
| Exhausted | System out of resources (storage, grant budget) | `auth.grant_expiry` (budget exhaustion) |
| Unavailable | Storage backend unavailable | `storage.unavailable` |

Additional trust-specific outcomes:
- `trust.untrusted_guest`: Guest artifact is untrusted
- `trust.unreviewed_plugin`: Plugin has not been reviewed
- `tenant.isolation_violation`: Tenant isolation boundary crossed

### Design decisions

1. **Failure outcomes are cross-referenced to earlier milestones**: The malformed,
   incompatible, and conflicting outcomes reference storage contracts from
   Milestone 4 ([Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md))
   and ([Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)).
   This avoids duplicating failure semantics and keeps the M5 chapter focused
   on security-specific outcomes.

2. **Error codes are namespaced by domain**: The `auth.*`, `trust.*`,
   `storage.*`, and `commit.*` prefixes distinguish the security failure
   outcomes from storage and concurrency failures defined in earlier milestones.

3. **Tenant isolation violation is a security outcome**: This is the most
   critical failure outcome for M5. It is listed alongside authentication
   failures because it represents a breach of the trust model.

## Subtask 1.3.1.2: Define bounded diagnostics

### Implementation

Defined the structure of bounded diagnostics. Each diagnostic MUST include:

1. **Error code**: Specific error code from the error code table
2. **Context**: The operation that failed (e.g., authentication, authorization)
3. **Entity identifiers**: Tenant ID, agent ID, or principal ID (without exposing sensitive data)
4. **Timestamp**: Time the error occurred
5. **Retryable**: Whether the operation can be retried

Prohibited content in diagnostics:
- Internal implementation details
- Secrets
- Sensitive data beyond what is permitted for entity identification

### Design decisions

1. **Diagnostics are bounded by prohibition, not by inclusion**: Rather than
   listing what to include, the spec explicitly prohibits what to exclude
   (secrets, internal details, sensitive data). This is more flexible for
   implementations and avoids accidentally omitting required fields.

2. **Entity identifiers are permitted but sanitized**: Tenant ID, agent ID, and
   principal ID may be included in diagnostics for operational visibility, but
   other identifiers (such as user email or API key fragments) are prohibited.

3. **Retryable is a boolean flag**: Simple and explicit. Implementations can
   derive this from the error code's failure outcome category (e.g.,
   `auth.authentication_failure` is typically retryable, while
   `auth.grant_revocation` is not).

## Subtask 1.3.1.3: Document implementation-defined choices and deferred work

### Implementation

**Implementation-defined choices** (must be documented in conformance profile):
1. Authentication mechanism (API keys, OAuth, mTLS)
2. Grant storage (in-memory, database, etc.)
3. Grant caching strategy
4. Audit log retention policy
5. Trust class assignment policy

**Deferred work**:
1. Dynamic trust classes: Runtime trust class adjustment based on behavior
2. Grant delegation: Automated grant delegation workflows
3. Tenant onboarding: Automated tenant provisioning
4. Security metrics: Security metrics and monitoring

**Results invalidating earlier milestones**:
1. Authentication overhead exceeding turn timeout
2. Grant storage exceeding capacity planned in earlier milestones
3. Audit log size exceeding capacity planned in earlier milestones

### Design decisions

1. **Implementation-defined choices are limited to operational concerns**:
   The normative contract (what must happen) is fully specified; only the
   mechanism (how it happens) is left to implementations. This ensures
   conformance while allowing flexibility.

2. **Deferred work is clearly separated from normative obligations**: The
   deferred items are explicitly marked as non-normative. This prevents
   scope creep and makes it clear what is required for M5 promotion.

3. **Invalidation results are observable conditions**: Each invalidation
   trigger is a measurable condition (latency, capacity, size) that can
   be monitored during integration testing.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary Contract And Data Model](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 30.2: [Threat Model Principals Trust Classes And Grant Vocabulary Behavior And Integration](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 30.4: [Threat Model Principals Trust Classes And Grant Vocabulary Phase 1 Integration Tests](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugins: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Open questions

1. Should bounded diagnostics include a severity level? The current design
   only includes a `retryable` flag. A severity level (info, warning, error,
   critical) would help operators prioritize responses.

2. How should grant caching interact with grant revocation? The spec says
   cached decisions must be invalidated on revocation, but does not specify
   the invalidation propagation mechanism (push, pull, or TTL-based).

3. Can audit log retention policies differ by principal kind? The spec
   defines retention as implementation-defined but does not address whether
   operator audit logs should have longer retention than agent audit logs.
