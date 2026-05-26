# Generated-Package Robot Task Probes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Phase 0 Newton robot task probe that consumes the generated link-aware collider package.

**Architecture:** Extend `newton/articulation_smoke.py` with a generated-package variant that reuses the articulation hold/trajectory runtime after attaching generated box shapes to imported robot bodies. Wire the new probe into Phase 0 reporting and config beside the existing source-USD articulation smoke.

**Tech Stack:** Python, pytest, Newton `ModelBuilder`, Warp, OpenUSD/PXR, YAML configs.

---

## File Structure

- Modify `src/primitive_collision_compiler/newton/articulation_smoke.py`: add generated-package constants, evaluation, runtime attachment, and blocked/runtime-failure reports.
- Modify `src/primitive_collision_compiler/phase0.py`: parse generated probe options, call the generated-package runner, update report scope and outcome counts.
- Modify `configs/experiments/phase0_baseline.yaml` and `configs/deepdive/mvp.yaml`: declare the new probe and bounded pass condition.
- Modify `tests/test_newton_articulation_smoke.py`: add generated-package evaluation and dependency-gap tests.
- Modify `tests/test_phase0_benchmark.py`: assert Phase 0 passes the generated package into the new runner and records the probe.
- Modify `tests/test_configs.py`: assert config coverage for the new probe.
- Update evidence docs and paper manifests after the real Phase 0 rerun records current numbers.

### Task 1: Generated-Package Probe Evaluation Tests

**Files:**
- Modify: `tests/test_newton_articulation_smoke.py`
- Modify after red: `src/primitive_collision_compiler/newton/articulation_smoke.py`

- [ ] **Step 1: Write failing tests**

Add tests importing `GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY`, `evaluate_generated_package_robot_task_probe`, and `run_newton_generated_package_robot_task_probe`.

Expected assertions:

```python
report = evaluate_generated_package_robot_task_probe(
    asset_path="robot.usda",
    package_metrics={
        "package_id": "robot:phase0_link_aware_bbox",
        "package_primitive_count": 2,
        "source_link_count": 2,
        "generated_collision_shape_count": 2,
        "consumed_primitive_count": 2,
        "missing_body_link_count": 0,
        "source_usd_shape_count": 0,
        "unsupported_primitive_count": 0,
        "invalid_box_primitive_count": 0,
    },
    import_metrics={"articulation_count": 1, "joint_count": 2, "joint_dof_count": 1, "body_count": 2, "shape_count": 2},
    gravity_hold_metrics={"finite_state": True, "max_joint_drift": 0.0},
    trajectory_metrics={"finite_state": True, "commanded_joint_index": 0, "commanded_joint_delta": 0.05, "end_effector_pose_delta_m": 0.01},
    options=ArticulationSmokeOptions(collapse_fixed_joints=False),
    environment=None,
    device="cpu",
)
assert report["stage"] == "newton_generated_package_robot_task_probe"
assert report["probe_type"] == "generated_package_robot_task_if_robot"
assert report["status"] == "smoke_passed"
assert report["metrics"]["generated_package_consumed"] is True
```

Also add a failure case where `missing_body_link_count == 1` and `source_usd_shape_count == 1`; assert the failure labels include `generated_package_missing_body_link` and `source_usd_collision_shapes_not_suppressed`.

- [ ] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_newton_articulation_smoke.py -q
```

Expected: import failure for the new constants/functions.

- [ ] **Step 3: Implement evaluation and blocked reports**

Add the generated-package constants and `evaluate_generated_package_robot_task_probe()`. Reuse `evaluate_articulation_smoke()` for articulation labels, then add package-consumption labels before computing final status.

- [ ] **Step 4: Verify green**

Run:

```bash
python -m pytest tests/test_newton_articulation_smoke.py -q
```

Expected: all tests in that file pass.

### Task 2: Runtime Package Attachment

**Files:**
- Modify: `src/primitive_collision_compiler/newton/articulation_smoke.py`

- [ ] **Step 1: Add runtime helpers**

Add helpers to normalize `CollisionPackage` or mapping payloads, collect source USD geometry paths, attach generated box shapes with `density=0.0`, and execute the shared articulation runtime after builder setup.

- [ ] **Step 2: Run a direct Franka smoke**

Run:

```bash
env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python - <<'PY'
from primitive_collision_compiler.newton.articulation_smoke import ArticulationSmokeOptions, run_newton_generated_package_robot_task_probe
from primitive_collision_compiler.robots.link_aware_package import build_link_aware_robot_package
asset = "/cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd"
pkg = build_link_aware_robot_package(asset_path=asset, asset_id="franka_import_smoke").package
report = run_newton_generated_package_robot_task_probe(
    asset_path=asset,
    collision_package=pkg,
    source_dir="/cpfs/user/zhuzihou/dev/newton",
    device="cpu",
    options=ArticulationSmokeOptions(hold_frames=15, substeps=2, iterations=2, collapse_fixed_joints=False, mesh_approximation=""),
)
print(report["status"])
print(report["metrics"]["generated_package_consumed"])
print(report["metrics"]["package_consumption"])
PY
```

Expected: `smoke_passed`, `True`, generated shape count equals package primitive count.

### Task 3: Phase 0 Integration Tests

**Files:**
- Modify: `tests/test_phase0_benchmark.py`
- Modify after red: `src/primitive_collision_compiler/phase0.py`

- [ ] **Step 1: Write failing integration assertions**

In `test_phase0_report_records_articulated_robot_smoke_case`, monkeypatch `phase0.run_newton_generated_package_robot_task_probe`. The fake should capture `len(collision_package["primitives"])`, `options.collapse_fixed_joints`, and `options.mesh_approximation`, then return an accept report with `probe_type: "generated_package_robot_task_if_robot"`.

Assert:

```python
assert captured_generated_package == {
    "primitive_count": 3,
    "collapse_fixed_joints": False,
    "mesh_approximation": "",
}
assert robot_case["probe_results"]["generated_package_robot_task_if_robot"]["outcome"] == "accept"
assert report["report_scope"]["generated_package_robot_task_checks"] is True
```

- [ ] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_phase0_benchmark.py::test_phase0_report_records_articulated_robot_smoke_case -q
```

Expected: missing attribute or missing probe assertion failure.

- [ ] **Step 3: Implement Phase 0 wiring**

Import the generated-package runner, add `_generated_package_robot_task_options()`, call the runner when a robot package exists and link audit passes, include the probe in outcome counts, and add `_has_generated_package_robot_task_check()`.

- [ ] **Step 4: Verify green**

Run:

```bash
python -m pytest tests/test_phase0_benchmark.py::test_phase0_report_records_articulated_robot_smoke_case -q
```

Expected: pass.

### Task 4: Config Coverage

**Files:**
- Modify: `configs/experiments/phase0_baseline.yaml`
- Modify: `configs/deepdive/mvp.yaml`
- Modify: `tests/test_configs.py`

- [ ] **Step 1: Add failing config assertions**

Assert `generated_package_robot_task_if_robot` appears in Phase 0 `verify`, has `collapse_fixed_joints: false`, and uses pass condition `generated_package_consumed_and_robot_task_smoke_passed`.

- [ ] **Step 2: Verify red**

Run:

```bash
python -m pytest tests/test_configs.py -q
```

Expected: config assertions fail.

- [ ] **Step 3: Update configs**

Add the probe to task probes, compile verify, and `phase0_defaults.probes` with bounded metrics:

```yaml
generated_package_robot_task_if_robot:
  initial_conditions:
    asset_role: articulated_robot_if_present
    collision_source: generated_link_aware_package
    source_usd_collision_shapes: ignored_when_separate_from_rigid_body
    collapse_fixed_joints: false
    enable_self_collisions: false
    mesh_approximation: ""
  solver:
    engine: newton
    settings: generated_package_recorded
    duration_seconds: 0.25
    seeds: 1
    substeps: 2
    iterations: 2
  metrics:
    - generated_package_consumed
    - generated_collision_shape_count
    - missing_body_link_count
    - source_usd_shape_count
    - gravity_hold_drift
    - trajectory_completion
  pass_condition: generated_package_consumed_and_robot_task_smoke_passed
```

- [ ] **Step 4: Verify green**

Run:

```bash
python -m pytest tests/test_configs.py -q
```

Expected: pass.

### Task 5: Full Verification and Evidence Update

**Files:**
- Modify evidence docs and paper manifests only after real command output exists.

- [ ] **Step 1: Run focused tests**

```bash
python -m pytest tests/test_newton_articulation_smoke.py tests/test_phase0_benchmark.py::test_phase0_report_records_articulated_robot_smoke_case tests/test_configs.py -q
```

- [ ] **Step 2: Run full Phase 0**

```bash
time -p timeout 1200 env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark
```

Expected: report includes `generated_package_robot_task_if_robot` with `generated_package_consumed: true`.

- [ ] **Step 3: Update docs/paper evidence**

Update only summaries that reference Phase 0 scope, outcome counts, robot probe inventory, and paper evidence manifests.

- [ ] **Step 4: Run final verification**

```bash
python scripts/validate_docs.py
git diff --check
make test
make test-paper
git status --short
```

Expected: tests pass and only intentional source/docs/config changes are present before commit.

- [ ] **Step 5: Review, commit, push**

Use a review subagent or reviewer pass for the implementation, fix any critical/important findings, then commit and push.
