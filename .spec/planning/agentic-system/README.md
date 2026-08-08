# Jido-Inspired Agentic System Roadmap

This roadmap turns the archive's Jido, Extism, WebAssembly, and assurance
research into a production-complete, architecture-neutral implementation
sequence. It targets a framework platform rather than a specific agent
application or generic web console.

## Purpose

Define the dependencies, contracts, implementation work, failure behavior, and
integration evidence needed to build a complete Jido-inspired agent system over
WebAssembly and Extism.

## What belongs here

Milestone indexes and phase plans for the agent protocol, decision semantics,
host runtime, durability, security, coordination, AI, assurance, and operations.

## Milestone Order

1. [Milestone 1 - Contracts, Profiles, And Artifacts](milestone-01-contracts-profiles-and-artifacts/README.md) — Establish the language-neutral vocabulary, compatibility rules, artifact model, and byte-level host–guest protocol on which every later runtime feature depends.
2. [Milestone 2 - Signals, Actions, State, And Strategies](milestone-02-signals-actions-state-and-strategies/README.md) — Implement the portable Jido-inspired decision vocabulary and deterministic reducer semantics independently of host scheduling and external effects.
3. [Milestone 3 - Host Actor Runtime And Lifecycle](milestone-03-host-actor-runtime-and-lifecycle/README.md) — Construct the host-owned live actor cell that serializes turns, invokes Extism reducers, manages lifecycle, and converts external events into signals.
4. [Milestone 4 - Durable State, Effects, And Recovery](milestone-04-durable-state-effects-and-recovery/README.md) — Make agent state transitions, history, directives, external effects, and activation recoverable across host crashes without claiming impossible exactly-once external behavior.
5. [Milestone 5 - Capabilities, Plugins, Security, And Tenancy](milestone-05-capabilities-plugins-security-and-tenancy/README.md) — Add host-owned authorization, composable framework plugins, artifact trust, resource governance, and defensible tenant isolation around untrusted guest code.
6. [Milestone 6 - Multi-Agent Coordination And Topology](milestone-06-multi-agent-coordination-and-topology/README.md) — Extend durable single-agent semantics to agent relationships, delegation, coordination, topology reconciliation, placement, and recoverable multi-agent workflows.
7. [Milestone 7 - AI, Tools, Memory, And Human Control](milestone-07-ai-tools-memory-and-human-control/README.md) — Layer provider-neutral model access, tools, retrieval, reasoning strategies, memory projections, approvals, quotas, and secret leases above the stable agent runtime.
8. [Milestone 8 - Portability, Verification, And Performance](milestone-08-portability-verification-and-performance/README.md) — Turn the research assurance design into release evidence spanning standards conformance, independent Extism runtimes, fuzzing, replay, isolation, fault behavior, and performance.
9. [Milestone 9 - Production Platform And Developer Experience](milestone-09-production-platform-and-developer-experience/README.md) — Package the runtime as an operable framework platform with stable host APIs, SDKs, local tooling, observability, upgrades, deployment guidance, and production acceptance evidence.

## Dependency Model

Milestones 1–5 establish the contract, semantic, runtime, durability, and trust
foundation. Milestone 6 adds multi-agent topology. Milestone 7 adds AI and
high-authority integrations. Milestone 8 turns all earlier fixtures into release
evidence. Milestone 9 packages the verified system for developers and operators.

Assurance work begins in every phase even though Milestone 8 owns the final
cross-runtime and release gates.

## Shared Conventions

- Numbering resets inside each milestone.
- Phases use `N`, sections use `N.M`, tasks use `N.M.K`, and subtasks use
  `N.M.K.L`.
- Every phase, section, task, and subtask uses an unchecked Markdown checkbox.
- Every phase, section, and task starts with a short description paragraph.
- Every phase ends with a final integration-testing section.
- One section is the intended implementation and commit boundary.
- Plans define behavior and interfaces without selecting a host language,
  database, transport, deployment platform, or AI provider.

## System-Wide Defaults

- The host owns authoritative state, policy, scheduling, effects, durability,
  topology, and audit evidence.
- Extism plug-ins implement portable decision logic through a versioned byte
  protocol.
- Canonical JSON is the bootstrap encoding.
- Durable directives and later result signals are preferred over synchronous
  host functions.
- Single-node correctness comes before horizontal coordination.
- Extism/Wasmtime and Extism/Wazero are the first independent runtime families.
- No milestone may claim exactly-once external effects without cooperation from
  the target system.

## Research Basis

- [Jido architecture and Wasm/Extism construction](../../../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
- [Extism plugin-system architecture](../../../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [WebAssembly foundations](../../../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Testing and assurance design](../../../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)

## Completion Definition

The roadmap is complete only when the supported profiles have reproducible
cross-runtime evidence, durable failure recovery, tenant isolation, bounded
resource behavior, operable deployment surfaces, and representative direct,
FSM, multi-agent, and tool-using workflows.

## Maintaining This Roadmap

Keep milestone order dependency-correct. New work belongs in the earliest
milestone whose exit gate it affects, and every new phase must end in explicit
integration tests.
