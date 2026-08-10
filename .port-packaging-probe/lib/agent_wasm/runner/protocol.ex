defmodule AgentWasm.Runner.Protocol do
  @version 1
  @maximum_frame_bytes 16 * 1024 * 1024

  def version, do: @version

  def request(operation) when operation in ["hello", "health", "shutdown"] do
    id = System.unique_integer([:positive, :monotonic]) |> Integer.to_string()
    payload = Jason.encode!(%{"protocol" => @version, "id" => id, "op" => operation})
    {id, payload}
  end

  def decode_response(payload) when byte_size(payload) <= @maximum_frame_bytes do
    with {:ok, response} when is_map(response) <- Jason.decode(payload),
         true <- is_binary(response["id"]),
         true <- is_boolean(response["ok"]) do
      {:ok, response}
    else
      _ -> {:error, :malformed_response}
    end
  end

  def decode_response(_payload), do: {:error, :oversized_response}
end
