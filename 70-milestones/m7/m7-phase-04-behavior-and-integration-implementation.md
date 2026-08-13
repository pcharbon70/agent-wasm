---
title: "Phase 4 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: developing
tags:
  - milestone-07
  - phase-04
  - implementation
  - behavior
  - integration
  - approvals
  - quotas
  - secret-leases
aliases:
  - "M7-P4 Behavior And Integration Implementation"
---

# Phase 4 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 4.2 from Phase 4 plan:
**Behavior And Integration** for Threads, Checkpoints, Memory, Approvals,
Quotas, And Secret Leases.

## Implementation notes

### Subtask 4.2.1.1 - Approval requests

Defined approval requests, eligible approvers, decision options, expiry,
escalation, and causally linked approval-result signals.

**Approval request schema:**

| Field | Content | Source |
|-------|---------|--------|
| `approval_id` | The `ApprovalId` of the approval request. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that requested approval. | Host runtime |
| `tenant_scope` | The tenant scope of the approval request. | Host runtime |
| `request_type` | The type of approval request (`action`, `plan`, `tool`, `code`, `memory`, `quota`). | Host runtime |
| `request_details` | The details of the approval request. | Host runtime |
| `eligible_approvers` | The list of eligible approvers. | Host runtime |
| `decision_options` | The decision options (`approve`, `reject`, `modify`, `delegate`). | Host runtime |
| `expiry` | The expiry timestamp of the approval request. | Host runtime |
| `escalation_policy` | The escalation policy for the approval request. | Host runtime |
| `status` | The approval status (`pending`, `approved`, `rejected`, `modified`, `delegated`, `expired`, `cancelled`). | Host runtime |
| `created_at` | The ISO 8601 timestamp of approval creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last approval update. | Host clock |
| `decided_at` | The ISO 8601 timestamp of the approval decision (null if pending). | Host clock |
| `decided_by` | The `TenantQualifiedAgentAddress` that decided the approval (null if pending). | Host runtime |

**Eligible approvers:**

Eligible approvers are defined by:
- `approver_type`: The type of approver (`user`, `agent`, `role`, `group`).
- `approver_address`: The `TenantQualifiedAgentAddress` of the approver (if type is `user` or `agent`).
- `role`: The role of the approver (if type is `role`).
- `group`: The group of the approver (if type is `group`).

**Decision options:**

Decision options define what actions the approver can take:
- `approve`: Approve the request as-is.
- `reject`: Reject the request.
- `modify`: Modify the request and resubmit.
- `delegate`: Delegate the approval to another approver.

**Expiry:**

Expiry defines when the approval request expires.
- `expiry_type`: The type of expiry (`fixed`, `relative`, `conditional`).
- `expiry_timestamp`: The fixed expiry timestamp (if type is `fixed`).
- `expiry_duration`: The relative duration (if type is `relative`).
- `expiry_condition`: The conditional expression (if type is `conditional`).

**Escalation policy:**

Escalation policy defines what happens when an approval request is not decided in time.
- `escalation_enabled`: Whether escalation is enabled.
- `escalation_timeout`: The timeout for escalation.
- `escalation_approvers`: The list of escalators.
- `escalation_action`: The action to take on escalation (`notify`, `auto_approve`, `auto_reject`).

**Causally linked approval-result signals:**

When an approval is decided, a causally linked signal is emitted.
The signal includes:
- `signal_id`: The `SignalId` of the approval-result signal.
- `approval_id`: The `ApprovalId` of the approval request.
- `decision`: The decision made (`approve`, `reject`, `modify`, `delegate`).
- `decided_by`: The `TenantQualifiedAgentAddress` that decided.
- `decided_at`: The ISO 8601 timestamp of the decision.
- `causal_link`: The causal link to the approval request.

**Approval flow:**

1. **Request**: The agent submits an approval request.
2. **Validation**: The host validates the approval request.
3. **Routing**: The host routes the approval request to eligible approvers.
4. **Notification**: The host notifies eligible approvers.
5. **Decision**: The approver makes a decision.
6. **Signal**: The host emits a causally linked approval-result signal.
7. **Action**: The agent acts on the approval decision.

**Approval behaviors:**

1. **Pending approval**: The approval request is pending a decision.
2. **Approved**: The approval request is approved.
3. **Rejected**: The approval request is rejected.
4. **Modified**: The approval request is modified and resubmitted.
5. **Delegated**: The approval request is delegated to another approver.
6. **Expired**: The approval request has expired without a decision.
7. **Cancelled**: The approval request is cancelled by the requester.

### Subtask 4.2.1.2 - Quotas

Defined tenant/agent/model/tool quotas and durable reservation, consumption,
release, and reconciliation records.

**Quota schema:**

| Field | Content | Source |
|-------|---------|--------|
| `quota_id` | The `QuotaId` of the quota. | Host runtime |
| `quota_type` | The type of quota (`tenant`, `agent`, `model`, `tool`). | Host runtime |
| `scope` | The scope of the quota (tenant, agent, model, or tool identifier). | Host runtime |
| `limit` | The quota limit. | Host runtime |
| `unit` | The unit of the quota (e.g., `requests`, `tokens`, `cost`, `time`). | Host runtime |
| `window` | The window of the quota (e.g., `hourly`, `daily`, `monthly`, `lifetime`). | Host runtime |
| `current_usage` | The current usage of the quota. | Host runtime |
| `reserved_usage` | The reserved usage of the quota. | Host runtime |
| `created_at` | The ISO 8601 timestamp of quota creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last quota update. | Host clock |
| `status` | The quota status (`active`, `exhausted`, `suspended`, `deleted`). | Host runtime |

**Reservation schema:**

| Field | Content | Source |
|-------|---------|--------|
| `reservation_id` | The `ReservationId` of the reservation. | Host runtime |
| `quota_id` | The `QuotaId` of the quota. | Host runtime |
| `requester` | The `TenantQualifiedAgentAddress` that made the reservation. | Host runtime |
| `amount` | The amount reserved. | Host runtime |
| `purpose` | The purpose of the reservation. | Host runtime |
| `expires_at` | The ISO 8601 timestamp of the reservation expiry. | Host clock |
| `created_at` | The ISO 8601 timestamp of the reservation creation. | Host clock |
| `status` | The reservation status (`active`, `consumed`, `released`, `expired`). | Host runtime |

**Consumption schema:**

| Field | Content | Source |
|-------|---------|--------|
| `consumption_id` | The `ConsumptionId` of the consumption. | Host runtime |
| `quota_id` | The `QuotaId` of the quota. | Host runtime |
| `requester` | The `TenantQualifiedAgentAddress` that consumed the quota. | Host runtime |
| `amount` | The amount consumed. | Host runtime |
| `purpose` | The purpose of the consumption. | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the consumption. | Host clock |

**Release schema:**

| Field | Content | Source |
|-------|---------|--------|
| `release_id` | The `ReleaseId` of the release. | Host runtime |
| `reservation_id` | The `ReservationId` of the reservation. | Host runtime |
| `releaser` | The `TenantQualifiedAgentAddress` that released the reservation. | Host runtime |
| `amount` | The amount released. | Host runtime |
| `reason` | The reason for the release. | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the release. | Host clock |

**Reconciliation schema:**

| Field | Content | Source |
|-------|---------|--------|
| `reconciliation_id` | The `ReconciliationId` of the reconciliation. | Host runtime |
| `quota_id` | The `QuotaId` of the quota. | Host runtime |
| `expected_usage` | The expected usage of the quota. | Host runtime |
| `actual_usage` | The actual usage of the quota. | Host runtime |
| `discrepancy` | The discrepancy between expected and actual usage. | Host runtime |
| `resolution` | The resolution of the discrepancy (if any). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of the reconciliation. | Host clock |

**Quota enforcement points:**

1. **Reservation**: Before reserving quota, the host checks if the quota has available capacity.
2. **Consumption**: Before consuming quota, the host checks if the quota has available capacity.
3. **Release**: After releasing quota, the host updates the quota usage.
4. **Reconciliation**: Periodically, the host reconciles quota usage.

**Quota behaviors:**

1. **Active quota**: The quota is active and can be used.
2. **Exhausted quota**: The quota has reached its limit.
3. **Suspended quota**: The quota is suspended (e.g., due to billing issues).
4. **Deleted quota**: The quota is deleted.

**Quota windows:**

- `hourly`: Quota resets every hour.
- `daily`: Quota resets every day.
- `monthly`: Quota resets every month.
- `lifetime`: Quota does not reset.

### Subtask 4.2.1.3 - Secret leases

Defined secret leases by principal, purpose, resource, expiry, non-exportability,
audit reference, and revocation behavior.

**Secret lease schema:**

| Field | Content | Source |
|-------|---------|--------|
| `lease_id` | The `LeaseId` of the secret lease. | Host runtime |
| `principal` | The `TenantQualifiedAgentAddress` that holds the lease. | Host runtime |
| `purpose` | The purpose of the lease (e.g., `model_access`, `tool_access`, `storage_access`). | Host runtime |
| `resource` | The resource that the lease covers. | Host runtime |
| `expiry` | The expiry timestamp of the lease. | Host runtime |
| `non_exportable` | Whether the secret can be exported from the host. | Host runtime |
| `audit_reference` | The audit reference for the lease. | Host runtime |
| `created_at` | The ISO 8601 timestamp of lease creation. | Host clock |
| `updated_at` | The ISO 8601 timestamp of the last lease update. | Host clock |
| `status` | The lease status (`active`, `expired`, `revoked`, `deleted`). | Host runtime |

**Non-exportability:**

Non-exportability prevents secrets from being exported from the host.
- `non_exportable`: If true, the secret cannot be exported.
- `export_policy`: Defines what types of exports are allowed (if non_exportable is false).

**Audit reference:**

Audit reference links the lease to an audit record.
- `audit_reference`: The reference to the audit record.
- `audit_scope`: The scope of the audit (e.g., `full`, `partial`).

**Revocation behavior:**

Revocation behavior defines what happens when a lease is revoked.
- `revocation_action`: The action to take on revocation (`revoke`, `notify`, `log`).
- `revocation_timeout`: The timeout for revocation.
- `revocation_approvers`: The list of approvers for revocation.

**Secret lease lifecycle:**

1. **Creation**: The host creates a secret lease for a principal.
2. **Access**: The principal accesses the secret using the lease.
3. **Renewal**: The principal renews the lease before expiry.
4. **Expiry**: The lease expires and the principal loses access.
5. **Revocation**: The host revokes the lease before expiry.
6. **Deletion**: The lease is deleted.

**Secret lease behaviors:**

1. **Active lease**: The lease is active and the principal can access the secret.
2. **Expired lease**: The lease has expired and the principal loses access.
3. **Revoked lease**: The lease has been revoked and the principal loses access.
4. **Deleted lease**: The lease is deleted.

**Secret lease security:**

1. **Non-exportability**: Secrets cannot be exported from the host.
2. **Audit logging**: All lease operations are logged for audit.
3. **Revocation**: Leases can be revoked before expiry.
4. **Expiry**: Leases have a configurable expiry.
5. **Access control**: Only authorized principals can access secrets.

## Key design decisions

1. **Approval workflow**: Approval requests follow a structured workflow with eligible approvers, decision options, expiry, and escalation.

2. **Causally linked signals**: Approval decisions emit causally linked signals for traceability.

3. **Quota types**: Four quota types (tenant, agent, model, tool) support different scoping levels.

4. **Reservation and consumption**: Quotas support reservation and consumption for accurate tracking.

5. **Reconciliation**: Periodic reconciliation ensures quota accuracy.

6. **Quota windows**: Quotas support configurable windows (hourly, daily, monthly, lifetime).

7. **Secret leases**: Secret leases provide secure access to secrets with non-exportability and audit logging.

8. **Lease lifecycle**: Secret leases have a clear lifecycle (creation, access, renewal, expiry, revocation, deletion).

9. **Revocation**: Secret leases can be revoked before expiry for security.

10. **Tenant isolation**: All quotas and leases are scoped to tenant boundaries.

## Open questions

1. Should approval requests support parallel approvals (e.g., require N out of M approvers)?

2. Should quotas support burst allowances (temporary overages)?

3. Should secret leases support hierarchical scoping?

4. Should approval requests support conditional decisions (e.g., "approve if X")?

5. Should quotas support predictive scaling (e.g., increase limit based on usage patterns)?

6. Should secret leases support automatic renewal?

7. Should approval requests support time-boxed decisions (e.g., "approve for 1 hour")?

8. Should quotas support shared pools (e.g., multiple agents sharing a quota)?

9. Should secret leases support secret rotation?

10. Should approval requests support auto-approval for low-risk requests?

11. Should quotas support per-request cost tracking (e.g., track cost per tool execution)?

12. Should secret leases support secret versioning (e.g., rotate secrets without invalidating leases)?

## Cross-references

### Earlier chapters

- [13-directives-strategies-continuations-and-terminal-states.md](../../60-specification/13-directives-strategies-continuations-and-terminal-states.md)
- [27-effect-handlers-attempts-idempotency-and-result-signals.md](../../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- [30-threat-model-principals-trust-classes-and-grant-vocabulary.md](../../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- [31-capability-policy-attenuation-limits-and-enforcement.md](../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)

### Related chapters (Phase 4)

- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md)
- [44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md](../../60-specification/44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md)
