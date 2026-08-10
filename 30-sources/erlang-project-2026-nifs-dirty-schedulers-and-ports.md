---
title: "Erlang NIFs, Dirty Schedulers, and Ports"
kind: source
created: "2026-08-10"
authors:
  - "Erlang/OTP Project"
published: null
citation_key: "erlangproject2026nifsdirtyschedulersports"
container: "Erlang/OTP System Documentation"
edition: "OTP 29.0.5"
isbn: null
doi: null
url: "https://www.erlang.org/doc/apps/erts/erl_nif.html"
accessed: "2026-08-10"
tags:
  - elixir
  - erlang
  - runtime
  - security
aliases: []
---

# Erlang NIFs, Dirty Schedulers, and Ports

## Reference

Erlang/OTP Project. *erl_nif* and *System Documentation: Built-In
Mechanisms*. OTP 29.0.5.
[NIF API](https://www.erlang.org/doc/apps/erts/erl_nif.html) and
[interoperability overview](https://www.erlang.org/doc/system/overview.html),
accessed 10 August 2026.

## Contribution

These are the authoritative safety, scheduling, cancellation, and failure-scope
rules for native code loaded into the BEAM and for external programs connected
through Ports.

## Findings

A NIF is a dynamically loaded native extension executed as part of the VM. It
does not receive BEAM memory protection or normal pre-emptive scheduling. The
OTP documentation warns that a crashing native function crashes the whole VM,
and that an erroneous NIF can corrupt internal state, hang the runtime, leak
memory or sensitive information, or degrade responsiveness.

A normal NIF should return within roughly one millisecond. Work that cannot be
split must run on a dirty CPU or dirty I/O scheduler, and correct classification
matters: CPU work on dirty I/O schedulers can starve ordinary schedulers. A
process executing a dirty NIF cannot complete termination until the NIF returns;
the NIF should check whether the process is still alive and cooperate with
cancellation.

OTP presents a threaded NIF as another option: dispatch native work to a thread
managed by the library, return from the NIF, and send the result back later.
That avoids occupying a scheduler but still shares the BEAM address space and
therefore does not contain a native crash.

A Port communicates with a separate operating-system process through a
byte-oriented interface. The boundary has encoding and IPC costs, but a worker
fault does not execute inside the BEAM. The official overview recommends an
external Port when possible and a NIF when the overhead is unacceptable.

## Relevance

This evidence is decisive for the Elixir/Rustler comparison. WebAssembly
execution is lengthy CPU work, and Wasmtime/Extism contain unsafe native
internals even when the application-facing Rust wrapper is safe. Rustler can
reduce interface mistakes and catch Rust panics, but it cannot replace the VM's
missing address-space boundary.

The Port byte stream also matches Agent WASM's coarse Extism bytes-in/bytes-out
turn boundary unusually well.

## Limits

The documentation does not quantify Port overhead for Agent WASM payloads or
show how much risk Rust removes relative to C. The recommendation to use a Port
is general guidance; a measured workload can justify a carefully designed NIF.

## Derived work

- [Host implementation comparison](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
- [Host language inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
- [Host implementation map](../10-maps/agent-wasm-host-implementation-language.md)
