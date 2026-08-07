---
title: "WebAssembly Micro Runtime"
kind: source
created: "2026-08-07"
authors:
  - "Bytecode Alliance"
published: null
citation_key: "bytecodealliance2026wamr"
container: "WAMR Project"
edition: null
isbn: null
doi: null
url: "https://github.com/bytecodealliance/wasm-micro-runtime"
accessed: "2026-08-07"
tags:
  - embedded-systems
  - runtime
  - webassembly
aliases:
  - "WAMR"
---

# WebAssembly Micro Runtime

## Reference

Bytecode Alliance. *WebAssembly Micro Runtime*.
[Official repository](https://github.com/bytecodealliance/wasm-micro-runtime), accessed 7 August 2026.

## Contribution

WAMR targets small-footprint deployments across microcontrollers, IoT, edge,
trusted execution environments, and cloud systems.

## Findings

The runtime supports classic and fast interpreters, ahead-of-time compilation,
Fast JIT, LLVM JIT, and dynamic tier-up. It offers built-in libc or WASI,
embedding APIs, native imports, threading, debugging, and execution-in-place
across a broad CPU and operating-system matrix.

Its architecture demonstrates that Wasm implementation choices are constrained
by code size, writable/executable memory, architecture support, startup, and
operational environment—not only peak throughput.

## Relevance

WAMR is an important counterpoint to server-class JIT engines if Agent WASM is
expected to run on edge devices or inside restricted hosts.

## Limits

Feature support varies by build mode and platform. Project footprint and
performance figures are configuration-specific and need reproduction on the
target hardware.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
