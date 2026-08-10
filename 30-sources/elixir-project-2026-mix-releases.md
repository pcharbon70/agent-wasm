---
title: "Elixir Project: Mix Releases"
kind: source
created: "2026-08-10"
authors:
  - "Elixir Project"
published: null
citation_key: "elixirproject2026mixreleases"
container: "Mix Documentation"
edition: "Mix 1.20.3"
isbn: null
doi: null
url: "https://mix.hexdocs.pm/Mix.Tasks.Release.html"
accessed: "2026-08-10"
tags:
  - deployment
  - elixir
  - runtime
aliases:
  - "Mix releases"
---

# Elixir Project: Mix Releases

## Reference

Elixir Project. *mix release*. Mix 1.20.3 documentation.
[Canonical documentation](https://mix.hexdocs.pm/Mix.Tasks.Release.html),
accessed 10 August 2026.

## Contribution

The documentation defines how Mix assembles, customizes, packages, configures,
starts, and deploys self-contained Elixir/OTP releases.

## Method

This note inspected the current task documentation for the release contents,
target requirements, ERTS inclusion, application `priv` layout, configuration,
overlays, custom steps, tar creation, container guidance, and lifecycle
commands.

## Findings

A default Mix release contains precompiled application code and includes ERTS,
so the target does not need the Elixir or Erlang toolchain. The generated tree
places each application beneath `lib/APP_NAME-APP_VSN/` and includes its
`priv/` directory. That makes application `priv` the ordinary location for a
private Port executable bundled with the host.

Releases are target-specific. The build host and deployment target must agree
on architecture, vendor/operating system, ABI, and required dynamic libraries.
The documentation specifically notes that native dependencies must be compiled
for the same target triple. It recommends matching CI/container environments
and describes `ERL_AFLAGS="+JMsingle true"` when emulation and the ERTS JIT
interact during image builds.

Mix supports release overlays, custom steps, and a `:tar` step. Runtime
configuration is evaluated from `config/runtime.exs` without Mix being present
in the release. Generated management commands cover foreground start, stop,
remote access, one-off evaluation, and related operational tasks.

## Relevance

This is the primary evidence that Agent WASM can ship as one self-contained
Elixir/OTP product while carrying a target-native worker inside application
`priv`. It also prevents the incorrect assumption that one assembled release
is portable across operating systems or CPU/ABI combinations.

## Limits

Mix assembles and launches the release but does not choose the native worker's
protocol, produce its provenance, prove its target compatibility, or define
Agent WASM upgrade policy. Those remain application and pipeline obligations.

## Derived work

- [Elixir/OTP Port packaging and release pipeline](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
- [Host implementation map](../10-maps/agent-wasm-host-implementation-language.md)
