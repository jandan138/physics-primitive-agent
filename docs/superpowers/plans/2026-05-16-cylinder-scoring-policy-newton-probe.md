# Cylinder Scoring Policy Newton Probe Plan

## Task 1: Add RED Tests

**Files:**
- Modify: `tests/test_cpd_like_synthetic.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_cpd_like_config.py`

- [x] Add report-builder tests for `build_cpd_like_cylinder_scoring_policy_newton_probe_report`.
- [x] Add a contact-gated task test: contact pass runs drop/settle and sphere-rain.
- [x] Add a blocked task test: contact failure prevents drop/settle and sphere-rain.
- [x] Add CLI tests for config-required execution and nonzero partial reports.
- [x] Add config ownership test for `configs/experiments/cylinder_scoring_policy_newton_probe.yaml`.

Expected RED: import fails because the new claim constant/report builder and CLI flag do not exist.

## Task 2: Implement Synthetic Newton Probe

**Files:**
- Modify: `src/primitive_collision_compiler/baselines/cpd_like/synthetic.py`

- [x] Add synthetic Newton probe claim/evidence constants.
- [x] Add `build_cpd_like_cylinder_scoring_policy_newton_probe_report`.
- [x] Build the default `box` package and opt-in `cylinder` package for the near-miss fixture.
- [x] Run `run_newton_contact_smoke` first.
- [x] Run `run_newton_drop_settle` and `run_newton_sphere_rain` only when contact passes.
- [x] Return blocked task payloads when contact does not pass.

## Task 3: Add CLI And Config

**Files:**
- Modify: `src/primitive_collision_compiler/cli.py`
- Create: `configs/experiments/cylinder_scoring_policy_newton_probe.yaml`

- [x] Add `--run-cpd-like-cylinder-scoring-policy-newton-probe`.
- [x] Require `--config` and `newton.source_dir`.
- [x] Parse `drop_settle` and `sphere_rain` options from `newton_diagnostic`.
- [x] Emit strict JSON and return 0 only for `smoke_passed`.
- [x] Add a claim-bounded synthetic config example.

## Task 4: Update Docs And Registry

**Files:**
- Create: `docs/records/2026-05-16-cylinder-scoring-policy-newton-probe.md`
- Modify: `docs/records/README.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- Modify: `docs/reference/cpd-like-face-merge-explainer.md`
- Modify: `docs/index.md`
- Modify: `experiments/registry.yaml`

- [x] Add a dated record.
- [x] Add safe and forbidden claim wording.
- [x] Update status explainers and record indexes.
- [x] Add registry entry after the package-probe entry.

## Task 5: Review And Verify

- [x] Request implementation review.
- [x] Request docs/claim-boundary review.
- [x] Fix Critical and Important findings.
- [x] Run focused tests.
- [x] Run a clean-env CLI smoke when Newton source is available.
- [x] Run full tests, docs validation, site claims, and `git diff --check`.
