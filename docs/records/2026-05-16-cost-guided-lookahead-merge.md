# 2026-05-16 Cost-Guided Lookahead Merge

## Date

2026-05-16

## Status

Complete

## Changes

- Added `merge_search_policy: two_step_lookahead`, an explicitly opt-in synthetic two-step
  lookahead policy for tiny CPD-like merge/search fixtures.
- The policy is bounded to at most six mesh faces and requires
  `component_merge: virtual_pairwise`.
- Added a deterministic `lookahead_merge_trap` fixture where greedy `cost_guided_pairwise` chooses
  a locally cheap first merge but a higher two-step total, while `two_step_lookahead` chooses a
  lower projected two-step path.
- Added `cpd_like_cost_guided_lookahead_merge_report`, a command-only offline synthetic report.
- Added CLI:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-lookahead-merge-report`.

## Result

The focused CLI smoke reported `smoke_passed`:

- fixture: `lookahead_merge_trap`;
- greedy source-face grouping: `[[0, 2, 3], [1]]`;
- lookahead source-face grouping: `[[0, 1], [2, 3]]`;
- `lookahead_decision_changed: true`;
- `projected_cost_improved: true`.

This is offline synthetic merge/search decision accounting. It is not a default merge-policy
change, merge-policy superiority result, package-path result, Newton task result, real-USD result,
bed/Franka evidence, collision-quality validation, benchmark evidence, safety certification, or
CPD paper reproduction.

## Verification

- RED decomposition:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_changes_first_merge_on_trap tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_requires_virtual_pairwise tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_rejects_non_tiny_mesh tests/test_cpd_like_decompose.py::test_decompose_mesh_two_step_lookahead_preserves_virtual_threshold_block`
  failed because `two_step_lookahead` was unknown.
- GREEN decomposition:
  the same command passed with 4 tests after implementation.
- Focused merge/search regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py -k "lookahead or cost_guided or merge_search"`
  passed with 10 tests.
- RED report/CLI:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_is_strict_json_serializable tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_emits_json tests/test_cli.py::test_cli_run_cpd_like_cost_guided_lookahead_merge_report_rejects_nonfinite_json`
  failed because the new claim constant, report builder, and CLI flag did not exist.
- GREEN report/CLI:
  the same command passed with 4 tests after implementation.
- Review-fix regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_synthetic.py::test_cost_guided_lookahead_merge_report_compares_greedy_and_lookahead`
  passed after making `projected_cost_improved` read from first-step projected-total report fields.
- Focused combined regression:
  `PYTHONPATH=src python -m pytest -q tests/test_cpd_like_decompose.py -k "lookahead or cost_guided or merge_search" tests/test_cpd_like_synthetic.py -k "lookahead" tests/test_cli.py -k "lookahead"`
  passed with 8 tests and 160 deselected.
- CLI smoke:
  `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cost-guided-lookahead-merge-report`
  returned exit code 0 and `smoke_passed`.
- Full regression:
  `python -m pytest -q` passed with 357 tests after review fixes.
- Documentation and claim checks:
  `python scripts/validate_docs.py`, `python scripts/validate_site_claims.py`, and
  `git diff --check` passed after review fixes.

Multi-agent review found no Critical or Important issues. Documentation review reported two Minor
wording issues around proof/first-claim language; both were rewritten to use narrower diagnostic
wording. Implementation review reported one Minor issue: `projected_cost_improved` should read
from projected-total trace/report fields rather than final accepted sums. That was fixed and
covered by regression.

## Claim Impact

This record supports only a bounded synthetic two-step merge/search lookahead smoke over one
deterministic toy fixture. It records that one opt-in lookahead lane changes the toy grouping and
lowers the projected two-step normalized merge-excess under the current surrogate.

It does not support default merge-policy change, merge-policy superiority, package-path evidence,
Newton contact/task evidence, real-USD package improvement, bed/Franka evidence,
collision-quality validation, benchmark evidence, safety certification, or CPD paper reproduction.

## Next Action

The follow-on package-path and Newton shape-mapping probe is now tracked in
`docs/records/2026-05-16-cost-guided-lookahead-package-probe.md`. The next legal gate after that
probe is an explicitly opt-in synthetic Newton task-smoke probe for the lookahead-changed package
pair, still before any capped bed/Franka rerun.
