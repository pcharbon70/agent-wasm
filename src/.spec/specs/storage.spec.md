# Revisioned Storage and Journals

```spec-meta
id: agent_wasm.storage
kind: contract
status: active
summary: Durable snapshots, append-only journals, history projections, storage isolation, and migration.
surface:
  - "lib/agent_wasm/storage/**/*.ex"
  - "test/agent_wasm/storage/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Revisioned Snapshots, Journals, History, and Storage Contracts](../../../60-specification/25-revisioned-snapshots-journals-history-and-storage-contracts.md)

## Requirements

```spec-requirements
- id: agent_wasm.storage.snapshots
  statement: Durable snapshots shall be tenant isolated, revisioned, checksummed, lifecycle consistent, and verified on every read.
  priority: must
  stability: stable
- id: agent_wasm.storage.journals
  statement: Audit and reconstruction journals shall be append-only, ordered, atomic, and sufficient for reconstruction while conversation views remain filtered projections.
  priority: must
  stability: stable
- id: agent_wasm.storage.guarantees
  statement: Storage adapters shall provide isolated reads, serializable compare-and-commit writes, durability, conflict rejection, backup, and recovery.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.storage.implementation_frontier
  covers:
    - agent_wasm.storage.snapshots
    - agent_wasm.storage.journals
    - agent_wasm.storage.guarantees
  reason: No durable storage adapter, snapshot store, or journal exists.
```
