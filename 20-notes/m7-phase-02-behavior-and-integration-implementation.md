---
title: "Phase 2 Behavior And Integration Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-02
  - implementation
  - behavior-and-integration
  - capability-resolution
  - tool-execution
  - outcome-definitions
aliases:
  - "M7-P2-2.2 Implementation"
---

# Phase 2 Behavior And Integration Implementation

## Overview

This note documents the implementation of Section 2.2 (Behavior And Integration) from
[Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md)
which establishes the behavior and integration rules for tool catalogs,
retrieval, code execution, and connectors.

## Subtask 2.2.1.1: Tool Resolution and Catalog Policy Filtering

### Implementation

#### Tool resolution flow

When a strategy or model requests the tool catalog, the host MUST:

1. **Query framework plugins**: Query all approved framework plugins for
   their registered tools.
2. **Validate descriptors**: Validate each tool descriptor against the
   schema defined in section 42.1. Invalid descriptors MUST be excluded
   from the catalog.
3. **Filter by status**: Exclude tools with status `deprecated` or
   `suspended` from the catalog.
4. **Apply capability policy**: Filter the catalog to include only tools
   for which the requesting agent has the required capability.
5. **Apply tenant scope**: Apply tenant scope filters to ensure that
   tools do not expose cross-tenant data.
6. **Return filtered catalog**: Return the filtered catalog to the
   requesting strategy or model.

### Design decisions

1. **Framework plugin querying**: Tools originate from framework plugins,
   which are approved by the host and isolated in their own tenant.
   This is consistent with the framework plugin model defined in
   [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).

2. **Descriptor validation**: Invalid tool descriptors are excluded from
   the catalog to prevent agents from using tools with malformed schemas.
   This ensures that tool execution proceeds with valid inputs and outputs.

3. **Status filtering**: Tools with status `deprecated` or `suspended`
   are excluded from the catalog to prevent agents from using tools that
   are no longer supported or have been disabled due to security issues.

4. **Capability-based filtering**: The catalog is filtered based on the
   agent's capabilities to ensure that agents only see tools they have
   been granted access to. This is consistent with the capability policy
   defined in
   [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md).

5. **Tenant scope enforcement**: Tenant scope filters ensure that tools
   do not expose cross-tenant data. This is consistent with the threat
   model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
   and the tenant isolation contract defined in
   [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

## Subtask 2.2.1.2: Tool Execution Through Durable Effect Attempts

### Implementation

#### Tool execution flow

When the host receives a tool execution request, it MUST:

1. **Validate the request**: Validate the request against the schema
   defined in section 42.1. Invalid requests MUST be rejected with the
   appropriate diagnostic.
2. **Check capabilities**: Verify that the agent has the required
   capability for the tool. Insufficient capabilities MUST be rejected
   with `tool.execution.denied_capability`.
3. **Check the catalog**: Verify that the tool is active and available
   in the filtered catalog. Stale or unavailable tools MUST be rejected
   with `tool.execution.unknown_tool` or `tool.execution.stale_catalog`.
4. **Create the effect attempt**: Create a durable effect attempt for
   the tool execution. The attempt captures the request, the tool
   descriptor, and the execution context.
5. **Execute the tool**: Invoke the tool through the framework plugin
   or connector interface. The execution is bounded by the `timeout_ms`
   and `resource_budget` fields.
6. **Normalize the result**: Normalize the tool result into the common
   format defined in section 42.1. Normalization includes schema
   validation, content filtering, and provenance capture.
7. **Emit the result signal**: Emit a `tool.execution.result` signal
   with the normalized result.
8. **Record the attempt**: Record the effect attempt in the durable
   journal with the result.

### Design decisions

1. **Durable effect attempts**: Tool executions are mediated through
   durable effect attempts to ensure auditability, replayability, and
   crash-resistance. This is consistent with the deterministic reducer
   semantics defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
   and the effect handler contract defined in
   [Effect Handlers Attempts Idempotency And Result Signals](../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md).

2. **Capability pre-check**: The host checks capabilities before creating
   the effect attempt to avoid wasting resources on unauthorized executions.
   This is consistent with the capability policy defined in
   [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md).

3. **Catalog validation**: The host validates that the tool is active
   and available in the filtered catalog before executing. This prevents
   agents from executing tools that have been deprecated, suspended, or
   revoked.

4. **Bounded execution**: The execution is bounded by the `timeout_ms`
   and `resource_budget` fields to prevent resource exhaustion. This is
   consistent with the resource bounding defined in
   [Profile Vocabulary And Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md).

5. **Result normalization**: The host normalizes tool results into a
   common format to ensure consistency across different tool implementations.
   Normalization includes schema validation, content filtering, and
   provenance capture.

6. **Result signal emission**: The host emits a `tool.execution.result`
   signal with the normalized result to enable downstream components
   (such as strategies and models) to react to tool execution results.

## Subtask 2.2.1.3: Outcome Definitions

### Implementation

#### Tool execution outcomes

| Outcome | Diagnostic | Cause | Host behavior |
|---------|------------|-------|---------------|
| Unknown tool | `tool.execution.unknown_tool` | Tool reference does not match any active descriptor in the catalog. | Reject execution; do NOT create partial execution state. |
| Schema mismatch | `tool.execution.schema_mismatch` | Request input does not conform to the tool's `input_schema`. | Reject execution; do NOT create partial execution state. |
| Schema mismatch | `tool.execution.result_schema_mismatch` | Tool result does not conform to the tool's `output_schema`. | Reject result; emit `tool.execution.failed` signal. |
| Denied capability | `tool.execution.denied_capability` | Agent does not have the required capability for the tool. | Reject execution; do NOT create partial execution state. |
| Stale catalog | `tool.execution.stale_catalog` | Tool descriptor version does not match the cached catalog version. | Reject execution; do NOT create partial execution state. |
| Unsafe output | `tool.execution.unsafe_output` | Tool result contains content that fails the safety filter. | Reject result; emit `tool.execution.failed` signal with safety metadata. |
| Sandbox failure | `tool.execution.sandbox_failure` | Code execution failed due to sandbox restrictions. | Cancel execution; emit `tool.execution.failed` signal. |
| Partial connector success | `tool.execution.partial_connector_success` | Connector returned a partial result. | Accept the partial result but mark it as partial in diagnostics. |
| Provenance loss | `tool.execution.provenance_loss` | Tool result is missing required provenance evidence. | Reject result; emit `tool.execution.failed` signal. |

### Design decisions

1. **Atomic rejection**: Every failure outcome MUST reject without creating
   partial execution state. This is consistent with the atomic commit
   protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md).

2. **Schema validation**: Schema validation is performed both for inputs
   (before execution) and outputs (after execution) to ensure data
   integrity.

3. **Safety filtering**: Unsafe outputs are rejected to prevent the
   propagation of harmful content (e.g., PII, malicious code, offensive
   content). This is consistent with the security contract defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

4. **Partial results**: Partial connector results are accepted but marked
   as partial in diagnostics to enable downstream components to handle
   incomplete data appropriately.

5. **Provenance requirements**: Tools that require provenance evidence
   must capture it during execution. Missing provenance results in
   rejection to ensure auditability.

## Cross-references

- Section 42.2: [Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md)
- Section 42.1: [Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- Framework plugin model: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Threat model: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Tenant isolation: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)
- Deterministic reducer: [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Effect handlers: [Effect Handlers Attempts Idempotency And Result Signals](../60-specification/27-effect-handlers-attempts-idempotency-and-result-signals.md)
- Atomic commit: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Security and audit: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)

## Open questions

1. Should the host cache the filtered catalog or regenerate it on each
   request? The current design regenerates the catalog on each request,
   but caching may improve performance at the cost of staleness.

2. Should tool execution support streaming results or only final results?
   The current design emits a single `tool.execution.result` signal for
   the final result, but some tools (e.g., long-running searches) may
   benefit from streaming partial results.

3. Should the host retry on `tool.execution.sandbox_failure` or reject
   outright? The current design rejects outright, but some sandbox
   failures (e.g., temporary resource exhaustion) may be transient.

4. Should provenance loss be a hard rejection or a warning? The current
   design rejects outright, but this may be too strict for tools that
   capture provenance asynchronously.
