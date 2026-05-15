# CPD Cost-Guided Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in CPD-like cost-guided merge-search smoke and compare it against the current topology-then-virtual behavior on deterministic synthetic fixtures.

**Architecture:** Preserve the current default decomposition behavior. Add a new merge-search policy inside `decompose.py`, expose it through objective accounting, then add a dedicated synthetic report and CLI path that exercise only in-memory toy meshes under strict claim boundaries.

**Tech Stack:** Python dataclasses, existing CPD-like decomposition/objective modules, argparse CLI, pytest, Markdown records.

---

### Task 1: Cost-Guided Decomposition Policy

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- Test: `tests/test_cpd_like_decompose.py`

- [ ] **Step 1: Write failing decomposition tests**

Add a helper mesh to `tests/test_cpd_like_decompose.py`:

```python
def _cost_guided_pair_choice_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [10.0, 10.0, 10.0],
                [0.05, 0.05, 0.05],
                [1.05, 0.05, 0.05],
                [0.05, 1.05, 0.05],
            ]
        ),
        faces=np.array([[0, 1, 2], [1, 2, 3], [4, 5, 6]]),
    )
```

Add tests:

```python
def test_decompose_mesh_default_merge_search_keeps_topology_before_virtual():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )

    assert report.status == "smoke_passed"
    assert report.merge_search_policy == "topology_then_virtual"
    assert report.topology_merge_count == 1
    assert report.virtual_component_merge_count == 0
    assert report.primitives[0].source_component_ids == (0, 1)


def test_decompose_mesh_cost_guided_pairwise_can_choose_virtual_before_topology():
    default_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
    )
    cost_guided_report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
    )

    assert cost_guided_report.stage == "cpd_like_cost_guided_merge_smoke"
    assert cost_guided_report.status == "smoke_passed"
    assert cost_guided_report.merge_search_policy == "cost_guided_pairwise"
    assert cost_guided_report.topology_merge_count == 0
    assert cost_guided_report.virtual_component_merge_count == 1
    assert cost_guided_report.primitives[0].source_component_ids == (0, 2)
    assert (
        cost_guided_report.merge_cost_summary["accepted_normalized_excess_sum"]
        < default_report.merge_cost_summary["accepted_normalized_excess_sum"]
    )


def test_decompose_mesh_cost_guided_pairwise_keeps_virtual_threshold_gate():
    report = decompose_mesh(
        _cost_guided_pair_choice_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        excess_volume_threshold_fraction=0.0,
    )

    assert report.status == "partial"
    assert report.topology_merge_count == 0
    assert report.virtual_component_merge_count == 0
    assert report.blocked_merge_count == 1
    assert report.fallback_reason == "component_merge_threshold_blocked"


def test_decompose_mesh_rejects_unknown_merge_search_policy():
    try:
        decompose_mesh(
            _square_mesh(),
            max_primitives=1,
            primitive_subset=("box",),
            merge_search_policy="paper_optimizer",
        )
    except ValueError as exc:
        assert "merge_search_policy" in str(exc)
    else:
        raise AssertionError("unknown merge_search_policy should be rejected")
```

- [ ] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k "cost_guided or merge_search"
```

Expected: failure because `merge_search_policy` and report field do not exist.

- [ ] **Step 3: Implement minimal decomposition support**

Modify `decompose.py`:

- add constants `MERGE_SEARCH_TOPOLOGY_THEN_VIRTUAL` and `MERGE_SEARCH_COST_GUIDED_PAIRWISE`;
- add `merge_search_policy` to `decompose_mesh(...)`, validation, `CPDLikeDecompositionReport`,
  and `to_dict()`;
- add `is_virtual_component_merge` to `_MergeCandidate`;
- implement `_best_cost_guided_merge(...)` by comparing best topology and best virtual candidates
  by normalized excess, with topology as tie-breaker;
- keep the existing topology-then-virtual loop unchanged for the default policy;
- keep threshold blocking only for virtual candidates.

Modify `objective.py` so `metrics["component_accounting"]` includes `merge_search_policy`.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k "cost_guided or merge_search or component_merge"
```

Expected: selected tests pass.

### Task 2: Cost-Guided Synthetic Report And CLI

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/__init__.py`
- Modify: `src/primitive_collision_compiler/cli.py`
- Test: `tests/test_cpd_like_synthetic.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write failing synthetic and CLI tests**

In `tests/test_cpd_like_synthetic.py`, import `build_cpd_like_cost_guided_synthetic_comparison_report`
and add:

```python
def test_cost_guided_synthetic_comparison_shows_old_new_merge_decision():
    report = build_cpd_like_cost_guided_synthetic_comparison_report()

    assert report["stage"] == "cpd_like_cost_guided_synthetic_objective_comparison"
    assert report["status"] == "smoke_passed"
    assert report["claim_boundary"] == "cost_guided_synthetic_comparison_not_collision_quality_validation"

    cases = {case["case_id"]: case for case in report["cases"]}
    case = cases["cost_guided_pair_choice"]
    assert case["expectation_status"] == "matched"
    assert case["policies"]["topology_then_virtual"]["component_accounting"][
        "topology_merge_count"
    ] == 1
    assert case["policies"]["cost_guided_pairwise"]["component_accounting"][
        "virtual_component_merge_count"
    ] == 1
    assert case["comparison"]["cost_guided_chose_virtual_instead_of_topology"] is True
    assert case["comparison"]["cost_guided_accepted_excess_delta"] < 0.0
```

In `tests/test_cli.py`, add:

```python
def test_cli_run_cpd_like_cost_guided_synthetic_comparison_emits_json_without_config(capsys):
    assert cli.main(["--run-cpd-like-cost-guided-synthetic-comparison"]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["stage"] == "cpd_like_cost_guided_synthetic_objective_comparison"
    assert payload["status"] == "smoke_passed"
    assert payload["cases"][0]["case_id"] == "cost_guided_pair_choice"
    assert captured.err == ""


def test_cli_run_cpd_like_cost_guided_synthetic_comparison_rejects_non_finite_json(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        cli,
        "build_cpd_like_cost_guided_synthetic_comparison_report",
        lambda: {
            "stage": "cpd_like_cost_guided_synthetic_objective_comparison",
            "status": "smoke_passed",
            "bad": float("nan"),
        },
    )

    assert cli.main(["--run-cpd-like-cost-guided-synthetic-comparison"]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "cpd_like_cost_guided_synthetic_comparison report contains non-finite JSON values" in captured.err
    assert "Traceback" not in captured.err
```

- [ ] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "cost_guided"
```

Expected: import/parser failures because the report builder and CLI flag do not exist.

- [ ] **Step 3: Implement report and CLI**

Modify `synthetic.py`:

- add constants for the cost-guided claim boundary and evidence level;
- add `_cost_guided_pair_choice_mesh()`;
- add `merge_search_policy` and `max_primitives` to `_PolicySpec` or `_SyntheticCase`;
- add `build_cpd_like_cost_guided_synthetic_comparison_report(...)`;
- include compact policy summaries with `component_accounting` and `merge_excess_terms`;
- add comparison fields `cost_guided_chose_virtual_instead_of_topology` and
  `cost_guided_accepted_excess_delta`.

Modify `__init__.py` exports.

Modify `cli.py`:

- import the new builder;
- add `--run-cpd-like-cost-guided-synthetic-comparison`;
- emit strict JSON with `allow_nan=False`;
- return `0` only when status is `smoke_passed`.

- [ ] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "cost_guided or synthetic_comparison or cpd_like_synthetic"
```

Expected: selected tests pass.

### Task 3: Documentation And Verification

**Files:**
- Create: `docs/records/2026-05-15-cpd-like-cost-guided-merge.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-objective-report-alignment.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/index.md`
- Modify: `README.md`
- Modify: `experiments/registry.yaml`

- [ ] **Step 1: Update docs and registry**

Use the phrase `focused CPD-like cost-guided merge-search smoke`. State that it uses
AABB-normalized merge-excess as a decision-making cost on deterministic synthetic fixtures.

Do not use the words `validated`, `benchmark`, `paper-faithful`, or `better collision geometry`
as supported claims.

- [ ] **Step 2: Run command smoke**

Run:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-synthetic-comparison
```

Expected: exit 0 and JSON with stage `cpd_like_cost_guided_synthetic_objective_comparison`.

- [ ] **Step 3: Run full verification**

Run:

```bash
python -m pytest -q
python scripts/validate_docs.py
git diff --check
```

Expected: all pass.

- [ ] **Step 4: Commit**

Run:

```bash
git add src/primitive_collision_compiler/baselines/cpd_like/decompose.py \
  src/primitive_collision_compiler/baselines/cpd_like/objective.py \
  src/primitive_collision_compiler/baselines/cpd_like/synthetic.py \
  src/primitive_collision_compiler/baselines/cpd_like/__init__.py \
  src/primitive_collision_compiler/cli.py \
  tests/test_cpd_like_decompose.py \
  tests/test_cpd_like_synthetic.py \
  tests/test_cli.py \
  docs/records/2026-05-15-cpd-like-cost-guided-merge.md \
  docs/records/README.md \
  docs/reference/claim-boundaries.md \
  docs/deepdive/evidence-status.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/cpd-objective-report-alignment.md \
  docs/reference/cpd-like-face-merge-explainer.md \
  docs/index.md \
  README.md \
  experiments/registry.yaml \
  docs/superpowers/specs/2026-05-15-cpd-cost-guided-merge-design.md \
  docs/superpowers/plans/2026-05-15-cpd-cost-guided-merge.md
git commit -m "feat: add cpd cost-guided synthetic merge smoke"
```

## Self-Review

The plan covers the design. No placeholders remain. It keeps the implementation opt-in, test-first,
synthetic-first, and claim-bounded.
