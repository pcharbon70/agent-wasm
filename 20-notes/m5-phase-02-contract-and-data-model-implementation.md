---
title: "Phase 2 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-02
  - implementation
  - contract-and-data-model
  - capability-policy
  - attenuation
  - limits
  - enforcement
aliases:
  - "M5-P2-2.1 Implementation"
---

# Phase 2 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 2.1 (Contract And Data Model) from
[Phase 2 - Capability Policy Attenuation Limits And Enforcement](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-02-capability-policy-attenuation-limits-and-enforcement.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[31-capability-policy-attenuation-limits-and-enforcement.md](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
which establishes host-owned policy decisions that bind every invocation and
effect to minimum authority and resource budgets.

## Subtask 2.1.1.1: Define policy input

### Implementation

Defined the `PolicyInput` structure that the host assembles from authenticated
principal, tenant, agent, artifact, plugin, purpose, signal, requested
capability, resource, and runtime context:

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
  runtime_context: RuntimeContext
}

RuntimeContext {
  turn_id: TurnId,
  turn_step: u64,
  session_id: SessionId?,
  parent_turn_id: TurnId?,
  invocation_id: InvocationId?,
  timestamp: UnixTimestamp
}
```

Required fields depend on context:
- `signal` is required when policy evaluation is triggered by signal admission
- `artifact_id` and `artifact_version` are required when policy evaluation involves artifact invocation
- `plugin_id` and `plugin_version` are required when policy evaluation involves plugin invocation

### Design decisions

1. **Policy input is context-aware**: The `runtime_context` field provides
   causal information (turn_id, session_id, parent_turn_id) that policy
   engines can use to make context-aware decisions such as session-scoped
   limits or parent-child turn relationships.

2. **Optional fields are conditional, not nullable**: The `plugin_id`,
   `plugin_version`, `session_id`, and `parent_turn_id` fields are only
   present when relevant. This avoids sending empty context that could
   confuse policy engines.

3. **Types are referenced from earlier milestones**: Principal, TenantId,
   AgentId, ArtifactId, TurnId, and other types are defined in chapters
   from Milestones 1-4. This ensures consistency and avoids duplication.

## Subtask 2.1.1.2: Define policy decisions

### Implementation

Defined five policy decision outcomes and their corresponding structures:

| Outcome | Description | Associated Config |
|---------|-------------|------------------|
| allow | Capability granted without modification | None |
| deny | Capability denied without exception | None |
| approval-required | Capability requires explicit approval | ApprovalConfig |
| attenuated | Capability granted with restrictions | AttenuationConfig |
| unavailable | Capability not available in current context | None |

Each decision includes:
- `outcome`: One of the five outcomes above
- `reason`: Stable reason identifier (e.g., `grant-absent`, `tenant-mismatch`)
- `attenuation`: Present only for `attenuated` decisions
- `approval`: Present only for `approval-required` decisions

Fourteen stable reason identifiers are defined:
`grant-absent`, `grant-expired`, `grant-revoked`, `grant-scoped`,
`tenant-mismatch`, `trust-class-insufficient`, `artifact-untrusted`,
`plugin-untrusted`, `resource-locked`, `rate-limit-exceeded`,
`quota-exhausted`, `approval-required`, `capability-disabled`,
`capability-unavailable`.

### Design decisions

1. **Reason identifiers enable auditability**: Each decision is accompanied
   by a stable `reason` identifier that traces back to the specific policy
   rule or condition. This supports debugging and automated alerting.

2. **Attenuation and approval are separate config structures**: This keeps
   the decision schema clean and ensures that only relevant configuration
   is present for each outcome.

3. **Deny and unavailable are absolute**: The host MUST NOT execute a
   capability when the decision is `deny` or `unavailable`. This is
   stronger than attenuation, which allows execution with restrictions.

## Subtask 2.1.1.3: Define attenuation

### Implementation

Defined nine attenuation dimensions with corresponding restriction structures:

| Dimension | Restriction Type | Enforcement |
|-----------|-----------------|-------------|
| paths | PathRestriction (allowed/denied prefixes) | Filesystem and network path access |
| origins | OriginRestriction (allowed/denied origins) | Network endpoint access |
| methods | MethodRestriction (allowed methods) | HTTP methods or operation types |
| models | ModelRestriction (allowed models) | Language model invocations |
| tools | ToolRestriction (allowed tools) | Tool or function access |
| record_sets | RecordSetRestriction (allowed sets) | Database or storage access |
| byte_counts | ByteCountRestriction (max input/output bytes) | Input/output size limits |
| durations | DurationRestriction (max duration ms) | Execution time limits |
| invocation_budgets | InvocationBudgetRestriction (max invocations in window) | Invocation frequency limits |

When multiple dimensions are specified, the host MUST apply ALL restrictions.
A capability MUST satisfy all applied restrictions to execute.

Precedence rules:
- `denied_prefixes` takes precedence over `allowed_prefixes`
- `denied_origins` takes precedence over `allowed_origins`

### Design decisions

1. **Attenuation is conjunctive**: All restrictions are applied together.
   This implements the principle of least privilege by combining multiple
   constraints rather than allowing any single permissive path.

2. **Deny-lists override allow-lists**: Explicit denials always override
   broader allowances. This is a safety-first approach that prevents
   accidental privilege escalation through allow-list misconfiguration.

3. **Byte counts, durations, and budgets are hard limits**: Exceeding any
   of these limits causes execution to fail with a specific diagnostic
   (`byte-count-exceeded`, `duration-exceeded`, `budget-exceeded`). This
   prevents resource exhaustion attacks.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement Contract And Data Model](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin composition: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Signal envelopes: [Signal Envelopes Causality Routing And Delivery](../60-specification/10-signals-causality-routing-and-delivery.md)
- Turn lifecycle: [Turn Lifecycle Protocols And Canonical Encoding](../60-specification/04-turn-lifecycle-protocols-and-canonical-encoding.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)

## Open questions

1. Should attenuation support dynamic adjustment during execution? The
   current design evaluates attenuation at policy evaluation time. Could
   a runtime policy engine adjust restrictions based on observed behavior?

2. How should conflicting attenuation dimensions be resolved? If one
   restriction allows an action but another denies it, the deny takes
   precedence, but the spec does not address priority between different
   dimension types (e.g., paths vs. origins).

3. Can approval workflows be nested? If an `approval-required` decision
   itself requires approval from a higher authority, the spec does not
   address recursive approval chains.
