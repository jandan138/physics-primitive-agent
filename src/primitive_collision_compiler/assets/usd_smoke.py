from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


def load_asset_manifest(path: str | Path) -> list[dict[str, Any]]:
    manifest_path = Path(path)
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise ValueError(f"could not read asset manifest: {manifest_path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"could not parse asset manifest: {manifest_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("asset manifest must be a mapping")
    assets = data.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("asset manifest key assets must be a list")
    return [dict(asset) for asset in assets if isinstance(asset, dict)]


def inspect_usd_asset(asset: dict[str, Any]) -> AssetSmokeReport:
    role = str(asset.get("role", "unknown"))
    path = str(asset.get("path", ""))
    asset_path = Path(path)
    checks: list[EnvironmentCheck] = []

    if not asset_path.exists():
        return AssetSmokeReport(
            stage="usd_open",
            status="missing_asset",
            role=role,
            path=path,
            checks=(EnvironmentCheck("asset_path", "missing_asset", "path does not exist"),),
            metadata={},
        )

    checks.append(EnvironmentCheck("asset_path", "found", "path exists"))
    hash_status = _check_sha256(asset_path, str(asset.get("sha256", "")), checks)
    if hash_status == "hash_mismatch":
        return AssetSmokeReport("usd_open", "hash_mismatch", role, path, tuple(checks), {})

    try:
        from pxr import Usd, UsdGeom
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("pxr_usd", "dependency_gap", str(exc)))
        return AssetSmokeReport("usd_open", "dependency_gap", role, path, tuple(checks), {})

    try:
        stage = Usd.Stage.Open(str(asset_path))
    except Exception as exc:
        detail = f"{type(exc).__name__}: {exc}"
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", detail))
        return AssetSmokeReport("usd_open", "usd_open_failed", role, path, tuple(checks), {})

    if stage is None:
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", "Usd.Stage.Open returned None"))
        return AssetSmokeReport("usd_open", "usd_open_failed", role, path, tuple(checks), {})

    metadata = _stage_metadata(stage, UsdGeom)
    checks.append(EnvironmentCheck("usd_open", "smoke_passed", "opened stage"))
    return AssetSmokeReport("usd_open", "smoke_passed", role, path, tuple(checks), metadata)


def _check_sha256(asset_path: Path, expected_sha256: str, checks: list[EnvironmentCheck]) -> str:
    if not expected_sha256:
        checks.append(EnvironmentCheck("sha256", "not_configured", "manifest has no sha256"))
        return "not_configured"

    actual_sha256 = _sha256_file(asset_path)
    if actual_sha256 != expected_sha256:
        detail = f"expected {expected_sha256}, got {actual_sha256}"
        checks.append(EnvironmentCheck("sha256", "hash_mismatch", detail))
        return "hash_mismatch"

    checks.append(EnvironmentCheck("sha256", "matched", actual_sha256))
    return "matched"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _stage_metadata(stage: Any, usd_geom: Any) -> dict[str, object]:
    default_prim = stage.GetDefaultPrim()
    default_path = default_prim.GetPath().pathString if default_prim else ""
    return {
        "default_prim": default_path,
        "prim_count": sum(1 for _ in stage.Traverse()),
        "up_axis": str(usd_geom.GetStageUpAxis(stage)),
        "meters_per_unit": float(usd_geom.GetStageMetersPerUnit(stage)),
    }
