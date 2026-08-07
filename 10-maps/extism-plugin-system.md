---
title: "Extism Plugin System"
kind: map
created: "2026-08-07"
tags:
  - extism
  - plugin-system
  - runtime
  - webassembly
aliases:
  - "Extism architecture"
---

# Extism Plugin System

## Scope

This map routes through Extism's plug-in contract, kernel and memory model,
manifest and capability controls, guest/host tooling, runtime implementations,
and the open decision about its role in Agent WASM.

## Start here

- [Extism Plugin-System Architecture and Runtimes](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
  — integrated explanation of the complete stack, call lifecycle, state,
  policy model, engine families, and Agent WASM implications.
- [Should Agent WASM Adopt Extism?](../40-inquiries/should-agent-wasm-adopt-extism.md)
  — converts the survey into a pinned profile, differential tests, benchmarks,
  threat-model work, and falsifiable adoption criteria.

## Trails

### Roles and guest tooling

- [Plug-in System Concepts](../30-sources/dylibso-2026-extism-plugin-system.md)
  — host, plug-in, Host SDK, PDK, exports, imports, and the application-owned
  extension point.
- [Plug-in Language and PDK Guide](../30-sources/dylibso-2026-extism-plugin-quickstart.md)
  — supported guest languages, compilation targets, WASI requirements, and
  how toolchains expose the common ABI.

### ABI and portable kernel

- [Plugin Calling Convention](../30-sources/extism-project-2026-plugin-calling-convention.md)
  — no-argument exports and offset/length message passing.
- [Host Function Namespaces](../30-sources/extism-project-2026-host-function-namespaces.md)
  — separates built-in `extism:host/env` from application
  `extism:host/user` imports.
- [Runtime Kernel](../30-sources/extism-project-2026-runtime-kernel.md) and
  [Memory](../30-sources/dylibso-2026-extism-memory.md) — the shared internal
  Wasm allocator, call metadata, copy path, and lifetimes.

### Policy and embedding surface

- [Manifest and Runtime Constraints](../30-sources/dylibso-2026-extism-manifest.md)
  — module resolution, hashes, configuration, paths, hosts, timeout, and
  selected memory limits.
- [Host Functions](../30-sources/dylibso-2026-extism-host-functions.md) — the
  application capability boundary and its memory, lifetime, and concurrency
  obligations.
- [Runtime C API](../30-sources/dylibso-2026-extism-runtime-apis.md) — creation,
  calls, output/errors, reset, cancellation, host callbacks, and the basis for
  FFI-backed SDKs.

### Runtime families

- [Reference Runtime](../30-sources/extism-project-2026-reference-runtime.md)
  — Rust, Wasmtime, `libextism`, fuel, epochs, WASI, pools, and the fullest
  implementation.
- [Go SDK](../30-sources/extism-project-2026-go-sdk.md) — independent pure-Go
  implementation over the [Wazero runtime](../30-sources/wazero-project-2026-runtime.md).
- [JavaScript SDK](../30-sources/extism-project-2026-js-sdk.md) — browsers,
  Node, Deno, Bun, workers, and their environment-specific Wasm/WASI behavior.
- [Java SDK](../30-sources/extism-project-2026-java-sdk.md) and
  [Chicory SDK](../30-sources/extism-project-2026-chicory-sdk.md) — native
  `libextism`/Wasmtime versus experimental pure-Java execution.

### Standards context

- [WebAssembly Foundations and Ecosystem](webassembly-foundations-and-ecosystem.md)
  — locates Extism's core-module bytes ABI beside WASI, WIT, the Component
  Model, runtime security, and implementation research.

## Open questions

- Which exact Extism subset can be made behaviorally portable across Wasmtime,
  Wazero, and JavaScript engines?
- What are the true reset and state-erasure semantics in each implementation?
- Are manifest limits measured over equivalent resources and failure modes?
- Can Agent WASM's typed, async, streaming, provenance, and authorization needs
  remain a thin layer, or do they favor WIT directly?
- Which JavaScript and Chicory limitations are temporary implementation gaps
  versus architectural differences?

These remain tracked in the
[Extism adoption inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md).
