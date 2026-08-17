defmodule AgentWasm.Invocation.PortWorker do
  @moduledoc """
  Private framed Port boundary for invoking an Extism guest export.

  Each invocation receives a fresh native worker and Extism instance. The
  worker uses four-byte big-endian packet framing and never enables WASI.
  """

  @exports ~w(describe initialize reduce migrate)
  @default_timeout 5_000
  @max_timeout 60_000
  @transport_grace 1_000
  @timeout_exit_status 124
  @max_request_bytes 8 * 1024 * 1024

  @type diagnostic :: %{required(:code) => String.t(), required(:message) => String.t()}

  @spec invoke(String.t(), map(), keyword()) :: {:ok, map()} | {:error, diagnostic()}
  def invoke(export, input, options \\ [])

  def invoke(export, input, options) when is_binary(export) and is_map(input) do
    timeout = Keyword.get(options, :timeout, @default_timeout)
    runner_path = Keyword.get(options, :runner_path, default_runner_path())
    wasm_path = Keyword.get(options, :wasm_path)

    with :ok <- validate_export(export),
         :ok <- validate_timeout(timeout),
         {:ok, effective_timeout} <- effective_timeout(export, input, timeout),
         :ok <- require_file(runner_path, "port.runner.unavailable"),
         :ok <- require_file(wasm_path, "port.guest.unavailable"),
         {:ok, input_json} <- Jason.encode(input),
         {:ok, request} <- encode_request(export, input_json, wasm_path, effective_timeout),
         :ok <- validate_request_size(request) do
      call_port(runner_path, request, effective_timeout + @transport_grace)
    end
  end

  def invoke(_export, _input, _options) do
    {:error, diagnostic("port.request.invalid", "export must be a string and input a map")}
  end

  @spec default_runner_path() :: String.t()
  def default_runner_path do
    Application.app_dir(
      :agent_wasm,
      "../../../../native/agent_wasm_runner/target/debug/agent_wasm_runner"
    )
  end

  defp validate_export(export) do
    if export in @exports do
      :ok
    else
      {:error, diagnostic("port.export.unsupported", "unsupported guest export: #{export}")}
    end
  end

  defp validate_timeout(timeout)
       when is_integer(timeout) and timeout > 0 and timeout <= @max_timeout,
       do: :ok

  defp validate_timeout(_timeout) do
    {:error,
     diagnostic(
       "port.timeout.invalid",
       "timeout must be a positive integer no greater than #{@max_timeout}"
     )}
  end

  defp effective_timeout("reduce", input, timeout) do
    case {Map.fetch(input, "deadline_ms"), Map.fetch(input, :deadline_ms)} do
      {{:ok, _deadline}, {:ok, _duplicate}} ->
        {:error, diagnostic("port.request.invalid", "deadline_ms is duplicated")}

      {{:ok, deadline}, :error} ->
        validate_deadline(deadline, timeout)

      {:error, {:ok, deadline}} ->
        validate_deadline(deadline, timeout)

      {:error, :error} ->
        {:ok, timeout}
    end
  end

  defp effective_timeout(_export, _input, timeout), do: {:ok, timeout}

  defp validate_deadline(deadline, timeout)
       when is_integer(deadline) and deadline > 0 and deadline <= timeout do
    {:ok, deadline}
  end

  defp validate_deadline(deadline, timeout)
       when is_integer(deadline) and deadline > timeout do
    {:error,
     diagnostic(
       "identity.limit.time.turn_ms",
       "deadline_ms exceeds the configured turn-duration ceiling"
     )}
  end

  defp validate_deadline(_deadline, _timeout) do
    {:error,
     diagnostic("protocol.semantic.duration_invalid", "deadline_ms must be a positive integer")}
  end

  defp require_file(path, code) when is_binary(path) do
    if File.regular?(path) do
      :ok
    else
      {:error, diagnostic(code, "required executable or artifact does not exist")}
    end
  end

  defp require_file(_path, code), do: {:error, diagnostic(code, "required path is missing")}

  defp encode_request(export, input_json, wasm_path, timeout) do
    Jason.encode(%{
      "operation" => "invoke",
      "wasm_path" => Path.expand(wasm_path),
      "export" => export,
      "input" => input_json,
      "timeout_ms" => timeout
    })
  end

  defp validate_request_size(request) when byte_size(request) <= @max_request_bytes, do: :ok

  defp validate_request_size(_request) do
    {:error, diagnostic("port.request.exhausted", "encoded request exceeds the Port limit")}
  end

  defp call_port(runner_path, request, timeout) do
    port =
      Port.open({:spawn_executable, runner_path}, [
        :binary,
        :exit_status,
        :hide,
        :use_stdio,
        {:packet, 4}
      ])

    try do
      if Port.command(port, request) do
        receive do
          {^port, {:data, response}} ->
            decode_response(response)

          {^port, {:exit_status, @timeout_exit_status}} ->
            {:error,
             diagnostic(
               "identity.limit.time.turn_ms",
               "guest invocation exceeded its effective duration ceiling"
             )}

          {^port, {:exit_status, status}} ->
            {:error,
             diagnostic("port.runner.failed", "native worker exited with status #{status}")}
        after
          timeout ->
            {:error, diagnostic("port.runner.timeout", "native worker did not return a response")}
        end
      else
        {:error, diagnostic("port.runner.failed", "native worker rejected the request")}
      end
    after
      close_port(port)
    end
  rescue
    error in [ArgumentError, ErlangError] ->
      {:error, diagnostic("port.runner.unavailable", Exception.message(error))}
  end

  defp close_port(port) do
    if Port.info(port) != nil, do: Port.close(port)
  rescue
    ArgumentError -> :ok
  end

  defp decode_response(response) do
    case Jason.decode(response) do
      {:ok, %{"ok" => true, "output" => output}} when is_binary(output) ->
        case Jason.decode(output) do
          {:ok, value} when is_map(value) ->
            {:ok, value}

          _error ->
            {:error, diagnostic("port.output.invalid", "guest output is not a JSON object")}
        end

      {:ok, %{"ok" => false, "error" => %{"code" => code, "message" => message}}}
      when is_binary(code) and is_binary(message) ->
        {:error, diagnostic(code, message)}

      _error ->
        {:error,
         diagnostic("port.response.invalid", "native worker returned an invalid response")}
    end
  end

  defp diagnostic(code, message), do: %{code: code, message: message}
end
