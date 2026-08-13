---
title: "Phase 1 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-01
  - implementation
  - contract-and-data-model
  - threat-model
  - principals
  - trust-classes
  - grants
aliases:
  - "M5-P1-1.1 Implementation"
---

# Phase 1 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 1.1 (Contract And Data Model) from
[Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
which establishes the threat model, principal forms, protected assets, trust classes,
and grant vocabulary used by every authorization decision.

## Subtask 1.1.1.1: Identify threat actors and protected assets

### Implementation

Defined eight threat actors and nine protected assets. Each actor has corresponding
countermeasures documented in section 1.2.

**Threat actors:**

| Actor | Description | Countermeasure |
|-------|-------------|----------------|
| Malicious guest | Agent artifact contains intentionally harmful code | Sandboxed execution with no external access |
| Compromised artifact | Agent artifact modified after signing | Digest verification and signature checks |
| Hostile input/output | External signals or results contain malicious data | Input validation at boundary |
| Confused deputy | Agent tricked into performing unauthorized action | Grant scoping by purpose and resource |
| Tenant attacker | Tenant attempts to access another tenant's data | Memory, state, capability, and resource separation |
| Dependency compromise | Plugin or external dependency is compromised | Dependency resolution and revocation checks |
| Operator error | Operator misconfigures the system | Bounded diagnostics and policy validation |
| Co-tenant attacker | Tenant accesses shared resources | Per-tenant state namespaces and capability grants |

**Protected assets:**

| Asset | Description | Access control |
|-------|-------------|----------------|
| Host memory | Host process memory space | Guest memory isolation via Extism |
| State | Agent state, journal, snapshots, outbox entries | Tenant-scoped storage (see [25-revisioned-snapshots-journals-history-and-storage-contracts.md](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| Secrets | API keys, tokens, and credentials | Not exposed to untrusted guests |
| Policy | Authorization policies, trust classes, and grants | Operator trust class only |
| Artifacts | Agent and plugin WASM modules | Digest-verified admission |
| Audit evidence | Logs and records of authorization decisions | Immutable with integrity checks |
| External systems | Downstream services contacted by agent | Origin restrictions via attenuation |
| Availability | Host process and its resources | Resource budgets and deadline enforcement |
| Model context | LLM context window and contents | Tenant-scoped and bounded |

### Design decisions

1. **Principal forms are exhaustive for the trust model**: Seven principal kinds
   cover all actors in the threat model. The `tenant_id` field is optional to
   support system-level principals (operator, effect worker) that are not
   tenant-scoped.

2. **Protected assets are scoped to the M5 boundary**: Assets from earlier
   milestones (state, artifacts, audit evidence) are re-listed here to establish
   ownership. Each references the corresponding milestone chapter for its
   detailed storage or invocation contract.

3. **Countermeasures are deferred to section 1.2**: The threat model section
   defines actors and assets; the behavior section defines the trust classes
   and grants that implement the countermeasures. This keeps the data model
   section focused on identity and scope.

## Subtask 1.1.1.2: Define principal forms

### Implementation

Defined the `Principal` data structure and its constituent types:

```
Principal {
  kind: PrincipalKind,
  id: PrincipalId,
  tenant_id: TenantId?,
  metadata: JsonObject
}

PrincipalKind = User | Service | Agent | PluginPublisher | Operator | EffectWorker | ExternalResultSource
```

The `metadata` field is implementation-defined and MUST NOT be used for
authorization decisions. The `TenantId` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md).

### Design decisions

1. **Metadata is decoupled from authorization**: The metadata field exists to
   allow implementation-defined enrichment (labels, tags, etc.) without
   coupling those fields to the normative authorization model. This prevents
   accidental policy drift when implementations add their own metadata.

2. **Seven principal kinds match the threat model**: Each threat actor maps to
   exactly one principal kind, making it straightforward to assign trust
   classes based on principal identity.

3. **Tenant-scoped vs. system-level distinction**: The optional `tenant_id`
   field cleanly separates tenant-scoped principals (user, service, agent,
   plugin publisher) from system-level principals (operator, effect worker,
   external result source) that operate across tenants.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary Contract And Data Model](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Grant vocabulary: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- Framework plugin manifests: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions and tenant isolation: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)

## Open questions

1. Should principal kinds be extensible? The current list of seven is exhaustive
   for the M5 threat model, but later milestones (e.g., multi-agent collaboration
   in Milestone 6) may require new principal kinds such as `collaborator` or
   `proxy`.

2. How should `tenant_id` be validated at the host boundary? The spec references
   [Revisioned Snapshots Journals History And Storage Contracts](../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   but does not specify whether tenant validation is a load-time or runtime check.

3. Can `metadata` be used for observability without affecting authorization?
   The spec forbids using metadata for authorization but does not address
   whether metadata can be indexed for search or filtering in the audit log.
