---
title: "Wazero Runtime"
kind: source
created: "2026-08-07"
authors:
  - "Wazero Project"
published: null
citation_key: "wazeroproject2026runtime"
container: "Wazero Source Repository"
edition: "1.11.0"
isbn: null
doi: null
url: "https://github.com/wazero/wazero"
accessed: "2026-08-07"
tags:
  - runtime
  - wasi
  - webassembly
aliases: []
---

# Wazero Runtime

## Reference

Wazero Project. *Wazero*. Version 1.11.0.
[Source repository](https://github.com/wazero/wazero), accessed 7 August 2026.

## Contribution

Wazero is a core Wasm runtime written in Go and used as the engine beneath the
independent Extism Go SDK.

## Findings

Wazero has no CGO requirement and emphasizes Go cross-compilation. It offers a
compiler on supported architectures and a portable interpreter elsewhere or
when explicitly selected. Compiled modules can be cached and instantiated
multiple times. Its host API includes runtime and module configuration,
filesystem configuration, WASI Preview 1, host functions, memory limits, and
context-driven closure for cancellation.

## Relevance

Wazero makes the Go Extism stack operationally and implementation-wise
independent from `libextism` and Wasmtime, which is valuable for differential
conformance.

## Limits

Core-spec conformance does not imply Extism host-service or WASI parity.
Compiler availability is architecture-dependent, and cancellation by closing a
module has different lifecycle consequences from Wasmtime epoch interruption.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
