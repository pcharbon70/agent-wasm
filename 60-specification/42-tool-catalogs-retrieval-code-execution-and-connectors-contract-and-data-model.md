---
title: "Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model"
kind: specification
created: "2026-08-09"
status: normative
spec_version: "0.2.0"
tags:
  - milestone-07
  - phase-02
  - tool-catalogs
  - retrieval
  - code-execution
  - connectors
  - capabilities
  - credential-custody
aliases:
  - "M7-P2 Contract And Data Model"
---

# Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model

## Status and authority

This chapter is a normative specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the contract and data model for tool catalogs, retrieval,
code execution, and connectors, including tool descriptors, retrieval
requests, code-execution requests, and the capability policy that binds
them.

Version `0.2.0` replaces connector-owned authentication and token-refresh
semantics with user-controlled authentication bindings and use-only
credential custody. A connector plugin may describe and prepare a typed
operation, but it does not receive provider credentials, authentication
headers, refresh tokens, or opaque credential handles.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 2
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
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
[Crash Injection Durable Effects And Milestone Acceptance](29-crash-injection-durable-effects-and-milestone-acceptance.md),
[Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md),
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md),
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md),
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md),
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md),
[Agent Identity Addressing Ownership And Dependency Relations](35-agent-identity-addressing-ownership-and-dependency-relations.md),
[Child Lifecycle Cancellation Monitoring And Restart Policy Contract And Data Model](36-child-lifecycle-cancellation-monitoring-and-restart-policy.md),
[Fan-Out Fan-In Delegation And Result Aggregation Contract And Data Model](37-fan-out-fan-in-delegation-and-result-aggregation-contract-and-data-model.md),
[Fan-Out Fan-In Delegation And Result Aggregation Behavior And Integration](37-fan-out-fan-in-delegation-and-result-aggregation-behavior-and-integration.md),
[Fan-Out Fan-In Delegation And Result Aggregation Failure Evidence And Operational Notes](37-fan-out-fan-in-delegation-and-result-aggregation-failure-evidence-and-operational-notes.md),
[Pod Topology Placement Activation Leases And Reconciliation Contract And Data Model](38-pod-topology-placement-activation-leases-and-reconciliation-contract-and-data-model.md),
[Pod Topology Placement Activation Leases And Reconciliation Behavior And Integration](38-pod-topology-placement-activation-leases-and-reconciliation-behavior-and-integration.md),
[Pod Topology Placement Activation Leases And Reconciliation Failure Evidence And Operational Notes](38-pod-topology-placement-activation-leases-and-reconciliation-failure-evidence-and-operational-notes.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Contract And Data Model](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-contract-and-data-model.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Behavior And Integration](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-behavior-and-integration.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Failure Evidence And Operational Notes](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-failure-evidence-and-operational-notes.md),
[Multi-Agent Recovery Clustering Seams And Milestone Acceptance Phase 5 Integration Tests](39-multi-agent-recovery-clustering-seams-and-milestone-acceptance-phase-5-integration-tests.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Contract And Data Model](41-provider-neutral-model-requests-responses-streaming-and-usage-contract-and-data-model.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Behavior And Integration](41-provider-neutral-model-requests-responses-streaming-and-usage-behavior-and-integration.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Failure Evidence And Operational Notes](41-provider-neutral-model-requests-responses-streaming-and-usage-failure-evidence-and-operational-notes.md),
[Provider-Neutral Model Requests Responses Streaming And Usage Phase 1 Integration Tests](41-provider-neutral-model-requests-responses-streaming-and-usage-phase-1-integration-tests.md),
[Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md),
[Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md),
[Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md),
[Tool Catalogs Retrieval Code Execution And Connectors Phase 2 Integration Tests](42-tool-catalogs-retrieval-code-execution-and-connectors-phase-2-integration-tests.md).

## 42.1 Contract And Data Model

### Tool descriptor identity and properties

> **Normative definition.**
A tool descriptor is a durable record that describes an external ability
available to agents through the host runtime.
The descriptor captures the tool's identity, version, schemas, capability,
side-effect class, idempotency, timeout, result limits, and provenance
requirements.

> **Normative definition.**
Every tool descriptor MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `tool_id` | A deterministic tool identity derived from the tool name, version, and framework plugin identifier. | Host runtime. |
| `name` | The tool name (e.g., `search`, `code_interpreter`, `email_send`). | Framework plugin. |
| `version` | The semantic version of the tool (e.g., `1.2.3`). | Framework plugin. |
| `description` | A human-readable description of the tool's purpose and behavior. | Framework plugin. |
| `input_schema` | The JSON Schema for the tool's input parameters. | Framework plugin. |
| `output_schema` | The JSON Schema for the tool's output result. | Framework plugin. |
| `capability` | The capability identifier granted to agents for using this tool (e.g., `tool.search.read`, `tool.code.execute`). | Capability policy. |
| `side_effect_class` | The side-effect class: `read_only`, `write`, `network`, `stateful`. | Framework plugin. |
| `network_destinations` | Sorted, duplicate-free exact destinations the tool may contact; non-empty only for `network`. | Framework plugin and host policy. |
| `idempotent` | Whether the tool is idempotent (safe to retry without side effects). | Framework plugin. |
| `timeout_ms` | The maximum execution time in milliseconds. | Framework plugin. |
| `result_limits` | Limits on the result size (e.g., `max_bytes`, `max_tokens`, `max_items`). | Framework plugin. |
| `provenance_required` | Whether provenance evidence is required for this tool's results. | Framework plugin. |
| `framework_plugin` | The framework plugin identifier that provides this tool. | Framework plugin. |
| `created_at` | The ISO 8601 timestamp of descriptor creation. | Host clock. |
| `status` | The current status: `active`, `deprecated`, `suspended`. | Host runtime. |

`timeout_ms` MUST be a positive integer no greater than the host's published
timeout implementation limit. A descriptor exceeding that limit is rejected
with `tool.execution.exhausted-timeout`.

> **Normative definition.**

```
NetworkDestination {
  scheme: "https" | "http" | "tcp",
  host: string,
  port: u16
}
```

`host` MUST be one of: a lowercase ASCII DNS A-label sequence without a
trailing dot; an IPv4 dotted-decimal address with four decimal octets and no
leading zeroes; or a lowercase RFC 5952 IPv6 address without brackets or a zone
identifier. `port` MUST be between 1 and 65535 inclusive. Wildcards, user
information, paths, queries, fragments, port zero, and port ranges are invalid.
The tuple `(scheme, host, port)` is the complete destination identity.
A network-class descriptor MUST contain at least one destination. Every other
side-effect class MUST contain an empty list.

> **Non-normative note.**
The `tool_id` is deterministic to enable idempotent tool resolution and
to ensure that the same tool version from the same framework plugin
produces the same identifier.
This is consistent with the deterministic reducer semantics defined in
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

### Tool capability and side-effect classes

> **Normative definition.**
Tools are classified by their side-effect class to enable capability
policy enforcement and resource bounding.
The side-effect class determines the minimum capability required to use
the tool and the resource budget applied.

| Side-effect class | Description | Minimum capability | Resource budget |
|-------------------|-------------|-------------------|-----------------|
| `read_only` | No state or network changes. | `tool.<name>.read` | Default read budget. |
| `write` | State changes within the agent's scope. | `tool.<name>.write` | Default write budget. |
| `network` | Network requests to external services. | `tool.<name>.network` | Network budget. |
| `stateful` | Persistent state changes or long-running operations. | `tool.<name>.stateful` | Extended budget. |

> **Non-normative note.**
The side-effect class hierarchy ensures that tools with broader side
effects require higher-privilege capabilities.
This is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Retrieval request and result schema

> **Normative definition.**
Retrieval requests and results capture the semantics of search, knowledge
base lookup, and content retrieval operations.
The retrieval contract includes tenant scope, query, filters, ranking
metadata, citations, and bounded content references.

> **Normative definition.**
Every retrieval request MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | A deterministic retrieval request identity derived from the agent address, query hash, and timestamp. | Host runtime. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Agent. |
| `query` | The search query or knowledge base lookup string. | Agent. |
| `tenant_scope` | The tenant scope for the retrieval (e.g., `self`, `team`, `organization`). | Agent. |
| `filters` | The filters applied to the retrieval (e.g., `source_type`, `date_range`, `tags`). | Agent. |
| `ranking` | The ranking metadata (e.g., `relevance`, `recency`, `authority`). | Agent. |
| `max_results` | The maximum number of results to return. | Agent. |
| `created_at` | The ISO 8601 timestamp of request creation. | Host clock. |
| `status` | The current status: `pending`, `completed`, `failed`, `cancelled`. | Host runtime. |

Retrieval requests use a fixed 60-second timeout. The host MUST cancel a
request that has not completed after 60 seconds and emit
`tool.execution.timeout`.

> **Normative definition.**
Every retrieval result MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `result_id` | A deterministic retrieval result identity derived from the `request_id` and result sequence number. | Host runtime. |
| `request_id` | The `request_id` of the associated retrieval request. | Normalized from retrieval source. |
| `items` | The list of retrieved items (each with content, metadata, and citation). | Normalized from retrieval source. |
| `total_results` | The total number of results available (before `max_results` limit). | Normalized from retrieval source. |
| `ranking_metadata` | The ranking metadata used for this retrieval. | Normalized from retrieval source. |
| `created_at` | The ISO 8601 timestamp of result creation. | Host clock. |

> **Normative definition.**
Each retrieval item MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `content` | The retrieved content (text, JSON, or binary reference). | Normalized from retrieval source. |
| `metadata` | The item metadata (source, author, date, tags, relevance score). | Normalized from retrieval source. |
| `citation` | The citation string for attribution and provenance. | Normalized from retrieval source. |
| `content_ref` | A bounded content reference (hash or URL) for deduplication. | Normalized from retrieval source. |

> **Non-normative note.**
The `content_ref` field enables deduplication of retrieval results and
prevents redundant storage of identical content.
This is consistent with the storage contract defined in
[Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md).

### Code-execution request and result schema

> **Normative definition.**
Code-execution requests and results capture the semantics of sandboxed
code execution operations.
The code-execution contract includes immutable environment, inputs,
capability policy, resource budget, output artifacts, and isolation class.

> **Normative definition.**
Every code-execution request MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | A deterministic code-execution request identity derived from the agent address, code hash, and timestamp. | Host runtime. |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Agent. |
| `language` | The programming language of the code (e.g., `python`, `javascript`, `rust`). | Agent. |
| `code` | The code to execute (redacted reference for storage). | Agent. |
| `inputs` | The input data for the code execution. | Agent. |
| `environment` | The immutable execution environment (e.g., `python:3.11-slim`, `node:20-alpine`). | Agent. |
| `capability` | The capability identifier granted to agents for code execution (e.g., `code.execute`). | Capability policy. |
| `resource_budget` | The resource budget for execution (e.g., `max_memory_mb`, `max_cpu_seconds`, `max_network_requests`). | Agent. |
| `network_tool` | The `tool_id` of the active network-class tool authorizing sandbox network access, or `null` when network access is not requested. | Agent. |
| `authorized_network_destinations` | Sorted, duplicate-free exact `NetworkDestination` values admitted for this request. | Host runtime. |
| `isolation_class` | The isolation class: `shared`, `tenant`, `isolated`. | Agent. |
| `timeout_ms` | The maximum execution time in milliseconds. | Agent. |
| `created_at` | The ISO 8601 timestamp of request creation. | Host clock. |
| `status` | The current status: `pending`, `executing`, `completed`, `failed`, `cancelled`. | Host runtime. |

The code-execution `timeout_ms` MUST be positive and no greater than the
published timeout implementation limit. `max_memory_mb` MUST be positive and
no greater than the published sandbox-memory implementation limit. Values
over those limits are rejected with `tool.execution.exhausted-timeout` and
`tool.execution.exhausted-memory` respectively.

Sandbox network access is denied unless the request names a tool with
`side_effect_class: network` and the agent has the corresponding
`tool.<name>.network` capability. Configuration MUST NOT grant network access
that either admission check denies. Failure of either admission check MUST be
reported as `tool.execution.denied_capability`. After both checks pass, a
runtime violation of an authorized sandbox destination or network budget MUST
be reported as `tool.execution.sandbox_failure`.

A request asks for network access when `network_tool` is non-null or
`resource_budget.max_network_requests` is greater than zero. Network admission
requires both a non-null `network_tool` and a positive
`max_network_requests`; a mismatched pair is rejected with
`tool.execution.denied_capability`.

For an admitted network request, the host MUST set
`authorized_network_destinations` to the exact intersection of the selected
descriptor's `network_destinations` and the resources allowed by the current
capability-policy decision. An empty intersection is denied with
`tool.execution.denied_capability`. Before every DNS resolution or connection,
the sandbox MUST compare the canonical destination to this durable list and
MUST reject a non-member with `tool.execution.sandbox_failure` before network
I/O. A request that does not ask for network access MUST contain an empty list
and run with sandbox network access disabled.

> **Normative definition.**
Every code-execution result MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `result_id` | A deterministic code-execution result identity derived from the `request_id` and result sequence number. | Host runtime. |
| `request_id` | The `request_id` of the associated code-execution request. | Normalized from code executor. |
| `exit_code` | The exit code of the code execution (0 for success, non-zero for failure). | Normalized from code executor. |
| `stdout` | The standard output of the code execution (redacted reference for storage). | Normalized from code executor. |
| `stderr` | The standard error of the code execution (redacted reference for storage). | Normalized from code executor. |
| `artifacts` | The output artifacts (e.g., files, images, data). | Normalized from code executor. |
| `resource_usage` | The resource usage (e.g., `memory_mb`, `cpu_seconds`, `network_requests`). | Normalized from code executor. |
| `execution_time_ms` | The actual execution time in milliseconds. | Normalized from code executor. |
| `created_at` | The ISO 8601 timestamp of result creation. | Host clock. |

> **Non-normative note.**
The `code`, `stdout`, and `stderr` fields are stored with redacted references
to protect sensitive data.
The actual content is stored in a separate, access-controlled storage
layer as defined in
[Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md).

### Connector registration and discovery

> **Normative definition.**
Connectors are registered with the host and expose typed interfaces for
external services (e.g., email, calendar, messaging, APIs).
The host discovers available connectors from approved framework plugins
and presents them to agents through the tool catalog.

> **Normative definition.**
Every connector MUST include the following plugin-facing capabilities:

| Capability | Description |
|------------|-------------|
| `list_tools` | List the tools provided by this connector. |
| `prepare_tool_operation` | Validate tool input and prepare a bounded typed operation without authentication material. |
| `normalize_tool_result` | Validate and normalize bounded external results. |

An unauthenticated connector MAY also execute its approved operation directly.
An authenticated connector MUST use a user-controlled
`ConnectorAuthenticationBinding`:

> **Normative definition.**

```
ConnectorAuthenticationBinding {
  binding_id: string,
  revision: u64,
  tenant_id: TenantId,
  connector_id: string,
  custodian_id: string,
  credential_lease_id: string,
  allowed_operations: string[],
  allowed_resources: string[],
  configured_by: PrincipalId,
  policy_version: Version,
  status: "active" | "pending-approval" | "stale" | "revoked" | "unavailable"
}
```

The user or an authorized tenant operator MUST create, approve, change, and
revoke this binding outside the plugin artifact. The plugin, guest, agent, and
connector adapter MUST NOT create or alter it. The binding MUST NOT contain a
raw credential, authentication header, refresh token, arbitrary endpoint, or
opaque credential handle. It references the use-only lease defined in Section
44; protected handle resolution remains inside the credential-use boundary.

In the `separated-credential-custody` profile, authentication, token refresh,
and the authenticated external operation MUST execute inside the registered
custodian. `authenticate` and `refresh_token` MUST NOT be callable plugin or
guest operations. The plugin, native Port adapter, and guest receive only
bounded results and verified receipt correlation. The host may retain only the
protected sender-constrained handle reference needed by Section 44, never its
underlying authentication material.

> **Non-normative note.**
Connectors are implemented as framework plugins as defined in
[Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).
Each connector is isolated in its own tenant and subject to the capability
policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Cross-references and precedence

> **Non-normative note.**
This section's contract and data model integrate with the following
earlier chapters:

1. For tool capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of tool-specific capability enforcement.
2. For retrieval storage: this section takes precedence over
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   for questions of retrieval-specific storage.
3. For code execution isolation: this section takes precedence over
   [Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
   for questions of code-execution-specific isolation.
4. For provenance: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of tool-specific provenance requirements.
5. For authenticated connector custody: the credential contract in
   [Threads Checkpoints Memory Approvals Quotas And Secret Leases Contract And Data Model](44-threads-checkpoints-memory-approvals-quotas-and-secret-leases-contract-and-data-model.md)
   takes precedence for handle, lease, typed-use, and receipt semantics.
6. Where both sections are applicable and agree, they are mutually
     reinforcing.

The precedence statements above are normative. In particular, Chapter 31
supplies the agent's resource authorization, while this chapter governs the
tool-specific mapping from that authorization to exact
`NetworkDestination` values and the resulting tool diagnostics.

## Variability register

The following table summarizes the variability documented in this chapter.

| Item | Location | Nature | Constraint |
|------|----------|--------|------------|
| Tool descriptor identity derivation | Section 42.1 | MAY | Must be deterministic across implementations. |
| Side-effect class assignment | Section 42.1 | MAY | Must be one of `read_only`, `write`, `network`, `stateful`. |
| Capability identifier format | Section 42.1 | MAY | Must match `tool.<name>.<operation>` pattern. |
| Tool descriptor field order | Section 42.1 | SHOULD | Must include all required fields. Order is informational. |
| Retrieval request field order | Section 42.1 | SHOULD | Must include all required fields. Order is informational. |
| Code-execution request field order | Section 42.1 | SHOULD | Must include all required fields. Order is informational. |
| Connector capability list | Section 42.1 | MAY | Must include at least `list_tools`, `prepare_tool_operation`, and `normalize_tool_result`. |
| Connector authentication binding | Section 42.1 | Required for authenticated connectors | User-controlled, versioned, and outside the plugin artifact; must contain no credential or opaque handle. |
| Connector credential custody | Section 42.1 | Required for end-user distributions | Authenticated operations must use Section 44 custody; host-local compatibility cannot claim separated custody. |
| Framework plugin query order | Section 42.2 | MAY | Must query all approved framework plugins. Order is informational. |
| Tool descriptor timeout | [Tool descriptor identity and properties](#tool-descriptor-identity-and-properties) | Implementation limit | Positive `timeout_ms` no greater than the published maximum; reject larger values with `tool.execution.exhausted-timeout`. |
| Code execution timeout | [Code-execution request and result schema](#code-execution-request-and-result-schema) | Implementation limit | Positive `timeout_ms` no greater than the published maximum; reject larger values with `tool.execution.exhausted-timeout`. |
| Retrieval timeout | [Retrieval request and result schema](#retrieval-request-and-result-schema) | Fixed | Cancel at exactly 60 seconds with `tool.execution.timeout`; configuration cannot alter the boundary. |
| Sandbox memory limit | [Code-execution request and result schema](#code-execution-request-and-result-schema) | Implementation limit | At least 64 MB and published; reject larger requests with `tool.execution.exhausted-memory`. |
| Sandbox network access | [Code-execution request and result schema](#code-execution-request-and-result-schema) | Fixed authorization rule | `network_tool` must name an active network-class tool and the agent must hold its matching capability; configuration may further restrict access but cannot grant denied access. |
| Authorized sandbox destinations | [Code-execution request and result schema](#code-execution-request-and-result-schema) | Fixed schema and intersection | Exact canonical destinations only; deny an empty intersection and reject a non-member before network I/O. |
| Diagnostic message format | Section 42.3 | MAY | Must include all required fields. Free-text portion is informational. |
| Evidence record field order | Section 42.3 | SHOULD | Must include all required fields. Order is informational. |
| Integration test ordering | Section 42.4 | MAY | Must cover all required scenarios. Order is informational. |
| Cross-milestone fixture selection | Section 42.4 | MUST | Must include all fixtures listed in section 42.4.4. |
