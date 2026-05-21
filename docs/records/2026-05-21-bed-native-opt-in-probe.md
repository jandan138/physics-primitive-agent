# 2026-05-21 Bed Native Opt-In Probe

## Date

2026-05-21

## Status

Complete record of the completed blocked diagnostic run plus local counterfactual,
field-ablation, and frame-window sensitivity checks to date. The original opt-in lane failed the
drop/settle task gate.

## Changes

- Added explicit bed-only real-USD opt-in config:
  `configs/experiments/bed_native_opt_in_probe.yaml`.
- Added explicit bed-only real-USD opt-in frame-window sensitivity configs:
  `configs/experiments/bed_native_opt_in_frame361_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame362_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame363_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame364_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame365_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame375_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame385_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame390_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame420_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame450_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame480_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame600_probe.yaml`, and
  `configs/experiments/bed_native_opt_in_long_window_probe.yaml` for the `720`-frame member.
- Kept the default support-aware lanes unchanged. The opt-in lane uses the same support-aware
  guard, capped `bed_dev_smoke` first-mesh scope, `256` source faces, and an explicit
  `cylinder: 0.88` score multiplier.

## Verification

- `python -m pytest tests/test_cpd_like_config.py::test_bed_native_opt_in_probe_config_is_real_usd_and_claim_bounded -q`:
  exit `0`, `1 passed`.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_probe.yaml --run-real-usd-native-fitting-comparison`:
  exit `0`, report `status: smoke_passed`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_probe.yaml --run-real-usd-native-task-comparison`:
  exit `2`, report `status: runtime_failure`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_native_opt_in_probe.yaml --run-real-usd-native-task-comparison > reports/generated/bed_native_opt_in_probe/task_rerun_after_com_axis_2026-05-21.stdout.json`:
  exit `2`, report `status: runtime_failure`. This current-worktree rerun preserved the earlier
  pattern: legacy/default native all-box lanes passed, while the opt-in lane failed drop/settle
  and passed sphere-rain.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python` with the local
  one-variable cylinder-revert drop-attribution script:
  exit `0`, report `status: counterfactual_blocker_cleared`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --output reports/generated/bed_native_opt_in_probe/drop_primitive6_compound_trace_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-inertia-counterfactual --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertia_counterfactual_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-inertia-field-ablation --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_field_ablation_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-inertial-component-ablation --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_component_ablation_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This 360-frame diagnostic keeps the opt-in
  cylinder geometry and COM while applying native all-box inertial component groups. The
  mass-only variant remained `not_settled`, the inertia-only variant cleared the recorded
  final-speed gate, and the mass+inertia variant remained `not_settled`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-com-axis-ablation --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_axis_subset_ablation_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-com-blend-ablation --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_ablation_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-com-blend-refinement --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_tail_suffix_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun adds descriptive
  `tail_linear_speed_summary` fields to the same COM-blend refinement variants.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame361_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `361` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame361_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-inertial-component-ablation --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_inertial_component_ablation_frame361_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This repeats the inertial-component ablation
  under the clean-control `361` frame window. The mass-only variant remained `not_settled`, while
  the inertia-only and mass+inertia variants cleared the recorded final-speed gate.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame362_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `362` frames.
- `PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_frame_transition_audit.py --clean-report reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json --dirty-report reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json --variant-label native_control_box --variant-label native_opt_in_cylinder_reverted --output reports/generated/bed_native_opt_in_frame_transition_audit/native_reverted_frame361_362_audit_2026-05-21.stdout.json`:
  exit `0`, report `status: frame_transition_audit_recorded`. This post-run audit compares
  the native all-box and cylinder-reverted controls across the adjacent `361` clean-control and
  `362` dirty-control reports. It records matching Newton model arrays and matching final
  support-contact labels while the `362` row adds `8` substeps and increases final linear speed
  by about `0.0189847 m/s` in both controls. This is a frame-transition audit only, not
  root-cause proof, sustained-settle evidence, a validated fix, or collision-quality validation.
- `PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_clean_frame_blocker_audit.py --report reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json --baseline-label native_control_box --baseline-label native_opt_in_cylinder_reverted --target-label native_opt_in_cylinder --output reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stdout.json`:
  exit `0`, report `status: clean_frame_blocker_audit_recorded`. This post-run audit compares
  the original opt-in cylinder against the native all-box and cylinder-reverted clean controls
  inside the same `361`-frame report. It records that both controls pass while the original
  opt-in cylinder remains `not_settled`, with matching final support-contact primitive suffixes
  (`12`, `15`, `15`, and `26`) and a final-speed delta of about `+0.0181910 m/s` from each
  clean control to the blocked target. It also records the same model deltas already visible in
  the report: mass `+1126.625` and COM about `[-0.0427847, 0.0171919, 0.2960243]`. This is
  clean-frame blocker accounting only, not root-cause proof, sustained-settle evidence, a
  validated fix, or collision-quality validation.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame363_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `363` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame364_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `364` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame365_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `365` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame375_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `375` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame385_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `385` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame390_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `390` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame420_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `420` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame450_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `450` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame480_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `480` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_frame600_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun keeps the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but changes drop/settle to
  `600` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_long_window_probe.yaml --source-dir /cpfs/user/zhuzihou/dev/newton --run-com-blend-refinement --sample-every-steps 480 --tail-steps 960 --output reports/generated/bed_native_opt_in_long_window_probe/drop_primitive6_com_blend_refinement_long_window_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`. This rerun uses the same capped bed
  first-mesh selection scope and `cylinder: 0.88` opt-in multiplier, but extends drop/settle to
  `720` frames.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/bed_native_opt_in_compound_trace.py --config configs/experiments/bed_native_opt_in_probe.yaml --source-dir '$NEWTON_SOURCE_DIR' --run-model-build-audit --output reports/generated/bed_native_opt_in_probe/drop_primitive6_model_build_audit_2026-05-21.stdout.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_model_build_delta_audit.py --report reports/generated/bed_native_opt_in_probe/drop_primitive6_model_build_audit_2026-05-21.stdout.json --output reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stdout.json`:
  exit `0`, report `status: model_build_delta_audit_recorded`. This post-run audit reads the
  existing pre-solver model-build audit and records the primitive-6 target shape-scale rows beside
  the target/rest/full mass, COM, and inertia deltas. It is model-build accounting only, not
  root-cause proof, a Newton mapping bug proof, a validated fix, scoring evidence, or
  collision-quality validation.
- `python -m py_compile scripts/diagnostics/bed_native_opt_in_compound_trace.py`: exit `0`.
- `python -m py_compile scripts/diagnostics/bed_native_opt_in_clean_frame_blocker_audit.py`:
  exit `0`.
- `python -m py_compile scripts/diagnostics/bed_native_opt_in_model_build_delta_audit.py`:
  exit `0`.
- `python -m pytest tests/test_cpd_like_config.py::test_bed_native_opt_in_frame_sweep_configs_keep_default_selection_scope -q`:
  exit `0`, `1 passed`.
- `python -m pytest tests/test_bootstrap_command_surface.py::test_clean_frame_blocker_audit_compares_target_to_clean_controls tests/test_bootstrap_command_surface.py::test_clean_frame_blocker_audit_main_writes_json -q`:
  exit `0`, `2 passed`.
- `python -m pytest tests/test_bootstrap_command_surface.py::test_model_build_delta_audit_records_target_shape_and_delta_context tests/test_bootstrap_command_surface.py::test_model_build_delta_audit_main_writes_json -q`:
  exit `0`, `2 passed`.
- `python -m json.tool reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stdout.json >/dev/null`:
  exit `0`.
- `python -m json.tool reports/generated/bed_native_opt_in_frame_transition_audit/native_reverted_frame361_362_audit_2026-05-21.stdout.json >/dev/null`:
  exit `0`.
- `python -m json.tool reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stdout.json >/dev/null`:
  exit `0`.
- `python -m json.tool reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stdout.json >/dev/null`:
  exit `0`.
- `python -m json.tool reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stdout.json >/dev/null && python -m json.tool reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stdout.json >/dev/null`:
  exit `0`.
- `git check-ignore -v reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stderr reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stderr reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stderr reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stderr`:
  exit `0`; the reports and runtime logs are ignored by `.gitignore`.
- `git check-ignore -v reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stdout.json reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.console.stdout reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stderr`:
  exit `0`; the report and runtime logs are ignored by `.gitignore`.
- `git check-ignore -v reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stdout.json reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.console.stdout reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stderr`:
  exit `0`; the report and runtime logs are ignored by `.gitignore`.
- `git check-ignore -v reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stderr reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stderr reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stderr reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stderr reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stderr reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stderr reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stderr reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stdout.json reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stderr`:
  exit `0`; the reports and runtime logs are ignored by `.gitignore`.
- `python -m pytest tests/test_bootstrap_command_surface.py::test_tail_linear_speed_summary_filters_tail_window tests/test_bootstrap_command_surface.py::test_compound_trace_main_json_safes_non_finite_report_values -q`:
  exit `0`, `2 passed`.
- `python -m pytest tests/test_bootstrap_command_surface.py::test_bed_native_opt_in_compound_trace_script_has_bounded_help -q`:
  exit `0`, `1 passed`.
- `python -m pytest tests/test_cpd_like_config.py tests/test_real_usd_native_comparison.py tests/test_cli.py -k "native_opt_in or real_usd_native" -q`:
  exit `0`, `29 passed, 121 deselected`.
- `python scripts/validate_docs.py`: exit `0`, `docs validation passed`.
- `python scripts/validate_site_claims.py`: exit `0`, `site claim validation passed`.
- `git diff --check`: exit `0`.

Observed current-config result:

- legacy lane: `32` boxes, fully mapped, contact `smoke_passed`, drop/settle `smoke_passed`,
  sphere-rain `smoke_passed`;
- default native lane: `32` boxes, fully mapped, contact `smoke_passed`, drop/settle
  `smoke_passed`, sphere-rain `smoke_passed`;
- opt-in native lane: `31` boxes plus `1` cylinder, fully mapped;
- opt-in contact canaries: representative `box` and `cylinder` canaries both `smoke_passed`,
  contact count `1` each;
- opt-in drop/settle: `runtime_failure` with `not_settled`; completed `2880` steps, final speed
  about `0.0823040 m/s`, final contact count `4`, no floor-breach label;
- opt-in sphere-rain: `smoke_passed`, contact-density proxy `0.1111111111111111`.

Exploratory checks:

- A local counterfactual drop-attribution diagnostic compared the default native all-box package,
  the original opt-in package, and a reverted opt-in package where only primitive index `6` /
  `source_faces: [32, 33, 34, 35, 36, 37, 38, 39]` was changed from the selected opt-in cylinder
  back to the native box geometry. The other `31` primitives had zero non-ID diffs. Under the same
  clean Newton environment and drop/settle options, the default native package passed with final
  speed about `0.0404565 m/s`, the original opt-in package failed with `not_settled` and final
  speed about `0.0823040 m/s`, and the reverted package passed with final speed about
  `0.0404565 m/s`.
- A follow-up center/shape 2x2 diagnostic kept the same primitive index and source faces and ran
  the two off-diagonal packages. `box_at_cylinder_center` passed drop/settle with final speed
  about `0.0464995 m/s`; `cylinder_at_box_center` still failed with `not_settled` and final speed
  about `0.0786721 m/s`. A companion geometry summary records the package anchor as unchanged
  across the variants, so the off-diagonal result is not explained by an anchor recomputation.
- A target-only one-primitive diagnostic then kept only primitive index `6` in the package. Under
  the same drop/settle settings, `native_box_target_only`,
  `box_at_cylinder_center_target_only`, `opt_cylinder_target_only`, and
  `cylinder_at_box_center_target_only` all passed with final speed `0.0 m/s`. This records that
  the selected cylinder shape alone does not reproduce the full 32-primitive package
  `not_settled` label under the target-only construction. The target-only packages recompute
  their own one-primitive anchor, so the off-diagonal center labels are anchor-normalization
  controls rather than center-causality evidence.
- A nearest-neighbor local-context diagnostic used the six closest AABB-gap neighbors
  `[3, 4, 24, 28, 5, 29]` around primitive index `6`. The local neighbors alone passed; the local
  shell plus native box passed with final speed about `0.0004933 m/s`; and the local shell plus
  opt-in cylinder also passed with final speed about `0.0007994 m/s`. This records that the
  nearest local shell does not reproduce the full-package blocker.
- The same local-context report includes a `full_without_target` control that removed primitive
  index `6` from the full opt-in package. It still failed with `not_settled` and final speed about
  `0.5413420 m/s`, so removal/subset controls are not clean attribution evidence by themselves.
- An anchor-preserved local subset then added nearest local neighbors plus full-package bounds
  keepers `[14, 16, 17, 22]`, preserving the full package anchor exactly across variants. In that
  subset, the native-box variant, `cylinder_at_box_center`, and `cylinder_at_cylinder_center` all
  failed with `no_descent` and `not_settled`, with final speeds about `4.30-4.35 m/s`. Because the
  paired box control also failed, this subset is recorded as a diagnostic-control failure, not as
  cylinder attribution evidence.
- A worktree full-compound body/contact trace script then reran the five fixed 32-primitive
  variants under the same drop/settle settings while recording Newton body mass, COM, inertia,
  body pose/velocity, support height, and contact details for regular samples plus the final
  `1.0` seconds. The native all-box control and cylinder-reverted package both passed with final
  speed about `0.0404565 m/s`, body mass `580154.0625`, and COM about
  `[-10.8548, 6.7308, 51.7157]`. The opt-in cylinder package failed with final speed about
  `0.0823040 m/s`, body mass `581280.6875`, and COM about `[-10.8976, 6.7480, 52.0118]`.
  `box_at_cylinder_center` passed with final speed about `0.0464995 m/s`, body mass
  `580154.0625`, and COM about `[-10.8515, 6.7355, 51.7150]`; `cylinder_at_box_center` failed
  with final speed about `0.0786721 m/s`, body mass `581280.6875`, and COM about
  `[-10.9013, 6.7427, 52.0126]`. The final contact labels for the passing and failing
  full-compound variants were the same support primitives (`12`, `15`, `15`, and `26`) against
  the ground plane, so this trace records a body-state/inertia and residual-velocity difference
  under a similar final support-contact set rather than a new target-only contact reproducer.
- The same worktree script then ran an explicit inertial-array counterfactual. The target package
  kept the opt-in cylinder geometry, but after Newton model finalization and before creating the
  XPBD solver, the script overwrote the model `body_mass`, `body_inv_mass`, `body_com`,
  `body_inertia`, and `body_inv_inertia` arrays with the native all-box control arrays. The
  source and target package anchors both recorded
  `[-42.68740478585236, 18.933394760109707, -115.0197216258088]`, so the direct array copy is
  recorded without an anchor-frame mismatch in this run. The override changed the opt-in cylinder
  package from body mass `581280.6875`, COM about `[-10.8976, 6.7480, 52.0118]`, and inertia
  tensor row 0 `[3121799680.0, -3759280.75, 721261952.0]` to body mass `580154.0625`, COM about
  `[-10.8548, 6.7308, 51.7157]`, and inertia tensor row 0
  `[3095483392.0, -3984028.75, 717470912.0]`. With cylinder geometry still present and those
  native all-box inertial arrays applied, drop/settle passed with final speed about
  `0.0404565 m/s`, final contact count `4`, and the same final support-contact labels
  (`12`, `15`, `15`, and `26`) against the ground plane.
- A COM-only field ablation then kept the opt-in cylinder geometry, mass, inverse mass, inertia,
  and inverse inertia unchanged, but copied only the native all-box `body_com` before solver
  creation. The override changed COM from about `[-10.8976, 6.7480, 52.0118]` to about
  `[-10.8548, 6.7308, 51.7157]`, while body mass stayed `581280.6875` and inertia tensor row 0
  stayed `[3121799680.0, -3759280.75, 721261952.0]`. Under the same fixed full-compound
  drop/settle gate, this COM-only override passed with final speed about `0.0425127 m/s`, final
  contact count `4`, and the same final support-contact labels (`12`, `15`, `15`, and `26`)
  against the ground plane.
- An inertial-component ablation then kept the opt-in cylinder geometry and opt-in `body_com`
  while copying selected native all-box inertial component groups before solver creation. Under
  the 360-frame gate, copying `body_mass`/`body_inv_mass` only remained `not_settled` with final
  speed about `0.0962726 m/s`; copying `body_inertia`/`body_inv_inertia` only passed with final
  speed about `0.0427094 m/s`; copying mass plus inertia remained `not_settled` with final speed
  about `0.0618353 m/s`. Under the clean-control 361-frame window, mass-only remained
  `not_settled` with final speed about `0.0610217 m/s`, while inertia-only passed at about
  `0.0343839 m/s` and mass+inertia passed at about `0.0381616 m/s`. This is component
  sensitivity accounting only, not a physical inertial repair or root-cause proof.
- A COM-axis subset ablation then kept the opt-in cylinder geometry, mass, inverse mass, inertia,
  and inverse inertia unchanged while copying selected axes from the native all-box `body_com`.
  The original opt-in cylinder failed again with final speed about `0.0823040 m/s`, and the
  native all-box control plus cylinder-reverted package passed again with final speed about
  `0.0404565 m/s`. Single-axis `x`, `y`, and `z` overrides all remained `not_settled`, with
  final speeds about `0.0842403`, `0.0935629`, and `0.0524167 m/s`. Pairwise `xy` and `yz`
  overrides also remained `not_settled`, with final speeds about `0.0712072` and
  `0.0586259 m/s`. The pairwise `xz` override passed with final speed about
  `0.0422074 m/s`. This records that the full COM-only pass is not reproduced by any single COM
  axis in this run, while the `x+z` subset clears the recorded label under the same fixed
  full-compound gate. The original opt-in and all COM-axis subset variants (`x`, `y`, `z`, `xy`,
  `xz`, and `yz`) recorded final contact count `4` with the same support-contact labels (`12`,
  `15`, `15`, and `26`) against the ground plane, so this subset result is recorded as a
  residual-velocity/body-COM sensitivity difference under the same final support-contact labels.
- A COM-blend ablation then kept the opt-in cylinder geometry, mass, inverse mass, inertia, and
  inverse inertia unchanged while interpolating the opt-in `body_com` toward the native all-box
  `body_com` at fixed fractions `0.0`, `0.25`, `0.5`, `0.75`, and `1.0`, for both full `xyz`
  and `xz` axes. The `0.0` endpoint reproduced the original opt-in `not_settled` label with final
  speed about `0.0823040 m/s`. The `0.25`, `0.5`, and `0.75` full-`xyz` blends remained
  `not_settled`, with final speeds about `0.0893670`, `0.0795233`, and `0.0765784 m/s`. The
  `0.25`, `0.5`, and `0.75` `xz` blends also remained `not_settled`, with final speeds about
  `0.0798824`, `0.0802833`, and `0.0735701 m/s`. The `1.0` endpoints reproduced the previous
  full-COM and `xz`-COM passes, with final speeds about `0.0425127` and `0.0422074 m/s`.
  This records that the intermediate fixed COM blends did not clear the label in this run; only
  the full native-COM endpoint did.
- A near-endpoint COM-blend refinement then kept the same opt-in cylinder geometry, mass, inverse
  mass, inertia, and inverse inertia unchanged while testing fixed fractions `0.75`, `0.875`,
  `0.9375`, `0.96875`, `0.984375`, and `1.0`, again for both full `xyz` and `xz` axes. For full
  `xyz`, `0.75` remained `not_settled` with final speed about `0.0765784 m/s`, while `0.875`,
  `0.9375`, `0.96875`, `0.984375`, and `1.0` passed with final speeds about `0.0362300`,
  `0.0437060`, `0.0370051`, `0.0430691`, and `0.0425127 m/s`. For `xz`, `0.75` and `0.875`
  remained `not_settled`, with final speeds about `0.0735701` and `0.0519546 m/s`, while
  `0.9375`, `0.96875`, `0.984375`, and `1.0` passed with final speeds about `0.0451888`,
  `0.0461983`, `0.0472314`, and `0.0422074 m/s`. This records a bounded near-endpoint
  sensitivity pattern for this one drop/settle gate, not a COM threshold proof.
- A follow-up real Newton rerun of the same COM-blend refinement added tail-window speed
  telemetry. The report used a `1.0` second tail window with `481` sampled steps and
  `step_dt_seconds: 0.0020833333333333333`. It shows that the existing pass/fail labels remain
  final-speed gated rather than sustained-tail gated: the native all-box control passed with final
  speed about `0.0404565 m/s`, but `475/481` tail samples were above the `0.05 m/s` threshold and
  only the final `6` samples (`0.0125 s`) were at or below it. The full-`xyz` `0.875` COM blend
  passed with final speed about `0.0362300 m/s`, but `473/481` tail samples were above threshold
  and only the final `8` samples (`0.0166667 s`) were at or below it. The `xz` `0.9375` COM
  blend passed with final speed about `0.0451888 m/s`, but `479/481` tail samples were above
  threshold and only the final `2` samples (`0.0041667 s`) were at or below it. The failed
  original opt-in cylinder, full-`xyz` `0.75`, `xz` `0.75`, and `xz` `0.875` variants all had
  `481/481` tail samples above threshold and zero final below-threshold samples. This is
  descriptive late-window velocity telemetry only; it is not a sustained-settle criterion.
- A bounded real Newton frame-window sensitivity sweep then reran the same COM-blend refinement at
  `361`, `362`, `363`, `364`, `365`, `375`, `385`, `390`, `420`, `450`, `480`, `600`, and `720`
  frames, preserving the same capped bed first-mesh scope, `256` source-face cap, primitive
  subsets, and `cylinder: 0.88` opt-in multiplier while changing only `drop_settle.frames`. The
  `361`-frame rerun keeps the native all-box and cylinder-reverted controls clean under the
  existing final-speed gate, both ending at about `0.0449881 m/s` with `947/961` two-second tail
  samples above the `0.05 m/s` cutoff; the original opt-in cylinder still fails at about
  `0.0631791 m/s`. The `362`-frame rerun is the first swept frame where the native all-box and
  cylinder-reverted controls fail `not_settled`, both ending at about `0.0639728 m/s` with
  `945/961` tail samples above that cutoff. The same controls fail at about `0.0957800 m/s` at
  `363` frames, `0.1194928 m/s` at `364`, `0.1464434 m/s` at `365`, `0.3574153 m/s` at `375`,
  `0.5688495 m/s` at `385`, `0.6757393 m/s` at `390`, `0.5461583 m/s` at `420`,
  `0.4750371 m/s` at `450`, `0.1789031 m/s` at `480`, `0.1768281 m/s` at `600`, and
  `0.2896395 m/s` at `720`. These tail summaries are not a sustained-settle criterion or new
  gate. The sweep now brackets the observed native/reverted-control final-speed task-gate flip
  between the `361` clean-control context and the `362` failure context under these settings.
  Dirty-control rows from `362` onward are rejected as COM-blend fix, sustained-settle,
  long-window stability, or stronger validation evidence; the clean-control `361` row remains
  one-config final-speed sensitivity accounting only.

  | Frames | Control lanes | Original opt-in cylinder | Selected near-endpoint blends | Claim use |
  | --- | --- | --- | --- | --- |
  | `360` | native/reverted controls clear the recorded final-speed gate; tail telemetry is not sustained-settle evidence | `not_settled`, final speed about `0.0823040 m/s` | full `xyz` clears the recorded label at `0.875+`; `xz` clears it at `0.9375+` | near-endpoint sensitivity accounting only |
  | `361` | native/reverted controls clear the recorded final-speed gate, final speed about `0.0449881 m/s` | `not_settled`, final speed about `0.0631791 m/s` | full `xyz` clears at `0.875+`; `xz` clears at `0.75+` under the final-speed gate | clean-control side of the `361`/`362` bracket; not sustained-settle evidence |
  | `362` | native/reverted controls fail `not_settled`, final speed about `0.0639728 m/s` | clears the recorded final-speed gate, final speed about `0.0373673 m/s` | mixed pass/fail labels across near-endpoint blends | dirty-control bracket side only; rejected as strengthening evidence |
  | `363` | native/reverted controls fail `not_settled`, final speed about `0.0957800 m/s` | clears the recorded final-speed gate, final speed about `0.0353086 m/s` | mixed labels; most near-endpoint full `xyz`/`xz` variants fail | dirty-control bracket side only; rejected as strengthening evidence |
  | `364` | native/reverted controls fail `not_settled`, final speed about `0.1194928 m/s` | fails, final speed about `0.0548617 m/s` | selected full `xyz`/`xz` refinement variants fail | dirty-control bracket side only; rejected as strengthening evidence |
  | `365` | native/reverted controls fail `not_settled`, final speed about `0.1464434 m/s` | fails, final speed about `0.0864127 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `375` | native/reverted controls fail `not_settled`, final speed about `0.3574153 m/s` | fails, final speed about `0.3122411 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `385` | native/reverted controls fail `not_settled`, final speed about `0.5688495 m/s` | fails, final speed about `0.5291869 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `390` | native/reverted controls fail `not_settled`, final speed about `0.6757393 m/s` | fails, final speed about `0.6291180 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `420` | native/reverted controls fail `not_settled`, final speed about `0.5461583 m/s` | fails, final speed about `0.7064976 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `450` | native/reverted controls fail `not_settled`, final speed about `0.4750371 m/s` | fails, final speed about `0.5356924 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `480` | native/reverted controls fail `not_settled`, final speed about `0.1789031 m/s` | fails, final speed about `0.1163292 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `600` | native/reverted controls fail `not_settled`, final speed about `0.1768281 m/s` | fails, final speed about `0.1585591 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
  | `720` | native/reverted controls fail `not_settled`, final speed about `0.2896395 m/s` | fails, final speed about `0.2691149 m/s` | selected full `xyz`/`xz` refinement variants fail | gate-flip bracketing only; rejected as strengthening evidence |
- A pre-solver model-build audit then built full, target-only, and rest-without-target Newton
  models for the native all-box and opt-in cylinder packages under their full-package anchors.
  The native and opt-in package anchors matched. The full opt-in-minus-native body delta was mass
  `+1126.625`, COM about `[-0.0427847, 0.0171919, 0.2960243]`, and inertia row-0 about
  `[26316288.0, 224748.0, 3791040.0]`. The target-only opt-in-minus-native delta under the
  full-package anchor was mass about `+1126.5820`, COM about
  `[0.2216988, 0.3152409, -0.0516510]`, and inertia row-0 about
  `[2962.6045, -683.8531, 436.1219]`. The rest-without-target opt-in-minus-native delta was
  exactly zero for mass, COM, and inertia row-0 in this audit, recording that the pre-solver
  model-build accounting shows zero rest-without-target delta while the full-package and
  target-only primitive-6 mass/COM/inertia deltas remain nonzero under matching anchors.
- A post-run model-build delta audit then read that existing pre-solver report and linked the
  same target/rest/full deltas to the primitive-6 target shape-scale rows. The native target row
  records shape scale `[0.2130423, 2.3121915, 2.1920862]`, while the opt-in target row records
  `[2.7009380, 0.2130423, 0.0]`, for an opt-in-minus-native shape-scale delta of about
  `[2.4878956, -2.0991491, -2.1920862]`. This is accounting over the recorded model-build JSON
  only; it does not prove a Newton mapping bug, root cause, validated fix, scoring evidence, or
  collision-quality validation.
- The same target cluster audit records `8` source faces, `9` unique points, AABB aspect ratios
  about `[1.0, 0.8305, 0.1641]`, native box weighted volume `8.6384801`, cylinder weighted volume
  `9.7650635`, and a configured `cylinder: 0.88` multiplier. A counterfactual tie multiplier for
  the cylinder to beat the box in this cluster is about `0.8846312`, so the configured multiplier
  flips selection by a small effective-score margin of about `0.0452242`; this is not a calibrated
  or recommended multiplier.
- A `128`-face bed opt-in config was rejected as evidence because the legacy/default native
  all-box lanes also failed task gates.
- The `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720`-frame
  drop/settle windows refine the native/reverted-control final-speed task-gate bracket to
  `361` clean versus `362` failing. The `362` and later dirty-control rows are rejected as
  strengthening evidence because the native all-box and cylinder-reverted diagnostic controls
  also became `not_settled` under those recorded runs.
- An `iterations: 4` drop/settle sensitivity run was rejected as a fix: legacy/default native
  all-box lanes still passed, but the opt-in lane remained `not_settled` and final speed increased
  to about `0.1000315 m/s`.
- A `substeps: 16` drop/settle sensitivity run was rejected as a fix: legacy/default native
  all-box lanes also became `not_settled`, and the opt-in lane remained `not_settled` with final
  speed about `0.1804757 m/s`.
- The earlier temporary two-role `cylinder: 0.5` exploratory run remains a stronger failed-bed
  stress case: `25` boxes plus `7` cylinders, contact passed, but drop/settle failed with
  `not_settled` and `floor_breach`, and sphere-rain failed with `no_contact_observed` and
  `insufficient_contact_density`.

## Artifacts

- Config: `configs/experiments/bed_native_opt_in_probe.yaml`
- Frame-window sensitivity configs:
  `configs/experiments/bed_native_opt_in_frame361_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame362_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame363_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame364_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame365_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame375_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame385_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame390_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame420_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame450_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame480_probe.yaml`,
  `configs/experiments/bed_native_opt_in_frame600_probe.yaml`, and
  `configs/experiments/bed_native_opt_in_long_window_probe.yaml`
- Fitting report: `reports/generated/bed_native_opt_in_probe/fitting_2026-05-21.stdout.json`
  (ignored; not committed).
- Current task report: `reports/generated/bed_native_opt_in_probe/task_2026-05-21.stdout.json`
  (ignored; not committed).
- Current-worktree task rerun after the COM-axis diagnostic:
  `reports/generated/bed_native_opt_in_probe/task_rerun_after_com_axis_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Drop sensitivity reports:
  `reports/generated/bed_native_opt_in_probe/drop_iterations4_2026-05-21.stdout.json` and
  `reports/generated/bed_native_opt_in_probe/drop_substeps16_2026-05-21.stdout.json` (ignored;
  not committed).
- Cylinder-revert drop-attribution report:
  `reports/generated/bed_native_opt_in_probe/drop_cylinder_revert_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 center/shape variant reports:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_center_shape_variants_2026-05-21.stdout.json`
  and
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_center_shape_variants_geometry_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 target-only report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_target_only_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 local context reports:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_local_context_2026-05-21.stdout.json`
  and
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_anchor_preserved_subset_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` files.
- Primitive-6 full-compound trace script and report:
  `scripts/diagnostics/bed_native_opt_in_compound_trace.py` and
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_compound_trace_2026-05-21.stdout.json`
  (report ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 inertial counterfactual report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_inertia_counterfactual_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 COM-only inertial-field ablation report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_field_ablation_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 inertial-component ablation reports:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_component_ablation_2026-05-21.stdout.json`
  and
  `reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_inertial_component_ablation_frame361_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` files.
- Primitive-6 COM-axis subset ablation report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_com_axis_subset_ablation_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 COM-blend ablation report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_ablation_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 COM-blend refinement report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 COM-blend refinement tail-summary rerun:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_tail_suffix_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 COM-blend refinement frame-window sensitivity reruns:
  `reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stdout.json`,
  `reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stdout.json`, and
  `reports/generated/bed_native_opt_in_long_window_probe/drop_primitive6_com_blend_refinement_long_window_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 `361`/`362` frame-transition audit:
  `scripts/diagnostics/bed_native_opt_in_frame_transition_audit.py` and
  `reports/generated/bed_native_opt_in_frame_transition_audit/native_reverted_frame361_362_audit_2026-05-21.stdout.json`
  (report ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 `361` clean-frame blocker audit:
  `scripts/diagnostics/bed_native_opt_in_clean_frame_blocker_audit.py` and
  `reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stdout.json`
  (report ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 pre-solver model-build audit report:
  `reports/generated/bed_native_opt_in_probe/drop_primitive6_model_build_audit_2026-05-21.stdout.json`
  (ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Primitive-6 post-run model-build delta audit:
  `scripts/diagnostics/bed_native_opt_in_model_build_delta_audit.py` and
  `reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stdout.json`
  (report ignored; not committed). Runtime logs are in the matching `.stderr` file.
- Exploratory preserved reports under `reports/generated/bed_native_opt_in_probe/` are ignored and
  not committed.

## Claim Impact

- Records only a partial opt-in diagnostic path: the capped bed first-mesh package with one
  selected Newton-native `cylinder` maps, passes representative contact canaries, and passes
  sphere-rain.
- Records that the same opt-in package does not pass the full contact-gated task-smoke suite
  because drop/settle fails with `not_settled`.
- Records a local counterfactual attribution check: reverting the single selected cylinder package
  delta at source faces `[32..39]` back to the native box clears the recorded drop/settle blocker
  under this config and Newton environment.
- Records a narrower center/shape separation check: moving the native box to the cylinder center
  still passes, while moving the cylinder to the native box center still fails. This supports only
  local task-smoke attribution to the selected cylinder shape/dimensions rather than the center
  shift for this recorded package and solver setting.
- Records a target-only control: the isolated primitive-6 box and cylinder variants all pass, so
  the full-package `not_settled` label is not reproduced by the standalone selected cylinder under
  one-primitive anchor recomputation. This points back to full-compound context, aggregate
  body/contact/inertia behavior, or final-speed gate interaction as still-open diagnostic factors.
- Records that the nearest-neighbor local shell does not reproduce the full-package blocker for
  either target variant.
- Records that a full-anchor-preserved local subset is not valid cylinder attribution evidence,
  because the paired native-box control also fails.
- Records a full-compound body/contact trace for the fixed native box, opt-in cylinder, reverted
  box, and center/shape variants. The trace records that the cylinder variants have higher
  full-body mass, shifted COM/inertia, and residual final linear speed above the configured
  settle threshold while the final support-contact labels match the passing box variants.
- Records an inertial-array counterfactual: with the opt-in cylinder geometry retained, copying
  the native all-box Newton body mass/COM/inertia arrays into the opt-in cylinder model before
  solver creation clears the drop/settle `not_settled` label for this run.
- Records a COM-only field ablation: with the opt-in cylinder geometry and mass/inertia retained,
  copying only the native all-box Newton `body_com` clears the drop/settle `not_settled` label for
  this run.
- Records an inertial-component ablation: with the opt-in cylinder geometry and COM retained,
  native all-box mass-only does not clear the recorded final-speed gate at 360 or 361 frames,
  while native all-box inertia-only clears it at both windows and mass+inertia clears it only in
  the clean-control 361-frame window.
- Records a COM-axis subset ablation: with the opt-in cylinder geometry and mass/inertia retained,
  copying only `body_com` axes `x`, `y`, `z`, `xy`, or `yz` does not clear the recorded
  `not_settled` label, while copying the `x+z` subset does clear it in this run.
- Records a COM-blend ablation: with the opt-in cylinder geometry and mass/inertia retained,
  partial fixed blends at `0.25`, `0.5`, and `0.75` toward native all-box `body_com` do not clear
  the recorded label for either full `xyz` or `xz` axes, while the `1.0` endpoint clears it in
  this run.
- Records a COM-blend refinement: with the same field-only override scope, full `xyz` clears the
  recorded `360`-frame final-speed gate label at `0.875` and above in this run, while `xz` still
  fails at `0.875` and clears the label at `0.9375` and above. This is near-endpoint sensitivity
  accounting only.
- Records a COM-blend refinement tail-summary rerun: `tail_linear_speed_summary` is descriptive
  late-window linear-speed telemetry for this rerun. The drop/settle pass/fail label remains the
  existing final-speed gate and failure-label logic; this field is not a sustained-settle
  criterion or proof.
- Records a `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720`-frame
  window sensitivity sweep: the same COM-blend refinement variants and all-box controls are run
  under longer drop/settle windows. The `361` row keeps the native all-box and cylinder-reverted
  controls clean under the existing final-speed gate; the `362` row is the first swept row where
  those controls fail, refining the control-lane bracket to `361` clean versus `362` failing.
  Dirty-control rows are rejected as COM-blend fix, sustained-settle, long-window stability, or
  stronger validation evidence.
- Records a `361`/`362` frame-transition audit for the native all-box and cylinder-reverted
  controls: Newton model arrays and final support-contact labels match across the adjacent
  reports, while `362` adds `8` substeps and increases final linear speed by about
  `0.0189847 m/s`. The audit aligns final trace rows by `steps_from_final`, not raw `step`.
- Records a `361` clean-frame blocker audit: inside the same clean-control report, the native
  all-box and cylinder-reverted controls pass while the original opt-in cylinder remains
  `not_settled`. Final support-contact primitive suffixes match (`12`, `15`, `15`, and `26`),
  while the blocked target has final speed about `+0.0181910 m/s` above each clean control, body
  mass `+1126.625`, and COM delta about `[-0.0427847, 0.0171919, 0.2960243]`.
- Records a pre-solver model-build audit: under matching full-package anchors, the full-package
  and target-only Newton model mass/COM/inertia deltas are nonzero for primitive index `6`, while
  the rest-without-target delta is zero in this audit.
- Records a post-run model-build delta audit: the existing pre-solver target/rest/full delta rows
  are linked to primitive-6 target shape-scale rows, with the rest-without-target delta still zero
  and the target/full deltas still nonzero.
- Records that the opt-in multiplier flips this cluster by a small surrogate score margin; this is
  diagnostic accounting, not multiplier calibration.
- Records that increasing drop/settle iterations or substeps did not clear the blocker under the
  current settings.
- Does not prove the cylinder caused the failure in a general sense, does not prove cylinders are
  worse than boxes, and does not implement or justify an automatic repair/revert policy. The
  target-only diagnostic also does not reproduce the exact full-package body origin, compound
  inertia, contact manifold, or support-height semantics.
- The full-compound trace narrows the next debugging target to body-state/inertia/residual-velocity
  behavior under a similar final support-contact set; it is not a root-cause proof and does not
  identify a validated automatic fix.
- The inertial counterfactual is a one-config sensitivity control, not a physically validated
  collision package. It does not prove a general root cause, does not validate an automatic
  inertial repair, and does not justify changing primitive scoring or default asset configs.
- The COM-only field ablation is also a one-config sensitivity control. It narrows the recorded
  blocker toward aggregate body COM behavior in this Newton drop/settle setup, but it is not
  causal proof or a validated package fix.
- The COM-axis subset ablation is also a one-config field-level sensitivity control. It narrows
  the recorded blocker toward coupled `body_com` axes under this one Newton drop/settle setup, but
  it is not causal proof, a validated package fix, or evidence for changing scoring/default
  configs.
- The COM-blend ablation is also a one-config field-level sensitivity control. It records a
  coarse one-config pass/fail sensitivity pattern in this run, but it is not causal proof, a
  validated package fix, or evidence for changing scoring/default configs.
- The COM-blend refinement is also a one-config field-level sensitivity control. It records a
  narrower near-endpoint pattern in this run, but it is not a COM threshold proof, causal proof,
  validated package fix, or evidence for changing scoring/default configs.
- The COM-blend refinement tail summary is also one-config telemetry. It does not prove sustained
  settling over the final second, add a new drop/settle gate, prove convergence, or strengthen
  validation beyond the recorded final-speed gate.
- The `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720`-frame window
  sweep is also one-config sensitivity accounting. It does not prove sustained settling,
  long-window stability, a validated COM-blend fix, root cause, scoring calibration,
  default-policy evidence, or collision-quality validation. The `361` row is clean-control
  final-speed bracket context only; the `362` and later dirty-control rows are rejected evidence
  for strengthening the COM-blend refinement claim.
- The `361`/`362` frame-transition audit is adjacent-run diagnostic accounting only. It does not
  prove sustained settling, root cause, a validated fix, a COM-blend stability claim, scoring
  calibration, default-policy evidence, or collision-quality validation.
- The `361` clean-frame blocker audit is same-report diagnostic accounting only. It does not
  prove sustained settling, root cause, a validated fix, a COM-blend stability claim, scoring
  calibration, default-policy evidence, or collision-quality validation.
- The model-build audit and post-run model-build delta audit are one-config accounting
  diagnostics. They do not prove a Newton mapping bug, a physical root cause, a validated
  inertial repair, scoring evidence, default-policy behavior, or a package-quality conclusion.
- The inertial-component ablation is a component sensitivity diagnostic only. It does not prove
  root cause, a validated inertial repair, a default repair recipe, physical package validation,
  scoring evidence, or collision-quality validation.
- Does not support native primitive quality improvement, calibrated cylinder score multipliers,
  collision-quality validation, benchmark superiority, deployment readiness, safety
  certification, real-world transfer, or default asset behavior.

## Next Action

- Use the recorded full-compound trace, inertial counterfactual, COM-only field ablation,
  COM-axis subset ablation, COM-blend ablation, COM-blend refinement, COM-blend refinement
  tail-summary rerun, inertial-component ablation, the
  `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720` frame-window
  sensitivity sweep, the `361`/`362` frame-transition audit, the `361` clean-frame blocker audit,
  pre-solver model-build audit, and post-run model-build delta audit as the current reproducible
  bed blocker evidence; do not broaden bed native opt-in claims or change default support-aware
  asset configs from this evidence.
