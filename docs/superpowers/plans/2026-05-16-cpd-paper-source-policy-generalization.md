# CPD Paper Source Policy Generalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close only `paper_generalization_batch_a_source_policy` by adding a bounded offline
source-policy generalization payload to `cpd_paper_offline_report`.

**Architecture:** Keep the report in `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
and keep it `partial`. The new payload is derived from existing synthetic fixture case payloads,
advances the next gate to `paper_generalization_batch_b_primitive_fit_engine`, and keeps package
generation, Newton runtime, real USD, and benchmark work blocked.

**Tech Stack:** Python 3.10+, NumPy, pytest, existing `npc-compile` CLI JSON surface, Markdown docs.

---

## File Structure

- Modify `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`:
  add `_paper_source_policy_generalization_payload(cases)`, centralize remaining generalization
  gates, advance current next-gate metadata to Batch B, and keep the report partial.
- Modify `tests/test_cpd_paper_offline.py`:
  add RED tests for the source-policy payload and case-row consistency, then update existing
  current gate expectations from Batch A to Batch B.
- Modify `tests/test_cli.py`:
  assert the CLI exposes the Batch A source-policy payload while B-E remain missing.
- Modify documentation:
  `README.md`, `docs/index.md`, `docs/deepdive/evidence-status.md`,
  `docs/reference/claim-boundaries.md`,
  `docs/reference/cpd-paper-reproduction-gap-matrix.md`,
  `docs/reference/cpd-paper-faithful-offline-lane-spec.md`,
  `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`,
  `docs/reference/cpd-paper-story-status.md`, and `docs/records/README.md`.
- Modify `experiments/registry.yaml`:
  add a registry entry for the source-policy generalization report gate.
- Create `docs/records/2026-05-16-cpd-paper-generalization-batch-a-source-policy.md`:
  record RED/GREEN verification, CLI smoke, full verification, review notes, and claim impact.

## Claim Boundary

This slice may support only:

```text
The command-only `cpd_paper_offline_report` now includes an offline source-policy
generalization matrix for deterministic synthetic meshes, and the report remains partial.
```

It must not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- robust arbitrary mesh cleanup;
- general polygon mesh intake;
- primitive-fit/search/postprocess/package generalization;
- package generation;
- Newton runtime execution;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Task 1: RED Tests For Source Policy Generalization

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add focused report payload test**

Add `test_cpd_paper_offline_report_records_source_policy_generalization_gate()` near the existing
generalization-plan test. It should assert:

```python
remaining_gates = [
    "paper_generalization_batch_b_primitive_fit_engine",
    "paper_generalization_batch_c_search_engine",
    "paper_generalization_batch_d_postprocess_policy",
    "paper_generalization_batch_e_package_boundary_readiness",
]

assert report["failure_labels"] == [f"{gate}_missing" for gate in remaining_gates]
assert report["next_required_gate"] == "paper_generalization_batch_b_primitive_fit_engine"
assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == remaining_gates
assert "paper_generalization_batch_a_source_policy" in report["paper_faithfulness"][
    "implemented_generalization_scope"
]
assert report["paper_faithful_offline_supported"] is False

payload = report["paper_generalization_batch_a_source_policy"]
assert payload["gate_id"] == "paper_generalization_batch_a_source_policy"
assert payload["gate_status"] == "implemented_offline_report_only_partial"
assert payload["closed_gate"] == "paper_generalization_batch_a_source_policy"
assert payload["next_required_gate"] == "paper_generalization_batch_b_primitive_fit_engine"
assert payload["decision"] == "remain_partial"
assert payload["paper_faithful_offline_allowed"] is False
assert payload["source_scope"] == "synthetic_in_memory_source_mesh_policy_matrix"
assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
assert payload["source_mesh_contract"] == {
    "accepted_source_representation": "vertices_plus_variable_arity_source_faces",
    "source_face_id_policy": "preserve_source_face_ids_distinct_from_generated_triangle_ids",
    "general_mesh_cleanup_supported": False,
}
assert payload["preprocessing_policy"]["deduplication_policy"] == (
    "exact_coordinate_first_occurrence_only"
)
assert payload["preprocessing_policy"]["distance_tolerance"] == 0.0
assert payload["preprocessing_policy"]["degenerate_face_policy"] == (
    "drop_after_exact_deduplication_from_executable_rows"
)
assert payload["source_face_intake_policy"]["accepted_preconditions"] == [
    "planar",
    "convex",
    "non_degenerate",
    "consistently_wound",
]
assert payload["source_face_intake_policy"]["triangulation_policy"] == (
    "fan_from_first_vertex"
)
assert payload["source_face_intake_policy"]["unsupported_policy"] == (
    "reject_concave_polygon_without_top_level_failure_label"
)
assert payload["operator_policy"]["triangle_operator_policy"] == (
    "compute_q_on_executable_triangles"
)
assert payload["operator_policy"]["source_face_aggregate_policy"] == (
    "sum_generated_triangle_q_rows_to_source_face"
)
assert payload["package_generation_triggered"] is False
assert payload["newton_runtime_triggered"] is False
assert payload["real_usd_triggered"] is False
assert payload["benchmark_triggered"] is False
assert [row["policy_row_id"] for row in payload["policy_matrix"]] == [
    "accepted_mixed_triangle_quad_polygon_exact_dedup",
    "accepted_degenerate_after_exact_dedup_drop",
    "rejected_concave_polygon",
]
assert payload["coverage_summary"] == {
    "evidence_case_count": 3,
    "accepted_policy_row_count": 2,
    "unsupported_policy_row_count": 1,
    "closed_gate_count": 1,
    "remaining_generalization_gate_count": 4,
}
assert payload["remaining_gaps"] == remaining_gates
```

- [ ] **Step 2: Add fixture-row consistency test**

Add `test_cpd_paper_source_policy_generalization_rows_match_case_payloads()`. It should build
`cases = {case["case_id"]: case for case in report["cases"]}` and verify:

```python
payload = report["paper_generalization_batch_a_source_policy"]
rows = {row["policy_row_id"]: row for row in payload["policy_matrix"]}

mixed = cases["paper_mixed_face_preprocess_operator"]
mixed_row = rows["accepted_mixed_triangle_quad_polygon_exact_dedup"]
assert mixed_row["evidence_case_id"] == mixed["case_id"]
assert mixed_row["source_face_arities"] == mixed["source_mesh"]["source_face_arities"]
assert mixed_row["source_face_count"] == mixed["source_mesh"]["source_face_count"]
assert mixed_row["triangulated_face_count"] == mixed["source_mesh"]["triangulated_face_count"]
assert mixed_row["duplicate_vertex_preprocessing"] == mixed["source_mesh"][
    "duplicate_vertex_preprocessing"
]
assert mixed_row["operator_aggregate_count"] == len(
    mixed["operator_audit"]["source_face_operator_aggregates"]
)
aggregates = mixed["operator_audit"]["source_face_operator_aggregates"]
assert mixed_row["operator_aggregate_source_face_ids"] == [
    aggregate["source_face_id"] for aggregate in aggregates
]
assert mixed_row["operator_aggregate_generated_triangle_face_ids"] == [
    aggregate["generated_triangle_face_ids"] for aggregate in aggregates
]
assert mixed_row["operator_q_aggregation_policy"] == (
    "aggregate_q_matrix_equals_sum_generated_triangle_q_rows"
)
face_q_by_id = {
    face["face_id"]: face["q_matrix"] for face in mixed["operator_audit"]["faces"]
}
for aggregate in aggregates:
    expected_q = [
        [
            sum(
                face_q_by_id[face_id][row_index][col_index]
                for face_id in aggregate["generated_triangle_face_ids"]
            )
            for col_index in range(3)
        ]
        for row_index in range(3)
    ]
    assert aggregate["q_matrix"] == expected_q

degenerate = cases["paper_degenerate_preprocess_face_drop"]
degenerate_row = rows["accepted_degenerate_after_exact_dedup_drop"]
assert degenerate_row["dropped_source_face_ids"] == degenerate["preprocessing_audit"][
    "dropped_source_face_ids"
]
assert degenerate_row["executable_source_face_ids"] == degenerate["source_mesh"][
    "executable_source_face_ids"
]
assert degenerate_row["operator_source_faces"] == degenerate["operator_audit"]["merged_group"][
    "source_faces"
]
assert degenerate_row["primitive_fit_source_faces"] == degenerate["primitive_fit_audit"][
    "source_faces"
]

concave = cases["paper_concave_polygon_rejected"]
concave_row = rows["rejected_concave_polygon"]
assert concave_row["case_status"] == concave["case_status"]
assert concave_row["failure_label"] == concave["mesh_intake_policy_audit"]["failure_label"]
assert concave_row["top_level_failure_label"] is False
assert concave_row["triangulated_face_count"] == 0
assert concave_row["operator_row_count"] == 0
assert concave_row["primitive_fit_row_count"] == 0
```

- [ ] **Step 3: Update existing report expectations**

Change the current expected generalization gates to B-E and the current top-level next gate to
`paper_generalization_batch_b_primitive_fit_engine`. Keep
`paper_fixture_breadth_completion_review["next_required_gate"] ==
"paper_faithful_offline_generalization_plan"` unchanged because it is historical.

- [ ] **Step 4: Update CLI expectations**

In `test_cli_run_cpd_paper_offline_report_emits_json()`, assert B-E failure labels, Batch B next
gate, and the new `paper_generalization_batch_a_source_policy` payload with false runtime triggers.

- [ ] **Step 5: Run RED commands**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_source_policy_generalization_gate -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_source_policy_generalization_rows_match_case_payloads -q
python -m pytest tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: failures show missing payload or stale Batch A next-gate/failure-label behavior.

## Task 2: Implement The Offline Payload

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] **Step 1: Add gate constants**

Add constants:

```python
_PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY = "paper_generalization_batch_a_source_policy"
_PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT = "paper_generalization_batch_b_primitive_fit_engine"
```

Use them for current next-gate and failure-label construction.

- [ ] **Step 2: Add source-policy payload helper**

Implement `_paper_source_policy_generalization_payload(cases)` so it finds the three evidence cases
by `case_id`, creates `source_mesh_contract`, `preprocessing_policy`, `source_face_intake_policy`,
`operator_policy`, `policy_matrix`, `coverage_summary`, and `remaining_gaps`, and keeps all triggers
false.

- [ ] **Step 3: Advance gate metadata**

Change `build_cpd_paper_offline_report()` so `missing_before_paper_faithful` is B-E, the top-level
`next_required_gate` is Batch B, and `paper_faithfulness.implemented_generalization_scope` contains
Batch A.

- [ ] **Step 4: Update generalization-plan current fields**

Keep the full planned Batch A-E table as historical/current plan content, but set
`decision_reason`, `next_required_gate`, `first_unresolved_gate`, and `remaining_generalization_gates`
to reflect Batch B as the first unresolved implementation gate.

- [ ] **Step 5: Run GREEN focused tests**

Run the same focused commands from Task 1 and confirm they pass.

## Task 3: Documentation And Record Updates

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
- Create: `docs/records/2026-05-16-cpd-paper-generalization-batch-a-source-policy.md`

- [ ] **Step 1: Update current-status wording**

Replace current wording that says the next gate is `paper_generalization_batch_a_source_policy` with
wording that says this gate is now implemented as an offline report-only source-policy matrix and
the next gate is `paper_generalization_batch_b_primitive_fit_engine`.

- [ ] **Step 2: Keep historical wording intact**

Do not rewrite old records or old implementation plans where Batch A was correctly a future gate at
the time of those records. Only update current-status docs and the new record.

- [ ] **Step 3: Add registry entry**

Add an executable registry entry for the same command:

```yaml
- id: cpd-paper-generalization-batch-a-source-policy
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

The claims must say this is partial offline source-policy generalization only, with B-E still
missing and no package/Newton/real-USD/benchmark evidence.

- [ ] **Step 4: Add dated record**

Create the record with:

```markdown
# 2026-05-16 CPD Paper Generalization Batch A Source Policy

## Status

Complete
```

Record RED/GREEN commands, CLI smoke, validation commands, review findings, claim impact, and next
gate.

## Task 4: Review, Verify, Commit, And Push

**Files:** all changed files.

- [ ] **Step 1: Run focused and full verification**

Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] **Step 2: Dispatch multi-agent review**

Dispatch at least three read-only agents:

```text
Agent 1: implementation/TDD/schema review.
Agent 2: claim-boundary and paper-story review.
Agent 3: docs/registry/record stale-wording review.
```

- [ ] **Step 3: Fix Critical and Important findings**

Apply verified review feedback with `superpowers:receiving-code-review`, then rerun the affected
tests and validators.

- [ ] **Step 4: Final verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] **Step 5: Commit, merge, push, and clean this worktree**

Use:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py README.md docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-generalization-batch-a-source-policy.md docs/superpowers/specs/2026-05-16-cpd-paper-source-policy-generalization-design.md docs/superpowers/plans/2026-05-16-cpd-paper-source-policy-generalization.md experiments/registry.yaml
git commit -m "feat: add CPD paper source policy generalization"
```

Then fast-forward merge to `main`, push `origin main`, and remove only this feature worktree.
