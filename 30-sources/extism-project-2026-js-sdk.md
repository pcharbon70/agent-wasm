---
title: "Extism JavaScript SDK"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026jssdk"
container: "Extism Source Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/extism/js-sdk"
accessed: "2026-08-07"
tags:
  - browser
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism JavaScript SDK

## Reference

Extism Project. *Extism JS SDK*.
[Source repository](https://github.com/extism/js-sdk), accessed 7 August 2026.

## Contribution

The JavaScript SDK implements Extism directly over the WebAssembly facilities
already present in browsers, Node.js, Deno, Bun, and Cloudflare Workers; it
does not load `libextism` through FFI.

## Findings

The SDK compiles manifest modules with the JavaScript `WebAssembly` API and
instantiates the shared kernel plus plug-in modules. Environment adapters
supply fetching, workers, WASI, logging, and other host facilities.

This portability has visible seams. WASI support depends on the JavaScript
environment; the repository identifies Deno as unsupported and Bun as partial.
Timeouts require worker execution. Extism HTTP with an allowlist generally
requires a worker unless the environment supplies WebAssembly JS Promise
Integration. Browser background execution requires `SharedArrayBuffer`,
atomics, and a cross-origin-isolated context. Read-only directory mappings are
not supported by the current option path.

Variables are per instance and survive calls. The README says they persist
until `plugin.reset()`, but current `CallContext` source resets call blocks and
the host context without clearing its variable map. This documentation/source
discrepancy requires a behavioral test. Host functions are grouped by import
namespace and receive a current-call context for shared-memory access.

## Relevance

This is the relevant Extism implementation for browser and edge-JavaScript
agents, and the clearest demonstration that “Extism runtime” does not always
mean Wasmtime.

## Limits

Engine features, worker availability, WASI, filesystem access, interruption,
and HTTP behavior inherit each JavaScript host's constraints. The README still
warns of possible breaking changes before a 1.0 release.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
