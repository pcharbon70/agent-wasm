---
id: agent_wasm.decision.portable_guest_protocol
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Portable Guest Protocol

## Context

Agent artifacts must remain portable across supported host languages and Wasm
runtimes while preserving exact protocol meaning.

## Decision

The guest boundary uses immutable content-addressed core-Wasm artifacts,
reviewable manifests, canonical value encoding, stable identities, and explicit
describe, initialize, reduce, and migrate lifecycle contracts. Guest SDKs lower
language types to that shared protocol rather than defining new semantics.

## Consequences

Wire schemas, canonicalization, version negotiation, fixtures, and diagnostics
must be implemented before language-specific convenience APIs. Runtime-private
handles and host-language values cannot cross the portable boundary.
