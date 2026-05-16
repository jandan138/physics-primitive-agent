# CPD Paper Polygon/Quad Intake Policy Design

## Context

The partial `cpd_paper_offline_report` now covers the first paper-side toy mechanics through
operator audit, primitive-fit audit rows, collapse-cost fields, priority-queue traces,
component-pair accepted/blocked events, and one enclosed-primitive postprocess cull audit. The
current top-level remaining failure label is `polygon_and_quad_face_policy_missing`, and the next
required gate is `paper_polygon_quad_intake_policy_audit`.

The current implementation uses `TriangleMesh`, so all executable geometry is triangle-only. That
is acceptable for a first offline lane only if the report explicitly documents how source quad and
polygon faces are converted into triangle subfaces and how source-face ownership is preserved for
paper-side accounting.

## Goal

Add a deterministic fixture-scoped polygon/quad intake policy audit to
`cpd_paper_offline_report`.

## Scope

- Add two synthetic source-face fixtures:
  - `paper_quad_face_intake`: one quad source face.
  - `paper_polygon_face_intake`: one five-vertex polygon source face.
- Keep the executable mesh as `TriangleMesh`.
- Record the original source face arity, the fan triangulation policy, and a source-face remap from
  original source face id to generated triangle face ids and generated triangle vertex triples.
- Record that operator ownership for non-triangle input is currently
  `triangulated_subfaces_summed_to_source_face`.
- Restrict this first fixture to planar, convex, non-degenerate, consistently wound source faces so
  fan triangulation has an unambiguous review target.
- Record package/Newton/real-USD/benchmark trigger boundaries as false.

## Non-Scope

- No general polygon mesh data structure.
- No USD real-asset rerun.
- No package generation.
- No Newton runtime invocation.
- No benchmark, speed, or collision-quality claim.
- No proof that fan triangulation is the paper's preferred polygon operator.
- No full `paper_faithful_offline` upgrade.

## Design

Extend `_PaperToyCase` with optional source-face intake metadata. Existing triangle fixtures keep
their current `triangle_only_fixture` source payload. The new quad/polygon fixtures use explicit
source metadata and a deterministic fan triangulation:

```text
source face: [v0, v1, v2, v3]
triangles: [v0, v1, v2], [v0, v2, v3]

source face: [v0, v1, v2, v3, v4]
triangles: [v0, v1, v2], [v0, v2, v3], [v0, v3, v4]
```

The source mesh payload should continue to include the existing fields and add policy-specific
fields for these fixtures:

```text
face_arity_policy: fan_triangulate_non_triangle_faces_preserve_source_face_remap
source_face_count: 1
source_face_arities: [4] or [5]
triangulated_face_count: 2 or 3
source_face_remap:
  - source_face_id: 0
    source_face_arity: 4 or 5
    source_vertex_ids: [...]
    generated_triangle_face_ids: [...]
    generated_triangle_vertex_ids: [...]
executable_triangle_face_count: 2 or 3
operator_ownership_policy: triangulated_subfaces_summed_to_source_face
normal_policy: triangle_normals_area_weighted_after_fan_triangulation
tangent_policy: triangle_edge_tangents_area_weighted_after_fan_triangulation
source_face_preconditions:
  - planar
  - convex
  - non_degenerate
  - consistently_wound
```

Each new case should also include a `mesh_intake_policy_audit` payload with the same policy details
and explicit false runtime triggers. This makes the policy easy to review without overloading the
generic `source_mesh` fields.

The operator audit should make the source-face aggregate explicit:

```text
face_scope: triangle_subfaces_from_source_face
source_face_operator_aggregates:
  - source_face_id: 0
    generated_triangle_face_ids: [...]
    q_matrix: sum of generated triangle q_matrix values
```

The primitive-fit audit should still operate on generated triangle face ids for the executable
`TriangleMesh`, but the mesh-intake policy audit records that those generated ids belong to source
face `0`. For the new fixtures, the relevant group-level payloads should expose both
`generated_triangle_face_ids` and `source_face_ids` so `source_faces` cannot be misread as original
source polygon ids.

## Report And Claim Boundary

After this slice, `polygon_and_quad_face_policy_missing` should be removed. The report should still
remain `status: partial` with `paper_faithful_offline_supported: false`.

Because the current OBB/sphere rows are still labeled as current surrogates and the paper-lane
primitive construction remains partial, the next gate should become
`paper_obb_sphere_fit_faithfulness_audit`, and the report should carry
`paper_obb_sphere_fit_faithfulness_missing`.

This is intentionally conservative: the polygon/quad policy gap is closed, but the project still
does not claim `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
package generation, real-USD evidence, benchmark evidence, or collision-quality validation.

## Verification

- RED/GREEN tests for `paper_quad_face_intake` and `paper_polygon_face_intake`.
- Preserve all existing paper offline fixtures.
- CLI smoke for `--run-cpd-paper-offline-report`.
- `python -m pytest -q`.
- `python scripts/validate_docs.py`.
- `python scripts/validate_site_claims.py`.
- `git diff --check`.
