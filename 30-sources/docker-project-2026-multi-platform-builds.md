---
title: "Docker Multi-Platform Builds"
kind: source
created: "2026-08-10"
authors:
  - "Docker Project"
published: null
citation_key: "dockerproject2026multiplatformbuilds"
container: "Docker Documentation"
edition: null
isbn: null
doi: null
url: "https://docs.docker.com/build/building/multi-platform/"
accessed: "2026-08-10"
tags:
  - deployment
  - runtime
aliases:
  - "Docker Buildx multi-platform builds"
---

# Docker Multi-Platform Builds

## Reference

Docker Project. *Multi-platform builds*.
[Docker documentation](https://docs.docker.com/build/building/multi-platform/),
accessed 10 August 2026.

## Contribution

The documentation explains how BuildKit/Buildx creates, stores, and selects
multiple operating-system and architecture variants under one OCI image name.

## Method

This note inspected the current description of manifest lists, platform
selection, builder prerequisites, emulation, native builders, and
cross-compilation strategies.

## Findings

A multi-platform image contains a manifest list whose child manifests point to
separate platform configurations and layers. A registry stores the list and
the individual variants; a pull selects the appropriate variant for the host's
architecture. Thus a single product tag can offer Linux AMD64 and ARM64 while
still carrying target-native ERTS and worker binaries in each child image.

Docker documents three build strategies: QEMU emulation, multiple native
builder nodes, and cross-compilation. Emulation is the easiest to start but can
be slow for compilation. A custom `docker-container` builder can build and push
multi-platform results even when the local classic image store cannot load the
manifest list.

## Relevance

The manifest-list model gives Agent WASM one operator-facing OCI product name
without pretending a native Mix release or Port worker is target-neutral. It
also clarifies that “multi-platform” here means OS/CPU release variants, not
multiple public host languages.

## Limits

Buildx does not prove that the Elixir release or native worker functions on a
target. Every child build still needs target-specific Port, release, and smoke
tests. Emulation can differ from native execution and is not sufficient
evidence for every production service objective.

## Derived work

- [Elixir/OTP Port packaging and release pipeline](../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
