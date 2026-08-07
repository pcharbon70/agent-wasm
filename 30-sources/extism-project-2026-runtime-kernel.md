---
title: "Extism Runtime Kernel"
kind: source
created: "2026-08-07"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026eip007"
container: "Extism Improvement Proposals"
edition: "EIP-007"
isbn: null
doi: null
url: "https://github.com/extism/proposals/blob/main/EIP-007-extism-runtime-kernel.md"
accessed: "2026-08-07"
tags:
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism Runtime Kernel

## Reference

Extism Project. *Extism Runtime Kernel*. EIP-007.
[Proposal](https://github.com/extism/proposals/blob/main/EIP-007-extism-runtime-kernel.md),
accessed 7 August 2026. Current
[kernel source](https://github.com/extism/extism/blob/main/kernel/src/lib.rs)
was used to confirm the implemented memory layout and exports.

## Contribution

EIP-007 moves the portable portion of the Extism runtime into an internal Wasm
module, `extism-runtime.wasm`, so host SDK implementations can reuse memory and
call bookkeeping across different underlying engines.

## Findings

The kernel owns an isolated linear memory, a resettable allocator, input and
output offsets and lengths, and error storage. The host instantiates and links
it with the user module, copies each call input into kernel memory, invokes the
user export, then reads the designated output or error.

Configuration, mutable variables, HTTP, logging, WASI, timeouts, cancellation,
and engine limits remain host-implementation responsibilities. The kernel
therefore standardizes the data plane, not the entire runtime behavior.

Current source implements a bump allocator with reusable freed blocks, uses
64-bit handles into kernel memory, treats zero as a null/failure offset, and
zeroes/reset metadata and allocations between calls.

## Relevance

The kernel is the reason a Wasmtime, Wazero, JavaScript, or Chicory host can
run the same Extism plug-in without reproducing every memory primitive.

## Limits

Shared kernel code reduces one source of drift but does not make all host
implementations conformant. It also introduces another Wasm module and copy
boundary whose cost and limits should be measured.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
