# CPD Eq.4 Alignment Design

## Goal

Add structured objective-report metadata that maps the current CPD-like merge-excess accounting to
the Convex Primitive Decomposition paper's Eq.4 collapse cost, while keeping the claim boundary
below paper-faithful reproduction.

## Context

The repository already has:

- a restricted geometry-only CPD-like primitive proposal baseline;
- an offline paper-aligned surrogate objective report;
- deterministic synthetic objective comparison cases;
- one cost-guided merge-search smoke that uses AABB-normalized merge-excess as a toy decision cost.

The next workbench step should make the paper alignment inspectable in JSON, not only in prose.

## Scope

This slice adds a `paper_alignment` metadata section to `metrics` in
`CPDLikeObjectiveReport`.

The section should state:

- the paper reference: `CPD Eq.4 collapse cost`;
- the Eq.4 cost shape: `V(merge(p0, p1)) - (V(p0) + V(p1))`;
- the current report term that corresponds to that shape: `merge_excess_terms`;
- that the current values are AABB-normalized and use current restricted primitive fits;
- that this is term-category mapping, not an Eq.4 implementation;
- that the current implementation excludes the Eq.5 intersection term;
- that the current implementation is a surrogate, not a paper-faithful objective or optimizer;
- the missing workbench gaps: paper-scope primitive vocabulary, paper primitive fitting,
  priority-queue collapse search, exact containment/surface-distance evaluation, benchmark
  evaluation, and collision-quality validation.

## Non-Goals

- Do not change primitive fitting.
- Do not change merge search.
- Do not add a new Newton probe.
- Do not claim CPD reproduction, paper-faithful optimization, benchmark evidence, or
  collision-quality validation.

## Report Shape

`metrics["paper_alignment"]` should be a small deterministic dictionary:

```python
{
    "alignment_version": "cpd_eq4_alignment_metadata_v0",
    "metadata_scope": "term_category_mapping_not_eq4_implementation",
    "paper_reference": "Convex Primitive Decomposition for Collision Detection Eq.4",
    "paper_cost_name": "collapse_excess_volume",
    "paper_cost_formula_reference": "C(p0,p1)=V(merge(p0,p1))-(V(p0)+V(p1))",
    "current_report_terms": ["merge_excess_terms", "geometric_excess_proxy"],
    "current_cost_units": "aabb_normalized_weighted_primitive_volume",
    "normalizer": "source_mesh_aabb_volume_with_minimum_epsilon",
    "uses_primitive_type_weights": bool,
    "uses_intersection_term": False,
    "computes_paper_eq4": False,
    "paper_faithfulness": "surrogate_not_paper_faithful",
    "matches_paper_story": [...],
    "known_gaps": [...],
}
```

`uses_primitive_type_weights` should be true when `CPDLikeObjectiveOptions.primitive_type_weights`
is non-empty.

## Tests

Add tests that:

1. `metrics` includes `paper_alignment` and stable keys.
2. The alignment section references Eq.4 and the existing merge-excess terms.
3. The alignment section reports `uses_primitive_type_weights` correctly.
4. The cost-guided synthetic report surfaces the alignment section in each policy summary.
5. JSON remains strict-serializable.

## Documentation

Update:

- `docs/reference/cpd-objective-report-alignment.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/deepdive/evidence-status.md`
- `docs/index.md`
- `docs/records/README.md`

Add a dated record for this slice.

## Verification

Required before merge:

- `python -m pytest tests/test_cpd_like_objective.py tests/test_cpd_like_synthetic.py -q`
- `python -m pytest -q`
- `python scripts/validate_docs.py`
- `git diff --check`

## Claim Boundary

This slice supports only structured paper-alignment metadata for the existing CPD-like objective
report. It does not add new algorithmic capability, Eq.4 implementation, or evaluation evidence.
