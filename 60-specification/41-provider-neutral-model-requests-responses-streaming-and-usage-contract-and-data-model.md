---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model"
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
aliases:
  - "M7-P1 Contract And Data Model"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model

## Status and authority

This chapter is a normative specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).
It defines logical model requirements, user-controlled model bindings,
provider-neutral intents, materialized requests, normalized responses,
streaming, and usage.

Version `0.2.0` replaces the `0.1.0` rules that sourced `provider` and
`model` from the agent. An agent now names only a logical model slot. A
user-approved, versioned binding is the sole source of the provider, model,
connection, adapter, and credential-use reference. This version also replaces
the implied adapter possession of provider credentials with the use-only
credential contract in
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md).

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations. Promotion to `status: normative` requires passing evidence from
[Phase 1 Integration Tests](41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md).

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md),
[Retry Timer Recovery Replay Hibernate And Migration](28-retry-timer-recovery-replay-hibernate-and-migration.md),
and
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

## 41.1 Contract And Data Model

### Logical model requirements

A model requirement describes portable behavior needed by an agent or
strategy. It does not select a vendor.

| Field | Type | Meaning |
| --- | --- | --- |
| `slot_id` | string | Stable logical name unique within the agent definition. |
| `description` | string | Human explanation of the slot's role. |
| `required_features` | ModelFeature[] | Features the selected model and adapter MUST support. |
| `min_context_tokens` | u64 | Minimum advertised context capacity. |
| `min_output_tokens` | u64 | Minimum advertised output capacity. |
| `optional` | bool | Whether installation may leave the slot unbound. |

`ModelFeature` is one of `text-generation`, `streaming`,
`tool-calling`, or `structured-output`. A later specification version MAY
add namespaced features.

A requirement MUST NOT contain a provider, model identifier, adapter,
connection, endpoint, authentication header, secret, or credential handle.
A required slot MUST have exactly one active compatible binding before the
agent definition is enabled. An optional slot MAY remain unbound, but an
intent that uses it then fails with `model.binding.missing`.

### Agent-originated model intent

An agent requests model behavior by emitting a provider-neutral `ModelIntent`.

| Field | Source | Meaning |
| --- | --- | --- |
| `intent_id` | Host runtime | Deterministic identity derived from agent address, turn, directive index, and canonical intent payload. |
| `agent_address` | Host runtime | Authenticated originating agent. |
| `model_slot` | Agent | Logical slot declared by the effective agent definition. |
| `messages` | Agent | Ordered provider-neutral conversation messages. |
| `structured_output_schema` | Agent | Optional JSON Schema for a structured result. |
| `tool_definitions` | Agent | Bounded tools available to this request. |
| `sampling` | Agent | Provider-neutral sampling limits accepted by policy. |
| `deadline` | Agent and host policy | Absolute completion deadline, attenuated by the host. |
| `budget` | Agent and host policy | Maximum authorized cost and token use. |
| `trace_context` | Host runtime | Bounded tracing context. |

The host MUST reject an intent that supplies `provider`, `model`,
`adapter_id`, `connection_id`, `endpoint`, authentication headers,
credential handles, or equivalent selection material with
`model.intent.forbidden_selection`. Removing or ignoring such fields is not
permitted because that would hide a publisher or guest selection attempt.

### User-controlled model connections and bindings

A `ModelConnection` is registered by the end user or an authorized tenant
operator independently of plugin installation.

| Field | Meaning |
| --- | --- |
| `connection_id` | Stable tenant-scoped connection identity. |
| `revision` | Monotonically increasing connection revision. |
| `tenant_id` | Owning tenant. |
| `adapter_id` | Reviewed host adapter or external effect-worker adapter. |
| `custody_mode` | `external-broker`, `provider-workload-identity`, explicitly opted-in `host-local`, or `none` for an unauthenticated local model. |
| `custodian_id` | Registered credential custodian, if authentication is required. |
| `credential_lease_id` | Active use-only credential lease, if authentication is required. |
| `credential_handle_ref` | Opaque sender-constrained reference, if authentication is required. |
| `endpoint_ref` | Reference to an operator-approved endpoint registry entry. |
| `catalog_revision` | Revision of advertised provider models and capabilities. |
| `status` | `active`, `suspended`, `revoked`, or `unavailable`. |

`endpoint_ref` MUST NOT be an arbitrary URL supplied by an agent or plugin.
`credential_handle_ref` MUST NOT contain credential bytes and MUST NOT be
sufficient as an unauthenticated bearer token.

Changing the adapter, custody mode, custodian, credential lease, protected
handle reference, endpoint, catalog revision, or status MUST create a new
connection revision. A `custody_mode: none` connection MUST identify a local
unauthenticated endpoint and MUST have null `custodian_id`,
`credential_lease_id`, and `credential_handle_ref` fields. Every other custody
mode used for an authenticated request MUST identify all three fields.

A `ModelBinding` records the user's concrete choice for one logical slot.

| Field | Source | Meaning |
| --- | --- | --- |
| `binding_id` | Host runtime | Stable binding identity. |
| `revision` | Host runtime | Monotonically increasing binding revision. |
| `tenant_id` | Installation context | Owning tenant. |
| `agent_definition_digest` | Host runtime | Immutable composed definition being configured. |
| `model_slot` | Manifest | Logical requirement being satisfied. |
| `connection_id` | User configuration | Selected registered connection. |
| `connection_revision` | Host runtime | Pinned revision of the selected connection. |
| `provider` | User configuration through catalog | Concrete provider identifier. |
| `model` | User configuration through catalog | Concrete provider model identifier. |
| `catalog_revision` | Host runtime | Catalog metadata used for compatibility validation. |
| `configured_by` | Authentication context | User or authorized tenant operator. |
| `approved_at` | Host clock | Time at which this revision was approved. |
| `policy_version` | Host policy | Policy revision that authorized the binding. |
| `status` | Host runtime | `active`, `pending-approval`, `stale`, `revoked`, or `unavailable`. |

The user is the selection authority. A publisher, guest artifact, strategy,
agent instance, provider adapter, or credential custodian MUST NOT create or
change a binding on the user's behalf.

Bindings are mutable configuration stored outside the immutable artifact.
Changing a binding MUST create a new revision and MUST NOT change the plugin
or agent artifact digest. Approval of one revision MUST NOT authorize a later
revision. Compatibility is evaluated from signed or operator-approved model
catalog metadata against every requirement field.

If the selected connection revision changes, the host MUST create and approve
a new binding revision before materializing another intent. A binding MUST NOT
float to the latest revision of its `connection_id`.

### Materialized model request

After authorization and binding resolution, the host materializes a durable
`ModelRequest`.

| Field | Source |
| --- | --- |
| `request_id` | Host, derived from agent address, turn, directive index, canonical intent, binding id, and binding revision. |
| `intent_id` | Admitted intent. |
| `agent_address` | Authenticated intent context. |
| `model_slot` | Admitted intent. |
| `binding_id` and `binding_revision` | Active approved binding. |
| `connection_id`, `connection_revision`, and `adapter_id` | Bound connection revision. |
| `credential_lease_id` | Bound use-only lease for authenticated dispatch, or null for `custody_mode: none`. |
| `provider` and `model` | User-approved binding. |
| `messages`, `structured_output_schema`, `tool_definitions`, `sampling` | Validated intent. |
| `deadline` and `budget` | Attenuated policy result. |
| `trace_context` and `created_at` | Host runtime and host clock. |
| `status` | `pending`, `dispatching`, `streaming`, `completed`, `failed`, or `cancelled`. |

The materialized request MUST NOT contain a raw credential, authentication
header, arbitrary endpoint, or transferable bearer value. The durable record
stores the binding and connection revisions, not credential bytes or the
opaque handle. The versioned connection registry retains the protected
handle reference needed for dispatch.

The host MUST atomically record the materialized request and its outbox effect
before an external provider is contacted. Retry and replay MUST use the
recorded binding, connection, provider, model, and request digest. They MUST
NOT resolve a new default or silently select an alternative.

### Provider adapter contract

A provider adapter is a reviewed host integration or authenticated external
effect worker. It is not an untrusted guest artifact.

Every adapter MUST implement:

| Operation | Responsibility |
| --- | --- |
| `validate_model` | Verify catalog identity and capabilities. |
| `prepare_dispatch` | Convert a materialized request into a bounded typed provider operation without authentication material. |
| `normalize_event` | Convert provider stream events into normalized events. |
| `cancel_request` | Request cancellation of an in-flight operation. |
| `check_status` | Reconcile an uncertain operation by idempotency identity. |

In the `separated-credential-custody` profile, the adapter MUST NOT receive,
read, unwrap, or log the provider credential. The prepared operation is
executed through `CredentialUse` by the custodian defined in Section 44.

### Normalized response and streaming events

Every normalized response MUST include:

| Field | Meaning |
| --- | --- |
| `response_id` | Deterministic identity derived from request identity and final sequence. |
| `request_id` | Associated materialized request. |
| `text` | Optional normalized text. |
| `structured_value` | Optional validated structured value. |
| `tool_requests` | Validated requested tools. |
| `finish_reason` | `stop`, `length`, `content_filter`, `tool_calls`, or `error`. |
| `usage` | Prompt, completion, total token, and cost observations. |
| `provider_response_ref` | Bounded provider correlation reference. |
| `safety_metadata` | Bounded provider safety result. |
| `credential_receipt` | Verified credential-use receipt or a host-created no-credential receipt. |
| `diagnostics` | Bounded latency and retry information. |
| `created_at` | Host timestamp. |

> **Normative definition.**

```
ModelCredentialReceipt = CredentialUseReceiptRef | NoCredentialReceipt

CredentialUseReceiptRef {
  kind: "credential-use",
  receipt_ref: string
}

NoCredentialReceipt {
  kind: "not-required",
  reason: "local-unauthenticated",
  connection_id: string,
  connection_revision: u64
}
```

An authenticated request MUST use `CredentialUseReceiptRef` and the referenced
receipt MUST pass Section 44 verification. A request through a pinned
`custody_mode: none` connection MUST use `NoCredentialReceipt`; the host MUST
create it only after verifying that the connection has no custodian, lease,
handle, or authenticated provider operation. Neither receipt variant grants
authority.

A streaming event includes `event_id`, `request_id`, monotonically
increasing `sequence`, `event_type`, the applicable bounded delta,
cumulative usage when available, and `created_at`. Event types are
`text_delta`, `tool_request_delta`, and `finish`.

Streaming events are observations and MUST NOT mutate authoritative agent
state directly. The final normalized response and usage record are durable.
The host MAY retain bounded streaming events for diagnostics if its
conformance profile documents retention and redaction.

### Usage and durable evidence

Every usage record MUST include `usage_id`, `request_id`,
`agent_address`, `model_slot`, `binding_id`, `binding_revision`,
`provider`, `model`, token counts, cost, currency or cost unit,
`credential_receipt`, and `created_at`.

Prompt and response bodies MUST be represented in durable request and result
records by access-controlled content references when policy classifies them as
sensitive. A durable record MUST NOT contain raw credentials, authentication
headers, opaque credential handles, arbitrary endpoint URLs, or unbounded
provider errors.

If a returned tool request is not present in `tool_definitions`, the host MUST
reject the response with `model.request.tool_call_mismatch`. If a structured
value does not satisfy `structured_output_schema`, the host MUST reject it
with `model.request.invalid_structured_output`.

### Cross-chapter type and precedence rules

For authenticated model requests, the `SecretLease`, `CredentialUseRequest`,
and `CredentialUseReceipt` types in
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md#credential-custodians-leases-handles-and-receipts)
govern credential-use scope and receipt verification. This chapter requires a
model connection's `credential_lease_id` to equal the governing `lease_id` and
adds only the
`NoCredentialReceipt` alternative for a connection that performs no
authenticated operation. `NoCredentialReceipt` MUST NOT be used to bypass or
replace a Section 44 receipt.

## Variability register

The following table summarizes fixed requirements and internal mechanisms.

> **Non-normative note.**

| Item | Permission | Recommendation | Constraint |
| --- | --- | --- | --- |
| Concrete provider and model selection | Required | User-approved binding for every required slot | Agent, publisher, adapter, and custodian selection is prohibited |
| Model connection revision | Required | Pin the complete connection authority used by a binding | Every authority-bearing connection change creates a new revision |
| Binding storage backend | Internal mechanism | Versioned tenant-scoped registry | Backend changes must preserve revision history and must not alter artifact identity or observable binding semantics |
| Model catalog source | Required trust rule | Signed provider catalog or operator-approved registry | Compatibility decision and catalog revision must be auditable |
| Adapter implementation | Internal mechanism | Reviewed host integration or authenticated external worker | Both forms must implement the same common contract and never expose credentials |
| Sensitive content storage | Internal mechanism | Access-controlled content references | Backend choice must not change authorization, boundedness, or durable reference semantics |
| Streaming-event retention | Optional | Do not retain deltas by default | Retention and redaction must be documented |
| Cost units and currency | Required preservation | Preserve provider observation and host calculation | Budget enforcement must retain both values and apply the conservative authorized amount |
| Credential custody | Required for authenticated end-user operations | Use separated credential custody | `host-local` must be explicit and cannot claim separated-custody conformance; `none` is restricted to local unauthenticated models |
| Model credential receipt | Closed required union | Verified Section 44 receipt or `NoCredentialReceipt` | The no-credential variant is valid only for a pinned `custody_mode: none` connection |
| Automatic model routing or fallback | Deferred | Require an explicit user binding | Runtime must not silently change provider or model |

## Rationale and evidence (non-normative)

Logical slots keep agent artifacts portable while making installation the
point where an end user chooses cost, privacy, locality, and provider trust.
Versioned bindings make that choice observable and replayable. Use-only
credential custody narrows the Elixir/OTP host to orchestration: it can request
the bound operation, but the separated-custody product does not need provider
credential bytes in the BEAM, its native Port, or a Wasm guest.
