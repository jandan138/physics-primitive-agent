# CPD Paper Faithful Offline Scope Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a top-level offline scope audit to `cpd_paper_offline_report` that explicitly keeps
the paper lane partial and points the next gate to fixture-breadth expansion.

**Architecture:** Keep the report command offline-only. Add a deterministic, static
criteria-table payload inside `offline.py`, test it through direct report and CLI JSON, and update
claim-boundary docs and registry records. The audit does not change primitive fitting, merge
search, package generation, Newton runtime behavior, real USD handling, or benchmark execution.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Update top-level direct-report tests to expect:

```python
assert report["failure_labels"] == ["paper_fixture_breadth_expansion_missing"]
assert report["next_required_gate"] == "paper_fixture_breadth_expansion_plan"
assert report["status"] == "partial"
assert report["paper_faithful_offline_supported"] is False
assert report["paper_faithfulness"]["missing_before_paper_faithful_offline"] == [
    "paper_fixture_breadth_expansion"
]
```

- [ ] Rename the two top-level gate tests so their names match the new behavior:

```python
def test_cpd_paper_offline_report_failure_labels_point_to_fixture_breadth_gap():
    report = build_cpd_paper_offline_report()
    assert report["failure_labels"] == ["paper_fixture_breadth_expansion_missing"]


def test_cpd_paper_offline_report_next_gate_is_fixture_breadth_plan():
    report = build_cpd_paper_offline_report()
    assert report["next_required_gate"] == "paper_fixture_breadth_expansion_plan"
```

- [ ] Assert `paper_faithful_offline_scope_audit` is present in
  `report["paper_faithfulness"]["implemented_fixture_scope"]`.

- [ ] Add helper constants in `tests/test_cpd_paper_offline.py`:

```python
EXPECTED_SCOPE_AUDIT_CRITERIA = [
    "source_mesh_and_preprocessing_policy",
    "source_face_intake_policy",
    "operator_q_audit",
    "primitive_vocabulary_and_fit",
    "paper_collapse_cost_and_weighting",
    "greedy_priority_queue_trace",
    "target_count_and_threshold_stop",
    "component_pair_edge_handling",
    "enclosed_primitive_postprocess",
    "report_schema_tests_and_records",
    "package_generation_boundary",
    "newton_runtime_boundary",
    "real_usd_boundary",
    "benchmark_evaluation_boundary",
]

EXPECTED_SCOPE_AUDIT_BLOCKERS = [
    "source_mesh_and_preprocessing_policy",
    "source_face_intake_policy",
    "operator_q_audit",
    "primitive_vocabulary_and_fit",
    "paper_collapse_cost_and_weighting",
    "greedy_priority_queue_trace",
    "target_count_and_threshold_stop",
    "component_pair_edge_handling",
    "enclosed_primitive_postprocess",
]

EXPECTED_SCOPE_AUDIT_ROWS = [
    {
        "criterion_id": "source_mesh_and_preprocessing_policy",
        "paper_requirement": (
            "Mesh vertices/faces plus duplicate or overlapped vertex preprocessing "
            "and source-face remap."
        ),
        "current_evidence": (
            "Triangle toy fixtures, fan-triangulated source-face fixtures, and one "
            "exact-coordinate duplicate-vertex fixture; broader unclean-mesh policy is absent."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Exact-overlap toy preprocessing only; no robust arbitrary mesh cleanup."
        ),
        "next_action": (
            "Expand preprocessing/source-mesh fixture breadth before stronger wording."
        ),
    },
    {
        "criterion_id": "source_face_intake_policy",
        "paper_requirement": (
            "Preserve face ownership across triangle, quad, and polygon source faces."
        ),
        "current_evidence": (
            "One quad and one five-vertex polygon fan-triangulation fixture with "
            "source-face remap and operator ownership accounting."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Source-face intake is toy-scoped, not a general polygon mesh implementation."
        ),
        "next_action": "Add broader source-face cases only after a fixture-breadth plan.",
    },
    {
        "criterion_id": "operator_q_audit",
        "paper_requirement": (
            "Per-face and merged-group Q operators with eigen decomposition."
        ),
        "current_evidence": (
            "Per-face and merged-group operator rows exist for named toy fixtures, "
            "including source-face aggregate rows."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Operator evidence is named-fixture audit data, not full paper decomposition."
        ),
        "next_action": "Expand operator degeneracy and fixture coverage.",
    },
    {
        "criterion_id": "primitive_vocabulary_and_fit",
        "paper_requirement": (
            "Audit the six paper primitive candidates, containment, formulas, axis "
            "policies, and primitive weights."
        ),
        "current_evidence": (
            "All six paper primitive names have fixture-scoped audit rows, but capped "
            "cylinder, frustum, and trapezoidal prism remain offline-only and fitting "
            "breadth is limited."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Primitive rows are audit rows, not Newton runtime support or "
            "collision-quality evidence."
        ),
        "next_action": "Expand fitting fixtures and paper-specific invariants.",
    },
    {
        "criterion_id": "paper_collapse_cost_and_weighting",
        "paper_requirement": (
            "Use paper base collapse cost, separate weighted priority cost, and no "
            "intersection-volume primary cost."
        ),
        "current_evidence": (
            "One two-face cost fixture plus priority-queue event fields record base "
            "and weighted costs."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": "Cost rows are toy accounting, not optimizer or benchmark evidence.",
        "next_action": "Broaden merge-cost fixtures and threshold cases.",
    },
    {
        "criterion_id": "greedy_priority_queue_trace",
        "paper_requirement": (
            "Initialize adjacent face-pair candidates, pop minimum priority cost, "
            "handle stale entries, and merge greedily."
        ),
        "current_evidence": (
            "Topology, deduplicated-topology, and component-pair toy traces exist "
            "with deterministic queue keys."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Search traces are toy-scoped and do not prove merge-policy superiority."
        ),
        "next_action": "Expand priority-queue fixtures before stronger wording.",
    },
    {
        "criterion_id": "target_count_and_threshold_stop",
        "paper_requirement": (
            "Stop at target primitive count or when valid threshold policy blocks "
            "remaining candidates."
        ),
        "current_evidence": (
            "Target-count traces and one zero finite-threshold component-pair block exist."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": "Threshold evidence is narrow toy accounting.",
        "next_action": "Add fixture-breadth plan for target/threshold combinations.",
    },
    {
        "criterion_id": "component_pair_edge_handling",
        "paper_requirement": (
            "Insert pairwise component candidates when disconnected topology cannot "
            "reach the target."
        ),
        "current_evidence": (
            "One accepted threshold-disabled component-pair trace and one finite-threshold "
            "blocked trace exist."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Component merging evidence is diagnostic accounting, not broad asset evidence."
        ),
        "next_action": "Decide whether capped skipped-pair fixtures are needed.",
    },
    {
        "criterion_id": "enclosed_primitive_postprocess",
        "paper_requirement": "Remove primitives enclosed by other primitives.",
        "current_evidence": (
            "One explicit identity-axis nested OBB cull fixture exists; generated-search "
            "postprocess breadth is absent."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Postprocess cull evidence is one offline canary, not a general containment library."
        ),
        "next_action": "Expand postprocess fixtures if required by scope audit follow-up.",
    },
    {
        "criterion_id": "report_schema_tests_and_records",
        "paper_requirement": (
            "Keep report schema, tests, registry, and dated records reproducible."
        ),
        "current_evidence": (
            "This slice adds RED/GREEN tests, final verification, registry entry, "
            "and a dated record."
        ),
        "status": "implemented_fixture_scope",
        "surrogate_or_paper_faithful": "paper_aligned_boundary",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": (
            "Reproducibility evidence supports the audit record only, not stronger "
            "algorithm claims."
        ),
        "next_action": "Keep records updated for every future gate.",
    },
    {
        "criterion_id": "package_generation_boundary",
        "paper_requirement": "Keep offline paper mechanics separate from package conversion.",
        "current_evidence": (
            "The report records package-generation false triggers and no CollisionPackage conversion."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Package generation is a later explicit adapter gate.",
        "next_action": (
            "Add package conversion only after a changed offline package boundary exists."
        ),
    },
    {
        "criterion_id": "newton_runtime_boundary",
        "paper_requirement": (
            "Keep offline paper mechanics separate from Newton runtime diagnostics."
        ),
        "current_evidence": "The report records Newton false triggers and no runtime execution.",
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Newton support requires separate mapping and diagnostic records.",
        "next_action": (
            "Run Newton only after package conversion and runtime admissibility are recorded."
        ),
    },
    {
        "criterion_id": "real_usd_boundary",
        "paper_requirement": "Keep toy fixture audit separate from real asset evidence.",
        "current_evidence": (
            "The report records real-USD false triggers and uses synthetic toy fixtures only."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Real-USD evidence requires separate asset manifests and records.",
        "next_action": (
            "Defer bed/Franka or other real assets until a package-changing gate exists."
        ),
    },
    {
        "criterion_id": "benchmark_evaluation_boundary",
        "paper_requirement": (
            "Keep paper benchmark evaluation separate from offline paper-mechanics audit."
        ),
        "current_evidence": (
            "The report records benchmark false triggers and no timing, surface-distance, "
            "byte-cost, or baseline comparison metrics."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": (
            "Benchmark evidence is not required for bounded offline status and is not claimed here."
        ),
        "next_action": (
            "Defer benchmarks until offline decomposition and runtime package gates are ready."
        ),
    },
]
```

- [ ] Add direct-report assertions:

```python
scope_audit = report["paper_faithful_offline_scope_audit"]
assert scope_audit["audit_scope"] == "fixture_scoped_offline_paper_lane"
assert scope_audit["audit_version"] == 1
assert scope_audit["decision"] == "remain_partial"
assert scope_audit["paper_faithful_offline_allowed"] is False
assert scope_audit["decision_reason"] == "fixture_scope_still_partial"
assert scope_audit["blocking_criteria_ids"] == EXPECTED_SCOPE_AUDIT_BLOCKERS
assert scope_audit["package_generation_triggered"] is False
assert scope_audit["newton_runtime_triggered"] is False
assert scope_audit["real_usd_triggered"] is False
assert scope_audit["benchmark_triggered"] is False
criteria = scope_audit["criteria"]
assert [row["criterion_id"] for row in criteria] == EXPECTED_SCOPE_AUDIT_CRITERIA
assert criteria == EXPECTED_SCOPE_AUDIT_ROWS
for row in criteria:
    assert set(row) == {
        "criterion_id",
        "paper_requirement",
        "current_evidence",
        "status",
        "surrogate_or_paper_faithful",
        "blocking_for_paper_faithful_offline",
        "claim_boundary",
        "next_action",
    }
    assert row["status"] in {
        "implemented_fixture_scope",
        "partial_fixture_scope",
        "not_started",
        "blocked_until_later_gate",
    }
    assert row["status"] != "paper_faithful_offline"
    assert row["surrogate_or_paper_faithful"] in {
        "fixture_scoped_paper_shaped",
        "paper_aligned_boundary",
        "not_paper_faithful",
        "out_of_offline_scope",
    }
    assert row["surrogate_or_paper_faithful"] != "paper_faithful_offline"
record_row = [
    row for row in criteria if row["criterion_id"] == "report_schema_tests_and_records"
][0]
assert record_row["status"] == "implemented_fixture_scope"
assert record_row["blocking_for_paper_faithful_offline"] is False
newton_row = [
    row for row in criteria if row["criterion_id"] == "newton_runtime_boundary"
][0]
assert newton_row["status"] == "blocked_until_later_gate"
assert newton_row["blocking_for_paper_faithful_offline"] is False
for boundary_id in [
    "package_generation_boundary",
    "real_usd_boundary",
    "benchmark_evaluation_boundary",
]:
    boundary_row = [row for row in criteria if row["criterion_id"] == boundary_id][0]
    assert boundary_row["status"] == "blocked_until_later_gate"
    assert boundary_row["blocking_for_paper_faithful_offline"] is False
```

- [ ] Strengthen `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to assert
  the CLI payload includes the new scope audit, the new failure label, the new next gate, and the
  same criteria id order.

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_fixture_breadth_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_plan tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: failures for the old scope-missing failure label, old scope-audit next gate, missing
implemented scope entry, and missing `paper_faithful_offline_scope_audit` payload.

### Task 2: Scope Audit Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Add `_SCOPE_AUDIT_ALLOWED_STATUSES`:

```python
_SCOPE_AUDIT_ALLOWED_STATUSES = {
    "implemented_fixture_scope",
    "partial_fixture_scope",
    "not_started",
    "blocked_until_later_gate",
}
_SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS = {
    "fixture_scoped_paper_shaped",
    "paper_aligned_boundary",
    "not_paper_faithful",
    "out_of_offline_scope",
}
```

- [ ] Add `_paper_faithful_offline_scope_criteria()` returning the fourteen criteria rows from the
  design spec's "Canonical Criteria Table" in exact order. Copy the row meanings into concrete
  strings; do not replace them with generic text. Every row must include:

```python
{
    "criterion_id": "source_mesh_and_preprocessing_policy",
    "paper_requirement": (
        "Mesh vertices/faces plus duplicate or overlapped vertex preprocessing "
        "and source-face remap."
    ),
    "current_evidence": (
        "Triangle toy fixtures, fan-triangulated source-face fixtures, and one "
        "exact-coordinate duplicate-vertex fixture; broader unclean-mesh policy is absent."
    ),
    "status": "partial_fixture_scope",
    "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
    "blocking_for_paper_faithful_offline": True,
    "claim_boundary": (
        "Exact-overlap toy preprocessing only; no robust arbitrary mesh cleanup."
    ),
    "next_action": (
        "Expand preprocessing/source-mesh fixture breadth before stronger wording."
    ),
}
```

- [ ] Add `_paper_faithful_offline_scope_audit_payload()`:

```python
def _paper_faithful_offline_scope_audit_payload() -> dict[str, object]:
    criteria = _paper_faithful_offline_scope_criteria()
    blocking = [
        row["criterion_id"]
        for row in criteria
        if row["blocking_for_paper_faithful_offline"]
    ]
    return {
        "audit_scope": "fixture_scoped_offline_paper_lane",
        "audit_version": 1,
        "decision": "remain_partial",
        "paper_faithful_offline_allowed": False,
        "decision_reason": "fixture_scope_still_partial",
        "criteria": criteria,
        "blocking_criteria_ids": blocking,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
```

- [ ] Add a small guard in `_paper_faithful_offline_scope_criteria()` or its caller:

```python
for row in criteria:
    if row["status"] not in _SCOPE_AUDIT_ALLOWED_STATUSES:
        raise ValueError(f"unsupported scope audit status: {row['status']}")
    if row["surrogate_or_paper_faithful"] not in _SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS:
        raise ValueError(
            "unsupported scope audit alignment label: "
            f"{row['surrogate_or_paper_faithful']}"
        )
```

- [ ] Update `build_cpd_paper_offline_report()`:

```python
missing_before_paper_faithful = ["paper_fixture_breadth_expansion"]
"next_required_gate": "paper_fixture_breadth_expansion_plan"
"paper_faithful_offline_scope_audit" in implemented_fixture_scope
"paper_faithful_offline_scope_audit": _paper_faithful_offline_scope_audit_payload()
```

- [ ] Run the RED command from Task 1 again.

Expected: all selected tests pass.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md`

- [ ] Update current paper-lane wording to say the report now includes
  `paper_faithful_offline_scope_audit`.
- [ ] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [ ] Add `paper_fixture_breadth_expansion_missing` as the current failure label.
- [ ] Make `paper_fixture_breadth_expansion_plan` the next gate.
- [ ] Add a registry entry:

```yaml
- id: cpd-paper-faithful-offline-scope-audit
  status: complete
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
  record: docs/records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md
  purpose: >
    Extend the command-only partial offline CPD paper-lane audit with a scope-audit table that
    keeps the lane partial and advances the next gate to fixture-breadth expansion.
  claims_supported:
    - partial fixture-scoped offline scope audit only
    - records criteria, blockers, non-blocking runtime/asset/benchmark boundaries, and the remain_partial decision
    - no paper_faithful_offline claim, full CPD reproduction claim, package-generation claim, Newton runtime claim, real-USD claim, collision-quality claim, benchmark-suite claim, deployment claim, or safety-certification claim
```

Claims must be limited to a scope audit that keeps the offline lane partial. No
`paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime, real-USD,
benchmark, collision-quality, deployment, or safety-certification claim is allowed.

- [ ] Create the dated record with `## Status` set to `Complete`, RED/GREEN commands, CLI smoke,
  multi-agent review notes, final verification commands, claim impact, and next action
  `paper_fixture_breadth_expansion_plan`.

### Task 4: Verification And Review

- [ ] Run focused pytest:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
```

- [ ] Run CLI smoke:

```bash
python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

- [ ] Run full verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] Request multi-agent implementation review for:
  - scope-audit criteria correctness versus gap matrix/offline lane spec;
  - test coverage and report schema clarity;
  - docs and claim-boundary consistency.

- [ ] Fix all Critical and Important review findings, then rerun relevant focused tests and final
  verification commands.

- [ ] Update `docs/records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md` after final
  verification and multi-agent review so it contains the actual command exit statuses and review
  outcomes before committing.

### Task 5: Commit And Push

- [ ] Commit the spec and plan checkpoint:

```bash
git add docs/superpowers/specs/2026-05-16-cpd-paper-faithful-offline-scope-audit-design.md docs/superpowers/plans/2026-05-16-cpd-paper-faithful-offline-scope-audit.md
git commit -m "docs: plan CPD paper faithful offline scope audit"
```

- [ ] Commit implementation after review and verification:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md experiments/registry.yaml
git commit -m "feat: audit CPD paper faithful offline scope"
```

- [ ] Push and confirm clean status:

```bash
git push
git status --short
```
