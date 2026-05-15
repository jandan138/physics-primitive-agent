# 2026-05-15 CPD-Like Synthetic Comparison

## Date

2026-05-15

## Status

Complete.

## Changes

- Added `cpd_like_synthetic_objective_comparison`, a command-only offline synthetic comparison
  over deterministic in-memory toy meshes.
- Added `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py` with three fixture
  cases: `adjacent_square`, `disconnected_pair`, and `blocked_disconnected_pair`.
- Added `--run-cpd-like-synthetic-comparison` as a no-config CLI path that emits strict JSON.
- Reused the existing CPD-like objective report for topology-only and `virtual_pairwise`
  component-merge accounting.
- Recorded the registry entry as command-backed rather than config-backed because the fixtures are
  defined in source and no asset/config file is needed.

## Verification

- `python -m pytest tests/test_cpd_like_synthetic.py -q`: 2 passed.
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "synthetic_comparison or cpd_like_synthetic"`: 4 passed, 37 deselected.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-synthetic-comparison`: exit 0.
- `python -m pytest -q`: 153 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.

## Smoke Summary

- Stage: `cpd_like_synthetic_objective_comparison`
- Status: `smoke_passed`
- Claim boundary: `synthetic_objective_comparison_not_collision_quality_validation`
- Evidence level: `offline_cpd_like_synthetic_comparison_smoke`
- Cases:
  - `adjacent_square`: topology-only and `virtual_pairwise` both report one primitive.
  - `disconnected_pair`: topology-only reports a partial two-primitive result with
    `unmerged_components`; `virtual_pairwise` reports one primitive and no failure labels.
  - `blocked_disconnected_pair`: `virtual_pairwise` reports `component_merge_blocked` when the
    virtual merge threshold is zero.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `tests/test_cpd_like_synthetic.py`
- `docs/superpowers/specs/2026-05-15-cpd-synthetic-comparison-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-synthetic-comparison.md`
- `experiments/registry.yaml`

Generated JSON output was not committed.

## Claim Impact

This record supports only a synthetic objective diagnostic comparison over deterministic toy
meshes. It does not support collision-quality validation, benchmark superiority, broad asset/task
coverage, paper-faithful optimization, full CPD paper reproduction, robot collider quality, or
safety/deployment claims.

## Next Action

Use the synthetic comparison harness to guide one focused primitive-fitting or merge-search
improvement, then compare the same fixtures again before changing Newton probes.
