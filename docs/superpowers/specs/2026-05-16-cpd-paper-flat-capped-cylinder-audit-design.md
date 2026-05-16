# CPD Paper Flat Capped Cylinder Audit Design

## Goal

Replace the current `capped_cylinder` hemisphere-proxy audit row in `cpd_paper_offline_report` with
an offline-only paper-shaped flat-capped cylinder audit row.

## Scope

This slice changes only the offline paper-lane report. It does not add a runtime primitive, does
not map capped cylinders to Newton, does not generate packages, does not run real USD assets, and
does not claim `paper_faithful_offline`.

## Approach

The paper describes capped cylinders as flat cylinders: choose one candidate per eigen axis, compute
height from the axis projection span, compute radius from radial distance, and choose the
minimum-volume candidate. The report will expose:

- `cap_model: flat_caps`;
- `axis_selection_policy: min_volume_flat_cylinder_axis`;
- three `flat_cylinder_axis_candidates`;
- selected radius, height, half-height, axis index, top center, bottom center;
- volume `pi * r^2 * h`;
- paper weight `1.05`;
- `newton_runtime_kind: offline_only_unmapped`.

The current CPD-like `capped_cylinder` proxy remains outside this paper lane. The paper lane still
remains partial because capsule axis policy, polygon/quad intake, full priority-queue trace,
component-pair insertion, and postprocess culling are still missing.

## Tests

The RED test in `tests/test_cpd_paper_offline.py` expects:

- no `paper_flat_capped_cylinder_fit_missing` failure label;
- `next_required_gate == "paper_capsule_axis_policy_audit"`;
- the `capped_cylinder` candidate row has `implementation_status:
  paper_shaped_offline_fit_audit`;
- the row has flat-cap dimensions, three axis candidates, containment, formula-consistent volume,
  and offline-only Newton status.

