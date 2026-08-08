---
title: "WebAssembly Testing and Verification"
kind: map
created: "2026-08-07"
tags:
  - extism
  - fuzzing
  - testing
  - verification
  - webassembly
aliases:
  - "Wasm assurance map"
---

# WebAssembly Testing and Verification

## Scope

This map routes through WebAssembly conformance, compiler and runtime testing,
fuzzing, differential methods, replay and reduction, formal semantics, Extism
plug-in testing, and the assurance problem for a host-owned Jido-like runtime.

## Start here

- [WebAssembly Testing, Verification, and Agent Runtime Assurance](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
  — integrates the tool landscape and research evidence into a layered,
  non-normative assurance design.
- [How Should Agent WASM Assure a Jido-Like Extism Runtime?](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
  — tracks the unresolved profiles, equivalence relation, invariants, fault
  model, and evidence thresholds.

## Trails

### Standards and executable semantics

- [WebAssembly Core Test Suite](../30-sources/webassembly-community-group-2026-core-testsuite.md)
  — baseline `.wast` assertions for the abstract machine.
- [WASI Test Suite](../30-sources/webassembly-wasi-subgroup-2026-wasi-testsuite.md)
  — adapter-driven interface tests with explicit skips and expected failures.
- [Mechanising and Verifying WebAssembly](../30-sources/watt-2018-mechanising-and-verifying-webassembly.md)
  — formal semantics, soundness, verified execution, and differential fuzzing.
- [SpecTec](../30-sources/youn-et-al-2024-spectec.md) — shared semantic source
  for generated prose and interpreter artifacts.

### Construction, mutation, and diagnosis

- [WABT](../30-sources/webassembly-project-2026-wabt-testing-toolchain.md) —
  validation, interpretation, inspection, and spec-script lowering.
- [Binaryen testing](../30-sources/webassembly-project-2026-binaryen-testing.md)
  — optimizer regressions, randomized pass testing, and reduction.
- [wasm-tools](../30-sources/bytecode-alliance-2026-wasm-tools-testing-toolchain.md)
  — deterministic valid generation, mutation, and predicate-based shrinking.
- [Wasm-Mutate](../30-sources/cabrera-arteaga-et-al-2024-wasm-mutate.md) —
  peer-reviewed evidence for rapid semantics-preserving diversification.

### Runtime testing and observed defects

- [Wasmtime Testing and Fuzzing](../30-sources/bytecode-alliance-2026-wasmtime-testing-and-fuzzing.md)
  — layered regression suites, structured generators, continuous fuzzing, and
  differential-oracle discipline.
- [Security and Correctness in Wasmtime](../30-sources/fitzgerald-2022-security-and-correctness-in-wasmtime.md)
  — practitioner account of fuzzing, formal verification, and disposable
  instances.
- [Wasmtime Security Advisory Lessons](../30-sources/wasmtime-project-2026-security-advisory-lessons.md)
  — invalid-input, architecture-coverage, and model-drift gaps exposed in 2026.
- [Runtime Bug Study](../30-sources/zhang-et-al-2023-webassembly-runtime-bugs.md)
  and [Compiler Bug Study](../30-sources/romano-et-al-2021-webassembly-compiler-bugs.md)
  — empirical taxonomies for directed testing at distinct pipeline layers.
- [Waltzz](../30-sources/zhang-et-al-2025-waltzz.md),
  [LWDIFF](../30-sources/zhou-et-al-2025-lwdiff.md), and
  [WASCII](../30-sources/fu-et-al-2026-wascii.md) — stack-aware and
  specification-assisted generation with confirmed cross-runtime findings.

### Realistic workloads, replay, and performance

- [Wasm-R3](../30-sources/baek-et-al-2024-wasm-r3.md) — captures host-dependent
  applications as reduced standalone cross-engine replays.
- [RR-Reduce](../30-sources/baek-et-al-2025-rr-reduce.md) — execution-aware
  minimization of bug-triggering modules.
- [WarpDiff](../30-sources/jiang-et-al-2023-warpdiff.md) — differential timing
  ratios as performance-outlier evidence.

### Embedding-specific tests

- [Testing Extism Plug-ins with XTP](../30-sources/dylibso-2026-extism-plugin-testing.md)
  — compiled plug-in calls, assertions, persistent state, input fixtures, and
  Wasm mock hosts.
- [wasm-bindgen-test](../30-sources/rustwasm-2026-wasm-bindgen-test.md) and
  [Web Platform Tests](../30-sources/web-platform-tests-2026-webassembly-suite.md)
  — separate browser/JavaScript integration profile.
- [Extism Plugin System](extism-plugin-system.md) — architecture whose ABI,
  kernel, manifest, capability, and engine boundaries define the middle tier.
- [Jido Agent Architecture](jido-agent-architecture.md) — host state machine,
  reducer/effect boundary, durability, and topology claims requiring the upper
  tiers.

## Open questions

- What exact Core/WASI/Extism/PDK profile is the first support target?
- What makes two `TurnResult` values semantically equivalent across runtimes?
- Which host invariants should be properties, fault-injection oracles, or
  formally modeled statements?
- Can fresh-instance equivalence establish a safe reset/pooling profile?
- How should realistic turn traces be redacted, replayed, and minimized?
- Which architectures receive continuous evidence rather than nominal support?

The active workbench is the
[Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md).
