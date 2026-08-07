---
title: "Provably-Safe Multilingual Software Sandboxing Using WebAssembly"
kind: source
created: "2026-08-07"
authors:
  - "Jay Bosamiya"
  - "Wen Shih Lim"
  - "Bryan Parno"
published: 2022
citation_key: "bosamiya2022sandboxing"
container: "31st USENIX Security Symposium"
edition: null
isbn: null
doi: null
url: "https://www.usenix.org/conference/usenixsecurity22/presentation/bosamiya"
accessed: "2026-08-07"
tags:
  - formal-methods
  - runtime
  - security
  - webassembly
aliases:
  - "vWasm and rWasm"
---

# Provably-Safe Multilingual Software Sandboxing Using WebAssembly

## Reference

Jay Bosamiya, Wen Shih Lim, and Bryan Parno. “Provably-Safe Multilingual
Software Sandboxing Using WebAssembly.” *USENIX Security 2022*.
[Open-access paper](https://www.usenix.org/conference/usenixsecurity22/presentation/bosamiya).

## Contribution

The work explores two paths to provable Wasm-to-native sandbox safety: vWasm,
a verified compiler in F*, and rWasm, a translator to safe Rust.

## Method

vWasm proves its sandboxing pass against a machine model. rWasm relies on safe
Rust's memory-safety boundary and forbids `unsafe`. The authors compare proof
effort, trusted components, portability, and PolyBench-C performance with
interpreters and compilers.

## Findings

vWasm required roughly two person-years and around 15,000 lines of F* and
proofs; rWasm took roughly one person-month. rWasm was competitive with
performance-oriented compilers in the evaluated workloads, while vWasm offered
a path to stronger compiler-correctness proofs.

## Relevance

Agent WASM can choose assurance levels deliberately: conventional runtime,
verified sandbox transformation, memory-safe translation, or isolated process.
Security and useful performance need not be treated as opposites.

## Limits

Provable sandbox containment does not prove semantic correctness, host API
safety, authorization, availability, or output integrity. rWasm also relies on
the safety of Rust and its compilation ecosystem.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
