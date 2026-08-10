---
title: "Rustler Precompiled NIF Distribution"
kind: source
created: "2026-08-10"
authors:
  - "Rustler Precompiled Project"
published: null
citation_key: "rustlerproject2026precompilednifdistribution"
container: "Hex and HexDocs"
edition: "0.9.0"
isbn: null
doi: null
url: "https://hex.pm/packages/rustler_precompiled"
accessed: "2026-08-10"
tags:
  - elixir
  - implementation-language
  - rust
  - rustler
  - runtime
aliases: []
---

# Rustler Precompiled NIF Distribution

## Reference

Rustler Precompiled Project. *rustler_precompiled*. Version 0.9.0, released
26 March 2026.
[Hex package](https://hex.pm/packages/rustler_precompiled),
[module documentation](https://rustler-precompiled.hexdocs.pm/RustlerPrecompiled.html),
and
[precompilation guide](https://rustler-precompiled.hexdocs.pm/precompilation_guide.html),
accessed 10 August 2026.

## Contribution

Rustler Precompiled automates target-specific NIF selection, download, checksum
verification, and source-build fallback so users do not need a Rust toolchain
for every Elixir release installation.

## Findings

Version 0.9.0 documents a default matrix covering Linux, macOS, and Windows,
several architectures, GNU and musl Linux variants, and OTP NIF versions. The
artifact name incorporates NIF version and Rust target information. Maintainers
publish a checksum file in the Hex package, and the installer verifies the
downloaded native artifact against that fingerprint.

The tool substantially improves consumer ergonomics, but it does not make a
native library portable by itself. Maintainers still own the build matrix,
minimum glibc or other ABI variants, CPU-feature variants, release hosting,
checksums, optional attestations, and testing against supported Elixir/OTP
combinations. A missing target either needs an explicit source-build path or
becomes an unsupported deployment.

Checksums bind an artifact to the package metadata; they do not prove the CI
builder, dependency graph, source revision, or native library is trustworthy.
Agent WASM's own provenance and admission evidence remains necessary.

## Relevance

This package mitigates one of Rustler's largest operational disadvantages but
does not eliminate the release and supply-chain matrix. It is useful if a NIF
adapter is offered, and largely unnecessary for an out-of-process Rust binary
that is already distributed as a normal application artifact.

## Limits

The documentation is for library distribution, not Agent WASM deployment. It
does not assess Extism/Wasmtime binary size, startup time, supported engine
features, or failure containment.

## Derived work

- [Host implementation comparison](../20-notes/agent-wasm-host-implementation-language-and-runtime-boundary.md)
- [Host language inquiry](../40-inquiries/which-host-implementation-approach-should-agent-wasm-use.md)
