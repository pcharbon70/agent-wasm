defmodule AgentWasm.MixProject do
  use Mix.Project

  def project do
    [
      app: :agent_wasm,
      version: "0.1.0",
      elixir: "~> 1.18",
      start_permanent: Mix.env() == :prod,
      deps: [{:jason, "~> 1.4"}],
      releases: [agent_wasm: [include_executables_for: [:unix]]]
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {AgentWasm.Application, []}
    ]
  end
end
