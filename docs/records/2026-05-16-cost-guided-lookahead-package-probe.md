# 2026-05-16 Cost-Guided Lookahead Package Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_cost_guided_lookahead_package_probe`, a command-only synthetic package-path and
  Newton shape-mapping probe for the `lookahead_merge_trap` package pair.
- The report compares:
  - greedy lane: `cost_guided_pairwise`;
  - lookahead lane: `two_step_lookahead`.
- The report converts both decompositions to `CollisionPackage`, compares package payloads, and
  records Newton shape-mapping status counts.
- Added CLI:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-lookahead-package-probe`.

## Result

The focused CLI smoke reported `smoke_passed`:

- greedy package source faces: `[[0, 2, 3], [1]]`;
- lookahead package source faces: `[[0, 1], [2, 3]]`;
- greedy package mapping status counts: `{"mapped": 2}`;
- lookahead package mapping status counts: `{"mapped": 2}`;
- `newton_task_comparison_triggered: false`.

This is package-path and Newton shape-mapping accounting only. It does not change default merge
behavior, rank merge policies, run Newton runtime tasks, touch real assets, report bed or Franka
results, measure collision geometry quality, compare against a benchmark suite, support deployment
or certification conclusions, or complete paper-level reproduction.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_outputs_mapped_changed_package tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_package_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_returns_nonzero_for_partial tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_package_probe_rejects_nonfinite_json`
  failed because the new claim constant, report builder, and CLI flag did not exist.
- GREEN:
  the same command passed with 5 tests after implementation.
- Focused regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py -k "lookahead_package" tests/test_cli.py -k "lookahead_package"`
  passed with 5 tests and 140 deselected.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-lookahead-package-probe`
  returned exit code 0 and `smoke_passed`.
- Multi-agent implementation re-review found no Critical, Important, or Minor findings for the
  scoped package-probe implementation.
- Multi-agent documentation re-review found no Critical or Important findings after claim-boundary
  wording and next-action updates. The remaining Minor wording cleanup was applied to this record.
- Full regression:
  `python -m pytest -q`
  passed with 362 tests.
- Documentation and workspace checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed.

## Claim Impact

This record supports only a synthetic lookahead package-path and Newton shape-mapping probe over
one deterministic toy fixture. It records that the greedy and lookahead package lanes differ and
that both packages map to Newton shapes.

It does not support a default merge-policy change, policy ranking, Newton runtime-task status,
real-asset package improvement, bed or Franka conclusions, collision geometry quality claims,
benchmark-suite conclusions, deployment or certification conclusions, or paper-level reproduction.

## Next Action

The next legal gate is an explicitly opt-in synthetic Newton task-smoke probe over the
lookahead-changed package pair, still before any capped bed/Franka rerun.
