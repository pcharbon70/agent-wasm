---
title: "Compatibility Upgrades Migrations Deployment And Horizontal Coordination Phase 4 Integration Tests"
kind: specification
created: "2026-08-10"
status: draft
spec_version: "0.2.0"
tags:
  - milestone-09
  - phase-04
  - compatibility
  - upgrades
  - migrations
  - deployment
  - horizontal-coordination
  - integration-tests
  - phase-4
aliases:
  - "M9-P4-S4 Phase 4 Integration Tests"
---

# Compatibility Upgrades Migrations Deployment And Horizontal Coordination Phase 4 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-04-compatibility-upgrades-migrations-deployment-and-horizontal-coordination.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It defines the integration tests that verify compatibility, upgrades,
migrations, deployment, and horizontal coordination across their real
dependency boundaries.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires passing this test suite and
a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md),
[Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model](48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md),
[Compatibility Upgrades Migrations Deployment And Horizontal Coordination Contract And Data Model](49-compatibility-upgrades-migrations-deployment-and-horizontal-coordination-contract-and-data-model.md),
[Compatibility Upgrades Migrations Deployment And Horizontal Coordination Behavior And Integration](49-compatibility-upgrades-migrations-deployment-and-horizontal-coordination-behavior-and-integration.md),
[Compatibility Upgrades Migrations Deployment And Horizontal Coordination Failure Evidence And Operational Notes](49-compatibility-upgrades-migrations-deployment-and-horizontal-coordination-failure-evidence-and-operational-notes.md).

## 49.4 Phase 4 Integration Tests

This section defines the observable behavior that the Phase 4 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### 49.4.1 Successful flow

Compatibility, upgrades, migrations, deployment, and horizontal coordination
MUST execute correctly and produce expected outputs with complete evidence.
The test MUST verify that:

1. Compatibility matrices are maintained for all components (host, protocol,
   manifest, guest-sdk, plugin, artifact, schema, strategy, storage, runtime, provider).
2. Compatibility checks pass for compatible versions and reject incompatible versions.
3. Upgrades execute successfully (pre-upgrade, expand, migrate, contract, post-upgrade).
4. Checkpoints are created at all required points (pre-expand, post-expand, pre-migrate,
   post-migrate, pre-contract, post-contract, pre-upgrade, post-upgrade).
5. Mixed-version windows remain within limits (time and state).
6. Unsupported downgrades are rejected with stable diagnostics.
7. Artifact/plugin rollout executes successfully (validation, canary, observation,
   promotion, rollback, quarantine).
8. Single-node packaging deploys host correctly (host-binary, configuration, storage,
   runtime, observability).
9. Durable volumes persist host state across restarts (state, configuration, observability,
   backup).
10. Graceful drain completes successfully (stop-accepting, complete-in-flight, drain-mailbox,
    drain-outbox, drain-completed).
11. Restart restores host from last checkpoint (graceful-restart, force-restart, rolling-restart).
12. Backup and restore preserve host state (backup, restore, verify).
13. Disaster recovery procedures execute correctly (failover, failback, recovery).
14. Horizontal routing distributes requests correctly (replaceable, load-balanced, tenant-aware,
    artifact-aware).
15. Activation coordination ensures only one node is active (leader-based, leaderless).
16. Placement routes requests correctly (static, dynamic, affinity-based).
17. Fencing prevents stale operations (epoch-based, token-based, version-based).
18. Split-brain scenarios are detected and resolved (multiple-leaders, stale-leader,
    conflicting-state).
19. The test records and retains:
    - Compatibility matrix data and check results.
    - Upgrade execution results and checkpoints.
    - Migration execution results and rollback evidence.
    - Deployment execution results (drain, restart, backup, restore, disaster recovery).
    - Horizontal coordination execution results (routing, activation, placement, fencing,
      split-brain resolution).
    - Artifact/plugin rollout execution results.

### 49.4.2 Malformed and incompatible input

Compatibility, upgrades, migrations, deployment, and horizontal coordination MUST
reject malformed and incompatible inputs with stable diagnostics.
The test MUST verify that:

1. Incompatible host version produces `compatibility.check.failed` diagnostic.
2. Incompatible protocol version produces `compatibility.check.failed` diagnostic.
3. Incompatible artifact schema produces `compatibility.check.failed` diagnostic.
4. Incompatible plugin version produces `compatibility.check.failed` diagnostic.
5. Incompatible strategy version produces `compatibility.check.failed` diagnostic.
6. Missing compatibility matrix produces `compatibility.matrix.missing` diagnostic.
7. Pre-upgrade validation failure produces `upgrade.pre-upgrade.failed` diagnostic.
8. Expand step failure produces `upgrade.expand.failed` diagnostic.
9. Migrate step failure produces `upgrade.migrate.failed` diagnostic.
10. Contract step failure produces `upgrade.contract.failed` diagnostic.
11. Post-upgrade validation failure produces `upgrade.post-upgrade.failed` diagnostic.
12. Migration interruption produces `migration.interruption` diagnostic.
13. Incompatible agent state produces `migration.incompatible-agent-state` diagnostic.
14. Stale worker produces `migration.stale-worker` diagnostic.
15. Replay mismatch produces `migration.replay-mismatch` diagnostic.
16. Drain timeout produces `deployment.drain.timeout` diagnostic.
17. Restart failure produces `deployment.restart.failed` diagnostic.
18. Backup failure produces `deployment.backup.failed` diagnostic.
19. Restore failure produces `deployment.restore.failed` diagnostic.
20. Disaster recovery failure produces `deployment.disaster-recovery.failed` diagnostic.
21. Multiple leaders produce `coordination.split-brain.multiple-leaders` diagnostic.
22. Stale leader produces `coordination.split-brain.stale-leader` diagnostic.
23. Conflicting state produces `coordination.split-brain.conflicting-state` diagnostic.
24. Invalid epoch produces `coordination.fencing.epoch.invalid` diagnostic.
25. Invalid token produces `coordination.fencing.token.invalid` diagnostic.
26. Invalid version produces `coordination.fencing.version.invalid` diagnostic.
27. Rollout validation failure produces `rollout.validation.failed` diagnostic.
28. Canary observation failure produces `rollout.canary.observation.failed` diagnostic.
29. Promotion failure produces `rollout.promotion.failed` diagnostic.
30. Quarantine failure produces `rollout.quarantine.failed` diagnostic.
31. No state, journal, or outbox entries are created for the failed operations.
32. The diagnostic identifies the specific field, type, or boundary that failed.
33. The diagnostic does not expose secrets or implementation internals.

### 49.4.3 Stale and duplicate input

Compatibility, upgrades, migrations, deployment, and horizontal coordination MUST
detect and reject stale or duplicate inputs.
The test MUST verify that:

1. Duplicate compatibility checks with same version produce stable diagnostic.
2. Duplicate upgrade attempts with same version produce stable diagnostic.
3. Duplicate migration attempts with same schema version produce stable diagnostic.
4. Duplicate drain attempts with same host state produce stable diagnostic.
5. Duplicate restart attempts with same checkpoint produce stable diagnostic.
6. Duplicate backup attempts with same timestamp produce stable diagnostic.
7. Duplicate restore attempts with same backup produce stable diagnostic.
8. Duplicate failover attempts with same secondary deployment produce stable diagnostic.
9. Duplicate horizontal routing attempts with same request produce stable diagnostic.
10. Duplicate activation coordination attempts with same leader produce stable diagnostic.
11. Duplicate placement attempts with same request produce stable diagnostic.
12. Duplicate fencing attempts with same epoch/token/version produce stable diagnostic.
13. No state, journal, or outbox entries are created for the rejected operations.
14. The diagnostic identifies the stale or duplicate input.

### 49.4.4 Boundary and limit inputs

Compatibility, upgrades, migrations, deployment, and horizontal coordination MUST
enforce configured boundaries and limits.
The test MUST verify that:

1. Mixed-version window time limits are enforced (e.g., expand window exceeds 1 hour).
2. Mixed-version window state limits are enforced (e.g., migrate window exceeds 10,000 revisions).
3. Rollout canary percentage limits are enforced (e.g., canary exceeds 10%).
4. Rollout observation metric limits are enforced (e.g., error rate exceeds 5%).
5. Graceful drain timeout is enforced (e.g., drain exceeds 30 seconds).
6. Horizontal routing load limits are enforced (e.g., node exceeds max connections).
7. Activation coordination health check timeout is enforced (e.g., leader not responsive).
8. Fencing epoch/token/version limits are enforced (e.g., stale epoch rejected).
9. No state, journal, or outbox entries are created for the rejected operations.
10. The diagnostic identifies the boundary or limit that was exceeded.

### 49.4.5 Timeout, cancellation, and unavailable dependency

Compatibility, upgrades, migrations, deployment, and horizontal coordination MUST
handle timeouts, cancellations, and unavailable dependencies gracefully
without leaving unauthorized or partial state.
The test MUST verify that:

1. Upgrade timeout produces stable diagnostic (e.g., upgrade exceeds time limit).
2. Migration timeout produces stable diagnostic (e.g., migration exceeds time limit).
3. Drain timeout produces `deployment.drain.timeout` diagnostic.
4. Restart timeout produces stable diagnostic (e.g., restart exceeds time limit).
5. Backup timeout produces stable diagnostic (e.g., backup exceeds time limit).
6. Restore timeout produces stable diagnostic (e.g., restore exceeds time limit).
7. Disaster recovery timeout produces stable diagnostic (e.g., failover exceeds time limit).
8. Unavailable storage produces stable diagnostic (e.g., storage write fails).
9. Unavailable checkpoint produces stable diagnostic (e.g., checkpoint not found).
10. Unavailable secondary deployment produces stable diagnostic (e.g., failover fails).
11. Unavailable host node produces stable diagnostic (e.g., node unreachable).
12. Cancellation of upgrade produces stable diagnostic (e.g., upgrade cancelled by operator).
13. Cancellation of migration produces stable diagnostic (e.g., migration cancelled by operator).
14. Cancellation of drain produces stable diagnostic (e.g., drain cancelled by operator).
15. The system transitions to a safe state (e.g., rolled back, paused) after failures.
16. No state, journal, or outbox entries are created for the failed operations.

### 49.4.6 Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.
The test MUST verify that:

1. All Phase 1 integration tests from Milestone 1 (Profile Vocabulary) still pass.
2. All Phase 5 integration tests from Milestone 1 (Guest SDK) still pass.
3. All Phase 3 integration tests from Milestone 3 (Agent Registry) still pass.
4. All Phase 1 integration tests from Milestone 7 (Provider-Neutral Model Requests) still pass.
5. All Phase 1 integration tests from Milestone 9 (Embedded And Server Host APIs) still pass.
6. All Phase 2 integration tests from Milestone 9 (Guest SDK, CLI, Simulator, Templates, Fixtures, And Debugging) still pass.
7. All Phase 3 integration tests from Milestone 9 (Telemetry, Tracing, Audit, Redaction, Health, And Operator Actions) still pass.
8. Any regression is recorded with:
   - The test ID and milestone.
   - The observed behavior.
   - The expected behavior.
   - The approval status (approved variability or defect).

> **Non-normative note.**
Cross-milestone fixtures ensure that Milestone 9 Phase 4 does not
introduce regressions in earlier milestone behavior.
Compatibility, upgrades, migrations, deployment, and horizontal coordination
are additive; they MUST NOT alter the behavior of earlier milestone contracts.

### 49.4.7 Rollback verification

Rollback MUST restore host state correctly after upgrade failure.
The test MUST verify that:

1. Upgrade failure triggers rollback to pre-upgrade checkpoint.
2. Migration interruption triggers rollback to pre-migrate checkpoint.
3. Incompatible agent state triggers rollback to pre-migrate checkpoint.
4. Stale worker triggers rollback to pre-migrate checkpoint.
5. Replay mismatch triggers rollback to pre-migrate checkpoint.
6. Rollback restores state from checkpoint correctly.
7. Rollback restores configuration from checkpoint correctly.
8. Rollback restores compatibility matrix from checkpoint correctly.
9. Rollback is irreversible (cannot rollback past a successful upgrade).
10. Rollback is logged at `ERROR` level.
11. Rollback is audited (audit event for rollback).

### 49.4.8 Checkpoint verification

Checkpoints MUST be created correctly at all required points.
The test MUST verify that:

1. Pre-upgrade checkpoint created before upgrade begins.
2. Post-upgrade checkpoint created after upgrade completes.
3. Pre-expand checkpoint created before expand step begins.
4. Post-expand checkpoint created after expand step completes.
5. Pre-migrate checkpoint created before migrate step begins.
6. Post-migrate checkpoint created after migrate step completes.
7. Pre-contract checkpoint created before contract step begins.
8. Post-contract checkpoint created after contract step completes.
9. Checkpoints are idempotent (same state produces same checkpoint).
10. Checkpoints are tamper-evident (cryptographic hashing).
11. Checkpoints are retained per retention policy.

### 49.4.9 Mixed-version window verification

Mixed-version windows MUST remain within configured limits.
The test MUST verify that:

1. Expand window remains within time and state limits.
2. Migrate window remains within time and state limits.
3. Contract window remains within time and state limits.
4. Window limit exceeded triggers upgrade failure diagnostic.
5. Window limit exceeded triggers automatic rollback (if configured).
6. Window limit exceeded is logged at `ERROR` level.
7. Window limit exceeded is audited (audit event for window limit exceeded).

### 49.4.10 Horizontal coordination verification

Horizontal coordination MUST ensure only one node is active at a time.
The test MUST verify that:

1. Leader election succeeds (leader-based coordination).
2. Leader health checks succeed (leader responsive).
3. Leader failover succeeds (if leader becomes unhealthy).
4. Consensus protocol succeeds (leaderless coordination).
5. Conflict resolution succeeds (if conflicting state detected).
6. Split-brain scenarios are detected (multiple leaders, stale leader, conflicting state).
7. Split-brain scenarios are resolved (via leader election or consensus).
8. Split-brain resolution is logged at `ERROR` level.
9. Split-brain resolution is audited (audit event for resolution).

### 49.4.11 Deployment verification

Deployment procedures MUST execute correctly.
The test MUST verify that:

1. Single-node packaging deploys host correctly.
2. Durable volumes persist host state across restarts.
3. Graceful drain completes successfully (stop-accepting, complete-in-flight,
   drain-mailbox, drain-outbox, drain-completed).
4. Restart restores host from last checkpoint.
5. Backup preserves host state correctly.
6. Restore restores host state correctly.
7. Disaster recovery procedures execute correctly (failover, failback, recovery).
8. Deployment procedures are logged at appropriate level (INFO, WARN, ERROR).
9. Deployment procedures are audited (audit event for each procedure).

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Compatibility matrix components | Section 49.4.1 | MUST | Must verify compatibility for all components listed in section 49.1.1. |
| Upgrade step verification | Section 49.4.1 | MUST | Must verify all upgrade steps (pre-upgrade, expand, migrate, contract, post-upgrade). |
| Checkpoint timing verification | Section 49.4.1 | MUST | Must verify checkpoints at all required points. |
| Mixed-version window limit verification | Section 49.4.1 | MUST | Must verify windows remain within limits. |
| Unsupported downgrade verification | Section 49.4.1 | MUST | Must verify downgrades are rejected. |
| Rollout step verification | Section 49.4.1 | MUST | Must verify all rollout steps (validation, canary, observation, promotion, rollback, quarantine). |
| Deployment procedure verification | Section 49.4.1 | MUST | Must verify all deployment procedures (single-node, durable volumes, drain, restart, backup, restore, disaster recovery). |
| Horizontal coordination verification | Section 49.4.1 | MUST | Must verify all horizontal coordination (routing, activation, placement, fencing, split-brain). |
| Cross-milestone fixtures | Section 49.4.6 | MUST | Must include all fixtures listed in section 49.4.6. |
| Regression approval | Section 49.4.6 | Required | Must record and approve or reject any regression. |
| Rollback verification | Section 49.4.7 | MUST | Must verify rollback restores state correctly and is irreversible. |
| Checkpoint verification | Section 49.4.8 | MUST | Must verify checkpoints created correctly at all required points. |
| Mixed-version window verification | Section 49.4.9 | MUST | Must verify windows remain within limits and trigger failure on exceed. |
| Horizontal coordination verification | Section 49.4.10 | MUST | Must verify only one node active and split-brain detected/resolved. |
| Deployment verification | Section 49.4.11 | MUST | Must verify all deployment procedures execute correctly. |

## Rationale and evidence (non-normative)

Integration tests for Milestone 9 Phase 4 verify that compatibility,
upgrades, migrations, deployment, and horizontal coordination work
correctly across their real dependency boundaries.
These tests prove the phase works as an integrated behavior and preserve
reproducible evidence for later milestone and release gates.

The test suite exercises:
- Successful flows with complete evidence retention.
- Malformed and incompatible inputs with stable diagnostics.
- Stale and duplicate inputs with proper rejection.
- Boundary and limit inputs with configured enforcement.
- Timeout, cancellation, and unavailable dependency handling.
- Cross-milestone fixture regression to ensure no behavioral changes.
- Rollback verification (state restoration, irreversibility).
- Checkpoint verification (creation at all required points).
- Mixed-version window verification (limits enforced).
- Horizontal coordination verification (only one node active, split-brain resolved).
- Deployment verification (all procedures execute correctly).

Passing this test suite is a prerequisite for promoting this chapter to
`status: normative` and for advancing Milestone 9 to Phase 5.
