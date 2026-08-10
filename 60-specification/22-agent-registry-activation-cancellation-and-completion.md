---
title: "Agent Registry Activation Cancellation And Completion"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "0.1.0"
tags:
  - milestone-03
  - phase-03
  - agent-registry
  - activation
  - cancellation
  - completion
aliases:
  - "M3-P3 Agent Registry And Lifecycle"
---

# Agent Registry Activation Cancellation And Completion

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/phase-03-agent-registry-activation-cancellation-and-completion.md)
of
[Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/README.md)
--
Host Actor Runtime And Lifecycle.
It manages logical agent identity and disposable live actors without
persisting engine or process handles.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 3
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

## 3.1 Contract And Data Model

### Registry record

> **Normative definition.**
A registry record represents a logical agent instance with tenant, agent
type/version, instance identity, artifact, lifecycle policy, durable
revision, and activation status.

> **Normative definition.**

```
RegistryRecord {
  tenant_id: TenantId,
  agent_id: AgentId,
  agent_type: string,
  agent_version: string,
  instance_id: InstanceId,
  artifact_digest: Digest,
  lifecycle_policy: LifecyclePolicy,
  durable_revision: u64,
  activation_status: ActivationStatus
}

InstanceId = string

LifecyclePolicy {
  activation: ActivationPolicy,
  completion: CompletionPolicy,
  cancellation: CancellationPolicy
}

ActivationPolicy {
  kind: ActivationKind,
  eager_config: EagerConfig?,
  lazy_config: LazyConfig?
}

ActivationKind = "eager" | "lazy" | "on-signal" | "disabled"

EagerConfig {
  initialize_immediately: bool,
  initial_state: JsonObject?
}

LazyConfig {
  max_idle_ms: u64,
  max_turns: u64?
}

CompletionPolicy {
  kind: CompletionKind,
  on_last_turn: LastTurnBehavior
}

CompletionKind = "automatic" | "explicit" | "never"

LastTurnBehavior = "retain_state" | "archive_state" | "delete_state"

CancellationPolicy {
  kind: CancellationKind,
  allow_during_turn: bool
}

CancellationKind = "never" | "always" | "during_idle"

ActivationStatus {
  kind: ActivationState,
  activated_at: UnixTimestamp?,
  last_turn_at: UnixTimestamp?,
  current_revision: u64?
}

ActivationState {
  Pending,
  Activating,
  Active,
  Suspended,
  Hibernal,
  Cancelled,
  Completed,
  Terminated
}
```

`TenantId`, `AgentId`, `Digest`, and `UnixTimestamp` are defined in
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `tenant_id` | TenantId | Yes | Tenant this agent belongs to |
| `agent_id` | AgentId | Yes | Unique agent identifier within the tenant |
| `agent_type` | string | Yes | Logical agent type (e.g., "customer-support") |
| `agent_version` | string | Yes | Semantic version of the agent type |
| `instance_id` | InstanceId | Yes | Unique instance identifier |
| `artifact_digest` | Digest | Yes | Digest of the compiled artifact |
| `lifecycle_policy` | LifecyclePolicy | Yes | Lifecycle behavior configuration |
| `durable_revision` | u64 | Yes | Last committed state revision |
| `activation_status` | ActivationStatus | Yes | Current activation state |

> **Normative definition.**
The `instance_id` is unique per `(tenant_id, agent_id)` tuple.
The host MUST reject duplicate instance IDs with `registry.instance.duplicate`.

> **Normative definition.**
The `durable_revision` is the last state revision that has been committed
to durable storage.
The host MUST NOT allow state revisions to regress below `durable_revision`.

### Registry operations

> **Normative definition.**
The registry MUST support the following operations:

1. **Create**: Create a new registry record.
2. **Resolve**: Look up a registry record by instance ID.
3. **Activate**: Transition a record from `Pending` to `Active` or `Activating`.
4. **Initialize**: Initialize a live actor for an activated record.
5. **Suspend**: Transition a live actor from `Active` to `Suspended`.
6. **Hibernate**: Transition a live actor from `Suspended` to `Hibernal`.
7. **Thaw**: Transition a live actor from `Hibernal` to `Active`.
8. **Cancel**: Cancel a live actor and transition to `Cancelled`.
9. **Terminate**: Terminate a live actor and transition to `Terminated`.
10. **Inspect**: Query the current state of a registry record.

> **Normative definition.**

```
RegistryOperations {
  create: (CreateRequest) -> RegistryRecord,
  resolve: (InstanceId) -> RegistryRecord?,
  activate: (ActivateRequest) -> ActivationResult,
  initialize: (InitializeRequest) -> InitializationResult,
  suspend: (InstanceId) -> ActivationResult,
  hibernate: (InstanceId) -> ActivationResult,
  thaw: (InstanceId) -> ActivationResult,
  cancel: (CancelRequest) -> CancellationResult,
  terminate: (InstanceId) -> TerminationResult,
  inspect: (InstanceId) -> RegistryRecord?
}

CreateRequest {
  tenant_id: TenantId,
  agent_id: AgentId,
  agent_type: string,
  agent_version: string,
  artifact_digest: Digest,
  lifecycle_policy: LifecyclePolicy
}

ActivateRequest {
  instance_id: InstanceId,
  initialize: bool
}

ActivationResult {
  status: ActivationStatus,
  diagnostics: Diagnostic[]
}

InitializeRequest {
  instance_id: InstanceId,
  initial_state: JsonObject?
}

InitializationResult {
  status: ActivationStatus,
  initial_revision: u64,
  diagnostics: Diagnostic[]
}

CancelRequest {
  instance_id: InstanceId,
  reason: string
}

CancellationResult {
  status: ActivationStatus,
  diagnostics: Diagnostic[]
}

TerminationResult {
  status: ActivationStatus,
  diagnostics: Diagnostic[]
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `tenant_id` | TenantId | Yes | Tenant creating the agent |
| `agent_id` | AgentId | Yes | Unique agent identifier |
| `agent_type` | string | Yes | Logical agent type |
| `agent_version` | string | Yes | Agent type version |
| `artifact_digest` | Digest | Yes | Compiled artifact digest |
| `lifecycle_policy` | LifecyclePolicy | Yes | Lifecycle behavior configuration |
| `instance_id` | InstanceId | Yes | Unique instance identifier |
| `initialize` | bool | Yes | Whether to initialize on activation |
| `initial_state` | JsonObject? | No | Initial state for initialization |
| `reason` | string | Yes | Reason for cancellation |

### Durable completion/cancellation state

> **Normative definition.**
The host MUST separate durable completion/cancellation state from live actor
presence.

> **Normative definition.**

```
DurableState {
  instance_id: InstanceId,
  durable_revision: u64,
  completion_state: CompletionState,
  cancellation_state: CancellationState
}

CompletionState {
  kind: CompletionKind,
  completed_at: UnixTimestamp?,
  final_revision: u64?
}

CancellationState {
  kind: CancellationKind,
  cancelled_at: UnixTimestamp?,
  cancellation_reason: string?
}
```

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `instance_id` | InstanceId | Yes | Unique instance identifier |
| `durable_revision` | u64 | Yes | Last committed state revision |
| `completion_state` | CompletionState | Yes | Durable completion state |
| `cancellation_state` | CancellationState | Yes | Durable cancellation state |

> **Normative definition.**
The `DurableState` concept MUST be maintained.
The concrete persistence mechanism for `DurableState` is deferred to Milestone 4.
During Milestone 3, `DurableState` is held in memory only.

> **Non-normative note.**
Milestone 4 will add durable storage for `DurableState`, registry records,
mailbox entries, sensor state, schedule state, and timer state.
Until then, a host restart will lose all state.

> **Normative definition.**
The live actor (Extism instance) is a disposable projection of the registry
record.
The host MUST NOT persist the live actor itself; only the registry record
and `DurableState` are durable concepts.

## 3.2 Behavior And Integration

### Activation policies

> **Normative definition.**
The host MUST support the following activation policies:

1. **Eager**: The host activates the agent immediately upon creation.
2. **Lazy**: The host activates the agent on the first turn request.
3. **On-signal**: The host activates the agent when a specific signal is received.
4. **Disabled**: The host never activates the agent.

> **Normative definition.**
The `activation_policy.kind` field selects the activation policy.
The host MUST enforce the activation policy for every registry record.

> **Normative definition.**
The host MUST document the activation policy for each registry record in
the conformance profile.

### Activation behavior

> **Normative definition.**
The host MUST handle the following activation scenarios:

1. **Activation deduplication**: If an agent is already activated, the host MUST reject duplicate activation requests with `registry.activation.duplicate`.
2. **Initialization failure**: If initialization fails, the host MUST transition the agent to `Terminated` with `registry.activation.initialization_failed`.
3. **Unknown artifact**: If the artifact digest is not found in the cache, the host MUST reject with `registry.activation.artifact_not_found`.
4. **Incompatible state**: If the agent is in an incompatible state (e.g., `Cancelled`), the host MUST reject with `registry.activation.incompatible_state`.
5. **Concurrent cancellation**: If a cancellation request arrives during activation, the host MUST cancel the activation with `registry.activation.cancelled_during_activation`.

> **Normative definition.**

```
ActivationFailure {
  kind: ActivationFailureKind,
  message: String,
  diagnostic_code: String
}

ActivationFailureKind {
  Duplicate,
  InitializationFailed,
  ArtifactNotFound,
  IncompatibleState,
  CancelledDuringActivation
}
```

| Kind | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| `Duplicate` | Agent already activated | Activation request for active agent | `registry.activation.duplicate` |
| `InitializationFailed` | Initialization failed | Initialize export trapped or returned error | `registry.activation.initialization_failed` |
| `ArtifactNotFound` | Artifact not in cache | Artifact digest not found | `registry.activation.artifact_not_found` |
| `IncompatibleState` | Agent in incompatible state | Activation request for cancelled/completed agent | `registry.activation.incompatible_state` |
| `CancelledDuringActivation` | Cancellation during activation | Cancellation request during activation | `registry.activation.cancelled_during_activation` |

### Disposable projections

> **Normative definition.**
The host MUST ensure that all live instance, worker, socket, and process
references remain disposable projections.

> **Normative definition.**
A disposable projection is a reference to a live resource that can be
released without affecting the durable state.
The host MUST NOT persist disposable projections; only the registry record
and `DurableState` are durable.

> **Normative definition.**
The host MUST release all disposable projections when the agent transitions
to `Cancelled`, `Completed`, or `Terminated`.

> **Normative definition.**
The host MUST NOT leak disposable projections across agent lifecycles.
Each agent MUST have a fresh set of disposable projections for each activation.

## 3.3 Failure Evidence And Operational Notes

### Failure modes

> **Normative definition.**
The following failure modes are relevant to agent registry, activation,
cancellation, and completion:

| Mode | Description | Conditions | Diagnostic |
|------|-------------|------------|------------|
| Malformed | Invalid registry request structure | Failed JSON parsing or schema validation | `registry.request.malformed` |
| Incompatible | Agent in incompatible state | Activation request for cancelled/completed agent | `registry.activation.incompatible_state` |
| Conflicting | Duplicate instance ID | Two agents with same instance ID | `registry.instance.duplicate` |
| Unauthorized | Missing capability for registry operation | Required capability not granted | `registry.request.unauthorized` |
| Exhausted | Resource limits exceeded | Maximum agents per tenant reached | `registry.capacity.exhausted` |
| Unavailable | Registry or artifact unavailable | Registry not found or artifact not cached | `registry.instance.unavailable`, `registry.activation.artifact_not_found` |
| InitializationFailed | Agent initialization failed | Initialize export trapped or returned error | `registry.activation.initialization_failed` |
| Duplicate | Agent already activated | Activation request for active agent | `registry.activation.duplicate` |
| CancellationFailed | Cancellation failed | Cancel request failed | `registry.cancellation.failed` |

> **Normative definition.**
All failure modes MUST produce a diagnostic and terminate the operation without
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
| `registry.request` | Registry request failures | `malformed`, `unauthorized` |
| `registry.instance` | Registry instance failures | `duplicate`, `unavailable` |
| `registry.activation` | Activation failures | `duplicate`, `initialization_failed`, `artifact_not_found`, `incompatible_state`, `cancelled_during_activation` |
| `registry.cancellation` | Cancellation failures | `failed` |
| `registry.capacity` | Capacity failures | `exhausted` |

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and do not create
conformance obligations.
The Variability register below catalogs all such choices.

1. **Activation policy enforcement**: The host MAY choose how to enforce activation policies. The enforcement mechanism MUST be documented in the conformance profile.

2. **Durable state storage**: The host MAY choose the durable state storage mechanism. The storage mechanism MUST be documented in the conformance profile.

3. **Disposable projection release**: The host MAY choose how to release disposable projections. The release mechanism MUST be documented in the conformance profile.

4. **Registry persistence**: The host MAY choose how to persist registry records. The persistence mechanism MUST be documented in the conformance profile.

### Deferred work

> **Non-normative note.**
The following work is deferred to future milestones and creates no
conformance obligation for current implementations:

1. **Registry replication**: A formal registry replication strategy will be implemented in future milestones. The protocol is language-neutral and does not require registry replication for base conformance.

2. **Multi-tenant isolation**: Enhanced multi-tenant isolation will be implemented in future milestones. The protocol is language-neutral and does not require enhanced isolation for base conformance.

3. **Agent migration**: A formal agent migration mechanism will be implemented in future milestones. The protocol is language-neutral and does not require agent migration for base conformance.

4. **Milestone 4 planning**: Future milestones will build on Milestone 3 contracts and may introduce additional phases and chapters.

## 3.4 Phase 3 Integration Tests

### Canonical successful flow

> **Normative conformance criterion.**
The canonical successful flow integration test validates that a valid agent
registry operation is processed successfully through the full registry
lifecycle pipeline.

Expected behavior:

- Input: valid create request with tenant_id, agent_id, agent_type, artifact_digest, and lifecycle_policy.
- Expected output: RegistryRecord with ActivationStatus.Pending.
- Expected error: null.

### Negative: malformed request

> **Normative conformance criterion.**
The negative malformed request test validates that invalid registry requests are rejected.

Expected behavior:

- Input: registry request with invalid JSON or missing required fields.
- Expected output: null.
- Expected error: `registry.request.malformed`.

### Negative: duplicate instance ID

> **Normative conformance criterion.**
The negative duplicate instance ID test validates that duplicate instance IDs are rejected.

Expected behavior:

- Input: create request with instance ID that already exists.
- Expected output: null.
- Expected error: `registry.instance.duplicate`.

### Negative: unauthorized

> **Normative conformance criterion.**
The negative unauthorized test validates that missing capabilities are rejected.

Expected behavior:

- Input: registry request with missing required capability.
- Expected output: null.
- Expected error: `registry.request.unauthorized`.

### Negative: artifact not found

> **Normative conformance criterion.**
The negative artifact not found test validates that missing artifacts are rejected.

Expected behavior:

- Input: create request with artifact digest that is not in the cache.
- Expected output: null.
- Expected error: `registry.activation.artifact_not_found`.

### Negative: incompatible state

> **Normative conformance criterion.**
The negative incompatible state test validates that incompatible states are rejected.

Expected behavior:

- Input: activation request for an agent in Cancelled state.
- Expected output: null.
- Expected error: `registry.activation.incompatible_state`.

### Negative: initialization failed

> **Normative conformance criterion.**
The negative initialization failed test validates that initialization failures are handled correctly.

Expected behavior:

- Input: activation request with initialize=true, where the initialize export traps.
- Expected output: null.
- Expected error: `registry.activation.initialization_failed`.

### Negative: capacity exhausted

> **Normative conformance criterion.**
The negative capacity exhausted test validates that capacity limits are enforced.

Expected behavior:

- Input: create request that exceeds the maximum agents per tenant.
- Expected output: null.
- Expected error: `registry.capacity.exhausted`.

### Negative: cancellation failed

> **Normative conformance criterion.**
The negative cancellation failed test validates that cancellation failures are handled correctly.

Expected behavior:

- Input: cancel request that fails (e.g., agent not found).
- Expected output: null.
- Expected error: `registry.cancellation.failed`.

### Cross-milestone fixture regression

> **Normative conformance criterion.**
All earlier milestone fixtures MUST be re-run after Phase 3 to verify
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
| Registry record structure | Required | Fields fixed by this chapter |
| Registry operations | Required | 10 operations fixed by this chapter |
| Durable state structure | Required | Fields fixed by this chapter |
| Activation policies | Required | eager, lazy, on-signal, disabled, fixed by this chapter |
| Activation behavior | Required | 5 scenarios fixed by this chapter |
| Disposable projections | Required | Must be disposable, fixed by this chapter |

Other variability choices are documented in the section on host-defined selections.

## Rationale and evidence (non-normative)

This chapter derives from the deterministic reducer requirements identified
in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The registry provides:

- Logical agent identity management.
- Disposable live actors without persistent engine/process handles.
- Clear lifecycle transitions from creation to termination.

The activation policies provide:

- Flexible activation strategies (eager, lazy, on-signal, disabled).
- Clear failure handling for each activation scenario.

The durable state provides:

- Persistent agent state across host restarts.
- Separation between durable state and disposable projections.

The failure modes provide:

- Clear diagnostics for debugging and monitoring.
- Protection against invalid or malicious inputs.
- Evidence that failures are handled correctly.

The integration tests provide:

- Verification that the canonical flow works end-to-end.
- Evidence that all failure modes are handled correctly.
- Foundation for cross-implementation conformance testing.
