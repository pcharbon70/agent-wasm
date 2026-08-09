---
title: "Extism Invocation Boundary Instances And Output Validation"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
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
  artifact_digest: Digest,
  manifest: Manifest,
  state_snapshot: StateSnapshot,
  grants: CapabilityGrants,
  limits: InvocationLimits,
  deadline: UnixTimestamp,
  trace_context: TraceContext
}

AuthContext {
  subject: Subject,
  scope: Scope
}

Digest {
  algorithm: HashAlgorithm,
  value: Bytes
}

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

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `auth_context` | AuthContext | Yes | Authentication and authorization context |
| `artifact_digest` | Digest | Yes | Hash of the compiled WebAssembly artifact |
| `manifest` | Manifest | Yes | Agent manifest with reducer configuration |
| `state_snapshot` | StateSnapshot | Yes | Current state revision for the turn |
| `grants` | CapabilityGrants | Yes | Granted capabilities for this invocation |
| `limits` | InvocationLimits | Yes | Resource limits for this invocation |
| `deadline` | UnixTimestamp | Yes | Absolute deadline for invocation completion |
| `trace_context` | TraceContext | Yes | Distributed tracing context |

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

### Compiled artifact caching

> **Normative definition.**
The host MUST cache compiled WebAssembly artifacts separately from mutable
instance creation and reuse.

> **Normative definition.**

```
ArtifactCache {
  digest: Digest,
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
| `digest` | Digest | Yes | Hash identifying the artifact |
| `compiled_module` | CompiledModule | Yes | Pre-compiled WebAssembly module |
| `created_at` | UnixTimestamp | Yes | Cache entry creation time |
| `last_used_at` | UnixTimestamp | Yes | Last invocation time |
| `usage_count` | u64 | Yes | Number of times the cache entry was reused |

> **Normative definition.**
The host MAY evict cache entries using a least-recently-used policy when the
cache exceeds its configured size limit.
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
  manifest: Manifest,
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

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `manifest` | Manifest | Yes | Agent manifest for this instance |
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
The `cancellation_token` MUST be checked periodically during long-running
invocations.
If the token is cancelled, the host MUST terminate the instance and return
`extism.invocation.cancelled`.

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

ExportSet {
  describe: Option<Function>,
  initialize: Option<Function>,
  reduce: Option<Function>,
  migrate: Option<Function>
}

InvocationUsage {
  input_bytes: u64,
  output_bytes: u64,
  host_calls: u64,
  memory_bytes_peak: u64,
  duration_ms: u64
}
```

> **Normative definition.**
The host MUST invoke exports in the following order for each turn:

1. **Describe** (optional): Query the reducer's capabilities and configuration.
2. **Initialize**: Initialize the reducer with the current state and grants.
3. **Reduce**: Execute the turn with the provided signals and instructions.
4. **Migrate** (optional): Migrate state to a new schema version if needed.

> **Normative definition.**
The host MUST capture the following metrics for each invocation:
- `input_bytes`: Bytes written to the guest
- `output_bytes`: Bytes read from the guest
- `host_calls`: Number of host function calls
- `memory_bytes_peak`: Peak memory usage
- `duration_ms`: Total invocation duration

> **Normative definition.**
If any export invocation fails with a trap, the host MUST capture the trap
information and proceed to output validation.
Traps MUST NOT leak guest memory or implementation details.

### Output validation

> **Normative definition.**
The host MUST validate output bytes, encoding, schema, semantics, revision,
directives, and limits before exposing a result to host state logic.

> **Normative definition.**

```
InvocationResult {
  status: InvocationStatus,
  state_patch: Option<StatePatch>,
  directives: Vec<Directive>,
  diagnostics: Vec<Diagnostic>,
  usage: InvocationUsage
}

InvocationStatus {
  kind: StatusKind,
  message: String,
  diagnostic_code: Option<String>
}

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
2. **Encoding validation**: Verify output is valid UTF-8 or canonical JSON.
3. **Schema validation**: Validate output against the expected schema.
4. **Semantic validation**: Verify state patch semantics (revision, operations).
5. **Revision validation**: Verify state patch revision matches expected revision.
6. **Directives validation**: Validate directive structure and capabilities.
7. **Limits validation**: Verify all usage metrics are within configured limits.

> **Normative definition.**
If any validation step fails, the host MUST reject the output and emit a
diagnostic with the appropriate error code.
The host MUST NOT expose the invalid output to host state logic.

> **Normative definition.**
The host MUST validate that the `state_patch.revision` matches the expected
revision from the `state_snapshot`.
If the revision does not match, the host MUST reject with
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

DispositionAction {
  Dispose,
  Quarantine
}

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
The host MUST log the quarantine event with the reason and retain the instance
for debugging purposes.

## 1.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to extism invocation boundary instances
and output validation:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid invocation input structure | Failed JSON parsing or schema validation | `extism.invocation.malformed` |
| Incompatible | Reducer incompatible with invocation | Profile version mismatch | `extism.invocation.incompatible` |
| Conflicting | Concurrent invocations on same revision | Same state revision targeted | `state.revision.conflict` |
| Unauthorized | Missing capability for host function | Required capability not granted | `extism.invocation.unauthorized` |
| Exhausted | Resource limits exceeded | Timeout, memory, or iteration limit | `extism.invocation.exhausted` |
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
| `extism.invocation` | Invocation failures | `malformed`, `incompatible`, `unauthorized`, `exhausted`, `unavailable`, `artifact_digest_mismatch`, `host_function_invalid` |
| `extism.output` | Output validation failures | `encoding_invalid`, `schema_invalid`, `semantic_invalid`, `revision_mismatch`, `limits_exceeded` |
| `extism.instance` | Instance lifecycle failures | `trap`, `timeout`, `cancelled`, `quarantined` |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Cache eviction policy**: The host MAY choose the cache eviction policy. The policy MUST be documented in the conformance profile.

2. **Host function registration**: The host MAY choose how to register and validate host functions. The mechanism is implementation-defined.

3. **Cancellation polling**: The host MAY choose how frequently to check the cancellation token. The frequency MUST be documented in the conformance profile.

4. **Quarantine retention**: The host MAY choose how long to retain quarantined instances. The retention period MUST be documented in the conformance profile.

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
The negative exhausted resources test validates that resource limit violations are rejected.

Expected behavior:

- Input: invocation that exceeds the configured timeout or memory limit.
- Expected output: null.
- Expected error: `extism.invocation.exhausted`.

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

### Negative: output revision mismatch

> **Normative definition.**
The negative output revision mismatch test validates that state patches with
mismatched revisions are rejected.

Expected behavior:

- Input: invocation producing state patch with revision that does not match the expected revision.
- Expected output: null.
- Expected error: `extism.output.revision_mismatch`.

### Negative: output limits exceeded

> **Normative definition.**
The negative output limits exceeded test validates that output exceeding limits is rejected.

Expected behavior:

- Input: invocation producing output that exceeds `max_output_bytes`.
- Expected output: null.
- Expected error: `extism.output.limits_exceeded`.

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
- Expected error: `extism.instance.timeout`.

### Negative: instance cancellation

> **Normative definition.**
The negative instance cancellation test validates that instance cancellations are handled correctly.

Expected behavior:

- Input: invocation that is cancelled via the cancellation token.
- Expected output: null.
- Expected error: `extism.instance.cancelled`.

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

| Clause | Type | Selection |
|--------|------|-----------|
| Invocation input structure | Required | Fields fixed by this chapter |
| Artifact caching | Required | Separate from instance creation, fixed by this chapter |
| Fresh instance creation | Required | Per-invocation, fixed by this chapter |
| Invocation order | Required | describe, initialize, reduce, migrate, fixed by this chapter |
| Output validation | Required | 7-step validation pipeline, fixed by this chapter |
| Instance disposal | Required | Dispose or quarantine, fixed by this chapter |
| Cache eviction policy | Implementation-defined | Documented in conformance profile |
| Host function registration | Implementation-defined | Documented in conformance profile |
| Cancellation polling | Implementation-defined | Documented in conformance profile |
| Quarantine retention | Implementation-defined | Documented in conformance profile |

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The invocation boundary provides:

- A host-owned boundary that resolves artifacts and creates constrained instances.
- A clear invocation order from describe through migrate.
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
