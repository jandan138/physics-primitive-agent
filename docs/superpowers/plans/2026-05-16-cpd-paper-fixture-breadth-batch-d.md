# CPD Paper Fixture Breadth Batch D Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Batch D component-pair breadth fixtures to the partial offline
`cpd_paper_offline_report`.

**Architecture:** Keep the implementation fixture-only, command-only, and offline-only. Extend the
existing priority-queue trace so disconnected component-pair candidates can be reported as a
candidate table, optionally capped with deterministic skipped-pair accounting, then add two toy
cases: one all-pairs multi-candidate ordering case and one capped skipped-pair case. Do not add
Newton, package generation, real USD, benchmark, runtime primitive mapping, or broad pair-search
optimization.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests For Batch D Report Surface

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add a failing offline-report test named
  `test_cpd_paper_offline_report_records_fixture_breadth_batch_d` to
  `tests/test_cpd_paper_offline.py`.

```python
def test_cpd_paper_offline_report_records_fixture_breadth_batch_d():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_d"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        trace = case["collapse_trace"]
        assert trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
        assert trace["component_pair_edge_insertion_triggered"] is True
        assert trace["topology_queue_exhausted_before_component_pair_insertion"] is True
        assert trace["initial_edge_count"] == 0
        assert trace["initial_candidates"] == []
        assert trace["package_generation_triggered"] is False
        assert trace["newton_runtime_triggered"] is False
        assert trace["real_usd_triggered"] is False
        assert trace["benchmark_triggered"] is False

    multi = cases["paper_component_pair_multi_candidate_order"]["collapse_trace"]
    assert multi["target_primitive_count"] == 2
    assert multi["threshold_policy"] == "disabled"
    assert multi["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert multi["component_pair_available_pair_count"] == 3
    assert multi["component_pair_candidate_count"] == 3
    assert multi["skipped_component_pair_count"] == 0
    assert multi["skipped_component_pair_keys"] == []
    assert len(multi["component_pair_candidates"]) == 3
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in multi["component_pair_candidates"]
    )
    selected = [event for event in multi["events"] if event["accepted"]][0]
    min_candidate = min(
        multi["component_pair_candidates"],
        key=lambda candidate: candidate["queue_key"],
    )
    assert selected["queue_key"] == min_candidate["queue_key"]
    assert selected["source_faces_merged"] == min_candidate["source_faces_merged"]
    assert multi["accepted_merge_count"] == 1
    assert multi["blocked_merge_count"] == 0
    assert multi["component_pair_attempted_pair_count"] == 1
    assert multi["stop_reason"] == "target_count_reached"
    assert len(multi["final_active_groups"]) == 2

    capped = cases["paper_component_pair_cap_skipped"]["collapse_trace"]
    assert capped["target_primitive_count"] == 3
    assert capped["threshold_policy"] == "disabled"
    assert capped["component_pair_candidate_cap"] == 2
    assert capped["component_pair_available_pair_count"] == 6
    assert capped["component_pair_candidate_count"] == 2
    assert capped["skipped_component_pair_count"] == 4
    assert len(capped["skipped_component_pair_keys"]) == 4
    assert len(capped["component_pair_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in capped["component_pair_candidates"]
    )
    assert all(
        skipped["skip_reason"] == "component_pair_candidate_cap_reached"
        for skipped in capped["skipped_component_pair_keys"]
    )
    assert capped["component_pair_attempted_pair_count"] == 1
    assert capped["accepted_merge_count"] == 1
    assert capped["blocked_merge_count"] == 0
    assert capped["stop_reason"] == "target_count_reached"
    assert len(capped["final_active_groups"]) == 3
```

- [ ] Update the next-gate tests so Batch D advances the current report to Batch E while the top
  report stays partial.

```python
def test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_e():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_fixture_breadth_batch_e"
```

- [ ] Update `test_cpd_paper_offline_report_covers_first_toy_slice` so it expects:

```python
assert report["next_required_gate"] == "paper_fixture_breadth_batch_e"
assert "paper_fixture_breadth_batch_d_component_pair" in report[
    "paper_faithfulness"
]["implemented_fixture_scope"]
```

- [ ] Add the two Batch D case ids to the exact `set(cases)` assertion in
  `test_cpd_paper_offline_report_covers_first_toy_slice`:

```python
"paper_component_pair_multi_candidate_order",
"paper_component_pair_cap_skipped",
```

- [ ] Update `EXPECTED_SCOPE_AUDIT_ROWS` in `tests/test_cpd_paper_offline.py` for the
  `component_pair_edge_handling` row only. Keep `status` as `partial_fixture_scope`, keep
  `blocking_for_paper_faithful_offline` as `True`, and keep the report decision as
  `remain_partial`.

```python
{
    "criterion_id": "component_pair_edge_handling",
    "current_evidence": (
        "Accepted and blocked component-pair toy traces exist, and Batch D records "
        "multi-candidate component-pair ordering plus deterministic skipped-pair "
        "accounting under a fixture cap."
    ),
    "next_action": "Continue with postprocess fixture breadth before stronger wording.",
}
```

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` so it expects
  `paper_fixture_breadth_batch_e`, includes the two Batch D ids in the case-id subset, and adds
  this lightweight JSON surface block.

```python
batch_d_cases = {
    case["case_id"]: case
    for case in payload["cases"]
    if case["case_id"]
    in {
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    }
}
assert set(batch_d_cases) == {
    "paper_component_pair_multi_candidate_order",
    "paper_component_pair_cap_skipped",
}
for case in batch_d_cases.values():
    trace = case["collapse_trace"]
    assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_d"
    assert trace["component_pair_edge_insertion_triggered"] is True
    assert trace["component_pair_candidate_count"] > 1
    assert trace["component_pair_available_pair_count"] >= trace[
        "component_pair_candidate_count"
    ]
    assert trace["component_pair_candidates"]
    assert case["package_generation_triggered"] is False
    assert case["newton_runtime_triggered"] is False
    assert case["real_usd_triggered"] is False
    assert case["benchmark_triggered"] is False
```

- [ ] Run the focused RED tests and verify they fail because the Batch D fields and gate do not
  exist yet.

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_d \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_e \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: FAIL, with missing Batch D case ids and `paper_fixture_breadth_batch_d` still reported as
the next gate.

### Task 2: Minimal Batch D Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Add an optional component-pair cap to `_PaperToyCase`.

```python
component_pair_candidate_cap: int | None = None
```

- [ ] Pass the cap from `_case_payload` into `_priority_queue_trace_payload`.

```python
component_pair_candidate_cap=case.component_pair_candidate_cap,
```

- [ ] Extend `_priority_queue_trace_payload` with a keyword-only
  `component_pair_candidate_cap: int | None = None`. Validate it before the queue loop.

```python
if component_pair_candidate_cap is not None and component_pair_candidate_cap < 1:
    raise ValueError("component_pair_candidate_cap must be positive")
```

- [ ] Add cumulative component-pair accounting variables before the queue loop.

```python
component_pair_available_pair_count = 0
component_pair_candidates: list[dict[str, object]] = []
skipped_component_pair_keys: list[dict[str, object]] = []
```

- [ ] When topology queue is exhausted, compute all currently available component pairs, apply the
  optional cap, append only admitted candidates to the queue, and record skipped pair keys.

```python
component_pairs = [
    (left, right)
    for left, right in _component_pair_group_pairs(active_groups)
    if _component_pair_key(left, right) not in component_pair_attempted_pairs
]
component_pair_available_pair_count += len(component_pairs)
if component_pair_candidate_cap is None:
    admitted_component_pairs = component_pairs
    skipped_component_pairs = []
else:
    admitted_component_pairs = component_pairs[:component_pair_candidate_cap]
    skipped_component_pairs = component_pairs[component_pair_candidate_cap:]
for left, right in skipped_component_pairs:
    skipped_component_pair_keys.append(
        _skipped_component_pair_payload(left, right)
    )
for left, right in admitted_component_pairs:
    entry = _queue_candidate_payload(
        mesh,
        left,
        right,
        insertion_order,
        edge_source="component_pair",
    )
    queue.append(entry)
    component_pair_candidates.append(_queue_candidate_summary(entry))
    insertion_order += 1
    component_pair_candidate_count += 1
```

- [ ] Add a helper for deterministic skipped-pair reporting.

```python
def _skipped_component_pair_payload(
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    left, right = _ordered_group_pair(left, right)
    return {
        "source_faces_left": sorted(int(face_id) for face_id in left),
        "source_faces_right": sorted(int(face_id) for face_id in right),
        "source_faces_merged": sorted(int(face_id) for face_id in left | right),
        "skip_reason": "component_pair_candidate_cap_reached",
    }
```

- [ ] Replace the existing `component_pair_candidate_cap`,
  `component_pair_candidate_count`, and `skipped_component_pair_count` payload fields with the
  richer accounting.

```python
component_pair_candidate_cap_value: int | str
if allow_component_pair_edges and component_pair_candidate_cap is None:
    component_pair_candidate_cap_value = "all_pairs_for_fixture"
elif allow_component_pair_edges:
    component_pair_candidate_cap_value = int(component_pair_candidate_cap)
else:
    component_pair_candidate_cap_value = "disabled"

"component_pair_available_pair_count": component_pair_available_pair_count,
"component_pair_candidate_count": component_pair_candidate_count,
"component_pair_candidate_cap": component_pair_candidate_cap_value,
"component_pair_candidates": component_pair_candidates,
"skipped_component_pair_count": len(skipped_component_pair_keys),
"skipped_component_pair_keys": skipped_component_pair_keys,
```

- [ ] Add two Batch D cases to `_paper_toy_cases()` after Batch C.

```python
_PaperToyCase(
    case_id="paper_component_pair_multi_candidate_order",
    description="Batch D three disconnected components fixture for component-pair candidate ordering",
    mesh=_three_disconnected_components_mesh(),
    face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
    priority_queue_target_count=2,
    component_pair_edge_insertion=True,
    fixture_breadth_batch="paper_fixture_breadth_batch_d",
),
_PaperToyCase(
    case_id="paper_component_pair_cap_skipped",
    description="Batch D four disconnected components fixture for capped skipped-pair accounting",
    mesh=_four_disconnected_components_mesh(),
    face_groups=(frozenset({0}), frozenset({1}), frozenset({2}), frozenset({3})),
    priority_queue_target_count=3,
    component_pair_edge_insertion=True,
    component_pair_candidate_cap=2,
    fixture_breadth_batch="paper_fixture_breadth_batch_d",
),
```

- [ ] Add the two mesh helpers.

```python
def _three_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _four_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
            [3.0, 3.0, 0.0],
            [4.0, 3.0, 0.0],
            [3.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)
```

- [ ] Advance the report gate and implemented fixture scope.

```python
"next_required_gate": "paper_fixture_breadth_batch_e",
```

```python
"paper_fixture_breadth_batch_d_component_pair",
```

- [ ] Update the component-pair scope audit row in `offline.py` to match the test string from
  Task 1.

- [ ] Run the focused GREEN tests.

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_d \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_e \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: PASS.

### Task 3: Documentation And Record Updates

**Files:**

- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-d.md`

- [ ] Update top-level and DeepDive evidence wording so it says Batch D is implemented and the
  next gate is Batch E, while keeping the report partial.

- [ ] Update the paper gap matrix component-pair row so it says Batch D records:
  multi-candidate component-pair ordering, deterministic capped skipped-pair accounting, and
  offline-only/no-runtime boundaries.

- [ ] Update the offline-lane spec and story-status docs so the story reads:

```text
Batch A: source/preprocess/intake/operator breadth
Batch B: primitive-fit breadth
Batch C: cost/search/stop breadth
Batch D: component-pair breadth
Next: Batch E postprocess breadth
```

- [ ] Update the fixture-breadth expansion plan status block:

```text
paper_fixture_breadth_batch_d
-> `paper_component_pair_multi_candidate_order`
-> `paper_component_pair_cap_skipped`
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

- [ ] Add a dated record with these command slots. Fill actual outputs after verification.

```markdown
# CPD Paper Fixture Breadth Batch D

Date: 2026-05-16

## Status

Complete.

## Scope

- Added `paper_component_pair_multi_candidate_order`.
- Added `paper_component_pair_cap_skipped`.
- Added component-pair candidate table, available-pair count, cap value, skipped-pair keys, and
  deterministic skipped-pair count.
- Kept the report partial and advanced the next gate to `paper_fixture_breadth_batch_e`.

## Non-Scope

- No package generation.
- No Newton runtime execution.
- No real USD loading.
- No benchmark or collision-quality claim.

## Verification

Record the exact command lines and observed exit-0 or expected-RED summaries from:

- RED focused pytest before implementation.
- GREEN focused pytest after implementation.
- CLI smoke output for Batch D fields.
- Full `python -m pytest -q` output.
- `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check`.

## Review Notes

Record implementation/schema, documentation/claim-boundary, and reproducibility/registry review
findings, including any fixes made before commit.
```

- [ ] Add an `experiments/registry.yaml` entry named
  `cpd-paper-fixture-breadth-batch-d` with status `complete`, command
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`, and
  the new record path.

### Task 4: Verification, Review, Commit, Push

**Files:**

- Inspect all files touched in Tasks 1-3.

- [ ] Run a CLI smoke to inspect the Batch D fields.

```bash
python - <<'PY'
from primitive_collision_compiler.baselines.cpd_paper.offline import build_cpd_paper_offline_report

report = build_cpd_paper_offline_report()
cases = {case["case_id"]: case for case in report["cases"]}
print(report["next_required_gate"])
for case_id in (
    "paper_component_pair_multi_candidate_order",
    "paper_component_pair_cap_skipped",
):
    trace = cases[case_id]["collapse_trace"]
    print(case_id)
    print("available", trace["component_pair_available_pair_count"])
    print("candidate_count", trace["component_pair_candidate_count"])
    print("cap", trace["component_pair_candidate_cap"])
    print("skipped", trace["skipped_component_pair_count"])
    print("accepted", trace["accepted_merge_count"])
    print("stop", trace["stop_reason"])
print(report["package_generation_triggered"], report["newton_runtime_triggered"], report["real_usd_triggered"], report["benchmark_triggered"])
PY
```

Expected:

```text
paper_fixture_breadth_batch_e
paper_component_pair_multi_candidate_order
available 3
candidate_count 3
cap all_pairs_for_fixture
skipped 0
accepted 1
stop target_count_reached
paper_component_pair_cap_skipped
available 6
candidate_count 2
cap 2
skipped 4
accepted 1
stop target_count_reached
False False False False
```

- [ ] Run focused tests.

```bash
python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: PASS.

- [ ] Run full verification.

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all commands exit 0.

- [ ] Dispatch at least three independent review agents:
  implementation/schema review, documentation/claim-boundary review, and reproducibility/registry
  review. Fix any Critical or Important finding before committing.

- [ ] Commit and push the plan checkpoint before implementation if this task is still only the
  plan. Commit and push the final implementation after all verification and reviews pass.

```bash
git add docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-batch-d.md
git commit -m "docs: plan CPD paper fixture breadth batch D"
git push
```

```bash
git add README.md docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-d.md experiments/registry.yaml src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py
git commit -m "feat: add CPD paper fixture breadth batch D"
git push
```

Expected: branch remains clean and synced with `origin/main`.

## Self-Review

- Spec coverage: the plan maps Batch D fixture ids, component-pair candidate ordering, cap/skipped
  accounting, RED/GREEN tests, docs, records, registry, review, commit, and push to explicit tasks.
- Placeholder scan: no unfilled task placeholders are present.
- Claim boundary: every task keeps package generation, Newton runtime, real USD, benchmark, and
  collision-quality claims out of scope.
