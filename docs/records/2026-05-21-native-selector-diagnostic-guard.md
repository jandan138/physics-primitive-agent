# 2026-05-21 Native Selector Diagnostic Guard

## Date

2026-05-21

## Status

Complete.

## Change

- Added an opt-in `native_opt_in_selection_guard` path for CPD-like primitive selection.
- The current guard is a diagnostic quarantine for large flat cylinder candidates:
  `radius > 0.5` and `half_height / radius < 0.1`.
- The guard is only threaded into explicitly configured `native_opt_in` lanes. Default
  `legacy` and `native` lanes remain unchanged.
- The historical unguarded bed and Franka opt-in configs remain unchanged so the previous blocker
  and passing records stay reproducible.
- Added guarded configs:
  `configs/experiments/bed_native_opt_in_guard_probe.yaml` and
  `configs/experiments/franka_native_opt_in_guard_probe.yaml`.
- Candidate-audit summaries now report diagnostic guard rejection counts separately from
  support-blocked extension candidates.

## Verification

- `python -m pytest tests/test_cpd_like_synthetic.py::test_selection_guard_rejects_oversized_native_extension_candidate tests/test_cpd_like_synthetic.py::test_selection_guard_reason_takes_precedence_over_low_support tests/test_cpd_like_decompose.py::test_decompose_mesh_applies_opt_in_primitive_selection_guard tests/test_cpd_like_decompose.py::test_decompose_mesh_rejects_bad_primitive_selection_guard tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_applies_opt_in_selection_guard tests/test_real_usd_native_comparison.py::test_real_usd_native_task_comparison_threads_opt_in_selection_guard tests/test_cpd_like_config.py::test_franka_native_opt_in_probe_config_is_real_usd_and_claim_bounded tests/test_cpd_like_config.py::test_bed_native_opt_in_probe_config_is_real_usd_and_claim_bounded tests/test_cpd_like_config.py::test_native_opt_in_guard_probe_configs_are_real_usd_and_claim_bounded tests/test_cpd_like_config.py::test_bed_native_opt_in_frame_sweep_configs_preserve_historical_selection_scope -q`:
  exit `0`, `10 passed`.
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cpd_like_decompose.py tests/test_real_usd_native_comparison.py tests/test_cpd_like_config.py -q`:
  exit `0`, `133 passed`.
- `python -m pytest tests/test_cli.py::test_cli_run_real_usd_native_fitting_comparison_reads_selection_guard tests/test_cli.py::test_cli_run_real_usd_native_fitting_comparison_reads_score_multipliers -q`:
  exit `0`, `2 passed`.
- `python -m pytest -q`: exit `0`, `2411 passed, 2 skipped`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_guard_probe.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, report `status: smoke_passed`. The guarded capped-bed opt-in lane selected `32`
  boxes, and the candidate audit reported `23` diagnostic guard rejected cylinder candidates.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_guard_probe.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, report `status: smoke_passed`. The guarded capped-Franka opt-in lane remained `24`
  boxes plus `8` cylinders, and the candidate audit reported `0` diagnostic guard rejections.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_guard_probe.yaml --run-real-usd-native-task-comparison`:
  exit `0`, report `status: smoke_passed`. The guarded capped-bed opt-in package passed contact,
  drop/settle, and sphere-rain.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_native_opt_in_guard_probe.yaml --run-real-usd-native-task-comparison`:
  exit `0`, report `status: smoke_passed`. The guarded capped-Franka opt-in package retained
  `8` cylinders and passed contact, drop/settle, and sphere-rain. The stderr log includes Newton
  inertia-validation correction warnings for representative contact canaries, while the JSON
  diagnostic status remains `smoke_passed`.

## Artifacts

- Bed fitting report:
  `reports/generated/native_selector_diagnostic_guard/bed_fitting_guard_2026-05-21.json`
  (ignored; not committed).
- Bed Newton task report:
  `reports/generated/native_selector_diagnostic_guard/bed_task_guard_2026-05-21.json`
  (ignored; not committed).
- Franka fitting report:
  `reports/generated/native_selector_diagnostic_guard/franka_fitting_guard_2026-05-21.json`
  (ignored; not committed).
- Franka Newton task report:
  `reports/generated/native_selector_diagnostic_guard/franka_task_guard_2026-05-21.json`
  (ignored; not committed).

## Claim Impact

- Supports only that a Newton-diagnosis-informed, opt-in selection guard can change the capped-bed
  opt-in package away from the previously blocked large flat cylinder candidate and that the
  resulting guarded package reaches the recorded Newton task smokes.
- Supports that the same guard does not reject the currently recorded capped-Franka small-cylinder
  opt-in selections.
- Does not support collision-quality validation, benchmark superiority, default config changes,
  calibrated cylinder multipliers, proof that boxes are better than cylinders, broad real-USD
  coverage, whole-robot Franka collider quality, full CPD reproduction, deployment readiness,
  safety certification, or real-world transfer.

## Next Action

- Treat this as a controlled selector-diagnostic slice. Any broader policy, threshold, or asset
  expansion needs its own config, tests, real-USD report, Newton record, and claim boundary.
