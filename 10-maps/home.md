---
title: "Agent WASM Research"
kind: map
created: "2026-08-07"
tags: []
aliases:
  - "Home"
---

# Agent WASM Research

This is the selective entry point to the archive. See the
[archive guide](../README.md) for its structure and authoring conventions.

## Implementation roadmap

- [Jido-Inspired Agentic System Roadmap](../.spec/planning/agentic-system/README.md)
  — nine production-oriented milestones covering contracts, agent semantics,
  host lifecycle, durability, security and plugins, multi-agent topology, AI,
  assurance, and platform operations.

## Active inquiries

- [How Should Agent WASM Assure a Jido-Like Extism Runtime?](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
  — defines the profiles, equivalence rules, state/effect invariants, fault
  boundaries, isolation matrix, replay records, and evidence needed before
  implementation claims are credible.
- [How Should Agent WASM Construct a Jido-Like Framework?](../40-inquiries/how-should-agent-wasm-construct-a-jido-like-framework.md)
  — tests a versioned reducer protocol, host-owned actor cell, durable outbox,
  state isolation, capability composition, topology reconciliation, and
  Extism-versus-WIT boundary.
- [How Should Agent WASM Use WebAssembly?](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
  — tests the core/component/WASI profile, runtime pair, capability model,
  resource controls, output boundary, and evidence contract for agent tools.
- [Should Agent WASM Adopt Extism?](../40-inquiries/should-agent-wasm-adopt-extism.md)
  — tests whether Extism's byte-buffer protocol and independent runtime
  implementations satisfy Agent WASM's portability, policy, and lifecycle
  requirements.

## Topic maps

- [Extism Plugin System](extism-plugin-system.md) — routes through Extism's
  ABI, kernel, manifest, capabilities, PDK/SDK tooling, Wasmtime, Wazero,
  JavaScript, native Java, and Chicory stacks.
- [Jido Agent Architecture](jido-agent-architecture.md) — routes through the
  language-independent agent model and its proposed reconstruction as portable
  Wasm decision modules inside a host-owned runtime.
- [WebAssembly Foundations and Ecosystem](webassembly-foundations-and-ecosystem.md)
  — routes through the current standards stack, representative implementations,
  foundational and corrective research, and Agent WASM implications.
- [WebAssembly Testing and Verification](webassembly-testing-and-verification.md)
  — routes through official suites, testing tools, fuzzing, differential
  methods, replay, reduction, Extism contracts, and host assurance.

## Recently developed

- [WebAssembly Testing, Verification, and Agent Runtime Assurance](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
  — separates standards, engine, plug-in, reducer, host-state, isolation, and
  operational evidence, then designs a non-normative assurance stack around the
  proposed Jido-like Extism host.
- [Jido Agent Architecture and a Wasm/Extism Construction](../20-notes/jido-agent-architecture-and-wasm-extism-construction.md)
  — separates decision, messaging, runtime, lifecycle, composition, and
  durability responsibilities, then defines the proposed host–guest boundary.
- [Extism Plugin-System Architecture and Runtimes](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
  — explains the end-to-end plug-in call, separates the portable kernel from
  host policy, and compares the four execution families in detail.
- [WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
  — synthesizes core semantics, standards maturity, runtime tradeoffs, eight
  security layers, and a reproducible evaluation program.
- [WebAssembly Core Specification 3.0](../30-sources/rossberg-2026-webassembly-core-specification-3-0.md)
  — anchors the language-independent instruction, validation, execution, and
  encoding model released in July 2026.
- [MCP-SandboxScan](../30-sources/tan-et-al-2026-mcp-sandboxscan.md) — provides
  direct recent evidence for Wasm/WASI containment and runtime analysis of
  untrusted agent tools.

## Unsettled threads

- Freeze the first Core/WASI/Extism/PDK profile and define semantic equivalence
  for cross-runtime `TurnResult` values before selecting an executable harness.
- Determine whether a host-owned, revisioned actor cell with disposable Extism
  reducers and a directive outbox survives cross-runtime, crash, isolation, and
  performance tests.
- Determine whether a pinned Extism subset behaves equivalently on the
  reference Wasmtime and Go/Wazero runtimes, including reset, state, limits,
  deadlines, cancellation, and error channels.
- Determine whether a pinned Component Model and WASI 0.3 developer-preview
  profile is stable enough for an initial Agent WASM contract.
- Select two independent runtimes and build the cold/warm, boundary,
  governance, isolation, and portability evaluation matrix.
- Define how capability decisions and output provenance bind artifact,
  principal, purpose, invocation, and downstream model context.
