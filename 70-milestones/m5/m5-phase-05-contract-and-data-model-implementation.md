---
title: "Phase 5 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-05
  - implementation
  - contract-and-data-model
  - provenance-signing
  - artifact-admission
  - evidence-recording
  - evidence-redaction
aliases:
  - "M5-P5-5.1 Implementation"
---

# Phase 5 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 5.1 (Contract And Data Model) from
[Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[34-provenance-signing-audit-security-and-milestone-acceptance.md](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
which establishes the contract and data model for artifact provenance
admission, host-owned evidence recording, and evidence redaction that
together form the security gate for milestone acceptance.

## Subtask 5.1.1.1: Verify artifact digest, signature, publisher identity, build provenance, dependencies, compiler/PDK, and revocation before admission

### Implementation

Defined artifact admission verification as the host-owned gate that validates
a plugin artifact before it is loaded, instantiated, or otherwise made
available to any guest, agent, or tenant. Seven admission checks:

| Check | Verifiable Claim | Failure Diagnostic |
|-------|-----------------|-------------------|
| Digest integrity | Artifact's cryptographic digest matches digest in manifest or attestation | `artifact.digest-mismatch` |
| Signature validity | Artifact's signature is valid and signed by trusted publisher identity | `artifact.signature-invalid` |
| Publisher identity | Signing identity maps to known, active publisher in trust store | `artifact.publisher-untrusted` |
| Build provenance | Build record identifies compiler, PDK version, build environment, timestamp | `artifact.build-provenance-invalid` |
| Dependency resolution | Every dependency resolves to verified, non-revoked artifact in dependency cache | `artifact.dependency-unresolved` |
| Compiler and PDK match | Artifact built with compiler and PDK version host policy declares compatible | `artifact.compiler-incompatible` |
| Revocation check | Artifact and signing identity not present in active revocation lists | `artifact.revoked` |

Defined `ArtifactAdmissionRequest` structure:

```
ArtifactAdmissionRequest {
  artifact_id: ArtifactId,
  artifact_digest: Digest,
  artifact_signature: Signature?,
  attestation: Attestation?,
  manifest: ArtifactManifest,
  publisher_hint: PublisherId?,
  admission_context: AdmissionContext
}

AdmissionContext {
  tenant_id: TenantId?,
  agent_id: AgentId?,
  requested_trust_tier: TrustTier?,
  deadline_ms: u64?
}

TrustTier = "untrusted" | "sandboxed" | "semi-trusted" | "trusted" | "operator"
```

Admission flow steps:
1. Validate `ArtifactAdmissionRequest` structure
2. Compute artifact digest using declared `HashAlgorithm`
3. Verify digest integrity against manifest/attestation
4. Verify artifact signature if present
5. Resolve publisher identity from signature
6. Query revocation lists for artifact and publisher
7. Validate build provenance fields
8. Resolve and verify all declared dependencies
9. Check compiler and PDK compatibility policy
10. Record `artifact.admitted` evidence with full admission result

On successful admission, host caches verified artifact in dependency cache.
Cached artifacts MAY be reused without re-performing checks 2-9, provided
cache entry is still valid (not expired, not revoked, not superseded by
policy revision).

### Design decisions

1. **All seven checks are mandatory**: Failure of any single check causes
   artifact rejection with `artifact.admission.failed`. Steps 3-9 are
   independent and MAY be executed in parallel by conforming implementation,
   provided final admission result is deterministic.

2. **`publisher_hint` is advisory, not authoritative**: The host verifies
   publisher identity from artifact's signature, not from `publisher_hint`.
   If signature is valid but signing identity does not match `publisher_hint`,
   host emits `artifact.publisher-hint-mismatch` diagnostic but does NOT
   fail admission. This supports operator workflows while maintaining
   cryptographic verification.

3. **Cached artifacts are not automatically unloaded on revocation**:
   Artifacts already loaded and instantiated before revocation are not
   automatically unloaded. Their lifecycle is governed by agent activation
   and instance mode policies defined in [33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

4. **Dependency cycle detection is a safety requirement**: The host MUST
   NOT load an artifact whose dependencies form a cycle. Cycle detection
   prevents infinite loops during admission verification.

## Subtask 5.1.1.2: Record host-owned evidence for authentication, policy, grants, limits, imports, directives, effects, revisions, and failures

### Implementation

Defined host-owned evidence as the complete set of structured records that
the host creates, modifies, or retains during artifact admission, invocation,
and lifecycle management. Evidence is host-owned: host determines format,
content, retention, and access policy. Guest modules, agents, and tenants
MAY request specific evidence fields for observability but have no authority
to modify, redact, or suppress host-owned evidence.

Nine evidence event types with required minimum fields:

| Event Type | Trigger | Required Minimum Fields |
|------------|---------|------------------------|
| `artifact.admitted` | Artifact passes all admission checks | `artifact_id`, `artifact_digest`, `publisher_id`, `trust_tier`, `timestamp`, `admission_result` |
| `artifact.rejected` | Artifact fails one or more admission checks | `artifact_id`, `artifact_digest`, `failed_check`, `diagnostic`, `timestamp` |
| `invocation.started` | Guest module invocation begins | `invocation_id`, `artifact_id`, `tenant_id`, `agent_id?`, `principal_id`, `timestamp` |
| `invocation.completed` | Guest module invocation completes successfully | `invocation_id`, `artifact_id`, `tenant_id`, `output_hash`, `duration_ms`, `timestamp` |
| `invocation.failed` | Guest module invocation traps, times out, or is cancelled | `invocation_id`, `artifact_id`, `tenant_id`, `failure_type`, `diagnostic`, `timestamp` |
| `grant.approved` | Capability grant approved for invocation | `grant_id`, `artifact_id`, `tenant_id`, `granted_capabilities`, `timestamp` |
| `grant.denied` | Capability grant request denied | `grant_id`, `artifact_id`, `tenant_id`, `requested_capabilities`, `denied_capabilities`, `reason`, `timestamp` |
| `tenant.isolation.violation` | Cross-tenant isolation invariant violated | `invocation_id`, `tenant_id`, `violation_type`, `evidence_hash`, `timestamp` |
| `residue.detected` | Test residue detected after invocation | `invocation_id`, `artifact_id`, `tenant_id`, `residue_category`, `evidence_hash`, `timestamp` |
| `policy.revision` | Host policy or compatibility policy revised | `policy_id`, `revision_number`, `changes_summary`, `timestamp` |

Defined `EvidenceRecord` structure:

```
EvidenceRecord {
  record_id: UUID,
  event_type: EventType,
  timestamp: ISO8601,
  fields: Map<String, Value>
}
```

Evidence retention and access rules:
1. **Retention**: Records retained for minimum period documented in
   conformance profile. Records MUST NOT be deleted before minimum
   retention period expires, except by explicit operator action with
   audit log entry documenting deletion.
2. **Access**: Records classified by access policy defined in
    [Evidence redaction](#subtask-5113-redact-secrets-prompts-large-payloads-and-tenant-sensitive-data-while-retaining-stable-references-and-access-policy). Host enforces access
   policy on every read or query.
3. **Integrity**: Records MUST be immutable once written. Corrupted or
   tampered record MUST be detected by integrity checks and reported
   with `evidence.integrity-violation` diagnostic.
4. **Audit**: Every access to evidence records (reads, writes, deletions)
   MUST be logged in separate audit log subject to retention and integrity
   rules.

### Design decisions

1. **Evidence is host-owned**: The host determines evidence format,
   content, retention, and access policy. Guest modules, agents, and
   tenants have no authority to modify, redact, or suppress host-owned
   evidence. This prevents adversaries from hiding their activities.

2. **Evidence immutability is primary defense against audit tampering**:
   If an adversary can modify evidence records, the entire audit system
   loses its value. The integrity check mechanism (append-only log,
   Merkle tree, cryptographic hash chain, or equivalent) is
   implementation-defined.

3. **`output_hash` enables forensic correlation**: The `output_hash`
   field in `invocation.completed` is a cryptographic hash of invocation's
   observable output bytes. This enables forensic correlation between
   completed invocation and its output without retaining output bytes in
   evidence record itself.

4. **Security alert path for isolation violations**: Evidence records
   for `tenant.isolation.violation` and `residue.detected` events trigger
   immediate security alert path in addition to normal record creation.
   Alert path records event, notifies operator, and MAY initiate
   containment actions such as instance quarantine or tenant suspension.

## Subtask 5.1.1.3: Redact secrets, prompts, large payloads, and tenant-sensitive data while retaining stable references and access policy

### Implementation

Defined evidence redaction as the host-owned process of removing or
replacing sensitive fields from evidence records before they are exposed
to agents, tenants, or external observers. Redaction is applied after
evidence is written and before it is read or queried by any non-operator
consumer. Host retains unredacted original; redacted views are derived
representations.

Four redaction categories:

| Category | Redacted Fields | Replacement | Access Policy for Unredacted |
|----------|----------------|-------------|------------------------------|
| Secrets | Any field containing secrets, keys, credentials, tokens, or private data | `<REDACTED>` marker with field name preserved | Operator-only |
| Prompts | Any field containing user or agent prompts, including prompt fragments | `<PROMPT-REDACTED>` marker with field name preserved | Tenant-scoped: submitting tenant can view |
| Large payloads | Any field whose value exceeds size limit in conformance profile | `<LARGE-PAYLOAD: {size}>` marker with size in bytes | Operator-only if exceeds operator threshold; tenant-scoped otherwise |
| Tenant-sensitive | Any field containing cross-tenant state, other tenants' identifiers beyond invoking tenant, or inter-tenant relationship data | `<TENANT-SENSITIVE>` marker with field name preserved | Operator-only |

Access matrix:

| Dimension | Operator | Tenant (own) | Tenant (other) | Agent |
|-----------|----------|--------------|----------------|-------|
| Secrets | Full | None | None | None |
| Prompts | Full | Own only | None | None |
| Large payloads | Full | Own if below operator threshold | None | None |
| Tenant-sensitive | Full | None | None | None |
| Non-sensitive fields | Full | Full | Full | Full (non-sensitive only) |

Redaction is applied at query time, not at write time. Original evidence
record is stored unredacted; redacted view is derived representation
produced on every read. This ensures that changes to redaction policy
take effect immediately for all subsequent queries without requiring
record re-processing.

### Design decisions

1. **Redaction at query time, not write time**: This is more flexible
   than write-time redaction because it supports dynamic policy changes
   without data migration. The tradeoff is per-query computational cost.

2. **Prompts are tenant-scoped**: The submitting tenant has a legitimate
   interest in viewing their own prompts, but no interest in viewing
   other tenants' prompts. This balances observability with privacy.

3. **Stable references preserve field position and semantic role**:
   Redacted field values are replaced with stable references that:
   - Preserve the field name
   - Indicate that original value was redacted
   - Indicate the redaction category
   - MAY include metadata such as original size or timestamp
   - Do NOT enable reconstruction of original value by any consumer
     without appropriate access policy approval

4. **Operator access to unredacted evidence is unconditional**: Operator
   access to unredacted evidence is unconditional for records within
   retention period. This ensures that operators can perform forensic
   analysis without restrictions.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 34.1: [Provenance Signing Audit Security And Milestone Acceptance Contract And Data Model](../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Effect handlers: [Effect Handlers Attempts Idempotency And Result Signals](../../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)
- Agent registry: [Agent Registry Activation Cancellation And Completion](../../60-specification/22-agent-registry-activation-cancellation-and-completion.md)
- Crash injection: [Crash Injection Durable Effects And Milestone Acceptance](../../60-specification/29-crash-injection-durable-effects-and-milestone-acceptance.md)

## Open questions

1. Should evidence redaction support field-level granularity? The current
   design redacts entire fields. Could field-level redaction (e.g.,
   redacting only specific keys within a JSON object) provide better
   privacy while retaining more observability?

2. How should redaction policy changes affect already-written evidence?
   The spec says redaction is applied at query time, so policy changes
   take effect immediately. But what about evidence records that were
   queried before the policy change? Are redacted views cached?

3. Can agents request specific evidence fields for observability? The
   spec says guests MAY request specific evidence fields but have no
   authority to modify, redact, or suppress host-owned evidence. How
   should this work in practice?
