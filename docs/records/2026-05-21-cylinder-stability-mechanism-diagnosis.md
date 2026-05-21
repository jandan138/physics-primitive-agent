# 2026-05-21 Cylinder Stability Mechanism Diagnosis

## Date

2026-05-21

## Status

Diagnostic synthesis recorded. The current strongest hypothesis is not a categorical Newton
`cylinder` failure. The recorded evidence points to full-compound body-state sensitivity introduced
by selecting one large flat cylinder: the package maps and contacts, but the cylinder package delta
changes aggregate COM/inertia enough that the recorded drop/settle final-speed gate stays above
threshold. The recorded Franka cylinders pass because they are a much smaller cylinder class in a
different compound package context.

This is not root-cause proof, a validated inertial repair, collision-quality validation, or a
default selector policy.

## Changes

- Added `primitive_collision_compiler.diagnostics.cylinder_stability`, a small claim-bounded
  diagnostic synthesis helper.
- Added `tests/test_cylinder_stability_mechanism.py`.
- Reran the capped bed opt-in task comparison and capped Franka cost-guided opt-in task comparison
  in the clean Newton environment.
- Generated ignored local report:
  `reports/generated/cylinder_stability_mechanism/mechanism_report.json`.

## Verification

- RED: `python -m pytest tests/test_cylinder_stability_mechanism.py -q` initially failed because
  `primitive_collision_compiler.diagnostics` did not exist.
- RED: after adding the report helper, the same test failed because
  `cylinder_geometry_from_package` did not exist.
- RED: reviewer hardening cases then failed on missing `primitive_kind_counts`, string
  `failure_labels`, multi-case role selection, and unconditional strong-hypothesis wording.
- GREEN: `python -m pytest tests/test_cylinder_stability_mechanism.py -q`:
  exit `0`, `5 passed`.
- Bed reproduction:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cylinder-stability-mechanism/src:$PYTHONPATH timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_probe.yaml --run-real-usd-native-task-comparison > reports/generated/cylinder_stability_mechanism/bed_task.json`:
  exit `2`, report `status: runtime_failure`.
- Franka reproduction:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=/cpfs/user/zhuzihou/dev/physics-primitive-agent/.worktrees/cylinder-stability-mechanism/src:$PYTHONPATH timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_cost_guided_merge_probe.yaml --run-real-usd-native-task-comparison > reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json`:
  exit `0`, report `status: smoke_passed`.
- Mechanism report generation:
  `PYTHONPATH=src:$PYTHONPATH python - <<'PY' ... PY` using
  `build_cylinder_stability_mechanism_report` and `cylinder_geometry_from_package`:
  exit `0`, report `status: diagnostic_recorded`.
- Mechanism report assertions:
  `PYTHONPATH=src:$PYTHONPATH python - <<'PY' ... PY`:
  exit `0`, `mechanism report assertions passed`.

## Key Results

- Bed opt-in reproduced the historical blocker:
  - default legacy/native lanes: `32` boxes, contact/drop/sphere all `smoke_passed`;
  - default/native drop final speed: about `0.0404565 m/s`;
  - opt-in lane: `31` boxes plus `1` cylinder;
  - opt-in contact: `smoke_passed`;
  - opt-in drop/settle: `runtime_failure`, failure labels `["not_settled"]`;
  - opt-in drop final speed: about `0.0823040 m/s`;
  - opt-in final contact count: `4`;
  - opt-in final support height: about `-0.00000295 m`;
  - opt-in sphere-rain: `smoke_passed`.
- Franka cost-guided opt-in reproduced the passing cylinder-containing package:
  - default legacy/native lanes: `32` boxes, contact/drop/sphere all `smoke_passed`;
  - opt-in lane: `25` boxes plus `7` cylinders;
  - opt-in contact/drop/sphere: all `smoke_passed`;
  - opt-in drop final speed: about `0.0007108 m/s`;
  - opt-in final contact count: `117`;
  - opt-in final support height: about `-0.0001043 m`.
- The failing bed cylinder is geometry-class distinct from the passing Franka cylinders:
  - bed cylinder index `6`, source faces `[32..39]`;
  - bed cylinder radius about `2.7009381 m`;
  - bed cylinder half-height about `0.2130423 m`;
  - bed half-height/radius ratio about `0.0788772`;
  - Franka cost-guided opt-in has `7` cylinders;
  - largest recorded Franka cylinder radius is about `0.0019825 m`;
  - bed max cylinder radius is about `1362x` the largest Franka cylinder radius in this capped
    comparison.

## Cause Assessment

- Mapping or contact gap is unlikely as the direct cause: both bed and Franka opt-in lanes pass
  representative contact canaries, and the bed failure appears downstream in drop/settle.
- Categorical Newton `cylinder` unsupported behavior is unlikely: Franka packages containing
  `8`, `3`, and now `7` cylinders have reached the recorded task smokes.
- Center shift alone is unlikely from the prior center/shape control: `box_at_cylinder_center`
  passed while `cylinder_at_box_center` still failed.
- Final support-contact labels alone are unlikely as the full explanation: the clean-frame blocker
  audit recorded matching final support-contact primitive suffixes for the failing opt-in cylinder
  and passing box/revert controls.
- Isolated target-cylinder behavior is insufficient: the target-only and nearest-neighbor local
  controls passed, so the one-cylinder full-package blocker is not reproduced by the standalone
  primitive.
- Full-compound context is supported: the full bed opt-in package fails while all-box and
  cylinder-reverted controls pass under the clean-control windows.
- COM/inertia body-state sensitivity is the strongest current hypothesis:
  - copying native all-box mass/COM/inertia arrays into the opt-in cylinder model clears the
    recorded label in one run;
  - copying only native all-box `body_com` also clears the recorded label while keeping cylinder
    geometry and mass/inertia;
  - mass-only does not clear the label;
  - inertia-only clears the 360/361 final-speed gates in the recorded component ablations.

## Interpretation

The current evidence-supported working interpretation for "why does bed fail while Franka passes?"
is:

1. The current records point away from missing Newton cylinder mapping or the contact canary as the
   direct explanation.
2. The bed selected cylinder is a large flat shape selected by a narrow opt-in score change.
3. That shape changes full-compound aggregate body state, especially COM/inertia, enough to leave
   residual final speed above the current drop/settle threshold.
4. Franka's recorded cylinders are much smaller and, in the recorded capped package contexts, do
   not produce the same final-speed failure.
5. The current guard is therefore a diagnostic risk control for the large-flat-cylinder class, not
   a proof that all bed cylinders are bad or all Franka cylinders are good.

## Claim Impact

- This strengthens the explanation for the guarded selector story: the guard avoids the large-flat
  bed cylinder class that produced the recorded full-compound body-state sensitivity.
- This does not validate cylinder quality, COM/inertia repair, a score multiplier, a default
  selector policy, merge-policy superiority, benchmark behavior, deployment readiness, safety
  certification, or real-world transfer.
- The next useful work, if continuing this thread, is a compact clean-control reproducer that
  separates large-flat geometry, aggregate COM/inertia, and contact manifold effects without the
  full bed asset.
