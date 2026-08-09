---
title: "Threat Model Principals Trust Classes And Grant Vocabulary"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-05
  - phase-01
  - security
  - threat-model
  - principals
  - trust-classes
  - grants
aliases:
  - "M5-P1 Threat Model Principals Trust Classes And Grant Vocabulary"
---

# Threat Model Principals Trust Classes And Grant Vocabulary

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/phase-01-threat-model-principals-trust-classes-and-grant-vocabulary.md)
of
[Milestone 5](../.spec/planning/agentic-system/milestone-05-capabilities-plugins-security-and-tenancy/README.md)
--
Capabilities, Plugins, Security, And Tenancy.
It defines adversaries, protected assets, authenticated identities, trust
zones, and the vocabulary used by every authorization decision.

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
[Stable Identities Versions Errors And Limits](02-stable-identities-versions-errors-and-limits.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md),
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
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
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md),
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md).

## 1.1 Contract And Data Model

### Threat model

> **Normative definition.**
The host MUST defend against the following threat actors:

1. **Malicious guest**: The agent artifact contains intentionally harmful code.
2. **Compromised artifact**: The agent artifact is modified after signing.
3. **Hostile input/output**: External signals or results contain malicious data.
4. **Confused deputy**: The agent is tricked into performing an unauthorized action.
5. **Tenant attacker**: A tenant attempts to access another tenant's data.
6. **Dependency compromise**: A plugin or external dependency is compromised.
7. **Operator error**: An operator misconfigures the system.
8. **Co-tenant attacker**: A tenant attempts to access shared resources.

> **Normative definition.**
Each threat actor MUST have corresponding countermeasures documented in section
1.2.

### Protected assets

> **Normative definition.**
The host MUST protect the following assets:

1. **Host memory**: The host process memory space.
2. **State**: Agent state, journal, snapshots, and outbox entries.
3. **Secrets**: API keys, tokens, and other credentials.
4. **Policy**: Authorization policies, trust classes, and grants.
5. **Artifacts**: Agent and plugin WASM modules.
6. **Audit evidence**: Logs and records of all authorization decisions.
7. **External systems**: Downstream services contacted by the agent.
8. **Availability**: The host process and its resources.
9. **Model context**: The LLM context window and its contents.

> **Normative definition.**
Each protected asset MUST have corresponding access controls documented in
section 1.2.

### Principal forms

> **Normative definition.**
The host MUST support the following principal forms:

1. **User**: A human operator or end user.
2. **Service**: A non-human service account.
3. **Agent**: An agent runtime instance.
4. **Plugin publisher**: The publisher of a framework plugin.
5. **Operator**: A system operator with administrative privileges.
6. **Effect worker**: A worker that processes external effects.
7. **External result source**: A source of external results (e.g., API).

> **Normative definition.**

```
Principal {
  kind: PrincipalKind,
  id: PrincipalId,
  tenant_id: TenantId?,
  metadata: JsonObject
}

PrincipalKind = User | Service | Agent | PluginPublisher | Operator | EffectWorker | ExternalResultSource
PrincipalId = string
TenantId = Defined in [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).
```

> **Normative definition.**
The `tenant_id` field is optional and is only set for principals that are
scoped to a specific tenant.
The `metadata` field is implementation-defined and MUST NOT be used for
authorization decisions.

## 1.2 Behavior And Integration

### Trust classes

> **Normative definition.**
The host MUST enforce the following trust classes:

1. **Untrusted guest**: Agent artifacts that have not been reviewed or signed.
   Run in a sandbox with no external access.
2. **Reviewed plugin**: Framework plugins that have been reviewed and signed.
   Run in a sandbox with limited external access based on grants.
3. **Privileged host integration**: Host-owned integrations with full access.
   Run with the host's privileges.
4. **Maintenance migration**: Migration artifacts that have been reviewed.
   Run with limited access for migration purposes only.
5. **Operator trust**: Operators with administrative privileges.
   Run with full access to configuration and policy.

> **Normative definition.**

```
TrustClass = UntrustedGuest | ReviewedPlugin | PrivilegedHostIntegration | MaintenanceMigration | OperatorTrust
```

> **Normative definition.**
The trust class of a principal is determined by:

1. **Authentication**: The principal's identity is verified.
2. **Authorization**: The principal has the required grants.
3. **Artifact provenance**: The artifact is signed and verified.
4. **Tenant isolation**: The principal is scoped to the correct tenant.

### Grant vocabulary

> **Normative definition.**
The host MUST support the following grant dimensions:

1. **Capability**: The specific capability being granted (e.g., `effects`,
   `signals`, `timers`, `child-lifecycle`).
2. **Tenant**: The tenant(s) the grant applies to.
3. **Resource**: The specific resource being granted (e.g., `agents/*`,
   `artifacts/v1/*`).
4. **Purpose**: The purpose for which the grant is made (e.g., `production`,
   `development`, `testing`).
5. **Operation**: The specific operation being granted (e.g., `read`, `write`,
   `delete`, `execute`).
6. **Constraints**: Any constraints on the grant (e.g., `max_requests_per_second`,
   `allowed_outbound_hosts`).
7. **Expiry**: The grant expiry time.
8. **Delegating authority**: Whether the grant can be delegated to other principals.

> **Normative definition.**

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

GrantId = string
Capability = Defined in [Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).
Resource = string
Purpose = "production" | "development" | "testing"
Operation = "read" | "write" | "delete" | "execute"
GrantConstraints = JsonObject
```

> **Normative definition.**
The `tenant_id` field is optional and is only set for grants that are scoped
to a specific tenant.
The `expiry` field is optional and is null if the grant does not expire.
The `delegating` field determines whether the grant can be delegated to other
principals.
The `metadata` field is implementation-defined and MUST NOT be used for
authorization decisions.

> **Normative definition.**
The host MUST enforce grants at every authorization boundary.
A principal MUST present a valid grant for every operation it performs.
The host MUST reject operations that lack valid grants.

### Authentication and authorization failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for authentication and
authorization:

1. **Authentication failure**: The principal's identity could not be verified.
2. **Principal mismatch**: The presented principal does not match the expected
   principal.
3. **Grant absence**: The principal does not have the required grant.
4. **Scope conflict**: The grant's scope conflicts with the requested operation.
5. **Grant expiry**: The grant has expired.
6. **Grant revocation**: The grant has been revoked.
7. **Untrusted publisher**: The artifact publisher is not trusted.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

## 1.3 Failure Evidence And Operational Notes

### Failure outcomes

> **Normative definition.**
The host MUST define the following failure outcomes for threat model principals
trust classes and grant vocabulary:

1. **Malformed**: Input data does not conform to the expected schema.
2. **Incompatible**: Data is incompatible with the current schema version or
   handler version.
3. **Conflicting**: Multiple writers attempt to write to the same record
   (optimistic concurrency conflict).
4. **Unauthorized**: The caller does not have permission to perform the operation.
5. **Exhausted**: The system is out of resources (e.g., storage capacity, grant
   budget).
6. **Unavailable**: The storage backend is unavailable.

> **Normative definition.**
Each failure outcome MUST be mapped to a specific error code and diagnostic
message.

### Error codes

> **Normative definition.**
The host MUST use the following error codes for threat model principals trust
classes and grant vocabulary:

| Error Code | Description |
|------------|-------------|
| `auth.authentication_failure` | Principal identity could not be verified |
| `auth.principal_mismatch` | Presented principal does not match expected principal |
| `auth.grant_absence` | Principal does not have required grant |
| `auth.scope_conflict` | Grant scope conflicts with requested operation |
| `auth.grant_expiry` | Grant has expired |
| `auth.grant_revocation` | Grant has been revoked |
| `auth.untrusted_publisher` | Artifact publisher is not trusted |
| `trust.untrusted_guest` | Guest artifact is untrusted |
| `trust.unreviewed_plugin` | Plugin has not been reviewed |
| `tenant.isolation_violation` | Tenant isolation boundary crossed |
| `storage.snapshot.duplicate` | Snapshot ID already exists (see
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `storage.unavailable` | Storage backend unavailable (see
  [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)) |
| `commit.conflict` | Optimistic concurrency conflict (see
  [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)) |

> **Normative definition.**
Each error code MUST be accompanied by a human-readable diagnostic message.
The diagnostic message MUST identify the phase contract, profile, and failed
boundary without exposing secrets.

### Bounded diagnostics

> **Normative definition.**
The host MUST emit bounded diagnostics for each failure outcome.
The diagnostics MUST include:

1. **Error code**: The specific error code from the table above.
2. **Context**: The operation that failed (e.g., authentication, authorization,
   grant validation).
3. **Entity identifiers**: The tenant ID, agent ID, or principal ID involved
   (without exposing sensitive data).
4. **Timestamp**: The time the error occurred.
5. **Retryable**: Whether the operation can be retried.

> **Normative definition.**
The host MUST NOT expose internal implementation details, secrets, or
sensitive data in diagnostics.

### Implementation-defined choices

> **Normative implementation-defined choice.**
The following choices are implementation-defined and MUST be documented in the
conformance profile:

1. **Authentication mechanism**: The mechanism used for principal authentication
   (e.g., API keys, OAuth, mTLS).
2. **Grant storage**: The grant storage implementation (in-memory, database, etc.).
3. **Grant caching**: The grant caching strategy.
4. **Audit log retention**: The audit log retention policy.
5. **Trust class assignment**: The policy for assigning trust classes to artifacts.

### Deferred work

> **Non-normative note.**
The following work is deferred to later phases or host implementations:

1. **Dynamic trust classes**: Runtime trust class adjustment based on behavior.
2. **Grant delegation**: Automated grant delegation workflows.
3. **Tenant onboarding**: Automated tenant onboarding and provisioning.
4. **Security metrics**: Security metrics and monitoring.

### Results invalidating earlier milestones

> **Non-normative note.**
The following results from Phase 1 MAY invalidate earlier milestone assumptions:

1. **Authentication overhead**: If authentication overhead exceeds the turn
   timeout, the timeout or authentication mechanism MUST be revised.
2. **Grant storage capacity**: If the grant storage exceeds the capacity planned
   in earlier milestones, the capacity plan MUST be revised.
3. **Audit log size**: If the audit log size exceeds the capacity planned in
   earlier milestones, the capacity plan MUST be revised.

> **Non-normative note.**
If any result from Phase 1 invalidates an earlier milestone assumption, the
affected milestone MUST be revised and re-validated.

## 1.4 Phase 1 Integration Tests

### Integration test objectives

> **Normative definition.**
The Phase 1 integration tests MUST verify the following objectives:

1. **Canonical successful flow**: The host authenticates principals, validates
   grants, and enforces trust classes successfully.
2. **Failure handling**: The host handles malformed, incompatible, stale,
   duplicate, and boundary-limit inputs correctly.
3. **Security enforcement**: The host enforces tenant isolation, grant
   constraints, and trust classes without leaving unauthorized state.
4. **Cross-milestone compatibility**: The phase does not introduce regressions
   in earlier milestones.

> **Normative definition.**
Each integration test MUST exercise observable contracts rather than private
implementation structure.

### Successful flow tests

> **Normative definition.**
The following tests MUST verify the canonical successful flow:

1. **Principal authentication**: Authenticate a user, service, agent, or operator
   principal and verify the authentication succeeds.
2. **Grant validation**: Validate a grant and verify the grant is valid.
3. **Trust class enforcement**: Enforce a trust class and verify the principal
   is restricted to the correct access level.
4. **Tenant isolation**: Verify that a tenant cannot access another tenant's data.
5. **Audit logging**: Verify that all authorization decisions are logged.

> **Normative definition.**
Each test MUST record the following evidence:

- Input data
- Expected output
- Actual output
- Pass/fail status

### Failure handling tests

> **Normative definition.**
The following tests MUST verify failure handling:

1. **Authentication failure**: Attempt to authenticate with invalid credentials and
   verify the `auth.authentication_failure` error code.
2. **Principal mismatch**: Present a principal that does not match the expected
   principal and verify the `auth.principal_mismatch` error code.
3. **Grant absence**: Attempt an operation without a valid grant and verify the
   `auth.grant_absence` error code.
4. **Scope conflict**: Present a grant with a conflicting scope and verify the
   `auth.scope_conflict` error code.
5. **Grant expiry**: Present an expired grant and verify the `auth.grant_expiry`
   error code.
6. **Grant revocation**: Present a revoked grant and verify the `auth.grant_revocation`
   error code.
7. **Untrusted publisher**: Attempt to load an artifact from an untrusted publisher
   and verify the `auth.untrusted_publisher` error code.
8. **Untrusted guest**: Attempt to run an untrusted guest and verify the
   `trust.untrusted_guest` error code.
9. **Tenant isolation violation**: Attempt to access another tenant's data and verify
   the `tenant.isolation_violation` error code.

> **Normative definition.**
Each test MUST verify that the error code and diagnostic message match the
expected values.

### Security enforcement tests

> **Normative definition.**
The following tests MUST verify security enforcement:

1. **Tenant data isolation**: Verify that tenant A cannot read tenant B's data.
2. **Grant constraint enforcement**: Verify that grant constraints (e.g., rate limits)
   are enforced.
3. **Trust class sandboxing**: Verify that untrusted guests are sandboxed.
4. **Audit log completeness**: Verify that all authorization decisions are logged.
5. **Secret isolation**: Verify that secrets are not exposed to untrusted guests.

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
   regressions. Milestone 2 fixtures are defined in the Phase 1-5 plans under
   [Milestone 2](../.spec/planning/agentic-system/milestone-02-signals-actions-state-and-strategies/).
3. **Milestone 3 fixtures**: Run all Milestone 3 fixtures and verify no
   regressions. Milestone 3 fixtures are defined in the Phase 1-5 plans under
   [Milestone 3](../.spec/planning/agentic-system/milestone-03-host-actor-runtime-and-lifecycle/).
4. **Milestone 4 fixtures**: Run all Milestone 4 fixtures and verify no
   regressions. Milestone 4 fixtures are defined in the Phase 1-5 plans under
   [Milestone 4](../.spec/planning/agentic-system/milestone-04-durable-state-effects-and-recovery/).

> **Normative definition.**
If any regression is detected, the affected milestone MUST be revised and
re-validated.

### Integration test evidence

> **Normative definition.**
The Phase 1 integration tests MUST produce the following evidence:

1. **Test report**: A report listing all tests with pass/fail status.
2. **Authentication evidence**: Evidence that principals are authenticated correctly.
3. **Grant validation evidence**: Evidence that grants are validated correctly.
4. **Trust class enforcement evidence**: Evidence that trust classes are enforced
   correctly.
5. **Tenant isolation evidence**: Evidence that tenant isolation is maintained.
6. **Audit log evidence**: Evidence that all authorization decisions are logged.
7. **Failure diagnostics**: Evidence that failure diagnostics are correct and
   bounded.

> **Normative definition.**
The integration test evidence MUST be retained for later milestone and release
gates.

## Variability register

| Item | Permission | Recommendation | Constraint |
|------|------------|----------------|------------|
| Authentication mechanism | Implementation-defined | Document in conformance profile | Must support principal forms |
| Grant storage | Implementation-defined | Document in conformance profile | Must support grant dimensions |
| Grant caching | Implementation-defined | Document in conformance profile | Must balance consistency and performance |
| Audit log retention | Implementation-defined | Document in conformance profile | Must preserve audit trail |
| Trust class assignment | Implementation-defined | Document in conformance profile | Must enforce trust boundaries |
| Tenant isolation | Implementation-defined | Document in conformance profile | Must prevent cross-tenant access |
| Secret management | Implementation-defined | Document in conformance profile | Must prevent exposure to untrusted guests |
