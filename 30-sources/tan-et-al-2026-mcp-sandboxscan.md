---
title: "MCP-SandboxScan: WASM-Based Secure Execution and Runtime Analysis for MCP Tools"
kind: source
created: "2026-08-07"
authors:
  - "Zhuoran Tan"
  - "Run Hao"
  - "Jeremy Singer"
  - "Yutian Tang"
  - "Christos Anagnostopoulos"
published: 2026
citation_key: "tan2026mcpsandboxscan"
container: "arXiv"
edition: "arXiv:2601.01241"
isbn: null
doi: null
url: "https://arxiv.org/abs/2601.01241"
accessed: "2026-08-07"
tags:
  - agent-tools
  - security
  - wasi
  - webassembly
aliases:
  - "MCP-SandboxScan"
---

# MCP-SandboxScan: WASM-Based Secure Execution and Runtime Analysis for MCP Tools

## Reference

Zhuoran Tan et al. “MCP-SandboxScan: WASM-based Secure Execution and Runtime
Analysis for MCP Tools.” arXiv:2601.01241, 2026.
[Preprint](https://arxiv.org/abs/2601.01241).

## Contribution

The paper directly studies Wasm/WASI as a containment and evidence layer for
executing untrusted Model Context Protocol tools.

## Method

The prototype injects distinguishable environment and filesystem canaries,
executes tools through WASI-backed or native paths, captures MCP-visible
outputs and egress evidence, and searches for source-to-sink witnesses. It adds
semantic profiling when dynamic execution is unavailable and evaluates
transformation-related false negatives and token-collision false positives.

## Findings

Targeted case studies surfaced reflected external values and denied filesystem
capabilities as auditable runtime evidence. Broader scanning showed that
packaging and startup variation constrain dynamic coverage; semantic fallback
expands visibility but is not vulnerability ground truth. Witnesses likewise
indicate exposure, not automatically exploitation.

## Relevance

This is the closest research to Agent WASM's likely problem. It supports a
design in which containment, capability-denial evidence, output provenance,
and agent-visible sink analysis are separate controls.

## Limits

The work is a 2026 preprint, its dynamic analysis is path-dependent, and simple
matching can miss transformed data or report benign coincidences. Three case
studies cannot establish production security.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
- [WebAssembly topic map](../10-maps/webassembly-foundations-and-ecosystem.md)
