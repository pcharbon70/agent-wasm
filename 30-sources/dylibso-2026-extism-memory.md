---
title: "Extism Memory and Message Passing"
kind: source
created: "2026-08-07"
authors:
  - "Dylibso"
published: null
citation_key: "dylibso2026extismmemory"
container: "Extism Documentation"
edition: null
isbn: null
doi: null
url: "https://extism.org/docs/concepts/memory/"
accessed: "2026-08-07"
tags:
  - extism
  - runtime
  - webassembly
aliases: []
---

# Extism Memory and Message Passing

## Reference

Dylibso. *Memory*. [Extism documentation](https://extism.org/docs/concepts/memory/),
accessed 7 August 2026.

## Contribution

The document explains Extism's bytes-in/bytes-out message boundary and the
Extism-managed memory used to bridge independently managed host and guest
memory.

## Findings

Before a call, Extism resets allocations from the prior call, allocates an
input buffer, copies host bytes into it, and marks its offset and length. The
guest can read or copy the data through PDK operations. Output follows the
reverse path: the guest allocates an Extism buffer, stores encoded output,
marks it as output, and the host reads it until the next call invalidates the
buffer.

PDKs and Host SDKs add idiomatic serialization, but the portable contract is a
byte buffer. JSON, MessagePack, Protobuf, strings, and domain schemas are
application conventions rather than intrinsic Extism types.

## Relevance

The call-memory lifetime, copy path, and serialization boundary determine
correctness, performance, and output-validation requirements for Agent WASM.

## Limits

The page describes the logical model rather than measuring copies, allocation
cost, or runtime parity. Extism-managed call memory is distinct from guest
linear memory and persistent Extism variables; resetting one does not imply a
fully fresh guest instance.

## Derived work

- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Extism evaluation inquiry](../40-inquiries/should-agent-wasm-adopt-extism.md)
- [Extism topic map](../10-maps/extism-plugin-system.md)
