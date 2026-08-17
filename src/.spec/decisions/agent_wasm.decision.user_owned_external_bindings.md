---
id: agent_wasm.decision.user_owned_external_bindings
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# User-Owned External Bindings

## Context

Portable artifacts can declare model and connector requirements but must not
choose a user's provider, account, endpoint, or credential relationship.

## Decision

The installing user or authorized tenant operator owns concrete model,
provider, connector, connection, and credential-custodian bindings. Bindings
are versioned outside immutable artifacts. Materialized requests pin the chosen
binding revision across retries and replay.

## Consequences

Publishers and guests express logical intent only. No hidden default routing,
provider fallback, credential substitution, or retry-time rebinding is allowed
unless a later normative rule explicitly defines it.
