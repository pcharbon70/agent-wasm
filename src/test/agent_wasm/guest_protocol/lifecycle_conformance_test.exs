defmodule AgentWasm.GuestProtocol.LifecycleConformanceTest do
  use ExUnit.Case, async: false

  alias AgentWasm.Invocation.PortWorker

  # covers: agent_wasm.guest_protocol.exports

  @wasm_path Path.expand(
               "../../../native/target/bootstrap_guest/wasm32-unknown-unknown/debug/bootstrap_guest.wasm",
               __DIR__
             )

  test "compiled no-WASI guest exposes the four-function lifecycle ABI" do
    assert {:ok, describe} = invoke("describe", %{"protocol_version" => "1.0.0"})
    assert describe["protocol_version"] == "1.0.0"
    assert describe["supported_protocol_versions"] == ["1.0.0"]

    initialization_id = "initialization:counter:00000000-0000-4000-8000-000000000001"

    assert {:ok, initialized} =
             invoke("initialize", %{
               "protocol_version" => "1.0.0",
               "initialization_id" => initialization_id,
               "agent_type" => "agent:test/counter:1.0.0",
               "instance_id" => "00000000-0000-4000-8000-000000000001",
               "state_schema_version" => "1.0.0",
               "initial_config" => %{"counter" => 0}
             })

    assert initialized == %{
             "protocol_version" => "1.0.0",
             "initialization_id" => initialization_id,
             "state_revision" => 1,
             "initial_state" => %{"counter" => 0},
             "startup_directives" => [],
             "diagnostics" => []
           }

    invocation_id = "invocation:00000000-0000-4000-8000-000000000001:0000000000000001"

    assert {:ok, reduced} =
             invoke("reduce", %{
               "protocol_version" => "1.0.0",
               "invocation_id" => invocation_id,
               "agent" => %{
                 "type" => "agent:test/counter:1.0.0",
                 "instance_id" => "00000000-0000-4000-8000-000000000001",
                 "expected_state_revision" => 1
               },
               "signal" => %{},
               "instruction" => nil,
               "state" => %{"counter" => 0},
               "strategy_state" => nil,
               "runtime_context" => %{},
               "grants" => [],
               "deadline_ms" => 1_000,
               "trace_context" => %{}
             })

    assert reduced["invocation_id"] == invocation_id
    assert reduced["expected_state_revision"] == 1
    assert reduced["domain_status"]["code"] == "ok"

    migration_id = "migration:counter:1.0.0:2.0.0"

    assert {:ok, migrated} =
             invoke("migrate", %{
               "protocol_version" => "1.0.0",
               "source_schema_version" => "1.0.0",
               "target_schema_version" => "2.0.0",
               "source_state_revision" => 1,
               "source_state" => %{"counter" => 0},
               "migration_id" => migration_id
             })

    assert migrated["migration_id"] == migration_id
    assert migrated["target_schema_version"] == "2.0.0"
    assert migrated["target_state_revision"] == 2
    assert migrated["target_state"] == %{"counter" => 0}
  end

  test "the private worker rejects exports outside the lifecycle" do
    assert {:error, %{code: "port.export.unsupported"}} =
             PortWorker.invoke("unknown", %{}, wasm_path: @wasm_path)
  end

  test "reduce rejects a non-positive effective duration ceiling" do
    assert {:error, %{code: "protocol.semantic.duration_invalid"}} =
             PortWorker.invoke("reduce", %{"deadline_ms" => 0}, wasm_path: @wasm_path)
  end

  test "reduce rejects a duration ceiling above the configured limit" do
    assert {:error, %{code: "identity.limit.time.turn_ms"}} =
             PortWorker.invoke("reduce", %{deadline_ms: 51},
               wasm_path: @wasm_path,
               timeout: 50
             )
  end

  test "the Port boundary rejects a timeout above its implementation limit" do
    assert {:error, %{code: "port.timeout.invalid"}} =
             PortWorker.invoke("describe", %{}, wasm_path: @wasm_path, timeout: 60_001)
  end

  test "a guest error message cannot spoof host timeout exhaustion" do
    assert {:error, %{code: "extism.invocation.failed"}} =
             PortWorker.invoke(
               "initialize",
               %{"initial_config" => %{"return_timeout_error" => true}},
               wasm_path: @wasm_path
             )
  end

  test "the one-shot worker interrupts guest execution at the effective duration ceiling" do
    started_at = System.monotonic_time(:millisecond)

    assert {:error, %{code: "identity.limit.time.turn_ms"}} =
             PortWorker.invoke(
               "initialize",
               %{
                 "protocol_version" => "1.0.0",
                 "initialization_id" =>
                   "initialization:counter:00000000-0000-4000-8000-000000000001",
                 "agent_type" => "agent:test/counter:1.0.0",
                 "instance_id" => "00000000-0000-4000-8000-000000000001",
                 "state_schema_version" => "1.0.0",
                 "initial_config" => %{"loop_forever" => true}
               },
               wasm_path: @wasm_path,
               timeout: 50
             )

    elapsed = System.monotonic_time(:millisecond) - started_at
    assert elapsed >= 25
    assert elapsed < 1_500

    assert {:ok, %{"protocol_version" => "1.0.0"}} =
             invoke("describe", %{"protocol_version" => "1.0.0"})
  end

  defp invoke(export, input) do
    PortWorker.invoke(export, input, wasm_path: @wasm_path)
  end
end
