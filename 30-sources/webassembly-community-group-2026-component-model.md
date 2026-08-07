---
title: "WebAssembly Component Model"
kind: source
created: "2026-08-07"
authors:
  - "WebAssembly Community Group"
published: null
citation_key: "webassembly2026component"
container: "WebAssembly Community Group"
edition: "Developer Preview 0.3"
isbn: null
doi: null
url: "https://github.com/WebAssembly/component-model"
accessed: "2026-08-07"
tags:
  - component-model
  - specification
  - webassembly
aliases: []
---

# WebAssembly Component Model

## Reference

WebAssembly Community Group. *Component Model Design and Specification*.
[Specification repository](https://github.com/WebAssembly/component-model), accessed 7 August 2026.

## Contribution

The Component Model extends core modules with typed interfaces, composition,
nesting, resources, WIT descriptions, and a Canonical ABI for moving rich
values across language boundaries.

## Findings

A component is a distinct self-describing binary form that can contain core
modules and nested components. Components interact through typed interfaces
rather than shared linear memory. WIT defines worlds, interfaces, records,
variants, resources, and functions; the Canonical ABI lowers and lifts those
types to core Wasm conventions.

Developer Preview 0.2 established component linking and resource types.
Preview 0.3 adds native async functions, futures, streams, and concurrency ABI
operations. The project explicitly says its formal specification and reference
interpreter are future work.

## Relevance

This is the strongest existing candidate for language-neutral agent-tool
contracts and capability-shaped imports. It could make tools composable without
inventing a private ABI.

## Limits

The Component Model remains an active phase-1 proposal. Preview stability is a
tooling commitment for feedback, not final WebAssembly standardization. Rich
interfaces also do not define authorization, quotas, identity, or provenance.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
