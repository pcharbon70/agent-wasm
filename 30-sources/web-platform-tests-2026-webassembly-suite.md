---
title: "Web Platform Tests for WebAssembly"
kind: source
created: "2026-08-07"
authors:
  - "Web Platform Tests Project"
published: null
citation_key: "wpt2026webassembly"
container: "Web Platform Tests"
edition: null
isbn: null
doi: null
url: "https://github.com/web-platform-tests/wpt/tree/master/wasm"
accessed: "2026-08-07"
tags:
  - browser
  - conformance
  - testing
  - webassembly
aliases:
  - "WPT WebAssembly tests"
---

# Web Platform Tests for WebAssembly

## Reference

Web Platform Tests Project. *WebAssembly Tests*.
[Official repository](https://github.com/web-platform-tests/wpt/tree/master/wasm)
and [results dashboard](https://results.web-platform-tests.org/), accessed
7 August 2026.

## Contribution

The WPT WebAssembly directory tests browser-facing WebAssembly APIs and their
integration with the Web platform. The shared WPT infrastructure publishes
cross-browser results for major browser engines.

## Findings

WPT complements the Core semantic suite: it targets observable Web API behavior
such as JavaScript integration rather than only the abstract machine. Shared
tests and public cross-browser results turn implementation disagreement into
visible interoperability evidence.

## Relevance

Agent WASM needs this layer only for a browser host profile. It should not be
mixed into the native Extism conformance gate, where the embedding APIs and
capability model differ.

## Limits

WPT is not an Extism, WASI, server-runtime, or agent-protocol suite. Browser
results also do not establish behavior on native Wasmtime or Wazero embeddings.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
