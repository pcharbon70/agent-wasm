---
title: "WebAssembly Proposals"
kind: source
created: "2026-08-07"
authors:
  - "WebAssembly Community Group"
published: null
citation_key: "webassembly2026proposals"
container: "WebAssembly Community Group"
edition: null
isbn: null
doi: null
url: "https://github.com/WebAssembly/proposals"
accessed: "2026-08-07"
tags:
  - specification
  - webassembly
aliases:
  - "Wasm proposal registry"
---

# WebAssembly Proposals

## Reference

WebAssembly Community Group. *WebAssembly Proposals*. [Official proposal registry](https://github.com/WebAssembly/proposals), accessed 7 August 2026.

## Contribution

The registry records active, finished, and inactive feature proposals and the
phase process through which ideas mature into standard features.

## Findings

The process separates feature proposal, proposed specification text,
implementation, standardization, and integration. In August 2026, threads were
in phase 4; stack switching and wide arithmetic were among phase-3 proposals;
the Component Model remained phase 1 despite substantial implementation and
WASI preview use. The registry links engine implementation status separately.

This prevents three common category errors: a repository does not imply a
stable standard, one runtime's support does not imply ecosystem portability,
and a developer preview does not imply frozen semantics.

## Relevance

Agent WASM must record the exact feature set it accepts rather than claim
generic “Wasm support.” Stack switching, threads, GC, component async, and
memory64 materially change runtime design and portability.

## Limits

Phase is process maturity, not a security or quality grade. The registry is
live and must be rechecked for time-sensitive decisions.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
