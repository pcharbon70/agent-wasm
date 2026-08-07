---
title: "Extism Runtime C API"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismruntimeapi"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/runtime-apis/"
accessed: "2026-08-07"
tags:
  - extism
  - plugin-system
  - runtime
aliases: []
---

# Extism Runtime C API

## Reference

Dylibso. *Runtime APIs*. [Extism documentation](https://extism.org/docs/concepts/runtime-apis/),
accessed 7 August 2026.

## Contribution

The API is the stable FFI surface through which many language SDKs embed the
Rust reference runtime.

## Findings

The host creates a plug-in from raw Wasm, WAT, or a JSON manifest plus custom
functions and a WASI flag. It can test for exports, call functions, read output
and errors, merge configuration, reset or free the plug-in, and cancel an
active call from another thread.

Host-function callbacks receive an `ExtismCurrentPlugin` for memory allocation,
length checks, reads, writes, and optional per-call host context. Functions can
be assigned a namespace. Successful `extism_plugin_call` returns zero; the
output pointer remains tied to plug-in-managed memory and its lifetime.

## Relevance

This surface explains why Python, Ruby, .NET, Java, and other SDKs can share
one Wasmtime-backed implementation while presenting idiomatic APIs.

## Limits

An SDK binding to this C API is not an independent runtime implementation.
FFI packaging, native-library compatibility, object lifetimes, thread safety,
and error translation become additional correctness concerns.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
