# CPD Paper Fixture Breadth Completion Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a command-only completion-review payload that closes the planned Batch A-E fixture-breadth gate while keeping the CPD paper offline lane partial.

**Architecture:** The report builder stays in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`. The new payload summarizes Batch A-E fixture evidence, maps it back to the scope-audit blockers, changes the next gate to paper-faithful offline generalization planning, and keeps all package/Newton/real-USD/benchmark triggers false.

**Tech Stack:** Python 3.10+, NumPy, pytest, existing `npc-compile` CLI surface.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`:
  add fixture-breadth batch metadata and a `paper_fixture_breadth_completion_review` payload.
- Modify `tests/test_cpd_paper_offline.py`:
  add RED tests for the new review payload, the next gate, and the updated failure label.
- Modify `tests/test_cli.py`:
  assert the CLI JSON exposes the same review and claim-boundary fields.
- Modify documentation:
  `README.md`, `docs/index.md`, `docs/deepdive/evidence-status.md`,
  `docs/reference/claim-boundaries.md`,
  `docs/reference/cpd-paper-reproduction-gap-matrix.md`,
  `docs/reference/cpd-paper-faithful-offline-lane-spec.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`,
  `docs/reference/cpd-paper-story-status.md`, and `docs/records/README.md`.
- Modify `experiments/registry.yaml`:
  add a completion-review registry entry.
- Create `docs/records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md`:
  record RED/GREEN verification, CLI smoke, full verification, claim impact, and review notes.

## Claim Boundary

This slice may support only:

```text
The repository has completed a fixture-breadth review for the command-only synthetic CPD paper offline lane across planned Batches A-E, and the report remains partial.
```

It must not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Task 1: RED Tests For Completion Review

**Files:**
- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add the focused offline report test**

Append this test near the existing Batch E test in `tests/test_cpd_paper_offline.py`:

```python
def test_cpd_paper_offline_report_records_fixture_breadth_completion_review():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == [
        "paper_faithful_offline_generalization_missing"
    ]
    assert report["next_required_gate"] == "paper_faithful_offline_generalization_plan"
    assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
        "paper_faithful_offline_generalization"
    ]
    assert "paper_fixture_breadth_completion_review" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]

    review = report["paper_fixture_breadth_completion_review"]
    assert review["review_scope"] == "synthetic_fixture_breadth_batches_a_to_e"
    assert review["closed_gate"] == "paper_fixture_breadth_expansion"
    assert review["decision"] == "remain_partial"
    assert review["decision_reason"] == "fixture_breadth_complete_but_generalization_missing"
    assert review["fixture_breadth_plan_complete"] is True
    assert review["paper_faithful_offline_allowed"] is False
    assert review["next_required_gate"] == "paper_faithful_offline_generalization_plan"
    assert review["package_generation_triggered"] is False
    assert review["newton_runtime_triggered"] is False
    assert review["real_usd_triggered"] is False
    assert review["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_fixture_breadth_batch_a",
            "purpose": "source_preprocess_intake_operator_breadth",
            "case_ids": [
                "paper_mixed_face_preprocess_operator",
                "paper_degenerate_preprocess_face_drop",
                "paper_concave_polygon_rejected",
            ],
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_b",
            "purpose": "primitive_fit_breadth",
            "case_ids": [
                "paper_rotated_box_fit",
                "paper_offset_sphere_fit",
                "paper_off_axis_capsule_fit",
                "paper_flat_capped_cylinder_axis_fit",
                "paper_tapered_frustum_fit",
                "paper_asymmetric_trapezoid_fit",
            ],
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_c",
            "purpose": "cost_search_stop_breadth",
            "case_ids": [
                "paper_branching_cost_order",
                "paper_equal_cost_queue_tie",
                "paper_nonzero_threshold_block",
            ],
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_d",
            "purpose": "component_pair_breadth",
            "case_ids": [
                "paper_component_pair_multi_candidate_order",
                "paper_component_pair_cap_skipped",
            ],
            "primary_criteria": [
                "component_pair_edge_handling",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_e",
            "purpose": "postprocess_breadth",
            "case_ids": [
                "paper_rotated_nested_primitive",
                "paper_cross_type_enclosure_boundary",
            ],
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
        },
    ]
    assert review["completed_batches"] == expected_batches
    cases_by_batch = {}
    for case in report["cases"]:
        batch = case.get("fixture_breadth_batch")
        if batch is not None:
            cases_by_batch.setdefault(batch, []).append(case["case_id"])
    assert cases_by_batch == {
        batch["batch_id"]: batch["case_ids"] for batch in expected_batches
    }
    assert review["remaining_blocking_criteria_ids"] == EXPECTED_SCOPE_AUDIT_BLOCKERS
    assert [row["criterion_id"] for row in review["criteria_after_completion"]] == (
        EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert all(
        row["status_after_completion"] == "partial_fixture_scope"
        for row in review["criteria_after_completion"]
    )
    assert all(
        row["remaining_gap"] == "paper_faithful_offline_generalization"
        for row in review["criteria_after_completion"]
    )
```

- [ ] **Step 2: Update the existing offline report status test**

Update all existing focused top-level gate tests in `tests/test_cpd_paper_offline.py`.

Rename and change `test_cpd_paper_offline_report_failure_labels_point_to_fixture_breadth_gap`:

```python
def test_cpd_paper_offline_report_failure_labels_point_to_generalization_gap():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == [
        "paper_faithful_offline_generalization_missing"
    ]
```

Rename and change `test_cpd_paper_offline_report_next_gate_is_fixture_breadth_completion_review`:

```python
def test_cpd_paper_offline_report_next_gate_is_generalization_plan():
    report = build_cpd_paper_offline_report()

    assert report["next_required_gate"] == "paper_faithful_offline_generalization_plan"
```

In `test_cpd_paper_offline_report_covers_first_toy_slice`, change these assertions:

```python
assert report["failure_labels"] == [
    "paper_faithful_offline_generalization_missing"
]
assert report["next_required_gate"] == "paper_faithful_offline_generalization_plan"
assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
    "paper_faithful_offline_generalization"
]
assert "paper_fixture_breadth_completion_review" in report["paper_faithfulness"][
    "implemented_fixture_scope"
]
```

- [ ] **Step 3: Update the CLI test**

In `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json`, change the top-level gate assertions and add review assertions:

```python
assert payload["failure_labels"] == [
    "paper_faithful_offline_generalization_missing"
]
assert payload["next_required_gate"] == "paper_faithful_offline_generalization_plan"
review = payload["paper_fixture_breadth_completion_review"]
assert review["closed_gate"] == "paper_fixture_breadth_expansion"
assert review["fixture_breadth_plan_complete"] is True
assert review["paper_faithful_offline_allowed"] is False
assert review["next_required_gate"] == "paper_faithful_offline_generalization_plan"
assert [batch["batch_id"] for batch in review["completed_batches"]] == [
    "paper_fixture_breadth_batch_a",
    "paper_fixture_breadth_batch_b",
    "paper_fixture_breadth_batch_c",
    "paper_fixture_breadth_batch_d",
    "paper_fixture_breadth_batch_e",
]
assert review["package_generation_triggered"] is False
assert review["newton_runtime_triggered"] is False
assert review["real_usd_triggered"] is False
assert review["benchmark_triggered"] is False
```

- [ ] **Step 4: Run RED tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: FAIL because the report still has `failure_labels:
["paper_fixture_breadth_expansion_missing"]`, still points to
`paper_fixture_breadth_completion_review`, and lacks the
`paper_fixture_breadth_completion_review` payload.

## Task 2: Implement Completion Review Payload

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add batch metadata helpers**

Add these helpers near `_paper_faithful_offline_scope_audit_payload()`:

```python
def _paper_fixture_breadth_completed_batches() -> list[dict[str, object]]:
    return [
        {
            "batch_id": "paper_fixture_breadth_batch_a",
            "purpose": "source_preprocess_intake_operator_breadth",
            "case_ids": [
                "paper_mixed_face_preprocess_operator",
                "paper_degenerate_preprocess_face_drop",
                "paper_concave_polygon_rejected",
            ],
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_b",
            "purpose": "primitive_fit_breadth",
            "case_ids": [
                "paper_rotated_box_fit",
                "paper_offset_sphere_fit",
                "paper_off_axis_capsule_fit",
                "paper_flat_capped_cylinder_axis_fit",
                "paper_tapered_frustum_fit",
                "paper_asymmetric_trapezoid_fit",
            ],
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_c",
            "purpose": "cost_search_stop_breadth",
            "case_ids": [
                "paper_branching_cost_order",
                "paper_equal_cost_queue_tie",
                "paper_nonzero_threshold_block",
            ],
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_d",
            "purpose": "component_pair_breadth",
            "case_ids": [
                "paper_component_pair_multi_candidate_order",
                "paper_component_pair_cap_skipped",
            ],
            "primary_criteria": [
                "component_pair_edge_handling",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_e",
            "purpose": "postprocess_breadth",
            "case_ids": [
                "paper_rotated_nested_primitive",
                "paper_cross_type_enclosure_boundary",
            ],
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
        },
    ]
```

- [ ] **Step 2: Add the review payload helper**

Add this helper after the batch metadata helper:

```python
def _paper_fixture_breadth_completion_review_payload() -> dict[str, object]:
    criteria = [
        row
        for row in _paper_faithful_offline_scope_criteria()
        if row["blocking_for_paper_faithful_offline"]
    ]
    remaining_blockers = [str(row["criterion_id"]) for row in criteria]
    return {
        "review_scope": "synthetic_fixture_breadth_batches_a_to_e",
        "closed_gate": "paper_fixture_breadth_expansion",
        "decision": "remain_partial",
        "decision_reason": "fixture_breadth_complete_but_generalization_missing",
        "fixture_breadth_plan_complete": True,
        "paper_faithful_offline_allowed": False,
        "next_required_gate": "paper_faithful_offline_generalization_plan",
        "completed_batches": _paper_fixture_breadth_completed_batches(),
        "criteria_after_completion": [
            {
                "criterion_id": str(row["criterion_id"]),
                "fixture_breadth_status": "covered_by_named_synthetic_fixtures",
                "status_after_completion": "partial_fixture_scope",
                "remaining_gap": "paper_faithful_offline_generalization",
                "claim_boundary": str(row["claim_boundary"]),
            }
            for row in criteria
        ],
        "remaining_blocking_criteria_ids": remaining_blockers,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] **Step 3: Wire the helper into `build_cpd_paper_offline_report()`**

Change `missing_before_paper_faithful`:

```python
missing_before_paper_faithful = [
    "paper_faithful_offline_generalization",
]
```

Change `next_required_gate`:

```python
"next_required_gate": "paper_faithful_offline_generalization_plan",
```

Add the implemented fixture scope item:

```python
"paper_fixture_breadth_completion_review",
```

Add the top-level report payload:

```python
"paper_fixture_breadth_completion_review": (
    _paper_fixture_breadth_completion_review_payload()
),
```

- [ ] **Step 4: Run GREEN focused tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_completion_review tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: PASS.

- [ ] **Step 5: Run the renamed top-level gate tests**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_generalization_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_generalization_plan -q
```

Expected: PASS.

## Task 3: Documentation, Record, And Registry

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
- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md`

- [ ] **Step 1: Update canonical docs**

Update wording in the exact stale next-gate surfaces:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-story-status.md`

Replace stale "completion review is next" wording with the narrower completed-review status:

```text
The command-only synthetic CPD paper offline lane now includes a fixture-breadth completion review
for planned Batches A-E. The report remains partial, `paper_faithful_offline_supported` remains
false, and the next gate is `paper_faithful_offline_generalization_plan`.
```

Define the next gate everywhere it is introduced:

```text
`paper_faithful_offline_generalization_plan` is a planning-only gate for broadening the offline
algorithm beyond named toy fixtures. It is not `paper_faithful_offline` support.
```

Keep these explicit negatives in reviewer-facing docs:

```text
This review does not support paper_faithful_offline, full CPD reproduction, package generation,
Newton runtime execution, real-USD evidence, collision-quality evidence, benchmark evidence,
deployment readiness, or safety certification.
```

- [ ] **Step 2: Add registry entry**

Add this entry after `cpd-paper-fixture-breadth-batch-e`:

```yaml
  - id: cpd-paper-fixture-breadth-completion-review
    status: in_progress
    command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
    record: docs/records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md
    purpose: >
      Add a command-only completion review for planned CPD paper fixture-breadth
      Batches A-E.
    claims_supported:
      - partial fixture-scoped completion review for planned synthetic Batch A-E breadth only
      - records the closed paper_fixture_breadth_expansion gate and the next gate paper_faithful_offline_generalization_plan
      - no paper_faithful_offline claim, full CPD reproduction claim, package-generation claim, Newton runtime claim, real-USD claim, collision-quality claim, benchmark-suite claim, deployment claim, or safety-certification claim
```

- [ ] **Step 3: Add pending record**

Create `docs/records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md` with status `In progress`, the planned changes, and clearly marked evidence fields for concrete command output that will be filled before final commit. The record must already state the claim boundary and next action.

- [ ] **Step 4: Run docs validators**

Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: all pass.

## Task 4: Review, Final Verification, And Commit

**Files:**
- All files changed by Tasks 1-3.

- [ ] **Step 1: Run focused CLI smoke**

Run:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report > /tmp/cpd_paper_offline_completion_review.json
python - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/cpd_paper_offline_completion_review.json").read_text())
review = report["paper_fixture_breadth_completion_review"]
print(report["failure_labels"])
print(report["next_required_gate"])
print(review["closed_gate"])
print(review["fixture_breadth_plan_complete"])
print([batch["batch_id"] for batch in review["completed_batches"]])
print(review["remaining_blocking_criteria_ids"])
print(
    review["package_generation_triggered"],
    review["newton_runtime_triggered"],
    review["real_usd_triggered"],
    review["benchmark_triggered"],
)
PY
```

Expected:

```text
['paper_faithful_offline_generalization_missing']
paper_faithful_offline_generalization_plan
paper_fixture_breadth_expansion
True
['paper_fixture_breadth_batch_a', 'paper_fixture_breadth_batch_b', 'paper_fixture_breadth_batch_c', 'paper_fixture_breadth_batch_d', 'paper_fixture_breadth_batch_e']
['source_mesh_and_preprocessing_policy', 'source_face_intake_policy', 'operator_q_audit', 'primitive_vocabulary_and_fit', 'paper_collapse_cost_and_weighting', 'greedy_priority_queue_trace', 'target_count_and_threshold_stop', 'component_pair_edge_handling', 'enclosed_primitive_postprocess']
False False False False
```

- [ ] **Step 2: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

Expected: pytest reports all tests passed; docs validators pass; `git diff --check` emits no output.

- [ ] **Step 3: Attempt multi-agent review and record result**

Request independent review from implementation, paper-claim-boundary, and documentation angles. If the platform quota blocks subagents, record the failed attempt exactly and perform a local fallback review from the same three angles.

- [ ] **Step 4: Finalize record and registry**

Replace `In progress` with `Complete`, add exact command output summaries, and change the registry entry to `complete`.

- [ ] **Step 5: Commit and push**

Run:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md experiments/registry.yaml
git commit -m "feat: add CPD paper fixture breadth completion review"
git push
```

Expected: commit succeeds and push updates `origin/main`.

## Self-Review

- Spec coverage: this plan covers the report payload, tests, CLI, docs, registry, record, verification, and review requirement for the completion-review gate.
- Unresolved-marker scan: no incomplete or unspecified behavior remains in implementation steps.
- Scope boundary: the plan closes only `paper_fixture_breadth_expansion`; it keeps the report partial and does not enter package generation, Newton runtime, real USD, or benchmarks.
- Type consistency: all new field names use JSON-compatible dict/list/string/bool values and match the test snippets.
