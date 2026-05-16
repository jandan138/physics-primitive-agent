# CPD Paper OBB/Sphere Fit Faithfulness Design

## Context

The current `cpd_paper_offline_report` next gate is
`paper_obb_sphere_fit_faithfulness_audit`. This gate exists because the report still labels the
`oriented_bounding_box` and `sphere` candidates as `current_surrogate_not_paper_faithful`, even
though the formulas in the shared CPD-like fitter are close to the paper construction.

The paper method describes the following primitive-construction requirements:

- decompose the accumulated operator `Q` into orthonormal eigenvectors;
- use those eigenvectors as OBB axes;
- project the vertices of subsumed faces onto each axis;
- compute OBB lower/upper bounds, center, half-extents, and volume from those projected bounds;
- clamp primitive dimensions with the paper's stated lower bound of `1e-3`;
- fit the sphere from the previously computed OBB world-space center, with radius equal to
  `max(max_point_distance_from_center, 1e-3)`.

The repository's shared CPD-like fitter already uses operator axes, projected point bounds, and
the OBB center for sphere fitting. The important mismatch is that it is a shared runtime/plumbing
fitter with `MIN_DIMENSION = 1e-6` and report labels that deliberately avoid paper-faithful claims.

## Chosen Approach

Add dedicated offline paper-lane OBB and sphere candidate rows inside
`src/primitive_collision_compiler/baselines/cpd_paper/offline.py`.

This keeps the CPD-like runtime primitive fitter unchanged and prevents accidental claim expansion.
The offline paper report will compute OBB and sphere rows using a paper-specific clamp
`PAPER_PRIMITIVE_MIN_DIMENSION = 1e-3`, explicit formula fields, containment checks, and source
fields recording that the sphere center came from the paper OBB center.

The current CPD-like OBB/sphere rows should be replaced in this report only. They can remain in
`cpd_like.primitives` for older package, Newton, and diagnostic paths.

## Alternatives Considered

1. Reclassify the existing CPD-like `box` and `sphere` rows as paper-shaped.
   This is too weak because the shared fitter uses a different clamp and would keep paper-lane
   claims tied to runtime/plumbing code.

2. Change `cpd_like.primitives.MIN_DIMENSION` from `1e-6` to `1e-3`.
   This would affect unrelated CPD-like package generation, Newton smokes, real-USD probes, and
   historical diagnostics. It is too broad for this paper-lane audit gate.

3. Add new offline paper-lane rows only in `cpd_paper.offline`.
   This is the selected approach because it isolates the paper audit while preserving existing
   behavior elsewhere.

## Report Behavior

After this slice:

- `failure_labels` should no longer contain `paper_obb_sphere_fit_faithfulness_missing`;
- `missing_before_paper_faithful_offline` should advance to the next explicit paper gap instead of
  implying the whole lane is complete;
- `paper_faithfulness.implemented_fixture_scope` should include
  `paper_obb_sphere_fit_faithfulness_audit`;
- every `primitive_fit_audit.candidates` row for `oriented_bounding_box` should have:
  - `implementation_status: paper_shaped_offline_fit_audit`;
  - `current_implementation_kind: offline_paper_oriented_bounding_box_fit`;
  - `fit_model: paper_operator_eigenbasis_projected_bounds`;
  - `primitive_parameter_lower_clamp: 0.001`;
  - dimensions containing `lower_bounds`, `upper_bounds`, `half_extents`, `paper_center_local`,
    `paper_center_world`, and `axis_order_policy`;
  - `axis_matrix_layout: rows_are_axes`;
  - `volume_formula: 8*hx*hy*hz`;
  - `contains_assigned_points: true` for the current deterministic nondegenerate fixtures.
- every `sphere` row should have:
  - `implementation_status: paper_shaped_offline_fit_audit`;
  - `current_implementation_kind: offline_paper_sphere_fit`;
  - `fit_model: paper_obb_center_max_distance_radius`;
  - `primitive_parameter_lower_clamp: 0.001`;
  - dimensions containing `radius`, `center_source: paper_obb_center`,
    `radius_source: max_distance_from_obb_center_clamped`, and `unclamped_radius`;
  - `volume_formula: 4/3*pi*r^3`;
  - `contains_assigned_points: true` for the current deterministic nondegenerate fixtures.

If a future fixture is invalid or degenerate enough that OBB/sphere containment fails, the row must
keep the explicit paper construction metadata, set `contains_assigned_points: false`, record a
non-null `fit_failure_reason`, and avoid closing the gate for that fixture.

The selected candidate rule remains `min_paper_weighted_volume_for_fixture_audit`, but the OBB and
sphere volumes now come from the paper-lane rows rather than the shared CPD-like fitter.
Each primitive audit must contain exactly one row per paper primitive name; OBB/sphere paper rows
replace the old shared CPD-like rows and must not be appended as duplicates.
Formula strings remain inside each row's `dimensions` dictionary, matching the existing capsule,
capped-cylinder, frustum, and trapezoidal-prism audit rows.

## Next Gate

This slice should not claim `paper_faithful_offline_supported: true`. The lane spec's record gate is
in scope for this slice through the dated record and registry entry. After that record exists,
`next_required_gate` should mean the next unresolved paper mechanic, not another record-only step.
The next conservative unresolved mechanic should become `paper_duplicate_vertex_preprocessing_audit`,
because the gap matrix still lists overlapped or duplicate vertex preprocessing as not started.

## Tests

Add tests that fail before implementation and pass after:

- exact top-level `failure_labels` advances from OBB/sphere to duplicate-vertex preprocessing;
- exact top-level `next_required_gate` becomes `paper_duplicate_vertex_preprocessing_audit`;
- `paper_obb_sphere_fit_faithfulness_audit` appears in implemented fixture scope;
- OBB candidate rows use paper-specific fit metadata and clamp `0.001`;
- OBB half-extents, local center, world center, and volume match projected vertex bounds for
  `paper_single_box`;
- sphere candidate rows use the OBB world center and clamp the max point distance to at least
  `1e-3` for `paper_single_box`;
- `paper_tiny_sphere_clamp` exercises the sphere radius clamp path when the unclamped radius is
  below `1e-3`;
- the same OBB/sphere formula helper is checked on a non-axis-aligned fixture such as
  `paper_three_face_chain` so transposed-axis and local/world-center mistakes are visible;
- every primitive audit contains unique `paper_primitive` names;
- report metadata labels operator eigenvectors as column vectors and primitive axes as row vectors;
- merge-cost and queue-trace tests continue to assert deterministic event order, finite costs,
  selected primitive identity fields, and queue keys after the OBB/sphere volume change;
- all package/Newton/real-USD/benchmark triggers remain false.

## Documentation And Records

Update:

- `docs/index.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- a new dated record under `docs/records/`.

The wording must stay bounded: this is an offline fixture-scoped paper-shaped OBB/sphere fit audit,
not full CPD reproduction, not Newton runtime support, not package generation, not real-USD
evidence, and not benchmark or collision-quality evidence.

When updating reference docs, also update the safe-current-wording sections that currently describe
OBB/sphere as "current surrogate" rows.

## Verification

Required verification:

- focused RED/GREEN pytest for the new OBB/sphere assertions and CLI JSON case;
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`;
- `python -m pytest -q`;
- `python scripts/validate_docs.py`;
- `python scripts/validate_site_claims.py`;
- `git diff --check`.
