# CPD Paper Fixture Breadth Expansion Plan Design

## Context

The completed `paper_faithful_offline_scope_audit` keeps `cpd_paper_offline_report`
`partial` and advances the next gate to `paper_fixture_breadth_expansion_plan`.

The scope audit has nine blocking criteria:

1. `source_mesh_and_preprocessing_policy`;
2. `source_face_intake_policy`;
3. `operator_q_audit`;
4. `primitive_vocabulary_and_fit`;
5. `paper_collapse_cost_and_weighting`;
6. `greedy_priority_queue_trace`;
7. `target_count_and_threshold_stop`;
8. `component_pair_edge_handling`;
9. `enclosed_primitive_postprocess`.

This slice should not implement those fixtures yet. Its job is to define the next fixture breadth
plan so later implementation slices can add one small deterministic fixture batch at a time.

## Chosen Approach

Create a durable reference document:

```text
docs/reference/cpd-paper-fixture-breadth-expansion-plan.md
```

The document should:

- map every blocking scope-audit criterion to planned synthetic fixture coverage;
- keep all planned work offline-only;
- define the smallest useful fixture batches;
- state which rows can share one fixture;
- define what evidence each future fixture must record;
- keep package generation, Newton runtime, real USD, and benchmark work out of scope;
- keep `paper_faithful_offline_supported: false` until future implementation records exist.

This is a planning artifact, not experiment evidence and not a paper-faithful implementation.

## Alternatives Considered

### Alternative A: Write The Fixture Plan First

This is the selected path. It turns the scope-audit blockers into a small ordered set of future
implementation batches before any new code is added.

Trade-off: it does not close any algorithmic gap by itself, but it reduces ambiguity and keeps the
next code slice narrow.

### Alternative B: Implement All Planned Fixtures Immediately

This would move faster on code, but it risks combining preprocessing, source-face intake,
operator degeneracy, primitive fitting, merge search, component-pair handling, and postprocess
behavior in one large change.

Trade-off: too much blast radius for the current proof point.

### Alternative C: Jump To Bed/Franka, Newton, Or Benchmark Work

This would be useful later, but it would skip the paper-side offline mechanics that the scope
audit explicitly marked as partial.

Trade-off: it would create runtime or real-asset activity without a changed offline paper package
boundary.

## Planned Fixture Batches

The reference plan should group future fixtures into five batches.

| Batch | Planned fixture ids | Primary blockers covered | Purpose |
| --- | --- | --- | --- |
| A. Source/preprocess/intake/operator breadth | `paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, `paper_concave_polygon_rejected` | source mesh/preprocessing, source-face intake, operator `Q` | Broaden mesh policy beyond current exact-overlap and simple convex source-face fixtures. |
| B. Primitive fit breadth | `paper_rotated_box_fit`, `paper_offset_sphere_fit`, `paper_off_axis_capsule_fit`, `paper_flat_capped_cylinder_axis_fit`, `paper_tapered_frustum_fit`, `paper_asymmetric_trapezoid_fit` | primitive vocabulary and fit | Broaden all six paper primitive names beyond current named minimal cases without changing Newton runtime support. |
| C. Cost/search/stop breadth | `paper_branching_cost_order`, `paper_equal_cost_queue_tie`, `paper_nonzero_threshold_block` | collapse cost, priority queue, target/threshold stop | Test cost ordering, queue tie/stale behavior, and nonzero finite threshold blocking. |
| D. Component-pair breadth | `paper_component_pair_multi_candidate_order`, `paper_component_pair_cap_skipped` | component-pair edge handling, target/threshold stop | Broaden disconnected-component pair insertion beyond one accepted and one blocked all-pairs case. |
| E. Postprocess breadth | `paper_rotated_nested_primitive`, `paper_cross_type_enclosure_boundary` | enclosed primitive postprocess | Broaden postprocess from one explicit identity-axis OBB canary to additional containment boundaries. |

The plan should mark Batch A as the recommended first implementation batch because it supports
source mesh, source-face intake, and operator policy at the same time while staying offline-only.

## Fixture Row Requirements

Every planned fixture row in the reference document must include:

- fixture id;
- blocking criteria covered;
- fixture geometry in plain language;
- required report additions for a future code slice;
- required tests for a future code slice;
- explicit non-goals;
- claim boundary.

## Documentation Updates

Update:

- `docs/index.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/records/README.md`;
- new dated record under `docs/records/`.

Do not add an `experiments/registry.yaml` entry unless an executable report or experiment command
is introduced. This slice is documentation-only.

## Claim Boundaries

The wording must not claim:

- new fixture implementation;
- `paper_faithful_offline`;
- full CPD reproduction;
- package generation;
- Newton runtime support;
- real-USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification.

Allowed wording:

- "fixture-breadth expansion plan";
- "planned synthetic fixture coverage";
- "offline-only paper-lane planning artifact";
- "next code slices remain blocked until implemented and recorded."

## Verification

Required verification:

- `python scripts/validate_docs.py`;
- `python scripts/validate_site_claims.py`;
- `git diff --check`;
- `python -m pytest -q`.
