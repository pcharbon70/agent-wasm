# Single-Agent Host Flow

```spec-meta
id: agent_wasm.host_flow
kind: workflow
status: active
summary: End-to-end admission, mailbox, lease, invocation, validation, commit, directive, and evidence flow.
surface:
  - "lib/agent_wasm/host_flow/**/*.ex"
  - "test/agent_wasm/host_flow/**/*_test.exs"
decisions:
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Single-Agent Host Flow and Milestone Acceptance](../../../60-specification/24-single-agent-host-flow-and-milestone-acceptance.md)

## Requirements

```spec-requirements
- id: agent_wasm.host_flow.order
  statement: A turn shall preserve the governing admission, dequeue, lease, snapshot, invocation, validation, commit, directive, and release order.
  priority: must
  stability: stable
- id: agent_wasm.host_flow.failure_atomicity
  statement: Trap, timeout, cancellation, invalid output, stale revision, and policy rejection shall leave no unauthorized successful or partial state.
  priority: must
  stability: stable
- id: agent_wasm.host_flow.acceptance
  statement: Direct, FSM, timer, sensor, cancellation, and terminal flows shall retain complete bounded turn and regression evidence.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.host_flow.implementation_frontier
  covers:
    - agent_wasm.host_flow.order
    - agent_wasm.host_flow.failure_atomicity
    - agent_wasm.host_flow.acceptance
  reason: End-to-end host orchestration and Milestone 3 fixtures are not implemented.
```
