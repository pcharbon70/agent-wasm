---
id: agent_wasm.decision.least_authority_credential_custody
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Least Authority and Credential Custody

## Context

Guests, plugins, host adapters, and external workers operate across different
trust zones and must not gain ambient authority or raw end-user credentials.

## Decision

Capabilities are independently authorized, attenuated, bounded, and revoked by
the host. End-user provider and connector credentials remain with an external
custodian or workload identity. The host dispatches typed use-only operations
with sender-constrained handles and admits results only with verified receipts.

## Consequences

Credential bytes and transferable bearer authority cannot enter guests,
plugins, general host memory, Port messages, state, journals, diagnostics,
traces, crash dumps, or support bundles. Direct authenticated egress that
bypasses the custodian is denied.
