# 2026-05-16 Cost-Guided Lookahead Newton Probe

## Date

2026-05-16

## Status

Complete

## Changes

- Added `cpd_like_cost_guided_lookahead_newton_probe`, an explicitly opt-in synthetic Newton
  task-smoke probe for the `lookahead_merge_trap` package pair.
- The report compares:
  - greedy lane: `cost_guided_pairwise`;
  - lookahead lane: `two_step_lookahead`.
- The report runs `newton_contact_smoke` first for each package lane.
- The report runs `newton_drop_settle` and `newton_sphere_rain` only for lanes whose contact canary
  reports `smoke_passed`.
- Added config:
  `configs/experiments/cost_guided_lookahead_newton_probe.yaml`.
- Added CLI:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cost_guided_lookahead_newton_probe.yaml --run-cpd-like-cost-guided-lookahead-newton-probe`.

## Result

Focused tests verify the report shape, contact gating, mixed-lane contact gating, wrong
package-face guard, config ownership, and CLI config handling. A clean Newton runtime smoke also
reported `smoke_passed` for contact, drop/settle, and sphere-rain on both package lanes.

This is synthetic Newton task-smoke status under recorded settings only. It does not change default
merge behavior, rank merge policies, touch real assets, report bed or Franka results, measure
collision geometry quality, compare against a benchmark suite, support deployment or certification
conclusions, or complete paper-level reproduction.

## Verification

- RED report-builder tests:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_runs_contact_gated_tasks tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_blocks_tasks_when_contact_fails tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_does_not_pass_when_pair_unchanged tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_newton_probe_report_is_strict_json_serializable`
  failed because the new constants and report builder did not exist.
- RED config and CLI tests:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded tests/test_cli.py -k "cost_guided_lookahead_newton_probe"`
  failed because the config, CLI flag, and CLI builder import did not exist.
- GREEN focused implementation/config/CLI tests:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py -k "lookahead_newton_probe" tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded tests/test_cli.py -k "cost_guided_lookahead_newton_probe"`
  passed with 15 tests.

- Clean Newton CLI smoke:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/cost_guided_lookahead_newton_probe.yaml --run-cpd-like-cost-guided-lookahead-newton-probe`
  returned exit code 0 with top-level `smoke_passed`.
- The clean Newton smoke reported:
  - greedy contact: `smoke_passed`;
  - lookahead contact: `smoke_passed`;
  - greedy drop/settle and sphere-rain: `smoke_passed`;
  - lookahead drop/settle and sphere-rain: `smoke_passed`;
  - decision status gate: `newton_tasks_smoke_passed`.

- Multi-agent implementation review found no Critical, Important, or Minor findings for the
  scoped implementation.
- Multi-agent documentation review found no Critical findings and three Important documentation
  status/boundary gaps, all fixed before completion.
- Focused regression after review:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py -k "lookahead_newton_probe" tests/test_cpd_like_config.py::test_cost_guided_lookahead_newton_probe_config_is_synthetic_and_claim_bounded tests/test_cli.py -k "cost_guided_lookahead_newton_probe"`
  passed with 15 tests.
- Full regression:
  `python -m pytest -q`
  passed with 379 tests.
- Documentation and workspace checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed.

## Claim Impact

This record supports focused test evidence, clean Newton CLI smoke evidence, multi-agent review,
and full verification for named synthetic task-smoke status on the lookahead-changed package pair
under recorded settings.

It does not support policy ranking, real-asset conclusions, bed or Franka conclusions, collision
geometry quality claims, benchmark-suite conclusions, deployment or certification conclusions, or
paper-level reproduction.

## Next Action

The next step is not a bed/Franka rerun unless a separate real package change is introduced and
passes full mapping, contact-canary, task-gate, and dated-record gates. Otherwise, continue with
the next paper-aligned objective, fitting, or merge-search slice.
