# 2026-05-25 Phase 0 Stack CoACD Articulation Follow-Up

## Date

2026-05-25

## Status

Complete for the scoped follow-up run. V-HACD dependency status is superseded by the
2026-05-26 runtime follow-up.

## Changes

- Added a dedicated Newton stack-or-slide task smoke runner and Phase 0 report integration.
- Added convex-mesh runtime mapping support so executable convex-decomposition hull packages can
  enter contact, drop/settle, stack-or-slide, and sphere-rain probes.
- Added a CoACD/V-HACD convex-decomposition baseline path. CoACD ran in the clean Newton
  environment; V-HACD is now recorded separately as `vhacd_if_available` and currently reports a
  dependency gap because `vhacdx` was not installed for this 2026-05-25 run.
- Added a Franka USD articulation smoke case with joint tree import, short gravity hold, and simple
  kinematic trajectory checks.
- Preserved the link-boundary claim boundary: link-aware robot package generation is not
  implemented in this Phase 0 runner, so link-boundary audit remains an explicit fallback.

## Results

Generated report:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-25.json`

Overall recorded outcomes:

- accept: 75
- dependency gap: 25
- failure: 7
- fallback: 31
- not applicable: 70

Asset scope:

- rigid assets: 5 from `assets/manifests/phase0_assets.yaml`
- articulated assets: 1 from `assets/manifests/franka_usd_smoke_assets.yaml`

Baseline and probe summary:

| Scope | Result |
|---|---|
| `bounding_primitive` | Generated for all five rigid assets and entered Newton probes. |
| `coacd_or_vhacd_if_available` | CoACD generated convex-mesh hull packages for all five rigid assets; hull counts were 1, 9, 5, 1, and 1. |
| `vhacd_if_available` | Recorded dependency gap for all five rigid assets in this historical run: `vhacdx` was not installed. |
| `cpd_style_primitive_candidate_if_available` | Generated CPD-style first-mesh candidates for all five rigid assets. |
| `single_convex_hull` | Kept as a simple fallback lane; executable convex-decomposition owns generated convex hull probes. |
| `stack_or_slide` | Ran as a Newton task smoke where the baseline package entered contact canary successfully. |
| Franka articulation smoke | Passed joint import, short gravity hold, and kinematic trajectory smoke. |
| Franka link-boundary audit | Fallback/not run because link-aware robot package generation is not implemented. |

Recorded failures are diagnostic outcomes, not hidden exclusions:

- bowl: CoACD drop/settle failed; CoACD stack-or-slide failed; CPD-style drop/settle failed;
  CPD-style stack-or-slide failed.
- cup: CoACD drop/settle failed; CPD-style drop/settle failed; CPD-style stack-or-slide failed.

## Verification

- `python -m pytest tests/test_cli.py::test_cli_run_phase0_benchmark_keeps_fd_stdout_json_only tests/test_cli.py::test_cli_run_phase0_benchmark_emits_json_for_partial_record tests/test_cli.py::test_cli_run_phase0_benchmark_returns_zero_for_recorded_failures tests/test_phase0_benchmark.py::test_phase0_report_records_articulated_robot_smoke_case tests/test_configs.py::test_phase0_config_defines_baselines_probes_and_required_metrics -q`:
  5 passed.
- `env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark > reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-25.json`:
  exit 0, report status `completed_with_recorded_failures`.
- Parsed generated JSON successfully after the CLI stdout redirection fix; native CoACD/Warp logs
  are routed to stderr instead of corrupting JSON stdout.
- Report stage is `phase0_asset_diagnostic_benchmark`; rigid package probes and Franka USD
  articulation smoke are recorded as separate case groups in the same report.

## Artifacts

- Config: `configs/experiments/phase0_baseline.yaml`.
- Rigid asset manifest: `assets/manifests/phase0_assets.yaml`.
- Articulation asset manifest: `assets/manifests/franka_usd_smoke_assets.yaml`.
- Generated report, ignored by git:
  `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-25.json`.

## Claim Impact

- Supports a scoped Phase 0 follow-up claim: stack-or-slide execution, CoACD executable convex
  baseline, convex-mesh Newton mapping, and Franka articulation smoke are now present in one
  reproducible report.
- Supports the claim that the diagnostic checker records accept, fallback, dependency-gap, and
  failure outcomes rather than hiding failing packages.
- Does not support V-HACD runtime comparison until `vhacdx` or another V-HACD executable is
  installed and a new report records it. This was later addressed for scoped runtime evidence in
  `docs/records/2026-05-26-phase0-vhacd-runtime-followup.md`.
- Does not support link-aware robot package generation or whole-robot Franka collider quality.
- V-HACD runtime parsing remains unverified for this 2026-05-25 report because the dependency was
  absent.
- Does not support broad benchmark superiority, full-simulation speedup, deployment readiness,
  real-world transfer, or safety certification.

## Next Action

The next major objective should be link-aware robot package generation and link-boundary probes:
build packages per robot link, forbid cross-link primitive merges, and rerun articulation smoke
with link-aware package evidence.
