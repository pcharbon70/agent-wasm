use extism_pdk::*;
use serde_json::{Value, json};

const PROTOCOL_VERSION: &str = "1.0.0";

#[plugin_fn]
pub fn describe(_input: String) -> FnResult<String> {
    Ok(json!({
        "protocol_version": PROTOCOL_VERSION,
        "manifest_version": "1.0.0",
        "actions": [],
        "routes": [],
        "state_schemas": [],
        "strategies": [],
        "required_capabilities": [],
        "required_wasm_features": [],
        "supported_protocol_versions": [PROTOCOL_VERSION]
    })
    .to_string())
}

#[plugin_fn]
pub fn initialize(input: String) -> FnResult<String> {
    let request = parse(&input)?;
    if request.pointer("/initial_config/loop_forever") == Some(&Value::Bool(true)) {
        loop_forever();
    }
    if request.pointer("/initial_config/return_timeout_error") == Some(&Value::Bool(true)) {
        return Err(WithReturnCode::new(Error::msg("timeout"), 134));
    }
    let initial_state = request
        .get("initial_config")
        .cloned()
        .unwrap_or_else(|| json!({}));

    Ok(json!({
        "protocol_version": PROTOCOL_VERSION,
        "initialization_id": required(&request, "initialization_id")?,
        "state_revision": 1,
        "initial_state": initial_state,
        "startup_directives": [],
        "diagnostics": []
    })
    .to_string())
}

#[plugin_fn]
pub fn reduce(input: String) -> FnResult<String> {
    let request = parse(&input)?;
    let expected_revision = request
        .get("agent")
        .and_then(|agent| agent.get("expected_state_revision"))
        .cloned()
        .ok_or_else(|| Error::msg("missing agent.expected_state_revision"))?;

    Ok(json!({
        "protocol_version": PROTOCOL_VERSION,
        "invocation_id": required(&request, "invocation_id")?,
        "expected_state_revision": expected_revision,
        "state_patch": null,
        "directives": [],
        "strategy_snapshot": null,
        "domain_status": {"code": "ok", "message": null, "details": null},
        "diagnostics": []
    })
    .to_string())
}

#[plugin_fn]
pub fn migrate(input: String) -> FnResult<String> {
    let request = parse(&input)?;
    let source_revision = request
        .get("source_state_revision")
        .and_then(Value::as_i64)
        .ok_or_else(|| Error::msg("missing source_state_revision"))?;

    Ok(json!({
        "protocol_version": PROTOCOL_VERSION,
        "target_schema_version": required(&request, "target_schema_version")?,
        "target_state_revision": source_revision + 1,
        "target_state": required(&request, "source_state")?,
        "migration_id": required(&request, "migration_id")?,
        "diagnostics": []
    })
    .to_string())
}

fn parse(input: &str) -> FnResult<Value> {
    Ok(serde_json::from_str(input).map_err(Error::from)?)
}

fn required<'a>(value: &'a Value, field: &str) -> FnResult<&'a Value> {
    Ok(value
        .get(field)
        .ok_or_else(|| Error::msg(format!("missing {field}")))?)
}

fn loop_forever() -> ! {
    loop {
        core::hint::spin_loop();
    }
}
