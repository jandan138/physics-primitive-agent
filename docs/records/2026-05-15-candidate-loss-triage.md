# 2026-05-15 Candidate Loss Triage

## Date

2026-05-15

## Status

Complete

## Changes

- Added a `triage` block to `cpd_like_real_usd_candidate_loss_diagnosis`.
- The triage block ranks near-miss extension candidates where box still wins by a small relative
  surrogate-cost margin.
- The triage block also flags low-support native-extension selections, where an extension wins on
  very small face/point support.
- Added `.claude/` to local machine-state ignores.

## Verification

- `python -m pytest -q tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_triages_near_miss_extension_targets` failed before implementation with missing `triage`.
- `python -m pytest -q tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_triages_near_miss_extension_targets` exited 0 with 1 passed after implementation.
- `python -m pytest -q tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_treats_near_equal_extension_cost_as_tie tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_triages_low_support_native_extension tests/test_real_usd_native_comparison.py::test_real_usd_candidate_loss_diagnosis_triages_near_miss_extension_targets` exited 0 with 3 passed after review fixes.
- `python -m pytest -q tests/test_real_usd_native_comparison.py` exited 0 with 15 passed after review fixes.
- `python -m pytest -q tests/test_real_usd_native_comparison.py tests/test_cli.py` exited 0 with 77 passed.
- `python -m pytest -q` exited 0 with 271 passed.
- `python scripts/validate_docs.py` exited 0 with docs validation passed.
- `python scripts/validate_site_claims.py` exited 0 with site claim validation passed.
- `git diff --check` exited 0.

## Artifacts

- `reports/generated/candidate_loss_diagnosis/bed_franka_candidate_loss_diagnosis.json`
- `docs/superpowers/plans/2026-05-15-candidate-loss-triage.md`
- `docs/reference/cpd-latest-diagnostic-loop-explainer.md`

## Result Summary

- Current capped bed triage reports one `cylinder` near-miss target, where the best cylinder is
  about `13%` more expensive than the selected box under the current surrogate.
- Current capped Franka triage reports three low-support `cylinder` selections, each with two
  source faces and four points.
- Current capped Franka triage also reports three `cylinder` near-miss box-selected clusters.

## Claim Impact

This adds deterministic planning metadata for choosing the next synthetic diagnostic target. It
does not add an optimizer, collision-quality evidence, benchmark evidence, whole-robot collider
quality evidence, or full CPD paper reproduction.

## Next Action

Build a synthetic fixture for either the low-support native-extension admissibility target or the
cylinder near-miss fitting target, then make one controlled algorithm change against that fixture.
