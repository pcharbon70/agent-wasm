---
title: "Sources"
kind: map
created: "2026-08-07"
tags:
  - archive-navigation
  - directory-index
aliases:
  - "Sources index"
---

# Sources (`30-sources`)

## Purpose

Source notes preserve bibliographic provenance and evidence-focused analysis.

## What belongs here

Create one note for each primary or substantively used secondary work. Record
what the source supports, how it reached its conclusions, and its limits.

## Index

### Subdirectories

- None yet.

### Documents

- [Jido 2.3.2 Source Architecture](agentjido-2026-jido-2-3-2-source-architecture.md)
  — confirms the framework decomposition in tagged source behaviors,
  protocols, normalized plugin specifications, and storage APIs.
- [Jido Actions and Execution](agentjido-2026-jido-actions.md) — distinguishes
  action definition, instruction normalization, execution policy, plans,
  schemas, state updates, and runtime-owned effects.
- [Jido AI Runtime](agentjido-2026-jido-ai-runtime.md) — locates model routing,
  reasoning strategies, tools, retrieval, quota, and providers above the core
  agent model.
- [Jido Directives and State Operations](agentjido-2026-jido-directives-and-state-operations.md)
  — separates internal state transitions from typed external effect requests
  and records directive-executor semantics.
- [Jido Multi-Tenancy and Worker Pools](agentjido-2026-jido-multi-tenancy-and-worker-pools.md)
  — distinguishes hard instance isolation from logical partitioning and
  documents mutable-state reuse hazards.
- [Jido Overview and Core Loop](agentjido-2026-jido-overview-and-core-loop.md)
  — defines the immutable agent, live runtime, reducer/effect boundary, and
  canonical signal-to-directive flow.
- [Jido Persistence and Storage](agentjido-2026-jido-persistence-and-storage.md)
  — documents append-only Threads, checkpoint projections, revision pointers,
  storage adapters, hibernate, and thaw.
- [Jido Plugins and Strategies](agentjido-2026-jido-plugins-and-strategies.md)
  — treats plugins as capability bundles and strategies as replaceable state-
  transition policies.
- [Jido Runtime and Coordination](agentjido-2026-jido-runtime-and-coordination.md)
  — covers serialized turns, preparation, route execution, directives,
  logical hierarchy, completion, cancellation, and fan-out/fan-in.
- [Jido Runtime Patterns and Pods](agentjido-2026-jido-runtime-patterns-and-pods.md)
  — separates lifecycle from tenancy and explains durable topology plus live
  reconciliation.
- [Jido Sensors and Scheduling](agentjido-2026-jido-sensors-and-scheduling.md)
  — explains host-owned external event sources, timers, cron durability, and
  their signal ingress path.
- [Jido Signals and Routing](agentjido-2026-jido-signals-and-routing.md) —
  records the CloudEvents-derived envelope, causal metadata, route precedence,
  dispatch adapters, and persistent subscription features.
- [Elixir Processes, Mailboxes, and Supervision](elixir-project-2026-processes-and-supervision.md)
  — documents lightweight isolated processes, non-blocking mailbox sends,
  links, monitors, supervision, process bottlenecks, and the gap between a raw
  mailbox and Agent WASM's explicit admission bounds.
- [Erlang NIFs, Dirty Schedulers, and Ports](erlang-project-2026-nifs-dirty-schedulers-and-ports.md)
  — establishes VM-wide NIF failure scope, lengthy-work scheduling rules,
  cooperative cancellation constraints, and external Port isolation.
- [Go Concurrency, Context, and C Interoperation](go-project-2026-concurrency-context-and-cgo.md)
  — covers goroutines, channels, bounded workers, cooperative cancellation,
  the cgo boundary, and built-in fuzzing.
- [Rust Ownership and Concurrency](rust-project-2026-ownership-and-concurrency.md)
  — records ownership, `Send`/`Sync`, safe concurrency, the unsafe boundary,
  and the actor semantics that remain application responsibilities.
- [Rustler Safe Rust NIF Bridge](rustler-project-2026-safe-rust-nifs.md) —
  covers typed NIF wrappers, panic catching, dirty scheduling, native resources,
  asynchronous thread replies, and the limits of safe-wrapper claims.
- [Rustler Precompiled NIF Distribution](rustler-project-2026-precompiled-nif-distribution.md)
  — documents checksummed native artifacts, target/NIF matrices, source-build
  fallback, and remaining release and provenance obligations.
- [Tokio Task Runtime and Blocking Work](tokio-project-2026-task-runtime.md) —
  distinguishes async tasks from bounded blocking or CPU work and records why
  task abort alone does not stop a running engine invocation.
- [Wasm-R3](baek-et-al-2024-wasm-r3.md) — record-reduce-replay construction of
  realistic standalone cross-engine Wasm benchmarks.
- [RR-Reduce](baek-et-al-2025-rr-reduce.md) — execution-aware minimization of
  bug-triggering Wasm programs through record and replay.
- [Provably-Safe Multilingual Software Sandboxing Using WebAssembly](bosamiya-et-al-2022-provably-safe-sandboxing.md)
  — compares a verified Wasm compiler with translation to safe Rust.
- [WebAssembly Micro Runtime](bytecode-alliance-2026-wamr.md) — documents the
  interpreter, AOT, JIT, footprint, and platform design space for embedded and
  edge deployments.
- [wasm-tools Generation, Mutation, and Reduction](bytecode-alliance-2026-wasm-tools-testing-toolchain.md)
  — deterministic valid-module generation, semantics-aware mutation, and
  predicate-based test-case shrinking.
- [Wasmtime Architecture and Security](bytecode-alliance-2026-wasmtime.md) —
  covers Cranelift compilation, allocation, components, WASI, fuel, epochs, and
  host-boundary responsibilities.
- [Wasmtime Testing and Fuzzing](bytecode-alliance-2026-wasmtime-testing-and-fuzzing.md)
  — upstream conformance, regressions, structured generators, differential
  oracles, continuous fuzzing, and reduction.
- [Wasm-Mutate](cabrera-arteaga-et-al-2024-wasm-mutate.md) — evaluates fast,
  semantics-preserving Wasm binary diversification for security and testing.
- [Extism Host Functions](dylibso-2026-extism-host-functions.md) — defines
  custom application capabilities, core-Wasm signatures, shared-memory
  handles, user-data lifetimes, and concurrency obligations.
- [Extism Manifest and Runtime Constraints](dylibso-2026-extism-manifest.md) —
  records module sources and hashes, configuration, path and host controls,
  timeout, and selected memory limits.
- [Extism Memory and Message Passing](dylibso-2026-extism-memory.md) — explains
  the kernel-backed bytes-in/bytes-out copy path and call-memory lifetime.
- [Extism Plug-in Language and PDK Guide](dylibso-2026-extism-plugin-quickstart.md)
  — catalogs guest toolchains, export lowering, compilation targets, and WASI
  requirements.
- [Testing Extism Plug-ins with XTP](dylibso-2026-extism-plugin-testing.md) —
  exercises compiled artifacts, plug-in state, timing, fixture input, and Wasm
  mock hosts.
- [Extism Plug-in System Concepts](dylibso-2026-extism-plugin-system.md) —
  defines host, plug-in, Host SDK, PDK, import, export, and extension-point
  roles.
- [Extism Runtime C API](dylibso-2026-extism-runtime-apis.md) — documents the
  FFI surface used by many language SDKs for creation, calls, memory, errors,
  host callbacks, reset, and cancellation.
- [Extism Chicory SDK](extism-project-2026-chicory-sdk.md) — experimental
  pure-Java implementation over the JVM-native Chicory engine.
- [Extism Elixir Host SDK](extism-project-2026-elixir-sdk.md) — source and API
  audit of the official Rustler-based Elixir binding, its pinned versions,
  string boundary, missing public capabilities, and normal-scheduler calls.
- [Extism Go SDK](extism-project-2026-go-sdk.md) — independent pure-Go Extism
  implementation over Wazero with contexts, WASI, caches, and instances.
- [Extism Host Function Namespaces](extism-project-2026-host-function-namespaces.md)
  — assigns built-ins and user capabilities to explicit Wasm import modules.
- [Extism Java SDK](extism-project-2026-java-sdk.md) — established Java API over
  native `libextism` and the Wasmtime reference runtime.
- [Extism JavaScript SDK](extism-project-2026-js-sdk.md) — direct implementation
  over browser and server JavaScript WebAssembly engines with environment-
  dependent workers and WASI.
- [Extism Plugin Calling Convention](extism-project-2026-plugin-calling-convention.md)
  — defines no-argument exports and offset/length byte-buffer exchange.
- [Extism Reference Runtime](extism-project-2026-reference-runtime.md) — Rust,
  Wasmtime, `libextism`, the embedded kernel, host services, limits, fuel,
  epochs, and pools.
- [Extism Runtime Kernel](extism-project-2026-runtime-kernel.md) — moves the
  shared allocator and input/output/error bookkeeping into an internal Wasm
  module for cross-engine portability.
- [Security and Correctness in Wasmtime](fitzgerald-2022-security-and-correctness-in-wasmtime.md)
  — practitioner account of continuous structured fuzzing, differential
  oracles, verification, and disposable instances.
- [WASCII](fu-et-al-2026-wascii.md) — accepted ISSTA 2026 work on LLM-assisted
  specification-to-implementation checks validated by execution and runtime
  differentials.
- [Bringing the Web Up to Speed with WebAssembly](haas-et-al-2017-bringing-web-up-to-speed.md)
  — founding design, formal semantics, representation, and early implementation
  evidence.
- [Not So Fast](jangda-et-al-2019-not-so-fast.md) — large-application evidence
  against treating near-native performance as a universal constant.
- [WarpDiff](jiang-et-al-2023-warpdiff.md) — applies differential timing ratios
  to discover server-side Wasm runtime performance issues.
- [Binary Security of WebAssembly](lehmann-et-al-2020-binary-security-of-webassembly.md)
  — distinguishes host containment from exploitability inside a guest's linear
  memory.
- [SpiderMonkey WebAssembly Implementation](mozilla-2026-spidermonkey.md) —
  independent production browser-engine architecture and Firefox context.
- [RLBox](narayan-et-al-2020-rlbox.md) — production fine-grained library
  isolation and typed validation of untrusted sandbox outputs.
- [Swivel](narayan-et-al-2021-swivel.md) — software and hardware-assisted
  hardening of Wasm isolation against speculative execution.
- [WebAssembly Core Specification 3.0](rossberg-2026-webassembly-core-specification-3-0.md)
  — authoritative core language, validation, execution, and encoding rules.
- [An Empirical Study of Bugs in WebAssembly Compilers](romano-et-al-2021-webassembly-compiler-bugs.md)
  — characterizes defects across AssemblyScript, Binaryen, Emscripten, and
  wasm-bindgen.
- [wasm-bindgen-test and wasm-pack test](rustwasm-2026-wasm-bindgen-test.md) —
  runs compiled Rust/Wasm tests through Node.js and browser embeddings.
- [Faasm](shillaker-pietzuch-2020-faasm.md) — Wasm software fault isolation,
  snapshots, sharing, and OS controls for stateful serverless workloads.
- [MCP-SandboxScan](tan-et-al-2026-mcp-sandboxscan.md) — Wasm/WASI containment,
  canary evidence, egress observation, and source-to-sink analysis for agent
  tools.
- [V8 WebAssembly Compilation Pipeline](v8-project-2026-webassembly-compilation-pipeline.md)
  — Liftoff/TurboFan tiering, caching, startup, and debugging tradeoffs.
- [Wasmtime Security Advisories and Assurance Lessons](wasmtime-project-2026-security-advisory-lessons.md)
  — identifies invalid-input fuzzing, aarch64 coverage, and formal-model drift
  gaps exposed by the April 2026 advisory release.
- [Wasmer Runtime](wasmer-2026-runtime.md) — multiple compiler and integration
  backends for portable embedding and packaging.
- [Wazero Runtime](wazero-project-2026-runtime.md) — pure-Go compiler and
  interpreter engine, caching, WASI Preview 1, memory configuration, and
  context-driven cancellation beneath the Extism Go SDK.
- [WasmEdge Runtime](wasmedge-2026-runtime.md) — cloud-native, edge, plug-in,
  and application integration perspective.
- [Web Platform Tests for WebAssembly](web-platform-tests-2026-webassembly-suite.md)
  — shared browser-facing WebAssembly API tests and cross-browser results.
- [WebAssembly Core Test Suite](webassembly-community-group-2026-core-testsuite.md)
  — executable `.wast` assertions for core semantics, validation, malformed
  modules, linking, and traps.
- [WebAssembly Component Model](webassembly-community-group-2026-component-model.md)
  — WIT, rich interfaces, resources, composition, async, and Canonical ABI.
- [WebAssembly Proposals](webassembly-community-group-2026-proposals.md) —
  authoritative maturity and evolution registry for core features.
- [Binaryen Testing, Fuzzing, and Reduction](webassembly-project-2026-binaryen-testing.md)
  — optimizer regressions, randomized modules and passes, and failure
  minimization.
- [WABT Testing Toolchain](webassembly-project-2026-wabt-testing-toolchain.md) —
  validation, interpretation, inspection, and conversion of spec scripts to
  portable fixtures.
- [WebAssembly System Interface 0.3](webassembly-wasi-subgroup-2026-wasi-0-3.md)
  — ratified developer preview using component-native futures, streams, and
  async host interfaces.
- [WASI Test Suite](webassembly-wasi-subgroup-2026-wasi-testsuite.md) —
  runtime-adapter testing for selected previews with explicit skips and known
  failures.
- [CT-Wasm](watt-et-al-2019-ct-wasm.md) — mechanized type-driven information-
  flow and constant-time cryptography extension.
- [Mechanising and Verifying the WebAssembly Specification](watt-2018-mechanising-and-verifying-webassembly.md)
  — Isabelle semantics, verified interpreter and checker, soundness, and
  differential fuzzing.
- [SpecTec](youn-et-al-2024-spectec.md) — generated standards prose and
  interpreter from a shared semantic DSL.
- [Characterizing and Detecting WebAssembly Runtime Bugs](zhang-et-al-2023-webassembly-runtime-bugs.md)
  — derives a runtime-defect taxonomy and detection framework from real bugs.
- [Waltzz](zhang-et-al-2025-waltzz.md) — stack-invariant greybox transformations
  and instruction-aware generation that found confirmed runtime vulnerabilities.
- [LWDIFF](zhou-et-al-2025-lwdiff.md) — LLM-assisted specification-aware
  mutations adjudicated through deterministic cross-runtime execution.

## Maintaining this index

Index every direct source note. Keep citation keys, DOIs, and canonical URLs
unique, and connect sources to the work derived from them.
