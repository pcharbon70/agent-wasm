---
title: "Phase 5 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-05
  - implementation
  - failure-evidence-and-operational-notes
  - provenance-diagnostics
  - admission-failures
  - evidence-integrity
  - bounded-diagnostics
aliases:
  - "M5-P5-5.3 Implementation"
---

# Phase 5 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 5.3 (Failure Evidence And
Operational Notes) from
[Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[34-provenance-signing-audit-security-and-milestone-acceptance.md](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
which consolidates failure outcomes, bounded diagnostics, evidence
requirements, implementation-defined choices, deferred work, and potential
invalidation results for artifact provenance, evidence recording, and
evidence redaction.

## Subtask 5.3.1.1: Define failure outcomes (consolidated)

### Implementation

Defined canonical failure outcomes for artifact admission:

| Outcome | Description | Error Code |
|---------|-------------|-----------|
| Malformed | `ArtifactAdmissionRequest` does not conform to schema | `artifact.admission.malformed` |
| Digest mismatch | Artifact computed digest does not match recorded digest | `artifact.digest-mismatch` |
| Signature invalid | Signature is cryptographically invalid, expired, or produced by unknown key | `artifact.signature-invalid` |
| Publisher untrusted | Signing identity does not map to known, active publisher in trust store | `artifact.publisher-untrusted` |
| Publisher hint advisory | `publisher_hint` field does not match identity from signature | `artifact.publisher-hint-mismatch` (advisory) |
| Build provenance invalid | Build record missing or invalid required fields | `artifact.build-provenance-invalid` |
| Dependency unresolved | Dependency not resolved to verified, non-revoked artifact | `artifact.dependency-unresolved` |
| Compiler incompatible | Artifact built with unsupported compiler or PDK version | `artifact.compiler-incompatible` |
| Revoked | Artifact or signing identity in active revocation list | `artifact.revoked` |
| Admission failed | General admission failure (any check failed) | `artifact.admission.failed` |

Additional failure outcomes:
- `artifact.admission.digest-computation-failed`: Digest computation failed
- `evidence.integrity-violation`: Evidence record corrupted or tampered
- Evidence recording failures (write, integrity, access policy)
- Evidence redaction failures (policy evaluation, access enforcement, stable reference generation)

### Design decisions

1. **`publisher-hint-mismatch` is advisory, not a failure**: The `publisher_hint`
   mismatch does NOT fail admission. This supports operator workflows where
   operator knows which publisher should have signed an artifact but artifact's
   own metadata is incomplete or ambiguous.

2. **`artifact.admission.failed` is general failure**: This is the top-level
   failure diagnostic when any admission check fails. Specific check failures
   are reported in addition to this general diagnostic.

3. **Evidence integrity violation is separate from admission failure**:
   `evidence.integrity-violation` is a failure outcome for evidence recording,
   not for artifact admission. This distinguishes between admission failures
   and evidence integrity failures.

## Subtask 5.3.1.2: Define bounded diagnostics and evidence

### Implementation

Defined bounded diagnostics for provenance signing, audit, and security failures.
Each diagnostic MUST contain:

1. **Error code**: Specific error code from error code table
2. **Context**: Operation that failed (e.g., artifact admission, evidence
   recording, evidence redaction)
3. **Entity identifiers**: Tenant ID, agent ID, or principal ID (sanitized)
4. **Timestamp**: Time of error
5. **Retryable**: Whether operation can be retried

**Prohibited content**: internal implementation details, secrets, sensitive data.

Bounded diagnostics for artifact admission:
- Include `artifact_id`, `artifact_digest`, `failed_check`, `diagnostic`
- Do NOT include raw artifact bytes, signature bytes, or private keys

Bounded diagnostics for evidence recording:
- Include `record_id`, `event_type`, `failure_type`, `diagnostic`
- Do NOT include raw evidence record contents beyond required fields

Bounded diagnostics for evidence redaction:
- Include `access_request_id`, `consumer_id`, `denied_fields`, `diagnostic`
- Do NOT include original field values that were redacted

### Design decisions

1. **Diagnostics are bounded by prohibition**: Rather than listing what to
   include, the spec explicitly prohibits what to exclude (raw bytes,
   signatures, private keys, original redacted values). This is more flexible
   for implementations and avoids accidentally omitting required fields.

2. **Diagnostic content varies by failure domain**: Artifact admission
   diagnostics include artifact-specific fields; evidence recording
   diagnostics include record-specific fields; evidence redaction diagnostics
   include access request-specific fields. This ensures that diagnostics
   are relevant to the failure domain.

3. **Retryable is derived from error code**: The spec implies that
   retryability can be determined from error code category. For example,
   `artifact.admission.malformed` is retryable (operator can fix request),
   while `artifact.revoked` is not (revocation is permanent until publisher
   trust is restored).

## Subtask 5.3.1.3: Document implementation-defined choices and deferred work

### Implementation

**Implementation-defined choices** (must be documented in conformance profile):
1. Publisher trust store format and storage mechanism
2. Revocation list format and storage mechanism
3. Compatibility policy record format and storage mechanism
4. Dependency cache format and storage mechanism
5. Evidence record storage mechanism (database, file system, object store,
   distributed log)
6. Evidence integrity check mechanism (append-only log, Merkle tree,
   cryptographic hash chain, or equivalent)
7. Evidence retention period
8. Evidence query interface
9. Redaction field patterns for identifying fields in each redaction category
10. Diagnostic serialization format (JSON, MessagePack, CBOR, etc.)
11. Alert notification mechanism for security alert path

**Deferred work**:
1. Distributed evidence records: Evidence records replicated across multiple
   hosts for high availability and fault tolerance
2. Cross-tenant evidence sharing: Authorized cross-tenant evidence sharing
   for collaborative investigation
3. Evidence retention automation: Automated evidence retention policies
   based on regulatory requirements
4. Evidence query optimization: Performance optimization for evidence
   queries over large evidence sets
5. Threat-to-control matrix automation: Automated threat-to-control matrix
   generation and maintenance
6. Adversarial simulation automation: Automated adversarial simulation
   framework for continuous security testing
7. Publisher trust store federation: Federation of publisher trust stores
   across multiple operator domains
8. Revocation list propagation: Automated revocation list propagation
   across distributed systems

Each deferred item has a defined triggering condition: observable operator
demand, security audit recommendation, or performance benchmark result.

**Results invalidating earlier milestones**:
1. Artifact admission latency exceeding turn timeout
2. Evidence storage exceeding capacity planned in earlier milestones
3. Evidence integrity check overhead exceeding resource budgets
4. Revocation list propagation delay exceeding bounded time requirement
5. Adversarial simulation revealing unmitigated residual risk
6. Evidence query performance degrading below acceptable thresholds

### Design decisions

1. **Implementation-defined choices are operational, not normative**:
   The normative contract (what must happen) is fully specified; only
   the mechanism (how it happens) is left to implementations. This
   ensures conformance while allowing flexibility.

2. **Deferred work requires explicit triggers**: Each deferred item has
   a defined triggering condition (operator demand, security audit,
   performance benchmark). Deferral is not a default position; it
   requires an explicit trigger.

3. **Invalidation results are observable conditions**: Each invalidation
   trigger is a measurable condition (latency, capacity, performance) that
   can be monitored during integration testing.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 34.1: [Provenance Signing Audit Security And Milestone Acceptance Contract And Data Model](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.2: [Provenance Signing Audit Security And Milestone Acceptance Behavior And Integration](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.4: [Provenance Signing Audit Security And Milestone Acceptance Phase 5 Integration Tests](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Effect handlers: [Effect Handlers Attempts Idempotency And Result Signals](../../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should evidence retention periods be regulatory-driven? The spec says
   retention is implementation-defined. Should minimum retention periods
   be normative to ensure compliance with regulations such as GDPR or SOC2?

2. How should evidence query interface be standardized? The spec allows
   implementations to define their own query interface. Should a normative
   query interface be defined to enable cross-implementation tooling?

3. Can deferred work items be implemented as extensions without
   specification changes? The spec lists deferred work but does not
   address whether these items can be implemented as extensions
   without becoming normative.
