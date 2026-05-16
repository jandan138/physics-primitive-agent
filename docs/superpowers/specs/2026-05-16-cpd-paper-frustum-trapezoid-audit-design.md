# CPD Paper Frustum And Trapezoid Audit Design

## Goal

Add the next offline paper-lane primitive-fit audit slice for `frustum` and
`trapezoidal_prism` candidates on deterministic synthetic toy fixtures.

## Scope

This slice extends `cpd_paper_offline_report` only. It does not generate Newton packages, load real
USD assets, run contact or task smokes, run benchmarks, or claim `paper_faithful_offline`.

## Approach

The report will keep the existing current surrogate/proxy rows for OBB, sphere, capsule, and
capped cylinder. It will append two offline-only paper-shaped candidate rows:

- `frustum`: initialized from the minimum-volume flat-cylinder axis over the eigen axes, with
  top/bottom radii chosen to contain all assigned points and volume
  `pi * h / 3 * (r_top^2 + r_top * r_bottom + r_bottom^2)`.
- `trapezoidal_prism`: evaluated over all six axis orderings, with `h_x`, `h_y`, `h_zt`, and
  `h_zb` chosen to contain all assigned points and volume `4 * h_x * h_y * (h_zt + h_zb)`.

Both rows are offline-only and unmapped to Newton. The implementation is paper-shaped audit
infrastructure, not a full paper reproduction, because capped-cylinder fitting, polygon/quad
policy, full priority-queue trace, component-pair insertion, and postprocess culling are still
missing.

## Data Flow

`build_cpd_paper_offline_report()` will produce four toy cases:

- `paper_single_box`
- `paper_two_face_merge`
- `paper_frustum_like`
- `paper_trapezoid_prism_like`

Each case will expose the same `primitive_fit_audit` schema. The candidate list will include all
six paper primitive names. `missing_paper_primitives` will be empty because the report now has an
audited row for each paper primitive type, but top-level `failure_labels` will still include the
remaining missing mechanics.

## Claim Boundary

Allowed claim: the repository can emit a command-only, fixture-scoped offline audit row for
frustum and trapezoidal-prism candidates.

Disallowed claims:

- paper-faithful CPD primitive fitting;
- full CPD paper reproduction;
- Newton runtime support for frustums or trapezoidal prisms;
- real-USD evidence;
- benchmark evidence;
- collision-quality improvement.

## Tests

The failing tests are already in `tests/test_cpd_paper_offline.py`:

- top-level missing labels no longer include `frustum_fit_missing` or
  `trapezoidal_prism_fit_missing`;
- `next_required_gate` becomes `paper_flat_capped_cylinder_fit_audit`;
- the report includes `paper_frustum_like` and `paper_trapezoid_prism_like`;
- candidate rows include all six paper primitives;
- frustum rows include offline-only status, top/bottom radii, selected cylinder-axis policy, and
  containment;
- trapezoidal-prism rows include offline-only status, six axis-order attempts, selected axis order,
  half-extents, and containment.

