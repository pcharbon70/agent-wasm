# Profiles and Architectural Boundaries

```spec-meta
id: agent_wasm.profile
kind: contract
status: active
summary: Host and guest ownership, profiles, model choice, credential custody, and bootstrap boundaries.
surface:
  - "lib/agent_wasm/profile/**/*.ex"
  - "test/agent_wasm/profile/**/*_test.exs"
decisions:
  - agent_wasm.decision.portable_guest_protocol
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Profile Vocabulary and Architectural Boundaries](../../../60-specification/01-profile-vocabulary-and-architectural-boundaries.md)

## Requirements

```spec-requirements
- id: agent_wasm.profile.ownership
  statement: Profiles shall preserve host authority over identity, state, scheduling, policy, effects, topology, and evidence while guests remain deterministic proposal producers.
  priority: must
  stability: stable
- id: agent_wasm.profile.bootstrap
  statement: The bootstrap guest profile shall expose the portable reducer boundary without ambient WASI or credential authority.
  priority: must
  stability: stable
- id: agent_wasm.profile.disclosure
  statement: A release shall publish its supported profile, versions, extensions, choices, and limits.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.profile.implementation_frontier
  covers:
    - agent_wasm.profile.ownership
    - agent_wasm.profile.bootstrap
    - agent_wasm.profile.disclosure
  reason: Profile loading, enforcement, and publication are not implemented.
```
