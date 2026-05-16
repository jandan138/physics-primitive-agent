# 2026-05-15 Low-Support Native Extension Admissibility

## Date

2026-05-15

## Status

Complete

## Summary

Added a support-aware primitive-selection guard for Newton-native extension candidates in the
CPD-like diagnostic workbench. The guard keeps candidate fitting intact, but ranks `cylinder`,
`cone`, and `ellipsoid` as selection-inadmissible when they have too little local support and a
fallback primitive is available.

This executes the low-support branch identified by the prior candidate-loss triage. It is not a
paper-faithful CPD objective, not benchmark evidence, and not collision-quality validation.

## Implementation

- Added support-aware ranking at `fit_best_primitive` selection time.
- Added `rank_primitive_candidates_for_selection` audit metadata:
  - `raw_cost_rank`;
  - support-aware selection rank;
  - `selection_admissible`;
  - `selection_admissibility_reason`;
  - source-face and unique-point support thresholds.
- Added a deterministic low-support patch test where a raw-cost cheaper `cylinder` loses to `box`
  because the patch has only two faces and four unique points.
- Added candidate-loss labeling for cheaper but blocked native extensions:
  `extension_candidate_blocked_by_support` and `extension_support_admissibility`.

Current thresholds:

- extension kinds: `cylinder`, `cone`, `ellipsoid`;
- minimum source faces: `3`;
- minimum unique assigned points: `5`;
- extension-only primitive subsets still return the best available extension candidate.

## Results

Synthetic native fitting comparison still reports `smoke_passed`:

| Fixture | Native selection | Support reason |
| --- | --- | --- |
| `cylindrical_rod` | `cylinder` | `support_thresholds_met` |
| `tapered_cone` | `cone` | `support_thresholds_met` |
| `ellipsoid_blob` | `ellipsoid` | `support_thresholds_met` |
| `squat_cylinder` | `cylinder` | `support_thresholds_met` |

Real-USD candidate-loss rerun:

| Asset role | Current native result | Candidate-loss interpretation |
| --- | --- | --- |
| `bed_dev_smoke` | `32` boxes | `32` extension candidates are more expensive under the surrogate; `1` cylinder near-miss target remains. |
| `franka_import_smoke` | `32` boxes | `29` extension candidates are more expensive; `3` cheaper raw-cost cylinders are blocked by support admissibility; `3` cylinder near-miss targets remain. |

Real-USD Newton gates under the conda-managed Newton environment:

| Gate | Status |
| --- | --- |
| contact comparison | `smoke_passed` for bed and Franka old/new lanes |
| drop/settle | `smoke_passed` for bed and Franka old/new lanes |
| sphere-rain | `smoke_passed` for bed and Franka old/new lanes |

Using the default shell `python` produced `dependency_gap` for Newton probes, while the
project-standard conda-managed interpreter entered Newton and passed the named smokes. This record
therefore treats the conda-managed environment as the evidence environment for Newton task claims.

## Verification

- `python -m pytest -q tests/test_cpd_like_synthetic.py tests/test_real_usd_native_comparison.py tests/test_cli.py::test_cli_run_newton_native_fitting_comparison_emits_json_without_config tests/test_cpd_like_config.py::test_newton_native_fitting_comparison_config_includes_bed_and_franka_scope`
  exited `0` with `35 passed`.
- `python -m pytest -q` exited `0` with `281 passed`.
- `python scripts/validate_docs.py` exited `0` with docs validation passed.
- `python scripts/validate_site_claims.py` exited `0` with site claim validation passed.
- `python -m pytest -q tests/test_site_claims.py` exited `0` with `13 passed`.
- `git diff --check` exited `0`.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --run-newton-native-fitting-comparison`
  exited `0` and reported synthetic status `smoke_passed`.
- `PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-candidate-loss-diagnosis`
  exited `0` and reported real-USD candidate-loss status `smoke_passed` with bed `32` boxes and
  Franka `32` boxes.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-contact-comparison`
  exited `0` and reported contact status `smoke_passed`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-task-comparison`
  exited `0` and reported task status `smoke_passed`.

## Claim Impact

This supports only support-aware diagnostic primitive selection and candidate-loss accounting under
capped first-mesh scope. It does not support:

- CPD paper reproduction;
- paper-faithful objective or priority-queue merge implementation;
- proof that boxes are better than cylinders;
- proof that cylinders are bad;
- whole-robot Franka collider quality;
- collision-quality validation;
- benchmark superiority.

## Next Step

Use the now-current near-miss targets to build a `cylinder_near_miss_cluster` fixture. That next
slice should test whether cylinder fitting or cluster grouping can be improved on a richer support
case, then rerun capped bed/Franka candidate-loss and Newton gates.
