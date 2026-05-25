# 2026-05-26 Link-Aware Robot Package Generation

## Date

2026-05-26

## Status

Complete for the first Phase 0 link-aware robot package generation slice.

## Changes

- Added `source_links` metadata to `PrimitiveSpec` so robot primitives can declare which USD link
  they came from.
- Added a link-aware robot package module that:
  - detects USD Physics rigid-body links;
  - reads USD Physics joint `body0`/`body1` relationships;
  - assigns meshes to their nearest ancestor link;
  - emits one link-framed box primitive for each mesh-bearing link;
  - audits primitive `frame` and `source_links` to reject cross-link merges.
- Integrated the generated robot package and link-boundary audit into Phase 0 articulated robot
  cases while keeping the Newton articulation smoke as a separate source-USD smoke.

## Results

Generated report:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`

Overall recorded outcomes:

- accept: 98
- dependency gap: 0
- failure: 11
- fallback: 30
- not applicable: 70

Report scope:

- rigid assets: 5 from `assets/manifests/phase0_assets.yaml`
- articulated assets: 1 from `assets/manifests/franka_usd_smoke_assets.yaml`
- `link_aware_robot_package_generation`: true
- `whole_robot_collision_quality`: false

Franka link-aware package summary:

| Metric | Value |
|---|---:|
| USD rigid-body links detected | 12 |
| USD joint edges detected | 12 |
| generated link-framed box primitives | 11 |
| cross-link merge count | 0 |
| link-boundary audit status | `smoke_passed` |
| articulation smoke status | `smoke_passed` |

Per-link primitive counts:

- one primitive each for `/panda/panda_link0` through `/panda/panda_link7`,
  `/panda/panda_hand`, `/panda/panda_leftfinger`, and `/panda/panda_rightfinger`;
- zero primitives for `/panda/panda_link8` because the source USD mirror has no mesh under that
  rigid-body link. Newton also reports an inertia/collider warning for `/panda/panda_link8` during
  articulation smoke, so this remains visible evidence for a follow-up meshless-link policy.

## Verification

- `python -m pytest tests/test_phase0_benchmark.py tests/test_link_aware_robot_package.py tests/test_contracts.py -q`:
  12 passed.
- Direct Franka package generation smoke:
  generated 11 primitives over 12 links with `cross_link_merge_count: 0`.
- `time -p timeout 1200 env NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/phase0_baseline.yaml --run-phase0-benchmark > reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`:
  exit 0, `real 925.98`, report status `completed_with_recorded_failures`.
- Parsed the generated JSON successfully. The report records link-aware robot package generation as
  true, Franka package status `generated`, link-boundary audit `smoke_passed`, and articulation
  smoke `smoke_passed`.

## Artifacts

- Design: `docs/superpowers/specs/2026-05-26-link-aware-robot-package-design.md`.
- Plan: `docs/superpowers/plans/2026-05-26-link-aware-robot-package.md`.
- Config: `configs/experiments/phase0_baseline.yaml`.
- Articulation asset manifest: `assets/manifests/franka_usd_smoke_assets.yaml`.
- Generated report, ignored by git:
  `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`.

## Claim Impact

- Supports the claim that the Phase 0 runner now generates a link-aware robot primitive package
  for one Franka USD smoke asset and records a link-boundary audit with zero cross-link merges.
- Supports only link-aware package generation and boundary accounting for the recorded Franka USD
  smoke asset.
- Does not support whole-robot collider quality, manipulation performance, broad robot-operation
  validation, deployment readiness, real-world transfer, or safety certification.
- Does not resolve meshless-link policy: `/panda/panda_link8` remains a recorded zero-primitive
  link requiring follow-up.

## Next Action

Keep the next robot objective focused on meshless-link policy and running articulation/task checks
with generated link-aware packages, while preserving the whole-robot claim boundary.
