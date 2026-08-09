---
title: "Phase 2 Failure Evidence And Operational Notes Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-02
  - implementation
  - failure-evidence
  - diagnostics
  - evidence-emission
  - implementation-defined-choices
aliases:
  - "M7-P2-2.3 Implementation"
---

# Phase 2 Failure Evidence And Operational Notes Implementation

## Overview

This note documents the implementation of Section 2.3 (Failure Evidence And Operational Notes) from
[Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md)
which establishes the failure evidence and operational notes for tool
catalogs, retrieval, code execution, and connectors.

## Subtask 2.3.1.1: Failure Outcomes

### Malformed outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.request.malformed` | Tool execution request with missing required fields. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-tool_id` | Tool execution request with invalid `tool_id` format. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-input` | Tool execution request with invalid `input` data. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-language` | Code execution request with invalid `language` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-code` | Code execution request with invalid `code` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-environment` | Code execution request with invalid `environment` field. | Reject request; do NOT create partial execution state. |
| `tool.request.malformed-query` | Retrieval request with missing or invalid `query` field. | Reject request; do NOT create partial execution state. |
| `tool.result.malformed-output` | Tool result with invalid `output` data. | Reject result; do NOT create partial result state. |
| `tool.result.malformed-usage` | Tool result with invalid `resource_usage` metrics. | Reject result; do NOT create partial result state. |

### Incompatible outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unknown_tool` | Tool execution request with unknown `tool_id`. | Reject request; do NOT create partial execution state. |
| `tool.execution.schema_mismatch` | Tool execution request input does not conform to the tool's `input_schema`. | Reject request; do NOT create partial execution state. |
| `tool.execution.result_schema_mismatch` | Tool result does not conform to the tool's `output_schema`. | Reject result; do NOT create partial result state. |
| `tool.execution.stale_catalog` | Tool descriptor version does not match the cached catalog version. | Reject request; do NOT create partial execution state. |

### Conflicting outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.duplicate-id` | Two tool execution requests with the same `request_id` submitted concurrently. | Reject second request; do NOT create partial execution state. |
| `tool.execution.conflicting-cancellation` | Two cancellation requests for the same `request_id` submitted concurrently. | Reject second cancellation; do NOT create partial execution state. |

### Unauthorized outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.denied_capability` | Tool execution request whose `agent_address` does not have the required capability. | Reject request; do NOT create partial execution state. |
| `tool.execution.cross-tenant-data` | Tool execution request that accesses cross-tenant data. | Reject request; do NOT create partial execution state. |
| `tool.execution.unauthorized_connector` | Tool execution request using an unauthorized connector. | Reject request; do NOT create partial execution state. |

### Exhausted outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.quota_exhausted` | Agent's capability budget is insufficient to cover the request. | Reject request; do NOT create partial execution state. |
| `tool.execution.exhausted-concurrency` | Host would exceed the implementation-defined maximum number of concurrent tool executions. | Reject request; do NOT create partial execution state. |
| `tool.execution.exhausted-code` | Host would exceed the implementation-defined maximum number of concurrent code executions. | Reject request; do NOT create partial execution state. |
| `tool.execution.timeout` | Tool execution exceeded the `timeout_ms` limit. | Cancel execution; do NOT create partial result state. |

### Unavailable outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unavailable_tool` | Tool is not active in the framework plugin registry. | Reject request; do NOT create partial execution state. |
| `tool.execution.unavailable_connector` | Connector is not active in the connector registry. | Reject request; do NOT create partial execution state. |
| `tool.execution.sandbox_failure` | Code execution failed due to sandbox restrictions. | Cancel execution; do NOT create partial result state. |
| `tool.execution.connector_failure` | Connector failed to execute the tool. | Cancel execution; do NOT create partial result state. |

### Safety outcomes

| Diagnostic | Cause | Host behavior |
|------------|-------|---------------|
| `tool.execution.unsafe_output` | Tool result contains content that fails the safety filter. | Reject result; emit safety metadata in diagnostics. |
| `tool.execution.provenance_loss` | Tool result is missing required provenance evidence. | Reject result; emit provenance warning in diagnostics. |

### Design decisions

1. **Atomic rejection**: Every failure outcome MUST reject without creating
   partial execution or result state. This is consistent with the atomic
   commit protocol defined in
   [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md).

2. **Consistent diagnostic format**: All diagnostics follow a consistent
   naming convention (`tool.request.*`, `tool.execution.*`, `tool.result.*`)
   and include the same set of fields, enabling consistent handling by
   downstream components.

3. **Cross-tenant rejection**: Cross-tenant data access is rejected outright
   to prevent authority leaks. This is consistent with the threat model
   defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

4. **Safety and provenance**: Safety-related and provenance-related
   diagnostics emit warnings in diagnostics to enable downstream filtering
   and auditing.

## Subtask 2.3.1.2: Bounded Diagnostics and Evidence

### Diagnostic fields

Every diagnostic MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `diagnostic` | The failure diagnostic code (e.g., `tool.execution.malformed`). | Host runtime |
| `phase` | The phase that produced the diagnostic (`Phase 2`). | Host runtime |
| `section` | The section that produced the diagnostic (e.g., `42.3`). | Host runtime |
| `contract` | The contract that produced the diagnostic (e.g., `Tool Catalogs Retrieval Code Execution And Connectors`). | Host runtime |
| `profile` | The conformance profile that produced the diagnostic. | Host runtime |
| `failed_boundary` | The failed boundary (e.g., `tool.execution.create`, `tool.execution.execute`, `tool.execution.cancel`). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of diagnostic emission. | Host clock |
| `message` | A human-readable description of the failure. | Host runtime |

### Evidence record fields

Every evidence record MUST include the following fields:

| Field | Content | Source |
|-------|---------|--------|
| `evidence_type` | The evidence type (`tool.execution.requested`, `tool.execution.completed`, `tool.execution.failed`, `tool.execution.cancelled`, `tool.execution.result`, `retrieval.requested`, `retrieval.completed`, `retrieval.failed`, `code.requested`, `code.completed`, `code.failed`, `code.completed`). | Host runtime |
| `request_id` | The `request_id` of the tool/retrieval/code execution request. | Host runtime |
| `agent_address` | The `TenantQualifiedAgentAddress` of the agent that originated the request. | Host runtime |
| `tool_id` | The `tool_id` of the tool executed (for tool executions). | Host runtime |
| `language` | The `language` of the code executed (for code executions). | Host runtime |
| `timestamp` | The ISO 8601 timestamp of evidence emission. | Host clock |
| `evidence_digest` | A deterministic hash of the evidence record. | Host runtime |

### Design decisions

1. **Bounded diagnostics**: Diagnostics identify the phase contract, profile,
   and failed boundary without exposing secrets. This is consistent with
   the security requirements defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

2. **Tamper-evident evidence**: The `evidence_digest` field enables
   downstream systems to verify that the evidence record has not been
   tampered with after creation.

3. **Comprehensive evidence types**: The evidence types cover all phases
   of tool/retrieval/code execution: requested, completed, failed,
   cancelled, and result.

4. **Contextual fields**: The `tool_id` and `language` fields provide
   additional context for tool and code executions, respectively.

## Subtask 2.3.1.3: Implementation-Defined Choices and Deferred Work

### Implementation-defined choices

| Choice | Description | Constraint |
|--------|-------------|------------|
| Maximum concurrent tool executions | The maximum number of concurrent tool executions. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent code executions | The maximum number of concurrent code executions. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Maximum concurrent retrieval requests | The maximum number of concurrent retrieval requests. | Must be at least 1 and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Tool execution timeout | The default maximum duration of a tool execution before timeout. | Must be longer than the maximum expected tool execution duration. Must be documented in the conformance profile. |
| Code execution timeout | The default maximum duration of a code execution before timeout. | Must be longer than the maximum expected code execution duration. Must be documented in the conformance profile. |
| Retrieval timeout | The default maximum duration of a retrieval request before timeout. | Must be longer than the maximum expected retrieval duration. Must be documented in the conformance profile. |
| Sandbox memory limit | The maximum memory for code execution sandboxes. | Must be at least 64 MB and at most the implementation-defined maximum. Must be documented in the conformance profile. |
| Sandbox network access | Whether code execution sandboxes have network access. | Must be configurable per tool or globally. Must be documented in the conformance profile. |

### Deferred work

The following work is deferred to future phases or milestones:

1. **Tool composition**: Composing multiple tools into a single compound
   tool is deferred to Milestone 8.

2. **Tool versioning**: Automatic tool version upgrades and rollback is
   deferred to Milestone 8.

3. **Tool marketplace**: A marketplace for third-party tools is deferred
   to Milestone 9.

4. **Tool analytics**: Analytics and metrics for tool usage is deferred
   to Milestone 9.

5. **Connector authentication caching**: Caching connector authentication
   tokens is deferred to Milestone 8.

### Design decisions

1. **Documented constraints**: Implementation-defined choices are documented
   in the conformance profile to ensure they are auditable and
   transparent.

2. **Deferred work**: The deferred work items are not within the scope
   of Phase 2 but may be addressed in future phases. Implementations
   MUST NOT implement deferred work without evidence from the
   corresponding future phase.

## Cross-references

- Section 42.3: [Tool Catalogs Retrieval Code Execution And Connectors Failure Evidence And Operational Notes](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-failure-evidence-and-operational-notes.md)
- Section 42.1: [Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- Section 42.2: [Tool Catalogs Retrieval Code Execution And Connectors Behavior And Integration](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-behavior-and-integration.md)
- Atomic commit protocol: [Atomic State Journal And Directive-Outbox Commits](../60-specification/26-atomic-state-journal-and-directive-outbox-commits.md)
- Threat model: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Security and audit: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Profile boundaries: [Profile Vocabulary And Architectural Boundaries](../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)
- Framework plugins: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)

## Open questions

1. Should the diagnostic format include the full stack trace or just the
   failed boundary? The current design includes only the failed boundary
   to avoid exposing implementation details, but this may make debugging
   harder.

2. Should the evidence record include the full request/response payload or
   just a hash? The current design includes only the hash (via
   `evidence_digest`), but this may make it harder to reconstruct the
   full context of a failure.

3. Should implementation-defined choices have default values or be required?
   The current design requires them to be documented, but this may be
   burdensome for simple deployments.

4. Should sandbox network access be disabled by default or enabled by
   default? The current design leaves this configurable, but a default
   would improve security out of the box.
