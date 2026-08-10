---
title: "Phase 5 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-05
  - implementation
  - behavior-and-integration
  - artifact-admission-flow
  - evidence-recording-flow
  - evidence-redaction-flow
  - security-exercises
  - adversarial-isolation
  - threat-to-control-matrix
aliases:
  - "M5-P5-5.2 Implementation"
---

# Phase 5 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 5.2 (Behavior And Integration) from
[Phase 5 - Provenance Signing Audit Security And Milestone Acceptance](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-05-provenance-signing-audit-security-and-milestone-acceptance.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[34-provenance-signing-audit-security-and-milestone-acceptance.md](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
which defines artifact admission flow, evidence recording flow, evidence
redaction flow, security exercises, adversarial isolation exercises, and
threat-to-control matrix publication.

## Subtask 5.2.1.1: Exercise malicious imports, oversized output, invalid UTF-8, forged identity, stale grant, route confusion, and output injection

### Implementation

Defined seven security exercises that simulate deliberate attacks and verify
that artifact provenance admission, evidence recording, and evidence redaction
systems detect and reject them:

| Exercise | Attack Vector | Expected Host Response | Relevant Checks |
|----------|--------------|----------------------|-----------------|
| Malicious imports | Artifact declares imports from modules not permitted by capability policy | Reject at admission if dependency resolution identifies unresolvable imports; otherwise detect at invocation time with `invocation.failed` and `capability-policy-violation` | Dependency resolution, capability policy, invocation boundary |
| Oversized output | Artifact produces invocation output exceeding output size limit | Truncate or reject at invocation time; record `invocation.failed` with `failure_type: output-oversize` | Invocation boundary, output validation (see [20-extism-invocation-boundary-instances-and-output-validation.md](../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)) |
| Invalid UTF-8 | Artifact produces invocation output containing invalid UTF-8 byte sequences in field declared as UTF-8 | Reject output at invocation time; record `invocation.failed` with `failure_type: invalid-utf8` | Output validation, UTF-8 conformance |
| Forged identity | Attacker submits artifact with signature produced by key impersonating trusted publisher | Reject with `artifact.signature-invalid` or `artifact.publisher-untrusted` | Signature validity, publisher identity |
| Stale grant | Artifact's publisher was revoked between artifact's build and its admission attempt | Reject with `artifact.revoked` | Revocation check |
| Route confusion | Artifact exploits ambiguous routing between agent, tenant, and system invocation paths to obtain capabilities it should not receive | Reject capability grant with `grant.denied` and record `tenant.isolation.violation` | Grant policy, tenant isolation |
| Output injection | Malicious artifact attempts to inject tenant-specific data into another tenant's evidence records through shared artifact | Reject cross-tenant write; record `tenant.isolation.violation` and emit security alert path | Tenant isolation, evidence recording |

**Malicious imports**: Tests that dependency resolution check catches imports
that violate capability policy. An import is malicious if it references a
module, function, or memory region that host's capability policy does not
grant to artifact's trust tier.

**Oversized output**: Tests that host enforces output size limit. Artifact
that produces output exceeding limit MUST NOT consume unbounded host
resources. Host MUST either truncate output to limit and emit diagnostic
or reject invocation entirely.

**Invalid UTF-8**: Tests that host validates UTF-8 conformance for output
fields declared as UTF-8. Invalid UTF-8 in declared UTF-8 field is
specification violation by artifact publisher, not host defect. Host MUST
record violation in `invocation.failed` evidence record and MUST NOT include
invalid bytes in any evidence record or diagnostic.

**Forged identity**: Tests that signature validity check and publisher
identity check together prevent attacker from impersonating trusted
publisher. Artifact with signature cryptographically valid but signed by
untrusted key MUST fail publisher identity check. Artifact with signature
not cryptographically valid MUST fail signature validity check. Host MUST
NOT accept artifact based solely on `publisher_hint` field.

**Stale grant**: Tests that revocation check queries active revocation
lists at moment of admission, not at moment of build. Artifact whose
publisher was revoked between build and admission MUST fail revocation
check regardless of whether artifact itself was signed before revocation.
Host MUST NOT cache revocation status; check is performed fresh for every
admission request.

**Route confusion**: Tests that host correctly routes capability grant
requests to appropriate policy. Artifact cannot exploit ambiguous routing
to obtain capabilities it should not receive. Host MUST evaluate grant
requests against correct policy deterministically and MUST NOT allow
artifact to influence which policy is evaluated.

**Output injection**: Tests that host isolates evidence records by tenant
and rejects cross-tenant writes. Artifact that attempts to inject tenant-
specific data into another tenant's evidence records MUST be detected and
rejected with `tenant.isolation.violation` and security alert path. Host
MUST enforce tenant isolation at evidence writing layer, not at guest
module layer, because guest module has no authority to write evidence
records directly.

### Design decisions

1. **Security exercises are normative test scenarios**: A conforming
   implementation MUST detect every attack vector defined below. This
   ensures that security controls are tested in the same conditions
   as real attacks.

2. **Each security exercise produces same evidence record as real attack**:
   This ensures that security alert path is tested in same conditions
   as real attack and that operator receives same notification for both
   test and real events.

3. **Output injection is most difficult attack vector**: The defense is
   in evidence recording flow's tenant-scoped write semantics. Guest
   module has no authority to write evidence records directly; host
   enforces tenant isolation at evidence writing layer.

4. **Malicious imports are most common attack vector**: The defense is
   at capability policy layer, not at sandbox layer. Sandbox boundary
   alone does not prevent artifact from declaring imports that host
   is configured to expose.

## Subtask 5.2.1.2: Exercise tenant residue, pool reset, cancellation races, capability revocation, compromised plugin upgrade, and audit tampering

### Implementation

Defined six adversarial isolation exercises that simulate deliberate
attempts to breach system's isolation guarantees and verify that system
detects breach and recovers to safe state:

| Exercise | Attack Vector | Expected Host Response | Relevant Invariants |
|----------|--------------|----------------------|--------------------|
| Tenant residue | Guest module invocation leaves state in another tenant's scope after completion | Detect residue with `residue.detected`; quarantine instance; require operator review | Tenant isolation, instance mode |
| Pool reset | Compromised instance in shared pool retains state after reset | Detect residue post-reset with `residue.detected`; escalate to operator | Instance pool, reset semantics |
| Cancellation races | Artifact exploits race between invocation cancellation and state commit to leave partial state | Detect partial state with `residue.detected`; roll back to pre-invocation state | Cancellation, atomicity |
| Capability revocation | Artifact retains capabilities after grant is revoked mid-invocation | Detect retained capabilities; revoke them; record `tenant.isolation.violation` | Capability policy, revocation |
| Compromised plugin upgrade | Malicious plugin upgrade replaces trusted plugin in agent's pin without re-admission | Detect unverified upgrade; reject with `artifact.admission.failed`; require full re-admission | Artifact admission, agent pin lifecycle |
| Audit tampering | Attacker modifies or deletes evidence records after writing | Detect modification with `evidence.integrity-violation`; emit security alert; quarantine affected records | Evidence integrity, audit log |

**Tenant residue**: Most dangerous isolation failure because it enables
cross-tenant data exfiltration without triggering `tenant.isolation.violation`
diagnostic (which is only emitted for detected violations, not for
successful stealthy leaks). Residue detection mechanism is defense-in-depth
control that catches violations that primary isolation layer misses.

**Pool reset**: Critical for instance pool reuse because same instance
may be used by multiple tenants over its lifecycle. If reset is
incomplete, subsequent tenant may observe residue from previous tenant's
invocation.

**Cancellation races**: Timing-dependent and difficult to test
deterministically. Defense is at atomicity layer, not at cancellation
layer. If atomic state journal is correctly implemented, cancellation
races are impossible by construction.

**Capability revocation**: Liveness property: system must respond to
revocation within bounded time, not eventually. Exact bounded time is
implementation-defined choice documented in conformance profile.

**Compromised plugin upgrade**: Primary defense against supply chain
attacks that target plugin lifecycle rather than artifact admission
layer. Ensures that admission gate is not a one-time check but a
continuous invariant enforced at every point of use.

**Audit tampering**: Most serious adversarial scenario because it
undermines entire audit system. If attacker can modify evidence records,
operator has no way to distinguish between legitimate events and
fabricated ones. Defense is evidence immutability, which is primary
invariant of audit system.

Each adversarial isolation exercise produces evidence record of same
type that would be produced by real attack of corresponding kind. This
ensures that security alert path is tested in same conditions as real
attack and that operator receives same notification for both test and
real events. It also ensures that detection and containment mechanisms
work correctly for both test and real scenarios.

### Design decisions

1. **Tenant residue is most dangerous**: The spec explicitly states
   that tenant residue is most dangerous isolation failure because it
   enables cross-tenant data exfiltration without triggering
   `tenant.isolation.violation` diagnostic. The residue detection
   mechanism is defense-in-depth control.

2. **Cancellation races are impossible by construction if atomic state journal is correctly implemented**: The spec states that if
   atomic state journal is correctly implemented, cancellation races
   are impossible by construction. This shifts the defense to the
   atomicity layer rather than the cancellation layer.

3. **Audit tampering is most serious**: The spec explicitly states
   that audit tampering is most serious adversarial scenario because
   it undermines entire audit system. Evidence immutability is primary
   invariant of audit system.

4. **Each exercise produces same evidence record as real attack**:
   This ensures that security alert path is tested in same conditions
   as real attack and that detection and containment mechanisms work
   correctly for both test and real scenarios.

## Subtask 5.2.1.3: Publish threat-to-control matrix, adversarial results, accepted residual risks, and required operator responses

### Implementation

Defined threat-to-control matrix as structured publication that maps each
threat identified in phase to control that mitigates it, adversarial test
result, any accepted residual risk, and required operator response.

Threat-to-control matrix is normative evidence for Milestone 5 acceptance;
MUST be published as part of phase completion evidence bundle.

Matrix contains one row for each threat-control pair. Each row contains:

| Field | Required | Content |
|-------|----------|---------|
| `threat_id` | Yes | Stable identifier for threat (e.g., `T-5-01`) |
| `threat_description` | Yes | Human-readable description of threat |
| `control_id` | Yes | Stable identifier for control that mitigates threat (e.g., `C-5-01`) |
| `control_description` | Yes | Human-readable description of control |
| `control_type` | Yes | Control type: `preventive`, `detective`, `corrective`, or `deterrent` |
| `adversarial_test_result` | Yes | Result of corresponding security or adversarial isolation exercise: `passed`, `failed`, or `deferred` |
| `residual_risk` | Yes | Residual risk after control applied: `accepted`, `mitigated`, or `unmitigated` |
| `residual_risk_rationale` | Conditional | If `residual_risk` is `accepted` or `unmitigated`, human-readable rationale |
| `operator_response` | Yes | Required operator action if control triggered: `monitor`, `investigate`, `contain`, `remediate`, or `escalate` |

Matrix MUST include rows for every threat identified in security exercises
and adversarial isolation exercises, plus every threat identified in
[Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
No threat identified in threat model or in phase's exercises MAY be omitted
from matrix.

Milestone acceptance rules:
- Threat with `residual_risk: unmitigated` blocks milestone acceptance
- Threat with `residual_risk: accepted` requires documented rationale and
  operator approval before milestone acceptance
- Threat with `residual_risk: mitigated` does not block milestone acceptance,
  provided corresponding control passed its adversarial test

### Design decisions

1. **Threat-to-control matrix is normative evidence for milestone acceptance**:
   The matrix is the primary artifact that demonstrates that phase has
   completed its security review. It provides milestone acceptance reviewers
   with single document that maps every threat to its mitigation, test
   result, and required operator response.

2. **`unmitigated` residual risk blocks acceptance**: This ensures that
   no threat with unmitigated residual risk can be accepted without
   additional work. This is a safety-first approach.

3. **`accepted` residual risk requires documented rationale and operator
   approval**: This ensures that accepted risks are explicitly documented
   and approved by operator, preventing accidental acceptance of
   unacceptable risks.

4. **Matrix is distinct from bounded diagnostics**: Bounded diagnostics
   are per-failure instances; threat-to-control matrix is strategic
   overview of all threats and their mitigations. Matrix references
   bounded diagnostics by `evidence_hash` where applicable.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 34.1: [Provenance Signing Audit Security And Milestone Acceptance Contract And Data Model](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.3: [Provenance Signing Audit Security And Milestone Acceptance Failure Evidence And Operational Notes](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Section 34.4: [Provenance Signing Audit Security And Milestone Acceptance Phase 5 Integration Tests](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Effect handlers: [Effect Handlers Attempts Idempotency And Result Signals](../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)
- Agent registry: [Agent Registry Activation Cancellation And Completion](../60-specification/22-agent-registry-activation-cancellation-and-completion.md)
- Crash injection: [Crash Injection Durable Effects And Milestone Acceptance](../60-specification/29-crash-injection-durable-effects-and-milestone-acceptance.md)

## Open questions

1. Should the threat-to-control matrix be machine-readable? The spec
   says matrix MUST be machine-readable (YAML, JSON, or equivalent)
   but does not specify a schema for machine parsing.

2. How should accepted residual risks be reviewed over time? The spec
   requires documented rationale for accepted risks but does not address
   whether accepted risks should be periodically re-reviewed or can
   remain accepted indefinitely.

3. Can the threat-to-control matrix be updated after milestone acceptance?
   The spec says matrix is normative evidence for milestone acceptance
   but does not address whether matrix can be updated after acceptance
   (e.g., if new threats are discovered).
