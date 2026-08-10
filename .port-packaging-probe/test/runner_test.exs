defmodule AgentWasm.RunnerTest do
  use ExUnit.Case, async: false

  test "the packaged Port worker completes its handshake and health request" do
    assert {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health()
  end
end
