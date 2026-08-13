---
title: "Phase 2 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-02
  - implementation
  - behavior-and-integration
  - policy-evaluation
  - attenuation-enforcement
  - approval-workflow
  - revocation
aliases:
  - "M5-P2-2.2 Implementation"
---

# Phase 2 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 2.2 (Behavior And Integration) from
[Phase 2 - Capability Policy Attenuation Limits And Enforcement](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-02-capability-policy-attenuation-limits-and-enforcement.md)
of
[Milestone 5](../../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[31-capability-policy-attenuation-limits-and-enforcement.md](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
which defines policy evaluation integration with the turn lifecycle,
attenuation enforcement, the approval workflow, and revocation/policy
versioning mechanisms.

## Subtask 2.2.1.1: Bind granted capabilities and limits into TurnRequest

### Implementation

Defined how the host binds granted capabilities and limits into the
`TurnRequest` while retaining independent host enforcement. The host
assembles the `PolicyInput` from authenticated principal, tenant, agent,
artifact, plugin, purpose, signal, requested capability, resource, and
runtime context. Grants are validated against the trust model defined in
[Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

### Design decisions

1. **Host owns policy evaluation**: The host, not the agent or guest,
   evaluates policy. This prevents agents from self-authorizing actions
   and ensures that policy decisions are independent of agent intent.

2. **Grants are validated, not just presented**: The host validates that
   the presented grants satisfy the `PolicyInput` requirements. Invalid
   or expired grants cause immediate denial with `policy.grant_absent`
   or `policy.grant_expired`.

3. **Independent enforcement is mandatory**: Even if the `TurnRequest`
   includes granted capabilities, the host MUST re-evaluate policy at
   each boundary. This prevents request-level caching from bypassing
   runtime policy checks.

## Subtask 2.2.1.2: Recheck policy at six boundaries

### Implementation

Defined six policy evaluation boundaries in the turn lifecycle:

| Boundary | Trigger | Action on deny/unavailable |
|----------|---------|---------------------------|
| Signal admission | Signal enters turn lifecycle | Reject signal with `reason` |
| Action resolution | Action resolved to instruction | Reject action with `reason` |
| Guest invocation | Guest export invoked | Skip invocation with `reason` |
| Directive validation | Directive validated for execution | Reject directive with `reason` |
| Effect dispatch | Effect dispatched to handler | Reject effect with `reason` |
| Result admission | Result admitted to turn | Reject result with `reason` |

Policy decisions are cached when `PolicyInput` is unchanged. Cache
invalidation occurs on:
- Policy version change
- Grant revocation or expiry
- Principal trust class change
- Tenant policy profile change
- Revocation signal received

### Design decisions

1. **Policy is re-evaluated at every boundary**: Continuous enforcement
   prevents scenarios where a capability is granted at one boundary but
   used unauthorizedly at a later boundary. This is defense-in-depth.

2. **Caching is safe because of invalidation triggers**: The spec lists
   five conditions that invalidate cached decisions. This ensures that
   cached decisions are never stale or inconsistent with current policy.

3. **Cached decisions are not used across policy versions**: The host
   MUST re-evaluate policy when any field of `PolicyInput` changes.
   This prevents policy version drift from causing unauthorized access.

## Subtask 2.2.1.3: Define revocation and policy versioning

### Implementation

Defined four revocation mechanisms:
1. Grant revocation: Explicit revocation by granting principal or operator
2. Policy version change: Active policy version updated
3. Trust class change: Principal's trust class updated
4. Tenant policy profile change: Tenant's policy profile updated

On revocation, the host MUST:
- Invalidate all cached policy decisions depending on revoked state
- NOT allow new invocations using invalidated decisions
- Allow in-flight invocations to complete or be rolled back

Policy versioning:
- Host tracks policy versions and includes current version in `PolicyInput`
- Evaluations with mismatched policy version are rejected
- Cache invalidation occurs on version change

### Design decisions

1. **In-flight invocations are not interrupted by revocation**: This
   prevents operational disruption but requires careful rollback
   semantics. The spec says invocations "MUST be allowed to complete
   or be rolled back" but does not specify which is preferred.

2. **Policy version is part of PolicyInput**: This makes policy version
   a first-class citizen in policy evaluation. It enables the host to
   detect and reject stale evaluations.

3. **Revocation is immediate for new invocations**: The spec requires
   that revoked grants prevent new invocations immediately. This is
   a liveness property that prevents policy gaps.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 31.1: [Capability Policy Attenuation Limits And Enforcement Contract And Data Model](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.3: [Capability Policy Attenuation Limits And Enforcement Failure Evidence And Operational Notes](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Section 31.4: [Capability Policy Attenuation Limits And Enforcement Phase 2 Integration Tests](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin composition: [Framework Plugin Manifests Composition And Lifecycle Hooks](../../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Signal envelopes: [Signal Envelopes Causality Routing And Delivery](../../60-specification/10-signals-causality-routing-and-delivery.md)
- Turn lifecycle: [Turn Lifecycle Protocols And Canonical Encoding](../../60-specification/04-turn-lifecycle-protocols-and-canonical-encoding.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)

## Open questions

1. Should policy evaluation be parallelizable? The spec lists six
   boundaries but does not address whether evaluations at different
   boundaries can be parallelized for performance.

2. How should approval deadlines interact with turn timeouts? If an
   approval deadline exceeds the turn timeout, the turn will timeout
   before approval is received. Should approval deadlines be bounded
   by turn timeouts?

3. Can policy decisions be audited for compliance? The spec requires
   audit logging of policy decisions but does not define the audit
   log format or retention policy for policy-specific evidence.
