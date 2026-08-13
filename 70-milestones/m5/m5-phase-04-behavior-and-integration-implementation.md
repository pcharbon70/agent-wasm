---
title: "Phase 4 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-04
  - implementation
  - behavior-and-integration
  - invocation-context
  - instance-modes
  - test-residue
  - tenant-isolation
aliases:
  - "M5-P4-4.2 Implementation"
---

# Phase 4 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 4.2 (Behavior And Integration) from
[Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
which defines invocation context binding, instance creation modes, test
residue verification, and failure outcomes for behavior and integration.

## Subtask 4.2.1.1: Bind every host callback to invocation, tenant, principal, artifact, grants, deadline, and output limits

### Implementation

Defined invocation context fields that every synchronous host function
callback MUST be bound to:

| Field | Required | Source | Constraint |
|-------|----------|--------|------------|
| `invocation_id` | Yes | Host-generated UUID | Unique per synchronous invocation |
| `tenant_id` | Yes | Turn principal identity | Derived from tenant isolation model |
| `principal_id` | Yes | Turn principal identity | As defined in threat model chapter |
| `agent_id` | Conditional | Initiating agent | Required if turn initiated by agent |
| `artifact_id` | Conditional | Loaded module identity | Required if invocation executes inside loaded plugin artifact |
| `grants` | Yes | Approved capability list | Subset of capability policy |
| `deadline_ms` | Yes | Turn policy | Hard wall-clock limit for entire invocation |
| `output_limit_bytes` | Yes | Turn policy | Hard byte limit on observable output |

Enforcement:
- `deadline_ms`: Hard limit on total wall-clock time including all nested
  host function calls. Exceeding causes trap with `invocation.deadline-exceeded`
  and rollback of partial state.
- `output_limit_bytes`: Hard limit on total bytes written to output buffer.
  Exceeding causes trap with `invocation.output-limit`. Partial output
  produced before limit is reached is discarded unless conformance profile
  documents truncation mode.
- `grants`: Acts as explicit filter on functions and interfaces. A host
  function whose capability requirements are not fully satisfied by grants
  MUST NOT be called. Insufficient grants cause `invocation.grant-missing`
  diagnostic.
- `artifact_id`: Required when invocation executes inside loaded plugin
  artifact. Ensures residue tracking can attribute every observable effect
  to correct artifact and tenant combination.

### Design decisions

1. **Every callback is bound to structured context**: This makes tenant
   isolation observable and auditable. Without this binding, a cross-tenant
   leak is indistinguishable from a within-tenant effect in the audit log.

2. **Deadline and output limits are hard**: The host traps the guest if
   limits are exceeded. This prevents resource exhaustion attacks and
   ensures that invocations cannot consume unbounded resources.

3. **Grants filter the available surface**: The `grants` field acts as
   an explicit filter on functions and interfaces. This ensures that
   even if a function is present in the application namespace, it cannot
   be called without the required grants.

4. **artifact_id enables residue attribution**: Binding every invocation
   to the artifact that executed it enables the host to track residue
   back to the specific artifact-tenant combination that caused it.

## Subtask 4.2.1.2: Define fresh, reset, pooled, and agent-pinned instance modes with fresh-instance behavior as the oracle

### Implementation

Defined four instance creation modes:

| Mode | Memory | State | WASI bindings | Reuse |
|------|--------|-------|---------------|-------|
| `fresh` | New allocation | New, empty | Re-evaluated from capability record | Never reused |
| `reset` | New allocation | New, empty | Re-evaluated from capability record | Reused after reset |
| `pooled` | Per-instance (policy-gated sharing) | Shared, isolated | Re-evaluated from capability record | Shared across tenants per pool |
| `agent-pinned` | New allocation | New per agent | Re-evaluated from capability record | Pinned to one agent |

`fresh` is the reference oracle. Every other mode MUST produce behavior
that is at least as restrictive as `fresh` on every isolation invariant
(memory, state, capability, resource separation). A mode that relaxes
any isolation invariant relative to `fresh` MUST be rejected with
`instance.mode-isolation-violation` diagnostic.

**fresh mode:**
- Creates new WebAssembly instance with freshly allocated guest memory,
  freshly initialized linear memory, no persistent state between invocations
- WASI bindings re-evaluated from capability record on every creation
- MUST NOT be reused, pooled, or reset

**reset mode:**
- Creates new instance identical to `fresh` on first creation
- After first invocation completes, host MAY recycle instance by resetting
  memory to initial zeroed state and re-running `_start` export
- Before recycling, host MUST verify no tenant state leaked into instance's
  memory or exports. Leakage causes `instance.reset-leakage-detected`
  diagnostic and instance is discarded (new `fresh` instance created instead).

**pooled mode:**
- Creates pool of pre-allocated instances, each belonging to single
  tenant's isolation domain
- Instances within pool share memory regions with other instances in
  same pool only if capability policy explicitly permits cross-instance
  memory sharing for specific host function
- WASI bindings re-evaluated from capability record on every invocation
- Tenant's pooled instances never accessed by another tenant's invocation

**agent-pinned mode:**
- Creates new instance pinned to single `agent_id` for entire lifetime
  within agent's activation
- Created with `fresh` semantics on first use (fresh memory, WASI re-evaluation)
- Subsequent invocations by same agent MAY reuse pinned instance without
  memory reset, provided agent's capability policy permits stateful instances
- Invocations by any other agent MUST NOT use pinned instance
- If agent is deactivated or cancelled, pinned instance destroyed with agent

Instance mode selection priority:
1. If invocation context specifies `agent_id` and agent's manifest declares
   `agent-pinned` mode for artifact, use `agent-pinned`
2. If invocation is cross-tenant or artifact is untrusted, use `fresh`
3. If invocation is same-tenant, artifact is trusted, and host's performance
   profile justifies pooling, use `pooled`
4. Otherwise, use `reset`

### Design decisions

1. **`fresh` is the safety oracle**: Every other mode must be at least as
   restrictive as `fresh` on every isolation invariant. This ensures that
   performance optimizations (reset, pooled, agent-pinned) never compromise
   security.

2. **Reset leakage is detected and handled**: Before recycling a `reset`
   instance, the host verifies no tenant state leaked into memory or exports.
   If leakage is detected, the instance is discarded and a new `fresh`
   instance is created. This prevents cross-tenant state leaks.

3. **Pooled mode is per-tenant, not cross-tenant**: Instances within a pool
   belong to a single tenant's isolation domain. This prevents cross-tenant
   state leaks while still enabling per-tenant performance optimization.

4. **Agent-pinned enables agent-level statefulness**: This is the only mode
   that permits inter-invocation state within a single agent's activation.
   It requires explicit policy permission and is isolated from other agents
   and tenants.

5. **Isolation is never compromised for performance**: The priority ensures
   that `fresh` is the safe default. Other modes are optimizations that
   require explicit policy or manifest approval.

## Subtask 4.2.1.3: Test residue across tenant, agent, artifact, success, trap, timeout, cancellation, memory pressure, and Extism-variable use

### Implementation

Defined test residue as any observable state, side effect, resource consumption,
or audit log entry that persists after a synchronous host function invocation
completes, regardless of outcome (success, trap, timeout, cancellation).

Nine residue categories tested for every invocation:

| Category | Scope | Expected on success | Expected on trap | Expected on timeout | Expected on cancellation |
|----------|-------|---------------------|------------------|--------------------|------------------------|
| `tenant` | Tenant state | Unchanged unless explicitly modified | Unchanged | Unchanged | Unchanged unless cancellation commits partial state |
| `agent` | Agent state | Updated per directive-outbox | Rolled back per atomic commit | Rolled back | Rolled back |
| `artifact` | Artifact memory and exports | Initialized per `_start` or empty | Reset to initial state | Reset to initial state | Reset to initial state |
| `success` | Output buffer | Exactly declared output, within limits | Empty or truncated | Empty or truncated | Empty or truncated |
| `trap` | Guest memory | Zeroed or safe state | Zeroed or safe state | Zeroed or safe state | Zeroed or safe state |
| `timeout` | All scopes | N/A (did not complete) | N/A | Host rolls back all effects, emits `invocation.deadline-exceeded` | N/A |
| `cancellation` | All scopes | N/A (did not complete) | N/A | N/A | Host rolls back all effects, emits `invocation.cancelled` |
| `memory-pressure` | Host memory | Within `max_native_alloc_bytes` | Within declared bounds | Within declared bounds | Within declared bounds |
| `extism-variable` | Extism internal state | Reset to pre-invocation state | Reset to pre-invocation state | Reset to pre-invocation state | Reset to pre-invocation state |

`memory-pressure` residue measured as difference between host's total native
memory consumption before and after invocation, excluding guest's linear memory.
MUST NOT exceed `max_native_alloc_bytes`.

`extism-variable` residue refers to state of Extism's internal input, output,
and error buffers after invocation. MUST be reset to pre-invocation state
after every invocation. Failure to reset constitutes cross-invocation leakage
vulnerability and is treated as isolation violation.

Matrix produces 36 distinct test scenarios per host function (9 categories x 4
failure outcomes).

Observable mechanism for residue verification:
1. Pre-invocation snapshot of every residue category
2. Post-invocation snapshot of every residue category
3. Diff report identifying any deviation from expected behavior
4. Audit log entry recording diff report with `invocation_id`

### Design decisions

1. **36 test scenarios per host function**: The matrix of 9 categories x 4
   failure outcomes produces comprehensive coverage. This is the primary
   evidence that the synchronous surface does not leak state between
   invocations, agents, or tenants.

2. **Extism variables must be reset**: The spec explicitly states that
   failure to reset Extism's internal buffers constitutes a
   cross-invocation leakage vulnerability. This is a critical security
   property.

3. **Snapshot and diff mechanism is lightweight**: The spec does not require
   full memory dumps. Implementations MAY use checksums, region watches,
   or capability tracking to detect residue without prohibitive overhead.

4. **Timeout and cancellation always roll back**: The expected behavior
   for timeout and cancellation is that the host rolls back all effects.
   This ensures that partial state never persists.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Contract And Data Model](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.3: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Failure Evidence And Operational Notes](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Section 33.4: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Phase 4 Integration Tests](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should residue detection be performed at every invocation or only
   during integration tests? The spec defines residue verification as
   a test requirement but does not address whether production systems
   should perform residue detection continuously.

2. How should `pooled` mode handle pool exhaustion? The spec defines
   pool creation but does not address what happens when all pooled
   instances are in use and a new invocation arrives.

3. Can `agent-pinned` mode be used across host restarts? The spec says
   pinned instances are destroyed when agent is deactivated or cancelled,
   but does not address whether pinned instances persist across host
   restarts.
