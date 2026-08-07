---
title: "Extism Go SDK"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026gosdk"
container: "Extism Source Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/extism/go-sdk"
accessed: "2026-08-07"
tags:
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism Go SDK

## Reference

Extism Project. *Extism Go SDK*.
[Source repository](https://github.com/extism/go-sdk), accessed 7 August 2026.

## Contribution

The Go SDK is an independent, pure-Go implementation of the Extism host stack
over Wazero rather than a binding to `libextism`.

## Findings

It embeds the common `extism-runtime.wasm`, compiles the kernel and plug-in
modules with Wazero, creates `extism:host/env` and user host modules, optionally
instantiates WASI Preview 1, and implements configuration, variables, Extism
HTTP, allowed hosts, filesystem mounts, and call memory in Go.

Manifest page limits are passed to Wazero's runtime configuration. Call
timeouts and cancellation use Go contexts together with Wazero's
close-on-context-done behavior. Compilation caches and `CompiledPlugin` allow
compiled code to be shared while producing separate stateful instances for
concurrency.

Wazero normally uses its compiler where supported and can use its portable
interpreter through runtime configuration, without CGO or a native Extism
library.

## Relevance

This runtime is a strong independent implementation for testing whether Agent
WASM behavior depends accidentally on Wasmtime or FFI packaging.

## Limits

API similarity does not establish exact parity. Timeout failure modes, WASI
coverage, engine proposals, exit-code behavior, memory accounting, HTTP, and
module linking need differential tests against the reference runtime.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
