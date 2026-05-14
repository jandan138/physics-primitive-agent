from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.contracts import CompileConfig


def load_compile_config(path: str | Path) -> CompileConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("compile config must be a mapping")

    asset_path = _nested_required(data, ("asset", "path"), "missing required config key: asset.path")
    task = _nested_required(data, ("task", "primary"), "missing required config key: task.primary")
    compile_section = data.get("compile", {})
    if compile_section is None:
        compile_section = {}
    if not isinstance(compile_section, dict):
        raise ValueError("compile config key compile must be a mapping")

    allowed_fallback = compile_section.get("allowed_fallback", ("coacd", "sdf"))
    return CompileConfig(
        asset_path=str(asset_path),
        task=str(task),
        method=str(compile_section.get("method", "primitive_first")),
        max_primitives=int(compile_section.get("max_primitives", 16)),
        allowed_fallback=tuple(str(item) for item in allowed_fallback),
    )


def _nested_required(data: dict[str, Any], keys: tuple[str, str], message: str) -> Any:
    section = data.get(keys[0])
    if not isinstance(section, dict) or keys[1] not in section:
        raise ValueError(message)
    value = section[keys[1]]
    if value in (None, ""):
        raise ValueError(message)
    return value
