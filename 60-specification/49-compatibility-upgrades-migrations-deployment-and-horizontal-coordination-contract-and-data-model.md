---
title: "Compatibility Upgrades Migrations Deployment And Horizontal Coordination Contract And Data Model"
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
  - contract
  - data-model
aliases:
  - "M9-P4-S1 Contract And Data Model"
---

# Compatibility Upgrades Migrations Deployment And Horizontal Coordination Contract And Data Model

## Status and authority

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/phase-04-compatibility-upgrades-migrations-deployment-and-horizontal-coordination.md)
of
[Milestone 9](../.spec/planning/agentic-system/milestone-09-production-platform-and-developer-experience/README.md)
--
Production Platform And Developer Experience.
It establishes the contract and data model for compatibility, upgrades,
migrations, deployment, and horizontal coordination.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests in
Section [Phase 4 Integration Tests](49-compatibility-upgrades-migrations-deployment-and-horizontal-coordination-phase-4-integration-tests.md)
and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Guest SDK Contracts Fixtures And Milestone Acceptance](05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md),
[Embedded And Server Host APIs Configuration And Packaging Contract And Data Model](46-embedded-and-server-host-apis-configuration-and-packaging-contract-and-data-model.md),
[Guest SDK CLI Simulator Templates Fixtures And Debugging Contract And Data Model](47-guest-sdk-cli-simulator-templates-fixtures-and-debugging-contract-and-data-model.md),
[Telemetry Tracing Audit Redaction Health And Operator Actions Contract And Data Model](48-telemetry-tracing-audit-redaction-health-and-operator-actions-contract-and-data-model.md).

## 49.1 Contract And Data Model

> **Normative definition.**
The following surfaces make upgrades and deployment changes reversible
while preserving durable agents, artifacts, protocols, and ownership.

### 49.1.1 Compatibility Matrices

> **Normative definition.**
The host maintains compatibility matrices for the following components:

| Component | Compatibility Scope |
| --- | --- |
| `host` | Host version compatibility (e.g., host 2.x compatible with host 2.y). |
| `protocol` | Protocol version compatibility (e.g., protocol 1.0 compatible with 1.1). |
| `manifest` | Manifest schema compatibility (e.g., manifest 2.0 compatible with 2.1). |
| `guest-sdk` | Guest SDK version compatibility (e.g., SDK 3.x compatible with 3.y). |
| `plugin` | Plugin version compatibility (e.g., plugin 1.0 compatible with 1.1). |
| `artifact` | Artifact version compatibility (e.g., artifact 2.0 compatible with 2.1). |
| `schema` | Schema version compatibility (e.g., schema 1.0 compatible with 1.1). |
| `strategy` | Strategy version compatibility (e.g., strategy 2.0 compatible with 2.1). |
| `storage` | Storage backend compatibility (e.g., SQLite 3.x compatible with 3.y). |
| `runtime` | Runtime family compatibility (e.g., Extism 1.x compatible with 1.y). |
| `provider` | Provider API compatibility (e.g., provider 1.0 compatible with 1.1). |

> **Non-normative note.**
Compatibility matrices are defined as:
- `compatible-with`: List of versions that are compatible with the current version.
- `incompatible-with`: List of versions that are incompatible with the current version.
- `deprecated-in`: List of versions where the current version is deprecated.
- `sunset-in`: List of versions where the current version is sunset.

Compatibility is checked at:
- Host startup (host version compatibility).
- Signal submission (protocol version compatibility).
- Artifact registration (artifact schema compatibility).
- Plugin composition (plugin version compatibility).
- Strategy selection (strategy version compatibility).

### 49.1.2 Upgrade Sequencing

> **Normative definition.**
Upgrades follow a defined sequencing:

| Step | Description |
| --- | --- |
| `expand` | Add new components (e.g., new schema version, new runtime adapter). |
| `migrate` | Migrate data (e.g., schema migration, state migration). |
| `contract` | Remove old components (e.g., remove deprecated schema version, remove old runtime adapter). |

> **Non-normative note.**
Upgrade sequencing ensures:
- Backward compatibility during migration (old components still work).
- Forward compatibility during migration (new components can be used).
- Clean removal of old components after migration is complete.

### 49.1.3 Checkpoints

> **Normative definition.**
Checkpoints capture the host state at specific points during upgrades:

| Checkpoint | Timing |
| --- | --- |
| `pre-expand` | Before expand step begins. |
| `post-expand` | After expand step completes. |
| `pre-migrate` | Before migrate step begins. |
| `post-migrate` | After migrate step completes. |
| `pre-contract` | Before contract step begins. |
| `post-contract` | After contract step completes. |
| `pre-upgrade` | Before upgrade begins. |
| `post-upgrade` | After upgrade completes. |

> **Non-normative note.**
Checkpoints include:
- State snapshot (durable agents, artifacts, protocols, ownership).
- Configuration snapshot (host configuration, runtime configuration).
- Metadata snapshot (version, compatibility matrix, migration state).

Checkpoints are used for:
- Rollback if upgrade fails.
- Verification that upgrade completed successfully.
- Evidence for compliance auditing.

### 49.1.4 Rollback

> **Normative definition.**
Rollback restores the host to a previous checkpoint if upgrade fails:

| Rollback Trigger | Behavior |
| --- | --- |
| `upgrade-failure` | Rollback to pre-upgrade checkpoint. |
| `migration-interruption` | Rollback to pre-migrate checkpoint. |
| `incompatible-agent-state` | Rollback to pre-contract checkpoint. |
| `stale-worker` | Rollback to pre-expand checkpoint. |
| `replay-mismatch` | Rollback to pre-migrate checkpoint. |

> **Non-normative note.**
Rollback includes:
- Restoring state from checkpoint.
- Restoring configuration from checkpoint.
- Restoring compatibility matrix from checkpoint.
- Logging rollback event as audit event.

Rollback is irreversible (cannot rollback past a successful upgrade).

### 49.1.5 Mixed-Version Windows

> **Normative definition.**
Mixed-version windows allow multiple versions to coexist during upgrades:

| Window | Description |
| --- | --- |
| `expand-window` | New components added; old components still operational. |
| `migrate-window` | Migration in progress; both old and new components active. |
| `contract-window` | Old components being removed; new components operational. |

> **Non-normative note.**
Mixed-version windows are bounded by:
- Time limits (e.g., migrate-window must complete within 24 hours).
- State limits (e.g., migrate-window must complete within 10,000 state revisions).

Exceeding mixed-version window limits triggers:
- Upgrade failure diagnostic.
- Automatic rollback (if configured).
- Manual intervention required.

### 49.1.6 Unsupported Downgrade Behavior

> **Normative definition.**
Downgrades are unsupported and produce stable diagnostics:

| Downgrade Attempt | Diagnostic | Behavior |
| --- | --- | --- |
| `host-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `protocol-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `manifest-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `sdk-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `plugin-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `artifact-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `schema-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `strategy-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `storage-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `runtime-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |
| `provider-downgrade` | `upgrade.downgrade.unsupported` | Reject downgrade. Log at `ERROR` level. |

> **Non-normative note.**
Downgrades are unsupported because:
- Data migrations may not be reversible.
- Compatibility matrices may not support reverse compatibility.
- State may have been altered by new components.

### 49.1.7 Artifact/Plugin Rollout

> **Normative definition.**
Artifact and plugin rollout follows a defined process:

| Step | Description |
| --- | --- |
| `validation` | Validate artifact/plugin before rollout. |
| `canary` | Roll out to canary tenants/agents (e.g., 1-5%). |
| `targeting` | Roll out to targeted tenants/agents. |
| `observation` | Observe canary behavior (e.g., error rates, latency). |
| `promotion` | Promote canary to full rollout if observation successful. |
| `rollback` | Rollback rollout if observation fails. |
| `quarantine` | Quarantine artifact/plugin if observation reveals issues. |

> **Non-normative note.**
Rollout configuration includes:
- Canary percentage (e.g., 1%, 5%, 10%).
- Target tenants/agents (e.g., specific tenant IDs, agent types).
- Observation metrics (e.g., error rates, latency, trap counts).
- Promotion criteria (e.g., error rate < 1%, latency < 100ms).
- Rollback criteria (e.g., error rate > 5%, latency > 1s).

### 49.1.8 Single-Node Packaging

> **Normative definition.**
Single-node packaging defines the host deployment as a single unit:

| Component | Description |
| --- | --- |
| `host-binary` | Host executable (e.g., `agent-wasm`). |
| `configuration` | Host configuration files (e.g., `config.yaml`). |
| `storage` | Storage backend (e.g., SQLite, PostgreSQL). |
| `runtime` | Runtime adapters (e.g., Extism, Wazero, Wasmtime). |
| `observability` | Observability exporters (e.g., OTLP, Prometheus). |

> **Non-normative note.**
Single-node packaging is intended for:
- Development and testing environments.
- Small-scale production deployments.
- Edge deployments with limited resources.

### 49.1.9 Durable Volume Requirements

> **Normative definition.**
Durable volumes persist host state across restarts:

| Volume | Contents | Persistence |
| --- | --- | --- |
| `state` | Durable agents, artifacts, protocols, ownership. | Persistent across restarts. |
| `configuration` | Host configuration, runtime configuration. | Persistent across restarts. |
| `observability` | Logs, metrics, traces, audit events. | Persistent across restarts (per retention policy). |
| `backup` | Backup snapshots. | Persistent across restarts. |

> **Non-normative note.**
Durable volumes are mounted as:
- Local filesystem volumes (e.g., `/data/state`).
- Network filesystem volumes (e.g., NFS, SMB).
- Cloud storage volumes (e.g., S3, GCS, Azure Blob).

### 49.1.10 Graceful Drain

> **Normative definition.**
Graceful drain stops accepting new requests and completes in-flight requests:

| Drain Phase | Behavior |
| --- | --- |
| `stop-accepting` | Stop accepting new signals and instructions. |
| `complete-in-flight` | Complete in-flight signals, instructions, and turns. |
| `drain-mailbox` | Drain mailbox queue (process remaining signals). |
| `drain-outbox` | Drain outbox queue (send remaining messages). |
| `drain-completed` | All queues drained; host ready for shutdown. |

> **Non-normative note.**
Graceful drain is triggered by:
- Operator action (`drain`).
- Upgrade begin.
- Shutdown.
- Deployment change.

Graceful drain has a configurable timeout (default: 30 seconds).
Exceeding timeout triggers:
- Drain failure diagnostic.
- Force shutdown (if configured).
- Manual intervention required.

### 49.1.11 Restart

> **Normative definition.**
Restart restores the host from the last checkpoint:

| Restart Type | Behavior |
| --- | --- |
| `graceful-restart` | Restart after graceful drain. |
| `force-restart` | Restart without graceful drain (e.g., crash recovery). |
| `rolling-restart` | Restart one node at a time in a multi-node deployment. |

> **Non-normative note.**
Restart includes:
- Loading state from last checkpoint.
- Loading configuration from last checkpoint.
- Loading compatibility matrix from last checkpoint.
- Resuming operations from last checkpoint.

### 49.1.12 Backup And Restore

> **Normative definition.**
Backup and restore preserve host state across deployments:

| Operation | Description |
| --- | --- |
| `backup` | Create a backup snapshot of host state. |
| `restore` | Restore host state from a backup snapshot. |
| `verify` | Verify backup snapshot integrity. |

> **Non-normative note.**
Backup includes:
- State snapshot (durable agents, artifacts, protocols, ownership).
- Configuration snapshot (host configuration, runtime configuration).
- Compatibility matrix snapshot.
- Observability data (per retention policy).

Restore includes:
- Restoring state from backup.
- Restoring configuration from backup.
- Restoring compatibility matrix from backup.
- Restoring observability data from backup.

### 49.1.13 Disaster Recovery

> **Normative definition.**
Disaster recovery procedures restore host operations after catastrophic failure:

| Procedure | Description |
| --- | --- |
| `failover` | Failover to secondary deployment. |
| `failback` | Failback to primary deployment. |
| `recovery` | Recovery from backup after primary deployment failure. |

> **Non-normative note.**
Disaster recovery includes:
- Automated failover (if secondary deployment available).
- Manual failback (after primary deployment restored).
- Backup restoration (if secondary deployment unavailable).

### 49.1.14 Horizontal Routing

> **Normative definition.**
Horizontal routing distributes requests across multiple host nodes:

| Routing Type | Description |
| --- | --- |
| `replaceable` | Nodes can be replaced without service interruption. |
| `load-balanced` | Requests distributed based on load (e.g., round-robin, least-connections). |
| `tenant-aware` | Requests routed based on tenant affinity. |
| `artifact-aware` | Requests routed based on artifact affinity. |

> **Non-normative note.**
Horizontal routing is implemented via:
- Load balancer (e.g., NGINX, HAProxy).
- Service mesh (e.g., Istio, Linkerd).
- Custom routing logic.

### 49.1.15 Activation Coordination

> **Normative definition.**
Activation coordination ensures only one host node is active at a time:

| Coordination Type | Description |
| --- | --- |
| `leader-based` | One node is leader; other nodes are followers. |
| `leaderless` | All nodes are equal; coordination via consensus. |

> **Non-normative note.**
Leader-based coordination includes:
- Leader election (e.g., Raft, Paxos).
- Leader health checks.
- Leader failover (if leader becomes unhealthy).

Leaderless coordination includes:
- Consensus protocol (e.g., Paxos, Raft).
- Conflict resolution (e.g., last-writer-wins, custom logic).

### 49.1.16 Placement

> **Normative definition.**
Placement determines which host node processes which requests:

| Placement Type | Description |
| --- | --- |
| `static` | Requests routed based on static configuration. |
| `dynamic` | Requests routed based on dynamic state (e.g., load, health). |
| `affinity-based` | Requests routed based on affinity (e.g., tenant, artifact). |

> **Non-normative note.**
Placement is configured via:
- Load balancer configuration.
- Service mesh configuration.
- Custom placement logic.

### 49.1.17 Fencing

> **Normative definition.**
Fencing prevents stale operations from affecting current state:

| Fencing Type | Description |
| --- | --- |
| `epoch-based` | Each upgrade has a unique epoch; stale epochs rejected. |
| `token-based` | Each upgrade has a unique token; stale tokens rejected. |
| `version-based` | Each upgrade has a unique version; stale versions rejected. |

> **Non-normative note.**
Fencing is applied at:
- State mutations (e.g., state revision commits).
- Signal processing (e.g., signal admission).
- Instruction processing (e.g., instruction submission).

### 49.1.18 Split-Brain Diagnostics

> **Normative definition.**
Split-brain diagnostics detect and resolve split-brain scenarios:

| Scenario | Diagnostic | Behavior |
| --- | --- | --- |
| `multiple-leaders` | `coordination.split-brain.multiple-leaders` | Resolve via leader election. |
| `stale-leader` | `coordination.split-brain.stale-leader` | Resolve via leader failover. |
| `conflicting-state` | `coordination.split-brain.conflicting-state` | Resolve via conflict resolution. |

> **Non-normative note.**
Split-brain diagnostics include:
- Leader election logs.
- Conflict resolution logs.
- Audit events for split-brain resolution.

## Variability and limits

See [Variability register](#variability-register).

### Variability register

| Item | Location | Nature | Constraint |
| --- | --- | --- | --- |
| Compatibility matrix components | Section 49.1.1 | Required | Must include all components listed in the table. |
| Upgrade sequencing steps | Section 49.1.2 | Required | Must include all steps listed in the table (expand, migrate, contract). |
| Checkpoint timing | Section 49.1.3 | Required | Must include all checkpoints listed in the table. |
| Rollback triggers | Section 49.1.4 | Required | Must include all triggers listed in the table. |
| Mixed-version window limits | Section 49.1.5 | Implementation-defined | Must document time and state limits for each window. |
| Unsupported downgrade diagnostics | Section 49.1.6 | Required | Must include all diagnostics listed in the table. |
| Rollout steps | Section 49.1.7 | Required | Must include all steps listed in the table. |
| Rollout configuration | Section 49.1.7 | Implementation-defined | Must document canary percentage, observation metrics, promotion/rollback criteria. |
| Single-node packaging components | Section 49.1.8 | Required | Must include all components listed in the table. |
| Durable volume types | Section 49.1.9 | Required | Must include all volumes listed in the table. |
| Graceful drain phases | Section 49.1.10 | Required | Must include all phases listed in the table. |
| Graceful drain timeout | Section 49.1.10 | Implementation-defined | Must document timeout duration. |
| Restart types | Section 49.1.11 | Required | Must include all types listed in the table. |
| Backup and restore operations | Section 49.1.12 | Required | Must include all operations listed in the table. |
| Disaster recovery procedures | Section 49.1.13 | Required | Must include all procedures listed in the table. |
| Horizontal routing types | Section 49.1.14 | MAY | Must support at least one routing type. Other types are permitted. |
| Activation coordination types | Section 49.1.15 | Required | Must include at least one coordination type. |
| Placement types | Section 49.1.16 | MAY | Must support at least one placement type. Other types are permitted. |
| Fencing types | Section 49.1.17 | Required | Must include at least one fencing type. |
| Split-brain diagnostics | Section 49.1.18 | Required | Must include all diagnostics listed in the table. |

## Rationale and evidence (non-normative)

The contract and data model for Milestone 9 Phase 4 makes upgrades and
deployment changes reversible while preserving durable agents, artifacts,
protocols, and ownership.
Compatibility matrices ensure that components are compatible before
upgrades and deployments.
Upgrade sequencing (expand, migrate, contract) ensures that upgrades are
performed in a safe and controlled manner.
Checkpoints capture host state at specific points during upgrades, enabling
rollback if upgrades fail.
Rollback restores host state to a previous checkpoint if upgrade fails.
Mixed-version windows allow multiple versions to coexist during upgrades,
bounded by time and state limits.
Unsupported downgrades produce stable diagnostics to prevent data loss
and compatibility issues.
Artifact and plugin rollout follows a defined process (validation, canary,
targeting, observation, promotion, rollback, quarantine) to ensure safe
deployment.
Single-node packaging, durable volume requirements, graceful drain, restart,
backup, restore, and disaster recovery procedures define the deployment
model for single-node and multi-node deployments.
Horizontal routing, activation coordination, placement, fencing, and
split-brain diagnostics define the coordination model for multi-node
deployments.

These surfaces ensure that upgrades and deployment changes are safe,
reversible, and observable.
