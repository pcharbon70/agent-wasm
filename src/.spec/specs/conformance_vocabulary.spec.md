# Conformance Vocabulary

```spec-meta
id: agent_wasm.conformance_vocabulary
kind: policy
status: active
summary: Requirement force, behavior classes, variability, limits, and profiles.
surface: []
decisions:
  - agent_wasm.decision.specification_authority
  - agent_wasm.decision.evidence_gated_conformance
```

## Source Traceability

- [Agent WASM Conformance Vocabulary](../../../CONFORMANCE-VOCABULARY.md)

## Requirements

```spec-requirements
- id: agent_wasm.conformance_vocabulary.requirement_words
  statement: Normative implementation work shall preserve the five canonical requirement words and their defined force.
  priority: must
  stability: stable
- id: agent_wasm.conformance_vocabulary.behavior_classes
  statement: Invalid input, implementation-defined choices, presentation variation, limits, and runtime failures shall remain distinguishable observable classes.
  priority: must
  stability: stable
- id: agent_wasm.conformance_vocabulary.profile
  statement: Every claimed release shall publish supported versions, choices, options, deviations, limits, and bounded presentation variation.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.conformance_vocabulary.implementation_frontier
  covers:
    - agent_wasm.conformance_vocabulary.requirement_words
    - agent_wasm.conformance_vocabulary.behavior_classes
    - agent_wasm.conformance_vocabulary.profile
  reason: The implementation profile and diagnostic class registry are not implemented.
```
