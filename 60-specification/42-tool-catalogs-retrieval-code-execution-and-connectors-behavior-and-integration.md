---
title: "Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration"
kind: specification
created: "2026-08-09"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-07
  - phase-02
  - tool-catalogs
  - retrieval
  - code-execution
  - connectors
  - behavior
  - integration
  - capability-resolution
  - tool-execution
  - outcome-definitions
aliases:
  - "M7-P2 Behavior And Integration"
---

# Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration

## Status and authority

This chapter is a draft specification produced by
[Phase 2](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md)
--
AI, Tools, Memory, And Human Control.
It establishes the behavior and integration rules for tool catalogs,
retrieval, code execution, and connectors, including tool resolution,
catalog policy filtering, execution through durable effect attempts,
and outcome definitions.

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
[Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md).

## 42.2 Behavior And Integration

### Tool resolution and catalog policy filtering

> **Normative definition.**
The host MUST resolve tools from approved framework plugins and policy-filter
the catalog before presenting it to a strategy or model.
Tool resolution ensures that only tools with valid descriptors and active
status are available, while catalog policy filtering ensures that only
tools the agent has been granted capabilities for are visible.

> **Normative definition.**
When a strategy or model requests the tool catalog, the host MUST:

1. **Query framework plugins**: The host MUST query all approved framework
   plugins for their registered tools.
2. **Validate descriptors**: The host MUST validate each tool descriptor
   against the schema defined in section 42.1. Invalid descriptors MUST
   be excluded from the catalog.
3. **Filter by status**: The host MUST exclude tools with status
   `deprecated` or `suspended` from the catalog.
4. **Apply capability policy**: The host MUST filter the catalog to include
   only tools for which the requesting agent has the required capability.
   Agents without the required capability MUST NOT see the tool.
5. **Apply tenant scope**: The host MUST apply tenant scope filters to
   ensure that tools do not expose cross-tenant data.
6. **Return filtered catalog**: The host MUST return the filtered catalog
   to the requesting strategy or model.

> **Non-normative note.**
Tool resolution and catalog policy filtering ensure that agents only see
and can use tools they have been explicitly granted access to.
This is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
and the tenant isolation contract defined in
[Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

### Tool execution through durable effect attempts

> **Normative definition.**
Tools, retrieval, code, and connectors are executed through durable effect
attempts with normalized result signals.
Execution is mediated by the host runtime through the effect handler
mechanism defined in
[Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md).

> **Normative definition.**
When the host receives a tool execution request, it MUST:

1. **Validate the request**: The host MUST validate the request against
   the schema defined in section 42.1. Invalid requests MUST be rejected
   with the appropriate diagnostic.
2. **Check capabilities**: The host MUST verify that the agent has the
   required capability for the tool. Insufficient capabilities MUST be
   rejected with `tool.execution.denied_capability`.
3. **Check the catalog**: The host MUST verify that the tool is active
   and available in the filtered catalog. Stale or unavailable tools MUST
   be rejected with `tool.execution.unknown_tool` or `tool.execution.stale_catalog`.
4. **Create the effect attempt**: The host MUST create a durable effect
   attempt for the tool execution. The attempt captures the request,
   the tool descriptor, and the execution context.
5. **Execute the tool**: The host MUST invoke the tool through the
   framework plugin or connector interface. The execution is bounded by
   the `timeout_ms` and `resource_budget` fields.
6. **Normalize the result**: The host MUST normalize the tool result
   into the common format defined in section 42.1. Normalization includes
   schema validation, content filtering, and provenance capture.
7. **Emit the result signal**: The host MUST emit a `tool.execution.result`
   signal with the normalized result.
8. **Record the attempt**: The host MUST record the effect attempt in
   the durable journal with the result.

> **Non-normative note.**
Tool execution through durable effect attempts ensures that all tool
operations are auditable, replayable, and crash-resistant.
This is consistent with the deterministic reducer semantics defined in
[Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md).

### Capability mapping for tool execution

> **Normative definition.**
The host MUST map the agent's grants to tool execution capabilities using
the following rules:

| Agent Grant | Tool Capability |
|-------------|----------------|
| `tool.<name>.read` | Execute tools with side-effect class `read_only` |
| `tool.<name>.write` | Execute tools with side-effect class `write` or `read_only` |
| `tool.<name>.network` | Execute tools with side-effect class `network`, `write`, or `read_only` |
| `tool.<name>.stateful` | Execute tools with any side-effect class |
| `code.execute` | Execute code execution requests |
| `retrieval.execute` | Execute retrieval requests |
| `connector.<name>.execute` | Execute tools provided by the connector |

> **Non-normative note.**
Capability mapping ensures that agents only have access to the tools and
operations that they have been granted.
This is consistent with the capability policy defined in
[Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md).

### Outcome definitions

> **Normative definition.**
The following outcomes are defined for tool catalogs, retrieval, code
execution, and connectors.
Each outcome describes a specific failure condition and the expected
host behavior.

#### Unknown tool

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unknown_tool` | Tool reference does not match any active descriptor in the catalog. | Reject execution; do NOT create partial execution state. |

> **Non-normative note.**
Unknown tool is caused by the agent referencing a tool that is not in
the filtered catalog (e.g., deprecated, suspended, or not granted).
The agent MUST update the tool reference and retry.

#### Schema mismatch

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.schema_mismatch` | Request input does not conform to the tool's `input_schema`. | Reject execution; do NOT create partial execution state. |
| `tool.execution.result_schema_mismatch` | Tool result does not conform to the tool's `output_schema`. | Reject result; emit `tool.execution.failed` signal. |

> **Non-normative note.**
Schema mismatch is caused by invalid input or unexpected output format.
The agent MUST update the input or the tool schema and retry.

#### Denied capability

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.denied_capability` | Agent does not have the required capability for the tool. | Reject execution; do NOT create partial execution state. |

> **Non-normative note.**
Denied capability is caused by the agent lacking the required grant.
The agent MUST request additional capability from the topology owner.

#### Stale catalog

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.stale_catalog` | Tool descriptor version does not match the cached catalog version. | Reject execution; do NOT create partial execution state. |

> **Non-normative note.**
Stale catalog is caused by the agent using a cached catalog that is out
of date with the server's catalog.
The agent MUST refresh the catalog and retry.

#### Unsafe output

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unsafe_output` | Tool result contains content that fails the safety filter. | Reject result; emit `tool.execution.failed` signal with safety metadata. |

> **Non-normative note.**
Unsafe output is caused by the tool returning content that violates
safety policies (e.g., PII, malicious code, offensive content).
The host MUST reject the result and emit a warning in diagnostics.

#### Sandbox failure

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.sandbox_failure` | Code execution failed due to sandbox restrictions (e.g., memory limit, network restriction). | Cancel execution; emit `tool.execution.failed` signal. |

> **Non-normative note.**
Sandbox failure is caused by the code violating sandbox restrictions.
The agent MUST update the code to comply with the sandbox policies.

#### Partial connector success

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.partial_connector_success` | Connector returned a partial result (e.g., some items retrieved, some failed). | Accept the partial result but mark it as partial in diagnostics. |

> **Non-normative note.**
Partial connector success is caused by the connector returning a subset
of the requested data (e.g., due to rate limits, partial failures).
The host MUST accept the partial result but emit a warning in diagnostics.

#### Provenance loss

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.provenance_loss` | Tool result is missing required provenance evidence. | Reject result; emit `tool.execution.failed` signal. |

> **Non-normative note.**
Provenance loss is caused by the tool or connector failing to capture
required provenance evidence.
The agent MUST update the tool or connector configuration to enable
provenance capture.

### Results that would invalidate an earlier milestone assumption

> **Non-normative note.**
The following results from Phase 2 behavior and integration would invalidate
an earlier milestone assumption:

1. **Tools bypass the durable journal**: If tool executions bypass the
   durable journal, this would invalidate the assumption defined in
   [Revisioned Snapshots Journals History And Storage Contracts](25-revisioned-snapshots-journals-history-and-storage-contracts.md)
   that all state transitions are durable across host restarts.
2. **Tools bypass the atomic commit protocol**: If tool executions bypass
   the atomic commit protocol, this would invalidate the assumption defined
   in [Atomic State Journal And Directive-Outbox Commits](26-atomic-state-journal-and-directive-outbox-commits.md)
   that all state transitions are atomic.
3. **Tools allow cross-tenant authority leaks**: If tools allow cross-tenant
   data access or result sharing, this would invalidate the assumption defined
   in [Threat Model Principals Trust Classes And Grant Vocabulary](30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   that all principals are isolated by tenant.
4. **Tools require shared mutable guest state**: If tools require shared
   mutable guest state, this would invalidate the assumption defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   that all state transitions are deterministic and replayable.

> **Non-normative note.**
These results would indicate a design flaw in Phase 2 and would require
a revision of the Phase 2 contracts before promotion to `status:
normative`.

### Cross-references and precedence

> **Non-normative note.**
This section's behavior and integration integrate with the following
earlier chapters:

1. For tool resolution: this section takes precedence over
   [Framework Plugin Manifests Composition And Lifecycle Hooks](32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
   for questions of tool-specific resolution.
2. For capability enforcement: this section takes precedence over
   [Capability Policy Attenuation Limits And Enforcement](31-capability-policy-attenuation-limits-and-enforcement.md)
   for questions of tool-specific capability mapping.
3. For tool execution: this section takes precedence over
   [Effect Handlers Attempts Idempotency And Result Signals](27-effect-handlers-attempts-idempotency-and-result-signals.md)
   for questions of tool-specific execution.
4. For tenant isolation: this section takes precedence over
   [Synchronous Host Functions WASI Restrictions And Tenant Isolation](33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
   for questions of tool-specific tenant isolation.
5. For provenance: this section takes precedence over
   [Provenance Signing Audit Security And Milestone Acceptance](34-provenance-signing-audit-security-and-milestone-acceptance.md)
   for questions of tool-specific provenance requirements.
6. Where both sections are applicable and agree, they are mutually
   reinforcing.
