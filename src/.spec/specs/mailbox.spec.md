# Mailboxes, Ordering, Fairness, and Turn Leases

```spec-meta
id: agent_wasm.mailbox
kind: module
status: active
summary: Bounded priority mailboxes, overload behavior, fairness, delivery metadata, leases, and fencing.
surface:
  - "lib/agent_wasm/mailbox/**/*.ex"
  - "test/agent_wasm/mailbox/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.logical_identity_disposable_placement
```

## Source Traceability

- [Mailboxes, Ordering, Bounds, Fairness, and Turn Leases](../../../60-specification/21-mailboxes-ordering-bounds-fairness-and-turn-leases.md)

## Requirements

```spec-requirements
- id: agent_wasm.mailbox.ordering_bounds
  statement: Mailboxes shall enforce priority, FIFO tie behavior, fairness, count, byte, age, source, tenant, and delivery bounds.
  priority: must
  stability: stable
- id: agent_wasm.mailbox.overload
  statement: Overload shall produce the configured reject, defer, coalesce, supersede, or dead-letter outcome with stable diagnostics.
  priority: must
  stability: stable
- id: agent_wasm.mailbox.lease_fencing
  statement: A valid per-agent lease and current fencing token shall be required for a turn, renewal, and authoritative completion.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.mailbox.implementation_frontier
  covers:
    - agent_wasm.mailbox.ordering_bounds
    - agent_wasm.mailbox.overload
    - agent_wasm.mailbox.lease_fencing
  reason: Mailbox scheduling, overload policies, and turn leases are not implemented.
```
