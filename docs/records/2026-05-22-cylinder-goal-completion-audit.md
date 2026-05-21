# 2026-05-22 Cylinder Goal Completion Audit

## Date

2026-05-22

## Status

Superseded for goal-status purposes by
[2026-05-22 Cylinder Goal Completion Audit After Contact Closure](2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md).
This record remains useful for the pre-contact-closure audit state.

## Objective Audited

Resolve why the capped bed selected cylinder records `not_settled` while recorded Franka cylinders
pass: decide whether the explanation comes from geometry ratio, inertia, COM, contact/floor
interaction, or full compound package context.

## Audit Result

Do not mark the goal complete yet under the strict completion audit. The current evidence is
strong enough for a claim-bounded mechanism diagnosis, but it is not strong enough for root-cause
proof or a validated repair.

The practical current answer is:

- The recorded bed failure requires full-compound package context.
- The best current mechanism is full-compound body-state sensitivity, especially aggregate COM
  and inertia, introduced by one large flat selected cylinder.
- Geometry alone, center shift alone, mass alone, and categorical Newton `cylinder` unsupported
  behavior are contradicted as sole explanations.
- Final contact/support labels are unlikely as the sole full-package explanation, but pair-level
  contact/floor effects remain open secondary context.
- Franka passes in the recorded evidence because its cylinder package is a different compound
  context with much smaller cylinders and no corresponding residual-speed failure under the same
  task-smoke gate.

## Requirement Audit

| Requirement from objective | Current evidence | Audit status |
| --- | --- | --- |
| Reproduce the bed `not_settled` contrast against Franka passing cylinders | Bed opt-in reproduces `not_settled` at about `0.0823040 m/s`; Franka cost-guided opt-in with `7` cylinders passes at about `0.0007108 m/s`. | Achieved for the recorded capped bed/Franka slice. |
| Decide whether Newton categorically cannot handle cylinders | Franka cylinder packages pass; largest recorded Franka cylinder passes as a single primitive. | Rejected for this recorded question. |
| Decide whether bed cylinder geometry alone causes the failure | Exact bed target cylinder passes alone; full bed opt-in fails. | Rejected as sole cause. |
| Decide whether geometry still matters | Bed selected cylinder is a large flat class: radius about `2.7009381 m`, half-height/radius about `0.0788772`, much larger than recorded Franka cylinders. | Supported as risk-shape context, not sole mechanism. |
| Decide whether full package context matters | Single bed cylinder passes; full opt-in bed package fails; native all-box and cylinder-reverted controls pass. | Required for the recorded label. |
| Decide whether COM matters | Native all-box `body_com` only clears the recorded full-package final-speed label while retaining cylinder geometry, mass, and inertia. | Strong positive sensitivity evidence. |
| Decide whether inertia matters | Native all-box `body_inertia`/`body_inv_inertia` only clears the recorded full-package label while retaining opt-in COM. | Strong positive sensitivity evidence. |
| Decide whether mass alone explains it | Native all-box `body_mass`/`body_inv_mass` only remains `not_settled` and records higher final speed than the original opt-in run. | Rejected as sole mechanism. |
| Decide whether contact/floor is the explanation | Original fail, COM-only pass, inertia-only pass, mass-only fail, native control, and cylinder-reverted control all record final contact count `4`, near-zero final support height, and the same final support primitive suffixes. Pair controls still include cylinder-only `floor_breach` cases. | Sole full-package contact explanation is unlikely; contact/floor remains secondary-open. |
| Explain why Franka passes | Recorded Franka cylinders are much smaller and pass in their package context; no corresponding residual final-speed failure is recorded. | Achieved for the recorded capped Franka slice; not broad Franka/cylinder generalization. |
| Provide physical root-cause proof | Current records are one-config Newton sensitivity controls and diagnostic synthesis. | Not achieved. |
| Provide validated COM/inertia repair or selector policy | Pre-solver field overrides and array copies are diagnostic only; current guard evidence remains opt-in diagnostic policy evidence. | Not achieved. |

## Why Goal Stays Active

The original question is now answered at the diagnostic-mechanism level, but strict completion
would require at least one of the following stronger endpoints:

1. A validated package-level mechanism proof that does not rely on direct pre-solver Newton array
   copying.
2. A validated repair or selector/risk policy that prevents the capped bed failure and preserves
   recorded Franka cylinder passes under the intended config scope.
3. A stronger contact/floor closure showing that the open pair-level `floor_breach` controls do
   not affect the full-package bed mechanism, or explicitly classifying them as a separate
   mechanism.

Until then, keep the goal active and describe the state as a claim-bounded mechanism diagnosis,
not a completed root-cause proof or fixed system.

## Next Minimal Work

The next useful slice should be a package-level risk/repair candidate that does not directly copy
Newton model arrays:

- compute a report-only full-package body-state delta or large-flat-cylinder risk feature from
  package geometry;
- check that it flags the recorded capped bed large-flat cylinder case;
- check that it does not block the recorded capped Franka cost-guided cylinder package;
- run the existing bed/Franka task smokes only after the risk rule is explicitly opt-in and
  claim-bounded.
