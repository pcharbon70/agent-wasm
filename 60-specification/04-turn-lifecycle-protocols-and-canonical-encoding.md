---
title: "Turn Lifecycle Protocols And Canonical Encoding"
kind: specification
created: "2026-08-08"
status: normative
spec_version: "1.0.0"
tags:
  - milestone-01
  - phase-04
  - protocol
  - turn
  - canonical
  - encoding
aliases:
  - "M1-P4 Turn Lifecycle"
---

# Turn Lifecycle Protocols And Canonical Encoding

## Status and authority

This chapter is a normative specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-04-turn-lifecycle-protocols-and-canonical-encoding.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It specifies the complete bytes-in/bytes-out lifecycle for description,
initialization, reduction, and migration.

Protocol version `1.0.0` replaces `0.1.0`. Adding deterministic delivery and
initialization identities and replacing the instruction wire shape are
breaking changes and therefore require this MAJOR-version increment.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 4
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Agent Manifests Artifacts Schemas And Registries](03-agent-manifests-artifacts-schemas-and-registries.md).

## Exports

> **Normative definition.**
Every conforming bootstrap artifact MUST expose all four exports below using
the Extism no-argument calling convention.
Input and output travel as byte buffers through the Extism kernel.
Each export returns `i32` zero on success or non-zero on failure.

| Export | Input type | Output type | Purpose |
| --- | --- | --- | --- |
| `describe` | `DescribeRequest` | `DescribeResponse` | Return schemas, routes, actions, strategy metadata |
| `initialize` | `InitializeRequest` | `InitializeResponse` | Calculate initial state without acquiring resources |
| `reduce` | `TurnRequest` | `TurnResult` | Process one agent turn |
| `migrate` | `MigrationRequest` | `MigrationResult` | Transform state between schema versions |

All exports accept input as JSON bytes in the Extism input buffer.
All exports return output as JSON bytes in the Extism output buffer.
Every request and response defined by this chapter MUST carry
`protocol_version: "1.0.0"`; another value is handled only by explicit version
negotiation before export invocation.

### Describe export

> **Normative definition.**
The `describe` export returns the artifact's capabilities without loading
state or executing decision logic.
The host MAY cache results indefinitely.

> **Normative definition.**

```
DescribeRequest {
  protocol_version: string
}

DescribeResponse {
  protocol_version: string,
  manifest_version: string,
  actions: ActionRef[],
  routes: RouteRef[],
  state_schemas: StateSchemaRef[],
  strategies: StrategyRef[],
  required_capabilities: CapabilityRef[],
  required_wasm_features: string[],
  supported_protocol_versions: string[]
}
```

The artifact MUST include all fields listed in the manifest.

### Initialize export

> **Normative definition.**
The `initialize` export calculates initial state and startup requests.
It MUST NOT acquire external resources, open network connections, or
perform side effects beyond computing state values.

> **Normative definition.**

```
InitializeRequest {
  protocol_version: string,
  initialization_id: string,
  agent_type: string,
  instance_id: string,
  state_schema_version: string,
  initial_config: JsonObject
}

InitializeResponse {
  protocol_version: string,
  initialization_id: string,
  state_revision: int,
  initial_state: JsonObject,
  startup_directives: Directive[],
  diagnostics: Diagnostic[]
}
```

The request `initialization_id` MUST equal the canonical initialization
identity derived from `agent_type` and `instance_id`; the response value MUST
match it. The returned state MUST conform to the declared state schema.
The state_revision MUST be 1 for a fresh initialization.
Startup directives are placed in the outbox for host processing.

### Reduce export

> **Normative definition.**
The `reduce` export processes one agent turn.
It is the primary decision boundary.
The reducer receives a value snapshot and returns a new state patch,
directives, and a strategy snapshot.

> **Normative definition.**

```
TurnRequest {
  protocol_version: string,
  invocation_id: string,
  agent: {
    type: string,
    instance_id: string,
    expected_state_revision: int
  },
  signal: SignalEnvelope,
  instruction: Instruction?,
  state: JsonObject,
  strategy_state: JsonObject?,
  runtime_context: RuntimeContext,
  grants: Grant[],
  deadline_ms: int,
  trace_context: TraceContext
}

TurnResult {
  protocol_version: string,
  invocation_id: string,
  expected_state_revision: int,
  state_patch: StatePatch?,
  directives: Directive[],
  strategy_snapshot: JsonObject?,
  domain_status: DomainStatus,
  diagnostics: Diagnostic[]
}
```

### Migrate export

> **Normative definition.**
The `migrate` export transforms state from one schema version to the next.
It operates under a separately authorized maintenance path.
The host MUST verify migration authorization before invoking this export.

> **Normative definition.**

```
MigrationRequest {
  protocol_version: string,
  source_schema_version: string,
  target_schema_version: string,
  source_state_revision: int,
  source_state: JsonObject,
  migration_id: string
}

MigrationResult {
  protocol_version: string,
  target_schema_version: string,
  target_state_revision: int,
  target_state: JsonObject,
  migration_id: string,
  diagnostics: Diagnostic[]
}
```

The returned state MUST conform to the target schema.
The migration_id MUST match the request.
Migrations are executed by the host; guest code does not commit them.
The host MUST verify source_state_revision matches the current committed revision.

## TurnRequest fields

### Invocation identity

> **Normative definition.**
The invocation_id identifies one turn of agent computation.
It MUST be the canonical monotonically increasing invocation identity defined
by
[Generation ownership](02-stable-identities-versions-errors-and-limits.md#generation-ownership).

### Agent identity

> **Normative definition.**
The agent field identifies the target agent:

- `type`: The agent type identifier (`agent:<tenant>/<name>:<version>`).
- `instance_id`: The agent instance identifier.
- `expected_state_revision`: The state revision the host loaded.
  The guest MUST NOT trust this value for authorization.

### Expected revision

> **Normative definition.**
The expected_state_revision in the TurnResult MUST match the
expected_state_revision in the TurnRequest.
This is an integrity check, not an authorization mechanism.
The host MUST verify this match before committing.

### Signal envelope

> **Normative definition.**
The signal field carries the incoming event:

> **Normative definition.**

```
SignalEnvelope {
  type: string,
  source: string,
  subject: string,
  correlation_id: string,
  causation_id: string?,
  delivery_id: string,
  timestamp: ISO 8601 (UTC),
  data: JsonObject?
}
```

The timestamp MUST use the canonical UTC representation in this chapter.
`delivery_id` MUST be the deterministic accepted-delivery identity defined by
[Transport identity](10-signals-causality-routing-and-delivery.md#transport-identity).

This is the only guest-wire `SignalEnvelope`. Chapter 10 wraps it in a
host-owned accepted-ingress record rather than extending it with duplicate
fields. For an accepted record, the host MUST construct `TurnRequest` as
follows:

- `signal` is the accepted record's `signal` value byte-for-byte.
- `runtime_context.tenant_id` and `runtime_context.principal_id` are copied
  from the accepted record's host-owned authentication context.
- `trace_context` is copied from the accepted record byte-for-byte.
- `agent.type` and `agent.instance_id` are copied from the accepted record's
  selected target agent type and instance.

The host MUST validate this projection before invoking `reduce`. A mismatched
tenant, principal, trace context, or selected target is rejected with
`protocol.semantic.context_projection_invalid`. A `delivery_id` that does not
match the accepted signal identity is rejected with
`protocol.semantic.delivery_identity_invalid`.

### Instruction

> **Normative definition.**
The instruction field is optional and carries explicit action invocations:

> **Normative definition.**

```
Instruction {
  action: ActionRef,
  arguments: JsonObject?,
  idempotency_key: string?,
  context_refs: ContextRef[],
  scheduling: Scheduling?
}

ActionRef {
  name: string,
  version: string?
}

ContextRef {
  id: string,
  source: "signal" | "state" | "directive",
  field_path: string?
}

Scheduling {
  delay_ms: int?,
  schedule_id: string?
}
```

Context references identify prior values for the action to consume.

### State and strategy state

> **Normative definition.**
The state field is the current agent state snapshot.
The strategy_state field is the current strategy snapshot (optional).
Both are read-only from the guest's perspective.

### Runtime context

> **Normative definition.**
The runtime_context field contains attenuated facts about the execution
environment.
Sensitive values MUST NOT be included.

> **Normative definition.**

```
RuntimeContext {
  tenant_id: string,
  principal_id: string?,
  turn_number: int,
  is_retry: bool
}
```

The invocation_id is not included here; it is already at the top level of TurnRequest.
`is_retry` MUST be `false` in the base protocol because an accepted signal has
one delivery attempt. Isolated conformance replay does not change this field.

### Grants

> **Normative definition.**
The grants field lists capabilities granted for this turn:

> **Normative definition.**

```
Grant {
  capability: string,
  resource: string?,
  purpose: string,
  deadline_ms: int?
}
```

The host enforces grants independently.
The guest MUST NOT rely on grants for authorization.

### Deadline

> **Normative definition.**
The deadline_ms field is a positive turn-duration ceiling in milliseconds.
It MUST NOT exceed the disclosed `time.turn_ms` implementation limit; a larger
request is rejected with `identity.limit.time.turn_ms`. For an accepted
request, `deadline_ms` is the effective turn ceiling. The host emits the same
diagnostic if execution exhausts that ceiling.
The guest SHOULD check the deadline periodically for long computations.

### Trace context

> **Normative definition.**
The trace_context field carries distributed tracing information:

> **Normative definition.**

```
TraceContext {
  trace_id: string,
  span_id: string,
  parent_span_id: string?
}
```

The host MUST pass these three values to tracing evidence unchanged. The guest
MUST NOT replace or synthesize trace identifiers.

## TurnResult fields

### State patch

> **Normative definition.**
The state_patch field is the structural update to agent state.
It is a typed patch that the host validates and applies.

> **Normative definition.**
This is the wire format returned in `TurnResult`.
The host internally converts this to the internal patch model defined in
[State Operations Patches Revisions And Conflicts](12-state-operations-patches-revisions-and-conflicts.md)
for atomic application with revision tracking and precondition enforcement.

> **Normative definition.**

```
StatePatch {
  replace?: JsonObject,
  set?: {path: string, value: JsonValue}[],
  delete?: string[],
  merge?: JsonObject
}
```

The host applies state patches in the following order:

1. `replace`: Replaces the entire state. Other patch fields are ignored.
2. `delete`: Removes the listed paths from the current state.
3. `merge`: Deep-merges the provided object into the current state.
4. `set`: Sets the value at each specified path.

If multiple patch types are present, `replace` takes priority and the other
fields are silently ignored.
The host MUST validate the resulting state against the current schema and revision.
Unknown paths, reserved namespaces, and size violations are rejected.

Deep merge recursively merges two objects by key. When both values at a key
are objects, they are merged recursively; otherwise the patch value replaces
the existing value. Arrays are values and are replaced, not concatenated.

Every `set.path` and `delete` entry MUST be the canonical JSON Pointer defined
by [Path constraints](12-state-operations-patches-revisions-and-conflicts.md#path-constraints).
The host converts the wire fields to the internal operation sequence exactly
as defined by [Patch](12-state-operations-patches-revisions-and-conflicts.md#patch).

> **Normative unspecified presentation.**
The internal patch-application strategy is bounded unspecified presentation:
the host MAY use a different order only when the resulting state is
semantically equivalent to the required order above.

### Directives

> **Normative definition.**
The directives field lists capability requests for host execution:

> **Normative definition.**

```
Directive {
  kind: string,
  id: string,
  payload: JsonObject?,
  capability: string,
  resource: string?,
  destination: string?,
  causation_id: string,
  completion_signal: CompletionSignal?,
  retry_class: RetryClass?,
  result_contract: ResultContract?
}

CompletionSignal {
  type: string,
  subject: string?,
  correlation_id: string
}

RetryClass {
  max_attempts: int,
  backoff_ms: int,
  jitter_ms: int?
}

ResultContract {
  expected_fields: string[],
  schema_version: string?
}
```

Each turn directive id MUST equal
`directive:<invocation_id>:<kind>:<zero-based-array-index>`. Each startup
directive id MUST equal
`directive:<initialization_id>:<kind>:<zero-based-array-index>`, and its
`causation_id` MUST equal the same `initialization_id`. Each turn directive's
`causation_id` MUST equal the producing `invocation_id`. Directive ids are
therefore deterministic and unique within their producing export.
Unknown directive kinds are rejected.
The completion_signal is optional and, if present, specifies how the host
should emit the result-bearing signal after the effect completes.

Before committing an initialization or turn, the host MUST validate every
directive's structure, kind, deterministic id, capability, resource,
destination, retry class, and result contract. An invalid or unauthorized
startup directive rejects the entire `InitializeResponse`; no initial state or
outbox entry is committed. An invalid or unauthorized turn directive rejects
the entire `TurnResult`; no state, journal entry, or outbox entry is committed.
Postcommit execution failure is a later effect outcome and does not revise the
committed response.

### Domain status

> **Normative definition.**
The domain_status field indicates the turn outcome:

> **Normative definition.**

```
DomainStatus {
  code: "ok" | "error" | "partial" | "terminal",
  message: string?,
  details: JsonObject?
}
```

| Code | Meaning |
| --- | --- |
| `ok` | Reducer processing completed successfully; the state patch and every validated directive are eligible for one atomic commit. |
| `error` | Turn failed. No state change committed. |
| `partial` | Domain logic intentionally produced an incomplete but valid result; every emitted directive still passed precommit validation and commits atomically with the state patch. |
| `terminal` | Agent has reached a final state. No further turns will be processed for this instance. |

`domain_status` describes reducer and precommit validation outcome only. It
MUST NOT predict or incorporate postcommit directive execution. A malformed,
unknown, or unauthorized directive makes the entire turn invalid and commits
no state, journal, or outbox entry.

Terminal status indicates the agent has reached a final state.
The host SHOULD record terminal status durably.

## Diagnostics

> **Normative definition.**
Diagnostics are structured error and status reports emitted by the host or
guest during protocol execution.
Every diagnostic contains the following fields:

> **Normative definition.**

```
Diagnostic {
  family: string,
  code: string,
  severity: "error" | "warning" | "info",
  message: string,
  details: JsonObject?
}
```

| Field | Type | Description |
| --- | --- | --- |
| `family` | `string` | Diagnostic family code (e.g., `protocol.decode`, `identity.limit`). |
| `code` | `string` | Specific diagnostic code within the family. |
| `severity` | `string` | `error`, `warning`, or `info`. |
| `message` | `string` | Human-readable description. Must not expose secrets. |
| `details` | `JsonObject?` | Optional additional context. |

### Diagnostic family codes

> **Normative definition.**
The following diagnostic family codes are defined:

| Family | Description |
| --- | --- |
| `protocol.decode` | JSON decode failures. |
| `protocol.schema` | Schema validation failures. |
| `protocol.semantic` | Semantic validation failures. |
| `protocol.encode` | Canonical encoding failures. |
| `identity.limit` | Named implementation-limit exhaustion defined by the identity and limits contract. |
| `protocol.cancel` | Cancellation requested. |

### Diagnostic codes

> **Normative definition.**
The following diagnostic codes are defined:

| Family | Code | Description |
| --- | --- | --- |
| `protocol.decode` | `syntax_error` | Invalid JSON syntax. |
| `protocol.decode` | `utf8_error` | Invalid UTF-8 sequence. |
| `protocol.decode` | `duplicate_key` | Duplicate object keys. |
| `protocol.decode` | `number_format` | Number is outside the finite binary64 or exact safe-integer domain. |
| `protocol.decode` | `string_escape` | Invalid string escape sequence. |
| `protocol.decode` | `non_canonical` | Input bytes do not equal their canonical re-encoding. |
| `protocol.schema` | `missing_required` | Required field missing. |
| `protocol.schema` | `type_mismatch` | Field type does not match schema. |
| `protocol.schema` | `format_invalid` | Field format does not match pattern. |
| `protocol.schema` | `size_exceeded` | Field size exceeds maximum. |
| `protocol.semantic` | `causation_invalid` | Causation reference invalid. |
| `protocol.semantic` | `context_projection_invalid` | Turn context does not match its accepted-ingress record. |
| `protocol.semantic` | `delivery_identity_invalid` | Delivery identity does not match the tenant-scoped signal identity. |
| `protocol.semantic` | `duration_invalid` | Duration ceiling is zero or negative. |
| `protocol.semantic` | `revision_stale` | State revision out of order. |
| `identity.limit` | `input.max_bytes` | Input size exceeds the effective ceiling. |
| `identity.limit` | `output.max_bytes` | Output size exceeds the effective ceiling. |
| `identity.limit` | `collection.max_items` | Collection size exceeds the effective ceiling. |
| `identity.limit` | `string.max_length` | String length exceeds the effective ceiling. |
| `protocol.encode` | `non_canonical` | Output not in canonical form. |
| `identity.limit` | `time.turn_ms` | Effective turn-duration ceiling exceeded. |
| `protocol.cancel` | `requested` | Cancellation requested. |

## Canonical JSON encoding

### General rules

> **Normative definition.**
All protocol messages use Canonical JSON encoding.
Canonical JSON is defined by the following rules:

1. **Keys sorted lexicographically.** Object keys are sorted by Unicode
   code point order.

2. **Unique finite-number encoding.** Numbers use the shortest decimal form
   that round-trips to the same IEEE 754 binary64 value under round-to-nearest,
   ties-to-even. Integers are represented without decimal points, `-0` is
   encoded as `0`, exponent markers use lowercase `e`, exponent plus signs are
   omitted, and fractional or exponent leading and trailing zeros are removed.
   If decimal and exponent forms have equal length, the decimal form is used.

3. **No leading zeros.** Numbers do not have leading zeros (except `0`
   itself).

4. **UTF-8 encoding.** Strings are UTF-8 encoded.

5. **No duplicate keys.** Object keys MUST be unique.

6. **No BOM.** No byte order mark is prepended.

7. **No comments.** JSON comments are not permitted.

8. **No trailing commas.** Trailing commas in arrays or objects are
   not permitted.

### Number representation

> **Normative definition.**
Numbers in Canonical JSON follow these rules:

| Type | Representation | Example |
| --- | --- | --- |
| Integer | No decimal point; magnitude at most `9007199254740991` | `42`, `-7`, `0` |
| Decimal | No trailing zeros | `3.14`, `0.5`, `-0.25` |
| Scientific | Lowercase `e`, no plus sign or redundant zeros | `1.5e10`, `2e-3` |
| Infinity/NaN | Not permitted | Rejected |
| Leading zeros | Not permitted | `007` rejected |

Every decoded JSON number MUST decode to a finite binary64 value without
overflow. Integer-valued fields MUST remain within the exact binary64 safe
integer range `[-9007199254740991, 9007199254740991]`, even when their schema
uses a wider source-language type. Values outside that domain are rejected with
`protocol.decode.number_format`.

### String representation

> **Normative definition.**
Strings in Canonical JSON follow these rules:

- UTF-8 encoded without BOM.
- Control characters MUST use six-byte `\u00xx` escapes with lowercase
  hexadecimal digits (`\u0000` through `\u001f`); short control escapes such
  as `\n` are not canonical.
- Quote and backslash MUST use the short escapes `\"` and `\\`.
- Forward slash MUST NOT be escaped.
- Non-control Unicode scalar values MUST be emitted directly as UTF-8 and
  MUST NOT use `\u` escapes.
- Unpaired surrogate code points are invalid.

### Identifier representation

> **Normative definition.**
Identifiers in Canonical JSON follow these rules:

- Identifiers are strings.
- Identifiers are case-sensitive.
- Identifiers MUST NOT contain leading or trailing whitespace.
- Identifiers MUST NOT contain control characters.

### Timestamp representation

> **Normative definition.**
Timestamps in Canonical JSON follow ISO 8601 format:

- Format: `YYYY-MM-DDTHH:MM:SSZ` for whole seconds or
  `YYYY-MM-DDTHH:MM:SS.sssZ` otherwise.
- Timezone MUST be UTC (Z suffix).
- Fractional seconds, when present, contain exactly three decimal digits.
- Sub-millisecond precision is rejected.
- No space between date and time.

### Ordering

> **Normative definition.**
Object keys are sorted lexicographically by Unicode code point.
Arrays preserve insertion order.

### Duplicate key rejection

> **Normative definition.**
Duplicate keys in objects are rejected at decode time.
The decoder MUST return a `protocol.decode.duplicate_key` diagnostic.

### Unknown field rejection

> **Normative definition.**
Every base-protocol structure rejects unknown fields. Silent fallback is
unsafe for protocol inputs and outputs.

This includes:

- `TurnRequest`
- `TurnResult`
- `DescribeResponse`
- `InitializeRequest`
- `InitializeResponse`
- `RuntimeContext`
- `Directive`
- `StatePatch`
- `MigrationRequest`
- `MigrationResult`

## Validation order

> **Normative definition.**
Protocol message validation proceeds in the following order.
Rejection at any step HALTS further validation.

1. **Decode:** Parse JSON, check syntax, validate UTF-8.
2. **Schema validation:** Check field types, required fields, format.
3. **Semantic validation:** Check values, constraints, ranges.
4. **Output-size enforcement:** Check output buffer size limits.
5. **Canonical re-encoding:** Re-encode output and compare to verify
   canonical form.

### Decode

> **Normative definition.**
The decoder MUST:

- Parse JSON according to RFC 8259.
- Reject invalid UTF-8 sequences.
- Reject duplicate keys.
- Reject numbers outside the JSON number range.
- Reject strings with invalid escape sequences.
- Reject a numeric token that decodes outside the finite binary64 or safe
  integer domain with `protocol.decode.number_format`.
- Canonically re-encode the decoded input and reject every other byte
  difference, including a non-shortest numeric spelling, with
  `protocol.decode.non_canonical`.

### Schema validation

> **Normative definition.**
The schema validator MUST:

- Check that every required field is present.
- Check field types match the schema.
- Check string formats (URLs, emails, identifiers).
- Check numeric ranges (min, max, exclusive).
- Check array/object sizes (minItems, maxItems, minProperties, maxProperties).
- Check pattern matches (regex).

### Semantic validation

> **Normative definition.**
The semantic validator MUST:

- Check field values against business rules.
- Check referenced identifiers exist.
- Check causal relationships (`causation_id` references a prior invocation or
  accepted delivery identity).
- Recompute `delivery_id` from the accepted record's tenant and signal fields
  and require an exact match.
- Require the tenant, principal, trace context, and selected target projection
  to match the persisted accepted-ingress record.
- Check duration ceilings are positive and do not exceed their governing
  implementation limit.
- Check state revisions are monotonically increasing.
- Check timestamps are in UTC (Z suffix).

### Output-size enforcement

> **Normative definition.**
The output validator MUST:

- Check output buffer size against `output.max_bytes`.
- Reject outputs that exceed the limit.
- Return an `identity.limit.output.max_bytes` diagnostic.

### Canonical re-encoding

> **Normative definition.**
The canonical encoder MUST:

- Re-encode the output using Canonical JSON rules.
- Compare the re-encoded output to the original output.
- If they differ, the output is not canonical.
- Reject the output and return a `protocol.encode.non_canonical` diagnostic.

## Fixed encoding and protocol choices and deferred work

### Fixed encoding and protocol choices

| Choice | Fixed selection |
| --- | --- |
| Number encoding | Shortest round-tripping finite binary64 decimal |
| Timestamp granularity | Whole seconds or exactly three millisecond digits |
| Invocation identity | Host-owned monotonic canonical identity |
| State patch merge | Fixed recursive object merge; arrays and non-objects replace |
| Directive identity | Producing invocation or initialization plus kind and array index |
| Trace context propagation | Input fields are propagated unchanged; guests do not synthesize replacements |
| Output buffer size | Effective disclosed `output.max_bytes` implementation limit |
| Canonical re-encoding | Reject non-canonical output |

### Deferred work

| Item | Target | Reason |
| --- | --- | --- |
| Binary encoding (MessagePack, CBOR) | Milestone 8 | Performance optimization; complements artifact compression in [Agent Manifests](03-agent-manifests-artifacts-schemas-and-registries.md) |
| Streaming for large outputs | Milestone 8 | Large-state agents; relates to Memory64 large-state runtime memory in [Profile Vocabulary](01-profile-vocabulary-and-architectural-boundaries.md) |
| Async protocol support | Milestone 6 | Multi-agent coordination |
| Protocol version negotiation | Milestone 5 | Dynamic capability discovery |
| Compression for large payloads | Milestone 8 | Bandwidth optimization; relates to artifact compression in [Agent Manifests](03-agent-manifests-artifacts-schemas-and-registries.md) |
| Protocol fuzzing corpus | Milestone 8 | Robustness testing |

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter:

1. Canonical JSON is insufficient for large state payloads; binary encoding
   is required for performance.
2. Synchronous exports cannot handle long-running computations; async
   protocol is required.
3. Monotonic invocation identities cannot be retained across migration;
   a versioned identity revision is required.
4. The fixed recursive merge cannot represent a required collection update;
   an explicit new patch operation is required.
5. Output buffer limits are too restrictive for large agent states;
    streaming is required; addressed by Streaming for large outputs and Compression for large payloads, both deferred to
    [Milestone 8](#deferred-work) in this file.

> **Non-normative note.**
> All items deferred to Milestone 8 fall under
> Milestone 8 - Portability, Verification, And Performance
> (planning document at `.spec/planning/agentic-system/milestone-08-portability-verification-and-performance/README.md`).
> The Milestone 8 boundary principle: Milestone 8 addresses portability,
> verification, and performance of the system as built by Milestones 1-7.
> Milestone 9 addresses production platform, developer experience, and
> operational tooling built on top of that verified system.

## Integration Test Expectations

This section defines the observable behavior that the Phase 4 integration
tests MUST verify.
These expectations are normative; passing the test suite is a prerequisite
for promoting this chapter to `status: normative`.

### Successful flow

The host MUST execute all four exports correctly and return canonical JSON
output.
The test MUST verify that:

1. `describe` returns all declared capabilities with correct field types.
2. `initialize` echoes the canonical initialization identity, returns revision
   1, and produces valid initial state conforming to the schema.
3. `reduce` processes one turn and returns a valid TurnResult.
4. `migrate` transforms state correctly and returns target schema state.
5. All outputs are canonical JSON (keys sorted, no trailing zeros, etc.).
6. State revisions are monotonically increasing.
7. Invocation IDs are unique within the agent instance.
8. Directive ids match their producing invocation or initialization identity,
   kind, and zero-based array index; every directive `causation_id` matches the
   same producer identity.
9. Accepted-ingress records project to byte-identical signal and trace values
   and matching tenant, principal, and target fields in `TurnRequest`.

### Malformed messages

The host MUST reject messages that fail to decode.
The test MUST verify that:

1. Invalid JSON syntax is rejected with a `protocol.decode.syntax_error` diagnostic.
2. Invalid UTF-8 is rejected with a `protocol.decode.utf8_error` diagnostic.
3. Duplicate keys are rejected with a `protocol.decode.duplicate_key` diagnostic.
4. Numbers with trailing zeros are rejected with a
   `protocol.decode.non_canonical` diagnostic.
5. Strings with invalid escape sequences are rejected.

### Incompatible messages

The host MUST reject messages with incompatible versions or fields.
The test MUST verify that:

1. Messages with unsupported protocol versions are rejected.
2. Messages with unknown fields in authoritative structures are rejected.
3. Messages with invalid field types are rejected.
4. Messages with missing required fields are rejected.
5. A result containing any invalid or unauthorized directive is rejected with
   no state, journal, or outbox commit.
6. A missing or mismatched `delivery_id` is rejected with
   `protocol.semantic.delivery_identity_invalid`.
7. Any mismatch between an accepted-ingress record and its projected tenant,
   principal, trace, or target field is rejected with
   `protocol.semantic.context_projection_invalid` before guest invocation.

### Stale messages

The host MUST detect and reject stale messages.
The test MUST verify that:

1. Messages with out-of-order state revisions are rejected.
2. Messages with non-positive duration ceilings or ceilings above the
   governing implementation limit are rejected.
3. Messages with invalid causal relationships are rejected.

### Duplicate messages

The host MUST deduplicate messages according to their delivery contract.
The test MUST verify that:

1. Duplicate invocations with the same invocation_id are identified.
2. No duplicate state revisions are created.
3. No duplicate outbox entries are created.

### Boundary-limit messages

The host MUST enforce message size limits.
The test MUST verify that:

1. Messages exceeding `input.max_bytes` are rejected with
   `identity.limit.input.max_bytes`.
2. Outputs exceeding `output.max_bytes` are rejected with a
   `identity.limit.output.max_bytes` diagnostic.
3. Arrays exceeding `collection.max_items` are rejected with
   `identity.limit.collection.max_items`.
4. Strings exceeding `string.max_length` are rejected with
   `identity.limit.string.max_length`.

### Timeout and cancellation

The host MUST enforce time limits during message processing.
The test MUST verify that:

1. Exports exceeding their effective duration ceiling are interrupted with
   `identity.limit.time.turn_ms`.
2. No partial state is committed for timed-out exports.
3. Cancellation during export execution is handled gracefully.

### Canonical encoding

The host MUST verify that outputs are canonical JSON.
The test MUST verify that:

1. Object keys are sorted lexicographically.
2. Numbers have no trailing zeros.
3. Strings use the unique escaping and direct UTF-8 rules.
4. No duplicate keys in outputs.
5. Re-encoding produces identical output.
6. Alternate Unicode escapes, short control escapes, exponent spellings, and
   negative zero are rejected as non-canonical.

### Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.

## Variability register

This register summarizes the governing clauses linked below; it does not
define or redeclare permitted variation.

> **Non-normative note.**

| Clause | Type | Selection |
| --- | --- | --- |
| Export signatures | Required | Four exports fixed by this chapter |
| [Initialization identity](#initialize-export) | Required | Request and response use one canonical initialization identity; startup directive ids and causation derive from it |
| TurnRequest fields | Required | Fields fixed by this chapter |
| [Accepted-signal projection](#signal-envelope) | Required | One guest `SignalEnvelope`; host metadata maps to existing turn fields without duplication |
| [Runtime retry flag](#runtime-context) | Required | `false` in the single-attempt base protocol |
| TurnResult fields | Required | Fields fixed by this chapter |
| Canonical JSON rules | Required | Rules fixed by this chapter |
| Number representation | Required | Rules fixed by this chapter |
| String representation | Required | Rules fixed by this chapter |
| Identifier representation | Required | Rules fixed by this chapter |
| Timestamp representation | Required | ISO 8601 UTC |
| Duplicate key rejection | Required | Reject at decode time |
| Unknown field rejection | Required | Reject in every base-protocol structure |
| Validation order | Required | 5-step order fixed by this chapter |
| [Describe result caching](#describe-export) | MAY | Cached bytes remain subject to current artifact identity and validation policy |
| [Deadline polling](#deadline) | SHOULD | Guests periodically check long computations; the host always enforces the limit |
| [Patch conversion and application](#state-patch) | Required with unspecified internal presentation | JSON Pointer conversion and semantic order are fixed; only equivalent internal machinery may vary |
| [Terminal-status persistence](#domain-status) | SHOULD | Record terminal status durably |
| [Canonical number and timestamp encoding](#fixed-encoding-and-protocol-choices) | Required | Fixed binary64 and millisecond rules |
| [Producer and directive identities](#fixed-encoding-and-protocol-choices) | Required | Initialization or invocation producer plus kind and array position |
| [State patch merge](#state-patch) | Required | Recursive object merge; arrays and non-objects replace |
| [Trace propagation](#trace-context) | Required | Propagate input identifiers unchanged |
| [Input and output ceilings](02-stable-identities-versions-errors-and-limits.md#limit-categories) | Implementation limit | Effective ceilings disclosed in conformance profile |
| [Canonical re-encoding](#canonical-re-encoding) | Required | Reject non-canonical output |

## Rationale and evidence (non-normative)

This chapter derives from the turn protocol requirements identified in
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md)
and the operational needs of a multi-tenant, multi-agent system.

The four-export model (`describe`, `initialize`, `reduce`, `migrate`)
provides a clean separation of concerns:

- `describe` enables host-side capability discovery without execution.
- `initialize` calculates initial state without side effects.
- `reduce` is the primary decision boundary for one turn.
- `migrate` handles state version upgrades under separate authorization.

Canonical JSON encoding ensures:

- Deterministic serialization for testing and debugging.
- Stable identity for content-addressed storage.
- Predictable parsing behavior across runtime families.

The validation order ensures:

- Early rejection of malformed messages.
- Schema conformance before semantic checks.
- Output integrity through canonical re-encoding.
