---
title: "Waltzz"
kind: source
created: "2026-08-07"
authors:
  - "Lingming Zhang"
  - "Binbin Zhao"
  - "Jiacheng Xu"
  - "Peiyu Liu"
  - "Qinge Xie"
  - "Yuan Tian"
  - "Jianhai Chen"
  - "Shouling Ji"
published: 2025
citation_key: "zhang2025waltzz"
container: "34th USENIX Security Symposium"
edition: null
isbn: "978-1-939133-52-6"
doi: null
url: "https://www.usenix.org/conference/usenixsecurity25/presentation/zhang-lingming"
accessed: "2026-08-07"
tags:
  - fuzzing
  - runtime
  - security
  - testing
  - webassembly
aliases:
  - "WebAssembly Runtime Fuzzing with Stack-Invariant Transformation"
---

# Waltzz

## Reference

Lingming Zhang et al. “Waltzz: WebAssembly Runtime Fuzzing with Stack-Invariant
Transformation.” *34th USENIX Security Symposium* (2025): 6159–6178.
[Open-access paper and artifacts](https://www.usenix.org/conference/usenixsecurity25/presentation/zhang-lingming).

## Contribution

Waltzz is a greybox fuzzer that maintains valid stack semantics while
transforming Wasm and systematically explores instruction combinations in
control and data flow.

## Method

Stack-invariant transformations, instruction-aware mutators, and skeleton-based
generation are evaluated on seven established runtimes against prior fuzzers.

## Findings

The authors report 12.4% more code coverage than the nearest evaluated
competitor, 1.38 times more unique bugs, 20 new confirmed bugs, and 17 assigned
CVE identifiers.

The result supports structured Wasm-aware mutation: preserving enough validity
to reach deep runtime states can be more productive than unconstrained binary
mutation.

## Relevance

Agent WASM should consume upstream findings and can apply stack-aware mutation
to its pinned feature profile. System-protocol fuzzing still needs separate
generators for signals, patches, directives, revisions, and crash schedules.

## Limits

Coverage and bug yield depend on the chosen versions, seeds, instrumentation,
time budget, and comparator. The technique targets runtime internals rather
than host application invariants.

## Derived work

- [WebAssembly testing synthesis](../20-notes/webassembly-testing-verification-and-agent-runtime-assurance.md)
- [Testing and verification map](../10-maps/webassembly-testing-and-verification.md)
