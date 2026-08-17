# Capability Policy and Attenuation

```spec-meta
id: agent_wasm.capability_policy
kind: policy
status: active
summary: Host-owned policy decisions, attenuation, approvals, cache invalidation, limits, and enforcement points.
surface:
  - "lib/agent_wasm/capability_policy/**/*.ex"
  - "test/agent_wasm/capability_policy/**/*_test.exs"
decisions:
  - agent_wasm.decision.host_owned_authority
  - agent_wasm.decision.least_authority_credential_custody
```

## Source Traceability

- [Capability Policy, Attenuation, Limits, and Enforcement](../../../60-specification/31-capability-policy-attenuation-limits-and-enforcement.md)

## Requirements

```spec-requirements
- id: agent_wasm.capability_policy.decisions
  statement: Host policy shall return allow, deny, approval-required, attenuated, or unavailable decisions with stable reasons for complete versioned inputs.
  priority: must
  stability: stable
- id: agent_wasm.capability_policy.attenuation
  statement: All populated restrictions shall combine restrictively, denials shall win, and authority shall never expand through fallback or substitution.
  priority: must
  stability: stable
- id: agent_wasm.capability_policy.enforcement
  statement: Policy shall be enforced at admission, action resolution, invocation, directive validation, effect dispatch, and result admission with revocation-safe caches.
  priority: must
  stability: stable
```

## Exceptions

```spec-exceptions
- id: agent_wasm.capability_policy.implementation_frontier
  covers:
    - agent_wasm.capability_policy.decisions
    - agent_wasm.capability_policy.attenuation
    - agent_wasm.capability_policy.enforcement
  reason: Policy evaluation, attenuation, approvals, enforcement, and cache invalidation are not implemented.
```
