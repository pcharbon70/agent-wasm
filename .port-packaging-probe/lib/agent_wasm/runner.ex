defmodule AgentWasm.Runner do
  use GenServer

  alias AgentWasm.Runner.Protocol

  @startup_timeout 5_000
  @request_timeout 5_000

  def start_link(options) do
    GenServer.start_link(__MODULE__, options, name: Keyword.fetch!(options, :name))
  end

  def health(server \\ __MODULE__) do
    GenServer.call(server, {:request, "health"}, @request_timeout + 1_000)
  end

  @impl true
  def init(_options) do
    Process.flag(:trap_exit, true)
    path = worker_path()

    if File.regular?(path) do
      port =
        Port.open(
          {:spawn_executable, String.to_charlist(path)},
          [:binary, {:packet, 4}, :exit_status, :use_stdio]
        )

      handshake(port)
    else
      {:stop, {:worker_not_found, path}}
    end
  end

  @impl true
  def handle_call({:request, operation}, from, %{pending: nil} = state) do
    {id, payload} = Protocol.request(operation)

    if Port.command(state.port, payload) do
      timer = Process.send_after(self(), {:request_timeout, id}, @request_timeout)
      {:noreply, %{state | pending: %{id: id, from: from, timer: timer}}}
    else
      {:reply, {:error, :worker_closed}, state}
    end
  end

  def handle_call({:request, _operation}, _from, state) do
    {:reply, {:error, :worker_busy}, state}
  end

  @impl true
  def handle_info({port, {:data, payload}}, %{port: port, pending: pending} = state)
      when not is_nil(pending) do
    case Protocol.decode_response(payload) do
      {:ok, %{"id" => id, "ok" => true, "result" => result}} when id == pending.id ->
        Process.cancel_timer(pending.timer)
        GenServer.reply(pending.from, {:ok, result})
        {:noreply, %{state | pending: nil}}

      {:ok, %{"id" => id, "ok" => false, "error" => error}} when id == pending.id ->
        Process.cancel_timer(pending.timer)
        GenServer.reply(pending.from, {:error, error})
        {:noreply, %{state | pending: nil}}

      _ ->
        GenServer.reply(pending.from, {:error, :invalid_worker_response})
        {:stop, :invalid_worker_response, %{state | pending: nil}}
    end
  end

  def handle_info({:request_timeout, id}, %{pending: %{id: id} = pending} = state) do
    GenServer.reply(pending.from, {:error, :timeout})
    Port.close(state.port)
    {:stop, :worker_timeout, %{state | pending: nil}}
  end

  def handle_info({port, {:exit_status, status}}, %{port: port} = state) do
    reply_pending(state.pending, {:error, {:worker_exit, status}})
    {:stop, {:worker_exit, status}, %{state | pending: nil}}
  end

  def handle_info({:EXIT, port, reason}, %{port: port} = state) do
    reply_pending(state.pending, {:error, {:worker_exit, reason}})
    {:stop, {:worker_exit, reason}, %{state | pending: nil}}
  end

  @impl true
  def terminate(_reason, %{port: port}) when is_port(port) do
    if Port.info(port), do: Port.close(port)
    :ok
  end

  def terminate(_reason, _state), do: :ok

  defp handshake(port) do
    {id, payload} = Protocol.request("hello")
    true = Port.command(port, payload)

    receive do
      {^port, {:data, response_payload}} ->
        case Protocol.decode_response(response_payload) do
          {:ok,
           %{
             "id" => ^id,
             "ok" => true,
             "result" => %{"protocol" => protocol}
           } = response}
          when protocol == Protocol.version() ->
            {:ok, %{port: port, hello: response, pending: nil}}

          other ->
            Port.close(port)
            {:stop, {:incompatible_worker, other}}
        end

      {^port, {:exit_status, status}} ->
        {:stop, {:worker_exit_during_handshake, status}}
    after
      @startup_timeout ->
        Port.close(port)
        {:stop, :worker_handshake_timeout}
    end
  end

  defp worker_path do
    System.get_env("AGENT_WASM_RUNNER_PATH") ||
      Application.app_dir(:agent_wasm, ["priv", "runner", executable_name()])
  end

  defp executable_name do
    if match?({:win32, _}, :os.type()), do: "agent-wasm-runner.exe", else: "agent-wasm-runner"
  end

  defp reply_pending(nil, _reply), do: :ok

  defp reply_pending(pending, reply) do
    Process.cancel_timer(pending.timer)
    GenServer.reply(pending.from, reply)
  end
end
