---
id: agent_wasm.decision.evidence_gated_conformance
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Evidence-Gated Conformance

## Context

The specification defines extensive fixtures, fault injection, security tests,
runtime matrices, SLOs, and production acceptance evidence. Passing code tests
alone cannot establish all required claims.

## Decision

Conformance and release claims are gated by the applicable normative
integration suites, cross-milestone regression fixtures, implementation
profile, signed evidence, and unresolved-risk review. Evidence is bounded,
tenant-safe, tamper-evident, and traceable to exact source headings.

<!-- covers: agent_wasm.package.conformance_gate -->

## Consequences

SpecLed requirements remain explicitly excepted until implementation proof
exists. Removing an exception requires targeted linked or executed verification
and cannot be justified only by an implementation assertion.
