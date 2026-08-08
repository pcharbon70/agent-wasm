---
title: "Turn Lifecycle Protocols And Canonical Encoding"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
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

This chapter is a draft specification produced by
[Phase 4](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-04-turn-lifecycle-protocols-and-canonical-encoding.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It specifies the complete bytes-in/bytes-out lifecycle for description,
initialization, reduction, and migration.

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
All four exports follow the Extism no-argument calling convention.
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
  agent_type: string,
  state_schema_version: string,
  initial_config: JsonObject
}

InitializeResponse {
  protocol_version: string,
  state_revision: int,
  initial_state: JsonObject,
  startup_directives: Directive[],
  diagnostics: Diagnostic[]
}
```

The returned state MUST conform to the declared state schema.
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
It MUST be unique within the agent instance and SHOULD be a UUID v4
or monotonic counter.

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
  timestamp: ISO 8601 (UTC),
  data: JsonObject?
}
```

The timestamp MUST be in UTC (Z suffix per ISO 8601).

### Instruction

> **Normative definition.**
The instruction field is optional and carries explicit action invocations:

> **Normative definition.**

```
Instruction {
  action: string,
  parameters: JsonObject,
  idempotency_key: string?,
  context_refs: ContextRef[]
}

ContextRef {
  id: string,
  type: "state" | "signal" | "directive"
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
The deadline_ms field is the wall-clock deadline for the turn in
milliseconds.
The host enforces this deadline.
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

## TurnResult fields

### State patch

> **Normative definition.**
The state_patch field is the structural update to agent state.
It is a typed patch that the host validates and applies.

> **Normative definition.**

```
StatePatch {
  replace?: JsonObject,
  set?: {path: string, value: JsonValue}[],
  delete?: string[],
  merge?: JsonObject
}
```

> **Normative implementation-defined choice.**
The host applies state patches in the following order:

1. `replace`: Replaces the entire state. Other patch fields are ignored.
2. `delete`: Removes the listed paths from the current state.
3. `merge`: Deep-merges the provided object into the current state.
4. `set`: Sets the value at each specified path.

If multiple patch types are present, `replace` takes priority and the other
fields are silently ignored.
The host MUST validate the resulting state against the current schema and revision.
Unknown paths, reserved namespaces, and size violations are rejected.

> **Normative unspecified presentation.**
The host MAY apply patches in a different order if the resulting state is
semantically equivalent.

### Directives

> **Normative definition.**
The directives field lists capability requests for host execution:

> **Normative definition.**

```
Directive {
  kind: string,
  id: string,
  payload: JsonObject,
  capability: string,
  resource: string?,
  causation_id: string,
  completion_signal: CompletionSignal?
}

CompletionSignal {
  type: string,
  subject: string?,
  correlation_id: string
}
```

Each directive MUST have a unique id within the turn.
Unknown directive kinds are rejected.
The completion_signal is optional and, if present, specifies how the host
should emit the result-bearing signal after the effect completes.

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
| `ok` | Turn completed successfully. State patch applied, all directives processed. |
| `error` | Turn failed. No state change committed. |
| `partial` | Turn completed but some directives failed or were rejected. State patch applied; failed directives are recorded in diagnostics. |
| `terminal` | Agent has reached a final state. No further turns will be processed for this instance. |

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
| `family` | `string` | Diagnostic family code (e.g., `protocol.decode`, `protocol.limit`). |
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
| `protocol.limit` | Resource limit violations. |
| `protocol.encode` | Canonical encoding failures. |
| `protocol.timeout` | Deadline exceeded. |
| `protocol.cancel` | Cancellation requested. |

### Diagnostic codes

> **Normative definition.**
The following diagnostic codes are defined:

| Family | Code | Description |
| --- | --- | --- |
| `protocol.decode` | `syntax_error` | Invalid JSON syntax. |
| `protocol.decode` | `utf8_error` | Invalid UTF-8 sequence. |
| `protocol.decode` | `duplicate_key` | Duplicate object keys. |
| `protocol.decode` | `number_format` | Invalid number representation. |
| `protocol.decode` | `string_escape` | Invalid string escape sequence. |
| `protocol.schema` | `missing_required` | Required field missing. |
| `protocol.schema` | `type_mismatch` | Field type does not match schema. |
| `protocol.schema` | `format_invalid` | Field format does not match pattern. |
| `protocol.schema` | `size_exceeded` | Field size exceeds maximum. |
| `protocol.semantic` | `causation_invalid` | Causation reference invalid. |
| `protocol.semantic` | `deadline_expired` | Deadline in the past. |
| `protocol.semantic` | `revision_stale` | State revision out of order. |
| `protocol.limit` | `input_exceeded` | Input size exceeds limit. |
| `protocol.limit` | `output_exceeded` | Output size exceeds limit. |
| `protocol.limit` | `collection_exceeded` | Collection size exceeds limit. |
| `protocol.limit` | `string_exceeded` | String length exceeds limit. |
| `protocol.encode` | `non_canonical` | Output not in canonical form. |
| `protocol.timeout` | `turn_exceeded` | Turn deadline exceeded. |
| `protocol.cancel` | `requested` | Cancellation requested. |

## Canonical JSON encoding

## Canonical JSON encoding

### General rules

> **Normative definition.**
All protocol messages use Canonical JSON encoding.
Canonical JSON is defined by the following rules:

1. **Keys sorted lexicographically.** Object keys are sorted by Unicode
   code point order.

2. **No trailing zeros in numbers.** Integers are represented without
   decimal points. Decimals are represented without trailing zeros.

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
| Integer | No decimal point | `42`, `-7`, `0` |
| Decimal | No trailing zeros | `3.14`, `0.5`, `-0.25` |
| Scientific | Allowed | `1.5e10`, `2.0e-3` |
| Infinity/NaN | Not permitted | Rejected |
| Leading zeros | Not permitted | `007` rejected |

### String representation

> **Normative definition.**
Strings in Canonical JSON follow these rules:

- UTF-8 encoded without BOM.
- Control characters MUST be escaped (`\u0000` through `\u001F`).
- Quote, backslash, and forward slash MUST be escaped.
- Unicode characters above U+001F MAY be represented as-is or escaped.
- No surrogate pairs unless representing valid Unicode code points.

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

- Format: `YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DDTHH:MM:SS.sssZ`
- Timezone MUST be UTC (Z suffix).
- Fractional seconds are optional.
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
Unknown fields in authoritative structures are rejected by default.
Silent fallback is unsafe for authority-bearing requests.

The following structures reject unknown fields:

- `TurnRequest`
- `TurnResult`
- `Directive`
- `StatePatch`
- `MigrationRequest`
- `MigrationResult`

The following structures MAY accept unknown fields for backward compatibility:

- `DescribeResponse` (host MAY ignore unknown fields)
- `RuntimeContext` (host MAY ignore unknown fields)

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

### Schema validation

> **Normative definition.**
The schema validator MUST:

- Check all REQUIRED fields are present.
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
- Check causal relationships (causation_id references a prior invocation).
- Check deadlines are in the future.
- Check state revisions are monotonically increasing.
- Check timestamps are in UTC (Z suffix).

### Output-size enforcement

> **Normative definition.**
The output validator MUST:

- Check output buffer size against `output.max_bytes`.
- Reject outputs that exceed the limit.
- Return a `protocol.limit.output_exceeded` diagnostic.

### Canonical re-encoding

> **Normative definition.**
The canonical encoder MUST:

- Re-encode the output using Canonical JSON rules.
- Compare the re-encoded output to the original output.
- If they differ, the output is not canonical.
- Return a `protocol.encode.non_canonical` diagnostic.

## Implementation-defined choices and deferred work

### Implementation-defined choices

| Choice | Domain | Required documentation |
| --- | --- | --- |
| Number precision | Encoding | Decimal precision and rounding policy |
| Timestamp granularity | Encoding | Millisecond or microsecond precision |
| Identifier generation | TurnRequest | UUID v4, counter, or hybrid |
| State patch merge strategy | TurnResult | Deep merge, shallow merge, or replace |
| Directive id generation | TurnResult | Deterministic hash or random UUID |
| Trace context propagation | TurnRequest | W3C Trace Context or custom format |
| Output buffer size limit | Validation | Default and override mechanism |
| Canonical re-encoding strictness | Validation | Reject non-canonical or warn |

### Deferred work

| Item | Target | Reason |
| --- | --- | --- |
| Binary encoding (MessagePack, CBOR) | Milestone 8 | Performance optimization |
| Streaming for large outputs | Milestone 8 | Large-state agents |
| Async protocol support | Milestone 6 | Multi-agent coordination |
| Protocol version negotiation | Milestone 5 | Dynamic capability discovery |
| Compression for large payloads | Milestone 8 | Bandwidth optimization |
| Protocol fuzzing corpus | Milestone 8 | Robustness testing |

### Potential invalidation of earlier assumptions

The following results from later phases would invalidate an assumption in
this chapter:

1. Canonical JSON is insufficient for large state payloads; binary encoding
   is required for performance.
2. Synchronous exports cannot handle long-running computations; async
   protocol is required.
3. UUID generation is too costly for high-throughput deployments;
   counter-based IDs are required.
4. State patch merge is ambiguous for nested structures; explicit merge
   strategy is required.
5. Output buffer limits are too restrictive for large agent states;
   streaming is required.

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
2. `initialize` returns valid initial state conforming to the schema.
3. `reduce` processes one turn and returns a valid TurnResult.
4. `migrate` transforms state correctly and returns target schema state.
5. All outputs are canonical JSON (keys sorted, no trailing zeros, etc.).
6. State revisions are monotonically increasing.
7. Invocation IDs are unique within the agent instance.

### Malformed messages

The host MUST reject messages that fail to decode.
The test MUST verify that:

1. Invalid JSON syntax is rejected with a `protocol.decode.syntax_error` diagnostic.
2. Invalid UTF-8 is rejected with a `protocol.decode.utf8_error` diagnostic.
3. Duplicate keys are rejected with a `protocol.decode.duplicate_key` diagnostic.
4. Numbers with trailing zeros are rejected with a `protocol.decode.number_format` diagnostic.
5. Strings with invalid escape sequences are rejected.

### Incompatible messages

The host MUST reject messages with incompatible versions or fields.
The test MUST verify that:

1. Messages with unsupported protocol versions are rejected.
2. Messages with unknown fields in authoritative structures are rejected.
3. Messages with invalid field types are rejected.
4. Messages with missing required fields are rejected.

### Stale messages

The host MUST detect and reject stale messages.
The test MUST verify that:

1. Messages with out-of-order state revisions are rejected.
2. Messages with expired deadlines are rejected.
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

1. Messages exceeding `input.max_bytes` are rejected.
2. Outputs exceeding `output.max_bytes` are rejected with a
   `protocol.limit.output_exceeded` diagnostic.
3. Arrays exceeding `collection.max_items` are rejected.
4. Strings exceeding `string.max_length` are rejected.

### Timeout and cancellation

The host MUST enforce time limits during message processing.
The test MUST verify that:

1. Exports exceeding their deadline are interrupted.
2. No partial state is committed for timed-out exports.
3. Cancellation during export execution is handled gracefully.

### Canonical encoding

The host MUST verify that outputs are canonical JSON.
The test MUST verify that:

1. Object keys are sorted lexicographically.
2. Numbers have no trailing zeros.
3. Strings are properly escaped.
4. No duplicate keys in outputs.
5. Re-encoding produces identical output.

### Cross-milestone fixture regression

The test suite MUST include fixtures from earlier milestones that are
affected by this phase.
Any regression MUST be recorded with its approval status.

## Variability register

| Clause | Type | Selection |
| --- | --- | --- |
| Export signatures | Required | Four exports fixed by this chapter |
| TurnRequest fields | Required | Fields fixed by this chapter |
| TurnResult fields | Required | Fields fixed by this chapter |
| Canonical JSON rules | Required | Rules fixed by this chapter |
| Number representation | Required | Rules fixed by this chapter |
| String representation | Required | Rules fixed by this chapter |
| Identifier representation | Required | Rules fixed by this chapter |
| Timestamp representation | Required | ISO 8601 UTC |
| Duplicate key rejection | Required | Reject at decode time |
| Unknown field rejection | Required | Reject for authoritative structures |
| Validation order | Required | 5-step order fixed by this chapter |
| Number precision | Implementation-defined | Documented in conformance profile |
| Timestamp granularity | Implementation-defined | Documented in conformance profile |
| Identifier generation | Implementation-defined | Documented in conformance profile |
| State patch merge strategy | Implementation-defined | Documented in conformance profile |
| Directive id generation | Implementation-defined | Documented in conformance profile |
| Trace context propagation | Implementation-defined | Documented in conformance profile |
| Output buffer size limit | Implementation-defined | Documented in conformance profile |
| Canonical re-encoding strictness | Implementation-defined | Documented in conformance profile |

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
