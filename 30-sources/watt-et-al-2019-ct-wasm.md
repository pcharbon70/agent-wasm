---
title: "CT-Wasm: Type-Driven Secure Cryptography for the Web Ecosystem"
kind: source
created: "2026-08-07"
authors:
  - "Conrad Watt"
  - "John Renner"
  - "Natalie Popescu"
  - "Sunjay Cauligi"
  - "Deian Stefan"
published: 2019
citation_key: "watt2019ctwasm"
container: "Proceedings of the ACM on Programming Languages, POPL 2019"
edition: null
isbn: null
doi: "10.1145/3290390"
url: "https://doi.org/10.1145/3290390"
accessed: "2026-08-07"
tags:
  - formal-methods
  - security
  - webassembly
aliases: []
---

# CT-Wasm: Type-Driven Secure Cryptography for the Web Ecosystem

## Reference

Conrad Watt et al. “CT-Wasm: Type-Driven Secure Cryptography for the Web
Ecosystem.” *PACMPL*, POPL 2019. DOI [10.1145/3290390](https://doi.org/10.1145/3290390).

## Contribution

CT-Wasm extends Wasm with secrecy types intended to enforce information-flow
security and constant-time cryptographic execution.

## Method

The authors mechanize the extension, prove type-system properties, build a
verified checker, implement reference and V8-based runtimes plus a rewriting
tool, and evaluate cryptographic primitives and TweetNaCl.

## Findings

Low-level portable code can carry stronger domain-specific guarantees that are
cheap to validate. The work measured its ported cryptographic code as
constant-time and found the extension practical in its evaluated cases.

## Relevance

Agent tools may process credentials and secrets. Core sandboxing prevents host
memory access but says little about information-flow or timing leakage inside
authorized interfaces; typed extensions or verified tool profiles may be
needed for high-assurance capabilities.

## Limits

CT-Wasm is a research extension rather than the standard core language. Its
guarantees depend on the stated threat model and do not cover all
microarchitectural channels or host-interface leaks.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
