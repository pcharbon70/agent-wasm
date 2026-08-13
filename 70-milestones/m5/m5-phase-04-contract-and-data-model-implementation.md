---
title: "Phase 4 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-04
  - implementation
  - contract-and-data-model
  - synchronous-host-functions
  - wasi-restrictions
  - tenant-isolation
  - eligibility-criteria
  - import-namespace
aliases:
  - "M5-P4-4.1 Implementation"
---

# Phase 4 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 4.1 (Contract And Data Model) from
[Phase 4 - Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
which establishes the contract and data model for synchronous host functions,
the rules for namespace-builtin Extism imports, the default-to-no-WASI policy,
and the tenant-isolation guarantees that bind the synchronous surface to
logical tenancy.

## Subtask 4.1.1.1: Define eligibility criteria for synchronous host functions

### Implementation

Defined four eligibility criteria that every synchronous host function MUST
satisfy to be admitted to the synchronous surface:

| Criterion | Requirement | Enforcement |
|-----------|-------------|-------------|
| Deterministic | Given same invocation context and inputs, produces same observable output. MUST NOT depend on wall-clock time, process identity, randomness, or unbound external state. | Validated at registration time |
| Bounded | Known, finite upper bound on: wall-clock time per invocation, guest memory read/write volume, number of recursive or nested calls, native memory allocation outside guest. Bounds declared in capability record and enforced before execution. | Enforced by host before execution |
| Cancellable | Exposes cancellation point at every iteration of any loop, every recursive call, and every I/O or blocking operation. Cancellation MUST complete within bounded time (at most twice declared upper bound). | Enforced by host |
| Retry-safe | MUST be idempotent on success, OR MUST return structured outcome that allows host to distinguish partial from complete results and retry without duplicating effects. Functions writing to durable state MUST use atomic commit protocol from [26-atomic-state-journal-and-directive-outbox-commits.md](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md). | Validated at registration time |

Defined `HostFunctionCapability` structure:

```
HostFunctionCapability {
  function_id: FunctionId,
  name: string,
  description: string?,
  input_schema: SchemaId?,
  output_schema: SchemaId?,
  bounds: HostFunctionBounds,
  cancellation_point_frequency: CancellationFrequency,
  retry_semantics: RetrySemantics,
  namespace: FunctionNamespace,
  requested_grants: Capability[]?,
  tenant_isolation: TenantIsolationMode
}

HostFunctionBounds {
  max_duration_ms: u64,
  max_memory_bytes: u64,
  max_recursive_calls: u32,
  max_native_alloc_bytes: u64
}

CancellationFrequency = "every-iteration" | "every-N-calls" | "every-N-bytes"
RetrySemantics = "idempotent" | "structured-partial"
FunctionNamespace = "builtin" | "application"
TenantIsolationMode = "tenant-scoped" | "shared"
```

### Design decisions

1. **Determinism does not require avoiding I/O**: The spec clarifies that
   determinism requires the observable result to be independent of unbound
   external state. A cache lookup whose key and value are fully specified
   by the caller satisfies determinism even if underlying storage is
   distributed. This is more permissive than a strict "no I/O" requirement.

2. **Bounded resources are enforced before execution**: The host enforces
   declared bounds before the function begins execution and traps the
   guest if bounds are exceeded. This prevents resource exhaustion attacks.

3. **TenantIsolationMode defaults to "tenant-scoped"**: All capability-scoped
   host functions default to tenant-scoped isolation. The "shared" mode
   is only permitted for functions that access no tenant-specific state
   and is subject to host policy.

## Subtask 4.1.1.2: Namespace built-in Extism imports separately from application capabilities

### Implementation

Defined two distinct import namespaces for WebAssembly guest modules:

**Built-in namespace:**
- Imports provided by Extism runtime and host framework
- Not declared by guest, not subject to guest's capability policy
- Contains at minimum: `extism:ctx/input`, `extism:ctx/output`,
  `extism:ctx/error`, `extism:host/env` functions for memory allocation
  and gas, and any other imports required by Extism runtime specification

**Application namespace:**
- Imports declared by host framework in response to capability grants
  approved through plugin manifest composition and authorization flow
- Subject to capability policy, tenant isolation model, and WASI policy

Rules:
- Guest MUST NOT declare imports that host cannot resolve to exactly one
  entry in either namespace. Unresolved imports cause `import.unresolved`
  diagnostic.
- Host MUST reject modules whose imports collide between the two namespaces.
  Collision causes `import.namespace-collision` diagnostic.
- Application namespace MUST be subset of capabilities declared in agent's
  manifest and approved by capability policy.

### Design decisions

1. **Namespace separation prevents privilege escalation**: A guest module
   cannot shadow a built-in import with an application import, which would
   be a privilege-escalation vector. This prevents malicious or buggy
   plugins from re-binding built-in imports.

2. **Application namespace is exactly the policy-approved surface**: The
   synchronous import surface visible to a guest is the intersection of
   (a) function eligibility, (b) manifest declaration, and (c) policy
   approval. Any gap is a specification gap, not an implementation-defined
   choice.

3. **Namespace collision is a hard error**: If the same module-level name
   and function signature appear in both namespaces, the host rejects the
   module. This prevents ambiguity and potential security issues.

## Subtask 4.1.1.3: Default to no WASI; grant selected interfaces only through explicit guest profile and host policy

### Implementation

Defined default-to-no-WASI policy. Host MUST NOT enable any WASI interface
by default. A guest module MUST operate without WASI unless host grants at
least one WASI interface explicitly through two independent controls:

1. **Guest profile**: Per-module declaration in framework plugin manifest
   or agent manifest listing specific WASI interfaces requested. Declarative
   metadata subject to manifest validation and composition flow.

2. **Host policy**: Host-side policy decision evaluated against trust model
   and capability attenuation rules. Approves or denies each requested WASI
   interface.

Both controls MUST agree for any individual WASI interface to be enabled.
A guest profile requesting an interface host policy denies causes
`wasi.policy-denied` diagnostic. A host policy that would approve an
interface for which guest profile makes no request is inert.

Closed list of permissible WASI interfaces:

| Interface | Description |
|-----------|-------------|
| `wasi:cli/environment` | Read process environment variables |
| `wasi:cli/stdin` | Read standard input |
| `wasi:cli/stdout` | Write standard output |
| `wasi:cli/stderr` | Write standard error |
| `wasi:filesystem/preopened-dir` | Access a pre-opened file system directory |
| `wasi:random/random` | Access a cryptographically secure random source |
| `wasi:time/clock` | Read monotonic and wall-clock time |

Guest profile requesting interface not in closed list causes `wasi.interface-unknown`
diagnostic.

### Design decisions

1. **Two independent controls prevent implicit grants**: Both guest profile
   and host policy must agree for WASI to be enabled. This prevents
   accidental WASI enablement through misconfiguration.

2. **Closed list limits attack surface**: Only seven WASI interfaces may
   be requested. This is intentionally small. `wasi:cli/stdout` and
   `wasi:cli/stderr` are recommended for general guest use.
   `wasi:filesystem/preopened-dir` requires operator-level approval.

3. **WASI evaluation occurs at composition gate**: WASI interfaces are
   evaluated at the same gate that prevents artifact loading without
   completed composition and authorization. This ensures WASI is never
   enabled retroactively.

4. **Grants are recorded in capability record**: Every approved WASI
   interface grant is recorded in module's capability record. Unrecorded
   interfaces are refused for any instance, including pooled and
   agent-pinned instances. This prevents instances from silently
   re-enabling interfaces revoked between instances.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 32.1: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Section 33.1: [Synchronous Host Functions WASI Restrictions And Tenant Isolation Contract And Data Model](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Extism invocation: [Extism Invocation Boundary Instances And Output Validation](../../60-specification/20-extism-invocation-boundary-instances-and-output-validation.md)
- Atomic state journal: [Atomic State Journal And Directive-Outbox Commits](../../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Single-agent host flow: [Single-Agent Host Flow And Milestone Acceptance](../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Open questions

1. Should the closed WASI interface list be extensible? The current
   design uses a closed list, but later milestones may require additional
   interfaces. What is the extension procedure?

2. How should `CancellationFrequency` be enforced for recursive functions?
   The spec defines "every-iteration" and "every-N-calls" but does not
   address how to count iterations for recursive functions.

3. Can `TenantIsolationMode: "shared"` host functions be used across
   multiple tenants simultaneously? The spec says "shared" is for
   functions that access no tenant-specific state but does not address
   whether multiple tenants can invoke the same function concurrently.
