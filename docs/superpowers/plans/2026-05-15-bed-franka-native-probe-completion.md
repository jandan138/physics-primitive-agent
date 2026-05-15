# Bed Franka Native Probe Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the five-step real-USD native fitting/probe path: offline bed+Franka old/new comparison, Newton contact comparison, and gated drop/settle plus sphere-rain comparison, with claim-safe documentation at each step.

**Architecture:** Add one real-USD comparison module that can build packages once and reuse them across offline, contact, and task probes. The CLI remains config-driven and emits JSON-only stdout. Newton task probes are gated by full shape mapping and contact-canary success so they do not imply collision-quality validation when earlier checks fail.

**Tech Stack:** Python, pytest, USD via `pxr`, Newton diagnostic wrappers already in `primitive_collision_compiler.newton`, YAML configs, Markdown records.

---

## Deliverables

The user asked to finish five concrete steps. The deliverables are:

1. A config-driven real-USD old/new native fitting report runner for bed and Franka roles.
2. Offline bed+Franka reports that compare legacy primitives with Newton-native primitives under face caps.
3. A contact-canary comparison runner that consumes the same old/new real-USD packages.
4. A gated task comparison runner that runs drop/settle and sphere-rain only after contact canary passes for a lane.
5. Documentation and dated records for each step, preserving DeepDive and claim-boundary wording.

## Files

- Create: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
  - Owns real-USD comparison artifacts, offline JSON reports, package summaries, and Newton probe comparison helpers.
- Modify: `src/primitive_collision_compiler/cli.py`
  - Adds CLI flags and config parsing for real-USD offline/contact/task comparison.
- Modify: `tests/test_real_usd_native_comparison.py`
  - Adds behavior tests for report builders using generated tiny USD assets and monkeypatched Newton probes.
- Modify: `tests/test_cli.py`
  - Adds CLI JSON/error tests for the new flags.
- Modify: `configs/experiments/newton_native_fitting_comparison.yaml`
  - Changes real-USD status from scope-only to runnable offline/contact/task comparison inputs.
- Add: `configs/experiments/bed_franka_native_probe_comparison.yaml`
  - Focused command config for the five-step bed+Franka path.
- Add: `docs/reference/bed-franka-native-probe-comparison.md`
  - User-facing explanation of the old/new offline/contact/task flow.
- Add: `docs/records/2026-05-15-real-usd-native-fitting-comparison.md`
  - Dated record for offline bed+Franka comparison.
- Add: `docs/records/2026-05-15-real-usd-native-contact-comparison.md`
  - Dated record for contact-canary comparison.
- Add: `docs/records/2026-05-15-real-usd-native-task-comparison.md`
  - Dated record for gated drop/settle and sphere-rain comparison.
- Modify: `docs/reference/bed-franka-native-fitting-next-steps.md`
  - Mark planned steps as implemented and point to the new reference.
- Modify: `docs/reference/newton-native-fitting-comparison.md`
  - Add real-USD status and explain synthetic vs real-USD evidence.
- Modify: `docs/reference/cpd-paper-story-status.md`
  - Place this slice in the CPD paper reproduction story without overclaiming.
- Modify: `docs/deepdive/evidence-status.md`
  - Add supported/unsupported evidence boundaries for the new reports.
- Modify: `docs/reference/claim-boundaries.md`
  - Add allowed and forbidden claim bullets.
- Modify: `docs/index.md`, `docs/records/README.md`, `experiments/registry.yaml`
  - Link new docs and configs.

## Task 1: Real-USD Offline Comparison Builder

**Files:**
- Create: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Create/Modify: `tests/test_real_usd_native_comparison.py`

- [ ] **Step 1: Write RED tests**

Add tests that generate two tiny USD meshes and a manifest. The tests assert that `build_real_usd_native_fitting_comparison_report(...)`:

```python
def test_real_usd_native_fitting_report_runs_roles_from_manifest(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)

    report = build_real_usd_native_fitting_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke", "franka_import_smoke"),
        max_primitives=1,
        legacy_subset=("box", "sphere", "capsule"),
        native_subset=("box", "sphere", "capsule", "cylinder", "cone", "ellipsoid"),
        max_source_faces_by_role={"bed_dev_smoke": 8, "franka_import_smoke": 4},
        component_merge_options={"component_merge": "virtual_pairwise"},
    )

    assert report["stage"] == "cpd_like_real_usd_native_fitting_comparison"
    assert report["status"] == "smoke_passed"
    assert [case["asset_role"] for case in report["cases"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
    assert report["cases"][0]["legacy"]["max_source_faces"] == 8
    assert report["cases"][1]["native"]["max_source_faces"] == 4
    assert "primitive_kind_counts" in report["cases"][0]["legacy"]
    assert "package_mapping" in report["cases"][0]["native"]
    assert report["claim_boundary"] == (
        "real_usd_native_fitting_comparison_not_collision_quality_validation"
    )
```

Add a strict JSON test:

```python
def test_real_usd_native_fitting_report_is_strict_json_serializable(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    report = build_real_usd_native_fitting_comparison_report(...)
    json.dumps(report, allow_nan=False, sort_keys=True)
```

Add a missing-role test:

```python
def test_real_usd_native_fitting_report_rejects_missing_role(tmp_path):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    with pytest.raises(ValueError, match="asset role 'missing_role' not found"):
        build_real_usd_native_fitting_comparison_report(
            manifest_path=str(manifest_path),
            roles=("missing_role",),
            ...
        )
```

- [ ] **Step 2: Run RED tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py -q
```

Expected: fail because `real_usd_comparison.py` does not exist.

- [ ] **Step 3: Implement minimal builder**

Implement:

```python
LEGACY_LABEL = "legacy_box_sphere_capsule"
NATIVE_LABEL = "native_newton_bundle"
REAL_USD_NATIVE_FITTING_STAGE = "cpd_like_real_usd_native_fitting_comparison"
REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY = (
    "real_usd_native_fitting_comparison_not_collision_quality_validation"
)
REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL = "offline_real_usd_native_fitting_smoke"
```

Implement artifact helpers:

```python
@dataclass(frozen=True)
class NativeLaneArtifact:
    label: str
    asset_role: str
    asset_path: str
    max_source_faces: int
    decomposition: CPDLikeDecompositionReport
    objective: dict[str, object]
    package: CollisionPackage

    def to_summary(self) -> dict[str, object]:
        ...

@dataclass(frozen=True)
class RealUsdComparisonArtifact:
    asset_role: str
    asset_path: str
    legacy: NativeLaneArtifact
    native: NativeLaneArtifact

    def to_summary(self) -> dict[str, object]:
        ...
```

Implement `build_real_usd_native_artifacts(...)`, `build_real_usd_native_fitting_comparison_report(...)`, `_resolve_manifest_roles(...)`, `_lane_artifact(...)`, `_package_mapping_summary(...)`, and `_comparison_summary(...)`.

Use existing code paths:

```python
assets = load_asset_manifest(manifest_path)
mesh = load_first_mesh(asset_path, max_faces=max_source_faces)
decomposition = decompose_mesh(mesh, max_primitives=max_primitives, primitive_subset=subset, **component_merge_options)
objective = build_cpd_like_objective_report(...).to_dict()
package = package_from_cpd_like_report(...)
map_package_shapes(package)
```

The comparison summary must include:

```python
{
    "legacy_primitive_count": ...,
    "native_primitive_count": ...,
    "primitive_count_delta_native_minus_legacy": ...,
    "legacy_normalized_weighted_volume": ...,
    "native_normalized_weighted_volume": ...,
    "native_normalized_volume_delta": ...,
    "legacy_fully_mapped": ...,
    "native_fully_mapped": ...,
    "native_uses_extended_primitive": ...,
}
```

- [ ] **Step 4: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py -q
```

Expected: pass.

- [ ] **Step 5: Add docs record for Task 1**

Create `docs/records/2026-05-15-real-usd-native-fitting-comparison.md` with:

- Scope: real-USD offline comparison for bed and Franka roles.
- Inputs: manifest path, roles, face caps.
- Outputs: JSON report fields.
- Claim impact: offline diagnostic only, not collision quality, not benchmark superiority.
- Commands: exact CLI command once Task 2 exists; until then list builder-level test command.

## Task 2: CLI And Config For Offline Real-USD Comparison

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `configs/experiments/newton_native_fitting_comparison.yaml`
- Add: `configs/experiments/bed_franka_native_probe_comparison.yaml`

- [ ] **Step 1: Write RED CLI tests**

Add `test_cli_run_real_usd_native_fitting_comparison_reads_roles_from_config`:

```python
def test_cli_run_real_usd_native_fitting_comparison_reads_roles_from_config(tmp_path, capsys):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    config_path = _write_real_usd_native_config(tmp_path, manifest_path)

    assert cli.main([
        "--config",
        str(config_path),
        "--run-real-usd-native-fitting-comparison",
    ]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_real_usd_native_fitting_comparison"
    assert [case["asset_role"] for case in payload["cases"]] == [
        "bed_dev_smoke",
        "franka_import_smoke",
    ]
```

Add a non-finite JSON rejection test by monkeypatching the builder.

- [ ] **Step 2: Run RED CLI tests**

Run:

```bash
python -m pytest tests/test_cli.py -q -k "real_usd_native_fitting"
```

Expected: fail because the CLI flag does not exist.

- [ ] **Step 3: Implement CLI flag and config parser**

Add parser flag:

```python
parser.add_argument(
    "--run-real-usd-native-fitting-comparison",
    action="store_true",
    help="run real-USD old/new Newton-native primitive fitting comparison",
)
```

Add config helper `_real_usd_native_comparison_options(config)` that reads:

- `cpd_like.asset_manifest`
- `cpd_like.asset_roles`
- `cpd_like.max_source_faces_by_role`
- `cpd_like.legacy_primitive_subset`
- `cpd_like.native_primitive_subset`
- `cpd_like.component_merge`
- `cpd_like.merge_search_policy`
- `cpd_like.excess_volume_threshold_fraction`
- `cpd_like.report_merge_trace`
- `compile.max_primitives`
- `native_fitting_comparison.claim_boundary`
- `native_fitting_comparison.evidence_level`

Add JSON strict output with `allow_nan=False`.

- [ ] **Step 4: Run GREEN CLI tests**

Run:

```bash
python -m pytest tests/test_cli.py -q -k "real_usd_native_fitting"
```

Expected: pass.

- [ ] **Step 5: Update configs and docs record**

Update `configs/experiments/newton_native_fitting_comparison.yaml` so `real_usd_status` no longer says `scope_declared_not_run`; use `offline_real_usd_comparison_configured_not_benchmark`.

Add `configs/experiments/bed_franka_native_probe_comparison.yaml` with the same bed+Franka roles plus Newton diagnostic sections for contact, drop/settle, and sphere-rain.

Update `docs/records/2026-05-15-real-usd-native-fitting-comparison.md` with the command:

```bash
python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison
```

## Task 3: Newton Contact Canary Comparison

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_real_usd_native_comparison.py`
- Modify: `tests/test_cli.py`
- Add: `docs/records/2026-05-15-real-usd-native-contact-comparison.md`

- [ ] **Step 1: Write RED tests**

Add builder tests that monkeypatch `run_newton_contact_smoke`:

```python
def test_real_usd_native_contact_comparison_runs_each_fully_mapped_lane(tmp_path, monkeypatch):
    manifest_path = _write_manifest_with_two_meshes(tmp_path)
    calls = []

    def fake_contact(package, *, source_dir, device, claim_boundary):
        calls.append((package.asset_id, source_dir, device, claim_boundary))
        return NewtonDiagnosticReport(...)

    monkeypatch.setattr(real_usd_comparison, "run_newton_contact_smoke", fake_contact)
    report = build_real_usd_native_contact_comparison_report(
        manifest_path=str(manifest_path),
        roles=("bed_dev_smoke", "franka_import_smoke"),
        source_dir="/tmp/newton-source",
        ...
    )

    assert report["stage"] == "newton_real_usd_native_contact_comparison"
    assert report["status"] == "smoke_passed"
    assert len(calls) == 4
    assert report["cases"][0]["legacy_contact"]["stage"] == "newton_contact_smoke"
```

Add mapping-gate test:

```python
def test_real_usd_native_contact_comparison_blocks_unmapped_lane_before_newton(...):
    ...
    assert report["cases"][0]["legacy_contact"]["status"] == "mapping_gap"
    assert fake_contact_was_not_called_for_that_lane
```

- [ ] **Step 2: Run RED tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py tests/test_cli.py -q -k "native_contact_comparison"
```

Expected: fail because the contact comparison builder/flag does not exist.

- [ ] **Step 3: Implement contact comparison**

Implement:

```python
def build_real_usd_native_contact_comparison_report(...):
    artifacts = build_real_usd_native_artifacts(...)
    for each artifact and lane:
        if not _lane_fully_mapped(lane):
            emit _blocked_probe_payload("mapping_gap", "full_package_shape_coverage_required")
        else:
            with contextlib.redirect_stdout(sys.stderr) in CLI only:
                run_newton_contact_smoke(...)
```

The top-level status is:

- `smoke_passed` when all lane reports are `smoke_passed`.
- `dependency_gap` when at least one lane is `dependency_gap` and no runtime failure exists.
- `partial` for mapping gaps or mixed non-passing statuses.
- `runtime_failure` when any lane has `runtime_failure`.

Add CLI flag `--run-real-usd-native-contact-comparison`.

- [ ] **Step 4: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py tests/test_cli.py -q -k "native_contact_comparison"
```

Expected: pass.

- [ ] **Step 5: Add contact docs**

Create `docs/records/2026-05-15-real-usd-native-contact-comparison.md` and update `docs/reference/bed-franka-native-probe-comparison.md` with:

- Contact canary is a minimal Newton consumption/contact smoke.
- It is not full package contact coverage unless the report explicitly says so.
- It is not collision-quality validation.
- Drop/settle and sphere-rain remain gated on this result.

## Task 4: Gated Drop/Settle And Sphere-Rain Comparison

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_real_usd_native_comparison.py`
- Modify: `tests/test_cli.py`
- Add: `docs/records/2026-05-15-real-usd-native-task-comparison.md`

- [ ] **Step 1: Write RED tests**

Add a test that contact success allows both tasks:

```python
def test_real_usd_native_task_comparison_runs_tasks_after_contact_passes(tmp_path, monkeypatch):
    monkeypatch contact to return smoke_passed
    monkeypatch drop to return smoke_passed
    monkeypatch sphere_rain to return smoke_passed

    report = build_real_usd_native_task_comparison_report(...)

    assert report["stage"] == "newton_real_usd_native_task_comparison"
    assert report["status"] == "smoke_passed"
    assert report["cases"][0]["legacy_tasks"]["drop_settle"]["status"] == "smoke_passed"
    assert report["cases"][0]["legacy_tasks"]["sphere_rain"]["status"] == "smoke_passed"
```

Add a test that contact failure blocks task execution:

```python
def test_real_usd_native_task_comparison_blocks_tasks_when_contact_fails(...):
    monkeypatch contact to return dependency_gap
    drop/sphere functions raise AssertionError if called

    report = build_real_usd_native_task_comparison_report(...)

    assert report["cases"][0]["legacy_tasks"]["drop_settle"]["status"] == "blocked_by_contact_canary"
    assert report["cases"][0]["legacy_tasks"]["sphere_rain"]["status"] == "blocked_by_contact_canary"
```

- [ ] **Step 2: Run RED tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py tests/test_cli.py -q -k "native_task_comparison"
```

Expected: fail because the task comparison builder/flag does not exist.

- [ ] **Step 3: Implement task comparison**

Implement:

```python
def build_real_usd_native_task_comparison_report(...):
    for each lane:
        contact = _run_or_block_contact(...)
        if contact["status"] != "smoke_passed":
            drop = _blocked_probe_payload("blocked_by_contact_canary", contact["status"])
            sphere_rain = _blocked_probe_payload("blocked_by_contact_canary", contact["status"])
        else:
            drop = run_newton_drop_settle(...).to_dict()
            sphere_rain = run_newton_sphere_rain(...).to_dict()
```

Add CLI flag `--run-real-usd-native-task-comparison`. It reads `newton_diagnostic.drop_settle` and `newton_diagnostic.sphere_rain` options from the existing parser helpers.

- [ ] **Step 4: Run GREEN tests**

Run:

```bash
python -m pytest tests/test_real_usd_native_comparison.py tests/test_cli.py -q -k "native_task_comparison"
```

Expected: pass.

- [ ] **Step 5: Add task docs**

Create `docs/records/2026-05-15-real-usd-native-task-comparison.md` and update reference docs with:

- Drop/settle asks whether one package can settle on a ground plane in Newton.
- Sphere-rain asks whether probe spheres produce contacts against the package.
- Both are task smokes, not benchmark superiority, not safety certification, and not proof of physical correctness.

## Task 5: End-To-End Docs, Review, Verification, Push

**Files:**
- Modify all docs listed above.

- [ ] **Step 1: Update reference docs**

Write `docs/reference/bed-franka-native-probe-comparison.md` with sections:

- What changed.
- How this fits the CPD paper story.
- Old lane vs new lane.
- Offline report fields.
- Contact gate.
- Drop/settle and sphere-rain gate.
- What this still does not prove.
- Commands to run.

- [ ] **Step 2: Update claim/evidence docs**

Update:

- `docs/reference/claim-boundaries.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/newton-native-fitting-comparison.md`
- `docs/reference/bed-franka-native-fitting-next-steps.md`

Use allowed wording:

- "real-USD diagnostic smoke"
- "offline comparison report"
- "Newton consumption/contact/task smoke"
- "not collision-quality validation"
- "not benchmark evidence"
- "not paper-faithful CPD"

Avoid:

- "better collider"
- "validated"
- "safe"
- "benchmark win"
- "paper reproduction complete"
- "robot collision package quality"

- [ ] **Step 3: Run real commands**

Run:

```bash
python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison
python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-contact-comparison
python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-task-comparison
```

Record each status in the dated records. If Newton dependency/runtime gaps appear, record them as current evidence rather than weakening the gate.

- [ ] **Step 4: Request multi-agent review**

Ask one agent to review spec coverage and one agent to review code quality. Required review questions:

- Does every requested step have an artifact and test?
- Are task probes gated by contact canary?
- Are dependency gaps reported instead of hidden?
- Do docs avoid collision-quality and benchmark claims?

- [ ] **Step 5: Final verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected:

- Pytest exits 0.
- Docs validation exits 0.
- Whitespace check exits 0.

- [ ] **Step 6: Commit and push**

Commit:

```bash
git add src tests configs docs experiments
git commit -m "feat: add real usd native probe comparisons"
git push
```

Do not add `docs/tmp/papers/arXiv-2602.07369v1/` unless explicitly requested.
