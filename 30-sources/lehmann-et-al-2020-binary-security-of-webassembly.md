---
title: "Everything Old Is New Again: Binary Security of WebAssembly"
kind: source
created: "2026-08-07"
authors:
  - "Daniel Lehmann"
  - "Johannes Kinder"
  - "Michael Pradel"
published: 2020
citation_key: "lehmann2020binarysecurity"
container: "29th USENIX Security Symposium"
edition: null
isbn: "978-1-939133-17-5"
doi: null
url: "https://www.usenix.org/system/files/sec20-lehmann.pdf"
accessed: "2026-08-07"
tags:
  - security
  - webassembly
aliases: []
---

# Everything Old Is New Again: Binary Security of WebAssembly

## Reference

Daniel Lehmann, Johannes Kinder, and Michael Pradel. “Everything Old Is New
Again: Binary Security of WebAssembly.” *USENIX Security 2020*, pp. 217–234.
[Open-access paper](https://www.usenix.org/system/files/sec20-lehmann.pdf).

## Contribution

The paper separates host sandbox security from the security of a program
compiled from a memory-unsafe language into one Wasm linear memory.

## Method

The authors construct attack primitives and end-to-end exploits across three
Wasm platforms, then assess their feasibility in real binaries and SPEC CPU
programs.

## Findings

Validation and fault isolation prevent arbitrary host-memory and control-flow
access, yet spatial bugs inside a guest's own linear memory can corrupt its
data, heap metadata, and application invariants. Some mitigations familiar from
native binaries do not map directly to the Wasm layout.

## Relevance

Agent WASM must not label a C/C++-derived tool “memory safe” merely because it
runs inside Wasm. Sandbox containment limits blast radius; source-language
safety, compartmentalization, and interface validation remain distinct.

## Limits

The work focuses on the then-current ecosystem and memory-unsafe source
programs. It does not show that Wasm host isolation is ineffective, nor does it
evaluate modern component boundaries.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
