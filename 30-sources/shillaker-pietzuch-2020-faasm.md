---
title: "Faasm: Lightweight Isolation for Efficient Stateful Serverless Computing"
kind: source
created: "2026-08-07"
authors:
  - "Simon Shillaker"
  - "Peter Pietzuch"
published: 2020
citation_key: "shillaker2020faasm"
container: "2020 USENIX Annual Technical Conference"
edition: null
isbn: "978-1-939133-14-4"
doi: null
url: "https://www.usenix.org/conference/atc20/presentation/shillaker"
accessed: "2026-08-07"
tags:
  - serverless
  - webassembly
aliases: []
---

# Faasm: Lightweight Isolation for Efficient Stateful Serverless Computing

## Reference

Simon Shillaker and Peter Pietzuch. “Faasm: Lightweight Isolation for
Efficient Stateful Serverless Computing.” *USENIX ATC 2020*, pp. 419–433.
[Open-access paper](https://www.usenix.org/conference/atc20/presentation/shillaker).

## Contribution

Faasm introduces “Faaslets,” Wasm-based in-process function isolation combined
with controlled shared regions, Linux resource controls, and initialized
snapshots for stateful serverless workloads.

## Method

The implementation combines software fault isolation with cgroups and a POSIX-
like host interface. Evaluation compares container-based execution on machine-
learning training and inference workloads.

## Findings

Co-located memory sharing and snapshots can reduce serialization, startup, and
memory costs. The paper reports a twofold training speedup with one-tenth the
memory and doubled inference throughput with lower tail latency in its studied
cases.

## Relevance

Agent workloads often combine many small stateful tools. Faasm demonstrates
the value—and risk—of separating logical isolation from physical co-location,
snapshots, shared state, and operating-system resource control.

## Limits

The host interface is not modern WASI 0.3, shared memory weakens simple
compartment reasoning, and the headline results do not generalize to arbitrary
agent workloads or current runtimes.

## Derived work

- [WebAssembly foundations and ecosystem synthesis](../20-notes/webassembly-foundations-ecosystem-and-agent-runtime-implications.md)
- [Agent runtime inquiry](../40-inquiries/how-should-agent-wasm-use-webassembly.md)
