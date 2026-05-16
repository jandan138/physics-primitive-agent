# CPD Paper Duplicate Vertex Preprocessing Design

## Context

The current `cpd_paper_offline_report` next gate is
`paper_duplicate_vertex_preprocessing_audit`. The CPD paper includes a preprocessing step that
removes overlapped vertices. The method discussion says duplicate vertices can change output
results, and the ablation discussion shows deduplication can change topology and final primitive
counts.

The current report still emits `duplicate_vertex_preprocessing:
not_applied_fixture_has_unique_vertices` for normal toy fixtures. That is correct for those
fixtures, but the paper-lane gap matrix still has no fixture recording what the offline report will
emit when overlapped vertices exist.

## Chosen Approach

Add one deterministic offline fixture, `paper_duplicate_vertex_preprocessing`, that contains two
triangles with distinct vertex ids but exactly overlapping coordinates on one edge. Before
preprocessing, the triangles are disconnected because the `TriangleMesh` adjacency logic is
index-based. After exact-coordinate deduplication, the two faces share a deduplicated edge and are
connected.

This slice records preprocessing as an audit artifact. It does not run package generation, Newton,
real USD, or benchmarks, and it does not claim robust unclean-mesh handling beyond the named
fixture.
It covers exactly overlapped vertices only. It does not cover nonzero distance-threshold
deduplication, approximate spatial hashing, or broad mesh-cleaning policy.

## Fixture

Use a triangle-only source mesh with six input vertices:

```text
v0 = [0, 0, 0]
v1 = [1, 0, 0]
v2 = [0, 1, 0]
v3 = [0, 0, 0]  # duplicate of v0
v4 = [1, 0, 0]  # duplicate of v1
v5 = [0, -1, 0]

f0 = [0, 1, 2]
f1 = [3, 4, 5]
```

Exact-coordinate deduplication should produce four vertices and remap:

```text
original_to_deduplicated_vertex_ids = [0, 1, 2, 0, 1, 3]
deduplicated_faces = [[0, 1, 2], [0, 1, 3]]
```

Expected topology:

- before deduplication: `connected_component_count_before == 2`;
- after deduplication: `connected_component_count_after == 1`;
- duplicate clusters: `[[0, 3], [1, 4]]`;
- dropped degenerate faces: `0`.

Deduplicated vertex ids use first-occurrence ordering over input vertices. The fixture relies on
index-edge adjacency after deduplication; winding is not part of this audit because
`TriangleMesh.adjacent_faces()` treats edges as sorted, orientation-insensitive index pairs.

## Report Behavior

For this fixture, the case payload should include `preprocessing_audit` with:

- `audit_scope: duplicate_vertex_preprocessing_fixture`;
- `preprocessing_policy: exact_coordinate_deduplication_for_fixture`;
- `distance_tolerance: 0.0`;
- `input_vertex_count: 6`;
- `deduplicated_vertex_count: 4`;
- `duplicate_cluster_count: 2`;
- `duplicate_clusters`;
- `original_to_deduplicated_vertex_ids`;
- `input_faces`;
- `deduplicated_faces`;
- `preprocessing_source_face_remap`, with rows:
  - `source_face_id`;
  - `input_vertex_ids`;
  - `deduplicated_vertex_ids`;
  - `face_preserved`;
  - `drop_reason`;
- `retained_source_face_ids`;
- `dropped_source_face_ids`;
- `connected_component_count_before`;
- `connected_component_count_after`;
- `topology_changed: true`;
- `degenerate_face_dropped_count: 0`;
- false package/Newton/real-USD/benchmark triggers.

The case `source_mesh` should make the preprocessing boundary visible:

- `duplicate_vertex_preprocessing: exact_coordinate_deduplication_for_fixture`;
- `vertex_count: 4` for executable geometry after deduplication;
- `preprocessed_input_vertex_count: 6`;
- `deduplicated_vertex_count: 4`;
- `source_face_remap: duplicate_vertex_preprocessing_face_id_preserving`;
- `preprocessing_source_face_remap`, using the same explicit row shape as the audit payload.

The executable `TriangleMesh` used by the rest of the report should be the deduplicated mesh, so
operator, primitive-fit, and topology traces operate on the post-preprocessing geometry. This keeps
one report path and makes the topology change observable.
The fixture must set `priority_queue_target_count: 1` and emit a topology trace that accepts the
merge between faces `[0]` and `[1]`. That trace is the independent evidence that the executable
mesh, not only the audit payload, uses deduplicated adjacency.
Operator, primitive-fit, and topology rows for this case should carry a fixture-scoped
preprocessing boundary field, for example
`preprocessing_boundary: exact_coordinate_duplicate_vertex_fixture`, so those rows are not read as
general unclean-mesh support.

## Gate Advancement

After this slice:

- `failure_labels` should no longer contain `paper_duplicate_vertex_preprocessing_missing`;
- `paper_faithfulness.implemented_fixture_scope` should include
  `paper_duplicate_vertex_preprocessing_audit`;
- `next_required_gate` should advance to `paper_faithful_offline_scope_audit`.
- `status` must remain `partial`;
- `paper_faithful_offline_supported` must remain `false`.

The next gate is intentionally a scope audit, not a runtime/package step. It should decide whether
the named-fixture offline lane is ready for bounded `paper_faithful_offline` wording or whether more
offline breadth is needed.
That scope audit must explicitly check every criterion in the gap matrix and offline lane spec
before allowing any `paper_faithful_offline` wording.

## Tests

Add RED/GREEN tests that verify:

- top-level failure label advances to `paper_faithful_offline_scope_missing`;
- top-level next gate advances to `paper_faithful_offline_scope_audit`;
- the new case is present in the CLI and direct report case order;
- `preprocessing_audit` records before/after vertex counts, duplicate clusters, vertex remap,
  input faces, deduplicated faces, component counts before/after, and `topology_changed: true`;
- `source_mesh` mirrors the preprocessing boundary;
- `collapse_trace` for the new case has `initial_edge_count == 1`, accepts the merge from `[0]` and
  `[1]`, and reaches `final_active_groups == [[0, 1]]`;
- operator, primitive-fit, and topology rows for this case carry the exact-coordinate fixture
  preprocessing boundary;
- top-level `status` remains `partial` and `paper_faithful_offline_supported` remains `false`;
- no degenerate faces are dropped in this fixture;
- package/Newton/real-USD/benchmark triggers stay false.

## Documentation And Records

Update:

- `docs/index.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- a new dated record under `docs/records/`.

The wording must stay bounded: this is exact-coordinate preprocessing audit on one deterministic
synthetic fixture, not robust arbitrary mesh cleanup, not full CPD reproduction, not Newton runtime
support, not package generation, not real-USD evidence, and not benchmark or collision-quality
evidence.
The registry entry must preserve the same audit-fixture-only wording and explicitly reject
benchmark and collision-quality evidence claims.

## Verification

Required verification:

- focused RED/GREEN pytest for duplicate-vertex preprocessing assertions and CLI JSON case order;
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`;
- `python -m pytest -q`;
- `python scripts/validate_docs.py`;
- `python scripts/validate_site_claims.py`;
- `git diff --check`.
