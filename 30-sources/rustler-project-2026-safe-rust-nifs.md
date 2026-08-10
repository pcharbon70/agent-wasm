---
title: "Rustler Safe Rust NIF Bridge"
kind: source
created: "2026-08-10"
authors:
  - "Rustler Project"
published: null
citation_key: "rustlerproject2026saferustnifs"
container: "Hex, HexDocs, and Rustler API Documentation"
edition: "0.38.0"
isbn: null
doi: null
url: "https://hex.pm/packages/rustler"
accessed: "2026-08-10"
tags:
  - elixir
  - implementation-language
  - rust
  - rustler
  - runtime
aliases: []
---

# Rustler Safe Rust NIF Bridge

## Reference

Rustler Project. *Rustler*. Version 0.38.0, released 25 May 2026.
[Hex package](https://hex.pm/packages/rustler),
[HexDocs](https://rustler.hexdocs.pm/),
[Rust API](https://docs.rs/rustler/latest/rustler/), and
[source repository](https://github.com/rusterlium/rustler), accessed 10 August
2026.

## Contribution

Rustler supplies Mix build integration and a Rust library for implementing
Erlang NIFs with typed term conversion, panic catching, resource handles,
scheduler annotations, and asynchronous message construction.

## Findings

Hex lists Rustler 0.38.0 as the current package. The `#[rustler::nif]` macro
wraps argument decoding, return encoding, and NIF boilerplate. The project
catches Rust panics before they unwind across the C boundary and aims to let
application authors write NIFs in safe Rust.

The macro documentation explicitly recommends a scheduler flag for work taking
more than about one millisecond, using `DirtyCpu` for compute and `DirtyIo` for
blocking I/O. These flags implement, rather than supersede, OTP's NIF scheduling
rules.

`ResourceArc<T>` is a thread-safe, reference-counted resource shared by Rust
and Erlang terms. It is useful for compiled modules, plug-in handles, and
cancellation tokens. Its destructor runs when the VM eventually collects the
last reference, so it is unsuitable as the sole owner of authoritative agent
state or prompt resource release.

`OwnedEnv` permits a non-BEAM Rust thread to build a term and send a result to
an Erlang process. This makes a bounded native worker pool possible without
holding a normal scheduler during an Extism call. `OwnedEnv` is not an Erlang
process and cannot execute Elixir callbacks.

Rustler's safe-Rust claim is meaningful but scoped. A wrapper can prevent many
term-lifetime mistakes and catch ordinary Rust panics; it cannot prove unsafe
code inside Wasmtime, Extism, a C dependency, an allocator, or the operating
system. OTP's process-wide NIF crash warning still applies to the loaded native
library as a whole.

## Relevance

Rustler makes a narrow Elixir/Rust execution adapter technically credible and
much safer to author than a handwritten C NIF. Its scheduling and resource APIs
also identify the design constraints that such an adapter must satisfy.

## Limits

Package currency and adoption are not proof of fitness for an untrusted Wasm
runtime. The sources provide no Agent WASM benchmark, no engine crash-containment
guarantee, and no automatic mailbox, tenant, or durability semantics.

## Derived work

- [Host implementation comparison](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
- [Host language inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
- [Host implementation map](../10-maps/agent-wasm-host-implementation-language.md)
