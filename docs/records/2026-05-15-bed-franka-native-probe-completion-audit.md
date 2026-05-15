# 2026-05-15 Bed Franka Native Probe Completion Audit

## Date

2026-05-15

## Status

Complete

## Supersession Note

This audit captures the pre-cylinder-axis completion state. Current status is superseded by
[2026-05-15 Candidate Loss Diagnosis And Cylinder Axis](2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md),
which adds candidate-loss diagnosis, a controlled cylinder-axis fitting update, and a rerun where
capped Franka native selects `3` cylinders under the surrogate. This remains diagnostic evidence,
not native primitive quality evidence.

## Objective

Complete the five-step bed/Franka real-USD native probe sequence:

1. add a config-driven real-USD old/new native fitting report;
2. run and compare offline bed/Franka reports;
3. run full-mapping-gated Newton contact canaries;
4. run contact-gated drop/settle and sphere-rain task smokes;
5. update claim-safe documentation and records.

## Prompt-To-Artifact Checklist

- Real-USD old/new fitting runner:
  - Code: `src/primitive_collision_compiler/baselines/cpd_like/real_usd_comparison.py`
  - CLI: `--run-real-usd-native-fitting-comparison`
  - Config: `configs/experiments/bed_franka_native_probe_comparison.yaml`
  - Test: `tests/test_real_usd_native_comparison.py`
  - Record: `docs/records/2026-05-15-real-usd-native-fitting-comparison.md`
- Offline field comparison:
  - Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_fitting_conda.json`
  - Fields: primitive kind counts, primitive count, volume proxy, merge-excess terms,
    containment proxy, paper primitive gap, mapping summary, failure labels.
  - Result: bed and Franka legacy/native lanes all selected `32` boxes and mapped cleanly.
- Contact canary:
  - CLI: `--run-real-usd-native-contact-comparison`
  - Gate: full package mapping required before contact.
  - Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_contact_conda.json`
  - Record: `docs/records/2026-05-15-real-usd-native-contact-comparison.md`
- Drop/settle and sphere-rain:
  - CLI: `--run-real-usd-native-task-comparison`
  - Gate: task probes run only after contact canary passes.
  - Report: `reports/generated/bed_franka_native_probe_comparison/real_usd_native_task_conda.json`
  - Record: `docs/records/2026-05-15-real-usd-native-task-comparison.md`
- Documentation and claim boundaries:
  - Reference: `docs/reference/bed-franka-native-probe-comparison.md`
  - Updated: `docs/reference/claim-boundaries.md`,
    `docs/deepdive/evidence-status.md`,
    `docs/reference/cpd-paper-story-status.md`,
    `docs/reference/newton-native-fitting-comparison.md`,
    `docs/reference/newton-native-primitive-bundle-explainer.md`,
    `docs/reference/bed-franka-native-fitting-next-steps.md`,
    `docs/index.md`,
    `README.md`,
    `experiments/registry.yaml`.

## Verification

- `python -m pytest -q` exited `0` with `226 passed`.
- `python scripts/validate_docs.py` exited `0`.
- `git diff --check` exited `0`.
- Real command statuses after switching the config back to `$NEWTON_SOURCE_DIR`:
  - `real_usd_native_fitting_conda.json`: `smoke_passed`
  - `real_usd_native_contact_conda.json`: `smoke_passed`
  - `real_usd_native_task_conda.json`: `smoke_passed`

## Review Fixes

- Added empty-role validation so builder APIs cannot return false-positive empty reports.
- Passed configured comparison claim boundaries from CLI into contact/task comparison builders and
  task child reports.
- Replaced the hardcoded Newton source path in the experiment config with `$NEWTON_SOURCE_DIR`.
- Updated stale docs that still described bed/Franka real-USD work as only next-scope.

## Claim Impact

- Supports capped bed and capped Franka first-mesh real-USD diagnostic smoke evidence under the
  recorded config and clean Newton conda environment.
- Does not support native primitive improvement on bed/Franka, because both old and native lanes
  selected boxes.
- Does not support collision-quality validation, benchmark superiority, whole-robot Franka
  collider quality, full CPD reproduction, safety certification, or deployment readiness.

## Next Action

Improve primitive fitting or merge search so real USD assets can actually exercise native
`cylinder`, `cone`, or `ellipsoid` choices before making any native primitive value claim.
