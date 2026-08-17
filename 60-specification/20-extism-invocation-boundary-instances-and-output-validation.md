---
title: "Extism Invocation Boundary Instances And Output Validation"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-03
  - phase-01
  - extism
  - invocation
  - boundary
  - instance
aliases:
  - "M3-P1 Extism Invocation Boundary"
---

# Extism Invocation Boundary Instances And Output Validation

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/phase-01-extism-invocation-boundary-instances-and-output-validation.md)
of
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
--
Host Actor Runtime And Lifecycle.
It establishes the host-owned boundary that resolves compiled artifacts,
creates constrained Extism instances, invokes exports, and treats all guest
output as untrusted until validated.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 1
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

## 1.1 Contract And Data Model

### Host invocation input

> **Normative definition.**
The host MUST assemble a single invocation input from authenticated context,
artifact digest, manifest, state snapshot, grants, limits, deadline, and
trace context.

> **Normative definition.**

```
InvocationInput {
  auth_context: AuthContext,
  artifact_digest: ArtifactDigest,
  manifest: AgentManifest,
  state_snapshot: StateSnapshot,
  grants: Grant[],
  limits: InvocationLimits,
  deadline: UnixTimestamp,
  trace_context: TraceContext
}

AuthContext {
  subject: Subject,
  scope: Scope
}

ArtifactDigest = string

InvocationLimits {
  max_memory_bytes: u64,
  max_duration_ms: u64,
  max_host_calls: u64,
  max_input_bytes: u64,
  max_output_bytes: u64
}

TraceContext {
  trace_id: Bytes,
  span_id: Bytes,
  parent_span_id: Bytes
}
```

`AgentManifest` is defined in
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).
`Grant` is defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#grants).

`Subject`, `Scope`, and `UnixTimestamp` are defined in
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md).
`ArtifactDigest` is the canonical `artifact:sha256:<hex>` identity defined by
[Artifact digests](03-agent-manifests-artifacts-schemas-and-registries.md#artifact-digests).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `auth_context` | AuthContext | Yes | Authentication and authorization context |
| `artifact_digest` | ArtifactDigest | Yes | Canonical identity of the admitted artifact |
| `manifest` | AgentManifest | Yes | Agent manifest with reducer configuration |
| `state_snapshot` | StateSnapshot | Yes | Current state revision for the turn |
| `grants` | Grant[] | Yes | Granted capabilities for this invocation |
| `limits` | InvocationLimits | Yes | Resource limits for this invocation |
| `deadline` | UnixTimestamp | Yes | Absolute deadline for invocation completion |
| `trace_context` | TraceContext | Yes | Distributed tracing context |

> **Normative definition.**

```
StateSnapshot {
  revision: int,
  schema_version: string,
  state: JsonObject,
  strategy_state: JsonObject?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `revision` | int | Yes | Current state revision number |
| `schema_version` | string | Yes | State schema version |
| `state` | JsonObject | Yes | Current agent state |
| `strategy_state` | JsonObject? | Yes | Current strategy state if applicable |

> **Normative definition.**
The `auth_context.subject` MUST be validated against the agent manifest's
authorized subjects before instance creation.
The `artifact_digest` MUST match the cached artifact's digest.
If the digest does not match, the host MUST reject with
`extism.invocation.artifact_digest_mismatch`.

> **Normative definition.**
The `limits` field constrains the Extism instance configuration:
`max_memory_bytes` sets the instance memory limit,
`max_duration_ms` sets the execution timeout,
`max_host_calls` sets the host function call limit,
`max_input_bytes` and `max_output_bytes` constrain guest memory usage.
These values MUST equal the effective named ceilings for
`memory.max_pages` multiplied by 65,536, `time.turn_ms`,
`host_calls.max_count`, `input.max_bytes`, and `output.max_bytes`,
respectively. Their exhaustion diagnostics use those limit identifiers.

### Compiled artifact caching

> **Normative definition.**
The host MUST cache compiled WebAssembly artifacts separately from mutable
instance creation and reuse.

> **Normative definition.**

```
ArtifactCache {
  digest: ArtifactDigest,
  compiled_module: CompiledModule,
  created_at: UnixTimestamp,
  last_used_at: UnixTimestamp,
  usage_count: u64
}

CompiledModule {
  bytes: Bytes,
  hash: Bytes
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `digest` | ArtifactDigest | Yes | Canonical identity of the artifact |
| `compiled_module` | CompiledModule | Yes | Pre-compiled WebAssembly module |
| `created_at` | UnixTimestamp | Yes | Cache entry creation time |
| `last_used_at` | UnixTimestamp | Yes | Last invocation time |
| `usage_count` | u64 | Yes | Number of times the cache entry was reused |

> **Normative definition.**
When the cache exceeds its configured size limit, the host MUST evict
least-recently-used entries until the cache is within the limit.
Cache entries MUST be validated against their digest on every access.
If a cached artifact's digest does not match, the host MUST recompile and
update the cache entry.

> **Normative definition.**
The host MUST NOT share compiled modules across tenants.
Each tenant's artifacts MUST be isolated by their digest and authorization
context.

### Fresh instance reference behavior

> **Normative definition.**
The host MUST create fresh Extism instances with explicit configuration:
manifest, memory, timeout, cancellation, and host-function configuration.

> **Normative definition.**

```
InstanceConfig {
  manifest: AgentManifest,
  memory_limit: u64,
  timeout_ms: u64,
  cancellation_token: CancellationToken,
  host_functions: Vec<HostFunction>
}

CancellationToken {
  id: String,
  cancelled: bool
}

HostFunction {
  name: String,
  signature: FunctionSignature,
  implementation: HostFunctionImpl
}

FunctionSignature {
  params: Vec<Type>,
  results: Vec<Type>
}
```

`AgentManifest` is defined in
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `manifest` | AgentManifest | Yes | Agent manifest for this instance |
| `memory_limit` | u64 | Yes | Maximum memory in bytes |
| `timeout_ms` | u64 | Yes | Execution timeout in milliseconds |
| `cancellation_token` | CancellationToken | Yes | Token for cancellation |
| `host_functions` | Vec\<HostFunction\> | Yes | Host functions exported to the guest |

> **Normative definition.**
Each instance MUST be created from a fresh compiled module.
Instances MUST NOT be reused across turns.
Instances MUST be disposed after each invocation completes, whether successfully
or with a trap.

> **Normative definition.**
The host MUST observe the `cancellation_token` before entering guest code, at
every host-function boundary, and before validating guest output. If the token
is cancelled at any of those points, or runtime interruption reports the
cancellation earlier, the host MUST terminate the instance and return
`extism.instance.cancelled`. It MUST NOT publish successful output, state
changes, or directives from that invocation.

> **Normative definition.**
Host functions MUST be registered with explicit signatures.
The host MUST validate that all host function calls from the guest conform
to their registered signatures.
If a host function is called with an invalid signature, the host MUST trap
the instance and return `extism.invocation.host_function_invalid`.

## 1.2 Behavior And Integration

### Invocation execution

> **Normative definition.**
The host MUST invoke `describe`, `initialize`, `reduce`, and `migrate` exports
through one bounded adapter.
The host MUST capture raw output, errors, traps, and usage metrics.

> **Normative definition.**

```
InvocationAdapter {
  instance: Instance,
  exports: ExportSet,
  input_buffer: Bytes,
  output_buffer: Bytes,
  usage: InvocationUsage
}
```

> **Normative definition.**

```
ExportSet {
  describe: Option<Function>,
  initialize: Option<Function>,
  reduce: Option<Function>,
  migrate: Option<Function>
}
```

> **Normative definition.**

```
InvocationUsage {
  input_bytes: u64,
  output_bytes: u64,
  host_calls: u64,
  memory_bytes_peak: u64,
  duration_ms: u64
}
```

> **Normative definition.**
The adapter uses exports according to operation lifecycle, not as a four-call
sequence around each turn:

1. **Describe** MAY run during artifact admission and MAY be served from a
   validated cache.
2. **Initialize** runs exactly once when creating fresh state for one agent
   instance. It MUST NOT run before an ordinary turn.
3. **Migrate** runs only on a separately authorized maintenance request and
   completes before a turn may load the migrated revision.
4. **Reduce** runs exactly once for each accepted turn attempt and is the only
   guest export invoked in the ordinary turn path.

For an agent lifecycle, successful initialization precedes any migration or
turn, each migration precedes turns using its target schema, and reductions
follow mailbox order. No adapter may invoke initialize or migrate
transparently in response to a reduce failure.

> **Normative definition.**
The host MUST capture the following metrics for each invocation:
- `input_bytes`: Bytes written to the guest
- `output_bytes`: Bytes read from the guest
- `host_calls`: Number of host function calls
- `memory_bytes_peak`: Peak memory usage
- `duration_ms`: Total invocation duration

> **Normative definition.**
If any export invocation fails with a trap, the host MUST capture the trap
information, skip output validation, and return `extism.instance.trap`.
Traps MUST NOT leak guest memory or implementation details.

### Output validation

> **Normative definition.**
The host MUST validate output bytes, encoding, schema, semantics, revision,
directives, and limits before exposing a result to host state logic.

> **Normative definition.**

```
InvocationResult {
  status: InvocationStatus,
  state_patch: StatePatch?,
  directives: Directive[],
  diagnostics: Diagnostic[],
  usage: InvocationUsage
}
```

`StatePatch` is defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#state-patch).

The `Directive`, `RetryClass`, and `ResultContract` wire structures are defined
in [Directives](04-turn-lifecycle-protocols-and-canonical-encoding.md#directives).
`DirectiveKindName`, host-derived `CausalMetadata`, and descriptor-only
`CapabilityRef` are defined by
[Directive](13-directives-strategies-continuations-and-terminal-states.md#directive).
Chapter 13 adds validation, commit, and execution semantics without replacing
the chapter 04 wire structure.

> **Normative definition.**

```
InvocationStatus {
  kind: StatusKind,
  message: String,
  diagnostic_code: Option<String>
}
```

> **Normative definition.**

```
StatusKind {
  Success,
  Error(String),
  Trap(String),
  Timeout,
  Cancelled,
  ArtifactNotFound,
  ArtifactDigestMismatch,
  HostFunctionInvalid
}
```

> **Normative definition.**
The host MUST perform the following validation steps in order:

1. **Byte validation**: Verify output bytes are within `max_output_bytes` limit.
2. **Encoding validation**: Verify output is valid UTF-8 and canonical JSON.
3. **Schema validation**: Validate output against the expected schema.
4. **Semantic validation**: Verify state patch operation and resulting-state semantics.
5. **Revision validation**: Verify `TurnResult.expected_state_revision`
   matches the request and loaded snapshot.
6. **Directives validation**: Validate directive structure and capabilities per
   [Directive processing](13-directives-strategies-continuations-and-terminal-states.md#directive-processing).
7. **Limits validation**: Verify all usage metrics are within configured limits.

> **Normative definition.**
If any validation step fails, the host MUST reject the output and emit a
diagnostic with the appropriate error code.
The host MUST NOT expose the invalid output to host state logic.

> **Normative definition.**
The host MUST validate that `TurnResult.expected_state_revision` matches the
request and the integer `state_snapshot.revision`; `StatePatch` contains no
revision field. If the result value does not match, the host MUST reject with
`extism.output.revision_mismatch`.

### Instance disposal

> **Normative definition.**
The host MUST dispose or quarantine instances after trap, timeout, cancellation,
invalid output, or uncertain host callback state.

> **Normative definition.**

```
InstanceDisposition {
  action: DispositionAction,
  reason: DispositionReason
}
```

> **Normative definition.**

```
DispositionAction {
  Dispose,
  Quarantine
}
```

> **Normative definition.**

```
DispositionReason {
  SuccessfulCompletion,
  Trap,
  Timeout,
  Cancelled,
  InvalidOutput,
  UncertainHostCallbackState,
  ArtifactNotFound,
  ArtifactDigestMismatch,
  HostFunctionInvalid
}
```

> **Normative definition.**
The host MUST dispose instances in the following cases:
- **Successful completion**: Dispose after successful output validation.
- **Trap**: Dispose after capturing trap information.
- **Timeout**: Dispose after timeout expiration.
- **Cancelled**: Dispose after cancellation.
- **Invalid output**: Dispose after output validation failure.

> **Normative definition.**
The host MUST quarantine instances in the following cases:
- **Uncertain host callback state**: When host function callbacks may have
  partially executed but the instance did not trap.

> **Normative definition.**
Quarantined instances MUST NOT be reused.
The host MUST record the quarantine event and reason, capture bounded debugging
evidence, and then dispose the instance. Disposal MUST complete before the host
accepts another invocation for the same agent.

## 1.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to extism invocation boundary instances
and output validation:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid invocation input structure | Failed JSON parsing or schema validation | `extism.invocation.malformed` |
| Incompatible | Reducer incompatible with invocation | Profile version mismatch | `extism.invocation.incompatible` |
| Conflicting | Invocation lacks the current turn lease | Another worker owns the agent lease | `mailbox.turn_lease.conflict` |
| Unauthorized | Missing capability for host function | Required capability not granted | `extism.invocation.unauthorized` |
| Exhausted | Named limit exceeded | Input, output, memory, duration, or host-call limit | `identity.limit.<limit_identifier>` |
| Unavailable | Artifact or dependency unavailable | Artifact not found or cache miss | `extism.invocation.unavailable` |
| ArtifactDigestMismatch | Cached artifact digest does not match | Artifact updated without cache invalidation | `extism.invocation.artifact_digest_mismatch` |
| HostFunctionInvalid | Host function called with invalid signature | Signature mismatch | `extism.invocation.host_function_invalid` |

> **Normative definition.**
All failure modes MUST produce a diagnostic and terminate the invocation without
partial state changes.
The host MUST NOT expose implementation details in diagnostics.

### Diagnostics

> **Normative definition.**
All diagnostics emitted by the host MUST conform to the `Diagnostic` type
defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics).

Diagnostics MUST identify the phase contract, profile, and failed boundary
without exposing secrets or implementation internal state.

### Diagnostic families

| Family | Purpose | Example codes |
|--------|---------|---------------|
| `extism.invocation` | Invocation failures independent of named limits | `malformed`, `incompatible`, `unauthorized`, `unavailable`, `artifact_digest_mismatch`, `host_function_invalid` |
| `extism.output` | Output validation failures | `encoding_invalid`, `schema_invalid`, `semantic_invalid`, `revision_mismatch` |
| `extism.instance` | Instance lifecycle failures independent of named limits | `trap`, `cancelled`, `quarantined` |
| `identity.limit` | Named invocation-limit exhaustion | `input.max_bytes`, `output.max_bytes`, `memory.max_pages`, `time.turn_ms` |

### Internal mechanisms and fixed behavior

> **Normative definition.**
The cache storage layout, host-function registration adapter, cancellation
delivery mechanism, and quarantine storage are internal mechanisms. Every such
mechanism MUST be observationally equivalent with respect to digest
validation, cache eviction order, registered signatures, cancellation status,
diagnostics, validated output, state changes, directives, and instance reuse.
An internal mechanism MUST NOT change whether an invocation is accepted,
cancelled, trapped, quarantined, or reported as successful.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Instance pooling**: A formal instance pooling strategy will be implemented in future milestones. The protocol is language-neutral and does not require instance pooling for base conformance.

2. **Hot-reload**: A formal hot-reload mechanism will be implemented in future milestones. The protocol is language-neutral and does not require hot-reload for base conformance.

3. **Multi-tenant isolation**: Enhanced multi-tenant isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 1.4 Phase 1 Integration Tests

### Canonical successful flow

> **Normative definition.**
The canonical successful flow integration test validates that a valid invocation
is processed successfully through the full invocation and validation pipeline.

Expected behavior:

- Input: valid invocation with authenticated context, cached artifact, and state snapshot.
- Expected output: InvocationResult with state_patch, directives, diagnostics, and usage.
- Expected error: null.

### Negative: malformed input

> **Normative definition.**
The negative malformed input test validates that invalid invocation input is rejected.

Expected behavior:

- Input: invocation with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `extism.invocation.malformed`.

### Negative: artifact digest mismatch

> **Normative definition.**
The negative artifact digest mismatch test validates that cached artifacts with
mismatched digests are rejected.

Expected behavior:

- Input: invocation with artifact digest that does not match cached artifact.
- Expected output: null.
- Expected error: `extism.invocation.artifact_digest_mismatch`.

### Negative: incompatible profile

> **Normative definition.**
The negative incompatible profile test validates that profile mismatches are rejected.

Expected behavior:

- Input: invocation with profile version that does not match the reducer's profile version.
- Expected output: null.
- Expected error: `extism.invocation.incompatible`.

### Negative: unauthorized

> **Normative definition.**
The negative unauthorized test validates that missing capabilities are rejected.

Expected behavior:

- Input: invocation with host function call requiring ungranted capability.
- Expected output: null.
- Expected error: `extism.invocation.unauthorized`.

### Negative: exhausted resources

> **Normative definition.**
The negative exhausted resources test validates that named invocation limits
use their canonical diagnostics.

Expected behavior:

- Input: separate invocations that exceed the configured turn-duration and
  memory-page limits.
- Expected output: null.
- Expected errors: `identity.limit.time.turn_ms` and
  `identity.limit.memory.max_pages`, respectively.

### Negative: unavailable artifact

> **Normative definition.**
The negative unavailable artifact test validates that missing artifacts are rejected.

Expected behavior:

- Input: invocation referencing an artifact that does not exist in the cache.
- Expected output: null.
- Expected error: `extism.invocation.unavailable`.

### Negative: invalid host function signature

> **Normative definition.**
The negative invalid host function signature test validates that host function
calls with invalid signatures are rejected.

Expected behavior:

- Input: invocation with host function call that does not match the registered signature.
- Expected output: null.
- Expected error: `extism.invocation.host_function_invalid`.

### Negative: result revision mismatch

> **Normative definition.**
The negative output revision mismatch test validates that a
`TurnResult.expected_state_revision` mismatch is rejected.

Expected behavior:

- Input: invocation whose `TurnResult.expected_state_revision` differs from
  both the request and `state_snapshot.revision`.
- Expected output: null.
- Expected error: `extism.output.revision_mismatch`.

### Negative: output limits exceeded

> **Normative definition.**
The negative output limits exceeded test validates that output exceeding limits is rejected.

Expected behavior:

- Input: invocation producing output that exceeds `max_output_bytes`.
- Expected output: null.
- Expected error: `identity.limit.output.max_bytes`.

### Negative: instance trap

> **Normative definition.**
The negative instance trap test validates that instance traps are handled correctly.

Expected behavior:

- Input: invocation that causes the guest instance to trap.
- Expected output: null.
- Expected error: `extism.instance.trap`.

### Negative: instance timeout

> **Normative definition.**
The negative instance timeout test validates that instance timeouts are handled correctly.

Expected behavior:

- Input: invocation that exceeds the configured timeout.
- Expected output: null.
- Expected error: `identity.limit.time.turn_ms`.

### Negative: instance cancellation

> **Normative definition.**
The negative instance cancellation test validates that instance cancellations are handled correctly.

Expected behavior:

- Input: invocation that is cancelled via the cancellation token.
- Expected output: null.
- Expected error: `extism.instance.cancelled`.

### Fixed mechanism conformance

> **Normative definition.**
The Phase 1 integration tests MUST verify the fixed behavior independently of
private implementation structure:

1. Configure a cache for three equal-sized entries, fill it, access the oldest
   entry, insert a fourth entry, and verify that the least-recently-used entry
   is evicted while the accessed entry remains.
2. Cancel an invocation before guest entry, during a host-function call, and
   after guest return but before output validation; each case MUST publish no
   successful output, state change, or directive and MUST return the
   cancellation diagnostic.
3. Produce uncertain host callback state and verify that the instance is never
   reused, bounded quarantine evidence is captured, and disposal completes
   before another invocation for the same agent is accepted.

### Cross-milestone fixture regression

> **Normative definition.**
All earlier milestone fixtures MUST be re-run after Phase 1 to verify
no regressions.

Expected behavior:

- All Phase 1 fixtures: PASS.
- All Phase 2 fixtures: PASS.
- All Phase 3 fixtures: PASS.
- All Phase 4 fixtures: PASS.
- All Milestone 1 fixtures: PASS.
- All Milestone 2 Phase 1 fixtures: PASS.
- All Milestone 2 Phase 2 fixtures: PASS.
- All Milestone 2 Phase 3 fixtures: PASS.
- All Milestone 2 Phase 4 fixtures: PASS.
- All Milestone 2 Phase 5 fixtures: PASS.

Any approved variability MUST be documented in the Milestone 3 exit report.

## Variability register

The register summarizes fixed behavior and internal mechanisms. It does not
independently license variation.

| Clause | Type | Selection | Constraint |
|--------|------|-----------|------------|
| Invocation input structure | Required | Fields fixed by this chapter | Validate before instance creation |
| [Artifact caching](#compiled-artifact-caching) | Required | Least-recently-used eviction | Validate the digest on every access |
| [Host-function registration](#fresh-instance-reference-behavior) | Internal mechanism | No profile selection | Preserve signatures, authorization, traps, and diagnostics |
| Fresh instance creation | Required | Per invocation | Never reuse an instance across turns |
| [Export lifecycle](#invocation-execution) | Required | Describe at admission, initialize once, migrate only under maintenance, reduce once per turn | Never wrap an ordinary reduce with initialize or migrate |
| Output validation | Required | Seven-step validation pipeline | Reject before exposing invalid output |
| [Invocation limit diagnostics](#failure-modes) | Required | `identity.limit.<limit_identifier>` | Map adapter limits to the canonical named ceilings |
| [Cancellation delivery](#fresh-instance-reference-behavior) | Internal mechanism | No profile selection | Observe cancellation at every specified boundary and publish no success after cancellation |
| [Quarantine storage](#instance-disposal) | Internal mechanism | No profile selection | Capture bounded evidence, never reuse, and dispose before the next invocation for the agent |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The invocation boundary provides:

- A host-owned boundary that resolves artifacts and creates constrained instances.
- A clear operation-specific lifecycle for describe, initialize, migrate, and reduce.
- A comprehensive output validation pipeline.
- Instance disposal and quarantine for safety.

The failure modes provide:

- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.
- Evidence that failures are handled correctly.

The integration tests provide:

- Verification that the canonical flow works end-to-end.
- Evidence that all failure modes are handled correctly.
- Foundation for cross-implementation conformance testing.
