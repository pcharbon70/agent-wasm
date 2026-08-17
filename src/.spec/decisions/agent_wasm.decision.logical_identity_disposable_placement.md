---
id: agent_wasm.decision.logical_identity_disposable_placement
status: accepted
date: 2026-08-11
affects:
  - repo.governance
---

# Logical Identity and Disposable Placement

## Context

Logical agents, relationships, and desired topology must survive replacement of
processes, hosts, workers, Wasm instances, sockets, and engine objects.

## Decision

Tenant-qualified logical identity and durable desired state are authoritative.
Live actors, guest instances, Port handles, process identifiers, network
endpoints, and physical placement are disposable projections fenced by leases
and recreated through reconciliation.

## Consequences

No live handle is persisted as agent identity. Recovery reconstructs placement
from durable records, and stale workers cannot commit through expired or lower
fencing authority.
