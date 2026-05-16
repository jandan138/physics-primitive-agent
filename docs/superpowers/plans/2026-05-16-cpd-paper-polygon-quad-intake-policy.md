# CPD Paper Polygon/Quad Intake Policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic offline quad/polygon source-face intake policy audit rows to
`cpd_paper_offline_report`.

**Architecture:** Keep executable geometry as `TriangleMesh`, but add explicit source-face intake
metadata for two new toy fixtures. The report records fan triangulation, source-face remap,
operator ownership, and claim boundaries without generating packages or invoking Newton.

**Tech Stack:** Python, pytest, Markdown docs, YAML registry, existing CPD paper offline report
helpers.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [x] Assert top-level `failure_labels == ["paper_obb_sphere_fit_faithfulness_missing"]`.
- [x] Assert `next_required_gate == "paper_obb_sphere_fit_faithfulness_audit"`.
- [x] Assert `paper_polygon_quad_intake_policy_audit` is present in
  `paper_faithfulness.implemented_fixture_scope`.
- [x] Assert report status boundaries still hold:
  - `status == "partial"`;
  - `paper_faithful_offline_supported is False`;
  - `paper_faithfulness.status == "partial"`.
- [x] Assert report cases include `paper_quad_face_intake` and `paper_polygon_face_intake` while
  preserving all existing cases.
- [x] Assert `paper_quad_face_intake["source_mesh"]` records:
  - `face_arity_policy == "fan_triangulate_non_triangle_faces_preserve_source_face_remap"`;
  - `source_face_count == 1`;
  - `source_face_arities == [4]`;
  - `triangulated_face_count == 2`;
  - `executable_triangle_face_count == 2`;
  - `face_count == 2`;
  - `executable_triangle_faces == [[0, 1, 2], [0, 2, 3]]`;
  - `source_face_remap == [{"source_face_id": 0, "source_face_arity": 4, "source_vertex_ids": [0, 1, 2, 3], "generated_triangle_face_ids": [0, 1], "generated_triangle_vertex_ids": [[0, 1, 2], [0, 2, 3]]}]`;
  - `operator_ownership_policy == "triangulated_subfaces_summed_to_source_face"`;
  - `source_face_preconditions == ["planar", "convex", "non_degenerate", "consistently_wound"]`.
- [x] Assert `paper_polygon_face_intake["source_mesh"]` records:
  - `source_face_arities == [5]`;
  - `triangulated_face_count == 3`;
  - `executable_triangle_face_count == 3`;
  - `face_count == 3`;
  - `executable_triangle_faces == [[0, 1, 2], [0, 2, 3], [0, 3, 4]]`;
  - `source_face_remap == [{"source_face_id": 0, "source_face_arity": 5, "source_vertex_ids": [0, 1, 2, 3, 4], "generated_triangle_face_ids": [0, 1, 2], "generated_triangle_vertex_ids": [[0, 1, 2], [0, 2, 3], [0, 3, 4]]}]`.
- [x] Assert each new case has `mesh_intake_policy_audit` with:
  - `audit_scope == "polygon_quad_source_face_intake_policy_fixture"`;
  - source-face count, source-face arities, triangulated face count, executable triangle face
    count, source-face remap, and source-face preconditions matching `source_mesh`;
  - `source_face_policy == "preserve_source_face_id_after_fan_triangulation"`;
  - `triangulation_policy == "fan_from_first_vertex"`;
  - `operator_ownership_policy == "triangulated_subfaces_summed_to_source_face"`;
  - `normal_policy == "triangle_normals_area_weighted_after_fan_triangulation"`;
  - `tangent_policy == "triangle_edge_tangents_area_weighted_after_fan_triangulation"`;
  - `package_generation_triggered is False`;
  - `newton_runtime_triggered is False`;
  - `real_usd_triggered is False`;
  - `benchmark_triggered is False`.
- [x] Assert each new case's `operator_audit.face_scope` remains `triangle_subfaces_from_source_face`.
- [x] Assert each new case's `operator_audit.source_face_operator_aggregates` records source face
  `0`, generated triangle ids `[0, 1]` for the quad and `[0, 1, 2]` for the polygon, and a
  `q_matrix` that equals the elementwise sum of the listed generated triangle face `q_matrix`
  values.
- [x] Assert each new case's `operator_audit.merged_group.source_faces` and
  `primitive_fit_audit.source_faces` equal the original source face ids: `[0]`.
- [x] Assert each new case's `operator_audit.merged_group.generated_triangle_face_ids`,
  `operator_audit.merged_group.source_face_ids`, `primitive_fit_audit.generated_triangle_face_ids`,
  and `primitive_fit_audit.source_face_ids` disambiguate generated triangle ids from original
  source face ids:
  - quad generated triangle ids `[0, 1]` and source face ids `[0]`;
  - polygon generated triangle ids `[0, 1, 2]` and source face ids `[0]`.
- [x] Update the CLI JSON test expected case list to this exact order:
  - `paper_single_box`;
  - `paper_two_face_merge`;
  - `paper_three_face_chain`;
  - `paper_disconnected_components`;
  - `paper_component_pair_threshold_blocked`;
  - `paper_frustum_like`;
  - `paper_trapezoid_prism_like`;
  - `paper_nested_primitive`;
  - `paper_quad_face_intake`;
  - `paper_polygon_face_intake`.
- [x] Make the RED assertions observable with separate independent tests:
  - one test for exact top-level `failure_labels`;
  - one test for exact top-level `next_required_gate`;
  - one test for new quad/polygon fixture payloads.
  Do not rely on one long test stopping at the first old-report mismatch.
- [x] Run:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_polygon_quad_intake_policy tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  and confirm the failure-label, next-gate, fixture-payload, and CLI case-list failures are each
  visible.
- [x] Run the new fixture-specific test and confirm it fails for missing `paper_quad_face_intake`
  and `paper_polygon_face_intake`.

### Task 2: Intake Policy Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [x] Add frozen dataclasses `_SourceFaceRemap` and `_SourceFaceIntakeAudit` with typed immutable
  fields:
  - `_SourceFaceRemap.source_face_id: int`;
  - `_SourceFaceRemap.source_face_arity: int`;
  - `_SourceFaceRemap.source_vertex_ids: tuple[int, ...]`;
  - `_SourceFaceRemap.generated_triangle_face_ids: tuple[int, ...]`;
  - `_SourceFaceRemap.generated_triangle_vertex_ids: tuple[tuple[int, int, int], ...]`;
  - `_SourceFaceIntakeAudit.source_face_arities: tuple[int, ...]`;
  - `_SourceFaceIntakeAudit.source_face_remap: tuple[_SourceFaceRemap, ...]`;
  - `face_arity_policy: str = "fan_triangulate_non_triangle_faces_preserve_source_face_remap"`;
  - `operator_ownership_policy: str = "triangulated_subfaces_summed_to_source_face"`.
- [x] Extend `_PaperToyCase` with `source_face_intake_audit: _SourceFaceIntakeAudit | None = None`.
- [x] Add `_quad_face_intake_mesh()` returning a two-triangle square fan mesh.
- [x] Add `_polygon_face_intake_mesh()` returning a three-triangle pentagon fan mesh.
- [x] Add `_source_face_intake_audit_payload(audit)` returning the `mesh_intake_policy_audit`
  fields required by tests.
- [x] Update `_source_mesh_payload(mesh, source_face_intake_audit=None)` so existing triangle-only
  fixtures are unchanged, and non-triangle fixtures add the source-face policy fields.
- [x] Update `_operator_audit_payload(mesh, face_groups, source_face_intake_audit=None)` so
  `face_scope` is `triangle_subfaces_from_source_face` only for the new fixtures.
- [x] Add `_source_face_operator_aggregates(mesh, source_face_intake_audit)` and include aggregate
  source-face rows in `operator_audit` only for the new fixtures.
- [x] Add generated/source id disambiguation fields to group-level payloads for new fixtures:
  `generated_triangle_face_ids` and `source_face_ids`.
- [x] Attach `mesh_intake_policy_audit` only when `case.source_face_intake_audit` is present.
- [x] Add `paper_quad_face_intake` and `paper_polygon_face_intake` to `_paper_toy_cases()`.
- [x] Replace `polygon_and_quad_face_policy` in `missing_before_paper_faithful` with
  `paper_obb_sphere_fit_faithfulness`.
- [x] Set `next_required_gate` to `paper_obb_sphere_fit_faithfulness_audit`.
- [x] Add `paper_polygon_quad_intake_policy_audit` to implemented fixture scope.
- [x] Run the RED test and confirm it passes.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-polygon-quad-intake-policy.md`

- [x] Update current paper-lane wording to say one quad and one five-vertex polygon intake policy
  fixture are recorded.
- [x] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [x] Make `paper_obb_sphere_fit_faithfulness_audit` the next gate.
- [x] Define the remaining `paper_obb_sphere_fit_faithfulness_missing` label in the gap matrix and
  lane spec.
- [x] Add an `experiments/registry.yaml` entry:
  - `id: cpd-paper-polygon-quad-intake-policy`;
  - `status: complete`;
  - `command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`;
  - `record: docs/records/2026-05-16-cpd-paper-polygon-quad-intake-policy.md`;
  - purpose describing the command-only partial offline source-face intake policy audit;
  - claims supported limited to fixture-scoped offline intake policy only, with explicit no
    `paper_faithful_offline`, full CPD reproduction, Newton runtime, package-generation, real-USD,
    collision-quality, benchmark, deployment, or safety-certification claim.
- [x] Keep package generation, Newton, real USD, benchmark, and collision-quality claims out of
  scope.
- [x] Add dated verification and multi-agent review notes.

### Task 4: Verification And Review

- [x] Run focused pytest for CPD paper offline and CLI report tests.
- [x] Run CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`.
- [x] Run `python -m pytest -q`.
- [x] Run `python scripts/validate_docs.py`.
- [x] Run `python scripts/validate_site_claims.py`.
- [x] Run `git diff --check`.
- [x] Request multi-agent review for mesh-intake policy schema, docs/claim boundaries, and test
  coverage.
- [x] Fix Critical/Important review findings before commit.

### Task 5: Commit

- [x] Commit with message `feat: audit CPD paper polygon quad intake policy`.
- [x] Push `main`.
- [x] Confirm `git status --short` is clean.
