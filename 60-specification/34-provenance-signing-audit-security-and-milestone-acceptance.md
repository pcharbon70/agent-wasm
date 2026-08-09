---
title: "Provenance Signing Audit Security And Milestone Acceptance"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-05
  - phase-05
  - provenance-signing
  - audit-security
  - milestone-acceptance
aliases:
  - "M5-P5 Provenance Signing Audit Security And Milestone Acceptance"
---

# Provenance Signing Audit Security And Milestone Acceptance

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
--
Capabilities, Plugins, Security, And Tenancy.
It establishes the contract and data model for artifact provenance admission,
host-owned evidence recording, and evidence redaction that together form the
security gate for milestone acceptance.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md).

## 5.1 Contract And Data Model

### Artifact admission verification

> **Normative definition.**
Artifact admission verification is the host-owned gate that validates a
plugin artifact before it is loaded, instantiated, or otherwise made
available to any guest, agent, or tenant.
An artifact that fails any single verification check MUST NOT proceed
past this gate.

> **Normative definition.**
A plugin artifact is any binary or package file that the host loads as a
WebAssembly guest module, including but not limited to `.wasm` files,
plugin bundles, and framework-managed module archives.
Every artifact has a publisher identity, a build record, a dependency
graph, and a compiler or PDK provenance claim that must be verified.

> **Normative definition.**
The host MUST verify every artifact against each of the following
admission checks.
Failure of any single check MUST cause the host to reject the artifact
with the diagnostic `artifact.admission.failed` and MUST NOT load the
artifact into any instance pool, agent pin, or cache.

| Check | Verifiable claim | Failure diagnostic |
|-------|-----------------|-------------------|
| **Digest integrity** | The artifact's cryptographic digest matches the digest recorded in its manifest or attestation. | `artifact.digest-mismatch` |
| **Signature validity** | The artifact's signature (code-signing, build-signing, or attestation signature) is valid and signed by a publisher identity the host trusts. | `artifact.signature-invalid` |
| **Publisher identity** | The signing identity maps to a known publisher in the host's trust store and has not been revoked. | `artifact.publisher-untrusted` |
| **Build provenance** | The build record identifies the compiler, PDK version, build environment, and build timestamp claimed by the publisher. | `artifact.build-provenance-invalid` |
| **Dependency resolution** | Every dependency declared in the artifact's manifest resolves to a verified, non-revoked artifact in the host's dependency cache. | `artifact.dependency-unresolved` |
| **Compiler and PDK match** | The artifact was built with a compiler and PDK version that the host policy declares compatible. | `artifact.compiler-incompatible` |
| **Revocation check** | The artifact and its signing identity are not present in any active revocation list maintained by the host or by upstream trust authorities. | `artifact.revoked` |

> **Normative definition.**
The digest integrity check uses a cryptographic hash algorithm declared
in the host conformance profile.
The host MUST compute the digest over the exact bytes of the artifact
file and compare it against the digest value recorded in the artifact's
manifest or attestation.
A byte-for-byte mismatch, regardless of cause, MUST fail this check.

> **Normative definition.**
The signature validity check requires the artifact to carry a signature
produced by a key pair whose public component is registered in the host's
publisher trust store.
The host MUST verify the signature over the artifact's digest, not over
the raw bytes, to prevent signature rebinding attacks.
The exact signature scheme (Ed25519, RSA-PSS, ECDSA, or another scheme)
is an implementation-defined choice documented in the conformance profile.

> **Normative definition.**
The publisher identity check maps the signing key to a publisher record
in the host trust store.
A publisher record contains at minimum: the publisher identifier, the
trusted public keys, the trust tier (see
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)),
and the active status.
A publisher that is inactive, unknown, or whose trusted keys do not
include the signing key MUST cause this check to fail.

> **Normative definition.**
The build provenance check requires the artifact's attestation or
manifest to include a build record with the following fields:

| Field | Required | Content |
|-------|----------|---------|
| `compiler_id` | Yes | Identifier of the compiler or build toolchain used. |
| `compiler_version` | Yes | Version string of the compiler. |
| `pdk_id` | Yes | Identifier of the Plugin Development Kit used. |
| `pdk_version` | Yes | Version string of the PDK. |
| `build_environment` | Yes | Identifier of the build environment (CI system, container image hash, or equivalent). |
| `build_timestamp` | Yes | ISO 8601 timestamp of when the artifact was built. |
| `build_source_commit` | Conditional | Source control commit hash used for the build. Required for published releases. |

> **Normative definition.**
The dependency resolution check requires every dependency declared in
the artifact's manifest to resolve to an artifact already verified and
cached by the host.
A dependency that is unresolved, whose resolved artifact is unverified,
or whose resolved artifact is revoked MUST fail this check.
The host MUST NOT load an artifact whose dependencies form a cycle.

> **Non-normative note.**
Dependency cycle detection prevents infinite loops during admission
verification and is a safety requirement, not a performance optimization.
The exact cycle detection algorithm (depth-first search, Tarjan's
strongly connected components, or equivalent) is implementation-defined.

> **Normative definition.**
The compiler and PDK match check requires the artifact's declared
compiler and PDK to match a compatibility policy record maintained by
the host.
A compatibility policy record declares which compiler-PDK-version
triples are permitted for each trust tier.
An artifact built with an unsupported compiler or PDK version MUST
fail this check, regardless of whether the resulting bytecode is
technically valid.

> **Normative definition.**
The revocation check queries the host's active revocation lists at the
moment of admission.
An artifact whose digest appears on any revocation list, or whose
publisher identity has been revoked, MUST fail this check.
Revocation lists are mutable and MAY be updated without restarting the
host, but updates take effect only for artifacts admitted after the
update.
Artifacts already loaded and instantiated before revocation are not
automatically unloaded; their lifecycle is governed by the agent
activation and instance mode policies defined in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

> **Normative definition.**

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

ArtifactId = string
Digest = { algorithm: HashAlgorithm, value: bytes }
HashAlgorithm = "sha256" | "sha384" | "sha512" | "blake3"
Signature = bytes
Attestation = bytes
PublisherId = string
AdmissionContext {
  tenant_id: TenantId?,
  agent_id: AgentId?,
  requested_trust_tier: TrustTier?,
  deadline_ms: u64?
}

TrustTier = "untrusted" | "sandboxed" | "semi-trusted" | "trusted" | "operator"
```

Every artifact admission request MUST include the request structure
defined above.
The host MUST validate the request structure before performing any
admission checks.
A malformed request MUST be rejected with the diagnostic
`artifact.admission.malformed`.

> **Normative definition.**
The `publisher_hint` field is advisory.
The host MUST verify the publisher identity from the artifact's
signature, not from this field.
If the signature is absent or invalid, the `publisher_hint` field is
ignored.
If the signature is valid but the signing identity does not match the
`publisher_hint`, the host MUST emit the diagnostic
`artifact.publisher-hint-mismatch` in addition to the standard admission
result.

> **Non-normative note.**
The `publisher_hint` field exists to support operator workflows where
the operator knows which publisher should have signed an artifact but
the artifact's own metadata is incomplete or ambiguous.
It does not substitute for cryptographic verification.

> **Normative implementation-defined choice.**
The host defines the exact format and storage mechanism for the publisher
trust store, revocation lists, compatibility policy records, and
dependency cache.
These data structures MUST support concurrent read access and MUST
document their maximum size, expiration policy, and update protocol in
the conformance profile.

### Host-owned evidence recording

> **Normative definition.**
Host-owned evidence is the complete set of structured records that the
host creates, modifies, or retains during artifact admission, invocation,
and lifecycle management.
Evidence is host-owned: the host determines its format, content,
retention, and access policy.
Guest modules, agents, and tenants MAY request specific evidence fields
for observability but have no authority to modify, redact, or suppress
host-owned evidence.

> **Normative definition.**
The host MUST create an evidence record for each of the following
events.
Each evidence record MUST include a globally unique record identifier,
a timestamp, the event type, and the minimum fields listed for that
event type.

| Event type | Trigger | Required minimum fields |
|------------|---------|------------------------|
| `artifact.admitted` | An artifact passes all admission checks and is loaded. | `artifact_id`, `artifact_digest`, `publisher_id`, `trust_tier`, `timestamp`, `admission_result`. |
| `artifact.rejected` | An artifact fails one or more admission checks. | `artifact_id`, `artifact_digest`, `failed_check`, `diagnostic`, `timestamp`. |
| `invocation.started` | A guest module invocation begins. | `invocation_id`, `artifact_id`, `tenant_id`, `agent_id?`, `principal_id`, `timestamp`. |
| `invocation.completed` | A guest module invocation completes successfully. | `invocation_id`, `artifact_id`, `tenant_id`, `output_hash`, `duration_ms`, `timestamp`. |
| `invocation.failed` | A guest module invocation traps, times out, or is cancelled. | `invocation_id`, `artifact_id`, `tenant_id`, `failure_type`, `diagnostic`, `timestamp`. |
| `grant.approved` | A capability grant is approved for an invocation. | `grant_id`, `artifact_id`, `tenant_id`, `granted_capabilities`, `timestamp`. |
| `grant.denied` | A capability grant request is denied. | `grant_id`, `artifact_id`, `tenant_id`, `requested_capabilities`, `denied_capabilities`, `reason`, `timestamp`. |
| `tenant.isolation.violation` | A cross-tenant isolation invariant is violated. | `invocation_id`, `tenant_id`, `violation_type`, `evidence_hash`, `timestamp`. |
| `residue.detected` | Test residue is detected after an invocation. | `invocation_id`, `artifact_id`, `tenant_id`, `residue_category`, `evidence_hash`, `timestamp`. |
| `policy.revision` | A host policy or compatibility policy is revised. | `policy_id`, `revision_number`, `changes_summary`, `timestamp`. |

> **Normative definition.**
The `admission_result` field in `artifact.admitted` records the complete
outcome of the admission verification process.
It MUST include a boolean `passed` field and a list of all individual
checks performed, each with its own `check_name`, `passed`, and
optional `detail` fields.
An admission result that records `passed: true` but has any individual
check with `passed: false` is a specification violation and MUST be
treated as a host implementation defect.

> **Normative definition.**
The `output_hash` field in `invocation.completed` is a cryptographic
hash of the invocation's observable output bytes.
The host MUST compute this hash using the same algorithm declared in
the conformance profile and MUST NOT include any metadata, headers, or
non-output bytes in the hash input.
The `output_hash` enables forensic correlation between a completed
invocation and its output without retaining the output bytes in the
evidence record itself.

> **Normative definition.**
The `evidence_hash` field in `tenant.isolation.violation` and
`residue.detected` records are computed over the minimal evidence
record that supports the violation or detection, following the same
principles as the `evidence_hash` field in bounded diagnostics defined
in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md#bounded-diagnostics-and-evidence).
The exact hashing algorithm and evidence record format are
implementation-defined choices documented in the conformance profile.

> **Normative definition.**

```
EvidenceRecord {
  record_id: UUID,
  event_type: EventType,
  timestamp: ISO8601,
  fields: Map<String, Value>
}

EventType = "artifact.admitted" | "artifact.rejected"
          | "invocation.started" | "invocation.completed"
          | "invocation.failed" | "grant.approved"
          | "grant.denied" | "tenant.isolation.violation"
          | "residue.detected" | "policy.revision"

UUID = string (UUID v4 format)
ISO8601 = string (ISO 8601 datetime format)
Value = string | number | boolean | null | bytes | Map<String, Value>
```

Every evidence record MUST conform to the structure defined above.
The `fields` map contains exactly the minimum required fields for the
record's event type, plus any additional fields the implementation
chooses to record.

> **Normative definition.**
The host MUST enforce the following evidence retention and access rules:

1. **Retention**: Evidence records MUST be retained for a minimum period
   documented in the conformance profile.
   Records MUST NOT be deleted before the minimum retention period
   expires, except by explicit operator action with an audit log entry
   documenting the deletion.
2. **Access**: Evidence records are classified by access policy as defined
   in [Evidence redaction](#evidence-redaction).
   The host MUST enforce access policy on every read or query of
   evidence records.
3. **Integrity**: Evidence records MUST be immutable once written.
   A corrupted or tampered evidence record MUST be detected by integrity
   checks and reported with the diagnostic `evidence.integrity-violation`.
4. **Audit**: Every access to evidence records, including reads, writes,
   and deletions, MUST be logged in a separate audit log that is itself
   subject to retention and integrity rules.

> **Non-normative note.**
Evidence immutability is the primary defense against audit tampering.
If an adversary can modify evidence records, the entire audit system
loses its value.
The integrity check mechanism (append-only log, Merkle tree, cryptographic
hash chain, or equivalent) is implementation-defined.

> **Normative implementation-defined choice.**
The host defines the exact storage mechanism for evidence records
(database, file system, object store, or distributed log), the
integrity check mechanism, the retention period, and the query interface.
These choices MUST be documented in the conformance profile.

### Evidence redaction

> **Normative definition.**
Evidence redaction is the host-owned process of removing or replacing
sensitive fields from evidence records before they are exposed to
agents, tenants, or external observers.
Redaction is applied after evidence is written and before it is
read or queried by any non-operator consumer.
The host retains the unredacted original; redacted views are derived
representations.

> **Normative definition.**
The host MUST apply redaction to evidence records according to the
following redaction categories.
Each category defines which fields are redacted, what replaces them,
and what access policy controls access to the unredacted version.

| Category | Redacted fields | Replacement | Access policy for unredacted |
|----------|----------------|-------------|------------------------------|
| **Secrets** | Any field containing secrets, keys, credentials, tokens, or private data. | `<REDACTED>` marker with field name preserved. | Operator-only. |
| **Prompts** | Any field containing user or agent prompts, including prompt fragments embedded in inputs or outputs. | `<PROMPT-REDACTED>` marker with field name preserved. | Tenant-scoped: the tenant who submitted the prompt can view it. |
| **Large payloads** | Any field whose value exceeds the size limit declared in the conformance profile. | `<LARGE-PAYLOAD: {size}>` marker with size in bytes. | Operator-only if the original exceeds the operator threshold; tenant-scoped otherwise. |
| **Tenant-sensitive** | Any field containing cross-tenant state, other tenants' identifiers beyond the invoking tenant, or inter-tenant relationship data. | `<TENANT-SENSITIVE>` marker with field name preserved. | Operator-only. |

> **Normative definition.**
The host MUST replace redacted field values with stable references
that preserve the field's position and semantic role in the evidence
record.
A stable reference is a replacement value that:
- preserves the field name,
- indicates that the original value was redacted,
- indicates the redaction category,
- MAY include metadata such as the original size or timestamp, and
- does NOT enable reconstruction of the original value by any
  consumer without the appropriate access policy approval.

> **Normative definition.**
Access policy for unredacted evidence records is enforced by the host
at query time.
An access request is evaluated against the following policy dimensions:

| Dimension | Operator | Tenant (own) | Tenant (other) | Agent |
|-----------|----------|--------------|----------------|-------|
| Secrets | Full | None | None | None |
| Prompts | Full | Own only | None | None |
| Large payloads | Full | Own if below operator threshold | None | None |
| Tenant-sensitive | Full | None | None | None |
| Non-sensitive fields | Full | Full | Full | Full (non-sensitive only) |

> **Non-normative note.**
This access matrix ensures that agents and tenants never observe data
belonging to other tenants, and that secrets and tenant-sensitive data
are accessible only to the operator.
Prompts are a special case: the submitting tenant has a legitimate
interest in viewing their own prompts, but no interest in viewing
other tenants' prompts.

> **Normative definition.**
The host MUST NOT apply redaction to evidence records that are consumed
by the operator through the host's administrative interface or API.
Operator access to unredacted evidence is unconditional for records
within the retention period.
Records outside the retention period are subject to the operator's own
deletion policy and are not required to be available.

> **Normative definition.**

```
RedactionPolicy {
  categories: RedactionCategory[],
  access_matrix: AccessMatrix,
  stable_reference_format: ReferenceFormat
}

RedactionCategory {
  name: String,
  field_patterns: String[],
  replacement: String,
  metadata_included: Boolean
}

AccessMatrix {
  operator: AccessLevel,
  tenant_own: AccessLevel,
  tenant_other: AccessLevel,
  agent: AccessLevel
}

AccessLevel = "full" | "none" | "own-only"
ReferenceFormat = "marker" | "hash" | "pointer"
```

The redaction policy is defined by the host and MUST be documented in
the conformance profile.
Changes to the redaction policy MUST be recorded as `policy.revision`
evidence records.

> **Normative implementation-defined choice.**
The host defines the exact field patterns used to identify fields in
each redaction category, the format of stable references, and the
mechanism used to enforce access policy at query time.
These choices MUST be documented in the conformance profile.

> **Non-normative note.**
Field patterns for secrets MAY use keyword matching (e.g., `*key*`,
`*secret*`, `*token*`), structural analysis (e.g., Base64-encoded
binary data in known positions), or schema-aware detection (e.g.,
fields typed as `Secret` or annotated with `sensitive: true`).
The choice of detection strategy affects both accuracy and performance
and is an implementation-defined tradeoff.

## 5.2 Behavior And Integration

### Artifact admission flow

> **Normative definition.**
The artifact admission flow is the ordered sequence of steps the host
executes when presented with an `ArtifactAdmissionRequest`.
Every step MUST complete before the next step begins.
A step that fails MUST abort the flow and produce an
`artifact.rejected` evidence record.

| Step | Action | On failure |
|------|--------|------------|
| 1 | Validate `ArtifactAdmissionRequest` structure. | Emit `artifact.admission.malformed` diagnostic. Emit `artifact.rejected` record. |
| 2 | Compute artifact digest using declared `HashAlgorithm`. | Emit `artifact.admission.digest-computation-failed` diagnostic. Emit `artifact.rejected` record. |
| 3 | Verify digest integrity against manifest/attestation. | Emit `artifact.digest-mismatch` diagnostic. Emit `artifact.rejected` record. |
| 4 | Verify artifact signature if present. | Emit `artifact.signature-invalid` diagnostic. Emit `artifact.rejected` record. |
| 5 | Resolve publisher identity from signature. | Emit `artifact.publisher-untrusted` diagnostic. Emit `artifact.rejected` record. |
| 6 | Query revocation lists for artifact and publisher. | Emit `artifact.revoked` diagnostic. Emit `artifact.rejected` record. |
| 7 | Validate build provenance fields. | Emit `artifact.build-provenance-invalid` diagnostic. Emit `artifact.rejected` record. |
| 8 | Resolve and verify all declared dependencies. | Emit `artifact.dependency-unresolved` diagnostic. Emit `artifact.rejected` record. |
| 9 | Check compiler and PDK compatibility policy. | Emit `artifact.compiler-incompatible` diagnostic. Emit `artifact.rejected` record. |
| 10 | Record `artifact.admitted` evidence with full admission result. | N/A (this is the success terminal step). |

> **Non-normative note.**
Steps 3 through 9 are independent checks and MAY be executed in parallel
by a conforming implementation, provided the final admission result is
deterministic and the evidence record reflects the complete set of
checks performed.
Sequential execution is the reference behavior; parallel execution is
an optimization that must not change observable outcomes.

> **Normative definition.**
If the `publisher_hint` field is present and the signing identity does
not match it, the host MUST emit the `artifact.publisher-hint-mismatch`
diagnostic but MUST NOT fail the admission flow on this mismatch alone.
The diagnostic is recorded in the `artifact.admitted` evidence record's
`detail` field for the `publisher_hint` check.

> **Normative definition.**
On successful admission, the host MUST cache the verified artifact in
its dependency cache and record its verified digest, publisher identity,
trust tier, and compatibility metadata.
Cached artifacts MAY be reused by subsequent admission requests without
re-performing checks 2 through 9, provided the cache entry is still
valid (not expired, not revoked, and not superseded by a policy revision).

> **Normative implementation-defined choice.**
The host defines the cache validity policy, including maximum entry age,
conditions for cache invalidation beyond revocation, and the behavior
when a cached artifact's publisher is later revoked (existing instances
are not affected per
[Revocation check](#artifact-admission-verification)).

### Evidence recording flow

> **Normative definition.**
The evidence recording flow is the host-owned process of creating,
writing, and indexing evidence records for each event type defined in
[Host-owned evidence recording](#host-owned-evidence-recording).
The flow has two phases: write and index.

| Phase | Action | Constraint |
|-------|--------|------------|
| **Write** | Create the evidence record with all required fields. | Write is atomic: the record is either fully written or not written at all. |
| **Index** | Index the record by `event_type`, `artifact_id`, `tenant_id`, and `timestamp` for query efficiency. | Indexing is best-effort: a missing index entry does not invalidate the record. |

> **Normative definition.**
The host MUST write the evidence record to durable storage before
proceeding to any downstream action that depends on the record's
existence (such as granting capability access or notifying an agent).
A downstream action that proceeds without a durably written evidence
record is a specification violation.

> **Normative definition.**
Evidence records for `tenant.isolation.violation` and `residue.detected`
events MUST trigger an immediate security alert path in addition to
normal record creation.
The alert path records the event, notifies the operator, and MAY
initiate containment actions such as instance quarantine or tenant
suspension.
The exact containment actions are implementation-defined choices
documented in the conformance profile.

> **Non-normative note.**
The security alert path for isolation violations and residue detection
is what makes the audit system an active security control rather than
a passive log.
Without it, a cross-tenant leak would be visible only in retrospective
forensic analysis.

> **Normative implementation-defined choice.**
The host defines the alert notification mechanism (email, webhook,
dashboard event, or other), the containment action catalog, and the
escalation policy for different severity levels.

### Evidence redaction flow

> **Normative definition.**
The evidence redaction flow is the process the host applies when
serving evidence records to non-operator consumers.
The flow has two modes: operator mode (no redaction) and constrained
mode (redaction applied per the redaction policy defined in
[Evidence redaction](#evidence-redaction)).

| Mode | Redaction applied | Access to unredacted records |
|------|-------------------|------------------------------|
| Operator | None | Full access to all records within retention period. |
| Constrained | Full redaction per policy | Access per access matrix; unredacted fields are replaced with stable references. |

> **Normative definition.**
In constrained mode, the host MUST apply redaction at query time, not
at write time.
The original evidence record is stored unredacted; the redacted view
is a derived representation produced on every read.
This ensures that changes to the redaction policy take effect
immediately for all subsequent queries without requiring record
re-processing.

> **Normative definition.**
The host MUST evaluate the access policy for every field in every
evidence record returned through a constrained-mode query.
A field returned in constrained mode MUST have been evaluated against
the consumer's access level for that field's redaction category.
A field that fails the access check MUST be redacted according to the
policy, regardless of whether the field's content is actually sensitive.

> **Non-normative note.**
Policy-at-query-time redaction is more flexible than write-time
redaction because it supports dynamic policy changes without data
migration.
The tradeoff is per-query computational cost; implementations with
high query throughput SHOULD cache redacted views with a policy-version
stamp and invalidate the cache on policy changes.

> **Normative implementation-defined choice.**
The host defines the query interface for evidence records, the caching
strategy for redacted views, and the cache invalidation protocol on
policy changes.

### Security exercises

> **Normative definition.**
Security exercises are controlled adversarial inputs that exercise the
specific attack vectors listed in
[5.2.1.1](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of the Phase 5 planning document.
Each security exercise simulates a deliberate attack and verifies that
the artifact provenance admission, evidence recording, and evidence
redaction systems detect and reject it.
Security exercises are normative test scenarios; a conforming
implementation MUST detect every attack vector defined below.

| Exercise | Attack vector | Expected host response | Relevant checks |
|----------|--------------|----------------------|-----------------|
| **Malicious imports** | An artifact declares imports from modules that are not permitted by the host's capability policy. | Reject at admission with `artifact.dependency-unresolved` or `artifact.signature-invalid`. | Dependency resolution, signature validity. |
| **Oversized output** | An artifact produces an invocation output that exceeds the output size limit defined in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md). | Truncate or reject at invocation time; record `invocation.failed` with `failure_type: output-oversize`. | Invocation boundary, output validation (see
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md)). |
| **Invalid UTF-8** | An artifact produces an invocation output containing invalid UTF-8 byte sequences in a field declared as UTF-8. | Reject output at invocation time; record `invocation.failed` with `failure_type: invalid-utf8`. | Output validation, UTF-8 conformance. |
| **Forged identity** | An attacker submits an artifact with a signature produced by a key that impersonates a trusted publisher. | Reject with `artifact.signature-invalid` or `artifact.publisher-untrusted`. | Signature validity, publisher identity. |
| **Stale grant** | An artifact's publisher was revoked between the artifact's build and its admission attempt. | Reject with `artifact.revoked`. | Revocation check. |
| **Route confusion** | An artifact exploits ambiguous routing between agent, tenant, and system invocation paths to obtain capabilities it should not receive. | Reject capability grant with `grant.denied` and record `tenant.isolation.violation`. | Grant policy, tenant isolation. |
| **Output injection** | A malicious artifact attempts to inject tenant-specific data into another tenant's evidence records through a shared artifact. | Reject cross-tenant write; record `tenant.isolation.violation` and emit the security alert path. | Tenant isolation, evidence recording. |

> **Normative definition.**
The malicious imports exercise tests that the dependency resolution check
catchs imports that violate the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).
An import is considered malicious if it references a module, function,
or memory region that the host's capability policy does not grant to
the artifact's trust tier.
The exact mechanism for declaring permitted imports (allowlist, denylist,
or capability-attenuation policy) is implementation-defined.

> **Non-normative note.**
Malicious imports are the most common attack vector in WebAssembly
ecosystems because the sandbox boundary alone does not prevent an
artifact from declaring imports that the host is configured to expose.
The defense is at the capability policy layer, not at the sandbox
layer.

> **Normative definition.**
The oversized output exercise tests that the host enforces the output
size limit defined in the conformance profile and in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).
An artifact that produces output exceeding the limit MUST NOT be
allowed to consume unbounded host resources.
The host MUST either truncate the output to the limit and emit a
diagnostic or reject the invocation entirely.
The choice between truncation and rejection is an implementation-defined
choice documented in the conformance profile.

> **Normative definition.**
The invalid UTF-8 exercise tests that the host validates UTF-8
conformance for output fields declared as UTF-8 in the artifact's
manifest or the host's capability policy.
Invalid UTF-8 in a declared UTF-8 field is a specification violation
by the artifact publisher, not a host defect.
The host MUST record the violation in an `invocation.failed` evidence
record and MUST NOT include the invalid bytes in any evidence record
or diagnostic.

> **Normative definition.**
The forged identity exercise tests that the signature validity check
and publisher identity check together prevent an attacker from
impersonating a trusted publisher.
An artifact with a signature that is cryptographically valid but signed
by an untrusted key MUST fail the publisher identity check.
An artifact with a signature that is not cryptographically valid MUST
fail the signature validity check.
The host MUST NOT accept an artifact based solely on the
`publisher_hint` field, as defined in
[Artifact admission verification](#artifact-admission-verification).

> **Normative definition.**
The stale grant exercise tests that the revocation check queries the
active revocation lists at the moment of admission, not at the moment
of build.
An artifact whose publisher was revoked between build and admission
MUST fail the revocation check regardless of whether the artifact
itself was signed before revocation.
The host MUST NOT cache revocation status; the check is performed
fresh for every admission request.

> **Non-normative note.**
The stale grant exercise is the primary defense against supply chain
attacks where an attacker compromises a publisher's signing key after
the key has been registered in the trust store but before the
compromise is detected and the key is revoked.

> **Normative definition.**
The route confusion exercise tests that the host correctly routes
capability grant requests to the appropriate policy and that an
artifact cannot exploit ambiguous routing to obtain capabilities it
should not receive.
A route confusion attack succeeds if an artifact can cause the host
to evaluate its grant request against a more permissive policy than
the one that applies to its actual trust tier, tenant scope, or agent
pin.
The host MUST evaluate grant requests against the correct policy
deterministically and MUST NOT allow an artifact to influence which
policy is evaluated.

> **Non-normative note.**
Route confusion is a subclass of privilege escalation attacks.
The defense is at the policy evaluation layer, not at the sandbox
layer.
The exact mechanism for preventing route confusion (immutable policy
binding, capability attestation, or equivalent) is implementation-defined.

> **Normative definition.**
The output injection exercise tests that the host isolates evidence
records by tenant and rejects cross-tenant writes.
An artifact that attempts to inject tenant-specific data into another
tenant's evidence records MUST be detected and rejected with
`tenant.isolation.violation` and the security alert path.
The host MUST enforce tenant isolation at the evidence writing layer,
not at the guest module layer, because the guest module has no
authority to write evidence records directly.

> **Non-normative note.**
Output injection is the most difficult attack vector to defend against
because it requires the host to enforce isolation between artifacts
that are individually admitted and invoked correctly.
The defense is in the evidence recording flow's tenant-scoped write
semantics defined in
[Evidence recording flow](#evidence-recording-flow).

> **Non-normative note.**
Each security exercise produces an evidence record of the same type
that would be produced by a real attack of the corresponding kind.
This ensures that the security alert path is tested in the same
conditions as a real attack and that the operator receives the same
notification for both test and real events.

### Adversarial isolation exercises

> **Normative definition.**
Adversarial isolation exercises are controlled scenarios that exercise
the specific resilience requirements listed in
[5.2.1.2](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of the Phase 5 planning document.
Each adversarial isolation exercise simulates a deliberate attempt to
breach the system's isolation guarantees and verifies that the system
detects the breach and recovers to a safe state.
Adversarial isolation exercises are normative test scenarios; a
conforming implementation MUST pass every exercise defined below.

| Exercise | Attack vector | Expected host response | Relevant invariants |
|----------|--------------|----------------------|--------------------|
| **Tenant residue** | A guest module invocation leaves state in another tenant's scope after completion. | Detect residue with `residue.detected`; quarantine the instance; require operator review. | Tenant isolation, instance mode. |
| **Pool reset** | A compromised instance in a shared pool retains state after reset. | Detect residue post-reset with `residue.detected`; escalate to operator. | Instance pool, reset semantics. |
| **Cancellation races** | An artifact exploits a race between invocation cancellation and state commit to leave partial state. | Detect partial state with `residue.detected`; roll back to pre-invocation state. | Cancellation, atomicity. |
| **Capability revocation** | An artifact retains capabilities after its grant is revoked mid-invocation. | Detect retained capabilities; revoke them; record `tenant.isolation.violation`. | Capability policy, revocation. |
| **Compromised plugin upgrade** | A malicious plugin upgrade replaces a trusted plugin in an agent's pin without re-admission. | Detect unverified upgrade; reject with `artifact.admission.failed`; require full re-admission. | Artifact admission, agent pin lifecycle. |
| **Audit tampering** | An attacker modifies or deletes evidence records after writing. | Detect modification with `evidence.integrity-violation`; emit security alert; quarantine affected records. | Evidence integrity, audit log. |

> **Normative definition.**
The tenant residue exercise tests that the host's instance mode
policies and tenant isolation invariants prevent a guest module from
leaving state in another tenant's scope.
Tenant residue is detected by comparing the host's view of each
tenant's state before and after an invocation.
If any state change is observed in a tenant's scope that is not
attributable to that tenant's own invocation, the host MUST emit
`residue.detected`.
The exact mechanism for detecting tenant residue (state snapshots,
capability auditing, or equivalent) is implementation-defined.

> **Non-normative note.**
Tenant residue is the most dangerous isolation failure because it
enables cross-tenant data exfiltration without triggering the
`tenant.isolation.violation` diagnostic, which is only emitted for
detected violations, not for successful stealthy leaks.
The residue detection mechanism is a defense-in-depth control that
catches violations that the primary isolation layer misses.

> **Normative definition.**
The pool reset exercise tests that the host's instance pool reset
semantics eliminate all state from a returned instance, including
any state that the instance may have retained in host-managed memory,
registers, or auxiliary data structures.
If any state remains after reset, the host MUST emit `residue.detected`
and MUST NOT return the instance to the pool for reuse.
The instance MUST be quarantined for operator review.

> **Non-normative note.**
Pool reset is critical for instance pool reuse because the same
instance may be used by multiple tenants over its lifecycle.
If reset is incomplete, a subsequent tenant may observe residue from
a previous tenant's invocation.

> **Normative definition.**
The cancellation races exercise tests that the host's cancellation
semantics prevent an artifact from exploiting a race between
invocation cancellation and state commit to leave partial state.
A cancellation race attack succeeds if an artifact can cause the host
to commit a partially-computed state change that is not rolled back
on cancellation.
The host MUST enforce atomicity for all state-changing operations,
as defined in
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
and MUST roll back any partial state on cancellation.

> **Non-normative note.**
Cancellation races are timing-dependent and difficult to test
deterministically.
The defense is at the atomicity layer, not at the cancellation layer.
If the atomic state journal is correctly implemented, cancellation
races are impossible by construction.

> **Normative definition.**
The capability revocation exercise tests that the host enforces
capability revocation immediately and completely.
If a capability grant is revoked mid-invocation, the host MUST
revoke the corresponding capabilities from the invoking instance
immediately and MUST NOT allow the instance to continue using
revoked capabilities.
The host MUST record the revocation in a `grant.denied` evidence
record and MUST emit `tenant.isolation.violation` if the instance
attempts to use revoked capabilities after revocation.

> **Non-normative note.**
Capability revocation is a liveness property: the system must
respond to revocation within a bounded time, not eventually.
The exact bounded time is an implementation-defined choice documented
in the conformance profile.

> **Normative definition.**
The compromised plugin upgrade exercise tests that the host does not
allow a plugin to be upgraded in an agent's pin without going through
the full artifact admission flow.
A compromised plugin upgrade attack succeeds if a malicious actor
can replace a trusted plugin in an agent's pin without re-admission,
either through a direct file system replacement, a cache poisoning
attack, or a lifecycle hook exploitation.
The host MUST verify the plugin's admission status at the moment of
use, not at the moment of installation, and MUST reject any plugin
that has not been admitted since its last modification.

> **Non-normative note.**
The compromised plugin upgrade exercise is the primary defense against
supply chain attacks that target the plugin lifecycle rather than the
artifact admission layer.
It ensures that the admission gate is not a one-time check but a
continuous invariant enforced at every point of use.

> **Normative definition.**
The audit tampering exercise tests that the host's evidence integrity
checks and audit log detect any modification or deletion of evidence
records.
An audit tampering attack succeeds if an attacker can modify or
delete an evidence record without triggering `evidence.integrity-violation`
or the security alert path.
The host MUST enforce evidence immutability as defined in
[Host-owned evidence recording](#host-owned-evidence-recording),
and MUST detect any tampering attempt with the integrity check.

> **Non-normative note.**
Audit tampering is the most serious adversarial scenario because it
undermines the entire audit system.
If an attacker can modify evidence records, the operator has no way
to distinguish between legitimate events and fabricated ones.
The defense is evidence immutability, which is the primary invariant
of the audit system.

> **Non-normative note.**
Each adversarial isolation exercise produces an evidence record of
the same type that would be produced by a real attack of the
corresponding kind.
This ensures that the security alert path is tested in the same
conditions as a real attack and that the operator receives the same
notification for both test and real events.
It also ensures that the detection and containment mechanisms work
correctly for both test and real scenarios.

### Threat-to-control matrix publication

> **Normative definition.**
The threat-to-control matrix is a structured publication that maps each
threat identified in this phase to the control that mitigates it, the
adversarial test result, any accepted residual risk, and the required
operator response.
The threat-to-control matrix is normative evidence for Milestone 5
acceptance; it MUST be published as part of the phase completion
evidence bundle.

> **Normative definition.**
The threat-to-control matrix contains one row for each threat-control
pair.
Each row contains the following fields:

| Field | Required | Content |
|-------|----------|---------|
| `threat_id` | Yes | Stable identifier for the threat (e.g., `T-5-01`). |
| `threat_description` | Yes | Human-readable description of the threat. |
| `control_id` | Yes | Stable identifier for the control that mitigates the threat (e.g., `C-5-01`). |
| `control_description` | Yes | Human-readable description of the control. |
| `control_type` | Yes | The control type: `preventive`, `detective`, `corrective`, or `deterrent`. |
| `adversarial_test_result` | Yes | The result of the corresponding security or adversarial isolation exercise: `passed`, `failed`, or `deferred`. |
| `residual_risk` | Yes | The residual risk after the control is applied: `accepted`, `mitigated`, or `unmitigated`. |
| `residual_risk_rationale` | Conditional | If `residual_risk` is `accepted` or `unmitigated`, a human-readable rationale explaining why the residual risk is acceptable or what additional work is required. |
| `operator_response` | Yes | The required operator action if the control is triggered: `monitor`, `investigate`, `contain`, `remediate`, or `escalate`. |

> **Normative definition.**
The threat-to-control matrix MUST include rows for every threat
identified in the security exercises and adversarial isolation
exercises of this section, plus every threat identified in the
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
No threat identified in the threat model or in this phase's exercises
MAY be omitted from the matrix.

> **Non-normative note.**
The threat-to-control matrix is the primary artifact that demonstrates
that the phase has completed its security review.
It provides the milestone acceptance reviewers with a single
document that maps every threat to its mitigation, test result, and
required operator response.
Without the matrix, the reviewers have no structured evidence that
the security review is complete.

> **Normative definition.**
A threat with `residual_risk: unmitigated` blocks milestone acceptance.
A threat with `residual_risk: accepted` requires a documented rationale
and operator approval before milestone acceptance.
A threat with `residual_risk: mitigated` does not block milestone
acceptance, provided the corresponding control passed its adversarial
test.

> **Normative implementation-defined choice.**
The host defines the format and storage mechanism for the threat-to-control
matrix.
The matrix MUST be machine-readable (YAML, JSON, or equivalent) and
MUST be includable in the phase's evidence bundle.
The exact format is an implementation-defined choice documented in
the conformance profile.

> **Non-normative note.**
The threat-to-control matrix is distinct from the bounded diagnostics
defined in
[5.3 Failure Evidence And Operational Notes](#53-failure-evidence-and-operational-notes).
Bounded diagnostics are per-failure instances; the threat-to-control
matrix is a strategic overview of all threats and their mitigations.
The matrix references bounded diagnostics by `evidence_hash` where
applicable.

## 5.3 Failure Evidence And Operational Notes

### Failure outcomes for artifact admission

> **Non-normative note.**
The canonical failure outcomes for artifact admission are listed below.
Detailed failure semantics, error codes, and diagnostic format
requirements are defined in the Phase 5
[Failure Evidence And Operational Notes](#53-failure-evidence-and-operational-notes)
section.

1. **Malformed**: The `ArtifactAdmissionRequest` does not conform to
   the schema defined in
   [Artifact admission verification](#artifact-admission-verification).
2. **Digest mismatch**: The artifact's computed digest does not match
   the recorded digest.
3. **Signature invalid**: The artifact's signature is cryptographically
   invalid, expired, or produced by an unknown key.
4. **Publisher untrusted**: The signing identity does not map to a
   known, active publisher in the trust store.
5. **Publisher hint mismatch**: The `publisher_hint` field does not
   match the identity derived from the artifact's signature.
6. **Build provenance invalid**: The build record is missing required
   fields or contains values that fail validation.
7. **Dependency unresolved**: A declared dependency cannot be resolved
   to a verified, non-revoked artifact.
8. **Compiler incompatible**: The artifact's compiler or PDK version
   is not in the compatibility policy.
9. **Revoked**: The artifact or its publisher is on an active
   revocation list.
10. **Dependency cycle**: The artifact's dependency graph contains a cycle.
11. **Cache failure**: The host cannot read or write its dependency
    cache.
12. **Trust store failure**: The host cannot read its publisher trust
    store or revocation lists.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and
bounded diagnostic following the naming convention
`artifact.admission.<subtype>` where `<subtype>` corresponds to the
failure outcome name in lowercase with hyphens.

### Failure outcomes for evidence recording

> **Non-normative note.**
The canonical failure outcomes for evidence recording are listed below.

1. **Write failure**: The host cannot durably write an evidence record.
2. **Integrity violation**: An evidence record's integrity check fails.
3. **Retention policy violation**: An evidence record is deleted before
   the minimum retention period expires without operator action.
4. **Audit log failure**: The host cannot write to the evidence access
   audit log.
5. **Alert path failure**: The security alert path for isolation
   violations or residue detection fails to deliver the alert.
6. **Index failure**: The host cannot update an evidence record index
   entry, though the record itself was written successfully.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and
bounded diagnostic following the naming convention
`evidence.<subtype>` where `<subtype>` corresponds to the failure
outcome name in lowercase with hyphens.

### Failure outcomes for evidence redaction

> **Non-normative note.**
The canonical failure outcomes for evidence redaction are listed below.

1. **Redaction policy error**: The redaction policy is malformed or
   missing required fields.
2. **Access evaluation error**: The host cannot evaluate the access
   policy for a field, due to a missing policy dimension or an
   ambiguous consumer classification.
3. **Reference format error**: The host cannot produce a valid stable
   reference for a redacted field.
4. **Cache invalidation failure**: A redacted view cache entry is not
   invalidated after a policy change.
5. **Query interface failure**: The host's evidence query interface
   is unavailable.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and
bounded diagnostic following the naming convention
`redaction.<subtype>` where `<subtype>` corresponds to the failure
outcome name in lowercase with hyphens.

### Bounded diagnostics and evidence

> **Normative definition.**
The host MUST emit a bounded diagnostic for every failure outcome
listed in the previous subsections.
A bounded diagnostic is a structured report that contains exactly
the following fields:

| Field | Required | Content |
|-------|----------|---------|
| `error_code` | Yes | Stable diagnostic identifier following the naming conventions defined in this section. |
| `phase` | Yes | The phase name, `phase-05-provenance-signing-audit-security-and-milestone-acceptance`. |
| `contract` | Yes | The subsection of this chapter where the failure boundary was crossed. |
| `profile` | Yes | The instance mode, tenant scope, or capability scope in effect at the time of failure. |
| `failed_boundary` | Yes | A human-readable description of the specific invariant or bound that was violated. |
| `invocation_id` | Conditional | Present if the failure occurred during an invocation; omitted for load-time or registration-time failures. |
| `tenant_id` | Conditional | Present if the failure is tenant-scoped; omitted if the failure is system-scoped. |
| `evidence_hash` | Yes | A cryptographic hash of the minimal evidence record that supports the diagnostic. |

> **Normative definition.**
The diagnostic MUST NOT contain any of the following:
- Raw guest module bytecode or data section contents.
- Secrets, keys, or credentials in any form.
- Tenant-specific state values or identifiers beyond `tenant_id`.
- Native memory addresses, stack traces, or process-internal pointers.
- Wall-clock timestamps beyond a coarse-grained duration window
  documented in the conformance profile.

> **Non-normative note.**
Bounded diagnostics for Phase 5 share the same design principles as
the bounded diagnostics defined in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md#bounded-diagnostics-and-evidence).
The error code naming conventions differ by phase; the structure and
redaction rules are consistent.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented
in the conformance profile.

1. **Error code catalog**: The exact error code catalog for the
   `artifact.admission.<subtype>`, `evidence.<subtype>`, and
   `redaction.<subtype>` naming conventions.
2. **Signature scheme**: The cryptographic signature scheme used for
   artifact signature verification.
3. **Hash algorithm**: The hash algorithm used for digest computation
   and evidence hashing.
4. **Evidence storage**: The storage mechanism, integrity check
   mechanism, and retention period for evidence records.
5. **Redaction field patterns**: The exact field patterns used to
   identify fields in each redaction category.
6. **Redaction cache strategy**: The caching strategy for redacted
   views and the invalidation protocol on policy changes.
7. **Security alert mechanism**: The alert notification mechanism and
   containment action catalog for isolation violations and residue
   detection.
8. **Publisher trust store format**: The exact format and update
   protocol for the publisher trust store and revocation lists.

> **Non-normative note.**
These implementation-defined choices do not alter the conformance
obligations defined elsewhere in this chapter.
They only define how an implementation realizes those obligations
in a specific host language and runtime.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations.
None of the items below are required for Phase 5 conformance.
Deferred items MUST be tracked in the phase's planning document and
MUST NOT be implied as mandatory by any normative text in this chapter.

1. **Cross-host provenance aggregation**: Aggregating provenance
   records across multiple host instances for multi-node deployments.
   This work requires a distributed provenance consensus protocol.
2. **Automated trust tier migration**: Automatic promotion or demotion
   of a publisher's trust tier based on observed behavior, subject to
   strict audit and operator approval.
   This work requires a trust tier evaluation engine and a formal
   migration procedure.
3. **Provenance attestation chaining**: Linking provenance records
   across supply chain stages (source code -> build -> sign -> deploy)
   into a single verifiable chain.
   This work requires a chain-of-custody data model and verification
   protocol.
4. **Dynamic redaction policy extension**: Runtime addition of new
   redaction categories or field patterns, subject to a formal
   extension procedure.
   This work requires a redaction policy registry and a host policy
   extension.
5. **Provenance-based admission optimization**: Skipping redundant
   admission checks for artifacts whose provenance chain is already
   fully verified by a trusted upstream host.
   This work requires a cross-host provenance trust protocol.
6. **Evidence query language**: A structured query language for
   evidence records that supports time-range, tenant-scope, and
   event-type filtering with access policy enforcement.
   This work requires a query parser and an access-aware query planner.

> **Non-normative note.**
Each deferred item above has a defined triggering condition that would
promote it to a later phase:
observable operator demand, a security audit recommendation, or
a performance benchmark result that demonstrates a clear need.
Deferral is not a default position; it requires an explicit trigger.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 5 MAY invalidate earlier milestone
assumptions.
Each invalidation triggers a revision of the affected milestone and
a re-validation of the affected fixtures.
The revision process is governed by
[Specification Authority](../SPECIFICATION-AUTHORITY.md) and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

1. **Provenance gaps**: If verified artifacts are admitted that later
   produce security incidents traceable to gaps in the provenance
   chain, the admission checks defined in this chapter MUST be revised.
   The trigger is any security incident where the root cause is an
   artifact that passed admission but lacked a provenance check
   that should have caught it.
2. **Audit tampering**: If evidence records are modified or deleted
   without triggering the integrity violation diagnostic, the
   immutability guarantees defined in this chapter MUST be revised.
   The trigger is any observed evidence record modification that is
   not detected by the integrity check.
3. **Redaction bypass**: If constrained-mode consumers can observe
   data they should not see due to a redaction policy evaluation
   failure, the redaction enforcement MUST be revised.
   The trigger is any observed data leak through the redaction layer.
4. **Admission performance**: If artifact admission exceeds the turn
   timeout defined in
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md)
   under the policy constraints of this chapter, the timeout or
   admission optimization policy MUST be revised.
   The trigger is a measured admission flow that exceeds the turn
   timeout by more than the host's documented admission overhead.
5. **Dependency cache scalability**: If the dependency cache does not
   scale to the expected number of artifacts and dependencies, the
   cache mechanism MUST be revised.
   The trigger is a cache lookup latency that exceeds the host's
   documented cache overhead for the expected artifact count.
6. **Publisher trust store availability**: If the publisher trust
   store or revocation lists are unavailable during admission, the
   host MUST define a graceful degradation policy.
   The trigger is any admission failure caused by trust store
   unavailability that is not covered by the defined degradation
   policy.

> **Non-normative note.**
If any result from Phase 5 invalidates an earlier milestone assumption,
the affected milestone MUST be revised and re-validated.
The revision process is governed by
[Specification Authority](../SPECIFICATION-AUTHORITY.md) and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).
All invalidated assumptions MUST be recorded in the phase's journal
evidence and in the affected milestone's revision history.

## 5.4 Phase 5 Integration Tests

### Test objectives

> **Normative definition.**
The Phase 5 integration tests verify that the artifact provenance
admission, evidence recording, and evidence redaction systems operate
as an integrated whole rather than as a collection of independently
passing unit tests.
The objectives below are exhaustive for Phase 5 integration evidence.

1. **Canonical flow**: Artifact admission, evidence recording, and
   evidence redaction operate successfully when all preconditions
   defined in
   [Contract And Data Model](#51-contract-and-data-model) and
   [Behavior And Integration](#52-behavior-and-integration) are satisfied.
2. **Failure handling**: Malformed, incompatible, stale, duplicate,
   and boundary-limit inputs produce stable, bounded diagnostics and
   leave no unauthorized residue, as defined in
   [Failure Evidence And Operational Notes](#53-failure-evidence-and-operational-notes).
3. **Adversarial isolation**: Malicious imports, forged identity,
   stale grants, and audit tampering attempts are detected and
   rejected, as defined in
   [Artifact admission verification](#artifact-admission-verification)
   and
   [Evidence recording](#host-owned-evidence-recording).
4. **Redaction correctness**: Constrained-mode queries return correctly
   redacted evidence that preserves field semantics without leaking
   sensitive data, as defined in
   [Evidence redaction](#evidence-redaction).

> **Non-normative note.**
These four objectives correspond directly to the four subtasks of the
Phase 5 integration test section defined in the planning document.
Each objective produces its own evidence bundle; the bundles are
assembled together to satisfy the phase promotion criterion defined in
this chapter's Status And Authority section.

### Successful flow tests

> **Normative definition.**
Successful flow tests verify that the artifact provenance system
produces the expected observable outcome when every precondition
defined in this chapter is satisfied.
A successful flow test MUST exercise at least one fully verified
artifact through the complete admission flow, record evidence for
every event type, and verify redaction correctness for both operator
and constrained modes.

#### Artifact admission success

1. **Fully verified artifact**: Submit an `ArtifactAdmissionRequest`
   for an artifact with valid signature, known publisher, complete
   build provenance, resolved dependencies, compatible compiler/PDK,
   and no revocation entries.
   The host MUST admit the artifact, emit an `artifact.admitted`
   evidence record with `passed: true` for all checks, and cache
   the artifact for subsequent reuse.
2. **Publisher hint mismatch**: Submit an `ArtifactAdmissionRequest`
   with a `publisher_hint` that does not match the signing identity.
   The host MUST admit the artifact (assuming all other checks pass),
   emit a `publisher-hint-mismatch` diagnostic in the evidence record,
   and NOT fail admission on this mismatch alone.
3. **Cached artifact reuse**: Submit a second `ArtifactAdmissionRequest`
   for an artifact already cached from the first admission.
   The host MUST skip redundant verification checks and admit the
   artifact using the cached entry.
4. **Parallel check execution**: Submit an `ArtifactAdmissionRequest`
   and measure whether checks 3 through 9 execute in parallel.
   The host MUST produce a deterministic admission result regardless
   of execution order.
   Parallel execution is an allowed optimization; it must not change
   observable outcomes.

#### Evidence recording success

1. **Complete evidence chain**: Run a complete artifact lifecycle
   (admission, invocation start, invocation completion, tenant
   isolation verification) and verify that an evidence record is
   created for each event type in the correct order.
2. **Durable write**: Interrupt the host after an evidence record
   write and verify that the record survives restart.
3. **Integrity check**: Modify an evidence record's bytes after
   writing and verify that the integrity check detects the
   modification on the next read.
4. **Audit log**: Verify that every evidence record access (read,
   write, delete) produces an entry in the audit log.

#### Evidence redaction success

1. **Operator mode**: Query evidence records in operator mode and
   verify that all fields are unredacted.
2. **Constrained mode - secrets**: Query evidence records in
   constrained mode and verify that fields matching the `Secrets`
   redaction category are replaced with `<REDACTED>` markers.
3. **Constrained mode - prompts**: Query evidence records in
   constrained mode as a tenant and verify that own prompts are
   visible but other tenants' prompts are redacted.
4. **Constrained mode - large payloads**: Query evidence records in
   constrained mode and verify that fields exceeding the size limit
   are replaced with `<LARGE-PAYLOAD: {size}>` markers.
5. **Constrained mode - tenant-sensitive**: Query evidence records
   in constrained mode and verify that cross-tenant data is
   redacted for non-operator consumers.
6. **Policy change propagation**: Change the redaction policy and
   verify that subsequent queries reflect the new policy without
   requiring record re-processing.

### Failure handling tests

> **Normative definition.**
Failure handling tests verify that every failure outcome defined in
[Failure outcomes for artifact admission](#failure-outcomes-for-artifact-admission),
[Failure outcomes for evidence recording](#failure-outcomes-for-evidence-recording),
and [Failure outcomes for evidence redaction](#failure-outcomes-for-evidence-redaction)
produces a stable diagnostic and leaves no unauthorized state.

1. **Malformed request**: Submit a malformed `ArtifactAdmissionRequest`
   and verify the `artifact.admission.malformed` diagnostic.
2. **Digest mismatch**: Submit an artifact with an incorrect digest
   in the manifest and verify the `artifact.digest-mismatch` diagnostic.
3. **Invalid signature**: Submit an artifact with a cryptographically
   invalid signature and verify the `artifact.signature-invalid`
   diagnostic.
4. **Unknown publisher**: Submit an artifact signed by an unknown key
   and verify the `artifact.publisher-untrusted` diagnostic.
5. **Revoked artifact**: Submit an artifact whose digest is on the
   revocation list and verify the `artifact.revoked` diagnostic.
6. **Missing dependency**: Submit an artifact with an unresolved
   dependency and verify the `artifact.dependency-unresolved` diagnostic.
7. **Incompatible compiler**: Submit an artifact built with an
   unsupported compiler and verify the `artifact.compiler-incompatible`
   diagnostic.
8. **Evidence write failure**: Simulate a durable storage failure
   during evidence writing and verify the `evidence.write-failure`
   diagnostic and that no downstream action proceeds without the
   record.
9. **Redaction policy error**: Submit a malformed redaction policy
   and verify the `redaction.policy-error` diagnostic.
10. **Access evaluation error**: Simulate an ambiguous consumer
    classification during a constrained-mode query and verify the
    `redaction.access-evaluation-error` diagnostic.

### Adversarial isolation tests

> **Non-normative note.**
The adversarial isolation tests exercise the specific attack vectors
listed in the Phase 5 planning document's behavior and integration
subtasks.
Each test simulates a deliberate attack and verifies that the system
detects and rejects it.

1. **Forged identity**: Submit an artifact with a signature produced
   by a key that the operator attempts to impersonate as a trusted
   publisher.
   The host MUST reject with `artifact.signature-invalid` or
   `artifact.publisher-untrusted`.
2. **Stale grant**: Submit an artifact whose publisher was revoked
   between the artifact's build and its admission attempt.
   The host MUST reject with `artifact.revoked`.
3. **Dependency poisoning**: Submit an artifact whose dependency
   graph includes a dependency that resolves to a malicious artifact.
   The host MUST reject with `artifact.dependency-unresolved`.
4. **Audit tampering**: Modify an evidence record after writing and
   verify the `evidence.integrity-violation` diagnostic and the
   security alert path.
5. **Redaction bypass**: Attempt to access unredacted secrets or
   tenant-sensitive data through a constrained-mode query as a
   non-operator consumer.
   The host MUST redact the data per the access matrix.
6. **Output injection**: Attempt to inject tenant-specific data into
   another tenant's evidence records through a shared artifact.
   The host MUST isolate evidence records by tenant and reject
   cross-tenant writes.

### Boundary and limit tests

> **Non-normative note.**
The boundary and limit tests exercise the size, count, and performance
limits defined in this chapter and in related chapters.

1. **Large artifact**: Submit an artifact whose size exceeds the
   host's documented maximum artifact size limit.
   The host MUST reject with an `implementation-limit` diagnostic.
2. **Many dependencies**: Submit an artifact with a dependency graph
   that exceeds the host's documented maximum dependency count.
   The host MUST reject with an `implementation-limit` diagnostic.
3. **Many evidence records**: Generate a high volume of evidence
   records and verify that query performance remains within the
   host's documented latency bounds.
4. **Redaction policy churn**: Apply many redaction policy changes in
   rapid succession and verify that cache invalidation keeps pace
   and no stale redacted views are served.

## Variability register

The following table enumerates every `MAY`, `SHOULD`, `SHOULD NOT`,
implementation limit, and implementation-defined choice in this chapter.
Each row references the normative text that licenses the variation.

| Item | License | Type | Bound / Choice | Profile requirement |
|------|---------|------|----------------|--------------------|
| Hash algorithm | [Digest integrity](#artifact-admission-verification) | Implementation-defined | `sha256`, `sha384`, `sha512`, or `blake3` | Publish selected algorithm. |
| Signature scheme | [Signature validity](#artifact-admission-verification) | Implementation-defined | Ed25519, RSA-PSS, ECDSA, or equivalent | Publish selected scheme and key sizes. |
| Publisher trust store format | [Publisher identity](#artifact-admission-verification) | Implementation-defined | File, database, or distributed store | Publish format, update protocol, and maximum size. |
| Revocation list update semantics | [Revocation check](#artifact-admission-verification) | Implementation-defined | Immediate or batched propagation | Publish propagation delay. |
| Dependency cache policy | [Cached artifact reuse](#artifact-admission-verification) | Implementation-defined | Max age, invalidation triggers | Publish policy and invalidation conditions. |
| Dependency cycle detection algorithm | [Dependency resolution](#artifact-admission-verification) | Implementation-defined | DFS, Tarjan's SCC, or equivalent | Publish algorithm. |
| Evidence record storage | [Host-owned evidence recording](#host-owned-evidence-recording) | Implementation-defined | Database, file system, object store, or distributed log | Publish mechanism, integrity check, and retention period. |
| Evidence integrity check | [Evidence integrity](#host-owned-evidence-recording) | Implementation-defined | Append-only log, Merkle tree, hash chain, or equivalent | Publish mechanism. |
| Evidence retention period | [Evidence retention](#host-owned-evidence-recording) | Implementation limit | Minimum retention period | Publish period in days. |
| Redaction field patterns | [Evidence redaction](#evidence-redaction) | Implementation-defined | Keyword, structural, schema-aware, or hybrid | Publish patterns and detection strategy. |
| Stable reference format | [Stable references](#evidence-redaction) | Implementation-defined | Marker, hash, or pointer | Publish format. |
| Redaction cache strategy | [Evidence redaction flow](#evidence-redaction-flow) | Implementation-defined | Cache with policy-version stamp or no cache | Publish strategy and invalidation protocol. |
| Security alert mechanism | [Evidence recording flow](#evidence-recording-flow) | Implementation-defined | Email, webhook, dashboard, or other | Publish mechanism and escalation policy. |
| Containment actions | [Evidence recording flow](#evidence-recording-flow) | Implementation-defined | Quarantine, suspend, or other | Publish action catalog. |
| Large payload size limit | [Large payloads](#evidence-redaction) | Implementation limit | Byte threshold | Publish threshold. |
| Operator large payload threshold | [Large payloads](#evidence-redaction) | Implementation limit | Byte threshold for operator-only access | Publish threshold. |
| Admission parallelism | [Artifact admission flow](#artifact-admission-flow) | Implementation-defined | Sequential or parallel checks 3-9 | Publish execution model. |
| Maximum artifact size | [Boundary and limit tests](#boundary-and-limit-tests) | Implementation limit | Byte threshold | Publish threshold. |
| Maximum dependency count | [Boundary and limit tests](#boundary-and-limit-tests) | Implementation limit | Count threshold | Publish threshold. |
