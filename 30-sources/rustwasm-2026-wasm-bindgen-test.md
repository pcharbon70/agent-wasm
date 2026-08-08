---
title: "wasm-bindgen-test and wasm-pack test"
kind: source
created: "2026-08-07"
authors:
  - "Rust and WebAssembly Working Group"
published: null
citation_key: "rustwasm2026wasmbindgentest"
container: "Rust and WebAssembly Documentation"
edition: null
isbn: null
doi: null
url: "https://rustwasm.github.io/docs/wasm-bindgen/wasm-bindgen-test/usage.html"
accessed: "2026-08-07"
tags:
  - browser
  - rust
  - testing
  - webassembly
aliases: []
---

# wasm-bindgen-test and wasm-pack test

## Reference

Rust and WebAssembly Working Group. *wasm-bindgen-test Usage* and
[*wasm-pack test*](https://rustwasm.github.io/docs/wasm-pack/commands/test.html).
Official documentation, accessed 7 August 2026.

## Contribution

`wasm-bindgen-test` supplies Rust test attributes and a runner that executes
compiled Wasm in Node.js or a browser. `wasm-pack test` coordinates that runner
and supported browser drivers.

## Findings

The tools let guest-library tests cross the native-to-Wasm compilation boundary
and exercise JavaScript/Web integration in the target environment. Browser
tests can therefore observe bindings, DOM/Web API behavior, and engine-specific
integration that a native Rust test cannot.

## Relevance

This is an adjacent profile for browser-hosted Agent WASM tools. It is not the
primary harness for server-side Extism reducers, but it illustrates the need to
test the final compiled artifact in its actual embedding.

## Limits

The stack is Rust- and JavaScript/Web-oriented and does not exercise Extism's
kernel, ABI, manifest, or native Host SDK behavior.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
