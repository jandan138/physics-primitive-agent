from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


@dataclass(frozen=True)
class ResolvedAssetPath:
    path: str
    path_kind: str
    configured_path: str
    source_path: str
    local_path: str
    expected_sha256: str

    def metadata(self) -> dict[str, str]:
        return {
            "selected_path": self.path,
            "selected_path_kind": self.path_kind,
            "configured_path": self.configured_path,
            "source_path": self.source_path,
            "local_path": self.local_path,
        }


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

    normalized_assets: list[dict[str, Any]] = []
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            raise ValueError(f"asset manifest entry {index} must be a mapping")
        normalized_assets.append(dict(asset))
    return normalized_assets


def resolve_asset_path(asset: dict[str, Any]) -> ResolvedAssetPath:
    configured_path = _string_path(asset.get("path"))
    source_path = _string_path(asset.get("source_path")) or configured_path
    local_path = _string_path(asset.get("local_path"))

    candidates = (
        ("local_path", local_path, _string_path(asset.get("local_sha256"))),
        ("path", configured_path, _string_path(asset.get("sha256"))),
        (
            "source_path",
            source_path,
            _string_path(asset.get("source_sha256")) or _string_path(asset.get("sha256")),
        ),
    )
    for path_kind, raw_path, expected_sha256 in candidates:
        expanded_path = _expanded_path(raw_path) if raw_path else None
        if expanded_path and expanded_path.exists():
            return ResolvedAssetPath(
                path=str(expanded_path),
                path_kind=path_kind,
                configured_path=configured_path,
                source_path=source_path,
                local_path=local_path,
                expected_sha256=expected_sha256,
            )

    for path_kind, raw_path, expected_sha256 in candidates:
        if raw_path:
            return ResolvedAssetPath(
                path=str(_expanded_path(raw_path)),
                path_kind=path_kind,
                configured_path=configured_path,
                source_path=source_path,
                local_path=local_path,
                expected_sha256=expected_sha256,
            )

    return ResolvedAssetPath(
        path="",
        path_kind="missing",
        configured_path=configured_path,
        source_path=source_path,
        local_path=local_path,
        expected_sha256="",
    )


def inspect_usd_asset(asset: dict[str, Any]) -> AssetSmokeReport:
    role = str(asset.get("role", "unknown"))
    resolved = resolve_asset_path(asset)
    path = resolved.path
    asset_path = _expanded_path(path)
    checks: list[EnvironmentCheck] = []

    if not asset_path.exists():
        return AssetSmokeReport(
            stage="usd_open",
            status="missing_asset",
            role=role,
            path=path,
            checks=(EnvironmentCheck("asset_path", "missing_asset", "path does not exist"),),
            metadata={"asset_resolution": resolved.metadata()},
        )

    checks.append(EnvironmentCheck("asset_path", "found", f"{resolved.path_kind} exists"))
    hash_status = _check_sha256(asset_path, resolved.expected_sha256, checks)
    if hash_status == "read_error":
        return AssetSmokeReport(
            "usd_open",
            "read_error",
            role,
            path,
            tuple(checks),
            {"asset_resolution": resolved.metadata()},
        )
    if hash_status == "hash_mismatch":
        return AssetSmokeReport(
            "usd_open",
            "hash_mismatch",
            role,
            path,
            tuple(checks),
            {"asset_resolution": resolved.metadata()},
        )

    try:
        from pxr import Usd, UsdGeom
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("pxr_usd", "dependency_gap", str(exc)))
        return AssetSmokeReport(
            "usd_open",
            "dependency_gap",
            role,
            path,
            tuple(checks),
            {"asset_resolution": resolved.metadata()},
        )

    try:
        stage = Usd.Stage.Open(str(asset_path))
    except Exception as exc:
        detail = f"{type(exc).__name__}: {exc}"
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", detail))
        return AssetSmokeReport(
            "usd_open",
            "usd_open_failed",
            role,
            path,
            tuple(checks),
            {"asset_resolution": resolved.metadata()},
        )

    if stage is None:
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", "Usd.Stage.Open returned None"))
        return AssetSmokeReport(
            "usd_open",
            "usd_open_failed",
            role,
            path,
            tuple(checks),
            {"asset_resolution": resolved.metadata()},
        )

    metadata = _stage_metadata(stage, UsdGeom)
    metadata["asset_resolution"] = resolved.metadata()
    checks.append(EnvironmentCheck("usd_open", "smoke_passed", "opened stage"))
    return AssetSmokeReport("usd_open", "smoke_passed", role, path, tuple(checks), metadata)


def _check_sha256(asset_path: Path, expected_sha256: str, checks: list[EnvironmentCheck]) -> str:
    if not expected_sha256:
        checks.append(EnvironmentCheck("sha256", "not_configured", "manifest has no sha256"))
        return "not_configured"

    try:
        actual_sha256 = _sha256_file(asset_path)
    except OSError as exc:
        detail = f"{type(exc).__name__}: {exc}"
        checks.append(EnvironmentCheck("sha256", "read_error", detail))
        return "read_error"
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


def _string_path(value: Any) -> str:
    if value in (None, ""):
        return ""
    return str(value)


def _expanded_path(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def _stage_metadata(stage: Any, usd_geom: Any) -> dict[str, object]:
    default_prim = stage.GetDefaultPrim()
    default_path = default_prim.GetPath().pathString if default_prim else ""
    return {
        "default_prim": default_path,
        "prim_count": sum(1 for _ in stage.Traverse()),
        "up_axis": str(usd_geom.GetStageUpAxis(stage)),
        "meters_per_unit": float(usd_geom.GetStageMetersPerUnit(stage)),
    }
