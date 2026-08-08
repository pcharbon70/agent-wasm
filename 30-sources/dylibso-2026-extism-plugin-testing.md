---
title: "Testing Extism Plug-ins with XTP"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismtesting"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/testing/"
accessed: "2026-08-07"
tags:
  - extism
  - testing
  - webassembly
aliases:
  - "XTP Extism test runner"
---

# Testing Extism Plug-ins with XTP

## Reference

Dylibso. *Testing Extism Plug-ins*.
[Official documentation](https://extism.org/docs/concepts/testing/), accessed
7 August 2026.

## Contribution

The documentation presents `xtp plugin test`, a Wasm-hosted test runner for
calling an Extism plug-in inside a real runtime. Test harness libraries are
available for JavaScript/TypeScript, Rust, Go, and Zig, while the target plug-in
may use any supported PDK language.

## Method

A test module calls exports on the target and asserts output, persistent plug-in
state, and timing. The runner accepts inline or file-backed mock input. For
plug-ins that import host functions, `--mock-host` loads another Wasm module
whose exports satisfy those imports; the documented example composes a mock key-
value host, the target plug-in, and the test plug-in.

## Findings

The architecture tests the compiled artifact and Extism ABI instead of only
the guest's source-language functions. Wasm-based mock hosts also make an import
contract portable across test-harness languages.

XTP does not by itself reproduce an application's native host implementation,
database transaction, mailbox scheduler, authorization layer, crash timing, or
multi-tenant instance pool. Those require host integration and system tests.

## Relevance

XTP fits the contract tier for Agent WASM reducers: golden turn vectors,
malformed input, state behavior, imported capability protocols, and per-call
timing. It should sit below the host actor-cell and durability suite.

## Limits

Mock fidelity is the test author's responsibility. Timing assertions can be
environment-sensitive, and the documentation does not establish identical
behavior across all Extism SDK/runtime families.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Agent runtime assurance inquiry](../40-inquiries/how-should-agent-wasm-assure-a-jido-like-extism-runtime.md)
