# Specification Authority

```spec-meta
id: agent_wasm.specification_authority
kind: policy
status: active
summary: Authority, applicability, traceability, promotion, and conflict handling.
surface: []
decisions:
  - agent_wasm.decision.specification_authority
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Agent WASM Specification Authority](../../../SPECIFICATION-AUTHORITY.md)

## Requirements

```spec-requirements
- id: agent_wasm.specification_authority.normative_source
  statement: Implementation behavior and conformance claims shall follow applicable normative specification chapters and visibly normative content.
  priority: must
  stability: stable
- id: agent_wasm.specification_authority.conflict_gate
  statement: Conflicting normative rules, ambiguity, and normative silence shall block conformance for the disputed behavior.
  priority: must
  stability: stable
- id: agent_wasm.specification_authority.traceability
  statement: Tests, implementation, and evidence shall cite governing document headings and shall not override normative text.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.specification_authority.implementation_frontier
  covers:
    - agent_wasm.specification_authority.normative_source
    - agent_wasm.specification_authority.conflict_gate
    - agent_wasm.specification_authority.traceability
  reason: Automated source-heading traceability and conflict gating are not implemented.
```
