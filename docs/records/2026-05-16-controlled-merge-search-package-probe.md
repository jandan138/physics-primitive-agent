# 2026-05-16 Controlled Merge-Search Package Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_controlled_merge_search_package_probe`, a command-only synthetic package-path
  probe for the existing `cost_guided_pair_choice` merge/search fixture.
- The report compares:
  - default lane: `topology_then_virtual`;
  - opt-in lane: `cost_guided_pairwise`.
- The report records:
  - default package primitive source faces `[[0, 1], [2]]`;
  - opt-in package primitive source faces `[[0, 2], [1]]`;
  - `package_pair_changed: true`;
  - `merge_search_behavior_changed: true`;
  - Newton shape-mapping status counts for both package lanes;
  - `newton_task_comparison_triggered: false`.
- Added CLI:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-controlled-merge-search-package-probe`.

## Result

The local CLI smoke returned `smoke_passed`:

- default accepted normalized merge-excess sum: `0.010062106570764756`;
- opt-in accepted normalized merge-excess sum: `0.000055121`;
- accepted normalized merge-excess delta: `-0.010006985570764756`;
- default mapping status counts: `{"mapped": 2}`;
- opt-in mapping status counts: `{"mapped": 2}`.

This is synthetic package-path and Newton shape-mapping accounting for one deterministic
merge/search fixture. It is not a new merge optimizer, default pipeline change, Newton task
diagnostic, simulation-checked package, real-USD result, collision-quality validation, benchmark
evidence, or CPD paper reproduction.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_controlled_merge_search_package_probe_outputs_mapped_changed_package tests/test_cpd_like_synthetic.py::test_controlled_merge_search_package_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_package_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_package_probe_returns_nonzero_for_partial`
  failed because the new claim constant, report builder, and CLI flag did not exist.
- GREEN:
  the same focused command passed with 4 tests after implementation.
- Focused regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_package_probe_rejects_nonfinite_json tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_package_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_package_probe_returns_nonzero_for_partial tests/test_cpd_like_synthetic.py::test_controlled_merge_search_package_probe_outputs_mapped_changed_package tests/test_cpd_like_synthetic.py::test_controlled_merge_search_package_probe_report_is_strict_json_serializable`
  passed with 5 tests after review added CLI non-finite JSON coverage.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-controlled-merge-search-package-probe`
  returned exit code 0 and `smoke_passed`.
- Full regression:
  `python -m pytest -q` passed with 335 tests.
- Documentation and claim checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed.

Multi-agent review found no Critical or Important issues. Minor review feedback was fixed by
aligning navigation/next-step wording and adding CLI non-finite JSON coverage.

## Claim Impact

This record supports only a single-fixture synthetic controlled merge-search package-path probe. It
shows that the existing opt-in cost-guided merge-search smoke changes the synthetic package grouping
and that both generated packages map to Newton shapes.

It does not support a default merge policy change, merge-policy superiority claim, Newton
contact/task evidence, real-USD package improvement, bed/Franka evidence, collision-quality
validation, benchmark evidence, safety certification, or CPD paper reproduction.

## Next Action

The follow-on controlled merge-search Newton probe now covers the explicitly opt-in synthetic
contact-gated task-smoke step for this changed package pair. The next legal slice is a more direct
algorithmic merge/search change with the same synthetic package, mapping, and Newton-task gates
before any capped bed/Franka rerun.
