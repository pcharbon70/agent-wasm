---
title: "Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests"
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
  - integration-tests
aliases:
  - "M7-P1 Integration Tests"
---

# Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests

## Status and authority

This chapter is a draft specification produced by
[Phase 1](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-01-provider-neutral-model-requests-responses-streaming-and-usage.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).
It defines observable integration evidence for user-selected model bindings,
provider-neutral intents, credential-custodian dispatch, streaming, durable
results, usage, retry, and cancellation.

Version `0.2.0` replaces the `0.1.0` test inputs that placed a provider and
model in an agent request. Existing test identifiers are retained where their
architectural purpose remains; their expected input now uses a logical slot
and a user-approved binding.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations. Every test in this chapter and the affected cross-milestone
fixtures MUST pass before the Phase 1 contract can be promoted to
`status: normative`.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md),
and
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md).

## 41.4 Phase 1 Integration Tests

### Test harness requirements

The integration harness MUST contain:

1. An agent artifact declaring at least one required logical slot and one
   optional slot.
2. Two provider adapters whose catalogs expose different compatible models.
3. A user-controlled external custodian containing a unique sentinel
   credential that is never supplied to the host process.
4. A provider-workload-identity custodian fixture with no long-lived user key.
5. A fake provider supporting streaming, idempotency reconciliation,
   cancellation, usage, and injected failures.
6. Instrumentation for guest I/O, host and Port process memory snapshots,
   state, journals, outbox, logs, traces, diagnostics, crash artifacts, network
   destinations, and support bundles.
7. A policy engine that records independent `ModelAccess` and
   `CredentialUse` decisions.

Test fixtures MUST use isolated tenants and deterministic clocks and identities.
The sentinel credential MUST exist only inside the custodian fixture.

### Successful model configuration and request flow

| Test ID | Scenario | Expected outcome |
| --- | --- | --- |
| `P1-SF-001` | User binds required slot to a compatible model, then the agent emits a valid intent. | Request is admitted with the user-selected provider and model. |
| `P1-SF-002` | Materialize the same intent twice in the same turn and binding revision. | Both calculations produce the same request identity; only one durable effect exists. |
| `P1-SF-003` | Intent includes a structured-output schema and the binding supports it. | Schema is recorded and the final value is validated. |
| `P1-SF-004` | Intent includes bounded tool definitions and the binding supports tool calling. | Only declared tools are available to the model. |
| `P1-SF-005` | Intent includes valid sampling controls. | Controls are attenuated and passed through the pinned adapter. |
| `P1-SF-006` | Intent includes a valid deadline. | The shorter host-policy deadline is recorded and enforced. |
| `P1-SF-007` | Intent includes a valid budget. | Quota is reserved before dispatch and verified usage is consumed. |
| `P1-SF-008` | Host creates trace context. | Bounded context correlates host, custodian, and provider without credential data. |
| `P1-SF-009` | Durable request commits. | Exactly one `model.request.created` signal is emitted. |
| `P1-SF-010` | Request reaches dispatch. | Request, binding revision, journal fact, quota reservation, and outbox entry exist before provider contact. |
| `P1-SF-011` | Provider streams text deltas. | Ordered bounded `model.response.text_delta` signals are emitted. |
| `P1-SF-012` | Provider streams a declared tool call. | Ordered bounded tool-request deltas are emitted and validated. |
| `P1-SF-013` | Provider emits finish. | Exactly one valid finish event is accepted. |
| `P1-SF-014` | Final response and receipt validate. | Response commits and `model.response.completed` is emitted. |
| `P1-SF-015` | Provider and receipt contain valid usage. | Usage is recorded against tenant, agent, slot, binding revision, provider, and model. |
| `P1-SF-016` | Cancel before final response. | Custodian cancellation is requested and `model.request.cancelled` is emitted once. |
| `P1-SF-017` | Cancel after committed final response. | Cancellation is idempotently ignored; terminal result is unchanged. |
| `P1-SF-018` | Cancel one of two independent requests. | Other request continues without state or stream interference. |
| `P1-SF-019` | Cancel before request deadline. | Cancellation is processed and unused quota is released. |
| `P1-SF-020` | Cancel after deadline and reconciliation. | Late cancellation does not change the terminal state. |
| `P1-SF-021` | User binds the same plugin to a different provider in another tenant. | Each tenant uses its own explicit binding; artifact digest is identical. |
| `P1-SF-022` | User changes a binding after one request is durable. | Old request stays pinned; new intent uses the newly approved revision. |
| `P1-SF-023` | External broker executes a typed request. | Host receives stream and receipt but never the sentinel credential. |
| `P1-SF-024` | Workload-identity custodian executes a typed request. | Request succeeds without a long-lived user provider key. |
| `P1-SF-025` | Custodian rotates its credential behind a stable authorized connection. | New request succeeds without plugin reinstall or credential change in the host. |
| `P1-SF-026` | Plugin is installed with an unbound optional slot and never uses it. | Plugin enables and operates without resolving that slot. |

### Malformed and incompatible input

| Test ID | Scenario | Expected diagnostic |
| --- | --- | --- |
| `P1-FH-001` | Intent omits `model_slot`. | `model.intent.missing_slot` |
| `P1-FH-002` | Intent supplies provider, model, endpoint, authentication header, or credential field. | `model.intent.forbidden_selection` |
| `P1-FH-003` | Intent has an empty or oversized messages list. | `model.intent.malformed_messages` |
| `P1-FH-004` | Intent has invalid sampling controls. | `model.intent.malformed_sampling` |
| `P1-FH-005` | Intent has an invalid or expired deadline. | `model.intent.malformed_deadline` |
| `P1-FH-006` | Intent has an invalid budget. | `model.intent.malformed_budget` |
| `P1-FH-007` | Response text violates encoding or size bounds. | `model.response.malformed_text` |
| `P1-FH-008` | Structured response is syntactically malformed. | `model.response.malformed_structured` |
| `P1-FH-009` | Usage is negative or internally inconsistent. | `model.response.malformed_usage` |
| `P1-FH-010` | Required or used optional slot has no active binding. | `model.binding.missing` |
| `P1-FH-011` | Selected model lacks a declared feature or minimum capacity. | `model.binding.incompatible` |
| `P1-FH-012` | Response requests an undeclared tool. | `model.request.tool_call_mismatch` |
| `P1-FH-013` | Structured value fails its declared schema. | `model.request.invalid_structured_output` |

Every test above MUST verify that no provider operation and no credential-use
request occurs before a durable request is valid and authorized.

### Conflict, authorization, and resource limits

| Test ID | Scenario | Expected diagnostic |
| --- | --- | --- |
| `P1-FH-014` | Non-equivalent concurrent requests reuse one request id. | `model.request.duplicate_id` |
| `P1-FH-015` | Concurrent cancellation races target one request. | Exactly one terminal cancellation; duplicate is idempotent. |
| `P1-FH-016` | Agent lacks `ModelAccess` for the slot. | `model.request.unauthorized` |
| `P1-FH-017` | Tool definition crosses tenant authority. | `model.request.cross_tenant_tool` |
| `P1-FH-018` | Result destination crosses tenant authority. | `model.request.cross_tenant_result` |
| `P1-FH-019` | Request exceeds concurrency limit before dispatch. | `model.request.exhausted_concurrency` |
| `P1-FH-020` | Stream exceeds event or byte buffer bounds. | `model.request.exhausted_stream` |
| `P1-FH-021` | Pinned connection is inactive. | `model.connection.unavailable` |
| `P1-FH-022` | Pinned provider reports that the selected model is unavailable. | `model.request.unavailable_model` |
| `P1-FH-023` | Binding approval refers to an older revision. | `model.binding.stale` |
| `P1-FH-024` | Effect worker lacks `CredentialUse` while agent has `ModelAccess`. | `credential.use.unauthorized` |
| `P1-FH-025` | Credential-use request changes provider, model, binding revision, resource, or budget. | `credential.use.scope_mismatch` |
| `P1-FH-026` | Caller requests credential read, unwrap, export, or a bearer token. | `credential.use.export_forbidden` |
| `P1-FH-027` | Custodian receipt has an invalid digest, signature, or request correlation. | `credential.receipt.invalid` |
| `P1-FH-028` | Previously accepted credential-use nonce is replayed. | `credential.use.replay` |
| `P1-FH-029` | Plugin upgrade changes a model requirement without reconfiguration. | `model.binding.stale` |

### Credential non-exposure and egress tests

| Test ID | Scenario | Expected invariant |
| --- | --- | --- |
| `P1-SEC-001` | Complete brokered request with sentinel credential. | Sentinel is absent from host and Port memory snapshots, guest I/O, state, journal, outbox, logs, traces, diagnostics, crash artifacts, and support bundles. |
| `P1-SEC-002` | Crash host and native Port during dispatch. | Crash artifacts contain request correlation only; sentinel and opaque handle are absent. |
| `P1-SEC-003` | Malicious guest scans all inputs and emits suspected credential fields. | No handle or credential is observable; output attempt is rejected and audited. |
| `P1-SEC-004` | Compromised adapter requests arbitrary URL, method, or authentication header. | Custodian rejects `credential.use.scope_mismatch` and no outbound request occurs. |
| `P1-SEC-005` | Host attempts direct authenticated provider egress. | Network policy denies egress; only the registered custodian can reach the authenticated provider path. |
| `P1-SEC-006` | Reuse opaque handle reference from another tenant or binding. | Sender and scope binding reject the request. |
| `P1-SEC-007` | Query policy cache, audit API, and diagnostics as every supported role. | No role receives credential bytes, opaque handles, or authentication headers. |
| `P1-SEC-008` | Publisher manifest includes disguised provider or credential material in model requirement fields. | Admission rejects `plugin.forbidden_model_selection`. |

The non-exposure suite MUST scan exact sentinel bytes and common encoded forms.
A passing scan does not replace the architectural proof that the fixture never
sends the credential across the custodian boundary; both conditions are
required.

### Timeout, cancellation, retry, and recovery

| Test ID | Scenario | Expected outcome |
| --- | --- | --- |
| `P1-TO-001` | Provider completes within timeout. | Response commits normally. |
| `P1-TO-002` | Request exceeds host timeout. | Cancellation and reconciliation occur; `model.request.timeout` is recorded. |
| `P1-TO-003` | Provider completes before intent deadline. | Response commits normally. |
| `P1-TO-004` | Response arrives after deadline. | It does not advance expired work; bounded usage and late-response evidence remain. |
| `P1-TO-005` | Timeout occurs with uncertain provider outcome. | Status is reconciled before any retry. |
| `P1-CA-001` | Cancel active request. | Pinned custodian receives cancellation. |
| `P1-CA-002` | Cancel finalized request. | Terminal result remains unchanged. |
| `P1-CA-003` | Send duplicate cancellation concurrently. | Exactly one terminal transition and signal occur. |
| `P1-CA-004` | Observe cancellation signals. | Signal is causally linked and contains no credential material. |
| `P1-RT-001` | Transient custodian transport fails before provider acceptance. | Retry uses same binding and request digest with a fresh nonce. |
| `P1-RT-002` | Adapter crashes after provider acceptance. | Reconciliation finds the existing provider operation; no duplicate billing. |
| `P1-RT-003` | Pinned model becomes unavailable between attempts. | Request fails; runtime does not select the second compatible fixture model. |
| `P1-RT-004` | Credential lease is revoked between attempts. | Retry is denied; new user configuration is required for a new intent. |

### Cross-milestone fixture scopes

| Contract | Interaction to verify |
| --- | --- |
| [Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md) | Logical requirements are portable and concrete selection fields are rejected. |
| [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md) | Request and outbox commit precedes external dispatch. |
| [Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md) | Attempts preserve binding and idempotency identities. |
| [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md) | `ModelAccess` and `CredentialUse` are independent. |
| [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md) | Binding, resource, nonce, deadline, and budget are attenuated. |
| [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md) | Configure and reapproval gates prevent publisher model selection. |
| [Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md) | Guest cannot bypass the typed effect boundary. |
| [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md) | Evidence is bounded, tenant-isolated, and tamper-evident. |
| [Threads Checkpoints Memory Approvals Quotas And Secret Leases Phase 4 Integration Tests](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-phase-4-integration-tests.md) | Custodian, lease, handle, receipt, revocation, and non-exposure fixtures agree. |

### Evidence requirements

Every test MUST record test id, objective, setup digest, relevant artifact and
binding revisions, policy revision, expected outcome, actual outcome, terminal
state, external-call count, credential-use count, diagnostics, evidence
digest, timestamp, and pass or fail.

Evidence MUST NOT contain the sentinel credential, its encoded forms,
authentication headers, opaque handles, prompts, raw responses, arbitrary
endpoints, or unbounded provider and custodian errors.

A Phase 1 run passes only if every listed test and affected fixture passes,
external-call counts match exactly, non-exposure scans find zero sentinel
occurrences, and signed evidence is complete.

## Variability register

| Item | Permission | Recommendation | Constraint |
| --- | --- | --- | --- |
| Fake providers and custodians | Implementation-defined | Deterministic local fixtures | Must exercise real process and transport boundaries |
| Memory and artifact inspection mechanism | Implementation-defined | Inspect host and native-worker artifacts after success and injected crashes | Must cover all declared product outputs |
| Test parallelism | Optional | Parallelize isolated tenants only | Shared binding, quota, or custodian tests must serialize |
| Timing bounds | Implementation-defined | Publish deterministic test-clock limits | Timeout tests must remain bounded |
| Sentinel encoding scan | Required | Raw, base64, hex, URL-encoded, and structured variants | Architectural non-transfer assertion is also required |

## Rationale and evidence (non-normative)

These tests prove more than redaction. The fixture never transmits its provider
credential to the Elixir/OTP host in the first place, while inspection and
fault injection check that no accidental alternate path was introduced.
Separate tenant bindings also demonstrate the end-user property: the same
plugin artifact can run against different user-chosen models without a rebuild.
