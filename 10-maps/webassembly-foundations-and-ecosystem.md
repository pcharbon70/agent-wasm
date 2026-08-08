---
title: "WebAssembly Foundations and Ecosystem"
kind: map
created: "2026-08-07"
tags:
  - runtime
  - webassembly
aliases:
  - "Wasm foundations"
---

# WebAssembly Foundations and Ecosystem

## Scope

This map routes through the WebAssembly standards stack, representative runtime
architectures, foundational and corrective research, and the open question of
how Agent WASM should use the ecosystem.

## Start here

- [WebAssembly Foundations, Ecosystem, and Agent Runtime Implications](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
  — integrated account of semantics, standards maturity, implementations,
  research findings, security layers, and a proposed evaluation program.
- [How Should Agent WASM Use WebAssembly?](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
  — converts the survey into falsifiable architecture and runtime questions.
- [WebAssembly Testing and Verification](webassembly-testing-and-verification.md)
  — continues from architecture into conformance, fuzzing, differential,
  replay, formal, Extism-contract, and host-state assurance.

## Trails

### Standards and evolution

- [Core Specification 3.0](../30-sources/rossberg-2026-webassembly-core-specification-3-0.md)
  — the language-neutral instruction, validation, execution, and encoding
  authority.
- [WebAssembly Proposals](../30-sources/webassembly-community-group-2026-proposals.md)
  — prevents implementation support and preview use from being confused with
  standardization.
- [Component Model](../30-sources/webassembly-community-group-2026-component-model.md)
  — WIT, rich interfaces, resources, composition, and the Canonical ABI.
- [WASI 0.3](../30-sources/webassembly-wasi-subgroup-2026-wasi-0-3.md)
  — portable host APIs rebased on native async components.

### Runtime implementation families

- [V8](../30-sources/v8-project-2026-webassembly-compilation-pipeline.md) and
  [SpiderMonkey](../30-sources/mozilla-2026-spidermonkey.md) — independent
  production browser engines and tiered compilation contexts.
- [Wasmtime](../30-sources/bytecode-alliance-2026-wasmtime.md) and
  [Wasmer](../30-sources/wasmer-2026-runtime.md) — server and embedding
  architectures with different compiler, allocation, and packaging choices.
- [Wazero](../30-sources/wazero-project-2026-runtime.md) — a pure-Go compiler
  and interpreter engine that supplies an independent Extism implementation.
- [WAMR](../30-sources/bytecode-alliance-2026-wamr.md) and
  [WasmEdge](../30-sources/wasmedge-2026-runtime.md) — embedded and edge
  constraints, modes, extensions, and deployment priorities.
- [Extism Plugin System](extism-plugin-system.md) — applies core Wasm through
  a portable byte-buffer plug-in ABI implemented over Wasmtime, Wazero,
  JavaScript engines, and Chicory.

### Language and specification foundations

- [Bringing the Web Up to Speed](../30-sources/haas-et-al-2017-bringing-web-up-to-speed.md)
  — founding goals and machine design.
- [Mechanising and Verifying WebAssembly](../30-sources/watt-2018-mechanising-and-verifying-webassembly.md)
  — Isabelle soundness and specification defect discovery.
- [SpecTec](../30-sources/youn-et-al-2024-spectec.md) — generated standards
  artifacts and proposal consistency.

### Performance and execution models

- [Not So Fast](../30-sources/jangda-et-al-2019-not-so-fast.md) — why
  near-native performance cannot be assumed from kernels.
- [Faasm](../30-sources/shillaker-pietzuch-2020-faasm.md) — snapshots,
  co-location, shared state, and OS controls for serverless Wasm.

### Security and assurance

- [Testing and Verification Synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
  — explains why engine conformance, plug-in correctness, and Jido-like host
  durability require distinct but connected evidence layers.
- [Binary Security of WebAssembly](../30-sources/lehmann-et-al-2020-binary-security-of-webassembly.md)
  — guest source vulnerabilities survive inside linear memory.
- [RLBox](../30-sources/narayan-et-al-2020-rlbox.md) — production
  compartmentalization and validation of untrusted outputs.
- [CT-Wasm](../30-sources/watt-et-al-2019-ct-wasm.md) — typed constant-time and
  information-flow guarantees beyond core Wasm.
- [Swivel](../30-sources/narayan-et-al-2021-swivel.md) — speculative-execution
  hardening.
- [Provably-Safe Sandboxing](../30-sources/bosamiya-et-al-2022-provably-safe-sandboxing.md)
  — verified and safe-language translation routes.
- [MCP-SandboxScan](../30-sources/tan-et-al-2026-mcp-sandboxscan.md) — direct
  evidence for sandboxed agent tools, canaries, egress, and output sinks.

## Open questions

- Which Component Model and WASI preview surface is stable enough to pin?
- Which runtime pair gives meaningful independent conformance evidence?
- What belongs in the Wasm capability layer versus the outer orchestrator?
- Which adversaries require process, VM, or hardware isolation beyond Wasm?
- How should provenance and taint move from a component result into model
  context and downstream tool calls?

These remain tracked in the
[Agent WASM inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md).
