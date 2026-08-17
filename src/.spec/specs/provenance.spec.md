# Provenance, Signing, Audit, and Security Acceptance

```spec-meta
id: agent_wasm.provenance
kind: policy
status: active
summary: Artifact admission, signatures, dependency provenance, immutable evidence, redaction, and security acceptance.
surface:
  - "lib/agent_wasm/provenance/**/*.ex"
  - "test/agent_wasm/provenance/**/*_test.exs"
decisions:
  - agent_wasm.decision.evidence_gated_conformance
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Provenance, Signing, Audit, Security, and Milestone Acceptance](../../../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

## Requirements

```spec-requirements
- id: agent_wasm.provenance.admission
  statement: Artifact admission shall verify digest, signature, publisher, build provenance, dependencies, toolchain compatibility, and revocation before availability.
  priority: must
  stability: stable
- id: agent_wasm.provenance.evidence
  statement: Security and authority events shall produce immutable tamper-evident host-owned evidence before dependent actions proceed.
  priority: must
  stability: stable
- id: agent_wasm.provenance.acceptance
  statement: Threat-to-control, malicious-input, tenant-isolation, revocation, residue, and audit-tampering exercises shall gate security acceptance.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.provenance.implementation_frontier
  covers:
    - agent_wasm.provenance.admission
    - agent_wasm.provenance.evidence
    - agent_wasm.provenance.acceptance
  reason: Signing, provenance, evidence storage, redaction, and security acceptance infrastructure are not implemented.
```
