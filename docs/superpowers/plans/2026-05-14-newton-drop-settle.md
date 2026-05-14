# Newton Drop/Settle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first task-level Newton drop/settle smoke probe for `CollisionPackage` output.

**Architecture:** Add a focused `newton/drop_settle.py` runner that reuses existing package shape mapping and runtime import boundaries, extend reports with typed drop/settle run summaries, add a CLI flag plus dedicated config, and record the clean-env result without broadening claims.

**Tech Stack:** Python 3.10, NumPy, PyYAML, pytest, optional Newton/Warp runtime in the clean external conda environment.

---

## File Structure

- Create `src/primitive_collision_compiler/newton/drop_settle.py`: task-level runner, settings, metric helpers, Newton XPBD loop.
- Modify `src/primitive_collision_compiler/reports/schema.py`: add serializable drop/settle run summary and allow `NewtonDiagnosticReport` to carry `drop_settle_runs`.
- Modify `src/primitive_collision_compiler/cli.py`: add `--run-newton-drop-settle`, parse drop/settle config, redirect Newton/Warp stdout to stderr.
- Create `configs/experiments/newton_drop_settle.yaml`: dedicated bed smoke config with no hardcoded `/cpfs/user/...` Newton source path.
- Modify `experiments/registry.yaml`: add the new experiment entry.
- Test with `tests/test_newton_drop_settle.py`, `tests/test_reports_schema.py`, `tests/test_cli.py`, and `tests/test_cpd_like_config.py`.
- Update docs and records after a real clean-env smoke: `docs/records/2026-05-14-newton-drop-settle.md`, `docs/reference/claim-boundaries.md`, `docs/deepdive/evidence-status.md`, `docs/index.md`, `docs/records/README.md`, and `docs/reference/newton-notes.md`.

## Task 1: Report Shape And Pure Metric Helpers

**Files:**
- Modify: `src/primitive_collision_compiler/reports/schema.py`
- Create: `src/primitive_collision_compiler/newton/drop_settle.py`
- Test: `tests/test_newton_drop_settle.py`, `tests/test_reports_schema.py`

- [ ] **Step 1: Write failing tests**

Add tests that do not require Newton:

```python
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.drop_settle import (
    DROP_SETTLE_CLAIM_BOUNDARY,
    DropSettleOptions,
    evaluate_drop_settle_trace,
    run_newton_drop_settle,
)
from primitive_collision_compiler.reports.schema import NewtonDropSettleRun


def test_drop_settle_blocks_partial_shape_mapping():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="box", kind="box", dimensions={"half_extents": [1.0, 1.0, 1.0]}),
            PrimitiveSpec(primitive_id="mesh", kind="mesh", dimensions={}),
        ),
    )

    report = run_newton_drop_settle(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_drop_settle"
    assert report.probe_type == "drop_settle"
    assert report.status == "mapping_gap"
    assert report.claim_boundary == DROP_SETTLE_CLAIM_BOUNDARY
    assert report.metrics["full_package_shape_coverage"] is False
    assert report.drop_settle_runs == ()


def test_evaluate_drop_settle_trace_labels_missing_contact():
    run = evaluate_drop_settle_trace(
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.20,
        min_height=0.20,
        final_linear_velocity=(0.0, 0.0, -0.1),
        max_contact_count=0,
        final_contact_count=0,
        finite_state=True,
    )

    assert run.status == "runtime_failure"
    assert run.descended is True
    assert run.contact_observed is False
    assert "no_contact_observed" in run.failure_labels


def test_newton_drop_settle_run_serializes_json_safe_metrics():
    run = NewtonDropSettleRun(
        run_id="seed0",
        status="smoke_passed",
        primitive_ids=("box",),
        completed_steps=16,
        initial_height=0.25,
        final_height=0.0,
        min_height=0.0,
        final_linear_velocity=(0.0, 0.0, 0.0),
        max_contact_count=1,
        final_contact_count=1,
        finite_state=True,
        descended=True,
        contact_observed=True,
        failure_labels=(),
    )

    payload = run.to_dict()

    assert payload["run_id"] == "seed0"
    assert payload["primitive_ids"] == ["box"]
    assert payload["final_linear_velocity"] == [0.0, 0.0, 0.0]
```

- [ ] **Step 2: Run red tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py tests/test_reports_schema.py -q
```

Expected: fail because `newton.drop_settle` and `NewtonDropSettleRun` do not exist.

- [ ] **Step 3: Implement minimal schema and helper code**

Add `NewtonDropSettleRun` to `reports/schema.py` with `to_dict()`. Extend
`NewtonDiagnosticReport` with:

```python
drop_settle_runs: tuple[NewtonDropSettleRun, ...] = ()
task_scope: str = ""
initial_conditions: dict[str, object] | None = None
solver: dict[str, object] | None = None
```

Create `DropSettleOptions`, `DROP_SETTLE_CLAIM_BOUNDARY`, and `evaluate_drop_settle_trace()` in
`newton/drop_settle.py`. Keep the helper pure and deterministic.

- [ ] **Step 4: Run green tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py tests/test_reports_schema.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/reports/schema.py src/primitive_collision_compiler/newton/drop_settle.py tests/test_newton_drop_settle.py tests/test_reports_schema.py
git commit -m "feat: add drop settle report metrics"
```

## Task 2: Newton Drop/Settle Runner

**Files:**
- Modify: `src/primitive_collision_compiler/newton/drop_settle.py`
- Test: `tests/test_newton_drop_settle.py`

- [ ] **Step 1: Write failing runner tests**

Add tests for runtime gating and option validation:

```python
from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.drop_settle import DropSettleOptions, run_newton_drop_settle


def test_drop_settle_reports_dependency_gap_after_full_mapping_passes(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.25}),
        ),
    )

    report = run_newton_drop_settle(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.probe_type == "drop_settle"
    assert report.metrics["full_package_shape_coverage"] is True
    assert report.solver["solver"] == "xpbd"


def test_drop_settle_options_reject_non_positive_steps():
    try:
        DropSettleOptions(frames=0)
    except ValueError as exc:
        assert "frames" in str(exc)
    else:
        raise AssertionError("frames=0 should be rejected")
```

- [ ] **Step 2: Run red tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py -q
```

Expected: fail because the runner does not yet gate runtime and options.

- [ ] **Step 3: Implement the runner**

Implement:

- full package mapping gate before importing Newton;
- reuse `_import_newton_runtime()`, `_runtime_environment()`, `_status_from_environment()`,
  `_shape_quat()`, and `_wp_vec3()` from `newton/diagnostics.py` for this slice;
- AABB estimation for `box`, `sphere`, and `capsule`;
- one dynamic compound body with local shape transforms;
- static `builder.add_ground_plane(height=options.ground_height_m)`;
- `SolverXPBD(model, iterations=options.iterations)`;
- loop `frames * substeps`, calling `state_0.clear_forces()`, `model.collide(state_0, contacts)`,
  `solver.step(...)`, and swapping states;
- final `model.collide(state_0, contacts)` before reading the final contact count.

- [ ] **Step 4: Run green tests**

Run:

```bash
python -m pytest tests/test_newton_drop_settle.py tests/test_newton_diagnostics.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/newton/drop_settle.py tests/test_newton_drop_settle.py
git commit -m "feat: run newton drop settle probe"
```

## Task 3: CLI And Config

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Create: `configs/experiments/newton_drop_settle.yaml`
- Modify: `experiments/registry.yaml`
- Test: `tests/test_cli.py`, `tests/test_cpd_like_config.py`

- [ ] **Step 1: Write failing CLI/config tests**

Add tests:

```python
def test_newton_drop_settle_config_owns_probe_parameters():
    config = load_compile_config("configs/experiments/newton_drop_settle.yaml")

    assert config.verify == ("newton_drop_settle",)
    assert config.protocol["newton"]["source_dir"] == "$NEWTON_SOURCE_DIR"
    assert config.protocol["newton_diagnostic"]["probe_type"] == "drop_settle"
    assert config.protocol["newton_diagnostic"]["drop_settle"]["frames"] == 120
    assert "/cpfs/user/" not in Path("configs/experiments/newton_drop_settle.yaml").read_text()


def test_cli_run_newton_drop_settle_keeps_stdout_json_only(tmp_path, capsys, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "asset:",
                "  id: noisy_asset",
                "  path: assets/example.usda",
                "task:",
                "  primary: collision_proxy_diagnostic",
                "newton:",
                f"  source_dir: {tmp_path / 'newton'}",
                "newton_diagnostic:",
                "  probe_type: drop_settle",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "_run_cpd_like_report", lambda config: (object(), "assets/example.usda", 8))
    monkeypatch.setattr(cli, "package_from_cpd_like_report", lambda *args, **kwargs: CollisionPackage("noisy_asset"))

    def noisy_drop_settle(*args, **kwargs):
        print("Warp 1.13.0 initialized:")
        return NewtonDiagnosticReport(
            stage="newton_drop_settle",
            status="smoke_passed",
            asset_id="noisy_asset",
            package_id="noisy_asset:pkg",
            probe_type="drop_settle",
            device="cpu",
            environment=None,
            primitive_count=0,
            type_counts={},
            shape_mappings=(),
            contact_canaries=(),
            drop_settle_runs=(),
            claim_boundary="drop_settle_task_smoke_not_collision_quality_or_safety",
            evidence_level="newton_drop_settle_task_smoke",
        )

    monkeypatch.setattr(cli, "run_newton_drop_settle", noisy_drop_settle)

    assert cli.main(["--config", str(config_path), "--run-newton-drop-settle"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "newton_drop_settle"
    assert captured.out.startswith("{")
    assert "Warp 1.13.0 initialized:" in captured.err
```

- [ ] **Step 2: Run red tests**

Run:

```bash
python -m pytest tests/test_cli.py::test_cli_run_newton_drop_settle_keeps_stdout_json_only tests/test_cpd_like_config.py -q
```

Expected: fail because the flag and config do not exist.

- [ ] **Step 3: Implement CLI/config**

Add `--run-newton-drop-settle`. Reuse the existing CPD-like orchestration, package adapter, source
path expansion, and stdout redirect pattern. Parse `newton_diagnostic.drop_settle` into
`DropSettleOptions`.

- [ ] **Step 4: Run green tests**

Run:

```bash
python -m pytest tests/test_cli.py tests/test_cpd_like_config.py -q
```

Expected: pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/primitive_collision_compiler/cli.py configs/experiments/newton_drop_settle.yaml experiments/registry.yaml tests/test_cli.py tests/test_cpd_like_config.py
git commit -m "feat: expose newton drop settle cli"
```

## Task 4: Real Smoke, Docs, Review, Merge

**Files:**
- Create: `docs/records/2026-05-14-newton-drop-settle.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/newton-notes.md`

- [ ] **Step 1: Run repository verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.

- [ ] **Step 2: Run clean-env smoke**

Run:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/newton_drop_settle.yaml \
  --run-newton-drop-settle
```

Expected: JSON with `stage: newton_drop_settle`. Record exact status, failure labels, and metrics.

- [ ] **Step 3: Write dated record and update claim docs**

Document command, Python path, Newton source commit, asset config, metrics, and limitations. If the
smoke passes, update evidence wording to say that the named task-level smoke diagnostic completed.
If it does not pass, keep evidence status as a failed or blocked probe and record the failure labels.

- [ ] **Step 4: Run final verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.

- [ ] **Step 5: Request code review and fix findings**

Dispatch independent reviewers for spec compliance and code quality. Fix Critical and Important
findings, then rerun final verification.

- [ ] **Step 6: Merge**

Merge the feature branch back to `master` only after verification and review are clean.
