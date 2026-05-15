# 2026-05-15 Real USD Candidate Audit

## Date

2026-05-15

## Status

Complete

## Supersession Note

This record captures pre-cylinder-axis candidate accounting. Current status is superseded by
[2026-05-15 Candidate Loss Diagnosis And Cylinder Axis](2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md),
which adds per-cluster candidate-loss diagnosis and records `3` capped Franka native
`cylinder` selections under the current surrogate.

## Changes

- Added `candidate_audit_summary` to each lane in the real-USD native fitting comparison report.
- The summary recomputes candidates for each final selected cluster using the same primitive
  fitting helper as the selector.
- The report records selected rank counts, extension-best counts, box-selected counts, and
  surrogate margins without emitting large raw per-candidate tables.
- Margin sign convention is `selected_cost_minus_comparator_cost`: negative means the selected
  primitive is cheaper under the surrogate, positive means the comparator is cheaper.

## Verification

- `python -m pytest tests/test_real_usd_native_comparison.py::test_real_usd_candidate_audit_reports_selected_rank_two_margin tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_runs_roles_from_manifest tests/test_real_usd_native_comparison.py::test_real_usd_native_fitting_report_is_strict_json_serializable -q`
  exited `0` with `3 passed`.
- `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -m primitive_collision_compiler.cli --config configs/experiments/bed_franka_native_probe_comparison.yaml --run-real-usd-native-fitting-comparison > reports/generated/bed_franka_native_probe_comparison/real_usd_native_fitting_conda.json`
  exited `0` and emitted report status `smoke_passed`.
- `python -m pytest -q` exited `0` with `240 passed`.
- `python scripts/validate_docs.py` exited `0`.
- `git diff --check` exited `0`.

## Artifacts

- Code: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
- Tests: `tests/test_real_usd_native_comparison.py`
- Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
- Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_fitting_conda.json`

## Claim Impact

- Supports real-USD candidate accounting for capped bed and capped Franka first-mesh old/new lanes.
- Explains whether `cylinder`, `cone`, or `ellipsoid` wins any selected cluster under the current
  weighted-volume surrogate.
- Does not support native primitive improvement, collision-quality validation, benchmark
  superiority, whole-robot Franka collider quality, paper-faithful CPD optimization, deployment
  readiness, or safety certification.

## Next Action

- Use the real-USD candidate audit summary to choose the smallest primitive-fitting or merge-search
  change that can make a justified non-box native primitive win on an inspectable case.

## Result Summary

- `bed_dev_smoke` native lane: `32` selected boxes, `0` clusters where an extension primitive was
  the cheapest candidate, and `32` box-selected clusters where an extension primitive was second.
- `franka_import_smoke` native lane: `32` selected boxes, `0` clusters where an extension primitive
  was the cheapest candidate, and `32` box-selected clusters where an extension primitive was
  second.
- Mean selected-minus-best-extension normalized margin was negative for both capped assets,
  meaning the selected boxes were still cheaper than the best extension candidates under the
  current surrogate:
  - `bed_dev_smoke`: `-4.832888497597031e-05`;
  - `franka_import_smoke`: `-7.566989131210826e-07`.
