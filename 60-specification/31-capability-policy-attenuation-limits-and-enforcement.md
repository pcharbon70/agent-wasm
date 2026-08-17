---
title: "Capability Policy Attenuation Limits And Enforcement"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-05
  - phase-02
  - capability-policy
  - attenuation
  - limits
  - enforcement
  - credential-use
aliases:
  - "M5-P2 Capability Policy Attenuation Limits And Enforcement"
---

# Capability Policy Attenuation Limits And Enforcement

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-02-capability-policy-attenuation-limits-and-enforcement.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
--
Capabilities, Plugins, Security, And Tenancy.
It establishes host-owned policy decisions that bind every invocation and
effect to minimum authority and resource budgets.

Version `0.2.0` extends the `0.1.0` policy input and attenuation contract with
credential-use context. It explicitly separates an agent's `ModelAccess`
authority from an effect worker's use-only `CredentialUse` authority.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
integration tests and a passing cross-milestone fixture run.

### Milestone acceptance criteria

> **Normative definition.**
Phase 2 MILESTONE ACCEPTANCE requires:

1. **Integration test pass**: 100% of Phase 2 integration tests MUST pass.
2. **Cross-milestone fixture**: A passing cross-milestone fixture run that
   exercises the policy and attenuation system in conjunction with other
   milestone capabilities.
3. **Performance bounds**: Policy evaluation latency and attenuation
   enforcement overhead MUST meet normative bounds defined in the
   conformance profile.
4. **Evidence recording**: All integration test evidence MUST be recorded
   as machine-readable YAML reports in the `50-journal/` directory.
5. **Conformance profile**: The conformance profile MUST document all
   profile selections declared by visible callouts in this chapter.

> **Normative definition.**
Phase 2 FAILS MILESTONE ACCEPTANCE if:
- Any integration test fails, OR
- Normative performance bounds are exceeded, OR
- The conformance profile is incomplete.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md),
[Actions Instructions Validation Plans And Results](11-actions-instructions-validation-plans-and-results.md),
[Extism Invocation Boundary Instances And Output Validation](20-extism-invocation-boundary-instances-and-output-validation.md),
[Mailboxes Ordering Bounds Fairness And Turn Leases](21-mailboxes-ordering-bounds-fairness-and-turn-leases.md),
[Single-Agent Host Flow And Milestone Acceptance](24-single-agent-host-flow-and-milestone-acceptance.md).

## 2.1 Contract And Data Model

### Policy input

> **Normative definition.**
The host MUST assemble a single policy evaluation input from authenticated
principal, tenant, agent, artifact, plugin, purpose, signal, requested
capability, resource, optional credential-use context, policy version, and
runtime context.

> **Normative definition.**

```
PolicyInput {
  principal: Principal,
  tenant_id: TenantId,
  agent_id: AgentId,
  artifact_id: ArtifactId,
  artifact_version: Version,
  plugin_id: PluginId?,
  plugin_version: Version?,
  purpose: Purpose,
  signal: SignalContext,
  capability: Capability,
  resource: Resource,
  credential_use: CredentialUseContext?,
  policy_version: Version,
  runtime_context: RuntimeContext
}

Principal = Defined in
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

TenantId = Defined in
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

AgentId = Defined in
  [Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md).

ArtifactId = Defined in
  [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).

PluginId = string

Purpose = "production" | "development" | "testing"

SignalContext = Defined in
  [Signal Envelopes Causality Routing And Delivery](10-signals-causality-routing-and-delivery.md).

Capability = Defined in
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

Resource = string

CredentialUseContext {
  credential_use_id: string,
  custodian_id: string,
  handle_fingerprint: string,
  operation: string,
  resource: Resource,
  request_digest: string,
  model_binding_id: string?,
  model_binding_revision: u64?,
  connector_binding_id: string?,
  connector_binding_revision: u64?,
  deadline: UnixTimestamp,
  nonce: string,
  budget: JsonObject
}

RuntimeContext {
  turn_id: TurnId,
  turn_step: u64,
  session_id: SessionId?,
  parent_turn_id: TurnId?,
  invocation_id: InvocationId?,
  timestamp: UnixTimestamp
}

TurnId = Defined in
  [Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

SessionId = string

InvocationId = string

UnixTimestamp = Defined in
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

Version = string
```

> **Normative definition.**
The `plugin_id` and `plugin_version` fields are optional and are only set
when the policy evaluation involves a plugin.
The `session_id` and `parent_turn_id` fields are optional and reflect
causal relationships that may affect policy decisions.

> **Normative definition.**
The `credential_use` field MUST be present exactly when `capability` is
`CredentialUse` and MUST be absent for every other capability.
It MUST contain a fingerprint rather than an opaque handle or credential.
For a bound model or connector operation, exactly one matching binding-id and
binding-revision pair MUST be present; model and connector binding pairs MUST
NOT both be populated.
Policy input, decision metadata, caches, and diagnostics MUST NOT contain raw
credentials, authentication headers, credential handles, or transferable
bearer values.

> **Normative definition.**
The host MUST include the `signal` field when the policy evaluation is
triggered by a signal admission.
The host MUST include the `artifact_id` and `artifact_version` fields when
the policy evaluation involves an artifact invocation.
The host MUST include the `plugin_id` and `plugin_version` fields when
the policy evaluation involves a plugin invocation.

> **Non-normative note.**
The `runtime_context` field provides causal information that policy engines
MAY use to make context-aware decisions such as session-scoped limits or
parent-child turn relationships.

### Policy decisions

> **Normative definition.**
The host MUST produce one of the following policy decisions for every policy
evaluation:

1. **allow**: The requested capability is granted without modification.
2. **deny**: The requested capability is denied without exception.
3. **approval-required**: The requested capability requires explicit
   approval before execution.
4. **attenuated**: The requested capability is granted with restrictions.
5. **unavailable**: The requested capability is not available in the current
   context.

> **Normative definition.**

```
PolicyDecision {
  outcome: DecisionOutcome,
  reason: ReasonId,
  attenuation: AttenuationConfig?,
  approval: ApprovalConfig?,
  metadata: JsonObject
}

DecisionOutcome = allow | deny | approval-required | attenuated | unavailable

ReasonId = string

AttenuationConfig = Defined in attenuation section below

ApprovalConfig {
  approver_ids: PrincipalId[],
  approval_deadline: UnixTimestamp?,
  approval_message: string?
}

PrincipalId = string
```

> **Normative definition.**
Each decision outcome MUST be accompanied by a stable `reason` identifier
that identifies the specific policy rule or condition that produced the
decision.

> **Normative definition.**
The `attenuation` field is present only when the outcome is `attenuated`.
The `approval` field is present only when the outcome is `approval-required`.
The `metadata` field is opaque to policy semantics. Consumers MUST NOT require
any metadata member or use metadata to alter the decision outcome, reason,
attenuation, approval, authorization, or tenant-isolation behavior.

> **Normative definition.**
The host MUST NOT execute a requested capability when the decision outcome
is `deny` or `unavailable`.
The host MUST suspend execution when the decision outcome is
`approval-required` until an explicit approval is received or the approval
deadline expires.

> **Non-normative note.**
The `reason` field enables operators to trace policy decisions back to
specific rules or conditions, supporting auditability and debugging without
exposing implementation details.

### Decision reasons

> **Normative definition.**
The host MUST use the following stable reason identifiers:

1. **`grant-absent`**: No grant exists for the requested capability.
2. **`grant-expired`**: The grant has expired.
3. **`grant-revoked`**: The grant has been revoked.
4. **`grant-scoped`**: The grant does not cover the requested resource or purpose.
5. **`tenant-mismatch`**: The tenant does not match the grant scope.
6. **`trust-class-insufficient`**: The trust class does not support the capability.
7. **`artifact-untrusted`**: The artifact is not trusted for the requested capability.
8. **`plugin-untrusted`**: The plugin is not trusted for the requested capability.
9. **`resource-locked`**: The resource is currently locked by another principal.
10. **`rate-limit-exceeded`**: The rate limit for the capability has been exceeded.
11. **`quota-exhausted`**: The resource quota has been exhausted.
12. **`approval-required`**: The capability requires explicit approval.
13. **`capability-disabled`**: The capability is disabled in the current profile.
14. **`capability-unavailable`**: The capability is not available in the current context.
15. **`credential-scope-mismatch`**: The requested operation, resource,
    binding, or budget is outside the credential-use grant.
16. **`credential-export-forbidden`**: The caller requested credential read,
    unwrap, export, or a transferable bearer value.
17. **`credential-custodian-unavailable`**: The selected custodian cannot
    perform the authorized operation.
18. **`credential-replay`**: A nonce or credential-use request was reused.

> **Non-normative note.**
The reason identifiers enable consistent diagnostics across implementations
and allow operators to build automated responses or alerts based on specific
policy failure modes.

### Attenuation

> **Normative definition.**
The host MUST apply attenuation restrictions when the decision outcome is
`attenuated`.
Attenuation MAY restrict the following dimensions:

1. **paths**: Filesystem or network paths accessible to the capability.
2. **origins**: Network origins or endpoints the capability may contact.
3. **methods**: HTTP methods or operation types the capability may use.
4. **models**: Language models the capability may invoke.
5. **tools**: Tools or functions the capability may access.
6. **record sets**: Database or storage record sets the capability may access.
7. **byte counts**: Maximum byte counts for input or output.
8. **durations**: Maximum duration for the capability execution.
9. **invocation budgets**: Maximum number of invocations within a time window.
10. **credential-use scopes**: Custodians, handle fingerprints, operations,
    resources, model or connector bindings, and per-use budgets available to
    an effect worker.

> **Normative definition.**
Attenuation is evaluated at policy evaluation time and is STATIC for the
duration of the invocation.
Runtime policy adjustment based on observed behavior is NOT permitted for
baseline conformance.
Conformance profiles MAY define mechanisms for policy re-evaluation triggered
by specific events (e.g., resource threshold crossing).

> **Normative definition.**
When multiple attenuation dimensions conflict, the DENY outcome takes precedence.
If any dimension denies an action, the entire action is denied regardless of
other dimensions allowing it.
Conformance profiles MAY define priority between dimension types for
diagnostic purposes, but the normative behavior is deny-on-conflict.

> **Normative definition.**
Approval deadlines MUST be bounded by the turn timeout.
If an approval deadline exceeds the turn timeout, the turn MUST timeout
before approval is received.
The host MUST reject approval configurations where the deadline exceeds the
turn timeout with the diagnostic `policy.approval-deadline-exceeds-turn-timeout`.

> **Normative definition.**
Approval workflows MAY be nested with a maximum depth of 3 levels for
baseline conformance.
Nested approvals deeper than 3 levels MUST be rejected with the diagnostic
`policy.approval-nesting-depth-exceeded`.
Conformance profiles MAY allow deeper nesting for specific deployment models.

### Policy Evaluation

> **Normative definition.**
Policy evaluations at independent boundaries MUST be executed sequentially
for baseline conformance.
Parallel policy evaluation is NOT permitted for baseline conformance.
Conformance profiles MAY define conditions under which parallel evaluation is
permitted, provided consistency guarantees are preserved.

### Policy Audit

> **Normative definition.**
Policy decisions MUST be auditable by a compliance audit role.
The compliance audit role has read-only access to policy decision logs and
MUST NOT have authority to modify or delete audit records.
Conformance profiles MAY define additional audit roles or access controls.

### Rule Versioning

> **Normative definition.**
Policy rules CANNOT be versioned independently.
Policies are versioned as a whole through the policy versioning mechanism
defined in this chapter.
Rule-level versioning is NOT supported for baseline conformance.
Conformance profiles MAY define bundle-level versioning as an extension.

### Attenuation Overhead Measurement

> **Normative definition.**
Policy evaluation latency is the elapsed monotonic-clock time, in microseconds,
from admission of a complete validated `PolicyInput` to availability of its
`PolicyDecision`. Attenuation enforcement overhead is the elapsed
monotonic-clock time, in microseconds, spent validating and applying all
populated `AttenuationConfig` restrictions before capability execution; it
excludes the capability's own execution time.
Clock implementation, sampling, and aggregation are internal mechanisms. They
MUST preserve these start and end boundaries, MUST NOT alter policy outcomes or
execution order, and MUST report clock resolution with the measurements.
Attenuation evidence MUST also report the number of populated restrictions, but
MUST NOT divide the elapsed duration into an invented per-restriction latency.
The conformance profile MUST publish latency ceilings for both metrics.

> **Normative definition.**

```
AttenuationConfig {
  paths: PathRestriction?,
  origins: OriginRestriction?,
  methods: MethodRestriction?,
  models: ModelRestriction?,
  tools: ToolRestriction?,
  record_sets: RecordSetRestriction?,
  byte_counts: ByteCountRestriction?,
  durations: DurationRestriction?,
  invocation_budgets: InvocationBudgetRestriction?,
  credential_use: CredentialUseRestriction?
}

PathRestriction {
  allowed_prefixes: string[],
  denied_prefixes: string[]
}

OriginRestriction {
  allowed_origins: string[],
  denied_origins: string[]
}

MethodRestriction {
  allowed_methods: string[]
}

ModelRestriction {
  allowed_models: string[]
}

ToolRestriction {
  allowed_tools: string[]
}

RecordSetRestriction {
  allowed_record_sets: string[]
}

ByteCountRestriction {
  max_input_bytes: u64,
  max_output_bytes: u64
}

DurationRestriction {
  max_duration_ms: u64
}

InvocationBudgetRestriction {
  max_invocations: u64,
  window_duration_ms: u64
}

CredentialUseRestriction {
  allowed_custodians: string[],
  allowed_handle_fingerprints: string[],
  allowed_operations: string[],
  allowed_resources: string[],
  allowed_model_bindings: string[],
  allowed_connector_bindings: string[],
  max_cost_per_use: u64?
}
```

> **Normative definition.**
When multiple attenuation dimensions are specified, the host MUST apply
ALL restrictions.
A capability MUST satisfy all applied restrictions to execute.

> **Normative definition.**
The `paths` restriction applies to filesystem and network path access.
The `allowed_prefixes` field specifies path prefixes the capability MAY access.
The `denied_prefixes` field specifies path prefixes the capability MUST NOT access.
When both fields are present, `denied_prefixes` takes precedence over
`allowed_prefixes`.

> **Normative definition.**
The `origins` restriction applies to network endpoints the capability MAY contact.
The `allowed_origins` field specifies origin patterns the capability MAY contact.
The `denied_origins` field specifies origin patterns the capability MUST NOT contact.
When both fields are present, `denied_origins` takes precedence over
`allowed_origins`.

> **Normative definition.**
The `byte_counts` restriction applies to input and output size limits.
The `max_input_bytes` field specifies the maximum bytes the capability MAY receive.
The `max_output_bytes` field specifies the maximum bytes the capability MAY produce.
Exceeding either limit MUST cause the capability execution to fail with
a `byte-count-exceeded` diagnostic.

> **Normative definition.**
The `durations` restriction applies to execution time limits.
The `max_duration_ms` field specifies the maximum milliseconds the capability MAY run.
Exceeding this limit MUST cause the capability execution to fail with
a `duration-exceeded` diagnostic.

> **Normative definition.**
The `invocation_budgets` restriction applies to invocation frequency limits.
The `max_invocations` field specifies the maximum number of invocations within the time window.
The `window_duration_ms` field specifies the time window in milliseconds.
Exceeding this budget MUST cause the capability execution to fail with
a `budget-exceeded` diagnostic.

> **Normative definition.**
The `credential_use` restriction applies only to `CredentialUse` decisions.
The requested custodian, handle fingerprint, operation, resource, model
or connector binding, and cost MUST satisfy every populated allowlist or
limit.
The host MUST deny on any mismatch and MUST NOT broaden a restriction by
falling back to another custodian, handle, connection, provider, or model.

> **Non-normative note.**
Attenuation enables fine-grained resource control without completely denying
capabilities.
For example, a capability MAY be allowed to access a specific directory
structure but restricted to a maximum of 1 MB of output bytes.

> **Non-normative note.**
The precedence rules for `denied_prefixes` over `allowed_prefixes` and
`denied_origins` over `allowed_origins` ensure that explicit denials always
override broader allowances, supporting the principle of least privilege.

### Policy evaluation flow

> **Normative definition.**
The host MUST evaluate policy at the following boundaries:

1. **Signal admission**: Before a signal enters the turn lifecycle.
2. **Action resolution**: Before an action is resolved to an instruction.
3. **Guest invocation**: Before a guest export is invoked.
4. **Directive validation**: Before a directive is validated for execution.
5. **Effect dispatch**: Before an effect is dispatched to a handler.
6. **Result admission**: Before a result is admitted to the turn.

For an authenticated external effect, the host MUST evaluate the originating
agent's domain capability and the effect worker's `CredentialUse` capability
as two separate decisions. A cached `ModelAccess` or `Effects` decision MUST
NOT satisfy the credential-use boundary.

> **Normative definition.**
The host MUST cache policy decisions when the policy input is unchanged.
The host MUST invalidate cached decisions when:

1. The policy version changes.
2. The grant is revoked or expired.
3. The principal's trust class changes.
4. The tenant's policy profile changes.
5. A revocation signal is received.

> **Normative definition.**
The host MUST NOT use cached decisions across different policy versions.
The host MUST re-evaluate policy when any field of the `PolicyInput`
changes.

> **Non-normative note.**
Caching policy decisions improves performance for repeated invocations with
identical context, such as within a single turn or session.
However, the host MUST ensure that cached decisions are invalidated when
the underlying policy state changes.

### Revocation and policy versioning

> **Normative definition.**
The host MUST support the following revocation mechanisms:

1. **Grant revocation**: A grant is explicitly revoked by the granting
   principal or an operator.
2. **Policy version change**: The active policy version is updated.
3. **Trust class change**: A principal's trust class is updated.
4. **Tenant policy profile change**: The tenant's policy profile is updated.

> **Normative definition.**
When a revocation occurs, the host MUST invalidate all cached policy
decisions that depend on the revoked or changed state.
The host MUST NOT allow new invocations using invalidated decisions.
In-flight invocations MUST be allowed to complete or be rolled back.

> **Normative definition.**
The host MUST track policy versions and include the current policy version
in the `PolicyInput`.
The host MUST reject policy evaluations when the policy version in the
`PolicyInput` does not match the current active policy version.

> **Non-normative note.**
Revocation and policy versioning ensure that policy changes take effect
immediately for new invocations while allowing in-flight operations to
complete safely.
This prevents policy gaps where outdated decisions could allow unauthorized
actions.

## 2.2 Behavior And Integration

### Policy evaluation integration with turn lifecycle

> **Normative definition.**
The host MUST integrate policy evaluation into the turn lifecycle as follows:

1. **Signal admission**: The host MUST evaluate policy before admitting a signal
   to the turn. If the policy decision is `deny` or `unavailable`, the signal
   MUST be rejected with the `reason` from the policy decision.
2. **Action resolution**: The host MUST evaluate policy before resolving an action
   to an instruction. If the policy decision is `deny` or `unavailable`, the action
   MUST be rejected with the `reason` from the policy decision.
3. **Guest invocation**: The host MUST evaluate policy before invoking a guest export.
   If the policy decision is `deny` or `unavailable`, the invocation MUST be skipped
   with the `reason` from the policy decision.
4. **Directive validation**: The host MUST evaluate policy before validating a directive.
   If the policy decision is `deny` or `unavailable`, the directive MUST be rejected
   with the `reason` from the policy decision.
5. **Effect dispatch**: The host MUST evaluate policy before dispatching an effect.
   If the policy decision is `deny` or `unavailable`, the effect MUST be rejected
   with the `reason` from the policy decision.
6. **Result admission**: The host MUST evaluate policy before admitting a result.
   If the policy decision is `deny` or `unavailable`, the result MUST be rejected
   with the `reason` from the policy decision.

> **Non-normative note.**
Policy evaluation at multiple boundaries ensures that capabilities are
continuously enforced throughout the turn lifecycle, not just at the initial
invocation.
This prevents scenarios where a capability is granted at one boundary but
used in an unauthorized way at a later boundary.

### Attenuation enforcement

> **Normative definition.**
The host MUST enforce attenuation restrictions at runtime.
When a capability is attenuated, the host MUST apply ALL restrictions from
the `AttenuationConfig` during execution.

> **Normative definition.**
The host MUST monitor capability execution for attenuation violations.
When a violation is detected, the host MUST:

1. Stop the capability execution.
2. Emit a diagnostic with the `reason` set to the specific violation
   (e.g., `byte-count-exceeded`, `duration-exceeded`, `budget-exceeded`).
3. Roll back any side effects of the capability execution.
4. Record the violation in the audit log.

> **Non-normative note.**
Runtime enforcement of attenuation ensures that capabilities cannot exceed
their granted boundaries, even if the initial policy decision allowed them
with restrictions.
This is critical for preventing resource exhaustion, data leakage, or
unauthorized access.

### Approval workflow

> **Normative definition.**
The host MUST implement the following approval workflow when the policy
decision outcome is `approval-required`:

1. **Suspend execution**: The host MUST suspend the capability execution
   and wait for an approval decision.
2. **Notify approvers**: The host MUST notify all approvers listed in the
   `ApprovalConfig`.
3. **Wait for approval**: The host MUST wait for an approval decision from
   at least one approver or until the approval deadline expires.
4. **Resume or deny**: If an approver grants approval, the host MUST resume
   the capability execution. If the approval deadline expires without approval,
   the host MUST deny the capability execution with the `reason` set to
   `approval-deadline-exceeded`.

> **Non-normative note.**
The approval workflow enables human-in-the-loop authorization for high-risk
capabilities, such as financial transactions or data deletion.
The `approval_deadline` field ensures that approvals do not hang indefinitely,
preventing operational deadlocks.

## 2.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for capability policy
attenuation limits and enforcement:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current policy version.
3. **Conflicting**: Multiple policy rules produce conflicting decisions.
4. **Unauthorized**: The caller does not have permission to evaluate policy.
5. **Exhausted**: The policy engine is out of resources (e.g., memory, budget).
6. **Unavailable**: The policy engine is unavailable.
7. **Approval deadline exceeded**: The approval deadline expired without approval.
8. **Attenuation violation**: A runtime attenuation restriction was violated.
9. **Policy version mismatch**: The policy version in the input does not match
   the current active version.
10. **Credential scope mismatch**: A credential-use request exceeds its
    attenuated scope.
11. **Credential export attempt**: A request attempts to reveal or convert
    credential material.
12. **Credential custodian unavailable**: The selected custodian cannot serve
    the request.
13. **Credential replay**: A credential-use nonce or request is reused.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for capability policy
attenuation limits and enforcement:

| Error Code | Description |
|------------|-------------|
| `policy.malformed_input` | Input data does not conform to the expected schema |
| `policy.incompatible_version` | Data is incompatible with the current policy version |
| `policy.conflicting_rules` | Multiple policy rules produce conflicting decisions |
| `policy.unauthorized` | The caller does not have permission to evaluate policy |
| `policy.exhausted` | The policy engine is out of resources |
| `policy.unavailable` | The policy engine is unavailable |
| `policy.approval_deadline_exceeded` | The approval deadline expired without approval |
| `policy.attenuation_violation` | A runtime attenuation restriction was violated |
| `policy.policy_version_mismatch` | The policy version in the input does not match the current active version |
| `policy.grant_absent` | No grant exists for the requested capability (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.grant_expired` | The grant has expired (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.grant_revoked` | The grant has been revoked (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.grant_scoped` | The grant does not cover the requested resource or purpose (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.tenant_mismatch` | The tenant does not match the grant scope (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.trust_class_insufficient` | The trust class does not support the capability (see
  [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)) |
| `policy.artifact_untrusted` | The artifact is not trusted for the requested capability |
| `policy.plugin_untrusted` | The plugin is not trusted for the requested capability |
| `policy.resource_locked` | The resource is currently locked by another principal |
| `policy.rate_limit_exceeded` | The rate limit for the capability has been exceeded |
| `policy.quota_exhausted` | The resource quota has been exhausted |
| `policy.capability_disabled` | The capability is disabled in the current profile |
| `policy.capability_unavailable` | The capability is not available in the current context |
| `policy.byte_count_exceeded` | The byte count restriction was exceeded |
| `policy.duration_exceeded` | The duration restriction was exceeded |
| `policy.budget_exceeded` | The invocation budget was exceeded |
| `policy.credential_scope_mismatch` | Credential use exceeds an allowed custodian, handle, operation, resource, model or connector binding, or budget |
| `policy.credential_export_forbidden` | Credential read, unwrap, export, or bearer conversion was requested |
| `policy.credential_custodian_unavailable` | The selected credential custodian is unavailable |
| `policy.credential_replay` | A credential-use nonce or request was reused |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome using exactly
the Chapter 04 `Diagnostic` top-level structure. The domain error is `code`,
`severity` is `error`, and `details` contains `phase`, `contract`, `profile`,
`failed_boundary`, `context`, `entity_identifiers`, `timestamp`, and
`retryable`.

| Family | Domain codes |
|--------|--------------|
| `identity.validation.capability_policy` | `policy.malformed_input`, `policy.attenuation_violation`, `policy.credential_scope_mismatch`, `policy.credential_export_forbidden` |
| `identity.compatibility.capability_policy` | `policy.incompatible_version`, `policy.policy_version_mismatch`, `policy.capability_disabled` |
| `identity.authorization.capability_policy` | `policy.unauthorized`, `policy.grant_absent`, `policy.grant_expired`, `policy.grant_revoked`, `policy.grant_scoped`, `policy.tenant_mismatch`, `policy.trust_class_insufficient`, `policy.artifact_untrusted`, `policy.plugin_untrusted` |
| `identity.conflict.capability_policy` | `policy.conflicting_rules`, `policy.resource_locked`, `policy.credential_replay` |
| `identity.limit.capability_policy` | `policy.exhausted`, `policy.approval_deadline_exceeded`, `policy.rate_limit_exceeded`, `policy.quota_exhausted`, `policy.byte_count_exceeded`, `policy.duration_exceeded`, `policy.budget_exceeded` |
| `identity.resource.capability_policy` | `policy.unavailable`, `policy.capability_unavailable`, `policy.credential_custodian_unavailable` |

No additional top-level diagnostic member is permitted.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:
Each selection is one of the alternatives or bounded domains stated below.
Observable approval-notification channels, policy-limit rejections, and
retained audit-history availability may differ according to the recorded
selections; policy decisions for the same inputs MUST NOT differ.

1. **Policy engine**: The policy engine implementation (e.g., OPA, custom).

2. **Grant storage**: The grant storage implementation (in-memory, database, etc.).

3. **Policy caching**: The policy decision caching strategy.
   Baseline conformance REQUIRES cache invalidation on policy changes.
   Cached policy decisions MUST be invalidated when the policy version changes.
   Implementations MAY cache policy decisions for repeated inputs with the same
   context, provided cache invalidation is triggered on policy changes.

4. **Audit log retention**: The audit log retention policy.
   Baseline conformance REQUIRES normative minimum retention periods aligned with
   common regulations (e.g., GDPR, SOC2).

5. **Approval notification mechanism**: The mechanism used to notify approvers
   (e.g., email, webhook, in-app notification).

6. **Attenuation enforcement mechanism**: The mechanism used to enforce
   attenuation restrictions at runtime (e.g., proxy, wrapper, native enforcement).

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Dynamic policy adaptation**: Runtime policy adjustment based on behavior.
2. **Policy simulation**: Simulating policy decisions before applying them.
3. **Policy versioning automation**: Automated policy versioning and deployment.
4. **Policy analytics**: Policy usage and effectiveness analytics.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 2 MAY invalidate earlier milestone assumptions:

1. **Policy evaluation latency**: If policy evaluation latency exceeds the turn
   timeout, the timeout or policy caching strategy MUST be revised.
2. **Grant storage capacity**: If the grant storage exceeds the capacity planned
   in earlier milestones, the capacity plan MUST be revised.
3. **Audit log size**: If the audit log size exceeds the capacity planned in
   earlier milestones, the capacity plan MUST be revised.

> **Non-normative note.**
If any result from Phase 2 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## 2.4 Phase 2 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 2 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host evaluates policy, grants capabilities,
   applies attenuation, and enforces limits successfully.
2. **Performance**: Policy evaluation latency and attenuation enforcement
   overhead meet normative latency bounds defined in the conformance profile.
3. **Failure handling**: The host handles malformed, incompatible, stale,
   duplicate, and boundary-limit inputs correctly.
4. **Security enforcement**: The host enforces policy decisions, attenuation
   restrictions, and limits without leaving unauthorized state.
5. **Cross-milestone compatibility**: The phase does not introduce regressions
   in earlier milestones.

### Test evidence recording

> **Normative definition.**
Phase 2 integration test evidence MUST be recorded as machine-readable YAML
reports in the `50-journal/` directory.
Each report MUST include:
- Test name and identifier
- Input data
- Expected output
- Actual output
- Pass/fail status
- Timestamp
- Policy-evaluation latency and total attenuation-enforcement overhead where
  applicable
- Monotonic-clock resolution and populated-restriction count for each
  attenuation measurement

### Test execution

> **Normative definition.**
Integration tests MAY be run in parallel if each test has isolated state.
Tests that share state MUST be run sequentially.
Conformance profiles MUST document which tests can be run in parallel and
which require sequential execution.

### Normative latency bounds

> **Normative definition.**
The conformance profile MUST define normative latency bounds for:
- Policy evaluation latency (microseconds per evaluation).
- Total attenuation enforcement overhead (microseconds per evaluation across
  all populated restrictions).

Tests MUST verify that implementations meet these bounds under representative
workloads and MUST verify the exact start and end boundaries, reported clock
resolution, and populated-restriction count defined in
[Attenuation Overhead Measurement](#attenuation-overhead-measurement).

> **Normative definition.**
Each integration test MUST exercise observable contracts rather than private
implementation structure.

### Successful flow tests

> **Normative definition.**
The following tests MUST verify the canonical successful flow:

1. **Policy evaluation**: Evaluate a policy input and verify the decision is
   `allow` or `attenuated`.
2. **Attenuation enforcement**: Apply attenuation restrictions and verify the
   capability executes within the granted boundaries.
3. **Approval workflow**: Trigger an `approval-required` decision and verify
   the approval workflow suspends execution until approval is received.
4. **Policy caching**: Verify that policy decisions are cached and invalidated
   when the policy input changes.
5. **Revocation**: Revoke a grant and verify that cached policy decisions are
   invalidated and new invocations are denied.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Malformed input**: Attempt to evaluate a malformed policy input and verify
   the `policy.malformed_input` error code.
2. **Grant absence**: Attempt to evaluate a policy input without a valid grant and
   verify the `policy.grant_absent` error code.
3. **Grant expiry**: Attempt to evaluate a policy input with an expired grant and
   verify the `policy.grant_expired` error code.
4. **Grant revocation**: Attempt to evaluate a policy input with a revoked grant and
   verify the `policy.grant_revoked` error code.
5. **Trust class insufficient**: Attempt to evaluate a policy input with an
   insufficient trust class and verify the `policy.trust_class_insufficient` error code.
6. **Artifact untrusted**: Attempt to evaluate a policy input with an untrusted
   artifact and verify the `policy.artifact_untrusted` error code.
7. **Byte count exceeded**: Attempt to execute an attenuated capability that exceeds
   the byte count restriction and verify the `policy.byte_count_exceeded` error code.
8. **Duration exceeded**: Attempt to execute an attenuated capability that exceeds
   the duration restriction and verify the `policy.duration_exceeded` error code.
9. **Budget exceeded**: Attempt to execute an attenuated capability that exceeds
   the invocation budget and verify the `policy.budget_exceeded` error code.
10. **Approval deadline exceeded**: Trigger an `approval-required` decision and wait
    for the approval deadline to expire without approval, verifying the
    `policy.approval_deadline_exceeded` error code.
11. **Credential scope mismatch**: Change the model or connector binding,
    resource, or budget after authorization and verify
    `policy.credential_scope_mismatch`.
12. **Credential export forbidden**: Request credential read or export with a
    valid `CredentialUse` grant and verify
    `policy.credential_export_forbidden`.
13. **Credential replay**: Reuse a previously accepted nonce and verify
    `policy.credential_replay`.

> **Normative definition.**
Each test MUST verify the exact Chapter 04 diagnostic shape, assigned family,
domain `code`, `severity: "error"`, message, and required bounded details.

### Security enforcement tests

> **Normative definition.**
The following tests MUST verify security enforcement:

1. **Tenant isolation**: Verify that a tenant cannot access another tenant's data
   through policy decisions.
2. **Attenuation enforcement**: Verify that attenuated capabilities execute within
   their granted boundaries.
3. **Policy versioning**: Verify that policy decisions are invalidated when the
   policy version changes.
4. **Revocation**: Verify that revoked grants prevent new invocations.
5. **Audit logging**: Verify that all policy decisions and violations are logged.
6. **Dual authorization**: Verify that agent `ModelAccess` does not satisfy
   effect-worker `CredentialUse`, and that neither decision exposes a handle or
   credential in policy input, caches, diagnostics, or audit evidence.

> **Normative definition.**
Each test MUST verify that no unauthorized or partial state is left after the
test.

### Cross-milestone compatibility tests

> **Normative definition.**
The following tests MUST verify cross-milestone compatibility:

1. **Milestone 1 fixtures**: Run all Milestone 1 fixtures and verify no
   regressions. Milestone 1 fixtures are defined in
   [Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md).
2. **Milestone 2 fixtures**: Run all Milestone 2 fixtures and verify no
   regressions.
3. **Milestone 3 fixtures**: Run all Milestone 3 fixtures and verify no
   regressions.
4. **Milestone 4 fixtures**: Run all Milestone 4 fixtures and verify no
   regressions.

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 2 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Policy evaluation evidence**: Evidence that policy evaluations produce correct
   decisions.
3. **Attenuation enforcement evidence**: Evidence that attenuated capabilities execute
   within their granted boundaries.
4. **Approval workflow evidence**: Evidence that the approval workflow suspends
   execution until approval is received.
5. **Policy caching evidence**: Evidence that policy decisions are cached and
   invalidated correctly.
6. **Revocation evidence**: Evidence that revoked grants prevent new invocations.
7. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.
8. **Audit log evidence**: Evidence that all policy decisions and violations are
   logged.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.

## Variability register

The register below indexes profile selections and other variability governed by
the linked clauses. It does not independently license variation.

> **Non-normative note.**

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| [Policy engine](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must support policy input, decisions, and attenuation |
| [Grant storage](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must support grant dimensions and revocation |
| [Policy caching](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must invalidate on policy version change or revocation |
| [Audit log retention](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must preserve audit trail |
| [Approval notification](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must notify all approvers and respect deadlines |
| [Attenuation enforcement](#implementation-defined-choices) | Implementation-defined | Document in conformance profile | Must enforce all restrictions at runtime |
| [Latency and overhead measurement](#attenuation-overhead-measurement) | Required | Monotonic microseconds over fixed boundaries | Publish clock resolution and latency ceilings |
| [Tenant isolation](#policy-evaluation-flow) | Required | Preserve tenant-qualified policy evaluation | Must prevent cross-tenant access |
| [Policy versioning](#revocation-and-policy-versioning) | Required | Track and validate the active policy version | Must invalidate cached decisions on version change |
| [Credential-use attenuation](#attenuation) | Required | Enforce custodian, handle fingerprint, operation, resource, binding, nonce, and budget restrictions | Must deny on mismatch and must not expose credentials or handles |
| [Domain and credential authorization](#policy-evaluation-flow) | Required | Evaluate as independent policy decisions | `ModelAccess` or `Effects` must not imply `CredentialUse` |
