# 2026-05-25 Phase 0 GRScenes Rigid Benchmark

## Date

2026-05-25

## Status

Complete for the initial scoped rigid-asset diagnostic run.
Superseded for current Phase 0 status by
[`2026-05-25-phase0-stack-coacd-articulation-followup.md`](2026-05-25-phase0-stack-coacd-articulation-followup.md),
which adds stack-or-slide execution, CoACD executable hull packages, explicit V-HACD dependency-gap
records, and Franka articulation smoke.
The command below used the then-current `configs/experiments/phase0_baseline.yaml`; that config has
since evolved, so use this record's generated report path as the historical artifact and the
follow-up record for current reruns.

## Changes

- Added `npc-compile --run-phase0-benchmark` as a Phase 0 report entry point.
- Ran the five materialized GRScenes rigid assets from `assets/manifests/phase0_assets.yaml`.
- Recorded two generated candidate lanes per asset:
  - `bounding_primitive`: one Newton-mappable box from the asset first-mesh bounds;
  - `cpd_style_primitive_candidate_if_available`: CPD-style first-mesh primitive candidates.
- Recorded explicit fallback or dependency-gap outcomes for:
  - `single_convex_hull`, because convex mesh is not currently Newton primitive-mappable in this
    runner;
  - `coacd_or_vhacd_if_available`, because no CoACD/V-HACD executable integration is configured;
  - `stack_or_slide`, because a dedicated Newton stack/slide runner is not implemented yet;
  - `precision_rejection`, where the keyboard precision negative control is routed to manual
    review instead of primitive-only acceptance.

## Results

Generated report:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_newton_2026-05-25.json`

Overall recorded outcomes:

- accept: 43
- fallback: 39
- dependency gap: 25
- failure: 2
- not applicable: 56

Per-asset summary:

| Asset role | Candidate lanes | Newton contact/drop/sphere outcome | Recorded fallback/failure |
|---|---:|---|---|
| `rigid_prop` | bbox 1, CPD 12 | both lanes pass drop and sphere | convex/CoACD/stack gaps |
| `container` | bbox 1, CPD 16 | bbox passes; CPD sphere passes | CPD drop `not_settled`, final speed 4.281419293463846 m/s |
| `contact_affordance` | bbox 1, CPD 16 | bbox passes; CPD sphere passes | CPD drop `not_settled`, final speed 0.35619539431284264 m/s |
| `stackable` | bbox 1, CPD 16 | both lanes pass drop and sphere | stack runner pending |
| `precision_negative_control` | bbox 1, CPD 12 | both lanes pass drop and sphere | precision manual review required |

The first attempted run used the ambient `/usr/bin/python` and produced Newton dependency gaps
because `warp` was unavailable. That report is retained only as an environment-misuse observation;
the evidence report above uses the documented clean Newton environment.

## Verification

- `env NPC_ENV_ROOT=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310 NPC_PYTHON=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python NPC_CODE_ROOT=/cpfs/user/zhuzihou/dev/physics-primitive-agent NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton NPC_OUTPUT_DIR=/cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/environment-readiness/local python scripts/env/readiness_check.py`:
  exit 0, status `smoke_passed`.
- `env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark > reports/generated/phase0_baseline/phase0_grscenes_rigid_newton_2026-05-25.json`:
  final rerun after source-hash, asset-gate, and CLI benchmark-record semantics, exit 0, elapsed
  298 seconds, report status
  `completed_with_recorded_failures`.
- `python -m pytest tests/test_phase0_benchmark.py tests/test_cli.py::test_cli_run_phase0_benchmark_emits_json_for_partial_record tests/test_cli.py::test_cli_run_phase0_benchmark_returns_zero_for_recorded_failures tests/test_configs.py::test_phase0_config_defines_baselines_probes_and_required_metrics -q`:
  5 passed.

## Artifacts

- Config: `configs/experiments/phase0_baseline.yaml`.
- Asset manifest: `assets/manifests/phase0_assets.yaml`.
- Generated report, ignored by git:
  `reports/generated/phase0_baseline/phase0_grscenes_rigid_newton_2026-05-25.json`.
- Environment readiness report, ignored by git:
  `reports/generated/environment-readiness/local/environment-readiness.json`.

## Claim Impact

- Supports a scoped rigid Phase 0 diagnostic table: five GRScenes rigid assets, recorded source
  manifests, generated candidate packages, and named Newton contact/drop/sphere outcomes.
- Supports the claim that the checker reports accept/fallback/failure outcomes instead of hiding
  failing primitive packages.
- Does not support broad benchmark superiority, full-simulation speedup, collision-quality
  validation, complete Phase 0 coverage, or whole-robot articulation claims.

## Next Action

Use the follow-up record for current Phase 0 status and next actions.
