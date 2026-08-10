---
title: "Phoenix Esbuild Binary Installer"
kind: source
created: "2026-08-10"
authors:
  - "Phoenix Framework Project"
published: null
citation_key: "phoenixproject2026esbuildbinaryinstaller"
container: "Phoenix Framework Esbuild Repository"
edition: "esbuild 0.10.0"
isbn: null
doi: null
url: "https://github.com/phoenixframework/esbuild"
accessed: "2026-08-10"
tags:
  - deployment
  - elixir
aliases:
  - "Elixir esbuild installer"
---

# Phoenix Esbuild Binary Installer

## Reference

Phoenix Framework Project. *Esbuild: Mix tasks for installing and invoking
esbuild*. Package documentation 0.10.0.
[Source repository](https://github.com/phoenixframework/esbuild) and
[Hex documentation](https://hexdocs.pm/esbuild/), accessed 10 August 2026.

## Contribution

This Elixir package supplies Mix tasks that install and invoke a separately
versioned, target-specific executable without turning that executable's source
language into an application-facing API.

## Method

This note inspected the installation, dependency, version configuration,
target-path, profile, and deployment guidance in the current project README and
Hex documentation.

## Findings

An Elixir application adds the package as a dependency, chooses an executable
version in application configuration, and runs a Mix installation task. The
selected executable is retained under `_build/esbuild-TARGET`, where `TARGET`
is the system target architecture. Mix profiles then invoke that executable
with application-owned arguments, working directory, and environment.

The package therefore establishes a familiar developer experience for an
Elixir wrapper that manages a target-native tool at build time. The public
programming and configuration surface remains Elixir.

## Relevance

Agent WASM can use the same broad distribution shape for an embeddable Hex
package: select and stage a private Port worker during dependency preparation,
then include it in the application's release. Agent WASM additionally needs a
signed asset manifest, strict checksum/provenance verification, offline
operation, release pairing, and a startup protocol handshake because the
worker is a production runtime component rather than an asset-development
tool.

## Limits

The project is a precedent for usability, not a complete supply-chain design
for Agent WASM. Its threat model, executable lifetime, failure semantics, and
production criticality differ from a Wasm engine worker.

## Derived work

- [Elixir/OTP Port packaging and release pipeline](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
