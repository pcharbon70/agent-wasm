---
title: "WebAssembly Core Specification 3.0"
kind: source
created: "2026-08-07"
authors:
  - "Andreas Rossberg"
published: "2026-07-28"
citation_key: "rossberg2026wasm3"
container: "W3C WebAssembly Community Group"
edition: "3.0"
isbn: null
doi: null
url: "https://webassembly.github.io/spec/core/"
accessed: "2026-08-07"
tags:
  - specification
  - webassembly
aliases:
  - "Wasm Core 3.0"
---

# WebAssembly Core Specification 3.0

## Reference

Andreas Rossberg, editor. *WebAssembly Core Specification*, release 3.0,
WebAssembly Community Group, 28 July 2026. [Living specification](https://webassembly.github.io/spec/core/).

## Contribution

The core specification is the authoritative definition of the language-neutral
Wasm instruction set, module structure, validation, instantiation, execution,
binary encoding, and text format. It deliberately excludes environmental I/O
and invocation policy.

## Findings

Wasm is a typed stack machine with structured control flow. Modules declare
imports and exports, functions, tables, memories, globals, tags, and data. A
module must validate before instantiation; execution can terminate normally or
trap. Release 3.0 integrates the post-2.0 type and execution surface while
retaining a layered embedding model.

The security boundary is narrow but important: core Wasm gives a module no
ambient host access. All environmental authority arrives through imported host
functions or shared objects chosen by the embedder. Linear-memory safety
protects the runtime and other instances; it does not make unsafe source code
inside one linear memory memory-safe.

## Relevance

Any Agent WASM runtime must treat this document as the semantic floor, then
define host capabilities, scheduling, resource limits, persistence, and tool
interfaces above it.

## Limits

The core spec does not define WASI, the Component Model, browser APIs,
capability policy, metering, deployment, or an agent protocol. Its release page
and W3C publication track also evolve independently.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
