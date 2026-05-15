# 2026-05-15 CPD-Like Cost-Guided Merge

## Date

2026-05-15

## Status

Complete.

## Changes

- Added an opt-in `cost_guided_pairwise` merge-search policy for the CPD-like decomposition
  baseline.
- Added `merge_search_policy` to decomposition reports and objective component accounting.
- Added `cpd_like_cost_guided_synthetic_objective_comparison`, a command-only deterministic
  synthetic smoke that compares the default `topology_then_virtual` merge order with the opt-in
  `cost_guided_pairwise` policy.
- Used AABB-normalized merge-excess as the decision-making cost for the focused synthetic merge
  choice.
- Added `--run-cpd-like-cost-guided-synthetic-comparison` as a no-config CLI path that emits
  strict JSON.
- Updated claim-boundary, evidence, CPD story, objective-alignment, index, README, and registry
  documentation.

## Verification

- `python -m pytest tests/test_cpd_like_decompose.py -q -k "cost_guided or merge_search or component_merge"`:
  8 passed, 5 deselected.
- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py -q`:
  24 passed.
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "cost_guided or synthetic_comparison or cpd_like_synthetic"`:
  8 passed, 37 deselected.
- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "cost_guided or synthetic_comparison or cpd_like_synthetic"`:
  10 passed, 48 deselected.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-synthetic-comparison`:
  exit 0.
- `python -m pytest -q`: 161 passed.
- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.

## Smoke Summary

- Stage: `cpd_like_cost_guided_synthetic_objective_comparison`
- Status: `smoke_passed`
- Claim boundary: `cost_guided_synthetic_comparison_not_collision_quality_validation`
- Evidence level: `offline_cpd_like_cost_guided_synthetic_comparison_smoke`
- Case: `cost_guided_pair_choice`
- Default policy: `topology_then_virtual`
- Default accepted normalized merge-excess sum: `0.010062106570764756`
- Cost-guided policy: `cost_guided_pairwise`
- Cost-guided accepted normalized merge-excess sum: `0.000055121`
- Diagnostic delta: `-0.010006985570764756`

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_like/decompose.py`
- `src/primitive_collision_compiler/baselines/cpd_like/objective.py`
- `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- `src/primitive_collision_compiler/cli.py`
- `tests/test_cpd_like_decompose.py`
- `tests/test_cpd_like_synthetic.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-15-cpd-cost-guided-merge-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-cost-guided-merge.md`
- `experiments/registry.yaml`

Generated JSON output was not committed.

## Claim Impact

This supports only a focused CPD-like cost-guided merge-search smoke over deterministic synthetic
fixtures and any explicitly re-run capped smoke assets. It is diagnostic accounting for future CPD
reproduction work, not full CPD paper reproduction, paper-faithful optimization, collision-quality
validation, benchmark evidence, broad asset/task evidence, robot collider quality, or
safety/deployment evidence.

## Next Action

Add a broader synthetic fixture only when it exposes a specific expected failure mode, or add one
focused primitive-fitting improvement against the current synthetic harness before changing Newton
probes.
