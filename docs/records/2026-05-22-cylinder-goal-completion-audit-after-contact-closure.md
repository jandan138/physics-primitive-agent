# 2026-05-22 Cylinder Goal Completion Audit After Contact Closure

## Date

2026-05-22

## Objective Audited

Resolve why the capped bed selected cylinder records `not_settled` while recorded Franka cylinders
pass: decide whether the explanation comes from geometry ratio, inertia, COM, contact/floor
interaction, or full compound package context.

## Completion Decision

The active thread goal is complete for the recorded capped bed/Franka diagnostic question.

The answer is:

- The recorded bed `not_settled` label is a full-compound package effect.
- The risky package change is one very large flat selected bed cylinder.
- That geometry does not fail alone; it matters because it changes full-compound body-state
  accounting.
- The strongest supported mechanism is full-compound COM/inertia body-state sensitivity that
  leaves residual final speed above the drop/settle gate.
- Mass alone is rejected as the explanation.
- Contact/floor is no longer the likely primary full-package mechanism after same-report
  contact/support closure; compact pair-level contact/floor anomalies remain secondary local
  context.
- Franka cylinders pass because the recorded Franka cylinder packages are different compound
  contexts with much smaller cylinders and no corresponding residual final-speed failure under the
  recorded task gate.

This completes the "why bed cylinder fails while Franka cylinders pass" diagnostic objective. It
does not complete broader work such as calibrated thresholds, a default selector policy, a
physically validated COM/inertia repair, broad cylinder stability evidence, benchmark evidence,
collision-quality validation, or safety evidence.

## Requirement Audit

| Requirement from objective | Current evidence | Audit status |
| --- | --- | --- |
| Reproduce bed `not_settled` against Franka passing cylinders | The recorded bed opt-in package fails drop/settle with final speed about `0.0823040 m/s`; the recorded Franka cost-guided cylinder package passes with final speed about `0.0007108 m/s`. | Achieved for the recorded capped bed/Franka scope. |
| Decide whether Newton categorically cannot handle cylinders | Franka packages containing cylinders pass; the largest recorded Franka cylinder also passes as a single primitive. | Rejected for this recorded question. |
| Decide whether bed cylinder geometry alone causes the failure | The exact bed target cylinder passes as a single primitive; the full bed opt-in package fails. | Rejected as sole cause. |
| Decide whether geometry ratio matters | The bed selected cylinder is a large-flat risk shape: radius about `2.7009381 m`, half-height/radius about `0.0788772`, and about `1362x` the largest recorded Franka cylinder radius. | Supported as the risky package-changing shape context. |
| Decide whether full compound package context matters | Single bed cylinder passes; full bed opt-in package fails; native all-box and cylinder-reverted full packages pass. | Required for the recorded label. |
| Decide whether COM matters | Native all-box `body_com` only clears the full-package label while retaining cylinder geometry, mass, and inertia. | Strong positive sensitivity evidence. |
| Decide whether inertia matters | Native all-box `body_inertia`/`body_inv_inertia` only clears the full-package label while retaining opt-in COM. | Strong positive sensitivity evidence. |
| Decide whether mass alone explains it | Native all-box `body_mass`/`body_inv_mass` only remains `not_settled` and records higher final speed than the original opt-in run. | Rejected as sole mechanism. |
| Decide whether contact/floor explains the full-package failure | Ten same-report full-package variants share final contact count `4`, final contact suffixes `12,15,15,26`, and near-zero support heights. Failing full-package variants fail `not_settled`, not `floor_breach`. | Rejected as the likely primary full-package mechanism; retained as secondary local-context evidence from compact pair controls. |
| Explain why Franka passes | Recorded Franka cylinders are much smaller and pass in their package context; the package body-state proxy does not flag the recorded Franka cylinder package, and no corresponding residual final-speed failure is recorded. | Achieved for the recorded capped Franka scope. |
| Keep claim boundaries | All records describe this as a diagnostic mechanism answer over recorded capped bed/Franka slices, not broad cylinder evidence, benchmark evidence, collision-quality validation, or safety evidence. | Achieved. |

## Evidence Used

- `reports/generated/cylinder_stability_mechanism/mechanism_report.json`
- `reports/generated/cylinder_clean_controls/compact_probe.json`
- `reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`
- `reports/generated/bed_franka_native_opt_in_package_body_state_guard_probe/task_2026-05-22.json`
- [Cylinder stability mechanism diagnosis](2026-05-21-cylinder-stability-mechanism-diagnosis.md)
- [Cylinder clean-control probe](2026-05-22-cylinder-clean-control-probe.md)
- [Cylinder repair-candidate controls](2026-05-22-cylinder-repair-candidate-controls.md)
- [Cylinder contact/floor closure audit](2026-05-22-cylinder-contact-floor-closure-audit.md)
- [Package body-state guard task path](2026-05-22-package-body-state-guard-task-path.md)

## Final Mechanism Statement

For the recorded capped bed/Franka Newton reproduction story, the bed cylinder does not fail
because cylinders are categorically unsupported or because that cylinder is unstable in isolation.
It fails when that large flat cylinder participates in the full bed compound package. In that
context, the package's COM/inertia body-state changes enough to leave residual final speed above
the recorded drop/settle threshold. Franka cylinders pass because their recorded package context
uses much smaller cylinders and does not show the same body-state risk or residual-speed failure.

## Remaining Non-Goals

- No calibrated default selector or guard threshold is claimed.
- No physically validated COM/inertia repair is claimed.
- No broad cylinder stability, bed/Franka benchmark, whole-robot collider-quality, or
  collision-quality validation claim is supported.
- No safety guarantee, deployment readiness, or real-world transfer claim is supported.

## Verification

- `python -m pytest tests/test_cylinder_clean_controls.py tests/test_cylinder_stability_mechanism.py tests/test_cylinder_package_risk.py -q`:
  `8 passed`.
- Parsed the current mechanism, clean-control, repair-control, and package guard generated reports
  listed above.

## Next Action

Treat this specific thread goal as answered. Future work should start a new goal around one of the
remaining non-goals: calibrated selector policy, repair validation, broader asset coverage, or
collision-quality evaluation.
