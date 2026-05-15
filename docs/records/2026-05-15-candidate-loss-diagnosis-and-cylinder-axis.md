# 2026-05-15 Candidate Loss Diagnosis And Cylinder Axis

## Date

2026-05-15

## Status

Complete

## Changes

- Added `cpd_like_real_usd_candidate_loss_diagnosis`, a real-USD per-selected-cluster diagnosis
  report for native lanes.
- Added CLI flag `--run-real-usd-candidate-loss-diagnosis`.
- Changed the `cylinder` proxy fitter to evaluate all candidate axes and select the lowest-volume
  containing cylinder. Capsule and capped-cylinder fitting remain on the previous longest-axis
  proxy.
- Added a deterministic squat-cylinder synthetic fixture to the native fitting comparison.
- Re-ran local-mirror bed/Franka fitting, candidate-loss diagnosis, contact, and task reports.

## Verification

- `python -m pytest -q tests/test_real_usd_native_comparison.py tests/test_cpd_like_synthetic.py tests/test_cpd_like_decompose.py tests/test_cli.py tests/test_cpd_like_config.py` exited 0 with 122 passed.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --check-assets` exited 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_native_fitting_comparison.yaml --run-newton-native-fitting-comparison` exited 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-candidate-loss-diagnosis` exited 0.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison` exited 0.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-contact-comparison` exited 0.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-task-comparison` exited 0.
- `python -m pytest -q` exited 0 with 268 passed.
- `python scripts/validate_docs.py` exited 0 with docs validation passed.
- `python scripts/validate_site_claims.py` exited 0 with site claim validation passed.
- `git diff --check` exited 0.

## Artifacts

- `reports/generated/asset_materialization/bed_franka_check_assets_after_candidate_loss.json`
- `reports/generated/newton_native_fitting_comparison/synthetic_native_fitting_after_cylinder_axis.json`
- `reports/generated/candidate_loss_diagnosis/bed_franka_candidate_loss_diagnosis.json`
- `reports/generated/bed_franka_native_probe_comparison/fitting_after_candidate_loss_and_cylinder_axis.json`
- `reports/generated/bed_franka_native_probe_comparison/contact_after_candidate_loss_and_cylinder_axis.json`
- `reports/generated/bed_franka_native_probe_comparison/task_after_candidate_loss_and_cylinder_axis.json`

## Result Summary

- Synthetic native fitting now includes four matched fixtures: `cylindrical_rod -> cylinder`,
  `tapered_cone -> cone`, `ellipsoid_blob -> ellipsoid`, and `squat_cylinder -> cylinder`.
- Current bed native lane remains `32` boxes.
- Current Franka native lane selects `29` boxes plus `3` cylinders under the surrogate.
- Candidate-loss diagnosis reports `32` bed box-selected clusters with extension candidates more
  expensive than the selected box, and `29` such Franka clusters plus `3` native-extension-selected
  Franka clusters.
- Bed and Franka old/new packages passed contact canaries and gated drop/settle plus sphere-rain
  task smokes under the recorded config.

## Claim Impact

This supports candidate-loss diagnostic accounting and a controlled synthetic cylinder-axis
fitting smoke. It does not support collision-quality validation, benchmark superiority, native
primitive improvement claims for bed/Franka, whole-robot Franka collider-quality claims, full CPD
paper reproduction, deployment readiness, or safety certification.

## Next Action

Use the candidate-loss diagnosis labels to choose the next narrow primitive-fitting or merge-search
change, then repeat the synthetic-first and bed/Franka-gated sequence.
