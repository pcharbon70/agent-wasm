---
title: "Swivel: Hardening WebAssembly against Spectre"
kind: source
created: "2026-08-07"
authors:
  - "Shravan Narayan"
  - "Craig Disselkoen"
  - "Daniel Moghimi"
  - "Sunjay Cauligi"
  - "Evan Johnson"
  - "Zhao Gang"
  - "Anjo Vahldiek-Oberwagner"
  - "Ravi Sahita"
  - "Hovav Shacham"
  - "Dean Tullsen"
  - "Deian Stefan"
published: 2021
citation_key: "narayan2021swivel"
container: "30th USENIX Security Symposium"
edition: null
isbn: "978-1-939133-24-3"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/narayan"
accessed: "2026-08-07"
tags:
  - security
  - webassembly
aliases: []
---

# Swivel: Hardening WebAssembly against Spectre

## Reference

Shravan Narayan et al. “Swivel: Hardening WebAssembly against Spectre.”
*USENIX Security 2021*, pp. 1433–1450.
[Open-access paper](https://www.usenix.org/conference/usenixsecurity21/presentation/narayan).

## Contribution

Swivel is a compiler framework for preventing speculative-execution attacks
from escaping a Wasm sandbox or coercing another tenant or host into leaking
data.

## Method

The authors design software-only and hardware-assisted defenses, each with
randomized and deterministic variants, then evaluate them on the
Wasm-compatible SPEC 2006 subset.

## Findings

Architectural isolation does not automatically hold under speculative
execution. The randomized variants stayed under 10.3% overhead in the reported
evaluation; deterministic variants ranged much higher on some benchmarks but
outperformed generic fence-based defenses.

## Relevance

Multi-tenant agent execution must state whether the adversary model includes
microarchitectural leakage. Runtime selection and host deployment topology may
matter as much as the Wasm language boundary.

## Limits

Swivel addresses Spectre classes in its modeled and evaluated configurations,
not every side channel or all current CPUs and runtimes. Reported overheads are
historical workload-specific evidence.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
