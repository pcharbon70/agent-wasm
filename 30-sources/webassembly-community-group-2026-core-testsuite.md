---
title: "WebAssembly Core Test Suite"
kind: source
created: "2026-08-07"
authors:
  - "WebAssembly Community Group"
published: null
citation_key: "webassemblycommunitygroup2026coretestsuite"
container: "WebAssembly Specification Repository"
edition: null
isbn: null
doi: null
url: "https://github.com/WebAssembly/spec/tree/main/test/core"
accessed: "2026-08-07"
tags:
  - conformance
  - testing
  - webassembly
aliases:
  - "Wasm spec tests"
---

# WebAssembly Core Test Suite

## Reference

WebAssembly Community Group. *WebAssembly Core Test Suite*.
[Official repository](https://github.com/WebAssembly/spec/tree/main/test/core),
accessed 7 August 2026.

## Contribution

The suite supplies executable examples and assertions for Core WebAssembly
semantics. Tests use the specification interpreter's S-expression script
format and cover successful execution, validation failures, malformed modules,
linking behavior, and traps.

## Method

The repository's runner executes `.wast` scripts against the reference
interpreter or another tool with compatible options. It can additionally run
the same scripts through a stand-alone JavaScript interpreter. The
`WebAssembly/testsuite` repository mirrors the core tests for consumers that do
not need the complete specification repository.

## Findings

The suite is the baseline for claims that an engine implements a particular
Core Wasm feature profile. Its script assertions make positive and negative
semantic cases portable, while independent engines can consume the same
vectors.

Passing the suite does not test WASI, Extism's calling convention, host
capability policy, resource limits, crash recovery, application protocols, or
tenant isolation.

## Relevance

Agent WASM should pin a Core feature profile and retain the upstream suite
revision used to test every supported engine. Application assurance must be a
separate layer above this conformance baseline.

## Limits

The suite is finite and example-based. It cannot establish implementation
correctness for every byte sequence, optimizer path, architecture, or embedding
configuration.

## Derived work

- [WebAssembly Testing, Verification, and Agent Runtime Assurance](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Testing and verification map](../10-maps/webassembly-testing-and-verification.md)
- [Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
