---
id: agent_wasm.decision.elixir_otp_product_host
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Elixir OTP Product Host

## Context

The source specification is language-neutral, while the resolved
[host-language research](../../../20-notes/elixir-otp-port-finished-product-packaging-and-release-pipeline.md)
selects the finished-product implementation model.

## Decision

Agent WASM is an Elixir/OTP product. Elixir owns the public API, supervision,
mailboxes, policy, lifecycle, configuration, telemetry, release, and operator
surfaces. Native Wasm-engine work is isolated behind a private byte-oriented
OTP Port and does not create a second public host API.

<!-- covers: agent_wasm.package.product_host -->

## Consequences

The Mix application and OTP release are the product unit. Native worker crashes
remain outside the BEAM failure domain and require supervised restart, bounded
framing, packaging, and platform qualification.
