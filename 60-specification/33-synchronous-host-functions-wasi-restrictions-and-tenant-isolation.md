---
title: "Synchronous Host Functions WASI Restrictions And Tenant Isolation"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-05
  - phase-04
  - synchronous-host-functions
  - wasi-restrictions
  - tenant-isolation
aliases:
  - "M5-P4 Synchronous Host Functions WASI Restrictions And Tenant Isolation"
---

# Synchronous Host Functions WASI Restrictions And Tenant Isolation

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
--
Capabilities, Plugins, Security, And Tenancy.
It establishes the contract and data model for synchronous host functions,
the rules for namespace-builtin Extism imports, the default-to-no-WASI policy,
and the tenant-isolation guarantees that bind the synchronous surface to
logical tenancy.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

## 4.1 Contract And Data Model

### Eligibility criteria for synchronous host functions

> **Normative definition.**
A synchronous host function is any native function exposed to a WebAssembly
guest through the Extism runtime that the agent or framework invokes
synchronously within a single turn.

> **Normative definition.**
A synchronous host function MUST satisfy every one of the following
eligibility criteria to be admitted to the synchronous surface.
Failure to satisfy any single criterion disqualifies the function from
the synchronous surface and requires the host to route invocation through
an asynchronous channel with its own contract.

1. **Deterministic**: Given the same invocation context and inputs,
   the function produces the same observable output.
   The function MUST NOT depend on wall-clock time, process identity,
   randomness, or any other unbound external state for its core logic.
   Side-channel timing is not a determinism violation provided the
   observable result is identical.
2. **Bounded**: The function has a known, finite upper bound on each of
   the following resources:
   - wall-clock time per invocation;
   - guest memory read/write volume;
   - number of recursive or nested calls it may initiate;
   - native memory allocation outside the guest.
   The bounds MUST be declared in the function's capability record and
   enforced by the host before the function begins execution.
3. **Cancellable**: The function MUST expose a cancellation point at every
   iteration of any loop, every recursive call, and every I/O or
   blocking operation it performs.
   Cancellation MUST complete within a bounded time that is at most
   twice the declared upper bound for the function.
4. **Retry-safe**: The function MUST be idempotent on success, or
   MUST return a structured outcome that allows the host to distinguish
   partial from complete results and retry without duplicating effects.
   A function that writes to durable state MUST use the atomic commit
   protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   and treat any abort as a full rollback.

> **Normative definition.**
The host MUST validate eligibility at registration time.
A function whose declared bounds exceed the host's policy limits, or
whose determinism claim conflicts with an observed dependency, MUST be
rejected with the diagnostic `host-function.ineligible`.

> **Non-normative note.**
Determinism does not require the function to avoid I/O entirely; it
requires the observable result to be independent of unbound external
state.
A cache lookup whose key and value are fully specified by the caller
satisfies determinism even if the underlying storage layer is distributed.

> **Non-normative note.**
Bounded resource consumption is the primary defense against resource
exhaustion attacks from within a guest module.
The host's capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
binds these bounds to the agent, tenant, and turn that initiated the
invocation.

> **Normative definition.**

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

FunctionId = string
HostFunctionBounds {
  max_duration_ms: u64,
  max_memory_bytes: u64,
  max_recursive_calls: u32,
  max_native_alloc_bytes: u64?
}

CancellationFrequency = "every-iteration" | "every-N-calls" | "every-N-bytes"
RetrySemantics = "idempotent" | "structured-partial"
FunctionNamespace = "builtin" | "application"
TenantIsolationMode = "tenant-scoped" | "shared"
```

Every eligible synchronous host function MUST be registered in the
host's capability registry with the record defined above.

> **Normative definition.**
The `bounds` field is authoritative.
The host MUST enforce the declared bounds before the function begins
execution and MUST trap the guest if the function exceeds any bound.
Exceeding a bound is an explicit runtime failure defined in the
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

> **Normative definition.**
The `namespace` field separates built-in Extism imports from
application-declared host functions.
This separation is required by
[Import namespace](#import-namespace).

> **Non-normative note.**
`TenantIsolationMode: "tenant-scoped"` is the default and REQUIRED
mode for all capability-scoped host functions.
`TenantIsolationMode: "shared"` is only permitted for host functions
that access no tenant-specific state and is subject to the host policy
defined in
[Default-to-no-WASI and guest profile](#default-to-no-wasi-and-guest-profile).

### Import namespace

> **Normative definition.**
The host MUST maintain two distinct import namespaces for WebAssembly
guest modules:

1. **Built-in namespace**: Imports provided by the Extism runtime and
   the host framework.
   These imports are not declared by the guest, are not subject to the
   guest's capability policy, and are not exposed through the agent's
   capability surface.
   The built-in namespace contains at minimum:
   - `extism:ctx/input`, `extism:ctx/output`, `extism:ctx/error`;
   - `extism:host/env` functions for memory allocation and gas;
   - any other imports required by the Extism runtime specification.
2. **Application namespace**: Imports declared by the host framework in
   response to capability grants approved through the manifest composition
   and authorization flow defined in
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).
   These imports are subject to the capability policy, the tenant
   isolation model, and the WASI policy defined in this chapter.

> **Normative definition.**
A WebAssembly module MUST NOT declare imports that the host cannot
resolve to exactly one entry in either the built-in or the application
namespace.
Any unresolved import MUST cause the host to reject the module at load
time with the diagnostic `import.unresolved`.

> **Normative definition.**
The host MUST reject any module whose imports collide between the two
namespaces.
A collision occurs when the same module-level name and function signature
appear in both the built-in and application namespaces.
The host MUST emit the diagnostic `import.namespace-collision` in this
case.

> **Non-normative note.**
Namespace separation prevents a guest module from shadowing a built-in
import with an application import, which would be a privilege-escalation
vector.
It also prevents a malicious or buggy plugin from accidentally or
deliberately re-binding a built-in import.

> **Normative implementation-defined choice.**
The host defines the exact algorithm used to resolve import names to
namespace entries.
The resolution algorithm MUST be deterministic and MUST be documented
in the host's conformance profile.

> **Normative definition.**
The application namespace MUST be a subset of the capabilities declared
in the agent's manifest and approved by the capability policy.
A host function that is eligible under
[Eligibility criteria](#eligibility-criteria-for-synchronous-host-functions)
but has not been approved through the capability policy MUST NOT be
exposed to the guest.

> **Non-normative note.**
This rule ensures that the synchronous import surface visible to a
guest module is exactly the intersection of (a) function eligibility,
(b) manifest declaration, and (c) policy approval.
Any gap in this intersection is a specification gap, not an
implementation-defined choice.

### Default-to-no-WASI and guest profile

> **Normative definition.**
The host MUST NOT enable any WASI interface by default.
A WebAssembly guest module MUST operate without WASI unless the host
grants at least one WASI interface explicitly through both of the
following independent controls:

1. **Guest profile**: A per-module declaration, recorded in the
   framework plugin manifest or the agent manifest, that lists the
   specific WASI interfaces the guest requests.
   The guest profile is declarative metadata and is subject to the
   manifest validation and composition flow defined in
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).
2. **Host policy**: A host-side policy decision, evaluated against the
   trust model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   and the capability attenuation rules defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
   that approves or denies each requested WASI interface.

> **Normative definition.**
Both controls MUST agree for any individual WASI interface to be
enabled.
A guest profile that requests an interface the host policy denies MUST
cause the host to emit the diagnostic `wasi.policy-denied`.
A host policy that would approve an interface for which the guest
profile makes no request is inert; no implicit grants are issued.

> **Normative definition.**
The host MUST evaluate the guest profile and host policy for WASI at
the same gate that prevents artifact loading without completed composition
and authorization, as defined in
[Composition and authorization before artifact loading](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md#composition-and-authorization-before-artifact-loading).
A WASI interface that is not approved at this gate MUST NOT be bound
to the guest instance, even if the instance is later created in a
different lifecycle stage.

> **Non-normative note.**
Default-to-no-WASI is the primary mechanism for ensuring that guest
modules cannot perform file system access, environment variable
reading, argument passing, or any other WASI-defined operation unless
the operator has explicitly opted in through both the manifest and
the host policy.
This is the minimal-privilege default for a multi-tenant agent system.

> **Normative definition.**
The set of WASI interfaces that may be requested is bounded to the
following closed list.
The host MUST reject any guest profile that requests a WASI interface
not in this list with the diagnostic `wasi.interface-unknown`.

| Interface | Description |
|-----------|-------------|
| `wasi:cli/environment` | Read process environment variables. |
| `wasi:cli/stdin` | Read standard input. |
| `wasi:cli/stdout` | Write standard output. |
| `wasi:cli/stderr` | Write standard error. |
| `wasi:filesystem/preopened-dir` | Access a pre-opened file system directory. |
| `wasi:random/random` | Access a cryptographically secure random source. |
| `wasi:time/clock` | Read monotonic and wall-clock time. |

> **Non-normative note.**
This closed list is intentionally small.
`wasi:cli/stdout` and `wasi:cli/stderr` are the only interfaces
recommended for general guest use.
`wasi:filesystem/preopened-dir` requires operator-level approval and
MUST be evaluated against the tenant-isolation model defined in
[Tenant isolation model](#tenant-isolation-model).
`wasi:time/clock` is permitted only for guests whose determinism
claim does not depend on wall-clock time, or only the monotonic clock.

> **Normative definition.**
The host MUST record every approved WASI interface grant in the
module's capability record and MUST refuse to bind an unrecorded
interface to any instance of the module, including pooled and
agent-pinned instances defined in the Behaviour And Integration section
of this chapter.

> **Non-normative note.**
Recording grants in the capability record ensures that instance-mode
transitions do not silently re-enable interfaces that were revoked
between instances.

### Tenant isolation model

> **Normative definition.**
Logical tenancy MUST be backed by memory, state, capability, and
resource separation.
The host MUST enforce the following isolation invariants for every
synchronous host function invocation:

1. **Memory isolation**: Each tenant's guest instances MUST operate
   in disjoint guest memory regions.
   The host MUST trap any cross-tenant memory access attempt.
2. **State isolation**: Each tenant's state MUST be stored in a
   namespace that is scoped to the tenant identifier.
   Cross-tenant state access is prohibited unless the host function
   is declared with `TenantIsolationMode: "shared"` and the capability
   policy explicitly permits it.
3. **Capability isolation**: Each tenant's capability grants are
   evaluated independently.
   A capability granted to tenant A MUST NOT be visible to tenant B
   unless the capability is declared as cross-tenant by the host policy.
4. **Resource isolation**: Each tenant's resource budget is tracked
   independently.
   Resource exhaustion in one tenant MUST NOT affect the budgets of
   other tenants.

> **Normative definition.**
The tenant identifier is derived from the turn's principal identity
as defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).
The host MUST validate the tenant identifier on every synchronous
invocation and MUST trap if the identifier is missing or invalid.

> **Non-normative note.**
These four isolation invariants are the operational meaning of
"logical tenancy" in this specification.
They are enforced at the host boundary and cannot be bypassed by any
guest module, regardless of its trust tier.

> **Normative definition.**

```
InvocationContext {
  tenant_id: TenantId,
  agent_id: AgentId?,
  turn_id: TurnId,
  principal_id: PrincipalId,
  invocation_id: InvocationId,
  deadline_ms: u64?,
  output_limit_bytes: u64?,
  grants: Capability[]
}

TenantId = string
AgentId = string
TurnId = string
PrincipalId = string
InvocationId = string
```

Every synchronous host function invocation MUST include the context
defined above, in addition to the function's declared inputs.

> **Normative definition.**
The host MUST use `tenant_id` to route the invocation to the correct
tenant-scoped state and memory region.
The host MUST enforce `deadline_ms` and `output_limit_bytes` as hard
limits on the invocation.
The host MUST enforce `grants` as a filter on the functions and
interfaces available to the invocation.

> **Non-normative note.**
The `agent_id` field is optional because not all invocations are
initiated by an agent.
Direct operator invocations and timer-initiated invocations MAY omit
the agent identifier.

> **Normative implementation-defined choice.**
The host defines the exact mechanism used to enforce memory isolation
between tenants (separate WebAssembly heaps, memory segments, or
address-space separation).
The mechanism MUST guarantee that cross-tenant access is impossible
without an explicit trap.

> **Normative implementation-defined choice.**
The host defines the exact mechanism used to enforce state isolation
between tenants (separate databases, table prefixes, in-memory maps,
or cryptographic separation).
The mechanism MUST guarantee that cross-tenant state access requires
an explicit policy approval.

### Failure outcomes for contract and data model

> **Non-normative note.**
The canonical failure outcomes for this section are defined below.
Detailed failure semantics, error codes, and diagnostic format
requirements are defined in the Phase 4
[Failure Evidence And Operational Notes](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-04-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md#43-section---failure-evidence-and-operational-notes)
section.

1. **Malformed**: The host function record does not conform to the
   schema defined in
   [Eligibility criteria](#eligibility-criteria-for-synchronous-host-functions).
2. **Ineligible**: The function fails to satisfy one or more of the
   four eligibility criteria.
3. **Unresolved import**: The guest module declares an import that the
   host cannot resolve to either namespace.
4. **Namespace collision**: The guest module's imports collide between
   the built-in and application namespaces.
5. **Policy denied**: The guest profile requests a WASI interface that
   the host policy denies.
6. **Interface unknown**: The guest profile requests a WASI interface
   not in the closed list.
7. **Tenant validation failed**: The invocation context is missing or
   contains an invalid tenant identifier.
8. **Isolation violation**: A cross-tenant memory, state, capability,
   or resource access attempt is detected.
9. **Bound exceeded**: The function exceeds a declared resource bound.
10. **Cancellation timeout**: The function does not respond to
    cancellation within the bounded time.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and bounded
diagnostic that identifies the phase contract, profile, and failed
boundary without exposing secrets.
The error codes for this section follow the naming convention
`host-function.<subtype>` for function-level failures and
`wasi.<subtype>` for WASI-level failures.

## Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented
in the conformance profile:

1. **Import resolution algorithm**: The exact algorithm used to resolve
   import names to namespace entries, as defined in
   [Import namespace](#import-namespace).
2. **Memory isolation mechanism**: The mechanism used to enforce
   memory isolation between tenants, as defined in
   [Tenant isolation model](#tenant-isolation-model).
3. **State isolation mechanism**: The mechanism used to enforce state
   isolation between tenants, as defined in
   [Tenant isolation model](#tenant-isolation-model).
4. **Cancellation enforcement**: The exact mechanism used to enforce
   cancellation points, including the overhead model and the
   implementation of `CancellationFrequency`.
5. **Deadline enforcement granularity**: The host's internal timer
   resolution and the overhead model for `deadline_ms` enforcement.
6. **Output limit enforcement**: The exact mechanism used to enforce
   `output_limit_bytes` on guest output, including how partial output
   is handled when the limit is exceeded mid-write.
7. **Tenant identifier validation**: The exact algorithm used to
   validate tenant identifiers, including the format, source, and
   revocation procedure.
8. **WASI interface binding granularity**: Whether WASI interfaces
   are bound at module load time, instance creation time, or
   invocation time.
   The binding MUST be re-evaluated on every instance creation.

## Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Cross-tenant host functions**: Host functions that intentionally
   access state across multiple tenants, subject to strict policy
   controls.
2. **Dynamic WASI interface addition**: Runtime addition of new WASI
   interfaces to the closed list, subject to a formal extension
   procedure.
3. **Tenant migration**: Live migration of a tenant's state and memory
   between host processes without interruption.
4. **Resource budget borrowing**: Temporary borrowing of resource
   budget from one tenant to another, subject to strict limits and
   audit.
5. **Host function hot-swap**: Live replacement of a host function
   without restarting guest instances.

## Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 4 MAY invalidate earlier milestone
assumptions:

1. **Determinism violations**: If observed host functions violate
   determinism despite declared bounds, the determinism model in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   MUST be revised.
2. **WASI performance**: If WASI-enabled guests exceed the turn timeout
   defined in
   [Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
   the timeout or WASI enablement policy MUST be revised.
3. **Tenant isolation overhead**: If the isolation mechanisms defined
   in this section exceed the resource budgets defined in
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
   the budget or isolation model MUST be revised.
4. **Import namespace scalability**: If the import namespace resolution
   algorithm does not scale to the expected number of host functions,
   the algorithm MUST be revised.

> **Non-normative note.**
If any result from Phase 4 invalidates an earlier milestone assumption,
the affected milestone MUST be revised and re-validated.
The revision process is governed by
[Specification Authority](../SPECIFICATION-AUTHORITY.md) and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Import resolution algorithm | Implementation-defined | Document in conformance profile | Must be deterministic and prevent shadowing |
| Memory isolation mechanism | Implementation-defined | Document in conformance profile | Must guarantee cross-tenant trap on access |
| State isolation mechanism | Implementation-defined | Document in conformance profile | Must require explicit policy approval for cross-tenant access |
| Cancellation enforcement | Implementation-defined | Document in conformance profile | Must complete cancellation within 2x declared bound |
| Deadline enforcement granularity | Implementation-defined | Document in conformance profile | Must enforce deadline as hard limit |
| Output limit enforcement | Implementation-defined | Document in conformance profile | Must trap or truncate at limit without publishing partial output |
| Tenant identifier validation | Implementation-defined | Document in conformance profile | Must validate on every invocation |
| WASI interface binding granularity | Implementation-defined | Document in conformance profile | Must re-evaluate on every instance creation |
| Guest profile evaluation gate | Must evaluate at composition/authorization gate | None | Cannot enable WASI after gate closes |
| Host function bound enforcement | Must trap on bound exceedance | None | Bound exceedance is explicit runtime failure |

## Operational variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Diagnostic formatting | Implementation-defined | Document in conformance profile | Must produce parseable output |
| Audit log retention | Implementation-defined | Document in conformance profile | Must support forensic analysis |
| Failure detection granularity | Implementation-defined | Document in conformance profile | Must detect all ten failure outcomes in this section |
