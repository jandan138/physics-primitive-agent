# 2026-05-16 Controlled Merge-Search Newton Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_controlled_merge_search_newton_probe`, a synthetic-only contact-gated Newton
  task-smoke probe for the existing `cost_guided_pair_choice` merge/search fixture.
- The report compares:
  - default package lane: `topology_then_virtual`;
  - opt-in package lane: `cost_guided_pairwise`.
- The report runs:
  - `newton_contact_smoke` first;
  - `newton_drop_settle` and `newton_sphere_rain` only if contact passes.
- Added config:
  `configs/experiments/controlled_merge_search_newton_probe.yaml`.
- Added CLI:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/controlled_merge_search_newton_probe.yaml --run-cpd-like-controlled-merge-search-newton-probe`.

## Result

The clean local Newton run reported `smoke_passed` for the synthetic package pair:

- default package source faces: `[[0, 1], [2]]`;
- opt-in package source faces: `[[0, 2], [1]]`;
- both packages passed contact canary;
- both packages passed drop/settle;
- both packages passed sphere-rain.

This is named synthetic task-smoke execution evidence for one changed merge/search package pair. It
is not merge-policy superiority evidence, collision-quality validation, real-USD evidence,
bed/Franka evidence, benchmark evidence, real contact-stress measurement, safety certification, or
CPD paper reproduction.

## Verification

- RED:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_runs_contact_gated_tasks tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_blocks_tasks_when_contact_fails tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_does_not_pass_when_pair_unchanged tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_requires_config tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_requires_source_dir tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_wrong_fixture tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_wrong_task tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_missing_verify tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_emits_json tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_rejects_nonfinite_json tests/test_cli.py::test_cli_run_cpd_like_controlled_merge_search_newton_probe_returns_nonzero_for_partial tests/test_cpd_like_config.py::test_controlled_merge_search_newton_probe_config_is_synthetic_and_claim_bounded`
  failed because the new claim constant, report builder, CLI flag, and config did not exist.
- GREEN:
  the same focused command passed with 13 tests after implementation.
- Clean-env CLI smoke:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/controlled_merge_search_newton_probe.yaml --run-cpd-like-controlled-merge-search-newton-probe`
  returned exit code 0 and `smoke_passed`.
- Review-fix regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_runs_contact_gated_tasks tests/test_cpd_like_synthetic.py::test_controlled_merge_search_newton_probe_blocks_tasks_when_contact_fails`
  passed with 2 tests after fixing the nested decision claim boundary and blocked-task
  `status_gate`.
- Full regression:
  `python -m pytest -q` passed with 348 tests after the review fixes.
- Documentation and claim checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed before and after the review fixes.

Multi-agent review found no Critical issues. Implementation review reported one Important issue:
the nested decision `status_gate` said `newton_tasks_smoke_passed` whenever the package pair
changed, even when contact blocked the task probes. That was fixed and covered by regression.
Documentation review reported one Important issue: canonical unsupported-claim text did not list
the controlled merge-search Newton probe among already recorded synthetic task-smoke exceptions.
That was fixed in the claim-boundary and evidence-status docs.

Final re-review reported no Critical or Important issues. One Minor wording issue was fixed by
renaming the evidence-status exception from ambiguous package smokes to controlled merge-search
Newton task smokes.

## Claim Impact

This record supports only a synthetic controlled merge-search Newton task-smoke probe over one
changed package pair. It records named contact, drop/settle, and sphere-rain task status under
recorded settings.

It does not support default merge-policy change, merge-policy superiority, real-USD package
improvement, bed/Franka evidence, collision-quality validation, benchmark evidence, safety
certification, or CPD paper reproduction.

## Next Action

Use this synthetic task-smoke evidence to design a more direct merge/search algorithmic change,
still under synthetic selection, package, mapping, and Newton-task gates before any capped
bed/Franka rerun.
