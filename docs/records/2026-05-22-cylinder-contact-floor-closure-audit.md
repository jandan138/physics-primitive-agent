# 2026-05-22 Cylinder Contact/Floor Closure Audit

## Date

2026-05-22

## Status

Complete for a same-report contact/floor closure audit over the recorded capped-bed
full-compound controls. Not complete as physical root-cause proof, proof that contact is
irrelevant in all settings, a validated repair, selector calibration, collision-quality
validation, or safety evidence.

## Inputs

- `reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`
- `reports/generated/cylinder_clean_controls/compact_probe.json`
- [Cylinder repair-candidate controls](2026-05-22-cylinder-repair-candidate-controls.md)
- [Cylinder clean-control probe](2026-05-22-cylinder-clean-control-probe.md)

No new Newton runner was added. This audit extracts contact/support facts from existing real
Newton reports.

## Full-Package Contact/Support Findings

The recorded full-compound bed repair-control report contains ten same-gate variants:

- `native_control_box`
- `native_opt_in_cylinder`
- `native_opt_in_cylinder_reverted`
- `box_at_cylinder_center`
- `cylinder_at_box_center`
- `native_opt_in_cylinder_with_native_box_inertia`
- `native_opt_in_cylinder_with_native_box_com`
- `native_opt_in_cylinder_with_native_box_inertia_tensor`
- `native_opt_in_cylinder_with_native_box_mass`
- `native_opt_in_cylinder_with_native_box_mass_inertia`

Across those variants:

- every variant records `final_contact_count: 4`;
- every variant records the same final contact primitive suffixes: `12`, `15`, `15`, `26`;
- final support height stays near zero, from about `-1.634e-06 m` to `-6.039e-06 m`;
- minimum support height stays within the configured floor-breach allowance, from about
  `-0.000424 m` to `-0.001017 m`;
- failing full-package variants fail with `not_settled`, not `floor_breach`;
- passing body-state variants clear the final-speed label while keeping the same final contact
  primitive suffixes.

Representative rows:

| Variant | Status | Failure labels | Final speed m/s | Final support m | Final contact suffixes |
| --- | --- | --- | --- | --- | --- |
| `native_control_box` | `smoke_passed` | `[]` | `0.0404565` | `-3.745e-06` | `12,15,15,26` |
| `native_opt_in_cylinder` | `runtime_failure` | `not_settled` | `0.0823040` | `-2.949e-06` | `12,15,15,26` |
| `native_opt_in_cylinder_reverted` | `smoke_passed` | `[]` | `0.0404565` | `-3.745e-06` | `12,15,15,26` |
| `native_opt_in_cylinder_with_native_box_com` | `smoke_passed` | `[]` | `0.0425127` | `-6.039e-06` | `12,15,15,26` |
| `native_opt_in_cylinder_with_native_box_inertia_tensor` | `smoke_passed` | `[]` | `0.0427094` | `-2.084e-06` | `12,15,15,26` |
| `native_opt_in_cylinder_with_native_box_mass` | `runtime_failure` | `not_settled` | `0.0962726` | `-5.681e-06` | `12,15,15,26` |
| `native_opt_in_cylinder_with_native_box_mass_inertia` | `runtime_failure` | `not_settled` | `0.0618353` | `-3.879e-06` | `12,15,15,26` |

## Compact Pair-Control Boundary

The compact clean-control report still contains pair-level contact/floor anomalies:

- single-primitive bed box, bed cylinder, and largest recorded Franka cylinder controls all pass;
- some local two-primitive bed pairs fail `not_settled` for both box and cylinder variants;
- two local cylinder-only pair controls fail `floor_breach`.

Those pair controls remain useful warning evidence that contact/floor behavior can be sensitive in
local contexts. They do not match the recorded full-package bed blocker, where the failing label is
`not_settled`, not `floor_breach`, and where same-report passing/failing full-package variants
share the final support/contact set.

## Interpretation

For the recorded capped-bed full-compound blocker, contact/floor is now unlikely as the primary
mechanism. The same final ground-contact set and near-zero support heights appear in both failing
and passing full-package variants. The label flips when COM/inertia body-state fields are changed,
while contact count and final contact primitive suffixes do not change.

The more precise current answer is:

- full-compound package context is required;
- large-flat cylinder geometry is the risky package change;
- the observed full-package failure is a residual final-speed `not_settled` behavior tied to
  COM/inertia body-state sensitivity;
- pair-level contact/floor anomalies remain secondary local-context evidence, not the best
  explanation for the recorded full-package bed-vs-Franka contrast.

## Claim Impact

This closes the previous "contact/floor may be the full-package main cause" gap for the recorded
capped-bed full-compound evidence. It does not close all contact/floor questions, prove physical
causality, validate a repair, or justify a default selector policy.

## Verification

- Baseline worktree tests:
  `python -m pytest tests/test_cylinder_clean_controls.py tests/test_cylinder_stability_mechanism.py -q`:
  `6 passed`.
- Parsed `reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`
  and confirmed the ten full-package variants share final contact count `4` and contact suffixes
  `12,15,15,26`.
- Parsed `reports/generated/cylinder_clean_controls/compact_probe.json` and confirmed the
  pair-level `floor_breach` labels are limited to compact local pair controls, not the recorded
  full-package bed blocker.

## Next Action

The remaining strict-goal gap is no longer contact/floor as a likely primary mechanism. The next
useful endpoint is either a non-Newton-array package-level repair candidate or a completion audit
that decides whether the current diagnostic mechanism answer is enough for the thread goal while
preserving claim boundaries.
