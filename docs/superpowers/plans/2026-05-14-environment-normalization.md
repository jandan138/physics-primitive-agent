# Environment Normalization Implementation Plan

Status: Historical implementation plan. Current evidence is recorded in
`docs/records/2026-05-14-clean-newton-environment-readiness.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Phase 1 local environment-readiness checker that records the Python/Newton/USD/GPU/output state needed before Newton CPD reproduction work, without installing packages or claiming compiler capability.

**Architecture:** Keep the reusable logic in `src/primitive_collision_compiler/environment/readiness.py` and expose it through a small script wrapper at `scripts/env/readiness_check.py`. The checker emits a structured JSON report with narrow readiness statuses, writes only to the requested report path, and treats missing dependencies as evidence rather than failure to hide.

**Tech Stack:** Python 3.10 standard library, existing `primitive_collision_compiler` package layout, pytest, Markdown docs.

---

## File Structure

- Create `src/primitive_collision_compiler/environment/__init__.py`: package marker and public exports.
- Create `src/primitive_collision_compiler/environment/readiness.py`: status classification, Python/module probe, Newton source inspection, output-dir check, optional setup-script fingerprint, GPU visibility probe, and repository diagnostic wrapper.
- Create `scripts/env/readiness_check.py`: command-line wrapper that calls the library, prints JSON to stdout, and writes the report to `--output` or `$NPC_OUTPUT_DIR/environment-readiness.json`.
- Create `tests/test_environment_readiness.py`: unit tests for classification, required variables, JSON shape, and output writing behavior.
- Create `docs/operations/environment.md`: operator-facing environment contract and commands.
- Create `docs/records/2026-05-14-environment-normalization.md`: dated decision record for the Phase 1 approach.

## Task 1: Report Shape And Status Classification

**Files:**
- Create: `src/primitive_collision_compiler/environment/__init__.py`
- Create: `src/primitive_collision_compiler/environment/readiness.py`
- Test: `tests/test_environment_readiness.py`

- [ ] **Step 1: Write the failing tests**

Add these tests to `tests/test_environment_readiness.py`:

```python
from primitive_collision_compiler.environment.readiness import (
    REQUIRED_ENV_VARS,
    build_configuration_report,
    pick_report_status,
)


def test_required_env_vars_are_the_phase1_contract():
    assert REQUIRED_ENV_VARS == (
        "NPC_ENV_ROOT",
        "NPC_PYTHON",
        "NPC_CODE_ROOT",
        "NEWTON_SOURCE_DIR",
        "NPC_OUTPUT_DIR",
    )


def test_pick_report_status_uses_readiness_precedence():
    assert pick_report_status(["smoke_passed", "dependency_gap"]) == "dependency_gap"
    assert pick_report_status(["dependency_gap", "import_error"]) == "import_error"
    assert pick_report_status(["runtime_failure", "import_error"]) == "runtime_failure"
    assert pick_report_status(["configuration_error", "runtime_failure"]) == "configuration_error"
    assert pick_report_status(["smoke_passed", "smoke_passed"]) == "smoke_passed"


def test_build_configuration_report_preserves_top_level_shape():
    report = build_configuration_report({"NPC_PYTHON": "/usr/bin/python"})

    assert report["stage"] == "environment_readiness"
    assert report["status"] == "configuration_error"
    assert report["scope"] == "local"
    assert "checks" in report
    assert "python" in report
    assert "modules" in report
    assert "newton_source" in report
    assert "gpu" in report
    assert "output" in report
    assert "repository_diagnostics" in report
    assert sorted(check["name"] for check in report["checks"] if check["status"] == "configuration_error") == [
        "NEWTON_SOURCE_DIR",
        "NPC_CODE_ROOT",
        "NPC_ENV_ROOT",
        "NPC_OUTPUT_DIR",
    ]
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
```

Expected: fail with `ModuleNotFoundError: No module named 'primitive_collision_compiler.environment'`.

- [ ] **Step 3: Implement the minimal report helpers**

Create `src/primitive_collision_compiler/environment/__init__.py`:

```python
from primitive_collision_compiler.environment.readiness import (
    REQUIRED_ENV_VARS,
    build_configuration_report,
    pick_report_status,
    run_readiness_check,
)

__all__ = [
    "REQUIRED_ENV_VARS",
    "build_configuration_report",
    "pick_report_status",
    "run_readiness_check",
]
```

Create the initial `src/primitive_collision_compiler/environment/readiness.py`:

```python
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

REQUIRED_ENV_VARS = (
    "NPC_ENV_ROOT",
    "NPC_PYTHON",
    "NPC_CODE_ROOT",
    "NEWTON_SOURCE_DIR",
    "NPC_OUTPUT_DIR",
)

_STATUS_ORDER = {
    "smoke_passed": 0,
    "dependency_gap": 1,
    "import_error": 2,
    "runtime_failure": 3,
    "configuration_error": 4,
}


def pick_report_status(statuses: list[str] | tuple[str, ...]) -> str:
    if not statuses:
        return "smoke_passed"
    return max(statuses, key=lambda status: _STATUS_ORDER.get(status, _STATUS_ORDER["runtime_failure"]))


def build_configuration_report(env: Mapping[str, str], *, scope: str = "local") -> dict[str, object]:
    checks = []
    for name in REQUIRED_ENV_VARS:
        value = env.get(name, "")
        if value:
            checks.append({"name": name, "status": "found", "detail": value})
        else:
            checks.append({"name": name, "status": "configuration_error", "detail": "required variable is not set"})

    return {
        "stage": "environment_readiness",
        "status": pick_report_status([check["status"] for check in checks]),
        "scope": scope,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "python": {"executable": env.get("NPC_PYTHON"), "realpath": None, "version": None, "prefix": None, "site_packages": []},
        "modules": {},
        "newton_source": {"path": env.get("NEWTON_SOURCE_DIR"), "remote": None, "branch": None, "commit": None, "dirty": None},
        "gpu": {"nvidia_smi": "not_checked"},
        "output": {"path": env.get("NPC_OUTPUT_DIR"), "writable": None},
        "repository_diagnostics": {},
    }


def run_readiness_check(env: Mapping[str, str], *, scope: str = "local") -> dict[str, object]:
    return build_configuration_report(env, scope=scope)
```

- [ ] **Step 4: Run the tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
```

Expected: pass.

- [ ] **Step 5: Commit Task 1**

Run:

```bash
git add src/primitive_collision_compiler/environment tests/test_environment_readiness.py
git commit -m "feat: add environment readiness report shell"
```

## Task 2: Python And Module Provenance Probe

**Files:**
- Modify: `src/primitive_collision_compiler/environment/readiness.py`
- Test: `tests/test_environment_readiness.py`

- [ ] **Step 1: Write the failing tests**

Add these tests:

```python
import sys

from primitive_collision_compiler.environment.readiness import inspect_python_environment


def test_inspect_python_environment_records_interpreter_identity():
    report = inspect_python_environment(sys.executable)

    assert report["status"] in {"smoke_passed", "dependency_gap", "import_error"}
    assert report["executable"] == sys.executable
    assert report["realpath"]
    assert report["version"].startswith(str(sys.version_info.major))
    assert isinstance(report["site_packages"], list)
    assert set(report["modules"]) == {"newton", "warp", "pxr_usd", "usd_core"}


def test_inspect_python_environment_reports_missing_executable(tmp_path):
    missing_python = tmp_path / "missing-python"

    report = inspect_python_environment(str(missing_python))

    assert report["status"] == "configuration_error"
    assert "does not exist" in report["detail"]
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```bash
python -m pytest tests/test_environment_readiness.py::test_inspect_python_environment_records_interpreter_identity tests/test_environment_readiness.py::test_inspect_python_environment_reports_missing_executable -q
```

Expected: fail because `inspect_python_environment` is not implemented.

- [ ] **Step 3: Implement the Python probe**

Extend `readiness.py` with `inspect_python_environment()`. It must execute `NPC_PYTHON` in a subprocess using a fixed embedded probe, collect `sys.executable`, `Path(sys.executable).resolve()`, `sys.version`, `sys.prefix`, `site.getsitepackages()`, `sys.path`, and module provenance for `newton`, `warp`, `pxr.Usd`, and `usd-core`. Missing modules become `dependency_gap`; import exceptions become `import_error`; subprocess failure becomes `runtime_failure`.

- [ ] **Step 4: Run the tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
```

Expected: pass.

- [ ] **Step 5: Commit Task 2**

Run:

```bash
git add src/primitive_collision_compiler/environment/readiness.py tests/test_environment_readiness.py
git commit -m "feat: inspect python environment provenance"
```

## Task 3: Source, Output, Setup Script, GPU, And Repository Diagnostics

**Files:**
- Modify: `src/primitive_collision_compiler/environment/readiness.py`
- Test: `tests/test_environment_readiness.py`

- [ ] **Step 1: Write the failing tests**

Add tests that exercise deterministic pieces without requiring Newton, DLC, or CUDA:

```python
from primitive_collision_compiler.environment.readiness import (
    inspect_newton_source,
    inspect_output_dir,
    inspect_setup_script,
    run_readiness_check,
)


def test_inspect_newton_source_reports_dependency_gap_for_missing_source(tmp_path):
    missing_source = tmp_path / "missing-newton"

    report = inspect_newton_source(str(missing_source))

    assert report["status"] == "dependency_gap"
    assert report["path"] == str(missing_source)
    assert report["exists"] is False


def test_inspect_output_dir_creates_and_fsyncs_tiny_probe(tmp_path):
    output_dir = tmp_path / "readiness-output"

    report = inspect_output_dir(str(output_dir))

    assert report["status"] == "smoke_passed"
    assert report["writable"] is True
    assert output_dir.exists()


def test_inspect_setup_script_records_hash_without_contents(tmp_path):
    setup_script = tmp_path / "setup.sh"
    setup_script.write_text("export TOKEN=secret\n", encoding="utf-8")

    report = inspect_setup_script(str(setup_script))

    assert report["status"] == "smoke_passed"
    assert report["sha256"]
    assert "TOKEN" not in str(report)
    assert "secret" not in str(report)


def test_run_readiness_check_combines_dependency_gap_status(tmp_path):
    output_dir = tmp_path / "out"
    env = {
        "NPC_ENV_ROOT": str(tmp_path),
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(Path(__file__).resolve().parents[1]),
        "NEWTON_SOURCE_DIR": str(tmp_path / "missing-newton"),
        "NPC_OUTPUT_DIR": str(output_dir),
    }

    report = run_readiness_check(env)

    assert report["status"] == "dependency_gap"
    assert report["python"]["executable"] == sys.executable
    assert report["newton_source"]["status"] == "dependency_gap"
    assert report["output"]["status"] == "smoke_passed"
```

- [ ] **Step 2: Run the tests and verify RED**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
```

Expected: fail because source/output/setup/readiness aggregation helpers are not implemented.

- [ ] **Step 3: Implement deterministic readiness checks**

Extend `readiness.py` with:

- `inspect_newton_source(source_dir)`: records path, realpath, existence, git remote, branch, commit, dirty state, and returns `dependency_gap` when the directory is missing.
- `inspect_output_dir(output_dir)`: creates the directory, writes `.readiness-write-test`, fsyncs it, removes it, records disk free bytes and inode count when available.
- `inspect_setup_script(path_or_none)`: records path, realpath, SHA-256, size, and mtime, never contents.
- `inspect_gpu_visibility()`: calls `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader`; missing `nvidia-smi` is a `dependency_gap`, not a crash.
- `run_repository_diagnostic(env, name, args)`: runs existing repository diagnostics with a deliberate
  `PYTHONPATH=$NPC_CODE_ROOT/src:$NPC_CODE_ROOT` and captures JSON status when available.
- `run_readiness_check(env, include_assets=False)`: aggregates all checks and applies `pick_report_status()`.

- [ ] **Step 4: Run the tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
```

Expected: pass.

- [ ] **Step 5: Commit Task 3**

Run:

```bash
git add src/primitive_collision_compiler/environment/readiness.py tests/test_environment_readiness.py
git commit -m "feat: aggregate environment readiness checks"
```

## Task 4: CLI Wrapper, Docs, And Decision Record

**Files:**
- Create: `scripts/env/readiness_check.py`
- Create: `docs/operations/environment.md`
- Create: `docs/records/2026-05-14-environment-normalization.md`
- Modify: `tests/test_environment_readiness.py`

- [ ] **Step 1: Write the failing script test**

Add this test:

```python
import json
import subprocess


def test_readiness_script_writes_output_file(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "env" / "readiness_check.py"
    output_path = tmp_path / "readiness.json"
    env = {
        **os.environ,
        "NPC_ENV_ROOT": str(tmp_path),
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(Path(__file__).resolve().parents[1]),
        "NEWTON_SOURCE_DIR": str(tmp_path / "missing-newton"),
        "NPC_OUTPUT_DIR": str(tmp_path / "out"),
    }

    result = subprocess.run(
        [sys.executable, str(script), "--output", str(output_path)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 1
    stdout_report = json.loads(result.stdout)
    file_report = json.loads(output_path.read_text(encoding="utf-8"))
    assert stdout_report["stage"] == "environment_readiness"
    assert file_report["stage"] == "environment_readiness"
    assert file_report["status"] == "dependency_gap"
```

- [ ] **Step 2: Run the script test and verify RED**

Run:

```bash
python -m pytest tests/test_environment_readiness.py::test_readiness_script_writes_output_file -q
```

Expected: fail because `scripts/env/readiness_check.py` does not exist.

- [ ] **Step 3: Implement the script wrapper**

Create `scripts/env/readiness_check.py` with:

```python
#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from primitive_collision_compiler.environment.readiness import run_readiness_check


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit local Newton environment readiness JSON.")
    parser.add_argument("--output", type=Path, help="report path; defaults to $NPC_OUTPUT_DIR/environment-readiness.json")
    parser.add_argument("--include-assets", action="store_true", help="also run configured USD asset smoke diagnostics when possible")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_readiness_check(os.environ, include_assets=args.include_assets)
    payload = json.dumps(report, sort_keys=True)
    print(payload)

    output_path = args.output
    if output_path is None and os.environ.get("NPC_OUTPUT_DIR"):
        output_path = Path(os.environ["NPC_OUTPUT_DIR"]) / "environment-readiness.json"
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")

    return 0 if report["status"] == "smoke_passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Add operation docs and dated record**

`docs/operations/environment.md` must document the canonical env variables, the recommended local conda path, the two future install commands, and the fact that `uv` is optional after Phase 1. `docs/records/2026-05-14-environment-normalization.md` must record that Phase 1 added only diagnostics and docs, not an installed environment or DLC submitter.

- [ ] **Step 5: Run checks and verify GREEN**

Run:

```bash
python -m pytest tests/test_environment_readiness.py -q
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass. The readiness script should return status `dependency_gap` in the current ambient environment when Newton/Warp is not fully installed, and that is expected evidence.

- [ ] **Step 6: Commit Task 4**

Run:

```bash
git add scripts/env/readiness_check.py docs/operations/environment.md docs/records/2026-05-14-environment-normalization.md tests/test_environment_readiness.py
git commit -m "docs: document environment readiness workflow"
```

## Final Verification

- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/validate_docs.py`.
- [ ] Run `git diff --check`.
- [ ] Run `NPC_ENV_ROOT=/isaac-sim/kit/python NPC_PYTHON=$(command -v python) NPC_CODE_ROOT=$(pwd) NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton NPC_OUTPUT_DIR=reports/generated/environment-readiness/local python scripts/env/readiness_check.py --output reports/generated/environment-readiness/local/readiness.json` and confirm it produces JSON with `stage=environment_readiness`.
- [ ] Request multi-agent review for claim boundaries, env/DLC reproducibility, and code/test quality before merging.
