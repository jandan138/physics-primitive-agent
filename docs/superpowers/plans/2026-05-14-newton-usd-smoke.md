# Newton USD Smoke Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a claim-safe USD asset-open smoke diagnostic for the CPD-like seed assets.

**Architecture:** Keep USD asset smoke separate from Newton source diagnostics. Reuse the existing config loader and report `EnvironmentCheck` shape, add a small asset report dataclass, and expose the smoke path through `npc-compile --check-assets`.

**Tech Stack:** Python 3.10, PyYAML, usd-core/`pxr.Usd`, pytest, existing `npc-compile` CLI.

---

## File Structure

- Create `src/primitive_collision_compiler/assets/__init__.py`: package exports.
- Create `src/primitive_collision_compiler/assets/usd_smoke.py`: manifest parsing and USD stage smoke checks.
- Modify `src/primitive_collision_compiler/reports/schema.py`: add `AssetSmokeReport`.
- Modify `src/primitive_collision_compiler/reports/__init__.py`: export `AssetSmokeReport`.
- Modify `src/primitive_collision_compiler/cli.py`: add `--check-assets` and prefer
  `cpd_like.asset_manifest` over the seed `asset.path`.
- Add `tests/test_usd_smoke.py`: hermetic USD smoke tests.
- Modify `tests/test_cli.py`: CLI asset-smoke tests using temporary manifests.
- Create `docs/records/2026-05-14-newton-usd-smoke.md`: durable record.

## Task 1: Asset Smoke Report Schema

**Files:**
- Modify: `src/primitive_collision_compiler/reports/schema.py`
- Modify: `src/primitive_collision_compiler/reports/__init__.py`
- Test: `tests/test_usd_smoke.py`

- [x] **Step 1: Write the failing report test**

Add to `tests/test_usd_smoke.py`:

```python
from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


def test_asset_smoke_report_serializes_metadata_and_checks():
    report = AssetSmokeReport(
        stage="usd_open",
        status="smoke_passed",
        role="bed_dev_smoke",
        path="/tmp/bed.usd",
        checks=(EnvironmentCheck("usd_open", "smoke_passed", "opened stage"),),
        metadata={"prim_count": 3, "up_axis": "Z", "meters_per_unit": 1.0},
    )

    payload = report.to_dict()

    assert payload["stage"] == "usd_open"
    assert payload["status"] == "smoke_passed"
    assert payload["role"] == "bed_dev_smoke"
    assert payload["metadata"]["prim_count"] == 3
    assert payload["checks"][0]["name"] == "usd_open"
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_usd_smoke.py::test_asset_smoke_report_serializes_metadata_and_checks -q`

Expected: FAIL because `AssetSmokeReport` does not exist.

- [x] **Step 3: Add minimal report dataclass**

Add to `src/primitive_collision_compiler/reports/schema.py`:

```python
@dataclass(frozen=True)
class AssetSmokeReport:
    stage: str
    status: str
    role: str
    path: str
    checks: tuple[EnvironmentCheck, ...]
    metadata: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "role": self.role,
            "path": self.path,
            "checks": [check.to_dict() for check in self.checks],
            "metadata": self.metadata,
        }
```

Update `src/primitive_collision_compiler/reports/__init__.py`:

```python
from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck, EnvironmentReport

__all__ = ["AssetSmokeReport", "EnvironmentCheck", "EnvironmentReport"]
```

- [x] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_usd_smoke.py::test_asset_smoke_report_serializes_metadata_and_checks -q`

Expected: PASS.

- [x] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/reports tests/test_usd_smoke.py
git commit -m "feat: add asset smoke report schema"
```

## Task 2: USD Smoke Module

**Files:**
- Create: `src/primitive_collision_compiler/assets/__init__.py`
- Create: `src/primitive_collision_compiler/assets/usd_smoke.py`
- Test: `tests/test_usd_smoke.py`

- [x] **Step 1: Write failing USD smoke tests**

Append to `tests/test_usd_smoke.py`:

```python
from pathlib import Path

import yaml
from pxr import Usd, UsdGeom

from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest


def _write_tiny_usd(path: Path):
    stage = Usd.Stage.CreateNew(str(path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    root = stage.DefinePrim("/Root", "Xform")
    stage.SetDefaultPrim(root)
    stage.GetRootLayer().Save()


def test_load_asset_manifest_returns_assets(tmp_path):
    asset_path = tmp_path / "asset.usda"
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "manifest_id": "fixture",
                "assets": [
                    {
                        "role": "fixture_asset",
                        "path": str(asset_path),
                        "sha256": "",
                        "include_in_cpd_like_aggregate": False,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assets = load_asset_manifest(manifest_path)

    assert assets == [
        {
            "role": "fixture_asset",
            "path": str(asset_path),
            "sha256": "",
            "include_in_cpd_like_aggregate": False,
        }
    ]


def test_inspect_usd_asset_reports_smoke_passed_for_openable_stage(tmp_path):
    asset_path = tmp_path / "asset.usda"
    _write_tiny_usd(asset_path)

    report = inspect_usd_asset({"role": "fixture_asset", "path": str(asset_path)})

    assert report.status == "smoke_passed"
    assert report.metadata["default_prim"] == "/Root"
    assert report.metadata["prim_count"] == 1
    assert report.metadata["up_axis"] == "Z"
    assert report.metadata["meters_per_unit"] == 1.0


def test_inspect_usd_asset_reports_missing_asset(tmp_path):
    missing_path = tmp_path / "missing.usd"

    report = inspect_usd_asset({"role": "fixture_asset", "path": str(missing_path)})

    assert report.status == "missing_asset"
    assert report.checks[0].name == "asset_path"
```

- [x] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_usd_smoke.py -q`

Expected: FAIL because `primitive_collision_compiler.assets` does not exist.

- [x] **Step 3: Add USD smoke implementation**

Create `src/primitive_collision_compiler/assets/__init__.py`:

```python
from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest

__all__ = ["inspect_usd_asset", "load_asset_manifest"]
```

Create `src/primitive_collision_compiler/assets/usd_smoke.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from primitive_collision_compiler.reports.schema import AssetSmokeReport, EnvironmentCheck


def load_asset_manifest(path: str | Path) -> list[dict[str, Any]]:
    manifest_path = Path(path)
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
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

    try:
        from pxr import Usd, UsdGeom
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("pxr_usd", "dependency_gap", str(exc)))
        return AssetSmokeReport("usd_open", "dependency_gap", role, path, tuple(checks), {})

    try:
        stage = Usd.Stage.Open(str(asset_path))
    except Exception as exc:
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", f"{type(exc).__name__}: {exc}"))
        return AssetSmokeReport("usd_open", "usd_open_failed", role, path, tuple(checks), {})

    if stage is None:
        checks.append(EnvironmentCheck("usd_open", "usd_open_failed", "Usd.Stage.Open returned None"))
        return AssetSmokeReport("usd_open", "usd_open_failed", role, path, tuple(checks), {})

    metadata = _stage_metadata(stage, UsdGeom)
    checks.append(EnvironmentCheck("usd_open", "smoke_passed", "opened stage"))
    return AssetSmokeReport("usd_open", "smoke_passed", role, path, tuple(checks), metadata)


def _stage_metadata(stage: Any, usd_geom: Any) -> dict[str, object]:
    default_prim = stage.GetDefaultPrim()
    default_path = default_prim.GetPath().pathString if default_prim else ""
    return {
        "default_prim": default_path,
        "prim_count": sum(1 for _ in stage.Traverse()),
        "up_axis": str(usd_geom.GetStageUpAxis(stage)),
        "meters_per_unit": float(usd_geom.GetStageMetersPerUnit(stage)),
    }
```

- [x] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_usd_smoke.py -q`

Expected: PASS.

- [x] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/assets tests/test_usd_smoke.py
git commit -m "feat: add usd asset smoke checks"
```

## Task 3: CLI Asset Smoke

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Test: `tests/test_cli.py`

- [x] **Step 1: Write failing CLI tests**

Append to `tests/test_cli.py`:

```python
from pxr import Usd, UsdGeom
import yaml


def _write_tiny_usd(path: Path):
    stage = Usd.Stage.CreateNew(str(path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    root = stage.DefinePrim("/Root", "Xform")
    stage.SetDefaultPrim(root)
    stage.GetRootLayer().Save()


def test_check_assets_emits_manifest_reports(tmp_path, capsys):
    asset_path = tmp_path / "asset.usda"
    _write_tiny_usd(asset_path)
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump({"assets": [{"role": "fixture_asset", "path": str(asset_path)}]}),
        encoding="utf-8",
    )
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                f"  path: {manifest_path}",
                "task:",
                "  primary: collision_proxy_diagnostic",
            ]
        ),
        encoding="utf-8",
    )

    assert cli.main(["--config", str(config_path), "--check-assets"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "asset_usd_open"
    assert payload["status"] == "smoke_passed"
    assert payload["reports"][0]["role"] == "fixture_asset"
    assert payload["reports"][0]["metadata"]["default_prim"] == "/Root"
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py::test_check_assets_emits_manifest_reports -q`

Expected: FAIL because `--check-assets` is not recognized.

- [x] **Step 3: Add CLI support**

Modify `src/primitive_collision_compiler/cli.py`:

```python
from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest
```

Add parser argument:

```python
parser.add_argument("--check-assets", action="store_true", help="emit USD asset smoke diagnostics")
```

Add handling before dry-run:

```python
    if args.check_assets and args.config:
        try:
            config = load_compile_config(args.config)
            assets = load_asset_manifest(_asset_manifest_path(config))
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        reports = [inspect_usd_asset(asset) for asset in assets]
        status = "smoke_passed" if all(report.status == "smoke_passed" for report in reports) else "smoke_failed"
        print(
            json.dumps(
                {
                    "stage": "asset_usd_open",
                    "status": status,
                    "reports": [report.to_dict() for report in reports],
                },
                sort_keys=True,
            )
        )
        return 0 if status == "smoke_passed" else 2

    if args.check_assets:
        print("npc-compile: --check-assets requires --config.", file=sys.stderr)
        return 2
```

Add helper:

```python
def _asset_manifest_path(config):
    cpd_like_section = config.protocol.get("cpd_like", {})
    if isinstance(cpd_like_section, dict):
        asset_manifest = cpd_like_section.get("asset_manifest")
        if asset_manifest:
            return str(asset_manifest)
    return config.asset_path
```

- [x] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_cli.py::test_check_assets_emits_manifest_reports -q`

Expected: PASS.

- [x] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/cli.py tests/test_cli.py
git commit -m "feat: expose usd asset smoke cli"
```

## Task 4: Record And Verification

**Files:**
- Create: `docs/records/2026-05-14-newton-usd-smoke.md`

- [x] **Step 1: Add durable record**

Create `docs/records/2026-05-14-newton-usd-smoke.md`:

```markdown
# 2026-05-14 Newton USD Smoke

## Date

2026-05-14

## Status

Complete

## Changes

- Added USD asset-open smoke diagnostics for the CPD-like smoke manifest.
- Added `npc-compile --check-assets`.
- Kept Newton runtime status separate from USD asset-open status.

## Verification

- `python -m pytest -q`: exit 0.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.
- `python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-assets`: exit 0.
- `python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton`: exit 0, status `dependency_gap`.

## Artifacts

- Config: `configs/experiments/cpd_like_baseline.yaml`
- Manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Raw USD assets: not committed.
- Generated report target: `reports/generated/cpd_like_baseline/` (ignored).

## Claim Impact

- Supports only deterministic USD-open smoke diagnostics and environment diagnostics.
- Does not support CPD reproduction, Newton simulation, collision quality, benchmark superiority,
  deployment readiness, or safety certification.

## Next Action

- Resolve Newton `warp` dependency in a reproducible environment.
- After Newton imports cleanly, add the first runtime asset import smoke check.
```

- [x] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-assets
python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton
```

Expected: tests pass; docs validate; whitespace check passes; asset smoke returns `smoke_passed`; Newton check returns `dependency_gap` until `warp` is installed.

- [x] **Step 3: Commit**

Run:

```bash
git add docs/records/2026-05-14-newton-usd-smoke.md
git commit -m "docs: record newton usd smoke slice"
```

## Self-Review

- Spec coverage: The plan implements USD manifest loading, USD-open smoke diagnostics, CLI output,
  and records. It does not attempt Newton simulation or CPD decomposition.
- Placeholder scan: No incomplete placeholders remain.
- Type consistency: `AssetSmokeReport`, `EnvironmentCheck`, and CLI JSON keys match across tests and
  implementation tasks.
