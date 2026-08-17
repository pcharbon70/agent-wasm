# Agent WASM Package

```spec-meta
id: agent_wasm.package
kind: package
status: active
summary: Elixir/OTP product boundary and complete normative source mapping.
surface:
  - README.md
  - mix.exs
  - lib/agent_wasm.ex
  - test/agent_wasm/guest_protocol/lifecycle_conformance_test.exs
  - test/test_helper.exs
decisions:
  - agent_wasm.decision.specification_authority
  - agent_wasm.decision.elixir_otp_product_host
  - agent_wasm.decision.evidence_gated_conformance
```

## Requirements

```spec-requirements
- id: agent_wasm.package.product_host
  statement: Agent WASM shall be delivered as an Elixir/OTP product whose public programming and operations surfaces belong to the Mix application.
  priority: must
  stability: stable
- id: agent_wasm.package.source_authority
  statement: Package behavior shall follow the complete applicable normative source corpus and shall not use implementation behavior to resolve source conflicts silently.
  priority: must
  stability: stable
- id: agent_wasm.package.source_coverage
  statement: The SpecLed workspace shall maintain one implementation subject for each of the 39 numbered technical areas and two governance specifications.
  priority: must
  stability: stable
- id: agent_wasm.package.conformance_gate
  statement: The package shall not claim implemented conformance until applicable exceptions are replaced by linked or executed evidence and normative acceptance gates pass.
  priority: must
  stability: stable
- id: agent_wasm.package.bootstrap_test
  statement: The current Elixir package shall compile and pass its ExUnit suite.
  priority: must
  stability: evolving
```

## Verification

```spec-verification
- kind: file
  target: .spec/decisions/agent_wasm.decision.elixir_otp_product_host.md
  covers:
    - agent_wasm.package.product_host
- kind: file
  target: .spec/decisions/agent_wasm.decision.specification_authority.md
  covers:
    - agent_wasm.package.source_authority
- kind: file
  target: .spec/decisions/agent_wasm.decision.evidence_gated_conformance.md
  covers:
    - agent_wasm.package.conformance_gate
- kind: command
  target: mix spec.validate
  execute: true
  covers:
    - agent_wasm.package.source_coverage
- kind: command
  target: mix test
  execute: true
  covers:
    - agent_wasm.package.bootstrap_test
```
