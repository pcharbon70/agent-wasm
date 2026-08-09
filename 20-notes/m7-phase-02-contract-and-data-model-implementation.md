---
title: "Phase 2 Contract And Data Model Implementation"
kind: note
created: "2026-08-09"
maturity: seed
tags:
  - milestone-07
  - phase-02
  - implementation
  - contract-and-data-model
  - tool-catalogs
  - retrieval
  - code-execution
  - connectors
aliases:
  - "M7-P2-2.1 Implementation"
---

# Phase 2 Contract And Data Model Implementation

## Overview

This note documents the implementation of Section 2.1 (Contract And Data Model) from
[Phase 2 - Tool Catalogs Retrieval Code Execution And Connectors](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/phase-02-tool-catalogs-retrieval-code-execution-and-connectors.md)
of
[Milestone 7](../.spec/planning/agentic-system/milestone-07-ai-tools-memory-and-human-control/README.md).

The implementation produced the specification chapter
[42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
which establishes the contract and data model for tool catalogs, retrieval,
code execution, and connectors.

## Subtask 2.1.1.1: Tool Descriptor Identity and Properties

### Implementation

Defined the following fields for tool descriptors:

| Field | Content | Source |
|-------|---------|--------|
| `tool_id` | Deterministic tool identity derived from tool name, version, and framework plugin identifier | Host runtime |
| `name` | Tool name (e.g., `search`, `code_interpreter`, `email_send`) | Framework plugin |
| `version` | Semantic version of the tool (e.g., `1.2.3`) | Framework plugin |
| `description` | Human-readable description of the tool's purpose and behavior | Framework plugin |
| `input_schema` | JSON Schema for the tool's input parameters | Framework plugin |
| `output_schema` | JSON Schema for the tool's output result | Framework plugin |
| `capability` | Capability identifier granted to agents for using this tool | Capability policy |
| `side_effect_class` | Side-effect class: `read_only`, `write`, `network`, `stateful` | Framework plugin |
| `idempotent` | Whether the tool is idempotent (safe to retry without side effects) | Framework plugin |
| `timeout_ms` | Maximum execution time in milliseconds | Framework plugin |
| `result_limits` | Limits on the result size (e.g., `max_bytes`, `max_tokens`, `max_items`) | Framework plugin |
| `provenance_required` | Whether provenance evidence is required for this tool's results | Framework plugin |
| `framework_plugin` | Framework plugin identifier that provides this tool | Framework plugin |
| `created_at` | ISO 8601 timestamp of descriptor creation | Host clock |
| `status` | Current status: `active`, `deprecated`, `suspended` | Host runtime |

### Design decisions

1. **Deterministic `tool_id`**: Enables idempotent tool resolution and
   ensures that the same tool version from the same framework plugin
   produces the same identifier. Consistent with the deterministic
   reducer semantics defined in
   [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md).

2. **Side-effect classification**: Tools are classified by their side-effect
   class to enable capability policy enforcement and resource bounding.
   The hierarchy (`read_only` < `write` < `network` < `stateful`) ensures
   that tools with broader side effects require higher-privilege capabilities.

3. **Capability binding**: Each tool is bound to a capability identifier
   that determines the minimum privilege required to use it. This is
   consistent with the capability policy defined in
   [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md).

4. **Framework plugin origin**: Tools originate from framework plugins,
   which are isolated in their own tenant and subject to the framework
   plugin manifest contract defined in
   [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md).

## Subtask 2.1.1.2: Retrieval Request and Result Schema

### Implementation

#### Retrieval request fields

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | Deterministic retrieval request identity derived from agent address, query hash, and timestamp | Host runtime |
| `agent_address` | `TenantQualifiedAgentAddress` of the agent that originated the request | Agent |
| `query` | Search query or knowledge base lookup string | Agent |
| `tenant_scope` | Tenant scope for the retrieval (e.g., `self`, `team`, `organization`) | Agent |
| `filters` | Filters applied to the retrieval (e.g., `source_type`, `date_range`, `tags`) | Agent |
| `ranking` | Ranking metadata (e.g., `relevance`, `recency`, `authority`) | Agent |
| `max_results` | Maximum number of results to return | Agent |
| `created_at` | ISO 8601 timestamp of request creation | Host clock |
| `status` | Current status: `pending`, `completed`, `failed`, `cancelled` | Host runtime |

#### Retrieval result fields

| Field | Content | Source |
|-------|---------|--------|
| `result_id` | Deterministic retrieval result identity derived from `request_id` and result sequence number | Host runtime |
| `request_id` | `request_id` of the associated retrieval request | Normalized from retrieval source |
| `items` | List of retrieved items (each with content, metadata, and citation) | Normalized from retrieval source |
| `total_results` | Total number of results available (before `max_results` limit) | Normalized from retrieval source |
| `ranking_metadata` | Ranking metadata used for this retrieval | Normalized from retrieval source |
| `created_at` | ISO 8601 timestamp of result creation | Host clock |

#### Retrieval item fields

| Field | Content | Source |
|-------|---------|--------|
| `content` | Retrieved content (text, JSON, or binary reference) | Normalized from retrieval source |
| `metadata` | Item metadata (source, author, date, tags, relevance score) | Normalized from retrieval source |
| `citation` | Citation string for attribution and provenance | Normalized from retrieval source |
| `content_ref` | Bounded content reference (hash or URL) for deduplication | Normalized from retrieval source |

### Design decisions

1. **Tenant scope enforcement**: The `tenant_scope` field ensures that
   retrieval operations are scoped to the appropriate tenant boundaries.
   This is consistent with the threat model defined in
   [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md).

2. **Content deduplication**: The `content_ref` field enables deduplication
   of retrieval results and prevents redundant storage of identical content.
   This is consistent with the storage contract defined in
   [Revisioned Snapshots Journals History And Storage Contracts](../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md).

3. **Citation and provenance**: Each retrieval item includes a citation
   string for attribution and provenance. This is consistent with the
   provenance contract defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

## Subtask 2.1.1.3: Code-Execution Request and Result Schema

### Implementation

#### Code-execution request fields

| Field | Content | Source |
|-------|---------|--------|
| `request_id` | Deterministic code-execution request identity derived from agent address, code hash, and timestamp | Host runtime |
| `agent_address` | `TenantQualifiedAgentAddress` of the agent that originated the request | Agent |
| `language` | Programming language of the code (e.g., `python`, `javascript`, `rust`) | Agent |
| `code` | Code to execute (redacted reference for storage) | Agent |
| `inputs` | Input data for the code execution | Agent |
| `environment` | Immutable execution environment (e.g., `python:3.11-slim`, `node:20-alpine`) | Agent |
| `capability` | Capability identifier granted to agents for code execution (e.g., `code.execute`) | Capability policy |
| `resource_budget` | Resource budget for execution (e.g., `max_memory_mb`, `max_cpu_seconds`, `max_network_requests`) | Agent |
| `isolation_class` | Isolation class: `shared`, `tenant`, `isolated` | Agent |
| `timeout_ms` | Maximum execution time in milliseconds | Agent |
| `created_at` | ISO 8601 timestamp of request creation | Host clock |
| `status` | Current status: `pending`, `executing`, `completed`, `failed`, `cancelled` | Host runtime |

#### Code-execution result fields

| Field | Content | Source |
|-------|---------|--------|
| `result_id` | Deterministic code-execution result identity derived from `request_id` and result sequence number | Host runtime |
| `request_id` | `request_id` of the associated code-execution request | Normalized from code executor |
| `exit_code` | Exit code of the code execution (0 for success, non-zero for failure) | Normalized from code executor |
| `stdout` | Standard output of the code execution (redacted reference for storage) | Normalized from code executor |
| `stderr` | Standard error of the code execution (redacted reference for storage) | Normalized from code executor |
| `artifacts` | Output artifacts (e.g., files, images, data) | Normalized from code executor |
| `resource_usage` | Resource usage (e.g., `memory_mb`, `cpu_seconds`, `network_requests`) | Normalized from code executor |
| `execution_time_ms` | Actual execution time in milliseconds | Normalized from code executor |
| `created_at` | ISO 8601 timestamp of result creation | Host clock |

### Design decisions

1. **Immutable execution environment**: The `environment` field specifies
   an immutable execution environment (e.g., Docker image) to ensure
   reproducibility and security. This is consistent with the isolation
   contract defined in
   [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md).

2. **Resource budgeting**: The `resource_budget` field enables per-request
   resource bounding to prevent resource exhaustion. This is consistent
   with the capability policy defined in
   [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md).

3. **Isolation classes**: The `isolation_class` field enables different
   levels of isolation based on the trust level of the code:
   - `shared`: Shared execution environment (low trust, limited capabilities)
   - `tenant`: Tenant-isolated execution environment (medium trust)
   - `isolated`: Fully isolated execution environment (high trust)

4. **Redacted storage**: The `code`, `stdout`, and `stderr` fields are
   stored with redacted references to protect sensitive data. This is
   consistent with the security contract defined in
   [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md).

5. **Artifact tracking**: The `artifacts` field tracks output artifacts
   (e.g., files, images, data) generated by code execution. This enables
   downstream tools and agents to consume the artifacts.

## Cross-references

- Section 42.1: [Tool Catalogs Retrieval Code Execution And Connectors Contract And Data Model](../60-specification/42-tool-catalogs-retrieval-code-execution-and-connectors-contract-and-data-model.md)
- Deterministic reducer semantics: [Deterministic Reducer Semantics And Milestone Acceptance](../60-specification/14-deterministic-reducer-semantics-and-milestone-acceptance.md)
- Capability policy: [Capability Policy Attenuation Limits And Enforcement](../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)
- Framework plugin model: [Framework Plugin Manifests Composition And Lifecycle Hooks](../60-specification/32-framework-plugin-manifests-composition-and-lifecycle-hooks.md)
- Threat model: [Threat Model Principals Trust Classes And Grant Vocabulary](../60-specification/30-threat-model-principals-trust-classes-and-grant-vocabulary.md)
- Storage contract: [Revisioned Snapshots Journals History And Storage Contracts](../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)
- Security and audit: [Provenance Signing Audit Security And Milestone Acceptance](../60-specification/34-provenance-signing-audit-security-and-milestone-acceptance.md)
- Isolation: [Synchronous Host Functions WASI Restrictions And Tenant Isolation](../60-specification/33-synchronous-host-functions-wasi-restrictions-and-tenant-isolation.md)

## Open questions

1. Should tools be versioned independently or as part of the framework
   plugin? The current design binds tools to framework plugins, but
   this may be too restrictive for tools that evolve independently.

2. Should the `tenant_scope` field support hierarchical scoping (e.g.,
   `organization.team.agent`)? The current design supports flat scopes.

3. Should code execution support stateful sessions or only stateless
   executions? The current design is stateless, but some tools (e.g.,
   REPLs) may benefit from stateful sessions.

4. Should connector authentication be handled by the host or by the
   agent? The current design delegates authentication to the connector
   framework plugin, but this may limit the host's ability to enforce
   cross-tenant isolation.
