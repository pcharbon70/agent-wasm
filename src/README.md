# AgentWasm

AgentWasm is an Elixir/OTP host for portable WebAssembly agents. Native Extism
and Wasmtime execution stays behind a private framed Port; the public product
surface remains on the BEAM.

The current executable slice demonstrates the four-function bootstrap guest ABI
(`describe`, `initialize`, `reduce`, and `migrate`) with a compiled no-WASI Rust
fixture. It also exercises a one-shot worker that bounds artifact loading,
instance creation, and guest execution with one total-invocation deadline.
Complete message contracts, canonical encoding, failure atomicity, and other
specification areas remain implementation frontiers and are not claimed as
conformant.

## Development

Build the native worker and compiled fixture, then run the conformance test:

```bash
mix deps.get
mix native.build
mix test test/agent_wasm/guest_protocol/lifecycle_conformance_test.exs --trace
```
