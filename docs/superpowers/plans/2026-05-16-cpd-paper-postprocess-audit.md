# CPD Paper Postprocess Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic offline enclosed-primitive postprocess audit to
`cpd_paper_offline_report`.

**Architecture:** Add one explicit toy postprocess fixture and a small postprocess payload helper.
The helper records culling accounting only; it does not generate collision packages or invoke
Newton.

**Tech Stack:** Python, pytest, Markdown docs, existing CPD paper offline report helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Add assertions that `postprocess_enclosed_primitive_culling_missing` is no longer in
  `failure_labels`, while `polygon_and_quad_face_policy_missing` remains.
- [ ] Assert `next_required_gate == "paper_polygon_quad_intake_policy_audit"`.
- [ ] Assert `postprocess_enclosed_primitive_culling_audit` is present in
  `paper_faithfulness.implemented_fixture_scope`.
- [ ] Assert report cases include `paper_nested_primitive`.
- [ ] Assert `paper_nested_primitive` case-level trigger fields are false:
  - `package_generation_triggered is False`;
  - `newton_runtime_triggered is False`;
  - `real_usd_triggered is False`;
  - `benchmark_triggered is False`.
- [ ] Assert `paper_nested_primitive["postprocess_audit"]` records:
  - `audit_scope == "enclosed_primitive_culling_fixture"`;
  - `postprocess_input_source == "explicit_audit_primitives_not_search_trace"`;
  - `postprocess_policy == "remove_primitives_enclosed_by_another_primitive"`;
  - `containment_test_type == "obb_corners_inside_obb"`;
  - `axis_policy == "shared_identity_axes"`;
  - `input_primitive_count == 2`;
  - `output_primitive_count == 1`;
  - `enclosed_primitive_ids == [1]`;
  - `enclosing_primitive_ids == [0]`;
  - `culled_primitive_ids == [1]`;
  - `kept_primitive_ids == [0]`;
  - no package, Newton, real USD, or benchmark trigger.
- [ ] Assert top-level status boundaries still hold:
  - `status == "partial"`;
  - `paper_faithful_offline_supported is False`;
  - `paper_faithfulness.status == "partial"`.
- [ ] Assert `input_primitives` contains two OBB rows:
  - outer primitive id `0`, kind `oriented_bounding_box`, center `[0, 0, 0]`, half extents
    `[1, 1, 1]`, and identity axes `[[1, 0, 0], [0, 1, 0], [0, 0, 1]]`;
  - inner primitive id `1`, kind `oriented_bounding_box`, center `[0, 0, 0]`, half extents
    `[0.25, 0.25, 0.25]`, and identity axes `[[1, 0, 0], [0, 1, 0], [0, 0, 1]]`.
- [ ] Assert `cull_records` contains exactly one row:
  - `culled_primitive_id == 1`;
  - `enclosing_primitive_id == 0`;
  - `cull_reason == "primitive_enclosed_by_larger_primitive"`;
  - `containment_passed is True`;
  - `tested_corner_count == 8`.
- [ ] Assert cross-field consistency:
  - `len(input_primitives) == input_primitive_count`;
  - `len(kept_primitive_ids) == output_primitive_count`;
  - `culled_primitive_ids` matches the culled ids in `cull_records`;
  - `enclosed_primitive_ids` and `enclosing_primitive_ids` match the cull record ids.
- [ ] Update the CLI JSON test expected case list to include `paper_nested_primitive`.
- [ ] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  and confirm it fails for the missing postprocess behavior.

### Task 2: Postprocess Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Extend `_PaperToyCase` with `postprocess_fixture: bool = False`.
- [ ] Add `paper_nested_primitive` using a tiny box-like mesh and `postprocess_fixture=True`.
- [ ] Add `_nested_primitive_mesh()` with a simple triangle-only cuboid or reuse the asymmetric
  cuboid mesh if that keeps source-mesh accounting simple.
- [ ] Add `_postprocess_audit_payload()` returning the explicit two-OBB culling audit.
- [ ] Add `_obb_corners(center, half_extents, axes)` helper for the eight inner corners.
- [ ] Add `_obb_contains_points(center, half_extents, axes, points)` for the identity-axis fixture.
- [ ] Attach `postprocess_audit` only when `case.postprocess_fixture` is true.
- [ ] Remove `postprocess_enclosed_primitive_culling` from `missing_before_paper_faithful`.
- [ ] Set `next_required_gate` to `paper_polygon_quad_intake_policy_audit`.
- [ ] Add `postprocess_enclosed_primitive_culling_audit` to implemented fixture scope.
- [ ] Run the RED test and confirm it passes.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-postprocess-audit.md`

- [ ] Update current paper-lane wording to say one toy postprocess cull is recorded.
- [ ] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [ ] Make polygon/quad intake policy the next gate.
- [ ] Define `paper_polygon_quad_intake_policy_audit` in the lane spec and gap matrix, including
  its remaining failure label and partial-status boundary.
- [ ] Keep package generation, Newton, real USD, benchmark, and collision-quality claims out of
  scope.
- [ ] Add dated verification and multi-agent review notes.

### Task 4: Verification And Review

- [ ] Run focused pytest for CPD paper offline and CLI report tests.
- [ ] Run CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/validate_docs.py`.
- [ ] Run `python scripts/validate_site_claims.py`.
- [ ] Run `git diff --check`.
- [ ] Request multi-agent review for postprocess algorithm, docs/claim boundaries, and report schema.
- [ ] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [ ] Commit with message `feat: audit CPD paper postprocess culling`.
- [ ] Push `main`.
- [ ] Confirm `git status --short` is clean.
