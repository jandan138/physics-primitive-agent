from __future__ import annotations

from collections import Counter
import os
from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.assets.usd_smoke import (
    _sha256_file,
    inspect_usd_asset,
    load_asset_manifest,
    resolve_asset_path,
)


def build_asset_materialization_report(
    manifest_path: str | Path,
    *,
    mirror_root: str | Path | None = None,
) -> dict[str, object]:
    manifest_id = _manifest_id(manifest_path)
    assets = load_asset_manifest(manifest_path)
    mirror_base = _mirror_root(mirror_root) / _safe_component(manifest_id, "manifest_id")
    reports = [
        materialize_asset(asset, mirror_base=mirror_base)
        for asset in assets
    ]
    statuses = [str(report["status"]) for report in reports]
    if not reports:
        status = "no_assets"
    elif any(_failed_status(status) for status in statuses):
        status = "failed"
    elif any(status != "materialized" for status in statuses):
        status = "materialized_with_warnings"
    else:
        status = "materialized"
    return {
        "stage": "asset_materialization",
        "status": status,
        "manifest": str(manifest_path),
        "manifest_id": manifest_id,
        "mirror_root": str(mirror_base),
        "assets": reports,
    }


def materialize_asset(asset: dict[str, Any], *, mirror_base: Path) -> dict[str, object]:
    role = str(asset.get("role", "unknown"))
    safe_role = _safe_component_or_none(role)
    if safe_role is None:
        return _failed_asset_report(role=role, status="unsafe_asset_role", detail=role)

    raw_source_path = asset.get("source_path") or asset.get("path")
    if not raw_source_path:
        return _failed_asset_report(role=role, status="missing_asset_path", detail="missing source_path/path")

    resolved = resolve_asset_path(
        {
            "path": raw_source_path,
            "sha256": asset.get("source_sha256") or asset.get("sha256") or "",
        }
    )
    source_path = Path(resolved.path)
    if not source_path.exists():
        return _failed_asset_report(
            role=role,
            status="missing_source_asset",
            detail=str(source_path),
            source_path=str(source_path),
        )
    if not source_path.is_file():
        return _failed_asset_report(
            role=role,
            status="source_asset_not_file",
            detail=str(source_path),
            source_path=str(source_path),
        )

    source_hash_report = _source_hash_report(source_path, resolved.expected_sha256)
    if source_hash_report["status"] not in {"matched", "not_configured"}:
        return {
            "role": role,
            "status": source_hash_report["status"],
            "source_path": str(source_path),
            "local_path": "",
            "source_hash": source_hash_report,
            "dependency_summary": _empty_dependency_summary(),
            "local_file_summary": _empty_local_file_summary(),
            "unresolved_dependencies": [],
        }

    destination_dir = mirror_base / safe_role
    destination_dir.mkdir(parents=True, exist_ok=True)
    dependency_summary = _dependency_summary(source_path)

    localize_result = False
    localize_error = ""
    try:
        from pxr import UsdUtils

        localize_result = bool(UsdUtils.LocalizeAsset(str(source_path), str(destination_dir)))
    except Exception as exc:
        localize_error = f"{type(exc).__name__}: {exc}"

    local_path = destination_dir / source_path.name
    if not local_path.exists() or not local_path.is_file():
        return {
            "role": role,
            "status": "failed",
            "source_path": str(source_path),
            "local_path": str(local_path),
            "localize_result": localize_result,
            "localize_error": localize_error,
            "dependency_summary": dependency_summary,
            "local_file_summary": _local_file_summary(destination_dir),
            "unresolved_dependencies": dependency_summary["unresolved_dependencies"],
        }

    local_sha256 = _sha256_file(local_path)
    local_asset = {
        "role": role,
        "local_path": str(local_path),
        "local_sha256": local_sha256,
        "source_path": str(source_path),
    }
    local_open_report = inspect_usd_asset(local_asset).to_dict()
    unresolved = dependency_summary["unresolved_dependencies"]
    unknown_unresolved = [
        dependency
        for dependency in unresolved
        if not _allowed_unresolved_dependency(str(dependency))
    ]
    if unknown_unresolved:
        status = "failed_unresolved_dependencies"
    elif unresolved:
        status = "materialized_with_unresolved_dependencies"
    elif localize_result:
        status = "materialized"
    else:
        status = "materialized_with_warnings"
    return {
        "role": role,
        "status": status,
        "source_path": str(source_path),
        "local_path": str(local_path),
        "local_sha256": local_sha256,
        "source_hash": source_hash_report,
        "localize_result": localize_result,
        "localize_error": localize_error,
        "dependency_summary": dependency_summary,
        "local_file_summary": _local_file_summary(destination_dir),
        "unresolved_dependencies": unresolved,
        "unknown_unresolved_dependencies": unknown_unresolved,
        "local_open_report": local_open_report,
    }


def _source_hash_report(source_path: Path, expected_sha256: str) -> dict[str, str]:
    if not expected_sha256:
        return {"status": "not_configured", "expected_sha256": "", "actual_sha256": ""}
    try:
        actual_sha256 = _sha256_file(source_path)
    except OSError as exc:
        return {
            "status": "source_hash_read_error",
            "expected_sha256": expected_sha256,
            "actual_sha256": "",
            "detail": f"{type(exc).__name__}: {exc}",
        }
    if actual_sha256 != expected_sha256:
        return {
            "status": "source_hash_mismatch",
            "expected_sha256": expected_sha256,
            "actual_sha256": actual_sha256,
        }
    return {
        "status": "matched",
        "expected_sha256": expected_sha256,
        "actual_sha256": actual_sha256,
    }


def _dependency_summary(source_path: Path) -> dict[str, object]:
    try:
        from pxr import UsdUtils

        layers, assets, unresolved = UsdUtils.ComputeAllDependencies(str(source_path))
    except Exception as exc:
        return {
            **_empty_dependency_summary(),
            "status": "dependency_gap",
            "detail": f"{type(exc).__name__}: {exc}",
        }

    layer_paths = sorted(path for path in (_layer_path(layer) for layer in layers) if path)
    asset_paths = sorted(str(asset) for asset in assets)
    unresolved_paths = sorted(str(asset) for asset in unresolved)
    return {
        "status": "discovered",
        "detail": "pxr.UsdUtils.ComputeAllDependencies",
        "layer_count": len(layer_paths),
        "asset_count": len(asset_paths),
        "unresolved_count": len(unresolved_paths),
        "layers": layer_paths,
        "assets": asset_paths,
        "unresolved_dependencies": unresolved_paths,
    }


def _local_file_summary(destination_dir: Path) -> dict[str, object]:
    files = sorted(path for path in destination_dir.rglob("*") if path.is_file())
    extensions = Counter(path.suffix.lower() or "<none>" for path in files)
    return {
        "file_count": len(files),
        "total_size_bytes": sum(path.stat().st_size for path in files),
        "extension_counts": dict(sorted(extensions.items())),
        "files": [
            {
                "relative_path": str(path.relative_to(destination_dir)),
                "size_bytes": path.stat().st_size,
                "sha256": _sha256_file(path),
            }
            for path in files
        ],
    }


def _failed_asset_report(
    *,
    role: str,
    status: str,
    detail: str,
    source_path: str = "",
) -> dict[str, object]:
    return {
        "role": role,
        "status": status,
        "detail": detail,
        "source_path": source_path,
        "local_path": "",
        "dependency_summary": _empty_dependency_summary(),
        "local_file_summary": _empty_local_file_summary(),
        "unresolved_dependencies": [],
    }


def _empty_dependency_summary() -> dict[str, object]:
    return {
        "status": "not_run",
        "detail": "",
        "layer_count": 0,
        "asset_count": 0,
        "unresolved_count": 0,
        "layers": [],
        "assets": [],
        "unresolved_dependencies": [],
    }


def _empty_local_file_summary() -> dict[str, object]:
    return {
        "file_count": 0,
        "total_size_bytes": 0,
        "extension_counts": {},
        "files": [],
    }


def _safe_component(value: str, field_name: str) -> str:
    safe_value = _safe_component_or_none(value)
    if safe_value is None:
        raise ValueError(f"{field_name} must be a simple path component")
    return safe_value


def _safe_component_or_none(value: str) -> str | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute() or value in {".", ".."} or "/" in value or "\\" in value:
        return None
    if any(part in {"", ".", ".."} for part in path.parts):
        return None
    return value


def _mirror_root(mirror_root: str | Path | None) -> Path:
    if mirror_root is not None:
        return Path(mirror_root)
    return Path(__file__).resolve().parents[3] / "assets" / "raw" / "mirrors"


def _failed_status(status: str) -> bool:
    return status == "failed" or status.startswith("failed_") or status in {
        "missing_asset_path",
        "missing_source_asset",
        "source_asset_not_file",
        "source_hash_mismatch",
        "source_hash_read_error",
        "unsafe_asset_role",
    }


def _allowed_unresolved_dependency(dependency: str) -> bool:
    return Path(dependency).name == "OmniPBR.mdl"


def _layer_path(layer: Any) -> str:
    real_path = str(getattr(layer, "realPath", "") or "")
    if real_path:
        return real_path
    return str(getattr(layer, "identifier", "") or "")


def _manifest_id(manifest_path: str | Path) -> str:
    try:
        data = yaml.safe_load(Path(manifest_path).read_text(encoding="utf-8")) or {}
    except OSError:
        return Path(manifest_path).stem
    if isinstance(data, dict) and data.get("manifest_id"):
        return str(data["manifest_id"])
    return Path(manifest_path).stem
