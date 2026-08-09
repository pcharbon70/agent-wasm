---
title: "Effect Handlers Attempts Idempotency And Result Signals"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-04
  - phase-03
  - durable-state
  - effect-handler
  - attempt
  - idempotency
  - result-signal
aliases:
  - "M4-P3 Effect Handlers Attempts Idempotency And Result Signals"
---

# Effect Handlers Attempts Idempotency And Result Signals

## Status and authority

This chapter is a draft specification produced by
[Phase 3](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/phase-03-effect-handlers-attempts-idempotency-and-result-signals.md)
of
[Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/README.md)
--
Durable State, Effects, And Recovery.
It interprets committed directives through typed handlers while retaining every
attempt and returning results as new signals.

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
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md),
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md),
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Agent Registry Activation Cancellation And Completion](22-agent-registry-activation-cancellation-and-completion.md),
[Sensors Schedules Timers And External Signal Ingress](23-sensors-schedules-timers-and-external-signal-ingress.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md),
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md).

## 3.1 Contract And Data Model

### Effect handler registration

> **Normative definition.**
An effect handler is a typed component that interprets a specific directive kind
and dispatches to an external target.
The host MUST register effect handlers by directive kind, schema version, trust
class, capability, and retry policy.

> **Normative definition.**

```
EffectHandlerRegistration {
  handler_id: HandlerId,
  directive_kind: DirectiveKindName,
  schema_version: string,
  trust_class: TrustClass,
  capability: HandlerCapability,
  retry_policy: RetryPolicy
}

HandlerId = string
DirectiveKindName = "emit" | "timer" | "effect" | "child-lifecycle" | "approval" | "topology"
TrustClass = Untrusted | Confined | Privileged
HandlerCapability {
  effects: Set<EffectKind>,
  signals: Set<SignalKind>,
  timers: Set<TimerKind>,
  child_lifecycle: ChildLifecyclePermission
}
ChildLifecyclePermission = None | Suspend | Cancel | Terminate
```

`DirectiveKindName` is defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `handler_id` | HandlerId | Yes | Unique handler identifier |
| `directive_kind` | DirectiveKindName | Yes | Directive kind this handler interprets |
| `schema_version` | string | Yes | Schema version for payload validation |
| `trust_class` | TrustClass | Yes | Trust class for the handler |
| `capability` | HandlerCapability | Yes | Capabilities granted to the handler |
| `retry_policy` | RetryPolicy | Yes | Retry policy for this handler |

> **Normative definition.**
The `trust_class` field determines the handler's trust level:
- **Untrusted**: Handler runs in a sandbox with no external access.
- **Confined**: Handler runs in a sandbox with limited external access.
- **Privileged**: Handler runs with full external access.

> **Normative definition.**
The `capability` field determines what the handler can do:
- `effects`: Set of effect kinds the handler can dispatch.
- `signals`: Set of signal kinds the handler can emit.
- `timers`: Set of timer kinds the handler can create.
- `child_lifecycle`: Permission to suspend, cancel, or terminate child agents.

> **Normative definition.**
The host MUST validate the handler's trust class and capability against the
agent's manifest before dispatching.
If the handler exceeds its trust class or capability, the host MUST reject the
dispatch with `handler.trust_violation`.

### Effect attempt

> **Normative definition.**
An effect attempt is a durable record of a single dispatch attempt for an
effect handler.
The host MUST retain every attempt for audit purposes.

> **Normative definition.**

```
EffectAttempt {
  attempt_id: AttemptId,
  tenant_id: TenantId,
  agent_id: AgentId,
  outbox_entry_id: EntryId,
  directive_id: DirectiveId,
  handler_id: HandlerId,
  lease: AttemptLease,
  handler_version: string,
  request_hash: Bytes,
  created_at: UnixTimestamp,
  dispatched_at: UnixTimestamp?,
  completed_at: UnixTimestamp?,
  outcome: AttemptOutcome,
  external_reference: String?,
  metadata: JsonObject
}

AttemptId = string
AttemptLease {
  lease_id: String,
  acquired_at: UnixTimestamp,
  expires_at: UnixTimestamp
}
AttemptOutcome {
  status: AttemptStatus,
  result: AttemptResult?
}
AttemptStatus = Pending | Dispatched | Completed | Failed | Cancelled
AttemptResult {
  status: DispatchStatus,
  response_hash: Bytes?,
  diagnostics: Diagnostics?
}
DispatchStatus = Success | DomainFailure | InfrastructureFailure | Timeout
Diagnostics {
  kind: DiagnosticsKind,
  message: String,
  code: String
}
DiagnosticsKind = Internal | External
```

`EntryId` is defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
`DirectiveId` is defined in
[Directives Strategies Continuations And Terminal States](13-directives-strategies-continuations-and-terminal-states.md).
`TenantId` and `AgentId` are defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `attempt_id` | AttemptId | Yes | Unique attempt identifier |
| `tenant_id` | TenantId | Yes | Tenant this attempt belongs to |
| `agent_id` | AgentId | Yes | Agent this attempt belongs to |
| `outbox_entry_id` | EntryId | Yes | Outbox entry this attempt is for |
| `directive_id` | DirectiveId | Yes | Directive this attempt is for |
| `handler_id` | HandlerId | Yes | Handler this attempt is dispatched to |
| `lease` | AttemptLease | Yes | Lease for this attempt |
| `handler_version` | string | Yes | Handler version used for this attempt |
| `request_hash` | Bytes | Yes | Hash of the dispatch request |
| `created_at` | UnixTimestamp | Yes | Attempt creation time |
| `dispatched_at` | UnixTimestamp? | No | Dispatch time (null if not yet dispatched) |
| `completed_at` | UnixTimestamp? | No | Completion time (null if not yet completed) |
| `outcome` | AttemptOutcome | Yes | Attempt outcome |
| `external_reference` | String? | No | External provider reference (if any) |
| `metadata` | JsonObject | Yes | Additional metadata |

> **Normative definition.**
The `lease` field is used to prevent concurrent dispatch of the same attempt.
The host MUST acquire a lease before dispatching an attempt.
If the lease expires, the host MUST mark the attempt as `Failed` with
`attempt.lease_expired` and MUST NOT dispatch it again until a new lease is
acquired.

> **Normative definition.**
The `request_hash` field is a hash of the dispatch request (e.g., SHA-256).
The host MUST compute the request hash before dispatching the attempt.
The host MUST verify the request hash on every retry to prevent request
mutation.

> **Normative definition.**
The `external_reference` field is set by the external provider when the
dispatch succeeds.
The host MUST store the external reference for audit purposes.

### Stable idempotency keys

> **Normative definition.**
The host MUST support stable idempotency keys to prevent duplicate dispatch
to external providers.
Idempotency keys are separate from attempt and external provider identities.

> **Normative definition.**

```
IdempotencyKey {
  key: String,
  scope: IdempotencyScope,
  expires_at: UnixTimestamp?
}

IdempotencyScope = Tenant | Agent | Directive | Global
```

> **Normative definition.**
The `scope` field determines the scope of the idempotency key:
- **Tenant**: The key is unique per tenant.
- **Agent**: The key is unique per agent within a tenant.
- **Directive**: The key is unique per directive within an agent.
- **Global**: The key is unique across all tenants and agents.

> **Normative definition.**
The host MUST check the idempotency key before dispatching an attempt.
If the key has already been used, the host MUST return the previous result
without dispatching again.
If the key has expired, the host MUST reject the attempt with
`handler.idempotency_key_expired`.

> **Normative definition.**
The host MUST NOT use the `attempt_id` or `external_reference` as the
idempotency key.
The idempotency key is determined by the directive payload and MUST be
deterministic for the same payload.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Handler registry implementation | Implementation-defined | Document in conformance profile | Must support hot-reload |
| Retry policy defaults | Implementation-defined | Document in conformance profile | Must not exceed turn timeout |
| Idempotency key scope | Implementation-defined | Document in conformance profile | Must support tenant/agent/directive/global |
| Response size limit | Implementation-defined | Document in conformance profile | Must be bounded |
| Duration limit | Implementation-defined | Document in conformance profile | Must be bounded |
| Handler trust classes | Implementation-defined | Document in conformance profile | Must enforce trust boundaries |

