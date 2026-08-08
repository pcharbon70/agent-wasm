---
title: "Guest SDK Contracts Fixtures And Milestone Acceptance"
kind: specification
created: "2026-08-08"
status: draft
spec_version: "0.1.0"
tags:
  - milestone-01
  - phase-05
  - sdk
  - fixture
  - conformance
  - acceptance
aliases:
  - "M1-P5 Guest SDK And Milestone Acceptance"
---

# Guest SDK Contracts Fixtures And Milestone Acceptance

## Status and authority

This chapter is a draft specification produced by
[Phase 5](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/phase-05-guest-sdk-contracts-fixtures-and-milestone-acceptance.md)
of
[Milestone 1](../.spec/planning/agentic-system/milestone-01-contracts-profiles-and-artifacts/README.md)
--
Contracts, Profiles, And Artifacts.
It turns the protocol into language-neutral fixtures and guest SDK
responsibilities without choosing initial SDK languages.

This chapter is normative by default within its stated scope.
Material visibly marked non-normative does not create conformance
obligations.
Promotion to `status: normative` requires evidence from the Phase 5
integration tests and a passing cross-milestone fixture run.

Governing policies:
[Specification Authority](../SPECIFICATION-AUTHORITY.md)
and
[Conformance Vocabulary](../CONFORMANCE-VOCABULARY.md).

Related chapters:
[Profile Vocabulary And Architectural Boundaries](01-profile-vocabulary-and-architectural-boundaries.md),
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md).

## Guest SDK responsibilities

### Export lowering

> **Normative definition.**
A guest SDK MUST implement the lowering of each protocol export to the
Extism no-argument calling convention.
Lowering is the transformation from the SDK's idiomatic function signature
to the `fn() -> i32` export expected by the Extism kernel.

Each exported function MUST:

1. Decode input bytes from the Extism input buffer using the canonical codec.
2. Invoke the idiomatic implementation.
3. Encode the response using the canonical codec.
4. Write the encoded bytes to the Extism output buffer.
5. Return `i32` zero on success or non-zero on failure.

> **Normative definition.**

```
GuestSDK {
  describe(request: DescribeRequest) -> DescribeResponse,
  initialize(request: InitializeRequest) -> InitializeResponse,
  reduce(request: TurnRequest) -> TurnResult,
  migrate(request: MigrationRequest) -> MigrationResult
}
```

### Extism memory exchange

> **Normative definition.**
The guest SDK MUST use the Extism kernel's input/output/error bookkeeping
for all memory exchange.
The SDK MUST NOT allocate or free memory directly.

> **Normative definition.**

```
MemoryExchange {
  input_set(input_offset: i32, input_length: i32) -> void,
  output_set(output_offset: i32, output_length: i32) -> void,
  error_set(error_offset: i32, error_length: i32) -> void,
  input_get() -> (offset: i32, length: i32),
  output_get() -> (offset: i32, length: i32),
  error_get() -> (offset: i32, length: i32)
}
```

The SDK MUST call `input_set` before invoking the export.
The SDK MUST call `output_set` after encoding the response.
The SDK MUST call `error_set` if the export fails.

### Canonical codec

> **Normative definition.**
The guest SDK MUST implement a canonical JSON codec that conforms to the
rules defined in
[Canonical JSON encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#canonical-json-encoding).

The codec MUST:

- Sort object keys lexicographically.
- Represent numbers without trailing zeros.
- Represent strings with proper escaping.
- Reject duplicate keys at decode time.
- Reject numbers outside the JSON number range.

> **Normative definition.**

```
CanonicalCodec {
  encode(value: JsonValue) -> bytes,
  decode(input: bytes) -> JsonValue
}
```

### Diagnostics

> **Normative definition.**
The guest SDK MAY emit diagnostics during export execution.
Diagnostics MUST conform to the `Diagnostic` type defined in
[Turn Lifecycle Protocols And Canonical Encoding](04-turn-lifecycle-protocols-and-canonical-encoding.md#diagnostics).

The guest MUST NOT emit diagnostics that expose secrets or implementation
internal state.
The host MAY filter or redact diagnostics before recording them.

> **Normative definition.**

```
GuestDiagnostic {
  family: string,
  code: string,
  severity: "error" | "warning" | "info",
  message: string
}
```

### Test-fixture loading

> **Normative definition.**
The guest SDK MAY provide test-fixture loading utilities for SDK
development and conformance testing.
Test fixtures are external to the protocol and do not create conformance
obligations.

> **Normative definition.**

```
TestFixtureLoader {
  load(fixture_path: string) -> TestFixture,
  fixtures: TestFixture[]
}

TestFixture {
  name: string,
  description: string,
  export: string,
  input: bytes,
  expected_output: bytes?,
  expected_error_category: string?,
  expected_error_code: string?,
  profile: string?,
  artifact_metadata: JsonObject?
}
```

## Positive fixtures

### Describe fixture

> **Normative definition.**
The describe positive fixture validates that the artifact returns all
declared capabilities without loading state or executing decision logic.

> **Normative definition.**

```
TestFixture {
  name: "describe_positive",
  description: "Artifact returns all declared capabilities",
  export: "describe",
  input: {
    protocol_version: "0.1.0"
  },
  expected_output: {
    protocol_version: "0.1.0",
    manifest_version: "0.1.0",
    actions: [ActionRef],
    routes: [RouteRef],
    state_schemas: [StateSchemaRef],
    strategies: [StrategyRef],
    required_capabilities: [CapabilityRef],
    required_wasm_features: [],
    supported_protocol_versions: ["0.1.0"]
  },
  expected_error_category: null,
  expected_error_code: null
}
```

### Initialize fixture

> **Normative definition.**
The initialize positive fixture validates that the artifact calculates
initial state without acquiring external resources.

> **Normative definition.**

```
TestFixture {
  name: "initialize_positive",
  description: "Artifact calculates initial state",
  export: "initialize",
  input: {
    protocol_version: "0.1.0",
    agent_type: "agent:test/chatbot:1.0.0",
    state_schema_version: "1.0.0",
    initial_config: {}
  },
  expected_output: {
    protocol_version: "0.1.0",
    state_revision: 1,
    initial_state: {
      counter: 0,
      status: "idle"
    },
    startup_directives: [],
    diagnostics: []
  },
  expected_error_category: null,
  expected_error_code: null
}
```

### Direct reduce fixture

> **Normative definition.**
The direct reduce positive fixture validates that the reducer processes
one turn correctly and returns a valid TurnResult.

> **Normative definition.**

```
TestFixture {
  name: "reduce_direct_positive",
  description: "Reducer processes direct instruction",
  export: "reduce",
  input: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:1",
    agent: {
      type: "agent:test/chatbot:1.0.0",
      instance_id: "u-1",
      expected_state_revision: 1
    },
    signal: {
      type: "api.request",
      source: "principal:test/svc:1",
      subject: "chatbot",
      correlation_id: "corr-1",
      causation_id: null,
      timestamp: "2026-08-08T00:00:00Z",
      data: null
    },
    instruction: {
      action: "increment",
      parameters: {},
      idempotency_key: null,
      context_refs: []
    },
    state: {
      counter: 0,
      status: "idle"
    },
    strategy_state: null,
    runtime_context: {
      tenant_id: "test",
      principal_id: "principal:test/svc:1",
      turn_number: 1,
      is_retry: false
    },
    grants: [],
    deadline_ms: 5000,
    trace_context: {
      trace_id: "trace-1",
      span_id: "span-1",
      parent_span_id: null
    }
  },
  expected_output: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:1",
    expected_state_revision: 1,
    state_patch: {
      set: [
        {path: "/counter", value: 1}
      ]
    },
    directives: [],
    strategy_snapshot: null,
    domain_status: {
      code: "ok",
      message: null,
      details: null
    },
    diagnostics: []
  },
  expected_error_category: null,
  expected_error_code: null
}
```

### FSM continuation fixture

> **Normative definition.**
The FSM continuation positive fixture validates that the reducer processes
a result-bearing instruction continuation correctly.

> **Normative definition.**

```
TestFixture {
  name: "reduce_fsm_continuation_positive",
  description: "Reducer processes FSM continuation",
  export: "reduce",
  input: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:2",
    agent: {
      type: "agent:test/chatbot:1.0.0",
      instance_id: "u-1",
      expected_state_revision: 2
    },
    signal: {
      type: "effect.result",
      source: "host",
      subject: "directive:inv:test/chatbot/u-1:1:effect:0",
      correlation_id: "corr-2",
      causation_id: "inv:test/chatbot/u-1:1",
      timestamp: "2026-08-08T00:00:01Z",
      data: {
        result: "success",
        value: 42
      }
    },
    instruction: null,
    state: {
      counter: 1,
      status: "processing"
    },
    strategy_state: {
      fsm_state: "waiting_for_result",
      fsm_transitions: [
        {from: "waiting_for_result", to: "complete", on: "effect.result"}
      ]
    },
    runtime_context: {
      tenant_id: "test",
      principal_id: "principal:test/svc:1",
      turn_number: 2,
      is_retry: false
    },
    grants: [],
    deadline_ms: 5000,
    trace_context: {
      trace_id: "trace-1",
      span_id: "span-2",
      parent_span_id: "span-1"
    }
  },
  expected_output: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:2",
    expected_state_revision: 2,
    state_patch: {
      set: [
        {path: "/status", value: "complete"},
        {path: "/result_value", value: 42}
      ]
    },
    directives: [],
    strategy_snapshot: {
      fsm_state: "complete",
      fsm_transitions: [
        {from: "waiting_for_result", to: "complete", on: "effect.result"}
      ]
    },
    domain_status: {
      code: "ok",
      message: null,
      details: null
    },
    diagnostics: []
  },
  expected_error_category: null,
  expected_error_code: null
}
```

### Terminal result fixture

> **Normative definition.**
The terminal result positive fixture validates that the reducer returns
a terminal domain status correctly.

> **Normative definition.**

```
TestFixture {
  name: "reduce_terminal_positive",
  description: "Reducer returns terminal domain status",
  export: "reduce",
  input: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:3",
    agent: {
      type: "agent:test/chatbot:1.0.0",
      instance_id: "u-1",
      expected_state_revision: 3
    },
    signal: {
      type: "api.request",
      source: "principal:test/svc:1",
      subject: "chatbot",
      correlation_id: "corr-3",
      causation_id: "inv:test/chatbot/u-1:2",
      timestamp: "2026-08-08T00:00:02Z",
      data: null
    },
    instruction: {
      action: "complete",
      parameters: {},
      idempotency_key: null,
      context_refs: []
    },
    state: {
      counter: 2,
      status: "complete",
      result_value: 42
    },
    strategy_state: null,
    runtime_context: {
      tenant_id: "test",
      principal_id: "principal:test/svc:1",
      turn_number: 3,
      is_retry: false
    },
    grants: [],
    deadline_ms: 5000,
    trace_context: {
      trace_id: "trace-1",
      span_id: "span-3",
      parent_span_id: "span-2"
    }
  },
  expected_output: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:3",
    expected_state_revision: 3,
    state_patch: null,
    directives: [],
    strategy_snapshot: null,
    domain_status: {
      code: "terminal",
      message: "Agent completed successfully",
      details: null
    },
    diagnostics: []
  },
  expected_error_category: null,
  expected_error_code: null
}
```

### Migration fixture

> **Normative definition.**
The migration positive fixture validates that the migrate export transforms
state correctly between schema versions.

> **Normative definition.**

```
TestFixture {
  name: "migrate_positive",
  description: "Artifact migrates state between schema versions",
  export: "migrate",
  input: {
    protocol_version: "0.1.0",
    source_schema_version: "1.0.0",
    target_schema_version: "2.0.0",
    source_state_revision: 1,
    source_state: {
      counter: 0,
      status: "idle"
    },
    migration_id: "mig-1"
  },
  expected_output: {
    protocol_version: "0.1.0",
    target_schema_version: "2.0.0",
    target_state_revision: 1,
    target_state: {
      counter: 0,
      status: "idle",
      version: "2.0.0"
    },
    migration_id: "mig-1",
    diagnostics: []
  },
  expected_error_category: null,
  expected_error_code: null
}
```

## Negative fixtures

### Malformed JSON fixture

> **Normative definition.**
The malformed JSON negative fixture validates that the host rejects
invalid JSON syntax with a `protocol.decode.syntax_error` diagnostic.

> **Normative definition.**

```
TestFixture {
  name: "decode_malformed_json",
  description: "Host rejects malformed JSON",
  export: "reduce",
  input: "invalid json {{{{",
  expected_output: null,
  expected_error_category: "protocol.decode",
  expected_error_code: "syntax_error",
  profile: "bootstrap",
  artifact_metadata: null
}
```

### Schema mismatch fixture

> **Normative definition.**
The schema mismatch negative fixture validates that the host rejects
inputs that violate the declared state schema.

> **Normative definition.**

```
TestFixture {
  name: "schema_mismatch",
  description: "Host rejects state violating schema",
  export: "reduce",
  input: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:1",
    agent: {
      type: "agent:test/chatbot:1.0.0",
      instance_id: "u-1",
      expected_state_revision: 1
    },
    signal: {
      type: "api.request",
      source: "principal:test/svc:1",
      subject: "chatbot",
      correlation_id: "corr-1",
      causation_id: null,
      timestamp: "2026-08-08T00:00:00Z",
      data: null
    },
    instruction: {
      action: "increment",
      parameters: {},
      idempotency_key: null,
      context_refs: []
    },
    state: {
      counter: "not_a_number",
      status: "idle"
    },
    strategy_state: null,
    runtime_context: {
      tenant_id: "test",
      principal_id: "principal:test/svc:1",
      turn_number: 1,
      is_retry: false
    },
    grants: [],
    deadline_ms: 5000,
    trace_context: {
      trace_id: "trace-1",
      span_id: "span-1",
      parent_span_id: null
    }
  },
  expected_output: null,
  expected_error_category: "protocol.schema",
  expected_error_code: "type_mismatch",
  profile: "bootstrap",
  artifact_metadata: null
}
```

### Duplicate keys fixture

> **Normative definition.**
The duplicate keys negative fixture validates that the host rejects
inputs with duplicate object keys.

> **Normative definition.**

```
TestFixture {
  name: "duplicate_keys",
  description: "Host rejects inputs with duplicate keys",
  export: "reduce",
  input: {
    "protocol_version": "0.1.0",
    "protocol_version": "0.2.0",
    "invocation_id": "inv:test/chatbot/u-1:1",
    "agent": {
      "type": "agent:test/chatbot:1.0.0",
      "instance_id": "u-1",
      "expected_state_revision": 1
    },
    "signal": {
      "type": "api.request",
      "source": "principal:test/svc:1",
      "subject": "chatbot",
      "correlation_id": "corr-1",
      "causation_id": null,
      "timestamp": "2026-08-08T00:00:00Z",
      "data": null
    },
    "instruction": {
      "action": "increment",
      "parameters": {},
      "idempotency_key": null,
      "context_refs": []
    },
    "state": {
      "counter": 0,
      "status": "idle"
    },
    "strategy_state": null,
    "runtime_context": {
      "tenant_id": "test",
      "principal_id": "principal:test/svc:1",
      "turn_number": 1,
      "is_retry": false
    },
    "grants": [],
    "deadline_ms": 5000,
    "trace_context": {
      "trace_id": "trace-1",
      "span_id": "span-1",
      "parent_span_id": null
    }
  },
  expected_output: null,
  expected_error_category: "protocol.decode",
  expected_error_code: "duplicate_key",
  profile: "bootstrap",
  artifact_metadata: null
}
```

### Stale version fixture

> **Normative definition.**
The stale version negative fixture validates that the host rejects
inputs with out-of-order state revisions.

> **Normative definition.**

```
TestFixture {
  name: "stale_version",
  description: "Host rejects stale state revision",
  export: "reduce",
  input: {
    protocol_version: "0.1.0",
    invocation_id: "inv:test/chatbot/u-1:1",
    agent: {
      type: "agent:test/chatbot:1.0.0",
      instance_id: "u-1",
      expected_state_revision: 5
    },
    signal: {
      type: "api.request",
      source: "principal:test/svc:1",
      subject: "chatbot",
      correlation_id: "corr-1",
      causation_id: null,
      timestamp: "2026-08-08T00:00:00Z",
      data: null
    },
    instruction: {
      action: "increment",
      parameters: {},
      idempotency_key: null,
      context_refs: []
    },
    state: {
      counter: 0,
      status: "idle"
    },
    strategy_state: null,
    runtime_context: {
      tenant_id: "test",
      principal_id: "principal:test/svc:1",
      turn_number: 1,
      is_retry: false
    },
    grants: [],
    deadline_ms: 5000,
    trace_context: {
      trace_id: "trace-1",
      span_id: "span-1",
      parent_span_id: null
    }
  },
  expected_output: null,
  expected_error_category: "protocol.semantic",
  expected_error_code: "revision_stale",
  profile: "bootstrap",
  artifact_metadata: null
}
```

### Oversized value fixture

> **Normative definition.**
The oversized value negative fixture validates that the host rejects
inputs that exceed resource limits.
### Fixture manifest

> **Normative definition.**
A fixture manifest binds each fixture to its expected canonical input,
output, error category, profile, and artifact metadata.
The manifest is the single source of truth for fixture conformance.

> **Normative definition.**

```
FixtureManifest {
  fixtures: TestFixture[],
  schema_version: "1.0.0",
  created: "2026-08-08T00:00:00Z"
}
```

### SDK conformance

> **Normative definition.**
SDK conformance is determined by compiled-artifact behavior, not source-level
unit-test success.
A conformance run executes each fixture against the compiled guest artifact
and verifies the observed output matches the expected output.

Conformance criteria:

- All positive fixtures MUST produce the expected output.
- All negative fixtures MUST produce the expected error category and code.
- All fixtures MUST complete within the deadline_ms specified in the fixture.
- All fixtures MUST leave no unauthorized or partial state.

### Milestone 1 exit report

> **Normative definition.**
The Milestone 1 exit report documents the profile, schema, fixture, and
unresolved-variability inventories.
It is produced at the end of Phase 5 and serves as evidence for milestone
acceptance.

The exit report MUST include:

- Profile inventory: list of all profiles defined and their capabilities.
- Schema inventory: list of all state schemas defined and their versions.
- Fixture inventory: list of all fixtures and their conformance status.
- Unresolved variability: list of any implementation-defined choices or
  deferred work that could not be resolved during Milestone 1.

> **Normative definition.**

```
Milestone1ExitReport {
  profile_inventory: ProfileInventory,
  schema_inventory: SchemaInventory,
  fixture_inventory: FixtureInventory,
  unresolved_variability: UnresolvedVariability[],
  produced_at: "2026-08-08T00:00:00Z"
}
```
