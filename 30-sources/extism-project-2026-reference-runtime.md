---
title: "Extism Reference Runtime"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026referenceruntime"
container: "Extism Source Repository"
edition: "1.21.0"
isbn: null
doi: null
url: "https://github.com/extism/extism"
accessed: "2026-08-07"
tags:
  - extism
  - runtime
  - webassembly
aliases:
  - "libextism"
---

# Extism Reference Runtime

## Reference

Extism Project. *Extism*. Version 1.21.0.
[Source repository](https://github.com/extism/extism), accessed 7 August 2026.

## Contribution

The repository contains the Rust Host SDK and reference runtime, C API and
shared library, manifest types, conversion helpers, and the internal Wasm
kernel.

## Findings

Release 1.21.0 embeds Wasmtime 41 with Cranelift, caching, pooling,
coredump, WAT, and related features. It instantiates `extism-runtime.wasm` as
`extism:host/env`, links user modules and optional WASI Preview 1 imports,
registers custom functions, and validates that callable exports have no
parameters and at most one `i32` result.

Each call resets kernel call memory, copies and marks input, invokes the guest,
collects output/error, and maps traps or return codes. Manifest timeouts and
cancellation use Wasmtime epoch interruption. Optional fuel is also supported.
Memory limits, Extism HTTP and variables, path preopens, module hashing,
compiled plug-ins, and instance pools are implemented around the engine.

The `libextism` C ABI packages this stack for FFI-based language SDKs. Official
build features distinguish loading Wasm over HTTP or from the filesystem from
giving a running plug-in the Extism HTTP host function.

## Relevance

This is the most complete implementation and the semantic reference against
which independent Extism runtimes are normally compared.

## Limits

Behavior tied to Wasmtime, native-library distribution, supported host
targets, and Rust implementation choices is not automatically portable to the
Go, JavaScript, or Chicory stacks. The project does not by itself establish
independent conformance or security assurance for every SDK.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
