# 2026-05-26 Phase 0 V-HACD Runtime Follow-Up

## Date

2026-05-26

## Status

Complete for the scoped V-HACD runtime follow-up.

## Changes

- Installed `vhacdx==0.0.10` in the clean Newton Python environment used for Phase 0 runs.
- Added configurable V-HACD resolution to `phase0_defaults.convex_decomposition`.
- Set the Phase 0 V-HACD smoke resolution to `20000` in
  `configs/experiments/phase0_baseline.yaml`.
- Ran V-HACD through a bounded child process so configured `timeout_seconds` is enforced and
  runtime failures become recorded baseline outcomes instead of hanging the report.

## Results

Generated report:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`

Overall recorded outcomes:

- accept: 96
- dependency gap: 0
- failure: 11
- fallback: 31
- not applicable: 70

Asset scope:

- rigid assets: 5 from `assets/manifests/phase0_assets.yaml`
- articulated assets: 1 from `assets/manifests/franka_usd_smoke_assets.yaml`

V-HACD summary:

| Asset | V-HACD result |
|---|---|
| `grscenes_box_040c0ca4_phase0` | generated, 1 hull |
| `grscenes_bowl_0cc93a88_phase0` | generated, 16 hulls |
| `grscenes_cup_08b88d9e_phase0` | generated, 16 hulls |
| `grscenes_tray_0e670d9c_phase0` | generated, 16 hulls |
| `grscenes_keyboard_b4cc03c7_phase0` | generated, 16 hulls |

Generated V-HACD packages are not all accepted by the Newton probes: the bowl/container V-HACD
package records drop/settle and stack-or-slide failures, while the cup/contact-affordance and
tray/stackable V-HACD packages record drop/settle failures.

Franka articulation smoke still passes. Link-boundary audit still records fallback/not run because
link-aware robot package generation is not implemented.

## Verification

- `python -m pytest tests/test_convex_decomposition.py tests/test_phase0_benchmark.py::test_phase0_vhacd_runtime_failure_records_failed_baseline tests/test_configs.py::test_phase0_config_defines_baselines_probes_and_required_metrics -q`:
  5 passed before the full report rerun.
- `time -p timeout 1200 env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark > reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`:
  exit 0, `real 900.18`, report status `completed_with_recorded_failures`.
- Parsed the generated JSON successfully. The report records zero dependency gaps and V-HACD
  generated packages for all five selected rigid assets with backend
  `trimesh_4.12.2_vhacdx_0.0.10`.

## Artifacts

- Config: `configs/experiments/phase0_baseline.yaml`.
- Rigid asset manifest: `assets/manifests/phase0_assets.yaml`.
- Articulation asset manifest: `assets/manifests/franka_usd_smoke_assets.yaml`.
- Generated report, ignored by git:
  `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`.

## Claim Impact

- Supports the claim that Phase 0 now has V-HACD runtime evidence in the clean Newton environment.
- Supports the claim that V-HACD failures are recorded as diagnostic outcomes instead of being
  hidden or treated as missing dependencies.
- Does not support complete V-HACD probe success across the selected assets because bowl, cup, and
  tray record V-HACD probe failures.
- Does not support link-aware robot package generation, whole-robot Franka collider quality, broad
  benchmark superiority, deployment readiness, real-world transfer, or safety certification.

## Next Action

Keep the next major objective focused on link-aware robot package generation and link-boundary
probes. Treat V-HACD probe-failure triage as a secondary baseline-stability task.
