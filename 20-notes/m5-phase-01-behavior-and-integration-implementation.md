---
title: "Phase 1 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-05
  - phase-01
  - implementation
  - behavior-and-integration
  - trust-classes
  - grants
  - authentication
  - authorization
aliases:
  - "M5-P1-1.2 Implementation"
---

# Phase 1 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 1.2 (Behavior And Integration) from
[Phase 1 - Threat Model Principals Trust Classes And Grant Vocabulary](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
-- Capabilities, Plugins, Security, And Tenancy.

The implementation produced the specification chapter
[30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
which defines trust classes, grant vocabulary, and authentication/authorization
failure outcomes.

## Subtask 1.2.1.1: Define trust classes

### Implementation

Defined five trust classes that classify principals by their authentication,
authorization, artifact provenance, and tenant isolation status:

| Trust Class | Scope | External Access |
|-------------|-------|-----------------|
| UntrustedGuest | Agent artifacts unreviewed and unsigned | Sandboxed, no external access |
| ReviewedPlugin | Framework plugins reviewed and signed | Limited access based on grants |
| PrivilegedHostIntegration | Host-owned integrations | Full host privileges |
| MaintenanceMigration | Reviewed migration artifacts | Limited access, migration-only |
| OperatorTrust | Operators with admin privileges | Full access to config and policy |

Trust class assignment is determined by four factors: authentication (identity
verification), authorization (required grants), artifact provenance (signature
verification), and tenant isolation (correct tenant scoping).

### Design decisions

1. **Trust class is a property of the principal-artifact pair, not just the principal**: The same principal (e.g., a plugin publisher) may be in different trust classes depending on whether the artifact they submit is reviewed and signed. This allows a trusted publisher to still produce untrusted artifacts.

2. **PrivilegedHostIntegration is host-owned and not a principal kind**: This trust class is reserved for host-native integrations, not for any principal kind defined in section 1.1. This prevents any guest or plugin from claiming privileged status.

3. **MaintenanceMigration is ephemeral**: It is a trust class for short-lived artifacts used only during plugin upgrades or system migrations. It does not persist across host restarts.

## Subtask 1.2.1.2: Define grant vocabulary

### Implementation

Defined the `Grant` data structure with eight authorization dimensions:

```
Grant {
  grant_id: GrantId,
  principal_id: PrincipalId,
  capability: Capability,
  tenant_id: TenantId?,
  resource: Resource,
  purpose: Purpose,
  operation: Operation,
  constraints: GrantConstraints,
  expiry: UnixTimestamp?,
  delegating: bool,
  metadata: JsonObject
}
```

Grant dimensions:
- **Capability**: Specific capability (e.g., `effects`, `signals`, `timers`, `child-lifecycle`)
- **Tenant**: Tenant(s) the grant applies to
- **Resource**: Resource pattern (e.g., `agents/*`, `artifacts/v1/*`)
- **Purpose**: Purpose (e.g., `production`, `development`, `testing`)
- **Operation**: Operation (e.g., `read`, `write`, `delete`, `execute`)
- **Constraints**: Additional constraints (e.g., `max_requests_per_second`, `allowed_outbound_hosts`)
- **Expiry**: Grant expiry time
- **Delegating**: Whether the grant can be delegated

### Design decisions

1. **Grants are evaluated at every authorization boundary**: The host MUST enforce grants at every point where a capability is exercised, not just at invocation time. This prevents privilege escalation between boundaries.

2. **Constraints are JSON objects for flexibility**: The `constraints` field uses `JsonObject` to allow implementations to define arbitrary constraint types without modifying the normative schema. However, the constraints MUST NOT be used for authorization decisions themselves (only for enforcement).

3. **Delegation is opt-in**: The `delegating` field defaults to `false`, ensuring that grants are not implicitly delegatable. This supports the principle of least privilege.

## Subtask 1.2.1.3: Define authentication and authorization failure outcomes

### Implementation

Defined seven authentication/authorization failure outcomes and their error codes:

| Outcome | Error Code | Description |
|---------|-----------|-------------|
| Authentication failure | `auth.authentication_failure` | Principal identity could not be verified |
| Principal mismatch | `auth.principal_mismatch` | Presented principal does not match expected principal |
| Grant absence | `auth.grant_absence` | Principal does not have required grant |
| Scope conflict | `auth.scope_conflict` | Grant scope conflicts with requested operation |
| Grant expiry | `auth.grant_expiry` | Grant has expired |
| Grant revocation | `auth.grant_revocation` | Grant has been revoked |
| Untrusted publisher | `auth.untrusted_publisher` | Artifact publisher is not trusted |

Each failure outcome is mapped to a specific error code and human-readable diagnostic
message that identifies the phase contract, profile, and failed boundary without
exposing secrets.

### Design decisions

1. **Error codes are namespaced by domain**: The `auth.*` and `trust.*` prefixes
   distinguish authentication/authorization errors from trust-class errors (e.g.,
   `trust.untrusted_guest`). This enables operators to filter and route diagnostics
   by domain.

2. **Diagnostics are bounded by construction**: The spec requires that diagnostic
   messages identify the phase contract, profile, and failed boundary but explicitly
   forbids exposing secrets, internal implementation details, or sensitive data.

3. **Failure outcomes are exhaustive for M5**: The seven outcomes cover all
   authentication and authorization failure modes relevant to the threat model.
   Later phases (capability policy, plugin composition) define additional failure
   outcomes in their own namespaces.

## Cross-references

- Section 30.1: [Threat Model Principals Trust Classes And Grant Vocabulary Contract And Data Model](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Section 30.2: [Threat Model Principals Trust Classes And Grant Vocabulary Behavior And Integration](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugins: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Host functions: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Provenance: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Profile vocabulary: [Profile Vocabulary And Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)
- Stable identities: [Stable Identities Versions Errors And Limits](../60-specification/02-stable-identities-versions-errors-and-limits.md)

## Open questions

1. Should grant revocation be immediate or allow in-flight invocations to complete?
   The spec says "in-flight invocations MUST be allowed to complete or be rolled back"
   but does not specify which behavior is preferred for different trust classes.

2. How should cross-milestone grant references work? The `Capability` type is
   defined in [Effect Handlers Attempts Idempotency And Result Signals](../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
   but the grant vocabulary chapter does not enumerate the specific capability values.

3. Can an operator trust principal authenticate via mTLS, API keys, or both?
   The authentication mechanism is implementation-defined; a conformance profile
   should document which mechanisms are supported.
