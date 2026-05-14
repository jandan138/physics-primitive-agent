from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.contracts import CompileConfig


def load_compile_config(path: str | Path) -> CompileConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ValueError(f"config file not found: {config_path}")

    try:
        raw_text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"could not read config file: {config_path}: {exc}") from exc

    try:
        data = yaml.safe_load(raw_text) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse config file: {config_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("compile config must be a mapping")

    asset_path = _nested_required(data, ("asset", "path"), "missing required config key: asset.path")
    asset_id = _nested_optional(data, ("asset", "id")) or Path(str(asset_path)).stem
    task = _nested_required(data, ("task", "primary"), "missing required config key: task.primary")
    compile_section = data.get("compile", {})
    if compile_section is None:
        compile_section = {}
    if not isinstance(compile_section, dict):
        raise ValueError("compile config key compile must be a mapping")

    allowed_fallback = _string_tuple(
        compile_section.get("allowed_fallback", ("coacd", "sdf")),
        "compile.allowed_fallback must be a list of strings",
    )
    verify = _string_tuple(
        compile_section.get("verify", ("drop", "stack", "sphere_rain")),
        "compile.verify must be a list of strings",
    )
    return CompileConfig(
        asset_path=str(asset_path),
        task=str(task),
        asset_id=str(asset_id),
        method=str(compile_section.get("method", "primitive_first")),
        max_primitives=int(compile_section.get("max_primitives", 16)),
        allowed_fallback=allowed_fallback,
        verify=verify,
        keep_visual=bool(compile_section.get("keep_visual", True)),
        protocol=_protocol_sections(data),
    )


def _nested_required(data: dict[str, Any], keys: tuple[str, str], message: str) -> Any:
    section = data.get(keys[0])
    if not isinstance(section, dict) or keys[1] not in section:
        raise ValueError(message)
    value = section[keys[1]]
    if value in (None, ""):
        raise ValueError(message)
    return value


def _nested_optional(data: dict[str, Any], keys: tuple[str, str]) -> Any:
    section = data.get(keys[0])
    if not isinstance(section, dict):
        return None
    value = section.get(keys[1])
    if value in (None, ""):
        return None
    return value


def _string_tuple(value: Any, message: str) -> tuple[str, ...]:
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError(message)

    result = tuple(str(item) for item in value)
    if not result or any(not item for item in result):
        raise ValueError(message)
    return result


def _protocol_sections(data: dict[str, Any]) -> dict[str, Any]:
    return {
        key: data[key]
        for key in ("phase0_defaults", "report", "cpd_like", "newton", "newton_diagnostic")
        if key in data and data[key] is not None
    }
