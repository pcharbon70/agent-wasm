---
title: "WebAssembly System Interface 0.3"
kind: source
created: "2026-08-07"
authors:
  - "WebAssembly WASI Subgroup"
published: "2026-06-11"
citation_key: "webassembly2026wasi03"
container: "WebAssembly Community Group"
edition: "0.3.0"
isbn: null
doi: null
url: "https://github.com/WebAssembly/WASI/releases/tag/v0.3.0"
accessed: "2026-08-07"
tags:
  - component-model
  - wasi
  - webassembly
aliases:
  - "WASI Preview 3"
---

# WebAssembly System Interface 0.3

## Reference

WebAssembly WASI Subgroup. *WASI 0.3.0*, ratified 11 June 2026.
[Release record](https://github.com/WebAssembly/WASI/releases/tag/v0.3.0).

## Contribution

WASI defines portable host interfaces above core Wasm. Version 0.3 rebases its
I/O model on the Component Model's native async functions, futures, and streams.

## Findings

WASI 0.3 replaces the 0.2 `pollable`, start/finish, and imperative stream
patterns with composable async functions and typed `future<T>` and `stream<T>`
values. CLI, sockets, HTTP, filesystem, and clocks were revised around those
primitives. Network authority is expressed by world imports rather than a
single threaded `network` resource.

WASI is modular and interface-oriented, not a POSIX clone or an operating
system. Hosts select and implement packages; a component receives only the
imports with which it is instantiated.

## Relevance

The async component surface aligns with long-running agent tools, streaming
results, HTTP mediation, cancellation, and explicit host capability injection.

## Limits

WASI 0.3 is a developer preview coupled to the still-evolving Component Model.
It does not define agent identity, policy, cost accounting, audit semantics, or
safe handling of untrusted tool output.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
