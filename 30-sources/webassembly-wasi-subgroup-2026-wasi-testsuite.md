---
title: "WASI Test Suite"
kind: source
created: "2026-08-07"
authors:
  - "WebAssembly WASI Subgroup"
published: null
citation_key: "webassemblywasi2026testsuite"
container: "WebAssembly WASI Test Suite Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/WebAssembly/wasi-testsuite"
accessed: "2026-08-07"
tags:
  - conformance
  - testing
  - wasi
  - webassembly
aliases: []
---

# WASI Test Suite

## Reference

WebAssembly WASI Subgroup. *WASI Test Suite*.
[Official repository](https://github.com/WebAssembly/wasi-testsuite), accessed
7 August 2026.

## Contribution

The project provides WASI tests and a runtime-neutral executor. At access time
the repository described coverage for Preview 1 and forthcoming Preview 3,
while explicitly excluding other experimental APIs from its bundled suites.

## Method

Runtime adapters invoke engine binaries in subprocesses. A runner discovers
available adapters or selects one explicitly, and optional TOML expectation
files distinguish skipped tests from known expected failures. Buck2 builds
multi-language fixtures with pinned toolchains; CI exercises supported
operating systems and publishes recurring results.

## Findings

The adapter and expectation design makes incomplete feature support visible
without pretending that skipped or expected-failing tests passed. The executor
can also run external proposal suites, such as WASI threads, without folding
their maturity into the bundled baseline.

## Relevance

If Agent WASM grants WASI capabilities, it needs this interface-level layer in
addition to Core conformance. Extism-only reducers with no WASI imports can
omit it from their guest profile, which is itself an auditable design choice.

## Limits

The suite follows selected previews and is not a general WASI security-policy
test. A conforming filesystem or socket implementation may still be granted
too broadly by the host.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Testing and verification map](../10-maps/webassembly-testing-and-verification.md)
