# 2026-05-22 Cylinder Repair-Candidate Controls

## Date

2026-05-22

## Status

Real Newton repair-candidate controls recorded for the capped bed full-compound package. The run
keeps the recorded opt-in cylinder geometry in the full bed package and applies selected
pre-solver Newton body-state overrides from the native all-box control package.

The result strengthens the current mechanism story: the recorded `not_settled` label is cleared
by native all-box `body_com`, by the full native all-box inertial-array copy, and by native all-box
inertia tensors only. It is not cleared by mass-only, and it is not cleared by mass+inertia while
retaining the opt-in `body_com` under the recorded 360-frame gate.

This is still one-config sensitivity evidence, not physical root-cause proof, not a validated
inertial repair, not a selector policy, not collision-quality validation, and not safety evidence.

## Changes

- Reused `scripts/diagnostics/bed_native_opt_in_compound_trace.py`; no new runner was needed.
- Ran the existing full-compound trace with:
  - `--run-inertia-counterfactual`;
  - `--run-inertia-field-ablation`;
  - `--run-inertial-component-ablation`;
  - `--run-model-build-audit`.
- Generated ignored local report:
  `reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`.

## Verification

- Baseline targeted worktree tests:
  `python -m pytest tests/test_cylinder_clean_controls.py tests/test_cylinder_stability_mechanism.py -q`:
  exit `0`, `6 passed`.
- Real Newton repair-candidate controls:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src:$PYTHONPATH timeout 900s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --device cpu --sample-every-steps 2880 --tail-steps 0 --max-contact-details 4 --run-inertia-counterfactual --run-inertia-field-ablation --run-inertial-component-ablation --run-model-build-audit --output reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `python -m json.tool reports/generated/cylinder_repair_controls/bed_full_package_repair_candidates.json >/dev/null`:
  exit `0`.

## Key Results

The run used the recorded 360-frame, 8-substep, 2-iteration drop/settle gate.

- `native_control_box`: `smoke_passed`, final speed about `0.0404565 m/s`.
- `native_opt_in_cylinder`: `runtime_failure`, failure labels `["not_settled"]`, final speed
  about `0.0823040 m/s`.
- `native_opt_in_cylinder_reverted`: `smoke_passed`, final speed about `0.0404565 m/s`.
- `box_at_cylinder_center`: `smoke_passed`, final speed about `0.0464995 m/s`.
- `cylinder_at_box_center`: `runtime_failure`, failure labels `["not_settled"]`, final speed
  about `0.0786721 m/s`.
- `native_opt_in_cylinder_with_native_box_inertia`: full native all-box
  `body_mass`/`body_inv_mass`/`body_com`/`body_inertia`/`body_inv_inertia` copy,
  `smoke_passed`, final speed about `0.0404565 m/s`.
- `native_opt_in_cylinder_with_native_box_com`: native all-box `body_com` only,
  `smoke_passed`, final speed about `0.0425127 m/s`.
- `native_opt_in_cylinder_with_native_box_inertia_tensor`: native all-box
  `body_inertia`/`body_inv_inertia` only, `smoke_passed`, final speed about
  `0.0427094 m/s`.
- `native_opt_in_cylinder_with_native_box_mass`: native all-box
  `body_mass`/`body_inv_mass` only, `runtime_failure`, failure labels `["not_settled"]`, final
  speed about `0.0962726 m/s`.
- `native_opt_in_cylinder_with_native_box_mass_inertia`: native all-box mass plus inertia tensors
  while retaining opt-in `body_com`, `runtime_failure`, failure labels `["not_settled"]`, final
  speed about `0.0618353 m/s`.

All listed variants recorded final contact count `4` and near-zero final support height under the
same task gate. The model-build audit recorded matching package anchors. Its delta summary
localized the nonzero native-vs-opt-in body-state delta to primitive 6: rest-without-target deltas
were zero, while the primitive-6 target and full-package mass/COM/inertia deltas were nonzero.

## Interpretation

The result narrows the active question:

1. Large-flat cylinder geometry alone is not enough, because the previous clean-control probe
   shows the single bed target cylinder settles.
2. Full package context is required, because the full opt-in bed package reproduces
   `not_settled`.
3. Within that full package context, native all-box `body_com` alone clears the recorded label
   while retaining cylinder geometry and mass/inertia.
4. Native all-box inertia tensors also clear the recorded label while retaining opt-in COM.
5. Mass-only does not clear the label and makes the final speed higher in this run.
6. Mass+inertia without COM does not clear the 360-frame gate, so COM remains a necessary part of
   the cleanest current explanation even though inertia is also a strong sensitivity factor.

The practical current answer is therefore: the bed cylinder fails in Newton because the selected
large flat cylinder changes full-compound body-state accounting, especially aggregate COM and
inertia, enough to leave residual final speed above the recorded settle threshold. Franka cylinders
pass because the recorded Franka cylinder package is much smaller and does not create the same
full-compound body-state sensitivity under the recorded gate.

## Claim Impact

- It is now stronger to say the active bed blocker is a full-compound body-state sensitivity, not
  cylinder geometry alone and not categorical Newton cylinder unsupported behavior.
- It is still too strong to claim root cause, physical causality, a validated COM/inertia repair,
  sustained settling, selector calibration, default policy, broad cylinder stability, benchmark
  evidence, collision-quality validation, or safety evidence.

