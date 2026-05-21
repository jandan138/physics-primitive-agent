# 2026-05-22 Cylinder Package Body-State Risk Probe

## Date

2026-05-22

## Status

Diagnostic package-risk probe recorded. This slice addresses the completion-audit gap for a
package-level body-state check that does not rely on direct pre-solver Newton model array copying.
It is still not root-cause proof, not a validated repair, and not a default selector policy.

## Changes

- Added `primitive_collision_compiler.diagnostics.cylinder_package_risk`, a report-only helper
  that computes volume-weighted package COM and inertia proxy features from `CollisionPackage`
  geometry.
- Added `scripts/diagnostics/cylinder_package_risk_probe.py`, which reads existing bed/Franka
  task reports and builds the same package-risk report without importing Newton or copying Newton
  model arrays.
- Added tests for the package geometry proxy and script-level bed/Franka report path.

## Recorded Real-Report Probe

Command:

```bash
PYTHONPATH=src python scripts/diagnostics/cylinder_package_risk_probe.py \
  --bed-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/bed_task.json \
  --franka-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json \
  --output reports/generated/cylinder_package_risk/bed_franka_package_risk.json
```

Result:

- `status: diagnostic_recorded`
- `contrast_assessment.assessment:
  bed_flagged_franka_not_flagged_matches_recorded_drop_contrast`
- bed package risk class: `large_flat_cylinder_body_state_delta_risk`
- Franka package risk class: `not_flagged`
- bed proxy COM delta norm: `0.29959574154339425 m`
- Franka proxy COM delta norm: `0.0007442881840283764 m`
- bed proxy inertia Frobenius delta: `37994.34752251509`
- Franka proxy inertia Frobenius delta: `1.192397515639078e-13`
- bed max cylinder radius: `2.700938098039964 m`
- Franka max cylinder radius: `0.001982486358351284 m`
- bed min half-height/radius: `0.07887716832535864`
- Franka min half-height/radius: `0.0009153215850011186`

The generated report is ignored by git under
`reports/generated/cylinder_package_risk/bed_franka_package_risk.json`.

## Claim Impact

This strengthens the current mechanism story because a package-level geometry proxy now flags the
recorded bed case and does not flag the recorded Franka cost-guided cylinder package without using
Newton model arrays. It supports the claim that the bed/Franka contrast is aligned with
large-flat-cylinder full-package COM/inertia body-state risk.

It does not prove the physical root cause, does not validate a COM/inertia repair, does not close
contact/floor effects, and does not establish a default selector or risk policy.

## Verification

- `python -m pytest tests/test_cylinder_package_risk.py -q`
- `python -m pytest tests/test_bootstrap_command_surface.py::test_cylinder_package_risk_probe_builds_bed_franka_report -q`
- Real-report probe command above, exit `0`

## Next Action

Turn the report-only risk feature into an explicitly opt-in selector or repair candidate and run
the recorded bed/Franka task smokes to check that it prevents the bed `not_settled` case while
preserving the recorded Franka cylinder pass.
