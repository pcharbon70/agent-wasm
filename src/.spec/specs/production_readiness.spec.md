# Examples, Runbooks, SLO Evidence, and Production Acceptance

```spec-meta
id: agent_wasm.production_readiness
kind: workflow
status: active
summary: Maintained examples, operational runbooks, service objectives, evidence, support, risk, ownership, and release gates.
surface:
  - "test/agent_wasm/production_readiness/**/*_test.exs"
  - "examples/**/*"
  - "runbooks/**/*"
decisions:
  - agent_wasm.decision.evidence_gated_conformance
  - agent_wasm.decision.elixir_otp_product_host
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/50-examples-runbooks-slo-evidence-and-production-acceptance-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/50-examples-runbooks-slo-evidence-and-production-acceptance-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/50-examples-runbooks-slo-evidence-and-production-acceptance-failure-evidence-and-operational-notes.md)
- [Phase 5 Integration Tests](../../../60-specification/50-examples-runbooks-slo-evidence-and-production-acceptance-phase-5-integration-tests.md)

## Requirements

```spec-requirements
- id: agent_wasm.production_readiness.examples_runbooks
  statement: Canonical examples and dependency, overload, stuck-turn, repeated-effect, divergence, revocation, tenant-incident, recovery, and rollback runbooks shall use supported surfaces and reproducible evidence.
  priority: must
  stability: stable
- id: agent_wasm.production_readiness.slos_evidence
  statement: Admission, latency, durability, effect delay, recovery, availability, isolation, and evidence completeness shall have measured objectives, budgets, alerts, immutable evidence, and retained reports.
  priority: must
  stability: stable
- id: agent_wasm.production_readiness.release_gate
  statement: Conformance, security, performance, runbook, example, support-matrix, residual-risk, ownership, deployment, and verification evidence shall gate production release.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.production_readiness.implementation_frontier
  covers:
    - agent_wasm.production_readiness.examples_runbooks
    - agent_wasm.production_readiness.slos_evidence
    - agent_wasm.production_readiness.release_gate
  reason: Production examples, runbooks, SLO measurement, evidence packages, and release acceptance do not exist.
```
