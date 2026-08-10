---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
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
  - behavior
  - integration
aliases:
  - "M7-P1 Behavior And Integration"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).
It defines installation-time model binding, request materialization, use-only
credential dispatch, response normalization, retry, cancellation, and signal
integration.

Version `0.2.0` replaces the `0.1.0` runtime resolution flow. The host no
longer resolves agent-supplied provider or model fields and no longer retries
through an automatically chosen adapter. It resolves a user-approved logical
slot once, pins that binding to the durable request, and uses the credential
custodian contract for authenticated dispatch.

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
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md),
and
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Behavior And Integration](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-behavior-and-integration.md).

## 41.2 Behavior And Integration

### Installation and configuration

When an installed agent definition declares model requirements, the host MUST:

1. Present every required logical slot and its feature and capacity
   requirements to the installing user.
2. Present compatible models only from registered, tenant-authorized
   connections and approved catalog revisions.
3. Require the user or an authorized tenant operator to choose the connection
   and model for each required slot.
4. Validate the selected model against every declared requirement.
5. Create a versioned binding outside the immutable artifact.
6. Obtain approval covering the binding, grant, policy, connection, and catalog
   revisions before enabling the definition.

The configure operation MUST NOT ask a user to place a raw credential in a
plugin manifest, agent state, BEAM environment variable, Port configuration,
or Wasm guest input when the distribution uses
`separated-credential-custody`. Credential enrollment is an independent
connection workflow owned by the user and custodian.

An unattended installer MAY accept an explicitly supplied binding file or
tenant policy object, but the authenticated user or tenant operator remains
the selection authority. The file MUST identify logical slots and registered
connections; it MUST NOT contain raw credentials.

### Binding revision behavior

A binding change MUST create a new revision and invalidate approval tied to the
previous revision. It MUST affect only intents materialized after approval of
the new revision. A request already recorded in the durable outbox remains
pinned to its original binding revision.

An agent-definition upgrade that adds a required slot or changes a slot's
features or limits MUST return the installation to
`configuration-required`. The host MUST NOT infer a replacement model from a
tenant default, a publisher hint, pricing, availability, or prior use.

Automatic model routing, quality optimization, provider failover, and
speculative multi-model execution are deferred. A future version MAY add them
only as an explicit user-approved policy with auditable selection evidence.

### Request admission and materialization

When the host receives a model intent, it MUST execute this order:

1. Authenticate the originating agent and validate the intent schema and
   bounds.
2. Reject any concrete selection, endpoint, authentication, or credential
   field.
3. Resolve `model_slot` against the effective agent definition.
4. Authorize the originating agent's `ModelAccess` for that slot, purpose,
   tools, content classification, deadline, and budget.
5. Load exactly one active approved binding revision for the slot.
6. Validate the bound model against the recorded catalog revision and current
   policy without changing the selection.
7. Materialize the concrete request and deterministic request identity.
8. Atomically commit the request, journal fact, quota reservation, and outbox
   effect before dispatch.
9. Dispatch the recorded outbox effect through the bound adapter and
   credential custodian.

Failure before step 8 MUST leave no request, quota reservation, or external
effect. Failure after step 8 is recovered through the durable effect protocol
and MUST NOT cause a new provider or model to be selected.

### Dual authorization and credential dispatch

Authenticated model dispatch has two independent authority checks:

| Principal | Capability | Scope |
| --- | --- | --- |
| Originating agent | `ModelAccess` | Logical slot, tools, content, deadline, and budget. |
| Authenticated effect worker | `CredentialUse` | Custodian, handle fingerprint, binding revision, provider operation, resource, request digest, deadline, nonce, and budget. |

The host MUST deny dispatch unless both checks allow it. `ModelAccess` MUST
NOT imply `CredentialUse`, and `CredentialUse` MUST NOT grant model choice,
tool authority, credential read, or credential export.

For `separated-credential-custody`, the dispatch flow is:

1. The reviewed adapter converts the materialized request into a typed
   provider operation without authentication material.
2. The host derives the canonical request digest and a unique attempt nonce.
3. Policy authorizes the effect worker's `CredentialUse`.
4. The host sends the typed operation, binding context, digest, nonce, deadline,
   and budget to the registered custodian over authenticated transport.
5. The custodian independently validates caller identity, tenant, agent,
   artifact digest, binding revision, provider, model, operation, resource,
   deadline, nonce, and budget.
6. The custodian executes the provider operation using its credential or
   provider-native workload identity.
7. The custodian streams bounded provider events and returns a verifiable
   receipt.
8. The host verifies the receipt before admitting the final response or usage.

The custodian MUST reject arbitrary origins, methods, authentication headers,
provider or model substitutions, reused nonces, and request-digest changes.
The host MUST NOT have direct authenticated egress to the bound provider in
this profile. Local unauthenticated models MAY use a connection that declares
no credential custodian, subject to normal network and tenant policy.

### Adapter and stream behavior

After dispatch begins, the adapter MUST normalize monotonically ordered events.
The host MUST validate event identity, sequence, size, request correlation,
tool deltas, and cumulative usage before emission.

The host MAY expose bounded text and tool-request deltas as causally linked
signals. These deltas are observations and MUST NOT directly commit agent
state. On completion, the host MUST validate tool requests, structured output,
finish reason, usage, safety metadata, and the custodian receipt before
atomically recording the final result.

The host MUST emit:

| Event | Signal |
| --- | --- |
| Intent admitted and request committed | `model.request.created` |
| Custodian dispatch accepted | `model.request.dispatching` |
| First valid delta | `model.request.streaming` |
| Valid text delta | `model.response.text_delta` |
| Valid tool delta | `model.response.tool_request_delta` |
| Final response admitted | `model.response.completed` |
| Final failure recorded | `model.response.failed` |
| Cancellation recorded | `model.request.cancelled` |
| Verified usage recorded | `model.usage.recorded` |

Every signal MUST preserve request causation and MUST NOT expose prompt
content beyond its policy classification, credential handles, authentication
headers, arbitrary endpoints, raw provider errors, or custodian internals.

### Cancellation

On cancellation, the host MUST:

1. Mark the durable request cancellation as requested.
2. Send cancellation through the same pinned connection and custodian.
3. Stop admitting new deltas.
4. Record whether the custodian confirmed cancellation.
5. Release unused quota and retain usage already confirmed.
6. Emit `model.request.cancelled` exactly once.

Cancellation is bounded best effort after provider dispatch. A late final
response MUST NOT advance agent state after cancellation, but its bounded
usage and reconciliation receipt MUST be retained when required for billing.

### Retry, recovery, and replay

A retry MUST use the recorded request identity, binding id and revision,
connection revision, provider, model, canonical request digest, and provider
idempotency identity. Each dispatch attempt MUST use a fresh nonce linked to
the same request.

The host MUST NOT retry with a different model, provider, adapter, connection,
credential handle, or custodian. If the recorded dependency is revoked,
missing, or incompatible, the request fails and awaits explicit user
reconfiguration. Reconfiguration applies to a new intent, not to mutation of
the old durable request.

The host MAY retry transport and adapter failures only when the adapter and
custodian declare the operation idempotent or support status reconciliation.
A retry after an uncertain outcome MUST reconcile by request identity before
creating another provider operation.

### Outcome definitions

| Outcome | Diagnostic | Required behavior |
| --- | --- | --- |
| Missing binding | `model.binding.missing` | Reject before durable request creation. |
| Stale or unapproved binding | `model.binding.stale` | Reject and require user review. |
| Incompatible binding | `model.binding.incompatible` | Reject without selecting an alternative. |
| Provider unavailable | `model.request.unavailable_provider` | Record failure for the pinned request; no fallback. |
| Model unavailable | `model.request.unavailable_model` | Record failure for the pinned request; no fallback. |
| Custodian unavailable | `credential.custodian.unavailable` | Preserve outbox request for bounded retry or fail by policy. |
| Credential use denied | `credential.use.unauthorized` | Record non-retryable authorization failure. |
| Quota exhausted | `model.request.quota_exhausted` | Reject before provider dispatch. |
| Invalid structured output | `model.request.invalid_structured_output` | Reject final response and emit failure. |
| Tool-call mismatch | `model.request.tool_call_mismatch` | Reject final response and emit failure. |
| Safety refusal | `model.request.safety_refused` | Record bounded safety metadata and emit failure. |
| Timeout | `model.request.timeout` | Cancel, reconcile, and emit failure. |
| Late response | `model.request.late_response` | Do not advance cancelled or expired work; retain bounded reconciliation evidence. |
| Ambiguous billing | `model.request.ambiguous_billing` | Preserve provider and host calculations; enforce the more conservative authorized budget. |
| Invalid custodian receipt | `credential.receipt.invalid` | Reject result admission and open reconciliation. |

### Security invariants

The following invariants apply to every model request:

1. A guest cannot select or discover a credential-bearing connection through
   model-intent fields.
2. A publisher cannot bind its plugin to a provider account.
3. Raw credential bytes do not enter the host, Port worker, guest, journal,
   evidence, diagnostic, trace, crash dump, or support bundle under separated
   custody.
4. A credential handle is never returned to a guest or provider adapter and is
   never logged.
5. A custodian accepts only the provider, model, resource, digest, deadline,
   nonce, and budget authorized for the binding revision.
6. A retry does not change the user's model choice.
7. A response is not admitted without valid correlation, policy, quota, and
   receipt evidence.

## Variability register

| Item | Permission | Recommendation | Constraint |
| --- | --- | --- | --- |
| Binding input presentation | Implementation-defined | Interactive installer or authenticated declarative configuration | User authority and full requirement visibility must be preserved |
| Adapter concurrency | Implementation-defined | Bound per tenant and connection | Must preserve per-request ordering and quotas |
| Stream buffering | Implementation-defined | Use bounded backpressure | Must not reorder accepted events |
| Transport retry limit | Implementation-defined | Exponential backoff with jitter | Must preserve binding and idempotency identity |
| Request timeout | Implementation-defined | Shorter of request deadline and policy limit | Must be documented and enforced |
| Local unauthenticated models | Optional | Register as explicit no-credential connections | Must still satisfy tenant, endpoint, model, and budget policy |
| Streaming signals | Optional | Emit bounded deltas | Deltas must not mutate authoritative state directly |
| Automatic provider/model fallback | Deferred | Fail closed and request user reconfiguration | Runtime substitution is prohibited |

## Rationale and evidence (non-normative)

This flow keeps the model choice where users expect it: installation and
configuration. Pinning the selected revision to a durable effect makes retry
and audit deterministic. The custodian performs the only operation that needs
provider authentication, so an Elixir/OTP control plane and its native Port
can supervise the workflow without becoming the store for end-user provider
keys.
