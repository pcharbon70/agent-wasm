---
title: "Phase 4 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-04
  - implementation
  - failure-evidence-and-operational-notes
  - host-function-diagnostics
  - wasi-diagnostics
  - isolation-violations
  - bounded-diagnostics
aliases:
  - "M5-P4-4.3 Implementation"
---

# Phase 4 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 4.3 (Failure Evidence And Operational Notes) from
[Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
which consolidates failure outcomes, bounded diagnostics, evidence
requirements, implementation-defined choices, deferred work, and potential
invalidation results for synchronous host functions, WASI restrictions,
and tenant isolation.

## Subtask 4.3.1.1: Define failure outcomes (consolidated)

### Implementation

Defined six primary failure outcomes for synchronous host functions:

| Outcome | Description | Error Code Pattern |
|---------|-------------|-------------------|
| Malformed | Host function record, guest module, or invocation context does not conform to schema | `host-function.malformed` |
| Incompatible | Function or WASI interface technically loadable but cannot operate within bounds, isolation, or determinism constraints | `host-function.incompatible` |
| Conflicting | Two or more host functions, WASI interfaces, or capability grants conflict such that they cannot all be satisfied without violating isolation | `host-function.conflicting` |
| Unauthorized | Invocation, host function, or WASI interface lacks capability grant, trust class, or operator approval | `host-function.unauthorized` |
| Exhausted | Resource bound exceeded (wall-clock time, memory, recursive calls, native allocation, output bytes, cancellation timeout) | `host-function.exhausted` |
| Unavailable | Dependency required by host function or WASI interface is unreachable, unresponsive, or unable to complete | `host-function.unavailable` |

Additional failure outcomes from Contract And Data Model:
- `host-function.ineligible`: Function fails eligibility criteria
- `import.unresolved`: Guest module declares unresolvable import
- `import.namespace-collision`: Imports collide between namespaces
- `wasi.policy-denied`: Guest profile requests interface host policy denies
- `wasi.interface-unknown`: Guest profile requests interface not in closed list
- `tenant.validation-failed`: Invocation context missing or invalid tenant
- `isolation.violation`: Cross-tenant access attempt detected
- `bound.exceeded`: Function exceeds declared resource bound
- `cancellation.timeout`: Function does not respond to cancellation within bounded time

Additional failure outcomes from Behavior And Integration:
- `invocation.context-missing`: Required field in invocation context missing
- `invocation.deadline-exceeded`: Invocation exceeds `deadline_ms`
- `invocation.output-limit`: Invocation exceeds `output_limit_bytes`
- `invocation.grant-missing`: Invocation lacks capability grant
- `instance.mode-isolation-violation`: Instance mode relaxes isolation invariant
- `instance.reset-leakage-detected`: State leaks into `reset` instance
- `residue.violation`: Observable residue persists after invocation

Error code naming conventions:
- `host-function.<subtype>` for function-level failures
- `wasi.<subtype>` for WASI-level failures
- `invocation.<subtype>` for context and enforcement failures
- `instance.<subtype>` for mode-related failures
- `residue.<subtype>` for residue verification failures
- `phase4.<failure-outcome>.<subtype>` for consolidated section (takes precedence)

### Design decisions

1. **Six primary outcomes are exhaustive**: The six primary failure
   outcomes (malformed, incompatible, conflicting, unauthorized,
   exhausted, unavailable) cover all failure modes. Additional outcomes
   are subtypes or specific cases.

2. **Error codes are namespaced by domain**: The `host-function.*`,
   `wasi.*`, `invocation.*`, `instance.*`, and `residue.*` prefixes
   distinguish different failure domains. This enables operators to
   filter diagnostics by domain.

3. **`phase4.<subtype>` takes precedence**: When both conventions apply
   to the same failure, the `phase4.<subtype>` convention takes precedence
   for diagnostic stability across phases.

## Subtask 4.3.1.2: Define bounded diagnostics and evidence

### Implementation

Defined bounded diagnostics for synchronous host function failures. Each
diagnostic MUST contain exactly:

| Field | Required | Content |
|-------|----------|---------|
| `error_code` | Yes | Stable diagnostic identifier following naming convention |
| `phase` | Yes | Phase name: `phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation` |
| `contract` | Yes | Subsection of chapter where failure boundary was crossed |
| `profile` | Yes | Instance mode, tenant scope, or capability scope in effect |
| `failed_boundary` | Yes | Human-readable description of violated invariant or bound |
| `invocation_id` | Conditional | Present if failure during invocation; omitted for load-time or registration-time failures |
| `tenant_id` | Conditional | Present if failure is tenant-scoped; omitted if system-scoped |
| `evidence_hash` | Yes | Cryptographic hash of minimal evidence record |

Prohibited content in diagnostics:
- Raw guest module bytecode or data section contents
- Tenant-specific state values or identifiers beyond `tenant_id`
- Capability grant values beyond their presence or absence
- Native memory addresses, stack traces, or process-internal pointers
- Secrets, keys, or credentials in any form
- Wall-clock timestamps beyond coarse-grained duration window

`evidence_hash` computed from minimal evidence record including:
- Type and count of offending input or state element
- Declared bound or invariant violated
- Instance mode and tenant scope in effect
- Counter of how many times same boundary crossed within current agent activation

### Design decisions

1. **Diagnostics are structured and machine-parseable**: The eight required
   fields provide a consistent structure for automated parsing and
   filtering. The `evidence_hash` enables forensic correlation without
   retaining raw state.

2. **Prohibited content is explicit**: The spec lists exactly what is
   prohibited (bytecode, memory addresses, secrets, etc.). This prevents
   accidental information leakage.

3. **Evidence hash enables forensic analysis**: The hash is computed from
   a minimal evidence record that includes the type and count of offending
   elements, the violated bound, and the context. This enables correlation
   between diagnostics and underlying state without retaining raw state.

4. **Conditional fields reduce noise**: `invocation_id` and `tenant_id`
   are only present when relevant. This reduces diagnostic noise for
   system-scoped or load-time failures.

## Subtask 4.3.1.3: Document implementation-defined choices and deferred work

### Implementation

**Implementation-defined choices** (must be documented in conformance profile):
1. Error code catalog for `phase4.<failure-outcome>.<subtype>` naming convention
2. Evidence record format for computing `evidence_hash`
3. Evidence hashing algorithm (digest size, collision resistance)
4. Diagnostic serialization format (JSON, MessagePack, CBOR, etc.)
5. Tenant identifier revocation procedure (invalidation, propagation delay, audit log format)
6. Diagnostic retention and query (retention policy, query interface, maximum retention period)

Additional implementation-defined choices from other sections:
- Import name resolution algorithm
- Memory isolation mechanism between tenants
- State isolation mechanism between tenants
- Residue detection algorithm for `reset` recycling
- Pool size, eviction policy, health-check frequency for `pooled` instances
- Snapshot and diff mechanism for residue verification

**Deferred work**:
1. Cross-tenant host functions: Host functions accessing state across multiple tenants
2. Dynamic WASI interface addition: Runtime addition of new WASI interfaces to closed list
3. Tenant migration: Live migration of tenant's state and memory between host processes
4. Resource budget borrowing: Temporary borrowing of resource budget between tenants
5. Host function hot-swap: Live replacement of host function without restarting guest instances
6. Adaptive cancellation frequency: Runtime adjustment of `CancellationFrequency` based on observed patterns
7. Multi-region tenant identity: Support for tenant identifiers resolved across multiple identity providers

Each deferred item has a defined triggering condition: observable operator
demand, security audit recommendation, or performance benchmark result.

**Results invalidating earlier milestones**:
1. Determinism violations: Observed host functions violate determinism despite declared bounds
2. WASI performance: WASI-enabled guests exceed turn timeout under policy constraints
3. Tenant isolation overhead: Isolation mechanisms exceed resource budgets
4. Import namespace scalability: Resolution algorithm does not scale to expected host function count
5. Instance mode safety: Any instance mode other than `fresh` fails to meet isolation oracle
6. Residue detection false negative: Residue verification mechanism fails to detect known residue injection

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
   trigger is a measurable condition (latency, capacity, safety) that
   can be monitored during integration testing.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Contract And Data Model](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.2: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Behavior And Integration](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.4: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Phase 4 Integration Tests](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should bounded diagnostics include a severity level? The current
   design only includes error code and failed boundary. A severity
   level (info, warning, error, critical) would help operators prioritize
   responses.

2. How should `evidence_hash` be verified? The spec defines the hash
   but does not address how verifyers can recompute it to detect
   tampering.

3. Can deferred work items be implemented as extensions without
   specification changes? The spec lists deferred work but does not
   address whether these items can be implemented as extensions
   without becoming normative.
