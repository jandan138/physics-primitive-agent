# CPD Paper Fixture Breadth Batch C Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Batch C cost/search/stop breadth fixtures to the partial offline
`cpd_paper_offline_report`.

**Architecture:** Keep the implementation fixture-only, command-only, and offline-only. Add three
synthetic toy cases under `cpd_paper.offline`: two topology priority-queue traces for weighted-cost
ordering and equal-cost deterministic tie/stale behavior, plus one positive finite threshold block
using the existing component-pair threshold path. Do not add Newton, package generation, real USD,
benchmark, runtime primitive mapping, or broad optimizer behavior.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests For Batch C Report Surface

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add this helper near the existing CPD paper test helpers in
  `tests/test_cpd_paper_offline.py`.

```python
def _event_signature(trace):
    return [
        (
            event["event_kind"],
            event["source_faces_left"],
            event["source_faces_right"],
            event["accepted"],
            event["stale_entry"],
            event["blocked"],
        )
        for event in trace["events"]
    ]
```

- [ ] Add a failing offline-report test named
  `test_cpd_paper_offline_report_records_fixture_breadth_batch_c`.

```python
def test_cpd_paper_offline_report_records_fixture_breadth_batch_c():
    report = build_cpd_paper_offline_report()
    report_again = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    cases_again = {case["case_id"]: case for case in report_again["cases"]}

    expected_case_ids = {
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_c"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["collapse_trace"]["package_generation_triggered"] is False
        assert case["collapse_trace"]["newton_runtime_triggered"] is False
        assert case["collapse_trace"]["real_usd_triggered"] is False
        assert case["collapse_trace"]["benchmark_triggered"] is False
        for candidate in case["collapse_trace"]["initial_candidates"]:
            assert isfinite(candidate["paper_base_cost"])
            assert isfinite(candidate["weighted_priority_cost"])
            assert isfinite(candidate["queue_key"][0])
            assert isfinite(candidate["queue_key"][1])
        for event in case["collapse_trace"]["events"]:
            assert isfinite(event["paper_base_cost"])
            assert isfinite(event["weighted_priority_cost"])
            assert isfinite(event["queue_key"][0])
            assert isfinite(event["queue_key"][1])

    branching = cases["paper_branching_cost_order"]["collapse_trace"]
    assert branching["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert branching["initial_edge_count"] == 2
    assert branching["target_primitive_count"] == 3
    assert branching["threshold_policy"] == "disabled"
    assert len(branching["initial_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "topology"
        for candidate in branching["initial_candidates"]
    )
    assert all("paper_base_cost" in candidate for candidate in branching["initial_candidates"])
    assert all(
        "weighted_priority_cost" in candidate
        for candidate in branching["initial_candidates"]
    )
    first_accepted = [
        event for event in branching["events"] if event["accepted"]
    ][0]
    assert first_accepted["weighted_priority_cost"] == min(
        candidate["weighted_priority_cost"]
        for candidate in branching["initial_candidates"]
    )
    assert first_accepted["queue_key"] == min(
        candidate["queue_key"] for candidate in branching["initial_candidates"]
    )
    assert first_accepted["queue_key"][0] == first_accepted["weighted_priority_cost"]
    assert first_accepted["queue_key"][1] == first_accepted["paper_base_cost"]
    assert first_accepted["updated_neighbor_insertion_count"] == 1
    assert branching["accepted_merge_count"] == 1
    assert branching["stop_reason"] == "target_count_reached"

    tie = cases["paper_equal_cost_queue_tie"]["collapse_trace"]
    tie_again = cases_again["paper_equal_cost_queue_tie"]["collapse_trace"]
    assert tie["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert tie["initial_edge_count"] == 2
    assert tie["target_primitive_count"] == 1
    first_candidate, second_candidate = tie["initial_candidates"]
    assert first_candidate["weighted_priority_cost"] == second_candidate[
        "weighted_priority_cost"
    ]
    assert first_candidate["paper_base_cost"] == second_candidate["paper_base_cost"]
    assert first_candidate["queue_key"][2:] < second_candidate["queue_key"][2:]
    assert first_candidate["left_primitive"] == second_candidate["left_primitive"]
    assert first_candidate["right_primitive"] == second_candidate["right_primitive"]
    assert first_candidate["merged_primitive"] == second_candidate["merged_primitive"]
    assert tie["events"][0]["event_kind"] == "accepted_merge"
    assert tie["events"][0]["source_faces_left"] == [0]
    assert tie["events"][0]["source_faces_right"] == [1]
    assert tie["events"][1]["event_kind"] == "eager_stale_prune"
    assert tie["events"][1]["stale_entry"] is True
    assert tie["events"][1]["source_faces_left"] == [0]
    assert tie["events"][1]["source_faces_right"] == [2]
    assert tie["events"][2]["event_kind"] == "accepted_merge"
    assert tie["events"][2]["source_faces_left"] == [0, 1]
    assert tie["events"][2]["source_faces_right"] == [2]
    assert len(tie["events"]) == 3
    assert tie["accepted_merge_count"] == 2
    assert tie["stale_entry_skipped_count"] == 1
    assert tie["final_active_groups"] == [[0, 1, 2]]
    assert _event_signature(tie) == [
        ("accepted_merge", [0], [1], True, False, False),
        ("eager_stale_prune", [0], [2], False, True, False),
        ("accepted_merge", [0, 1], [2], True, False, False),
    ]
    assert _event_signature(tie) == _event_signature(tie_again)

    blocked = cases["paper_nonzero_threshold_block"]["collapse_trace"]
    assert blocked["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert blocked["component_pair_edge_insertion_triggered"] is True
    assert blocked["topology_queue_exhausted_before_component_pair_insertion"] is True
    assert blocked["threshold_policy"] == "component_pair_paper_base_cost_lte_threshold"
    assert blocked["excess_volume_threshold"] == 1e-6
    assert blocked["accepted_merge_count"] == 0
    assert blocked["blocked_merge_count"] == 1
    assert blocked["stop_reason"] == "all_remaining_edges_blocked_by_threshold"
    blocked_events = [
        event for event in blocked["events"] if event["event_kind"] == "blocked_by_threshold"
    ]
    assert len(blocked_events) == 1
    blocked_event = blocked_events[0]
    assert blocked_event["edge_source"] == "component_pair"
    assert blocked_event["threshold_metric"] == "paper_base_cost"
    assert blocked_event["threshold_value"] == 1e-6
    assert blocked_event["paper_base_cost"] > blocked_event["threshold_value"] > 0.0
    assert blocked_event["blocked_reason"] == "component_pair_threshold_exceeded"
```

- [ ] Update the next-gate tests so Batch C advances the current report to Batch D while the top
  report stays partial.

```python
def test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_d():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_fixture_breadth_batch_d"
```

- [ ] Update `test_cpd_paper_offline_report_covers_first_toy_slice` so it expects:

```python
assert report["next_required_gate"] == "paper_fixture_breadth_batch_d"
assert "paper_fixture_breadth_batch_c_cost_search_stop" in report[
    "paper_faithfulness"
]["implemented_fixture_scope"]
```

- [ ] Add the three Batch C case ids to the exact `set(cases)` assertion in
  `test_cpd_paper_offline_report_covers_first_toy_slice`:

```python
"paper_branching_cost_order",
"paper_equal_cost_queue_tie",
"paper_nonzero_threshold_block",
```

- [ ] Update `EXPECTED_SCOPE_AUDIT_ROWS` in `tests/test_cpd_paper_offline.py` for these three
  rows only. Keep `status` as `partial_fixture_scope`, keep
  `blocking_for_paper_faithful_offline` as `True`, and keep the report decision as
  `remain_partial`.

```python
{
    "criterion_id": "paper_collapse_cost_and_weighting",
    "current_evidence": (
        "One two-face cost fixture plus Batch C cost/search/stop fixtures record "
        "base and weighted costs, weighted priority ordering, and one positive "
        "finite threshold block."
    ),
}
{
    "criterion_id": "greedy_priority_queue_trace",
    "current_evidence": (
        "Topology, deduplicated-topology, component-pair, and Batch C toy traces "
        "exist with deterministic queue keys, weighted-cost ordering, and "
        "equal-cost stale-prune behavior."
    ),
}
{
    "criterion_id": "target_count_and_threshold_stop",
    "current_evidence": (
        "Target-count traces, one zero finite-threshold component-pair block, and "
        "one Batch C positive nonzero finite-threshold component-pair block exist."
    ),
}
```

- [ ] Update `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` so it expects
  `paper_fixture_breadth_batch_d`, includes the three Batch C ids in the case-id subset, and adds
  this lightweight JSON surface block.

```python
batch_c_cases = {
    case["case_id"]: case
    for case in payload["cases"]
    if case["case_id"]
    in {
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
    }
}
assert set(batch_c_cases) == {
    "paper_branching_cost_order",
    "paper_equal_cost_queue_tie",
    "paper_nonzero_threshold_block",
}
for case in batch_c_cases.values():
    assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_c"
    assert case["package_generation_triggered"] is False
    assert case["newton_runtime_triggered"] is False
    assert case["real_usd_triggered"] is False
    assert case["benchmark_triggered"] is False

assert batch_c_cases["paper_branching_cost_order"]["collapse_trace"][
    "accepted_merge_count"
] == 1
assert batch_c_cases["paper_equal_cost_queue_tie"]["collapse_trace"][
    "stale_entry_skipped_count"
] >= 1
assert batch_c_cases["paper_nonzero_threshold_block"]["collapse_trace"][
    "excess_volume_threshold"
] == 1e-6
```

- [ ] Run the RED command and confirm it fails because the Batch C cases, implemented scope, and
  Batch D next gate are absent.

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_c \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_d \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: fail with missing Batch C case ids or the current next gate
`paper_fixture_breadth_batch_c`.

### Task 2: Implement Batch C Fixtures

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Add these deterministic synthetic mesh helpers after the existing toy mesh helpers.

```python
def _paper_branching_cost_order_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.2, -0.2, 0.0],
            [1.8, 1.2, 0.0],
            [10.0, 0.0, 0.0],
            [11.0, 0.0, 0.0],
            [10.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [2, 1, 4],
            [5, 6, 7],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _paper_equal_cost_queue_tie_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 3, 1],
            [0, 2, 4],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)
```

- [ ] Add three `_PaperToyCase` rows after Batch B in `_paper_toy_cases()`.

```python
_PaperToyCase(
    case_id="paper_branching_cost_order",
    description="Batch C branching topology fixture for weighted priority cost ordering",
    mesh=_paper_branching_cost_order_mesh(),
    face_groups=(
        frozenset({0}),
        frozenset({1}),
        frozenset({2}),
        frozenset({3}),
    ),
    priority_queue_target_count=3,
    fixture_breadth_batch="paper_fixture_breadth_batch_c",
),
_PaperToyCase(
    case_id="paper_equal_cost_queue_tie",
    description="Batch C symmetric topology fixture for deterministic equal-cost queue ties",
    mesh=_paper_equal_cost_queue_tie_mesh(),
    face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
    priority_queue_target_count=1,
    fixture_breadth_batch="paper_fixture_breadth_batch_c",
),
_PaperToyCase(
    case_id="paper_nonzero_threshold_block",
    description="Batch C positive finite component-pair threshold block fixture",
    mesh=_disconnected_components_mesh(),
    face_groups=(frozenset({0}), frozenset({1})),
    priority_queue_target_count=1,
    component_pair_edge_insertion=True,
    component_pair_excess_volume_threshold=1e-6,
    fixture_breadth_batch="paper_fixture_breadth_batch_c",
),
```

- [ ] Update `build_cpd_paper_offline_report()`:

```python
"next_required_gate": "paper_fixture_breadth_batch_d",
```

- [ ] Add Batch C to `paper_faithfulness["implemented_fixture_scope"]`:

```python
"paper_fixture_breadth_batch_c_cost_search_stop",
```

- [ ] Update `_paper_faithful_offline_scope_criteria()` current evidence for only these rows:

```python
"paper_collapse_cost_and_weighting"
"greedy_priority_queue_trace"
"target_count_and_threshold_stop"
```

The texts must match the RED test exactly. Do not mark any of the three rows
`implemented_fixture_scope`, because Batch D/E and broader paper-lane mechanics are still open.

- [ ] Run the GREEN focused command:

```bash
python -m pytest -q \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_c \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_d \
  tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice \
  tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: pass.

### Task 3: Update Docs, Record, And Registry

**Files:**

- Modify: `README.md`
- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-c.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`

- [ ] Update canonical docs so they say Batch A, Batch B, and Batch C are implemented, the next
  gate is `paper_fixture_breadth_batch_d`, and Batch C is limited to cost/search/stop breadth.
  Keep every claim boundary explicit:

```text
no package generation, Newton runtime, real USD, benchmark, collision-quality,
deployment, or safety-certification claim
```

- [ ] In `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`, change the Batch Status
  section so Batch C is implemented and the next code slice is Batch D component-pair breadth.
  Keep the Claim Boundary section saying Batch D-E are not implemented.

- [ ] Create a pending Batch C record before final verification. The pending record exists so the
  registry can point at a real file during validation, but it must not claim completed tests or
  review outcomes before those commands actually run.

```markdown
# 2026-05-16 CPD Paper Fixture Breadth Batch C

## Status

Pending implementation verification.

## Summary

- Planned three Batch C cost/search/stop breadth fixtures for the partial offline
  `cpd_paper_offline_report`.
- Planned `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, and
  `paper_nonzero_threshold_block`.
- Intended next gate after implementation: `paper_fixture_breadth_batch_d`.
- Intended boundaries: keep `status: partial`, `paper_faithful_offline_supported: false`, and
  `failure_labels: ["paper_fixture_breadth_expansion_missing"]`.

## Verification

Pending. Replace this section after RED, GREEN, full verification, and review have actually run.

## Review Notes

Pending final implementation review.

## Claim Boundary

Supports only partial, fixture-scoped, command-only Batch C cost/search/stop breadth accounting.
Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
readiness, or safety certification.

## Next

- Proceed to `paper_fixture_breadth_batch_d`.
```

- [ ] Add this record to `docs/records/README.md` after Batch B.

```markdown
- [2026-05-16 CPD Paper Fixture Breadth Batch C](2026-05-16-cpd-paper-fixture-breadth-batch-c.md):
  partial command-only cost/search/stop fixture-breadth audit inside
  `cpd_paper_offline_report`.
```

- [ ] Add this registry entry after `cpd-paper-fixture-breadth-batch-b`. Keep it `pending` until
  Task 4 and the Task 5 implementation reviews are complete.

```yaml
  - id: cpd-paper-fixture-breadth-batch-c
    status: pending
    command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
    record: docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-c.md
    purpose: >
      Extend the command-only partial offline CPD paper-lane audit with Batch C cost,
      search, and threshold-stop fixture breadth.
    claims_supported:
      - partial fixture-scoped offline cost/search/stop Batch C audit only
      - records branching weighted-cost ordering, equal-cost deterministic queue tie and stale-prune behavior, one positive finite component-pair threshold block, and the next gate paper_fixture_breadth_batch_d
      - no paper_faithful_offline claim, full CPD reproduction claim, package-generation claim, Newton runtime claim, real-USD claim, collision-quality claim, benchmark-suite claim, deployment claim, or safety-certification claim
```

- [ ] Run docs validation.

```bash
python scripts/validate_docs.py
```

Expected: pass.

### Task 4: Focused CLI Smoke And Full Verification

**Files:**

- No source files beyond Task 1-3 unless verification exposes a real issue.

- [ ] Run a command-line JSON smoke and inspect the important fields.

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

Expected JSON facts:

```text
next_required_gate == paper_fixture_breadth_batch_d
implemented_fixture_scope contains paper_fixture_breadth_batch_c_cost_search_stop
cases contain paper_branching_cost_order
cases contain paper_equal_cost_queue_tie
cases contain paper_nonzero_threshold_block
paper_nonzero_threshold_block.collapse_trace.excess_volume_threshold == 1e-6
package_generation_triggered == false
newton_runtime_triggered == false
real_usd_triggered == false
benchmark_triggered == false
```

- [ ] Run focused CPD paper tests.

```bash
python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json
```

Expected: pass.

- [ ] Run full project verification.

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

### Task 5: Multi-Agent Review, Fixes, Commit, And Push

**Files:**

- Modify only if review or verification finds concrete issues.

- [ ] Dispatch three read-only reviewers after implementation:

```text
1. Implementation reviewer: inspect Batch C source/test behavior and deterministic queue assertions.
2. Docs/claim reviewer: inspect wording against claim boundaries and DeepDive readiness.
3. Repro/registry reviewer: inspect command, record, registry, and validation risks.
```

- [ ] Fix Critical or Important findings with focused patches and rerun affected tests.

- [ ] Replace the pending Batch C record with actual evidence from the commands and reviews that
  ran. Only after this step may `## Status` become `Complete.`.

- [ ] Change the `cpd-paper-fixture-breadth-batch-c` registry entry from `pending` to `complete`
  after the record status is `Complete.` and validation passes.

- [ ] If docs changed after review, rerun:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] Commit all Batch C changes.

```bash
git add \
  docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-batch-c.md \
  README.md \
  docs/index.md \
  docs/reference/claim-boundaries.md \
  docs/deepdive/evidence-status.md \
  docs/reference/cpd-paper-reproduction-gap-matrix.md \
  docs/reference/cpd-paper-faithful-offline-lane-spec.md \
  docs/reference/cpd-paper-fixture-breadth-expansion-plan.md \
  docs/reference/cpd-paper-story-status.md \
  docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-c.md \
  docs/records/README.md \
  experiments/registry.yaml \
  src/primitive_collision_compiler/baselines/cpd_paper/offline.py \
  tests/test_cpd_paper_offline.py \
  tests/test_cli.py
git commit -m "feat: add CPD paper fixture breadth batch C"
```

- [ ] Push to `origin main` only when this local commit is intended to publish on the shared
  branch. This repository has previously used `origin main` for completed checkpoints; otherwise
  stop at the local commit and report the commit hash.

```bash
git push
```

## Self-Review

- The plan covers exactly the three Batch C fixture ids from
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`.
- Batch C remains offline-only and does not touch Newton, real USD, package generation, or
  benchmark code.
- The positive nonzero threshold fixture intentionally uses the existing component-pair threshold
  path; it does not claim a global topology-edge threshold implementation.
- The next gate advances only to Batch D, while `failure_labels` keeps
  `paper_fixture_breadth_expansion_missing` because Batch D/E remain open.
- The plan contains no TODO/TBD placeholders.
