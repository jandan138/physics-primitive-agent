# 2026-05-22 Cylinder Mechanism Decision Matrix

## Date

2026-05-22

## Status

Mechanism decision matrix recorded from the current real Newton evidence. This record does not add
a new runner; it consolidates the dated mechanism report, compact clean-control probe, and
full-compound repair-candidate controls into one hypothesis-by-hypothesis answer for the active
bed-vs-Franka cylinder question.

The current best answer is: the recorded capped bed `not_settled` label requires full-compound
context and is best explained by body-state sensitivity, especially aggregate COM and inertia,
introduced by one large flat selected cylinder. Geometry alone, center shift alone, mass alone,
and categorical Newton cylinder unsupported behavior are all contradicted by the current controls.
Pair-level contact/floor effects remain an open secondary factor, but the full-package recorded
failure is a final-speed `not_settled` label under the same final support-contact set as passing
body-state controls.

This is still diagnostic synthesis over one capped bed/Franka slice, not root-cause proof, a
validated COM/inertia repair, selector calibration, collision-quality validation, benchmark
evidence, or safety evidence.

## Evidence Inputs

- `reports/generated/cylinder_stability_mechanism/mechanism_report.json`
- `reports/generated/cylinder_clean_controls/compact_probe.json`
- `reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`
- [Cylinder stability mechanism diagnosis](2026-05-21-cylinder-stability-mechanism-diagnosis.md)
- [Cylinder clean-control probe](2026-05-22-cylinder-clean-control-probe.md)
- [Cylinder repair-candidate controls](2026-05-22-cylinder-repair-candidate-controls.md)

## Decision Matrix

| Hypothesis | Current status | Main evidence | Boundary |
| --- | --- | --- | --- |
| Categorical Newton `cylinder` unsupported behavior | Rejected for this recorded question | Franka cost-guided package contains `7` cylinders and passes; largest recorded Franka cylinder also passes as a single primitive. | Does not prove all cylinders are safe or stable. |
| Bed large-flat cylinder geometry alone | Rejected as sole cause | The exact bed target cylinder passes as a single primitive; the full bed opt-in package fails. | Large-flat geometry still matters as the selected shape that changes full-package body state. |
| Center shift alone | Rejected as sole cause | `box_at_cylinder_center` passes while `cylinder_at_box_center` still fails. | Does not rule out center participating through full body-state accounting. |
| Full-compound package context | Required for the recorded `not_settled` label | Single bed cylinder passes; full bed opt-in fails; native all-box and cylinder-reverted controls pass. | Required context is not by itself the physical mechanism. |
| Aggregate COM | Strong positive evidence | Native all-box `body_com` only clears the recorded full-package label while retaining cylinder geometry, mass, and inertia; COM-axis/blend records show coupled COM sensitivity. | One-config pre-solver field control, not a validated physical COM repair. |
| Inertia tensor | Strong positive evidence | Native all-box `body_inertia`/`body_inv_inertia` only clears the recorded full-package label while retaining opt-in COM. | One-config field control; does not prove a general inertial repair. |
| Mass | Negative as sole mechanism | Native all-box `body_mass`/`body_inv_mass` only remains `not_settled` and records higher final speed than the original opt-in run. | Mass can still affect dynamics, but it is not the clearing component in this evidence. |
| Mass plus inertia without COM | Negative under the recorded 360-frame gate | Mass+inertia while retaining opt-in COM remains `not_settled`. | A 361-frame record cleared this variant; use the 360-frame recorded gate for this matrix. |
| Full inertial-array body-state copy | Strong sensitivity evidence | Full native all-box mass/COM/inertia array copy clears the recorded label with cylinder geometry retained. | Direct Newton array copy is diagnostic only, not a package-level repair. |
| Final contact/support labels as sole cause | Unlikely for the full-package recorded label | Original failing opt-in, COM-only pass, inertia-only pass, mass-only fail, native/reverted controls all record final contact count `4`, near-zero support height, and the same final support primitive suffixes `12`, `15`, `15`, `26`. | Pair-level cylinder-only `floor_breach` controls keep contact/floor effects open as secondary context. |
| Pair-level contact/floor interaction | Open secondary factor | Compact pair controls are mixed: some box and cylinder pairs both fail `not_settled`, two cylinder-only pairs fail `floor_breach`, and one pair passes for both. | Those labels differ from the full bed package's recorded `not_settled` label. |
| Franka-vs-bed contrast | Explained by size plus context in current evidence | Bed selected cylinder radius is about `2.7009381 m`; largest recorded Franka cylinder radius is about `0.0019825 m`; Franka package passes in its recorded context. | Does not establish a broad bed/Franka benchmark or cylinder quality ranking. |

## Compact Answer

The recorded bed cylinder is not failing because Newton categorically cannot handle cylinders, and
it is not failing because the cylinder geometry alone is unstable. The failure appears only when
that large flat cylinder participates in the full capped bed compound package. In that context,
the selected primitive changes the aggregate Newton body state: the full opt-in package has
nonzero target/full mass, COM, and inertia deltas while the rest-without-target deltas are zero.

The strongest current mechanism is full-compound COM/inertia body-state sensitivity. COM-only and
inertia-only native all-box overrides both clear the recorded 360-frame final-speed label; mass
only does not. The final support-contact set remains the same across failing and passing
body-state variants, so the recorded full-package label is best treated as residual final-speed
behavior under similar final support contacts, not as a missing-contact or target-only contact
reproducer.

The Franka cylinders pass because the recorded Franka cylinder package is a different compound
context with much smaller cylinders and no corresponding residual-speed failure under the same
recorded task-smoke gate.

## Claim Impact

- It is now appropriate to describe the current answer as a claim-bounded mechanism diagnosis:
  full-compound COM/inertia body-state sensitivity is the best current explanation for the
  recorded bed-vs-Franka cylinder contrast.
- Keep pair-level contact/floor interaction open as a secondary factor.
- Do not call this root-cause proof, a validated COM/inertia repair, sustained settling,
  selector calibration, benchmark evidence, collision-quality validation, or safety evidence.

