# CPD-Like Newton Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first executable Newton-facing proof slice for the CPD-like baseline: reproducible config intake, smoke asset manifests, environment diagnostics, and JSON report scaffolding.

**Architecture:** Keep the CPD-like path as a baseline lane under config and reports, with Newton integration limited to dependency/source diagnostics until the runtime imports cleanly. The code must produce evidence records without claiming CPD reproduction, benchmark quality, or production compiler functionality.

**Tech Stack:** Python 3.11, PyYAML, pytest, Newton source tree at `/cpfs/user/zhuzihou/dev/newton`, commit-safe Markdown/YAML manifests.

---

## File Structure

- `configs/experiments/cpd_like_baseline.yaml`: DeepDive-safe experiment config for the CPD-like baseline lane.
- `assets/manifests/cpd_like_smoke_assets.yaml`: Commit-safe manifest for the bed and Franka USD smoke assets; no raw assets are committed.
- `src/primitive_collision_compiler/config.py`: Extend protocol preservation so the new config sections survive load/round-trip.
- `src/primitive_collision_compiler/reports/schema.py`: Small typed report objects for environment and smoke-stage evidence.
- `src/primitive_collision_compiler/newton/env.py`: Inspect Newton source availability, git commit, and Python import readiness.
- `src/primitive_collision_compiler/cli.py`: Add `--check-newton` to emit environment diagnostics as JSON.
- `tests/test_cpd_like_config.py`, `tests/test_reports_schema.py`, `tests/test_newton_env.py`, `tests/test_cli.py`: TDD coverage for the new slice.
- `docs/records/2026-05-14-cpd-like-newton-slice.md`: Durable record of what was built and what remains blocked.

## Task 1: CPD-Like Config And Smoke Asset Manifest

**Files:**
- Create: `configs/experiments/cpd_like_baseline.yaml`
- Create: `assets/manifests/cpd_like_smoke_assets.yaml`
- Modify: `src/primitive_collision_compiler/config.py`
- Test: `tests/test_cpd_like_config.py`

- [ ] **Step 1: Write the failing config test**

```python
from pathlib import Path

import yaml

from primitive_collision_compiler.config import load_compile_config


def test_cpd_like_baseline_preserves_newton_and_cpd_sections():
    config = load_compile_config("configs/experiments/cpd_like_baseline.yaml")

    assert config.asset_id == "grscenes_bed_0a85b986_smoke"
    assert config.task == "collision_proxy_diagnostic"
    assert config.method == "cpd_like_baseline"
    assert config.max_primitives == 32
    assert config.allowed_fallback == ("convex_hull",)
    assert config.verify == ("newton_import",)
    assert config.keep_visual is False
    assert config.protocol["newton"]["source_dir"] == "/cpfs/user/zhuzihou/dev/newton"
    assert config.protocol["cpd_like"]["primitive_subset"] == ["sphere", "capsule", "box"]
    assert config.protocol["cpd_like"]["claim_boundary"] == "internal_baseline_not_reproduction_claim"


def test_smoke_asset_manifest_records_paths_without_committing_assets():
    manifest = yaml.safe_load(Path("assets/manifests/cpd_like_smoke_assets.yaml").read_text())

    assert manifest["manifest_id"] == "cpd_like_smoke_assets_2026_05_14"
    roles = {asset["role"]: asset for asset in manifest["assets"]}
    assert roles["bed_dev_smoke"]["path"].endswith("0a85b986de35ccfdec7c686d791fd747.usd")
    assert roles["bed_dev_smoke"]["sha256"] == "1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265"
    assert roles["franka_import_smoke"]["path"] == "/cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd"
    assert roles["franka_import_smoke"]["include_in_cpd_like_aggregate"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cpd_like_config.py -q`

Expected: FAIL because `configs/experiments/cpd_like_baseline.yaml` does not exist.

- [ ] **Step 3: Write minimal config, manifest, and config loader change**

Create `configs/experiments/cpd_like_baseline.yaml`:

```yaml
asset:
  id: grscenes_bed_0a85b986_smoke
  path: /cpfs/user/zhuzihou/assets/dedup_workspaces/test0_transitive_apply_parallel/dataset/GRScenes_assets/bed/0a85b986de35ccfdec7c686d791fd747/usd/0a85b986de35ccfdec7c686d791fd747.usd
task:
  primary: collision_proxy_diagnostic
compile:
  method: cpd_like_baseline
  max_primitives: 32
  allowed_fallback:
    - convex_hull
  verify:
    - newton_import
  keep_visual: false
cpd_like:
  paper: Convex Primitive Decomposition for Collision Detection
  primitive_subset:
    - sphere
    - capsule
    - box
  decomposition_stage: not_implemented
  claim_boundary: internal_baseline_not_reproduction_claim
newton:
  source_dir: /cpfs/user/zhuzihou/dev/newton
  expected_remote: https://github.com/newton-physics/newton.git
  runtime_stage: source_import_check
report:
  output_dir: reports/cpd_like_baseline
  evidence_level: environment_and_config_only
```

Create `assets/manifests/cpd_like_smoke_assets.yaml`:

```yaml
manifest_id: cpd_like_smoke_assets_2026_05_14
assets:
  - role: bed_dev_smoke
    path: /cpfs/user/zhuzihou/assets/dedup_workspaces/test0_transitive_apply_parallel/dataset/GRScenes_assets/bed/0a85b986de35ccfdec7c686d791fd747/usd/0a85b986de35ccfdec7c686d791fd747.usd
    sha256: 1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265
    size_bytes: 41358161
    provenance_status: internal_dataset_path_unreviewed
    include_in_cpd_like_aggregate: false
  - role: franka_import_smoke
    path: /cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd
    sha256: 2bfd004928d4157ca2fdca3e79bcfb913b4008eef3ec16f839ad89314141976b
    size_bytes: 79079
    provenance_status: internal_dataset_path_unreviewed
    include_in_cpd_like_aggregate: false
```

Modify `src/primitive_collision_compiler/config.py`:

```python
def _protocol_sections(data: dict[str, Any]) -> dict[str, Any]:
    return {
        key: data[key]
        for key in ("phase0_defaults", "report", "cpd_like", "newton")
        if key in data and data[key] is not None
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_cpd_like_config.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add assets/manifests/cpd_like_smoke_assets.yaml configs/experiments/cpd_like_baseline.yaml src/primitive_collision_compiler/config.py tests/test_cpd_like_config.py
git commit -m "feat: add cpd-like baseline config"
```

## Task 2: Report Schema

**Files:**
- Create: `src/primitive_collision_compiler/reports/__init__.py`
- Create: `src/primitive_collision_compiler/reports/schema.py`
- Test: `tests/test_reports_schema.py`

- [ ] **Step 1: Write the failing report schema test**

```python
from primitive_collision_compiler.reports.schema import EnvironmentCheck, EnvironmentReport


def test_environment_report_serializes_dependency_gap():
    report = EnvironmentReport(
        stage="newton_import",
        status="dependency_gap",
        source_dir="/cpfs/user/zhuzihou/dev/newton",
        source_commit="96713fa965463b69c229a4d30582c733ff3526bb",
        checks=(
            EnvironmentCheck(
                name="newton_import",
                status="dependency_gap",
                detail="No module named 'warp'",
            ),
        ),
    )

    payload = report.to_dict()

    assert payload["stage"] == "newton_import"
    assert payload["status"] == "dependency_gap"
    assert payload["source_commit"] == "96713fa965463b69c229a4d30582c733ff3526bb"
    assert payload["checks"][0]["name"] == "newton_import"
    assert payload["checks"][0]["status"] == "dependency_gap"
    assert payload["checks"][0]["detail"] == "No module named 'warp'"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_reports_schema.py -q`

Expected: FAIL because `primitive_collision_compiler.reports` does not exist.

- [ ] **Step 3: Write minimal report schema**

Create `src/primitive_collision_compiler/reports/__init__.py`:

```python
from primitive_collision_compiler.reports.schema import EnvironmentCheck, EnvironmentReport

__all__ = ["EnvironmentCheck", "EnvironmentReport"]
```

Create `src/primitive_collision_compiler/reports/schema.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentCheck:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


@dataclass(frozen=True)
class EnvironmentReport:
    stage: str
    status: str
    source_dir: str
    source_commit: str | None
    checks: tuple[EnvironmentCheck, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "source_dir": self.source_dir,
            "source_commit": self.source_commit,
            "checks": [check.to_dict() for check in self.checks],
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_reports_schema.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/reports tests/test_reports_schema.py
git commit -m "feat: add environment report schema"
```

## Task 3: Newton Environment Diagnostic

**Files:**
- Create: `src/primitive_collision_compiler/newton/__init__.py`
- Create: `src/primitive_collision_compiler/newton/env.py`
- Test: `tests/test_newton_env.py`

- [ ] **Step 1: Write the failing Newton diagnostic tests**

```python
from pathlib import Path

from primitive_collision_compiler.newton.env import inspect_newton_environment


def test_inspect_newton_environment_reports_missing_source(tmp_path):
    missing = tmp_path / "missing-newton"

    report = inspect_newton_environment(missing)

    assert report.status == "missing_source"
    assert report.source_dir == str(missing)
    assert report.source_commit is None
    assert report.checks[0].name == "source_dir"


def test_inspect_newton_environment_records_git_commit_for_source_dir():
    source_dir = Path("/cpfs/user/zhuzihou/dev/newton")

    report = inspect_newton_environment(source_dir)

    assert report.stage == "newton_import"
    assert report.source_dir == str(source_dir)
    assert report.source_commit
    assert any(check.name == "newton_import" for check in report.checks)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_newton_env.py -q`

Expected: FAIL because `primitive_collision_compiler.newton` does not exist.

- [ ] **Step 3: Write minimal Newton diagnostic**

Create `src/primitive_collision_compiler/newton/__init__.py`:

```python
from primitive_collision_compiler.newton.env import inspect_newton_environment

__all__ = ["inspect_newton_environment"]
```

Create `src/primitive_collision_compiler/newton/env.py`:

```python
from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

from primitive_collision_compiler.reports.schema import EnvironmentCheck, EnvironmentReport


def inspect_newton_environment(source_dir: str | Path) -> EnvironmentReport:
    source_path = Path(source_dir)
    if not source_path.exists():
        return EnvironmentReport(
            stage="newton_import",
            status="missing_source",
            source_dir=str(source_path),
            source_commit=None,
            checks=(EnvironmentCheck("source_dir", "missing_source", "path does not exist"),),
        )

    source_commit = _git_commit(source_path)
    checks = [EnvironmentCheck("source_dir", "found", "path exists")]

    try:
        sys.path.insert(0, str(source_path))
        importlib.import_module("newton")
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("newton_import", "dependency_gap", str(exc)))
        status = "dependency_gap"
    except Exception as exc:
        checks.append(EnvironmentCheck("newton_import", "import_error", f"{type(exc).__name__}: {exc}"))
        status = "import_error"
    else:
        checks.append(EnvironmentCheck("newton_import", "smoke_passed", "import newton succeeded"))
        status = "smoke_passed"
    finally:
        try:
            sys.path.remove(str(source_path))
        except ValueError:
            pass

    return EnvironmentReport(
        stage="newton_import",
        status=status,
        source_dir=str(source_path),
        source_commit=source_commit,
        checks=tuple(checks),
    )


def _git_commit(source_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(source_path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_newton_env.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/newton tests/test_newton_env.py
git commit -m "feat: add newton environment diagnostic"
```

## Task 4: CLI Newton Check

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI test**

Append to `tests/test_cli.py`:

```python
def test_check_newton_emits_environment_report(capsys):
    config_path = Path(__file__).resolve().parents[1] / "configs" / "experiments" / "cpd_like_baseline.yaml"

    assert cli.main(["--config", str(config_path), "--check-newton"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["stage"] == "newton_import"
    assert report["source_dir"] == "/cpfs/user/zhuzihou/dev/newton"
    assert report["status"] in {"dependency_gap", "import_error", "smoke_passed"}
    assert any(check["name"] == "newton_import" for check in report["checks"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py::test_check_newton_emits_environment_report -q`

Expected: FAIL because `--check-newton` is not recognized.

- [ ] **Step 3: Add CLI support**

Modify `src/primitive_collision_compiler/cli.py`:

```python
from primitive_collision_compiler.newton.env import inspect_newton_environment
```

Add parser argument:

```python
parser.add_argument("--check-newton", action="store_true", help="emit Newton environment diagnostics")
```

Add command handling before dry-run handling:

```python
    if args.check_newton and args.config:
        try:
            config = load_compile_config(args.config)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        newton_section = config.protocol.get("newton", {})
        source_dir = newton_section.get("source_dir") if isinstance(newton_section, dict) else None
        if not source_dir:
            print("npc-compile: --check-newton requires config key newton.source_dir.", file=sys.stderr)
            return 2
        print(json.dumps(inspect_newton_environment(source_dir).to_dict(), sort_keys=True))
        return 0

    if args.check_newton:
        print("npc-compile: --check-newton requires --config.", file=sys.stderr)
        return 2
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_cli.py::test_check_newton_emits_environment_report -q`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/cli.py tests/test_cli.py
git commit -m "feat: expose newton environment check"
```

## Task 5: Record And Verification

**Files:**
- Create: `docs/records/2026-05-14-cpd-like-newton-slice.md`

- [ ] **Step 1: Add durable record**

Create `docs/records/2026-05-14-cpd-like-newton-slice.md`:

```markdown
# 2026-05-14 CPD-Like Newton Slice

## Decision

Add a minimal CPD-like baseline execution slice before implementing decomposition logic.

## What This Enables

- Load a CPD-like baseline config through the existing compiler config path.
- Track smoke asset paths and hashes without committing raw USD assets.
- Inspect the locally installed Newton source checkout and emit a JSON environment report.

## Current Evidence Boundary

- This is environment and config evidence only.
- It does not show CPD reproduction.
- It does not show collision detection quality, benchmark superiority, or deployment readiness.

## Observed Newton Runtime State

Newton source is expected at `/cpfs/user/zhuzihou/dev/newton`. The diagnostic records the source
commit and then attempts `import newton` from that source tree. A `dependency_gap` status is an
acceptable current result when Python dependencies such as Warp are not installed.

## Next Work

- Install Newton Python dependencies in a reproducible environment.
- Add USD import smoke checks for the bed and Franka assets.
- Implement a restricted primitive proposal/evaluation loop only after import smoke checks pass.
```

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton
```

Expected: tests pass; docs validate; whitespace check passes; CLI returns JSON with `stage` equal to `newton_import`.

- [ ] **Step 3: Commit**

Run:

```bash
git add docs/records/2026-05-14-cpd-like-newton-slice.md
git commit -m "docs: record cpd-like newton slice"
```

## Self-Review

- Spec coverage: This plan covers Newton source discovery, smoke asset manifests, baseline config, report schema, and a CLI environment diagnostic. It deliberately excludes primitive decomposition and collision-quality metrics until runtime dependencies and import checks are reproducible.
- Placeholder scan: No `TBD`, `TODO`, or unspecified implementation steps remain.
- Type consistency: `EnvironmentCheck`, `EnvironmentReport`, and `inspect_newton_environment` signatures match across tests, implementation, and CLI use.
