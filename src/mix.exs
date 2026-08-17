defmodule AgentWasm.MixProject do
  use Mix.Project

  def project do
    [
      app: :agent_wasm,
      version: "0.1.0",
      elixir: "~> 1.18",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      aliases: aliases()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger]
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:jason, "~> 1.4"},
      {:spec_led_ex,
       git: "https://github.com/specleddev/specled_ex.git", only: [:dev, :test], runtime: false}
    ]
  end

  defp aliases do
    [
      "native.build": [
        "cmd cargo build --locked --manifest-path native/agent_wasm_runner/Cargo.toml",
        "cmd cargo build --locked --target wasm32-unknown-unknown --target-dir native/target/bootstrap_guest --manifest-path test/fixtures/guest_protocol/bootstrap_guest/Cargo.toml"
      ],
      test: ["native.build", "test"]
    ]
  end
end
