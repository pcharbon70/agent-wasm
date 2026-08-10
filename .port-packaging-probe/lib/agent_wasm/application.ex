defmodule AgentWasm.Application do
  use Application

  @impl true
  def start(_type, _args) do
    Supervisor.start_link(
      [{AgentWasm.Runner, name: AgentWasm.Runner}],
      strategy: :one_for_one,
      name: AgentWasm.Supervisor
    )
  end
end
