# CPD Paper Duplicate Vertex Preprocessing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fixture-scoped duplicate/overlapped vertex preprocessing audit to
`cpd_paper_offline_report`.

**Architecture:** Keep the report command offline-only. Add one exact-coordinate duplicate-vertex
toy fixture whose executable mesh is deduplicated before operator, primitive-fit, and topology
audits run. Record before/after vertex ids, duplicate clusters, face remap, topology change, and
claim boundaries without generating packages or invoking Newton.

**Tech Stack:** Python, NumPy, pytest, Markdown docs, YAML registry.

---

### Task 1: RED Tests

**Files:**

- Modify: `tests/test_cpd_paper_offline.py`
- Modify: `tests/test_cli.py`

- [ ] Update top-level direct-report tests to expect:

```python
assert report["failure_labels"] == ["paper_faithful_offline_scope_missing"]
assert report["next_required_gate"] == "paper_faithful_offline_scope_audit"
assert report["status"] == "partial"
assert report["paper_faithful_offline_supported"] is False
```

- [ ] Assert `paper_duplicate_vertex_preprocessing_audit` is present in
  `report["paper_faithfulness"]["implemented_fixture_scope"]`.

- [ ] Add `paper_duplicate_vertex_preprocessing` to the expected case set and CLI case order after
  `paper_tiny_sphere_clamp`.

- [ ] Add direct-report assertions for `paper_duplicate_vertex_preprocessing`:

```python
case = cases["paper_duplicate_vertex_preprocessing"]
audit = case["preprocessing_audit"]
assert audit["audit_scope"] == "duplicate_vertex_preprocessing_fixture"
assert audit["preprocessing_policy"] == "exact_coordinate_deduplication_for_fixture"
assert audit["distance_tolerance"] == 0.0
assert audit["input_vertex_count"] == 6
assert audit["deduplicated_vertex_count"] == 4
assert audit["duplicate_cluster_count"] == 2
assert audit["duplicate_clusters"] == [[0, 3], [1, 4]]
assert audit["original_to_deduplicated_vertex_ids"] == [0, 1, 2, 0, 1, 3]
assert audit["input_faces"] == [[0, 1, 2], [3, 4, 5]]
assert audit["deduplicated_faces"] == [[0, 1, 2], [0, 1, 3]]
assert audit["connected_component_count_before"] == 2
assert audit["connected_component_count_after"] == 1
assert audit["topology_changed"] is True
assert audit["degenerate_face_dropped_count"] == 0
assert audit["retained_source_face_ids"] == [0, 1]
assert audit["dropped_source_face_ids"] == []
assert audit["preprocessing_source_face_remap"] == [
    {
        "source_face_id": 0,
        "input_vertex_ids": [0, 1, 2],
        "deduplicated_vertex_ids": [0, 1, 2],
        "face_preserved": True,
        "drop_reason": None,
    },
    {
        "source_face_id": 1,
        "input_vertex_ids": [3, 4, 5],
        "deduplicated_vertex_ids": [0, 1, 3],
        "face_preserved": True,
        "drop_reason": None,
    },
]
assert audit["package_generation_triggered"] is False
assert audit["newton_runtime_triggered"] is False
assert audit["real_usd_triggered"] is False
assert audit["benchmark_triggered"] is False
```

- [ ] Assert `source_mesh` mirrors the preprocessing boundary:

```python
source_mesh = case["source_mesh"]
assert source_mesh["duplicate_vertex_preprocessing"] == "exact_coordinate_deduplication_for_fixture"
assert source_mesh["preprocessed_input_vertex_count"] == 6
assert source_mesh["deduplicated_vertex_count"] == 4
assert source_mesh["vertex_count"] == 4
assert source_mesh["source_face_remap"] == (
    "duplicate_vertex_preprocessing_face_id_preserving"
)
assert source_mesh["preprocessing_source_face_remap"] == [
    {
        "source_face_id": 0,
        "input_vertex_ids": [0, 1, 2],
        "deduplicated_vertex_ids": [0, 1, 2],
        "face_preserved": True,
        "drop_reason": None,
    },
    {
        "source_face_id": 1,
        "input_vertex_ids": [3, 4, 5],
        "deduplicated_vertex_ids": [0, 1, 3],
        "face_preserved": True,
        "drop_reason": None,
    },
]
```

- [ ] Assert the deduplicated executable mesh is used by the topology trace:

```python
trace = case["collapse_trace"]
assert trace["preprocessing_boundary"] == "exact_coordinate_duplicate_vertex_fixture"
assert trace["initial_edge_count"] == 1
assert trace["accepted_merge_count"] == 1
assert trace["final_active_groups"] == [[0, 1]]
assert trace["events"][0]["source_faces_left"] == [0]
assert trace["events"][0]["source_faces_right"] == [1]
assert trace["events"][0]["resulting_source_faces"] == [0, 1]
```

- [ ] Assert operator and primitive-fit rows carry the fixture boundary:

```python
assert case["operator_audit"]["preprocessing_boundary"] == (
    "exact_coordinate_duplicate_vertex_fixture"
)
assert case["primitive_fit_audit"]["preprocessing_boundary"] == (
    "exact_coordinate_duplicate_vertex_fixture"
)
```

- [ ] Assert the case-level flags remain false:

```python
assert case["package_generation_triggered"] is False
assert case["newton_runtime_triggered"] is False
assert case["real_usd_triggered"] is False
assert case["benchmark_triggered"] is False
```

- [ ] Strengthen `tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json` to assert the
  CLI payload includes the new case and the preprocessing audit keys above.

- [ ] Run:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_duplicate_vertex_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_duplicate_vertex_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q
```

Expected: failures for the old duplicate-vertex failure label, old next gate, missing implemented
scope entry, missing case, and missing preprocessing payload.

### Task 2: Duplicate Vertex Audit Implementation

**Files:**

- Modify: `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`

- [ ] Add frozen dataclass `_DuplicateVertexPreprocessingAudit`:

```python
@dataclass(frozen=True)
class _DuplicateVertexPreprocessingAudit:
    input_points: tuple[tuple[float, float, float], ...]
    input_faces: tuple[tuple[int, int, int], ...]
    deduplicated_points: tuple[tuple[float, float, float], ...]
    deduplicated_faces: tuple[tuple[int, int, int], ...]
    original_to_deduplicated_vertex_ids: tuple[int, ...]
    duplicate_clusters: tuple[tuple[int, ...], ...]
    distance_tolerance: float = 0.0
```

- [ ] Extend `_PaperToyCase` with:

```python
duplicate_vertex_preprocessing_audit: _DuplicateVertexPreprocessingAudit | None = None
```

- [ ] Add `_duplicate_vertex_preprocessing_audit()` returning the exact fixture from the spec.
  Deduplicated vertex ids must use first-occurrence ordering over input vertices.

- [ ] Add `_duplicate_vertex_preprocessing_mesh()` returning a `TriangleMesh` from the audit's
  deduplicated points and faces.

- [ ] Add `_preprocessing_audit_payload(audit)` emitting all test-required fields and false trigger
  flags.

- [ ] Add `_duplicate_vertex_source_face_remap(audit)` returning the two source-face remap rows.

- [ ] Update `_source_mesh_payload(mesh, ..., duplicate_vertex_preprocessing_audit=None)`:
  - leave existing fixtures unchanged;
  - when audit exists, set `duplicate_vertex_preprocessing`,
    `preprocessed_input_vertex_count`, `deduplicated_vertex_count`, and source-face remap.

- [ ] Update `_case_payload(case)` to pass the audit into `_source_mesh_payload` and attach
  `preprocessing_audit`.

- [ ] Add `_PaperToyCase(case_id="paper_duplicate_vertex_preprocessing", ...)` after
  `paper_tiny_sphere_clamp`. Set `priority_queue_target_count=1` so the topology trace proves the
  deduplicated executable mesh is connected.

- [ ] Advance top-level report state:

```python
missing_before_paper_faithful = ["paper_faithful_offline_scope"]
"next_required_gate": "paper_faithful_offline_scope_audit"
"paper_duplicate_vertex_preprocessing_audit" in implemented_fixture_scope
```

- [ ] Run the RED command from Task 1 again.

Expected: all selected tests pass.

### Task 3: Docs, Registry, And Record

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/records/README.md`
- Modify: `experiments/registry.yaml`
- Create: `docs/records/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md`

- [ ] Update current paper-lane wording to include `paper_duplicate_vertex_preprocessing`.
- [ ] Keep `status: partial` and `paper_faithful_offline_supported: false`.
- [ ] Add `paper_faithful_offline_scope_missing` as the current failure label.
- [ ] Make `paper_faithful_offline_scope_audit` the next gate.
- [ ] Add a registry entry:

```yaml
- id: cpd-paper-duplicate-vertex-preprocessing
  status: complete
  command: PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
  record: docs/records/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md
```

Claims must be limited to fixture-scoped exact-coordinate duplicate-vertex preprocessing audit, with
no nonzero distance-threshold deduplication, approximate spatial hashing, general mesh cleanup,
`paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime, real-USD,
benchmark, collision-quality, deployment, or safety-certification claim.
The registry entry must preserve audit-fixture-only wording and explicitly reject benchmark and
collision-quality evidence claims.

- [ ] Create the dated record with RED/GREEN commands, CLI smoke, multi-agent review notes, final
  verification commands, claim impact, and next action `paper_faithful_offline_scope_audit`.

### Task 4: Verification And Review

- [ ] Run focused pytest:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q
```

- [ ] Run CLI smoke:

```bash
python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report
```

- [ ] Run full verification:

```bash
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] Request multi-agent implementation review for:
  - dedup/topology correctness;
  - test coverage and report schema clarity;
  - docs and claim-boundary consistency.

- [ ] Fix all Critical and Important review findings, then rerun relevant focused tests and final
  verification commands.

### Task 5: Commit And Push

- [ ] Commit the spec and plan checkpoint:

```bash
git add docs/superpowers/specs/2026-05-16-cpd-paper-duplicate-vertex-preprocessing-design.md docs/superpowers/plans/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md
git commit -m "docs: plan CPD paper duplicate vertex preprocessing"
```

- [ ] Commit implementation after review and verification:

```bash
git add src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py docs/index.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-story-status.md docs/records/README.md docs/records/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md experiments/registry.yaml docs/superpowers/plans/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md
git commit -m "feat: audit CPD paper duplicate vertex preprocessing"
```

- [ ] Push and confirm clean status:

```bash
git push
git status --short
```
