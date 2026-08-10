# syntax=docker/dockerfile:1.7

FROM rust:1.92-bookworm AS rust-build
WORKDIR /src
COPY native/agent_wasm_runner/Cargo.toml native/agent_wasm_runner/Cargo.lock ./
COPY native/agent_wasm_runner/src ./src
RUN cargo build --locked --release

FROM elixir:1.18.4-otp-27-slim AS elixir-build
ENV MIX_ENV=prod
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/* \
    && mix local.hex --force \
    && mix local.rebar --force
COPY mix.exs mix.lock ./
COPY config ./config
RUN mix deps.get --only prod && mix deps.compile
COPY lib ./lib
COPY test ./test
COPY --from=rust-build /src/target/release/agent-wasm-runner /app/priv/runner/agent-wasm-runner
RUN chmod 0755 /app/priv/runner/agent-wasm-runner \
    && MIX_ENV=test mix test \
    && MIX_ENV=prod mix compile \
    && MIX_ENV=prod mix release --overwrite \
    && _build/prod/rel/agent_wasm/bin/agent_wasm eval \
       'Application.ensure_all_started(:agent_wasm); {:ok, %{"status" => "ok"}} = AgentWasm.Runner.health()'

FROM scratch AS release-files
COPY --from=elixir-build /app/_build/prod/rel/agent_wasm /agent_wasm

FROM debian:bookworm-slim AS runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libgcc-s1 libncurses6 libssl3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system agent-wasm \
    && useradd --system --gid agent-wasm --home-dir /opt/agent-wasm agent-wasm
WORKDIR /opt/agent-wasm
COPY --from=elixir-build --chown=agent-wasm:agent-wasm /app/_build/prod/rel/agent_wasm ./
USER agent-wasm
ENTRYPOINT ["/opt/agent-wasm/bin/agent_wasm"]
CMD ["start"]
