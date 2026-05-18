# CPD Paper Mapped-Subset Newton Shape Runtime Builder-Construction Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the bounded offline/report-only `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` gate after the existing builder-preflight gate.

**Architecture:** Consume exactly one builder-preflight row for `paper_single_box`, reconstruct the repo-local `NewtonShapeMapping`, call the existing repo-local `_add_static_shape` dispatch helper with a recording builder and fake Warp-like module, and record the resulting fake-builder `add_shape_box` call as JSON-safe evidence. This may import the repo-local `primitive_collision_compiler.newton.diagnostics` helper, but it must not import the real `newton` or `warp` runtime packages, instantiate `newton.ModelBuilder`, create a Newton engine shape object, finalize a model, run Newton, load real USD, benchmark, or measure collision quality.

**Tech Stack:** Python, pytest, Markdown docs, existing `primitive_collision_compiler.baselines.cpd_paper.offline` report builders, existing repo-local `primitive_collision_compiler.newton.diagnostics._add_static_shape`, and existing `NewtonShapeMapping`.

---

## Baseline

The branch starts from commit `35d7cf4` and baseline verification passed:

```text
PYTHONPATH=src python -m pytest -q
1535 passed, 2 skipped
```

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
  - Add `_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT`.
  - Add `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_construction()`.
  - Add builder-construction false/true flags.
  - Add source validation helpers for the builder-preflight payload and row.
  - Add a small recording builder and fake Warp-like module local to the offline report helpers.
  - Add helper that reconstructs `NewtonShapeMapping` and calls `_add_static_shape`.
  - Add row, coverage, and payload helpers.
  - Wire the payload into `build_cpd_paper_offline_report()`.
- Modify `tests/test_cpd_paper_offline.py`
  - Add expected gate constants and required key sets.
  - Add RED tests for report next gate, payload schema, row schema, recorded fake-builder call, input drift, source-row drift, mapping drift, call-plan drift, false/true flags, JSON safety, and static boundary.
- Modify `tests/test_cli.py`
  - Update `--run-cpd-paper-offline-report` expected failure label, next gate, runtime lane, output scope, and builder-construction payload counters.
- Update docs:
  - `README.md`
  - `docs/index.md`
  - `docs/deepdive/evidence-status.md`
  - `docs/deepdive/message-map.md`
  - `docs/reference/claim-boundaries.md`
  - `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
  - `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
  - `docs/reference/cpd-paper-reproduction-gap-matrix.md`
  - `docs/reference/cpd-paper-story-status.md`
  - `docs/records/README.md`
  - `docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md`

## Task 1: RED Tests For Top-Level Gate And CLI

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add expected constants**

Add:

```python
EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
)
EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT,
]
```

- [ ] **Step 2: Add top-level report gate assertions**

Add a test named:

```python
def test_cpd_paper_records_mapped_subset_newton_shape_runtime_builder_construction_contract_gate():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_"
            "preflight_contract_missing"
        )
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_REMAINING_GAPS
    )
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    )
```

- [ ] **Step 3: Update CLI expectations**

In `test_cli_run_cpd_paper_offline_report_emits_json`, change:

```python
assert payload["failure_labels"] == [
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_missing",
]
assert (
    payload["next_required_gate"]
    == "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
)
assert payload["paper_faithfulness"]["runtime_lane_remaining_gates"] == [
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract",
]
assert (
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    in payload["paper_faithfulness"]["implemented_output_contract_scope"]
)
assert payload[
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
]["recording_builder_shape_call_count"] == 1
assert payload[
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
]["newton_builder_shape_call_count"] == 0
```

- [ ] **Step 4: Run RED command**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate' -q
```

Expected: failures because the payload/key does not exist and top-level next gate is still
`paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.

## Task 2: RED Tests For Payload And Row Schema

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add required payload keys**

Add a `NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS` set containing:

```python
{
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_builder_construction_action",
    "newton_shape_runtime_builder_construction_contract",
    "input_contract_summary",
    "newton_shape_runtime_builder_construction_row_count",
    "source_newton_shape_runtime_builder_preflight_row_count",
    "recording_builder_shape_call_count",
    "recorded_builder_call_count",
    "repo_local_static_shape_helper_call_count",
    "real_newton_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_builder_construction_rows",
    "coverage_summary",
    "remaining_gaps",
}
```

Then union the new false/true flag key sets.

- [ ] **Step 2: Add required row keys**

Add a `NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_ROW_REQUIRED_KEYS` set containing lineage keys,
mapping keys, `builder_call_plan`, `repo_local_static_shape_helper`,
`repo_local_static_shape_helper_called`, `recording_builder_kind`,
`recording_builder_shape_call_count`, `recorded_builder_method_name`,
`recorded_builder_call`, `recorded_builder_call_count`, `fake_wp_call_summary`,
all zero real-runtime counters, and all false/true flags.

- [ ] **Step 3: Add exact payload schema test**

Add:

```python
def test_cpd_paper_newton_shape_runtime_builder_construction_payload_schema_is_exact():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_repo_local_recording_builder_construction_only_partial"
    )
    assert payload["artifact_kind"] == (
        "repo_local_recording_builder_call_not_newton_engine_shape"
    )
    assert payload["runtime_builder_construction_action"] == (
        "call_repo_local_static_shape_helper_with_recording_builder_and_fake_wp"
    )
    assert payload["recording_builder_shape_call_count"] == 1
    assert payload["recorded_builder_call_count"] == 1
    assert payload["repo_local_static_shape_helper_call_count"] == 1
    assert payload["real_newton_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
```

- [ ] **Step 4: Add exact row and recorded call test**

Add:

```python
def test_cpd_paper_newton_shape_runtime_builder_construction_records_fake_builder_call():
    report = build_cpd_paper_offline_report()
    preflight_row = report[
        "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
    ]["newton_shape_runtime_builder_preflight_rows"][0]
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]
    row = payload["newton_shape_runtime_builder_construction_rows"][0]

    assert set(row) == NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_ROW_REQUIRED_KEYS
    assert row["source_newton_shape_runtime_builder_preflight_row_id"] == (
        preflight_row["newton_shape_runtime_builder_preflight_row_id"]
    )
    assert row["repo_local_static_shape_helper"] == "_add_static_shape"
    assert row["repo_local_static_shape_helper_called"] is True
    assert row["recording_builder_kind"] == (
        "repo_local_recording_builder_not_newton_model_builder"
    )
    assert row["recording_builder_shape_call_count"] == 1
    assert row["recorded_builder_method_name"] == "add_shape_box"
    mapping = preflight_row["constructed_newton_shape_mapping_dict"]
    assert row["recorded_builder_call"] == _expected_builder_construction_recorded_call(
        mapping
    )
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_engine_shape_object_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    json.dumps(row["recorded_builder_call"])
    assert _contains_callable(row["recorded_builder_call"]) is False
```

- [ ] **Step 5: Run RED command**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction' -q
```

Expected: failures because the construction payload does not exist.

## Task 3: RED Tests For Drift And Boundaries

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`

- [ ] **Step 1: Add source-input helper**

Add:

```python
def _newton_shape_runtime_builder_construction_input() -> dict[str, object]:
    return json.loads(
        json.dumps(
            build_cpd_paper_offline_report()[
                "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
            ]
        )
    )
```

- [ ] **Step 2: Add drift tests**

Add parametrized tests that mutate:

- input `gate_id`
- input `next_required_gate`
- `builder_call_plan_count`
- `builder_call_allowed_count`
- `newton_builder_shape_call_count`
- `newton_engine_shape_object_count`
- `newton_runtime_execution_count`
- source row count
- source row ids
- source `builder_call_plan.method`
- source `builder_call_plan.dimension_arguments`
- source mapping center/axes/half_extents
- previous false flags
- previous true flags

Expected errors should be specific:

```text
newton_shape_runtime_builder_construction_input_gate_id_mismatch
newton_shape_runtime_builder_construction_input_next_gate_mismatch
newton_shape_runtime_builder_construction_input_count_mismatch:<field>
newton_shape_runtime_builder_construction_row_count_mismatch
newton_shape_runtime_builder_construction_source_row_mismatch:<field>
newton_shape_runtime_builder_construction_call_plan_mismatch:<field>
newton_shape_runtime_builder_construction_mapping_mismatch:<field>
newton_shape_runtime_builder_construction_input_flag_true:<field>
newton_shape_runtime_builder_construction_input_flag_missing:<field>
newton_shape_runtime_builder_construction_input_flag_false:<field>
```

- [ ] **Step 3: Add static boundary test**

Inspect only the new builder-construction helpers and assert forbidden real-runtime patterns are not
present:

```python
for pattern in (
    'importlib.import_module("newton")',
    "import newton",
    "from newton",
    'importlib.import_module("warp")',
    "import warp",
    "from warp",
    "newton.ModelBuilder",
    "ModelBuilder(",
    "CollisionPipeline",
    ".finalize(",
    "pipeline.collide",
    "run_newton_contact_smoke",
    "run_newton_drop_settle",
    "run_newton_sphere_rain",
    "load_first_mesh",
    "inspect_usd_asset",
    "timeit",
    "perf_counter",
    "benchmark_metric",
    "measure_collision_quality",
):
    assert pattern not in source
```

Do not forbid `add_shape_box` in this static test; it is the recording builder method under test.

- [ ] **Step 4: Run RED command**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction' -q
```

Expected: failures because the construction helpers do not exist.

## Task 4: Implement Builder-Construction Helpers

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add constants and remaining-gaps helper**

Add:

```python
_PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
)


def _paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_construction() -> list[str]:
    return [
        _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    ]
```

- [ ] **Step 2: Add false and true flags**

False flags must include all previous false flags plus:

```python
"real_newton_import_triggered",
"newton_model_builder_instantiated",
"newton_model_finalized",
"newton_collision_pipeline_created",
"newton_collision_pipeline_collide_called",
"newton_contact_diagnostic_triggered",
"newton_drop_settle_triggered",
"newton_sphere_rain_triggered",
```

True flags:

```python
"newton_shape_runtime_builder_construction_recorded",
"repo_local_recording_builder_shape_call_recorded",
"repo_local_static_shape_helper_called",
```

- [ ] **Step 3: Add fake Warp and recording builder helpers**

Add local helper classes/functions near the builder-construction block:

```python
class _PaperFakeWarp:
    @staticmethod
    def vec3(x: float, y: float, z: float) -> list[float]:
        return [float(x), float(y), float(z)]

    @staticmethod
    def matrix_from_cols(*cols: list[float]) -> dict[str, object]:
        return {"kind": "fake_wp_matrix_from_cols", "cols": [list(col) for col in cols]}

    @staticmethod
    def quat_from_matrix(matrix: dict[str, object]) -> dict[str, object]:
        return {"kind": "fake_wp_quat_from_matrix", "matrix": matrix}

    @staticmethod
    def transform(translation: list[float], rotation: dict[str, object]) -> dict[str, object]:
        return {
            "kind": "fake_wp_transform",
            "translation": list(translation),
            "rotation": rotation,
        }


class _PaperRecordingNewtonBuilder:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def add_shape_box(self, *, body: int, xform: dict[str, object], hx: float, hy: float, hz: float) -> int:
        self.calls.append(
            {
                "method": "add_shape_box",
                "body": int(body),
                "xform": xform,
                "hx": float(hx),
                "hy": float(hy),
                "hz": float(hz),
            }
        )
        return len(self.calls) - 1
```

- [ ] **Step 4: Add source validation**

Add `_paper_newton_shape_runtime_builder_construction_source_row(preflight)` that validates:

- `preflight["gate_id"] == _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT`
- `preflight["next_required_gate"] == _PAPER_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT`
- all previous false flags are false
- all previous true flags are true
- counts match exactly
- one and only one `newton_shape_runtime_builder_preflight_rows` row exists
- row lineage matches `paper_single_box`
- row `builder_call_plan` matches method `add_shape_box` and half-extents `[1.0, 0.5, 0.25]`
- no source package dicts are copied

- [ ] **Step 5: Add repo-local construction helper**

Add:

```python
def _paper_construct_recording_builder_shape_call(
    source_row: dict[str, object],
) -> dict[str, object]:
    from primitive_collision_compiler.newton.diagnostics import _add_static_shape
    from primitive_collision_compiler.reports.schema import NewtonShapeMapping

    mapping_dict = source_row["constructed_newton_shape_mapping_dict"]
    mapping = NewtonShapeMapping(
        primitive_id=str(mapping_dict["primitive_id"]),
        kind=str(mapping_dict["kind"]),
        status=str(mapping_dict["status"]),
        detail=str(mapping_dict["detail"]),
        center=tuple(float(value) for value in mapping_dict["center"]),
        axes=tuple(tuple(float(axis_value) for axis_value in axis) for axis in mapping_dict["axes"]),
        dimensions=dict(mapping_dict["dimensions"]),
    )
    builder = _PaperRecordingNewtonBuilder()
    _add_static_shape(builder, mapping, _PaperFakeWarp)
    if len(builder.calls) != 1:
        raise ValueError("newton_shape_runtime_builder_construction_call_count_mismatch")
    return builder.calls[0]
```

- [ ] **Step 6: Add row, coverage, and payload helpers**

The row helper should call `_paper_construct_recording_builder_shape_call(source_row)` and return
the exact row described in the design spec. The payload helper should include exact counters:

```python
"newton_shape_runtime_builder_construction_row_count": 1,
"source_newton_shape_runtime_builder_preflight_row_count": 1,
"recording_builder_shape_call_count": 1,
"recorded_builder_call_count": 1,
"repo_local_static_shape_helper_call_count": 1,
"real_newton_import_count": 0,
"newton_model_builder_instantiated_count": 0,
"newton_model_finalized_count": 0,
"newton_engine_shape_object_count": 0,
"newton_builder_shape_call_count": 0,
"newton_runtime_execution_count": 0,
```

- [ ] **Step 7: Wire the payload into `build_cpd_paper_offline_report()`**

After `mapped_subset_newton_shape_runtime_builder_preflight`, build:

```python
mapped_subset_newton_shape_runtime_builder_construction = (
    _paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
        mapped_subset_newton_shape_runtime_builder_preflight
    )
)
```

Use `_paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_builder_construction()` for the
top-level runtime lane and include the new payload in the returned report.

- [ ] **Step 8: Run GREEN command**

```bash
PYTHONPATH=src python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate' -q
```

Expected: all selected tests pass.

## Task 5: Update Documentation And Record

**Files:**
- Modify docs listed in File Structure.
- Add record file listed in File Structure.

- [ ] **Step 1: Locate stale next-gate wording**

Run:

```bash
rg -n 'builder_construction_contract_missing|current next gate.*builder_construction|next step.*builder-construction|paper_mapped_subset_newton_shape_runtime_builder_construction_contract' README.md docs/index.md docs/deepdive docs/reference docs/records/README.md
```

- [ ] **Step 2: Update durable docs**

Each updated doc must say:

- builder-construction is now closed as repo-local recording-builder evidence only;
- exactly one fake-builder `add_shape_box` call is recorded for `paper_single_box`;
- the current next gate is
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`;
- real Newton/Warp import, `ModelBuilder`, engine shape objects, model finalization, Newton runtime,
  real USD, benchmark, collision-quality, deployment, and safety certification remain out of scope.

- [ ] **Step 3: Add dated record**

Create:

`docs/records/2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md`

Include:

```markdown
# 2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Builder-Construction Contract

## Summary

Closed `paper_mapped_subset_newton_shape_runtime_builder_construction_contract` as a single-fixture
repo-local recording-builder contract inside `cpd_paper_offline_report`.

## Evidence Added

- One source builder-preflight row consumed.
- One repo-local `_add_static_shape` helper call made with a recording builder and fake Warp-like
  module.
- One JSON-safe fake-builder `add_shape_box` call recorded.
- Real Newton import count, Newton `ModelBuilder` count, Newton engine shape object count, Newton
  builder shape call count, and Newton runtime execution count remain zero.

## Claim Boundary

This is not Newton runtime evidence, not Newton support, not collision-quality evidence, not a
benchmark, not real-USD evidence, not deployment readiness, and not safety certification.

## Verification

Fill in exact command outputs after final verification.

## Next Gate

`paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`
```

- [ ] **Step 4: Run docs validation**

```bash
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 6: Final Verification, Review, Commit, Merge, Push, Cleanup

**Files:**
- All modified files.

- [ ] **Step 1: Run focused verification**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'newton_shape_runtime_builder_construction or cpd_paper_offline_report_next_gate or cli_run_cpd_paper_offline_report' -q
```

- [ ] **Step 2: Run full verification**

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/validate_docs.py
PYTHONPATH=src python scripts/validate_site_claims.py
git diff --check
```

- [ ] **Step 3: Update dated record with exact verification output**

Replace the placeholder verification text with the exact results from Step 1 and Step 2.

- [ ] **Step 4: Multi-agent final review**

Run read-only reviewers for:

- schema/test consistency;
- Newton/runtime boundary;
- documentation/claim boundary.

Fix any critical or important issue and rerun relevant verification.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add CPD Newton builder construction contract"
```

- [ ] **Step 6: Merge and push**

```bash
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent switch main
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent pull --ff-only
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent merge --ff-only cpd-paper-newton-shape-builder-construction-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent push
```

- [ ] **Step 7: Cleanup**

```bash
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent worktree remove .worktrees/cpd-paper-newton-shape-builder-construction-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent branch -d cpd-paper-newton-shape-builder-construction-contract
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent status --short --branch
git -C /cpfs/user/zhuzihou/dev/physics-primitive-agent worktree list
```

Expected final status: clean `main`, pushed to `origin/main`, and no remaining builder-construction
worktree.
