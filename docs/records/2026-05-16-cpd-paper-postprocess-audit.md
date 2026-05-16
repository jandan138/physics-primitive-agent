# 2026-05-16 CPD Paper Postprocess Audit

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_nested_primitive`, a deterministic toy fixture for offline enclosed-primitive
  postprocess accounting.
- Added explicit postprocess input rows for two identity-axis `oriented_bounding_box` primitives:
  an outer primitive with half extents `[1, 1, 1]` and an inner primitive with half extents
  `[0.25, 0.25, 0.25]`.
- Recorded one cull record where primitive `1` is enclosed by primitive `0`, with eight tested
  inner corners and `primitive_enclosed_by_larger_primitive` as the cull reason.
- Removed `postprocess_enclosed_primitive_culling_missing` from the partial paper-lane failure
  labels.
- Advanced the next paper-lane gate to `paper_polygon_quad_intake_policy_audit`.
- Extended `scripts/validate_docs.py` so docs validation now checks experiment registry record
  targets, complete record status, and basic claim-boundary presence for complete registry entries.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed in the RED step for the old `postprocess_enclosed_primitive_culling_missing` label and
  the missing `paper_nested_primitive` case.
- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 2 tests after implementation.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 6 tests.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` emitted JSON with
  `status: partial`, `failure_labels: ["polygon_and_quad_face_policy_missing"]`,
  `next_required_gate: paper_polygon_quad_intake_policy_audit`, `paper_nested_primitive`,
  `postprocess_enclosed_primitive_culling_audit`, input primitive count `2`, output primitive
  count `1`, culled primitive id `[1]`, kept primitive id `[0]`, and no package, Newton, real-USD,
  or benchmark trigger.
- `python -m pytest -q` initially failed because `docs/index.md` and `docs/records/README.md`
  referenced this record before the file existed. This record file fixed the missing-link root
  cause.
- `python -m pytest -q` passed with 414 tests after final review fixes.
- `python scripts/validate_docs.py` passed after adding registry/record consistency checks.
- `python scripts/validate_site_claims.py` passed.
- `python -m pytest tests/test_docs_validation.py tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice -q`
  passed with 7 tests after adding registry validation tests and exact failure-label coverage.
- `git diff --check` passed with no output.

## Multi-Agent Review

- Design review found no Critical issues. Important fixes were applied before implementation:
  identity axes were made explicit, the postprocess input source was recorded as explicit audit
  primitives rather than search output, and cross-field consistency tests were added to the plan.
- Documentation and claim-boundary review found no Critical or Important issues after the plan
  update. The next `paper_polygon_quad_intake_policy_audit` gate was required to be defined in the
  lane spec and gap matrix.
- Final documentation review found two Important stale-doc issues: the gap matrix still referenced
  postprocess as future work, and the command index omitted `paper_nested_primitive`. Both were
  fixed before commit.
- Final test/registry review found one Important coverage issue: docs validation did not actually
  check registry/record consistency. The validator and tests were extended before commit.
- Re-review of both Important fixes found no remaining Critical, Important, or Minor issues.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_docs_validation.py`
- `tests/test_cli.py`
- `scripts/validate_docs.py`
- `docs/index.md`
- `docs/records/README.md`
- `docs/records/2026-05-15-low-support-native-extension-admissibility.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-postprocess-audit-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-postprocess-audit.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only enclosed-primitive postprocess cull audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, general primitive
  containment, Newton runtime support, package generation, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The report remains `status: partial` with `paper_faithful_offline_supported: false`.

## Next Action

- Define `paper_polygon_quad_intake_policy_audit` for triangle, quad, and higher-arity polygon
  intake before stronger paper-lane wording.
