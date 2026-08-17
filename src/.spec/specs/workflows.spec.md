# Agentic Workflows, Provenance, Safety, and Acceptance

```spec-meta
id: agent_wasm.workflows
kind: workflow
status: active
summary: Representative AI workflows, provenance, hostile-output validation, budgets, deterministic resume, and Milestone 7 acceptance.
surface:
  - "lib/agent_wasm/workflows/**/*.ex"
  - "test/agent_wasm/workflows/**/*_test.exs"
decisions:
  - agent_wasm.decision.atomic_durable_effects
  - agent_wasm.decision.least_authority_credential_custody
  - agent_wasm.decision.user_owned_external_bindings
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Contract and Data Model](../../../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-contract-and-data-model.md)
- [Behavior and Integration](../../../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-behavior-and-integration.md)
- [Failure Evidence and Operational Notes](../../../60-specification/45-agentic-workflows-provenance-safety-and-milestone-acceptance-failure-evidence-and-operational-notes.md)

## Requirements

```spec-requirements
- id: agent_wasm.workflows.corpus
  statement: Direct model, structured response, model-tool continuation, retrieval-grounded, code-execution, and multi-agent workflows shall use durable explicit state and pinned dependencies.
  priority: must
  stability: stable
- id: agent_wasm.workflows.safety
  statement: Hostile output, approvals, quotas, credential revocation, stream cancellation, provenance, and workflow budgets shall be validated before state, context, tool, or user admission.
  priority: must
  stability: stable
- id: agent_wasm.workflows.acceptance
  statement: Workflow, provenance, safety, cost, resume, credential non-exposure, and residual model-risk evidence shall gate Milestone 7 acceptance.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.workflows.implementation_frontier
  covers:
    - agent_wasm.workflows.corpus
    - agent_wasm.workflows.safety
    - agent_wasm.workflows.acceptance
  reason: Agentic workflows and their integration acceptance corpus are not implemented.
```
