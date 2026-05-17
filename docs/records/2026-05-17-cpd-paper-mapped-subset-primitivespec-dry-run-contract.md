# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Dry-Run Contract

## Date

2026-05-17

## Status

Complete

## Changes

- Added `paper_mapped_subset_primitivespec_dry_run_contract` to the partial
  `cpd_paper_offline_report`.
- The new payload consumes only `paper_mapped_subset_adapter_preflight_contract`.
- It records six PrimitiveSpec dry-run requirement rows:
  - OBB maps to future runtime kind `box`;
  - sphere maps to future runtime kind `sphere`;
  - capsule maps to future runtime kind `capsule`;
  - capped cylinder and frustum remain blocked behind an approximation policy;
  - trapezoidal prism remains no-op/offline for current unmapped rows.
- It records 16 current-row dry-run no-op rows, all for `trapezoidal_prism` /
  `offline_only_unmapped`.
- It records zero current PrimitiveSpec candidates, zero generated PrimitiveSpec rows, zero
  generated CollisionPackage rows, and zero runtime-admissibility checks.
- It advances the next gate to `paper_mapped_subset_primitivespec_validation_contract`.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_dry_run or offline_report_next_gate' -q`
  passed with 15 tests selected.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q` passed with 180 tests.
- `python -m pytest -q` passed with 479 tests after copying the ignored paper source fixture into
  the feature worktree.
- `python scripts/validate_docs.py` passed.
- `python scripts/validate_site_claims.py` passed.
- `git diff --check` passed.

## Artifacts

- Code: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- Tests: `tests/test_cpd_paper_offline.py`, `tests/test_cli.py`
- Registry: `experiments/registry.yaml`
- Design: `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md`

## Claim Impact

This supports only a command-only offline PrimitiveSpec dry-run contract over deterministic
synthetic fixture records. It does not support real `PrimitiveSpec` generation, `CollisionPackage`
generation, package readiness, package conversion execution, runtime admissibility, Newton support
or execution, approximation support, real-USD evidence, benchmark evidence, collision-quality
evidence, deployment readiness, or safety certification.

## Next Action

Implement `paper_mapped_subset_primitivespec_validation_contract` as the next offline contract
gate before any real `PrimitiveSpec` or package generation.
