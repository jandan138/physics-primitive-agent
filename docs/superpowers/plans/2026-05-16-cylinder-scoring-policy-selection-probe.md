# Cylinder Scoring Policy Selection Probe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a synthetic/offline, strictly opt-in cylinder scoring-policy selection probe that can
change candidate selection on the near-miss fixture while keeping default package generation
unchanged.

**Architecture:** Add optional primitive score multipliers to the candidate-ranking helper without
changing default callers. Add a dedicated synthetic report and CLI flag that compare default and
opt-in rankings for `cylinder_near_miss_cluster` and `boxy_cuboid_guardrail`.

**Tech Stack:** Python, pytest, JSON CLI reports, existing CPD-like synthetic fixture helpers.

---

### Task 1: Opt-In Ranking Helper

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Test: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Write the failing test**

Add a test that imports and calls a new optional multiplier path:

```python
def test_opt_in_cylinder_multiplier_flips_near_miss_without_default_change():
    mesh = cpd_synthetic._cylinder_near_miss_cluster_mesh()
    face_ids = frozenset(range(mesh.face_count))

    default_fit = fit_best_primitive(mesh, face_ids, primitive_subset=("box", "cylinder"))
    opt_in_ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, primitive_subset=("box", "cylinder")),
        primitive_score_multipliers={"cylinder": 0.88},
    )

    assert default_fit.primitive_type == "box"
    assert opt_in_ranked[0].primitive_type == "cylinder"
    assert opt_in_ranked[0].effective_score < opt_in_ranked[1].effective_score
```

Add a second negative-control test:

```python
def test_opt_in_cylinder_multiplier_preserves_boxy_guardrail():
    mesh = cpd_synthetic._boxy_cuboid_guardrail_mesh()
    face_ids = frozenset(range(mesh.face_count))

    default_fit = fit_best_primitive(mesh, face_ids, primitive_subset=("box", "cylinder"))
    opt_in_ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, primitive_subset=("box", "cylinder")),
        primitive_score_multipliers={"cylinder": 0.88},
    )

    assert default_fit.primitive_type == "box"
    assert opt_in_ranked[0].primitive_type == "box"
```

- [x] **Step 2: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_opt_in_cylinder_multiplier_flips_near_miss_without_default_change tests/test_cpd_like_synthetic.py::test_opt_in_cylinder_multiplier_preserves_boxy_guardrail
```

Expected: fail because `primitive_score_multipliers` and `effective_score` do not exist.

- [x] **Step 3: Implement minimal helper support**

Extend `PrimitiveCandidateSelection` with:

```python
effective_score: float
score_multiplier: float
```

Extend `rank_primitive_candidates_for_selection()` with optional keyword-only:

```python
primitive_score_multipliers: Mapping[str, float] | None = None
```

Keep default behavior unchanged by using multiplier `1.0` for every primitive when no mapping is
provided. Sort by `(not admissible, effective_score, candidate_order)`.

- [x] **Step 4: Run GREEN**

Run the two focused tests from Step 2.

Expected: both pass.

### Task 2: Synthetic Selection Probe Report And CLI

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Write the failing report test**

Add:

```python
def test_cylinder_scoring_policy_selection_probe_reports_opt_in_selection():
    report = cpd_synthetic.build_cpd_like_cylinder_scoring_policy_selection_probe_report()

    assert report["stage"] == "cpd_like_cylinder_scoring_policy_selection_probe"
    assert report["status"] == "smoke_passed"
    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {"cylinder_near_miss_cluster", "boxy_cuboid_guardrail"}
    assert cases["cylinder_near_miss_cluster"]["default_selected_primitive_type"] == "box"
    assert cases["cylinder_near_miss_cluster"]["opt_in_selected_primitive_type"] == "cylinder"
    assert cases["cylinder_near_miss_cluster"]["default_behavior_changed"] is False
    assert cases["cylinder_near_miss_cluster"]["decision"]["newton_task_comparison_triggered"] is False
    assert cases["boxy_cuboid_guardrail"]["default_selected_primitive_type"] == "box"
    assert cases["boxy_cuboid_guardrail"]["opt_in_selected_primitive_type"] == "box"
```

- [x] **Step 2: Write the failing CLI test**

Add:

```python
def test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_emits_json(capsys):
    assert cli.main(["--run-cpd-like-cylinder-scoring-policy-selection-probe"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "cpd_like_cylinder_scoring_policy_selection_probe"
    assert payload["status"] == "smoke_passed"
```

- [x] **Step 3: Run RED**

Run:

```bash
PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cylinder_scoring_policy_selection_probe_reports_opt_in_selection tests/test_cli.py::test_cli_run_cpd_like_cylinder_scoring_policy_selection_probe_emits_json
```

Expected: fail because the report builder and CLI flag do not exist.

- [x] **Step 4: Implement report and CLI**

Add constants beside the existing scoring-policy ablation constants:

```python
CYLINDER_SCORING_POLICY_SELECTION_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_selection_probe_not_default_or_collision_quality_validation"
)
CYLINDER_SCORING_POLICY_SELECTION_PROBE_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_scoring_policy_selection_probe_smoke"
)
CYLINDER_SCORING_POLICY_SELECTION_PROBE_STATUS_SEMANTICS = (
    "opt_in_selection_probe_not_quality_success"
)
```

Add `build_cpd_like_cylinder_scoring_policy_selection_probe_report()` and a helper that records
default rows and opt-in rows using `primitive_score_multipliers={"cylinder": 0.88}`.

Add CLI flag:

```python
--run-cpd-like-cylinder-scoring-policy-selection-probe
```

- [x] **Step 5: Run GREEN**

Run the RED command again.

Expected: both tests pass.

### Task 3: Documentation And Registry

**Files:**

- Create: `docs/records/2026-05-16-cylinder-scoring-policy-selection-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] **Step 1: Record the slice**

Write that this is synthetic/offline/opt-in only, near-miss flips under opt-in ranking, boxy
guardrail does not flip, and default packages/Newton task gates remain unchanged.

- [x] **Step 2: Update claim boundaries**

Add allowed wording for the opt-in selection probe and explicitly reject default scoring-policy
change, real-USD improvement, Newton task improvement, benchmark, and CPD reproduction claims.

- [x] **Step 3: Update story/status pages and registry**

Add the new CLI command to `experiments/registry.yaml` and include the new record in docs indexes.

### Task 4: Verification And Review

**Files:**

- Modify: `docs/records/2026-05-16-cylinder-scoring-policy-selection-probe.md`
- Modify: this plan file

- [x] **Step 1: Full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-selection-probe
```

- [x] **Step 2: Multi-agent review**

Request implementation and docs reviews. Fix Critical/Important findings and re-review.

- [x] **Step 3: Mark verification**

Update this plan and the dated record with the final verification commands and review outcome.
