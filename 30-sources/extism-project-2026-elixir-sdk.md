---
title: "Extism Elixir Host SDK"
kind: source
created: "2026-08-10"
authors:
  - "Extism Project"
published: null
citation_key: "extismproject2026elixirsdk"
container: "Hex, HexDocs, and Extism Source Repository"
edition: "1.0.0; repository commit 79d20e1"
isbn: null
doi: null
url: "https://github.com/extism/elixir-sdk"
accessed: "2026-08-10"
tags:
  - elixir
  - extism
  - rust
  - rustler
  - runtime
  - webassembly
aliases: []
---

# Extism Elixir Host SDK

## Reference

Extism Project. *Extism Elixir Host SDK*. Hex version 1.0.0 and repository
commit `79d20e1`.
[Source repository](https://github.com/extism/elixir-sdk),
[Hex package](https://hex.pm/packages/extism), and
[HexDocs](https://extism.hexdocs.pm/Extism.Plugin.html), accessed 10 August
2026.

## Contribution

This is the official Extism package for Elixir and Erlang. Its implementation
shows what "Elixir support" actually means at the engine boundary and provides
a concrete baseline against which a new adapter must be assessed.

## Method

The package metadata, public documentation, `mix.exs`, Elixir wrapper modules,
Rust crate manifest, and Rust NIF implementation on the repository's default
branch were inspected. The latest repository commit changes ownership metadata;
the current Hex release remains 1.0.0, published 8 January 2024.

## Findings

The SDK is not a pure-Elixir Extism runtime. It compiles a Rustler NIF whose
Rust crate pins `extism = "1.0.0"` and `rustler = "0.30.0"`. It stores a Rust
`Plugin` behind a `ResourceArc` and lock, manually asserts `Send` and `Sync` for
the plug-in and cancellation resource wrappers, and exposes creation, calls,
function existence, and freeing through Elixir.

The public `Extism.Plugin` API accepts and returns strings rather than arbitrary
binary payloads. The README says host functions are not supported and leaves
configuration marked as unfinished. Native cancellation-handle functions exist
in the Rust and internal Elixir modules, but the public `Extism.Plugin` module
does not expose them.

The Rust functions for plug-in creation and `plugin_call` use the default
`#[rustler::nif]` annotation without `DirtyCpu`, `DirtyIo`, or asynchronous
dispatch. Because compilation and arbitrary Wasm execution can exceed the
normal-NIF time budget, this is not an acceptable scheduling model for the
Agent WASM host without redesign.

The release also trails the separately researched Extism reference runtime
1.21.0. That gap includes years of runtime, engine, limit, and API evolution.
The package is useful proof that the basic binding works, but it is not a
drop-in foundation for the repository's current invocation, host-function,
cancellation, binary-codec, evidence, and runtime-parity requirements.

## Relevance

The package collapses a misleading comparison: current in-process "Elixir
Extism" already means Elixir plus Rust through Rustler. A serious Elixir option
must choose explicitly among maintaining a modern Rustler adapter, using a
supervised external worker, or invoking a remote runtime.

## Limits

This is a source and API audit, not an execution test. A new upstream release
could change the conclusion, and unexposed internal functions might be usable
through a fork. Download counts or official ownership do not establish feature
completeness.

## Derived work

- [Host implementation comparison](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
- [Extism architecture synthesis](../20-notes/extism-plugin-system-architecture-and-runtimes.md)
- [Host language inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
- [Host implementation map](../10-maps/agent-wasm-host-implementation-language.md)
