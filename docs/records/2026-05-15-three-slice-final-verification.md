# 2026-05-15 Three-Slice Final Verification

## Date

2026-05-15

## Status

Complete.

## Changes

- Closed final review findings for the sphere-rain, Franka, and component-merge-gate slice.
- Tightened `newton_sphere_rain` so contact density is based only on explicitly tracked unique
  contacted probe spheres, never inferred from raw Newton contact rows.
- Normalized direct `decompose_mesh(..., excess_volume_threshold_fraction=...)` inputs to float
  before threshold comparisons.
- Made CLI integer parsing report non-finite numbers as config errors instead of uncaught
  exceptions.
- Expanded the sphere-rain record with environment, code-root, branch, base commit, Python,
  Newton, and hardware provenance.
- Removed duplicated Franka absolute-path assertions from tests; machine paths remain in manifests
  and dated records.

## Verification

- `python -m pytest -q`: 128 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/newton_sphere_rain.yaml --run-newton-sphere-rain`: exit 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/franka_cpd_like_smoke.yaml --run-cpd-like`: exit 0.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_component_merge_gate.yaml --run-cpd-like`: exit 0.

Final smoke summaries:

- Sphere-rain: `smoke_passed`, 32/32 primitives mapped, 9 probe spheres, max raw package-probe
  contact rows 1, max unique contacted probe spheres 1, contact density `0.1111111111111111`, no
  failure labels.
- Franka CPD-like smoke: `smoke_passed`, 10384 mesh points, 128 capped faces, 16 restricted
  primitive proposals, `merge_policy: topology_only`, `virtual_component_merge_count: 0`.
- Component-merge gate bed smoke: `smoke_passed`, 1898 mesh points, 256 capped faces, 32
  restricted primitive proposals, 224 topology merges, 0 virtual component merges needed, 0
  blocked merges.

## Artifacts

- Configs:
  - `configs/experiments/newton_sphere_rain.yaml`
  - `configs/experiments/franka_cpd_like_smoke.yaml`
  - `configs/experiments/cpd_like_component_merge_gate.yaml`
- Records:
  - `docs/records/2026-05-15-newton-sphere-rain.md`
  - `docs/records/2026-05-15-franka-cpd-like-smoke.md`
  - `docs/records/2026-05-15-cpd-like-component-merge-gate.md`
- Generated console JSON and runtime logs were not committed.

## Claim Impact

This final verification does not add stronger claims. It confirms the three narrow smoke slices
remain inside the documented boundaries: no full CPD reproduction, no collision-quality
validation, no benchmark claim, no whole-robot evidence, no real contact-stress measurement, and
no safety or deployment claim.

## Next Action

Commit the verified worktree and merge it back to `master`.
