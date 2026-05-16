# CPD Paper Capsule Axis Audit Design

## Context

The partial `cpd_paper_offline_report` now has audit rows covering all six paper primitive names,
but OBB and sphere are still current surrogate rows, and the capsule row still comes from the
current CPD-like surrogate fitter. That fitter uses the longest local span as the capsule axis. The
paper says capsules are similar to cylinders and that one capsule is computed per axis.

## Goal

Replace the paper-lane capsule row with a fixture-scoped offline audit row that fits one capsule per
operator axis, records every axis candidate, and selects the minimum-volume capsule candidate.

## Scope

- Synthetic toy fixtures only.
- Command-only `cpd_paper_offline_report` only.
- No package generation.
- No Newton runtime invocation.
- No real USD, bed, Franka, benchmark, or collision-quality claim.

## Design

The report will stop using the current CPD-like capsule row in the paper-lane candidate set. It will
keep current rows for `box` and `sphere`, then append an offline paper-shaped capsule row before the
offline flat capped-cylinder, frustum, and trapezoidal-prism rows.

For each candidate axis:

1. Use the operator/OBB axis basis already computed for the face group.
2. Use the OBB center as the point on the capsule axis.
3. Compute the capsule radius as the maximum radial distance to that axis.
4. Compute the spherical-cap-adjusted axial values from the paper equation:
   `h(p) = dot(axis, p - center) - sqrt(radius^2 - radial_distance(p)^2)`.
5. Use the min/max of those values as the capsule segment endpoints.
6. Record radius, height, half-height, center, volume, containment, and all three axis candidates.

The selected row uses the minimum unweighted capsule volume, with paper weight `1.0`. Because capsule
is a Newton-native primitive but this report does not generate packages, the row records
`newton_runtime_kind: capsule` plus report-level `newton_runtime_triggered: false`.

## Claim Boundary

This closes only the `paper_capsule_axis_policy_missing` gap inside the named synthetic offline
audit report. It does not make the report `paper_faithful_offline`; remaining gaps are polygon/quad
face policy, full priority-queue trace, component-pair edge insertion, and enclosed-primitive
postprocessing.

## Verification

- Focused unit tests for the capsule row, failure labels, and next gate.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
