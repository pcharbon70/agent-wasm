---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-01
  - model-requests
  - model-bindings
  - responses
  - streaming
  - usage
  - provider-neutral
  - credential-use
  - failure-evidence
  - diagnostics
aliases:
  - "M7-P1 Failure Evidence And Operational Notes"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).
It defines stable model-intent, binding, dispatch, response, receipt, and
usage failures together with bounded diagnostics and evidence.

Version `0.2.0` replaces the `0.1.0` diagnostics that treated an
agent-supplied provider or model as an ordinary input. Concrete selection
fields are now forbidden agent input; missing, stale, or incompatible
user-controlled bindings are distinct failures.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations. Promotion to `status: normative` requires passing evidence from
[Phase 1 Integration Tests](41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md).

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
and
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Failure Evidence And Operational Notes](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md).

## 41.3 Failure Evidence And Operational Notes

### Stable diagnostics

#### Intent and schema failures

| Diagnostic | Cause | Retry classification |
| --- | --- | --- |
| `model.intent.malformed` | Intent does not satisfy the data model. | Non-retryable until input changes. |
| `model.intent.missing_slot` | `model_slot` is absent or undeclared. | Non-retryable until input or definition changes. |
| `model.intent.forbidden_selection` | Intent includes provider, model, adapter, connection, endpoint, authentication, or credential selection. | Non-retryable security failure. |
| `model.intent.malformed_messages` | Messages are empty, invalid, or over limits. | Non-retryable until input changes. |
| `model.intent.malformed_sampling` | Sampling controls are invalid or over policy. | Non-retryable until input changes. |
| `model.intent.malformed_deadline` | Deadline is invalid or already expired. | Non-retryable until input changes. |
| `model.intent.malformed_budget` | Budget is invalid or exceeds an absolute limit. | Non-retryable until input changes. |

#### Binding and connection failures

| Diagnostic | Cause | Retry classification |
| --- | --- | --- |
| `model.binding.missing` | No active binding exists for the logical slot. | User reconfiguration required. |
| `model.binding.stale` | Binding approval, policy, connection, or catalog revision is stale. | User review or reapproval required. |
| `model.binding.incompatible` | Selected model lacks a declared feature or minimum capacity. | User reconfiguration required. |
| `model.binding.unauthorized` | Caller or tenant cannot use the binding. | Non-retryable authorization failure. |
| `model.binding.conflict` | Concurrent configuration attempted to update the same revision. | Retry configuration after reload. |
| `model.connection.unavailable` | Recorded connection is inactive or unavailable. | Retry only if the same connection recovers. |
| `model.connection.revision_mismatch` | Binding or durable request omits or changes the pinned connection revision or credential lease. | User reconfiguration or durable-record repair required. |
| `model.request.unavailable_provider` | Pinned provider is unavailable. | Retry only against the same pinned request. |
| `model.request.unavailable_model` | Pinned model is unavailable or removed. | User reconfiguration for a new intent. |

#### Request, response, and usage failures

| Diagnostic | Cause | Retry classification |
| --- | --- | --- |
| `model.request.duplicate_id` | A non-equivalent request reused an existing identity. | Non-retryable conflict. |
| `model.request.unauthorized` | Originating agent lacks `ModelAccess`. | Non-retryable authorization failure. |
| `model.request.cross_tenant_tool` | A tool definition crosses tenant authority. | Non-retryable security failure. |
| `model.request.cross_tenant_result` | Result target crosses tenant authority. | Non-retryable security failure. |
| `model.request.quota_exhausted` | Authorized budget or quota is exhausted. | Retry only after budget changes. |
| `model.request.exhausted_concurrency` | Concurrency limit is reached. | Retryable with bounded backoff. |
| `model.request.exhausted_stream` | Stream limit or buffer bound is reached. | Retryable only from a safe request boundary. |
| `model.request.tool_call_mismatch` | Returned tool is not in the request catalog. | New intent required after tool definition changes. |
| `model.request.invalid_structured_output` | Returned value fails its JSON Schema. | New intent MAY change prompt or sampling. |
| `model.request.safety_refused` | Provider or policy refuses content. | Non-retryable without content or policy change. |
| `model.request.timeout` | Request exceeds its bounded timeout. | Retryable only with idempotency reconciliation. |
| `model.request.late_response` | Result arrives after deadline or cancellation. | Not automatically retryable. |
| `model.request.cancelled` | Authorized cancellation terminated the request. | New intent required. |
| `model.request.ambiguous_billing` | Provider and host usage calculations disagree. | Reconciliation required. |
| `model.receipt.invalid_no_credential` | A no-credential receipt is used for an authenticated connection or does not match the pinned local connection revision. | Non-retryable result-admission failure. |
| `model.response.malformed_text` | Text event or final text violates encoding or bounds. | Adapter or provider correction required. |
| `model.response.malformed_structured` | Structured payload is malformed before schema validation. | Adapter or provider correction required. |
| `model.response.malformed_usage` | Usage metrics are negative, inconsistent, or over bounds. | Reconciliation required. |
| `model.adapter.error` | Pinned adapter fails while preparing or normalizing. | Retryable only if request identity is preserved. |
| `model.network.error` | Authenticated custodian transport fails. | Retryable only if outcome is reconciled. |

Credential-custody failures use the canonical `credential.*` diagnostics
defined in
[Section 44.3](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-failure-evidence-and-operational-notes.md).
The model subsystem MUST preserve those codes rather than translating them to
generic adapter or network errors.

### Failure-state invariants

On every failure, the host MUST preserve these invariants:

1. A failure before durable request commit leaves no request, outbox entry,
   quota reservation, provider call, or credential-use request.
2. A failure after durable request commit retains the pinned binding and
   idempotency identity.
3. No retry changes provider, model, adapter, connection, custodian, or binding
   revision.
4. No rejected response advances authoritative agent state.
5. Quota and usage are reconciled after uncertain provider outcomes.
6. Diagnostics and evidence contain no prompt body unless policy permits it,
   and never contain credentials, authentication headers, handle references,
   arbitrary endpoint URLs, unbounded provider errors, or raw custodian
   responses.

The connection identity in invariant 3 includes its exact revision and
credential lease linkage. A `NoCredentialReceipt` is bounded receipt evidence,
not a credential-use receipt, and MUST NOT create lease or handle evidence.

### Bounded diagnostics

Every model diagnostic MUST include:

| Field | Meaning |
| --- | --- |
| `diagnostic_code` | Stable code from this chapter or Section 44. |
| `phase` and `contract` | `milestone-07`, `phase-01`, and this contract family. |
| `boundary` | `intent-admission`, `binding-resolution`, `request-commit`, `credential-dispatch`, `stream-normalization`, `result-admission`, or `usage-reconciliation`. |
| `tenant_id` and `agent_address` | Authenticated bounded identities. |
| `intent_id` or `request_id` | Correlation identity when created. |
| `model_slot` | Logical slot. |
| `binding_id` and `binding_revision` | Only after binding resolution. |
| `provider` and `model` | Only after binding resolution and when policy permits operator visibility. |
| `retryable` | Whether the same pinned request may be retried. |
| `timestamp` | Host timestamp. |

The diagnostic MUST NOT include `credential_handle_ref`,
`handle_fingerprint`, credential bytes, authentication headers, request
bodies, provider URLs, or custodian transport details. A stable non-authority
bearing correlation fingerprint MAY be included if the conformance profile
documents its derivation.

### Evidence emission

The host MUST emit bounded evidence for:

| Evidence type | Meaning |
| --- | --- |
| `model.intent.admitted` | Intent schema and agent authority accepted. |
| `model.binding.resolved` | A specific approved binding revision was selected. |
| `model.request.created` | Durable request and outbox effect committed. |
| `model.request.dispatch_requested` | Credential-use dispatch was requested. |
| `model.request.streaming` | First valid normalized event admitted. |
| `model.response.completed` | Final response validated and committed. |
| `model.response.failed` | Final failure recorded. |
| `model.request.cancelled` | Cancellation reached its durable terminal state. |
| `model.usage.recorded` | Verified or reconciled usage committed. |

Each entry MUST include tenant, agent, intent or request identity, model slot,
binding id and revision when resolved, policy version, outcome, timestamp, and
the relevant evidence digest. Provider and model MAY be included for the
authorized user and audit roles. Credential-use evidence is emitted by
Section 44 and correlated by a non-authority-bearing use fingerprint.

Evidence MUST NOT contain credentials, authentication headers, opaque handles,
prompt or response bodies, arbitrary endpoints, or unbounded provider and
custodian payloads.

### Retry classification

The same pinned request MAY be retried only for:

- bounded connection unavailability where no provider outcome occurred;
- adapter or custodian transport failure with idempotency reconciliation;
- timeout with status reconciliation;
- concurrency exhaustion before dispatch.

The host MUST NOT automatically retry missing, stale, incompatible, or
unauthorized bindings; forbidden selection attempts; quota exhaustion;
credential-use denials; safety refusals; tool mismatches; structured-output
failures; or invalid receipts. These require user action, a new intent, or an
operator reconciliation decision.

### Implementation limits and fixed rules

| Choice | Documentation requirement |
| --- | --- |
| Maximum concurrent requests and streams | Positive implementation limits published per tenant and connection; exhaustion uses `model.request.exhausted_concurrency` or `model.request.exhausted_stream`. |
| Request and cancellation timeout | Earlier of the request deadline and the published host policy limit; expiry uses `model.request.timeout`. |
| Stream buffer size | Positive byte and event implementation limits with bounded backpressure; exhaustion uses `model.request.exhausted_stream`. |
| Usage reconciliation | Preserve provider observation and host calculation and enforce the more conservative authorized amount. |
| Diagnostic visibility | Provider/model identifiers are visible only to the authorized user and audit roles. |
| Evidence retention | Retain until the associated release leaves the support matrix and no open incident references the evidence; enforce tenant isolation and redaction throughout. |
| Local unauthenticated receipt | Exact `NoCredentialReceipt` union member from Section 41.1; reject any use on an authenticated connection with `model.receipt.invalid_no_credential`. |

### Internal mechanisms (non-normative)

Retry scheduling, backoff calculation, registry storage, and evidence-storage
backends are internal mechanisms. They may vary only when they preserve the
retry classification above, pinned selection and idempotency, timeout
boundaries, tenant isolation, retained evidence, and every externally visible
diagnostic and terminal outcome.

### Deferred work

Automatic model routing, provider fallback, speculative multi-model execution,
quality-based selection, and cost optimization are deferred. They MUST NOT be
implemented as hidden extensions to the `0.2.0` binding contract.

### Results invalidating this contract

The contract requires revision if evidence shows that:

1. A provider cannot be called through a typed custodian without exposing its
   long-lived credential to the host.
2. Provider idempotency or status reconciliation cannot prevent duplicate
   billing after an uncertain outcome.
3. Catalog metadata cannot reliably establish declared feature compatibility.
4. A provider-neutral intent cannot preserve required semantics without
   provider-specific selection by guest code.

## Variability register

The following table summarizes the variability governed by linked
declarations.

> **Non-normative note.**

| Item | Permission | Recommendation | Constraint |
| --- | --- | --- | --- |
| Diagnostic provider/model visibility | Optional | Restrict to user and audit roles | Never expose credential or handle material |
| Correlation fingerprints | Optional | Domain-separated non-authority-bearing digest | Must not be usable for credential access |
| [Retry policy](#internal-mechanisms-non-normative) | Internal mechanism | Retry only reconciled transient failures | Must preserve recorded selection and observable outcomes |
| [Evidence retention](#implementation-limits-and-fixed-rules) | Fixed requirement | Retain until the associated release leaves support and no open incident references the evidence | Must enforce tenant isolation and redaction |
| Automatic routing and fallback | Deferred | Require explicit user reconfiguration | Must not occur at runtime |

## Rationale and evidence (non-normative)

Separating intent, binding, and credential failures gives users actionable
diagnostics: a plugin bug is different from missing installation
configuration, and both are different from a custodian outage. Preserving the
original custody diagnostic also prevents an adapter from hiding a credential
scope or replay violation behind a generic network error.
