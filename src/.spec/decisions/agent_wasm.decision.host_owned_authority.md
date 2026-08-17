---
id: agent_wasm.decision.host_owned_authority
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Host-Owned Authority

## Context

Untrusted guest reducers propose decisions while the host protects tenant
isolation, authoritative state, policy, external effects, and evidence.

## Decision

The host owns authentication, admission, routing, mailbox order, turn leases,
snapshot loading, invocation limits, output validation, policy enforcement,
authoritative commit, effect dispatch, lifecycle, topology, and evidence.
Guests receive value snapshots and return untrusted patches and directives.

## Consequences

No guest receives authoritative mutable handles, ambient credentials, or direct
effect authority. Rejected, trapped, timed-out, or cancelled proposals cannot
publish successful or partial authoritative output.
