# CPD Eq.4 Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add structured Eq.4 paper-alignment metadata to the CPD-like objective report without changing decomposition behavior.

**Architecture:** Add raw Eq.4-like merge deltas in the decomposition summary, then expose paper-alignment metadata in the objective-report layer with one synthetic-report pass-through for reviewability. Documentation and records must keep the claim as paper-aligned surrogate accounting metadata, not Eq.4 implementation or paper-faithful CPD reproduction.

**Tech Stack:** Python dataclasses/dicts, existing CPD-like objective and synthetic report builders, pytest, Markdown records.

---

### Task 1: Raw Eq.4-Like Merge-Cost Accounting

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- Test: `tests/test_cpd_like_decompose.py`

- [x] **Step 1: Write failing decomposition tests**

Add tests for:

- raw accepted Eq.4-like cost equals `merged.weighted_volume - left.weighted_volume - right.weighted_volume`;
- normalized accepted cost equals raw cost divided by `normalizer_volume`;
- negative raw Eq.4-like cost serializes without being treated as invalid.

- [x] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k eq4
```

Expected: failure because raw Eq.4-like fields do not exist.

- [x] **Step 3: Implement raw and normalized summary fields**

Add `accepted_eq4_costs` and `blocked_eq4_costs` alongside the existing normalized lists. Extend
`_merge_cost_summary(...)` with:

```python
"accepted_eq4_cost_min": _min_or_none(accepted_eq4_costs),
"accepted_eq4_cost_max": _max_or_none(accepted_eq4_costs),
"accepted_eq4_cost_sum": float(sum(accepted_eq4_costs)),
"blocked_eq4_cost_min": _min_or_none(blocked_eq4_costs),
"blocked_eq4_cost_max": _max_or_none(blocked_eq4_costs),
"blocked_eq4_cost_sum": float(sum(blocked_eq4_costs)),
"normalization": {
    "kind": "source_mesh_aabb_volume",
    "floor": MIN_NORMALIZATION_VOLUME,
    "normalizer_volume": normalizer_volume,
    "applied_to": [
        "accepted_normalized_excess",
        "blocked_normalized_excess",
        "excess_volume_threshold_fraction",
    ],
},
```

- [x] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_decompose.py -q -k eq4
```

Expected: selected tests pass.

### Task 2: Objective Alignment Metadata

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- Test: `tests/test_cpd_like_objective.py`

- [x] **Step 1: Write failing objective tests**

Add assertions to `test_objective_report_preserves_stable_schema_keys`:

```python
assert "paper_alignment" in payload["metrics"]
assert set(payload["metrics"]["paper_alignment"]) == {
    "alignment_version",
    "metadata_scope",
    "paper_reference",
    "paper_cost_name",
    "paper_cost_formula_reference",
    "current_report_terms",
    "current_cost_units",
    "cost_unit_terms",
    "normalizer",
    "uses_primitive_type_weights",
    "uses_intersection_term",
    "computes_paper_eq4",
    "paper_faithfulness",
    "matches_paper_story",
    "known_gaps",
}
```

Add a focused test:

```python
def test_objective_report_maps_merge_excess_to_cpd_eq4_boundary():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
    ).to_dict()

    alignment = payload["metrics"]["paper_alignment"]
    assert alignment["alignment_version"] == "cpd_eq4_alignment_metadata_v0"
    assert alignment["metadata_scope"] == "term_category_mapping_not_eq4_implementation"
    assert "Eq.4" in alignment["paper_reference"]
    assert alignment["paper_cost_name"] == "collapse_excess_volume"
    assert alignment["paper_cost_formula_reference"] == (
        "C(p0,p1)=V(merge(p0,p1))-(V(p0)+V(p1))"
    )
    assert "merge_excess_terms" in alignment["current_report_terms"]
    assert alignment["current_cost_units"] == (
        "mixed_raw_and_aabb_normalized_weighted_primitive_volume"
    )
    assert alignment["cost_unit_terms"] == {
        "metrics.merge_excess_terms.accepted_eq4_cost_*": (
            "raw_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.blocked_eq4_cost_*": (
            "raw_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.accepted_normalized_excess_*": (
            "aabb_normalized_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.blocked_normalized_excess_*": (
            "aabb_normalized_weighted_primitive_volume_delta"
        ),
        "metrics.geometric_excess_proxy.normalized_*": (
            "aabb_normalized_weighted_primitive_volume"
        ),
    }
    assert alignment["normalizer"] == "source_mesh_aabb_volume_with_minimum_epsilon"
    assert alignment["uses_primitive_type_weights"] is False
    assert alignment["uses_intersection_term"] is False
    assert alignment["computes_paper_eq4"] is False
    assert alignment["paper_faithfulness"] == "surrogate_not_paper_faithful"
    assert "excess_volume_difference_shape" in alignment["matches_paper_story"]
    assert "paper_scope_priority_queue_collapse_search" in alignment["known_gaps"]
```

Add a weight-sensitive test:

```python
def test_objective_report_alignment_notes_report_weights_when_configured():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
        options=CPDLikeObjectiveOptions(primitive_type_weights={"box": 2.0}),
    ).to_dict()

    assert payload["metrics"]["paper_alignment"]["uses_primitive_type_weights"] is True
```

- [x] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_objective.py -q -k "paper_alignment or stable_schema"
```

Expected: failure because `paper_alignment` does not exist.

- [x] **Step 3: Implement objective metadata**

Add constants and helper:

```python
PAPER_ALIGNMENT_VERSION = "cpd_eq4_alignment_metadata_v0"


def _paper_alignment_metadata(*, uses_primitive_type_weights: bool) -> dict[str, object]:
    return {
        "alignment_version": PAPER_ALIGNMENT_VERSION,
        "metadata_scope": "term_category_mapping_not_eq4_implementation",
        "paper_reference": "Convex Primitive Decomposition for Collision Detection Eq.4",
        "paper_cost_name": "collapse_excess_volume",
        "paper_cost_formula_reference": "C(p0,p1)=V(merge(p0,p1))-(V(p0)+V(p1))",
        "current_report_terms": ["merge_excess_terms", "geometric_excess_proxy"],
        "current_cost_units": "mixed_raw_and_aabb_normalized_weighted_primitive_volume",
        "cost_unit_terms": {
            "metrics.merge_excess_terms.accepted_eq4_cost_*": (
                "raw_weighted_primitive_volume_delta"
            ),
            "metrics.merge_excess_terms.blocked_eq4_cost_*": (
                "raw_weighted_primitive_volume_delta"
            ),
            "metrics.merge_excess_terms.accepted_normalized_excess_*": (
                "aabb_normalized_weighted_primitive_volume_delta"
            ),
            "metrics.merge_excess_terms.blocked_normalized_excess_*": (
                "aabb_normalized_weighted_primitive_volume_delta"
            ),
            "metrics.geometric_excess_proxy.normalized_*": (
                "aabb_normalized_weighted_primitive_volume"
            ),
        },
        "normalizer": "source_mesh_aabb_volume_with_minimum_epsilon",
        "uses_primitive_type_weights": uses_primitive_type_weights,
        "uses_intersection_term": False,
        "computes_paper_eq4": False,
        "paper_faithfulness": "surrogate_not_paper_faithful",
        "matches_paper_story": [
            "excess_volume_difference_shape",
            "aabb_relative_threshold_accounting",
            "primitive_type_weight_hook",
        ],
        "known_gaps": [
            "paper_scope_primitive_vocabulary",
            "paper_scope_primitive_fitting",
            "paper_scope_priority_queue_collapse_search",
            "exact_surface_containment_or_distance",
            "benchmark_or_collision_quality_evaluation",
        ],
    }
```

Add it to `metrics`.

- [x] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_objective.py -q
```

Expected: all objective tests pass.

### Task 3: Synthetic Pass-Through

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- Test: `tests/test_cpd_like_synthetic.py`

- [x] **Step 1: Write failing synthetic test**

Add to `test_cost_guided_synthetic_comparison_shows_old_new_merge_decision`:

```python
assert case["policies"]["topology_then_virtual"]["paper_alignment"]["paper_cost_name"] == (
    "collapse_excess_volume"
)
assert case["policies"]["cost_guided_pairwise"]["paper_alignment"]["paper_faithfulness"] == (
    "surrogate_not_paper_faithful"
)
```

- [x] **Step 2: Run test and confirm RED**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py -q -k cost_guided
```

Expected: failure because policy summaries do not expose `paper_alignment`.

- [x] **Step 3: Include paper alignment in policy summaries**

In `_policy_summary`, read `paper_alignment = objective["metrics"]["paper_alignment"]` and include:

```python
"paper_alignment": paper_alignment,
```

- [x] **Step 4: Run targeted tests and confirm GREEN**

Run:

```bash
python -m pytest tests/test_cpd_like_synthetic.py tests/test_cpd_like_objective.py -q
```

Expected: all selected tests pass.

### Task 4: Documentation And Record

**Files:**
- Create: `docs/records/2026-05-15-cpd-eq4-alignment-metadata.md`
- Modify: `docs/reference/cpd-objective-report-alignment.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/index.md`
- Modify: `docs/records/README.md`

- [x] **Step 1: Update docs**

Use these phrases:

- `structured Eq.4 alignment metadata`;
- `paper-aligned surrogate accounting`;
- `not paper-faithful CPD objective or optimizer`;
- `no new collision-quality or benchmark evidence`.

- [x] **Step 2: Add dated record**

Record implementation, verification, artifacts, claim impact, and next action.

- [x] **Step 3: Run documentation checks**

Run:

```bash
python scripts/validate_docs.py
git diff --check
```

Expected: both pass.

### Task 5: Review, Final Verification, Commit

**Files:**
- All changed files.

- [x] **Step 1: Run full tests**

```bash
python -m pytest -q
```

Expected: all tests pass.

- [x] **Step 2: Request focused agent review**

Ask one reviewer to check Eq.4 alignment and one reviewer to check claim boundaries.

- [x] **Step 3: Fix Important/Critical findings**

If review finds Important or Critical issues, fix them with tests and rerun verification.

- [x] **Step 4: Commit**

```bash
git add src/primitive_collision_compiler/baselines/cpd_like/objective.py \
  src/primitive_collision_compiler/baselines/cpd_like/decompose.py \
  src/primitive_collision_compiler/baselines/cpd_like/synthetic.py \
  tests/test_cpd_like_decompose.py \
  tests/test_cpd_like_objective.py \
  tests/test_cpd_like_synthetic.py \
  tests/test_cli.py \
  README.md \
  docs/records/2026-05-15-cpd-eq4-alignment-metadata.md \
  docs/reference/cpd-objective-report-alignment.md \
  docs/reference/cpd-paper-story-status.md \
  docs/reference/claim-boundaries.md \
  docs/deepdive/evidence-status.md \
  docs/index.md \
  docs/records/README.md \
  docs/superpowers/specs/2026-05-15-cpd-eq4-alignment-design.md \
  docs/superpowers/plans/2026-05-15-cpd-eq4-alignment.md
git commit -m "feat: add cpd eq4 alignment metadata"
```

## Self-Review

No placeholders remain. The plan is intentionally narrow and does not alter algorithm behavior or
Newton diagnostics.
