# 2026-05-15 CPD Synthetic Expected-Failure Workbench

## Date

2026-05-15

## Status

Complete

## Changes

- Added `cpd_like_expected_failure_synthetic_workbench`, a command-only deterministic
  expected-failure synthetic workbench for the current CPD-like baseline.
- Added `npc-compile --run-cpd-like-expected-failure-workbench`, which emits strict JSON without a
  config file because the meshes are in-memory fixtures.
- Added three expected limitation fixtures:
  - `restricted_primitive_vocabulary_gap`;
  - `single_proxy_wraps_disconnected_components`;
  - `threshold_blocks_component_merge`.
- Added expected/observed/missing/unexpected diagnostic flag accounting for each fixture.
- Added `status_semantics` value
  `expected_limitations_reported_not_decomposition_success` to make `smoke_passed` explicit.

## Fixture Semantics

`restricted_primitive_vocabulary_gap` checks that the current restricted `box` subset still reports
unsupported CPD paper primitive types and that the paper alignment remains a surrogate, not a
paper-faithful objective.

`single_proxy_wraps_disconnected_components` checks that a virtual component merge over
disconnected triangles reports a virtual component merge and an empty-space wrapper proxy.

`threshold_blocks_component_merge` checks that a zero virtual-merge threshold reports the blocked
component merge, unmerged components, and primitive-budget pressure.

For all cases, `expectation_status: matched` means the expected diagnostic flags matched the
observed diagnostic flags with no missing or unexpected flags. It does not mean the decomposition
is good.

## Verification

- `PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-expected-failure-workbench`
  exited 0 and emitted strict JSON with stage `cpd_like_expected_failure_synthetic_workbench`,
  status `smoke_passed`, and status semantics
  `expected_limitations_reported_not_decomposition_success`.
- `python scripts/validate_docs.py`: exit 0, `docs validation passed`.
- `git diff --check`: exit 0, no whitespace errors.
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "expected_failure or synthetic_comparison"`:
  exit 0, `14 passed, 38 deselected`.
- `python -m pytest -q`: exit 0, `173 passed`.
- `python -m ruff check .`: not run to completion because the current `/usr/bin/python`
  environment does not have `ruff` installed.

## Artifacts

- Source: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`
- CLI: `src/primitive_collision_compiler/cli.py`
- Tests: `tests/test_cpd_like_synthetic.py`, `tests/test_cli.py`
- Registry: `experiments/registry.yaml`
- No raw or generated 3D assets, large logs, videos, or run directories were added.

## Claim Impact

This record supports only a narrow diagnostic claim: the current code can run deterministic
expected limitation fixtures and report whether known CPD-paper gaps remain visible as diagnostic
flags.

This does not support benchmark evidence, collision-quality validation, general failure detection,
safe collider rejection, paper-faithful CPD optimization, or full CPD paper reproduction.

## Next Action

Use the matched expected limitation fixtures to select one focused primitive-fitting or merge-search
improvement. Re-run bed and Franka smokes only after the synthetic diagnostic changes in a named,
inspectable way.
