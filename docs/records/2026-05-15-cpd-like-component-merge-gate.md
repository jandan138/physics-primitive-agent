# 2026-05-15 CPD-Like Component Merge Gate

## Date

2026-05-15

## Status

Complete for the narrow algorithmic smoke slice.

## Changes

- Added an opt-in `cpd_like_component_merge_gate` stage behind
  `cpd_like.component_merge: virtual_pairwise`.
- Kept the default CPD-like path as topology-only face merging.
- Added pairwise disconnected-component merge candidates after topological adjacency merges are
  exhausted, with an optional AABB-normalized excess-volume threshold.
- Added report fields for merge policy, AABB volume, target primitive count, initial/final
  component counts, topology merge count, virtual component merge count, blocked merge count,
  normalized total weighted volume, and merge-cost summary.
- Added per-primitive `source_face_count`, `source_component_ids`, and `cost_weight` fields to the
  CPD-like report JSON.
- Added `configs/experiments/cpd_like_component_merge_gate.yaml` as the bed smoke config for this
  slice.

## Verification

- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_config.py::test_cpd_like_component_merge_gate_config_is_opt_in_and_claim_bounded tests/test_cli.py::test_cli_run_cpd_like_component_merge_gate_emits_merge_metrics -q`: 10 passed.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_component_merge_gate.yaml --run-cpd-like`: exit 0.

Clean-env bed smoke result summary:

- `stage`: `cpd_like_component_merge_gate`
- `status`: `smoke_passed`
- `evidence_level`: `geometry_only_cpd_like_component_merge_smoke`
- asset: capped GRScenes bed manifest role `bed_dev_smoke`
- mesh: 1898 points, 256 capped faces
- primitive budget: 32
- primitive output count: 32
- merge policy: `virtual_pairwise`
- initial component count: 256
- final component count: 32
- topology merge count: 224
- virtual component merge count: 0
- blocked merge count: 0
- mesh AABB volume: `582378.0582874214`
- normalized total weighted volume: `0.0009961811821648128`
- accepted normalized excess max: `8.193793579898176e-05`

The real bed smoke did not need a virtual disconnected-component merge because topological
adjacency merges already reached the configured primitive budget. The virtual merge behavior is
covered by the focused unit and CLI tests using disconnected triangle components.

## Artifacts

- Config: `configs/experiments/cpd_like_component_merge_gate.yaml`
- Code: `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- Primitive report schema: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- CLI: `src/primitive_collision_compiler/cli.py`
- Generated console JSON was not committed; large/generated run outputs remain outside git.

## Claim Impact

This supports only a geometry-only CPD-like component-merge gate smoke. It is useful as a
paper-story step because it exposes disconnected-component merge candidates and normalized
excess-volume accounting, but it is not the CPD paper algorithm.

It does not support full CPD paper reproduction, paper-scope primitive coverage, collision quality
validation, benchmark superiority, broad asset/task coverage, deployment readiness, or safety
certification.

## Next Action

Run full verification and request final review over the combined sphere-rain, Franka, and
component-merge-gate diff before merging the worktree.
