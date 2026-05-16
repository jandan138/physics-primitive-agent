from __future__ import annotations

from dataclasses import dataclass
from math import pi

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.baselines.cpd_like.primitives import (
    MIN_DIMENSION,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh

CPD_PAPER_OFFLINE_CLAIM_BOUNDARY = (
    "fixture_scoped_cpd_paper_offline_report_not_runtime_or_benchmark"
)
CPD_PAPER_OFFLINE_EVIDENCE_LEVEL = "offline_cpd_paper_toy_fixture_audit"
CPD_PAPER_OFFLINE_STATUS_SEMANTICS = (
    "fixture_scoped_paper_mechanics_audit_not_full_reproduction"
)
PAPER_Q_EPSILON = 1e-6
PAPER_PRIMITIVE_MIN_DIMENSION = 1e-3
PAPER_PRIMITIVE_WEIGHTS = {
    "oriented_bounding_box": 1.0,
    "sphere": 1.0,
    "capsule": 1.0,
    "capped_cylinder": 1.05,
    "frustum": 2.1,
    "trapezoidal_prism": 1.4,
}
_AUDITED_PAPER_PRIMITIVES = (
    "oriented_bounding_box",
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
)
_PAPER_PRIMITIVE_NAMES = {
    "box": "oriented_bounding_box",
    "sphere": "sphere",
}
_NEWTON_RUNTIME_KIND = {
    "box": "box",
    "sphere": "sphere",
}
_SCOPE_AUDIT_ALLOWED_STATUSES = {
    "implemented_fixture_scope",
    "partial_fixture_scope",
    "not_started",
    "blocked_until_later_gate",
}
_SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS = {
    "fixture_scoped_paper_shaped",
    "paper_aligned_boundary",
    "not_paper_faithful",
    "out_of_offline_scope",
}


@dataclass(frozen=True)
class _SourceFaceRemap:
    source_face_id: int
    source_face_arity: int
    source_vertex_ids: tuple[int, ...]
    generated_triangle_face_ids: tuple[int, ...]
    generated_triangle_vertex_ids: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class _SourceFaceIntakeAudit:
    source_face_arities: tuple[int, ...]
    source_face_remap: tuple[_SourceFaceRemap, ...]
    face_arity_policy: str = "fan_triangulate_non_triangle_faces_preserve_source_face_remap"
    operator_ownership_policy: str = "triangulated_subfaces_summed_to_source_face"


@dataclass(frozen=True)
class _DuplicateVertexPreprocessingAudit:
    input_points: tuple[tuple[float, float, float], ...]
    input_faces: tuple[tuple[int, int, int], ...]
    deduplicated_points: tuple[tuple[float, float, float], ...]
    deduplicated_faces: tuple[tuple[int, int, int], ...]
    original_to_deduplicated_vertex_ids: tuple[int, ...]
    duplicate_clusters: tuple[tuple[int, ...], ...]
    distance_tolerance: float = 0.0


@dataclass(frozen=True)
class _UnsupportedSourceFaceIntakeAudit:
    source_face_id: int
    source_face_arity: int
    source_vertex_ids: tuple[int, ...]
    failure_label: str = "source_face_intake_unsupported_concave_polygon"
    case_status: str = "unsupported_fixture_policy"
    rejection_reason: str = "concave_non_triangle_source_face"


@dataclass(frozen=True)
class _PaperToyCase:
    case_id: str
    description: str
    mesh: TriangleMesh
    face_groups: tuple[frozenset[int], ...]
    collapse_pair: tuple[frozenset[int], frozenset[int]] | None = None
    priority_queue_target_count: int | None = None
    component_pair_edge_insertion: bool = False
    component_pair_excess_volume_threshold: float | None = None
    component_pair_candidate_cap: int | None = None
    postprocess_fixture: bool = False
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None
    duplicate_vertex_preprocessing_audit: _DuplicateVertexPreprocessingAudit | None = None
    unsupported_source_face_intake_audit: _UnsupportedSourceFaceIntakeAudit | None = None
    fixture_breadth_batch: str | None = None
    executable_source_face_ids: tuple[int, ...] | None = None


def _paper_faithful_offline_scope_criteria() -> list[dict[str, object]]:
    criteria: list[dict[str, object]] = [
        {
            "criterion_id": "source_mesh_and_preprocessing_policy",
            "paper_requirement": (
                "Mesh vertices/faces plus duplicate or overlapped vertex preprocessing "
                "and source-face remap."
            ),
            "current_evidence": (
                "Triangle toy fixtures, fan-triangulated source-face fixtures, and one "
                "exact-coordinate duplicate-vertex fixture; broader unclean-mesh policy is absent."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Exact-overlap toy preprocessing only; no robust arbitrary mesh cleanup."
            ),
            "next_action": (
                "Expand preprocessing/source-mesh fixture breadth before stronger wording."
            ),
        },
        {
            "criterion_id": "source_face_intake_policy",
            "paper_requirement": (
                "Preserve face ownership across triangle, quad, and polygon source faces."
            ),
            "current_evidence": (
                "One quad and one five-vertex polygon fan-triangulation fixture with "
                "source-face remap and operator ownership accounting."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Source-face intake is toy-scoped, not a general polygon mesh implementation."
            ),
            "next_action": "Add broader source-face cases only after a fixture-breadth plan.",
        },
        {
            "criterion_id": "operator_q_audit",
            "paper_requirement": (
                "Per-face and merged-group Q operators with eigen decomposition."
            ),
            "current_evidence": (
                "Per-face and merged-group operator rows exist for named toy fixtures, "
                "including source-face aggregate rows."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Operator evidence is named-fixture audit data, not full paper decomposition."
            ),
            "next_action": "Expand operator degeneracy and fixture coverage.",
        },
        {
            "criterion_id": "primitive_vocabulary_and_fit",
            "paper_requirement": (
                "Audit the six paper primitive candidates, containment, formulas, axis "
                "policies, and primitive weights."
            ),
            "current_evidence": (
                "All six paper primitive names have fixture-scoped audit rows, including "
                "Batch B primitive-fit breadth fixtures; capped cylinder, frustum, and "
                "trapezoidal prism remain offline-only."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Primitive rows are audit rows, not Newton runtime support or "
                "collision-quality evidence."
            ),
            "next_action": "Expand fitting fixtures and paper-specific invariants.",
        },
        {
            "criterion_id": "paper_collapse_cost_and_weighting",
            "paper_requirement": (
                "Use paper base collapse cost, separate weighted priority cost, and no "
                "intersection-volume primary cost."
            ),
            "current_evidence": (
                "One two-face cost fixture plus Batch C cost/search/stop fixtures record "
                "base and weighted costs, weighted priority ordering, and one positive "
                "finite threshold block."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": "Cost rows are toy accounting, not optimizer or benchmark evidence.",
            "next_action": "Broaden merge-cost fixtures and threshold cases.",
        },
        {
            "criterion_id": "greedy_priority_queue_trace",
            "paper_requirement": (
                "Initialize adjacent face-pair candidates, pop minimum priority cost, "
                "handle stale entries, and merge greedily."
            ),
            "current_evidence": (
                "Topology, deduplicated-topology, component-pair, and Batch C toy traces "
                "exist with deterministic queue keys, weighted-priority ordering, and "
                "equal-cost stale-prune behavior."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Search traces are toy-scoped and do not prove merge-policy superiority."
            ),
            "next_action": "Expand priority-queue fixtures before stronger wording.",
        },
        {
            "criterion_id": "target_count_and_threshold_stop",
            "paper_requirement": (
                "Stop at target primitive count or when valid threshold policy blocks "
                "remaining candidates."
            ),
            "current_evidence": (
                "Target-count traces, one zero finite-threshold component-pair block, and "
                "one Batch C positive nonzero finite-threshold component-pair block exist."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": "Threshold evidence is narrow toy accounting.",
            "next_action": "Add fixture-breadth plan for target/threshold combinations.",
        },
        {
            "criterion_id": "component_pair_edge_handling",
            "paper_requirement": (
                "Insert pairwise component candidates when disconnected topology cannot "
                "reach the target."
            ),
            "current_evidence": (
                "Accepted and blocked component-pair toy traces exist, and Batch D records "
                "multi-candidate component-pair ordering plus deterministic skipped-pair "
                "accounting under a fixture cap."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Component merging evidence is diagnostic accounting, not broad asset evidence."
            ),
            "next_action": "Continue with postprocess fixture breadth before stronger wording.",
        },
        {
            "criterion_id": "enclosed_primitive_postprocess",
            "paper_requirement": "Remove primitives enclosed by other primitives.",
            "current_evidence": (
                "One explicit identity-axis nested OBB cull fixture exists; generated-search "
                "postprocess breadth is absent."
            ),
            "status": "partial_fixture_scope",
            "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
            "blocking_for_paper_faithful_offline": True,
            "claim_boundary": (
                "Postprocess cull evidence is one offline canary, not a general containment library."
            ),
            "next_action": "Expand postprocess fixtures if required by scope audit follow-up.",
        },
        {
            "criterion_id": "report_schema_tests_and_records",
            "paper_requirement": (
                "Keep report schema, tests, registry, and dated records reproducible."
            ),
            "current_evidence": (
                "This slice adds RED/GREEN tests, registry metadata, and a dated "
                "record path."
            ),
            "status": "implemented_fixture_scope",
            "surrogate_or_paper_faithful": "paper_aligned_boundary",
            "blocking_for_paper_faithful_offline": False,
            "claim_boundary": (
                "Reproducibility evidence supports the audit record only, not stronger "
                "algorithm claims."
            ),
            "next_action": "Keep records updated for every future gate.",
        },
        {
            "criterion_id": "package_generation_boundary",
            "paper_requirement": "Keep offline paper mechanics separate from package conversion.",
            "current_evidence": (
                "The report records package-generation false triggers and no CollisionPackage conversion."
            ),
            "status": "blocked_until_later_gate",
            "surrogate_or_paper_faithful": "out_of_offline_scope",
            "blocking_for_paper_faithful_offline": False,
            "claim_boundary": "Package generation is a later explicit adapter gate.",
            "next_action": (
                "Add package conversion only after a changed offline package boundary exists."
            ),
        },
        {
            "criterion_id": "newton_runtime_boundary",
            "paper_requirement": (
                "Keep offline paper mechanics separate from Newton runtime diagnostics."
            ),
            "current_evidence": "The report records Newton false triggers and no runtime execution.",
            "status": "blocked_until_later_gate",
            "surrogate_or_paper_faithful": "out_of_offline_scope",
            "blocking_for_paper_faithful_offline": False,
            "claim_boundary": "Newton support requires separate mapping and diagnostic records.",
            "next_action": (
                "Run Newton only after package conversion and runtime admissibility are recorded."
            ),
        },
        {
            "criterion_id": "real_usd_boundary",
            "paper_requirement": "Keep toy fixture audit separate from real asset evidence.",
            "current_evidence": (
                "The report records real-USD false triggers and uses synthetic toy fixtures only."
            ),
            "status": "blocked_until_later_gate",
            "surrogate_or_paper_faithful": "out_of_offline_scope",
            "blocking_for_paper_faithful_offline": False,
            "claim_boundary": "Real-USD evidence requires separate asset manifests and records.",
            "next_action": (
                "Defer bed/Franka or other real assets until a package-changing gate exists."
            ),
        },
        {
            "criterion_id": "benchmark_evaluation_boundary",
            "paper_requirement": (
                "Keep paper benchmark evaluation separate from offline paper-mechanics audit."
            ),
            "current_evidence": (
                "The report records benchmark false triggers and no timing, surface-distance, "
                "byte-cost, or baseline comparison metrics."
            ),
            "status": "blocked_until_later_gate",
            "surrogate_or_paper_faithful": "out_of_offline_scope",
            "blocking_for_paper_faithful_offline": False,
            "claim_boundary": (
                "Benchmark evidence is not required for bounded offline status and is not claimed here."
            ),
            "next_action": (
                "Defer benchmarks until offline decomposition and runtime package gates are ready."
            ),
        },
    ]
    for row in criteria:
        if row["status"] not in _SCOPE_AUDIT_ALLOWED_STATUSES:
            raise ValueError(f"unsupported scope audit status: {row['status']}")
        if (
            row["surrogate_or_paper_faithful"]
            not in _SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS
        ):
            raise ValueError(
                "unsupported scope audit alignment label: "
                f"{row['surrogate_or_paper_faithful']}"
            )
    return criteria


def _paper_faithful_offline_scope_audit_payload() -> dict[str, object]:
    criteria = _paper_faithful_offline_scope_criteria()
    blocking = [
        str(row["criterion_id"])
        for row in criteria
        if row["blocking_for_paper_faithful_offline"]
    ]
    return {
        "audit_scope": "fixture_scoped_offline_paper_lane",
        "audit_version": 1,
        "decision": "remain_partial",
        "paper_faithful_offline_allowed": False,
        "decision_reason": "fixture_scope_still_partial",
        "criteria": criteria,
        "blocking_criteria_ids": blocking,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def build_cpd_paper_offline_report() -> dict[str, object]:
    """Build the first fixture-scoped offline CPD paper mechanics audit."""

    cases = [_case_payload(case) for case in _paper_toy_cases()]
    missing_before_paper_faithful = [
        "paper_fixture_breadth_expansion",
    ]
    return {
        "stage": "cpd_paper_offline_report",
        "status": "partial",
        "report_generation_status": "smoke_passed",
        "claim_boundary": CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
        "evidence_level": CPD_PAPER_OFFLINE_EVIDENCE_LEVEL,
        "status_semantics": CPD_PAPER_OFFLINE_STATUS_SEMANTICS,
        "source_scope": "synthetic_toy_fixtures_only",
        "paper_faithful_offline_supported": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
        "failure_labels": [
            f"{missing_item}_missing"
            for missing_item in missing_before_paper_faithful
        ],
        "next_required_gate": "paper_fixture_breadth_batch_e",
        "paper_faithfulness": {
            "status": "partial",
            "implemented_fixture_scope": [
                "triangle_only_mesh_intake",
                "operator_audit",
                "primitive_fit_audit_all_paper_names_with_surrogate_rows",
                "single_pop_collapse_cost_audit",
                "priority_queue_trace_audit_topology_only",
                "component_pair_edge_insertion_audit_threshold_disabled",
                "component_pair_threshold_blocking_audit",
                "postprocess_enclosed_primitive_culling_audit",
                "paper_polygon_quad_intake_policy_audit",
                "paper_obb_sphere_fit_faithfulness_audit",
                "paper_duplicate_vertex_preprocessing_audit",
                "paper_faithful_offline_scope_audit",
                "paper_fixture_breadth_batch_a_source_preprocess_intake_operator",
                "paper_fixture_breadth_batch_b_primitive_fit",
                "paper_fixture_breadth_batch_c_cost_search_stop",
                "paper_fixture_breadth_batch_d_component_pair",
            ],
            "missing_before_paper_faithful_offline": missing_before_paper_faithful,
        },
        "paper_faithful_offline_scope_audit": (
            _paper_faithful_offline_scope_audit_payload()
        ),
        "paper_weights": PAPER_PRIMITIVE_WEIGHTS,
        "cases": cases,
    }


def _case_payload(case: _PaperToyCase) -> dict[str, object]:
    if case.unsupported_source_face_intake_audit is not None:
        return _unsupported_source_face_case_payload(case)

    preprocessing_boundary = (
        "exact_coordinate_duplicate_vertex_fixture"
        if case.duplicate_vertex_preprocessing_audit is not None
        else None
    )
    primitive_fit_audits = [
        _primitive_fit_audit_payload(
            case.mesh,
            face_group,
            case.source_face_intake_audit,
            preprocessing_boundary,
            case.executable_source_face_ids,
        )
        for face_group in case.face_groups
    ]
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "description": case.description,
        "source_mesh": _source_mesh_payload(
            case.mesh,
            case.source_face_intake_audit,
            case.duplicate_vertex_preprocessing_audit,
            case.executable_source_face_ids,
        ),
        "operator_audit": _operator_audit_payload(
            case.mesh,
            case.face_groups,
            case.source_face_intake_audit,
            preprocessing_boundary,
            case.executable_source_face_ids,
        ),
        "primitive_fit_audit": primitive_fit_audits[-1],
        "primitive_fit_audits": primitive_fit_audits,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if case.fixture_breadth_batch is not None:
        payload["fixture_breadth_batch"] = case.fixture_breadth_batch
    if case.collapse_pair is not None:
        left, right = case.collapse_pair
        payload["collapse_cost_audit"] = _collapse_cost_payload(case.mesh, left, right)
        payload["collapse_trace"] = _collapse_trace_payload(left, right)
    if case.priority_queue_target_count is not None:
        payload["collapse_trace"] = _priority_queue_trace_payload(
            case.mesh,
            case.face_groups,
            case.priority_queue_target_count,
            allow_component_pair_edges=case.component_pair_edge_insertion,
            component_pair_excess_volume_threshold=case.component_pair_excess_volume_threshold,
            component_pair_candidate_cap=case.component_pair_candidate_cap,
            preprocessing_boundary=preprocessing_boundary,
        )
    if case.postprocess_fixture:
        payload["postprocess_audit"] = _postprocess_audit_payload()
    if case.source_face_intake_audit is not None:
        payload["mesh_intake_policy_audit"] = _source_face_intake_audit_payload(
            case.source_face_intake_audit
        )
    if case.duplicate_vertex_preprocessing_audit is not None:
        payload["preprocessing_audit"] = _preprocessing_audit_payload(
            case.duplicate_vertex_preprocessing_audit
        )
    return payload


def _unsupported_source_face_case_payload(case: _PaperToyCase) -> dict[str, object]:
    audit = case.unsupported_source_face_intake_audit
    if audit is None:
        raise ValueError("unsupported source face intake audit is required")
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "description": case.description,
        "case_status": audit.case_status,
        "source_mesh": _unsupported_source_mesh_payload(audit),
        "mesh_intake_policy_audit": _unsupported_source_face_intake_audit_payload(audit),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if case.fixture_breadth_batch is not None:
        payload["fixture_breadth_batch"] = case.fixture_breadth_batch
    return payload


def _source_mesh_payload(
    mesh: TriangleMesh,
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    duplicate_vertex_preprocessing_audit: _DuplicateVertexPreprocessingAudit | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "fixture_scope": "synthetic_toy_mesh",
        "face_arity_policy": "triangle_only_fixture",
        "vertex_count": int(len(mesh.points)),
        "face_count": mesh.face_count,
        "source_face_remap": "identity",
        "connected_component_count": _connected_component_count(mesh),
        "duplicate_vertex_preprocessing": "not_applied_fixture_has_unique_vertices",
    }
    if duplicate_vertex_preprocessing_audit is not None:
        audit = duplicate_vertex_preprocessing_audit
        payload.update(
            {
                "duplicate_vertex_preprocessing": (
                    "exact_coordinate_deduplication_for_fixture"
                ),
                "preprocessed_input_vertex_count": len(audit.input_points),
                "deduplicated_vertex_count": len(audit.deduplicated_points),
                "source_face_remap": (
                    "duplicate_vertex_preprocessing_face_id_preserving"
                ),
                "preprocessing_source_face_remap": (
                    _duplicate_vertex_source_face_remap(audit)
                ),
            }
        )
    if executable_source_face_ids is not None:
        payload["executable_source_face_ids"] = [
            int(source_face_id) for source_face_id in executable_source_face_ids
        ]
    if source_face_intake_audit is None:
        return payload

    payload.update(
        {
            "face_arity_policy": source_face_intake_audit.face_arity_policy,
            "source_face_count": len(source_face_intake_audit.source_face_arities),
            "source_face_arities": list(source_face_intake_audit.source_face_arities),
            "triangulated_face_count": mesh.face_count,
            "executable_triangle_face_count": mesh.face_count,
            "executable_triangle_faces": [
                [int(index) for index in mesh.faces[face_id]]
                for face_id in range(mesh.face_count)
            ],
            "source_face_remap": _source_face_remap_payload(
                source_face_intake_audit.source_face_remap
            ),
            "operator_ownership_policy": (
                source_face_intake_audit.operator_ownership_policy
            ),
            "source_face_preconditions": _source_face_preconditions(),
        }
    )
    return payload


def _unsupported_source_mesh_payload(
    audit: _UnsupportedSourceFaceIntakeAudit,
) -> dict[str, object]:
    return {
        "fixture_scope": "synthetic_unsupported_source_face_fixture",
        "face_arity_policy": "reject_unsupported_concave_polygon",
        "vertex_count": len(audit.source_vertex_ids),
        "face_count": 0,
        "source_face_count": 1,
        "source_face_arities": [int(audit.source_face_arity)],
        "source_face_remap": [],
        "triangulated_face_count": 0,
        "executable_triangle_face_count": 0,
        "executable_triangle_faces": [],
        "duplicate_vertex_preprocessing": "not_applied_unsupported_intake_fixture",
        "source_face_preconditions": [
            "planar",
            "concave",
            "non_degenerate",
            "consistently_wound",
        ],
    }


def _duplicate_vertex_source_face_remap(
    audit: _DuplicateVertexPreprocessingAudit,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_face_id, input_face in enumerate(audit.input_faces):
        deduplicated_face = tuple(
            audit.original_to_deduplicated_vertex_ids[vertex_id]
            for vertex_id in input_face
        )
        face_preserved = len(set(deduplicated_face)) == len(deduplicated_face)
        rows.append(
            {
                "source_face_id": int(source_face_id),
                "input_vertex_ids": [int(vertex_id) for vertex_id in input_face],
                "deduplicated_vertex_ids": [
                    int(vertex_id) for vertex_id in deduplicated_face
                ],
                "face_preserved": face_preserved,
                "drop_reason": None if face_preserved else "degenerate_after_deduplication",
            }
        )
    return rows


def _executable_deduplicated_faces(
    audit: _DuplicateVertexPreprocessingAudit,
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple(int(vertex_id) for vertex_id in face)
        for face in audit.deduplicated_faces
        if len(set(face)) == len(face)
    )


def _preprocessing_audit_payload(
    audit: _DuplicateVertexPreprocessingAudit,
) -> dict[str, object]:
    source_face_remap = _duplicate_vertex_source_face_remap(audit)
    retained_source_face_ids = [
        int(row["source_face_id"]) for row in source_face_remap if row["face_preserved"]
    ]
    dropped_source_face_ids = [
        int(row["source_face_id"]) for row in source_face_remap if not row["face_preserved"]
    ]
    input_mesh = TriangleMesh(
        points=np.asarray(audit.input_points, dtype=np.float64),
        faces=np.asarray(audit.input_faces, dtype=np.int64),
    )
    executable_faces = _executable_deduplicated_faces(audit)
    deduplicated_mesh = TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(executable_faces, dtype=np.int64),
    )
    return {
        "audit_scope": "duplicate_vertex_preprocessing_fixture",
        "preprocessing_policy": "exact_coordinate_deduplication_for_fixture",
        "distance_tolerance": float(audit.distance_tolerance),
        "input_vertex_count": len(audit.input_points),
        "deduplicated_vertex_count": len(audit.deduplicated_points),
        "duplicate_cluster_count": len(audit.duplicate_clusters),
        "duplicate_clusters": [
            [int(vertex_id) for vertex_id in cluster]
            for cluster in audit.duplicate_clusters
        ],
        "original_to_deduplicated_vertex_ids": [
            int(vertex_id) for vertex_id in audit.original_to_deduplicated_vertex_ids
        ],
        "input_faces": [
            [int(vertex_id) for vertex_id in face] for face in audit.input_faces
        ],
        "deduplicated_faces": [
            [int(vertex_id) for vertex_id in face] for face in audit.deduplicated_faces
        ],
        "executable_deduplicated_faces": [
            [int(vertex_id) for vertex_id in face] for face in executable_faces
        ],
        "preprocessing_source_face_remap": source_face_remap,
        "retained_source_face_ids": retained_source_face_ids,
        "dropped_source_face_ids": dropped_source_face_ids,
        "connected_component_count_before": _connected_component_count(input_mesh),
        "connected_component_count_after": _connected_component_count(deduplicated_mesh),
        "topology_changed": True,
        "degenerate_face_dropped_count": len(dropped_source_face_ids),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _operator_audit_payload(
    mesh: TriangleMesh,
    face_groups: tuple[frozenset[int], ...],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    preprocessing_boundary: str | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    merged_group = face_groups[-1]
    merged_operator = _group_operator(mesh, merged_group)
    payload: dict[str, object] = {
        "operator": "area_weighted_normal_plus_tangent_outer_product",
        "epsilon": PAPER_Q_EPSILON,
        "face_scope": "triangle_only",
        "faces": [
            _face_operator_payload(
                mesh,
                face_id,
                (
                    executable_source_face_ids[face_id]
                    if executable_source_face_ids is not None
                    else None
                ),
            )
            for face_id in range(mesh.face_count)
        ],
        "merged_group": _group_operator_payload(
            merged_operator,
            merged_group,
            source_face_intake_audit,
            executable_source_face_ids,
        ),
    }
    if source_face_intake_audit is not None:
        payload["face_scope"] = "triangle_subfaces_from_source_face"
        payload["source_face_operator_aggregates"] = _source_face_operator_aggregates(
            mesh,
            source_face_intake_audit,
        )
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    if executable_source_face_ids is not None:
        payload["preprocessing_degeneracy_labels"] = [
            "dropped_degenerate_faces_after_preprocessing"
        ]
    return payload


def _face_operator_payload(
    mesh: TriangleMesh,
    face_id: int,
    source_face_id: int | None = None,
) -> dict[str, object]:
    area, normal, tangent, operator = _face_operator_terms(mesh, face_id)
    payload: dict[str, object] = {
        "face_id": int(face_id),
        "area": area,
        "normal": _vector(normal),
        "tangent": _vector(tangent),
        "q_matrix": _matrix(operator),
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }
    if source_face_id is not None:
        payload["source_face_id"] = int(source_face_id)
    return payload


def _source_face_ids_for_generated_group(
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None,
) -> list[int]:
    if source_face_intake_audit is None:
        return []
    return [
        int(remap.source_face_id)
        for remap in source_face_intake_audit.source_face_remap
        if set(remap.generated_triangle_face_ids).issubset(face_group)
    ]


def _group_operator_payload(
    operator: NDArray[np.float64],
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    order = np.argsort(eigenvalues)[::-1]
    sorted_values = eigenvalues[order]
    sorted_vectors = eigenvectors[:, order]
    if np.linalg.det(sorted_vectors) < 0:
        sorted_vectors[:, -1] *= -1.0
    generated_triangle_face_ids = sorted(int(face_id) for face_id in face_group)
    source_face_ids = _source_face_ids_for_generated_group(face_group, source_face_intake_audit)
    if executable_source_face_ids is not None:
        source_face_ids = [
            int(executable_source_face_ids[int(face_id)])
            for face_id in sorted(face_group)
        ]
    payload: dict[str, object] = {
        "source_faces": (
            source_face_ids
            if source_face_intake_audit is not None
            or executable_source_face_ids is not None
            else generated_triangle_face_ids
        ),
        "q_matrix": _matrix(operator),
        "eigenvalues": [float(value) for value in sorted_values],
        "eigenvectors": _matrix(sorted_vectors),
        "eigenvector_matrix_layout": "columns_are_eigenvectors",
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }
    if source_face_intake_audit is not None:
        payload["generated_triangle_face_ids"] = generated_triangle_face_ids
        payload["source_face_ids"] = source_face_ids
    return payload


def _primitive_fit_audit_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    preprocessing_boundary: str | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    obb_row = _paper_obb_candidate_payload(mesh, face_group)
    rows = [
        obb_row,
        _paper_sphere_candidate_payload(mesh, face_group, obb_row),
    ]
    rows.append(_paper_capsule_candidate_payload(mesh, face_group))
    rows.append(_flat_capped_cylinder_candidate_payload(mesh, face_group))
    rows.append(_frustum_candidate_payload(mesh, face_group))
    rows.append(_trapezoidal_prism_candidate_payload(mesh, face_group))
    selected = min(rows, key=lambda row: (float(row["weighted_volume"]), row["candidate_order"]))
    generated_triangle_face_ids = sorted(int(face_id) for face_id in face_group)
    source_face_ids = _source_face_ids_for_generated_group(face_group, source_face_intake_audit)
    if executable_source_face_ids is not None:
        source_face_ids = [
            int(executable_source_face_ids[int(face_id)])
            for face_id in sorted(face_group)
        ]
    payload: dict[str, object] = {
        "source_faces": (
            source_face_ids
            if source_face_intake_audit is not None
            or executable_source_face_ids is not None
            else generated_triangle_face_ids
        ),
        "candidate_scope": "paper_primitive_set_offline_audit_slice",
        "selection_rule": "min_paper_weighted_volume_for_fixture_audit",
        "missing_paper_primitives": [],
        "candidates": rows,
        "selected": selected,
    }
    if source_face_intake_audit is not None or executable_source_face_ids is not None:
        payload["generated_triangle_face_ids"] = generated_triangle_face_ids
        payload["source_face_ids"] = source_face_ids
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    return payload


def _paper_obb_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    local = points @ axes
    lower = local.min(axis=0)
    upper = local.max(axis=0)
    center_local = (lower + upper) * 0.5
    half_extents = np.maximum(
        (upper - lower) * 0.5,
        PAPER_PRIMITIVE_MIN_DIMENSION,
    )
    center = axes @ center_local
    volume = float(8.0 * np.prod(half_extents))
    contains = bool(np.all(np.abs(local - center_local) <= half_extents + 1e-8))
    return _offline_paper_candidate_payload(
        paper_primitive="oriented_bounding_box",
        current_implementation_kind="offline_paper_oriented_bounding_box_fit",
        fit_model="paper_operator_eigenbasis_projected_bounds",
        axis_selection_policy="paper_q_eigenbasis",
        center=center,
        axes=axes,
        dimensions={
            "lower_bounds": _vector(lower),
            "upper_bounds": _vector(upper),
            "paper_center_local": _vector(center_local),
            "paper_center_world": _vector(center),
            "half_extents": _vector(half_extents),
            "axis_order_policy": "descending_abs_q_eigenvalue",
            "volume_formula": "8*hx*hy*hz",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="box",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )


def _paper_sphere_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
    obb_row: dict[str, object],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    center = np.asarray(obb_row["center"], dtype=np.float64)
    axes = np.asarray(obb_row["axes"], dtype=np.float64).T
    distances = np.linalg.norm(points - center, axis=1)
    unclamped_radius = float(distances.max(initial=0.0))
    radius = max(unclamped_radius, PAPER_PRIMITIVE_MIN_DIMENSION)
    volume = float((4.0 / 3.0) * pi * radius**3)
    contains = bool(np.all(distances <= radius + 1e-8))
    centroid = points.mean(axis=0)
    center_centroid_distance = float(np.linalg.norm(center - centroid))
    return _offline_paper_candidate_payload(
        paper_primitive="sphere",
        current_implementation_kind="offline_paper_sphere_fit",
        fit_model="paper_obb_center_max_distance_radius",
        axis_selection_policy="paper_obb_center",
        center=center,
        axes=axes,
        dimensions={
            "radius": radius,
            "center_source": "paper_obb_center",
            "radius_source": "max_distance_from_obb_center_clamped",
            "unclamped_radius": unclamped_radius,
            "center_centroid_distance": center_centroid_distance,
            "center_differs_from_point_centroid": center_centroid_distance > 1e-3,
            "fixture_center_relation": (
                "differs_from_point_centroid"
                if center_centroid_distance > 1e-3
                else "matches_point_centroid"
            ),
            "volume_formula": "4/3*pi*r^3",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="sphere",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )


def _candidate_payload(candidate) -> dict[str, object]:
    paper_primitive = _PAPER_PRIMITIVE_NAMES[candidate.primitive_type]
    weight = PAPER_PRIMITIVE_WEIGHTS[paper_primitive]
    return {
        "candidate_order": _AUDITED_PAPER_PRIMITIVES.index(paper_primitive),
        "paper_primitive": paper_primitive,
        "current_implementation_kind": candidate.primitive_type,
        "implementation_status": _implementation_status(candidate.primitive_type),
        "fit_model": _fit_model(candidate.primitive_type),
        "axis_selection_policy": _axis_selection_policy(candidate.primitive_type),
        "primitive_parameter_lower_clamp": MIN_DIMENSION,
        "newton_runtime_kind": _NEWTON_RUNTIME_KIND[candidate.primitive_type],
        "center": list(candidate.center),
        "axes": [list(axis) for axis in candidate.axes],
        "dimensions": candidate.dimensions,
        "volume": float(candidate.volume),
        "paper_weight": float(weight),
        "weighted_volume": float(candidate.volume * weight),
        "contains_assigned_points": bool(candidate.contains_assigned_points),
    }


def _offline_paper_candidate_payload(
    *,
    paper_primitive: str,
    current_implementation_kind: str,
    fit_model: str,
    axis_selection_policy: str,
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    dimensions: dict[str, object],
    volume: float,
    contains_assigned_points: bool,
    newton_runtime_kind: str = "offline_only_unmapped",
    primitive_parameter_lower_clamp: float = MIN_DIMENSION,
) -> dict[str, object]:
    weight = PAPER_PRIMITIVE_WEIGHTS[paper_primitive]
    return {
        "candidate_order": _AUDITED_PAPER_PRIMITIVES.index(paper_primitive),
        "paper_primitive": paper_primitive,
        "current_implementation_kind": current_implementation_kind,
        "implementation_status": "paper_shaped_offline_fit_audit",
        "fit_model": fit_model,
        "paper_primitive_variant": paper_primitive,
        "axis_selection_policy": axis_selection_policy,
        "primitive_parameter_lower_clamp": primitive_parameter_lower_clamp,
        "containment_tolerance": 1e-8,
        "fit_failure_reason": None if contains_assigned_points else "assigned_points_not_contained",
        "newton_runtime_kind": newton_runtime_kind,
        "center": _vector(center),
        "axes": _matrix(axes.T),
        "axis_matrix_layout": "rows_are_axes",
        "dimensions": dimensions,
        "volume": float(volume),
        "paper_weight": float(weight),
        "weighted_volume": float(volume * weight),
        "contains_assigned_points": bool(contains_assigned_points),
    }


def _frustum_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, local = _obb_center_and_local(points, axes)
    relative = local - ((local.min(axis=0) + local.max(axis=0)) * 0.5)
    axis_candidates = _flat_cylinder_axis_candidates(points, center, axes, relative)
    selected_axis = min(
        axis_candidates,
        key=lambda row: (float(row["flat_cylinder_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected_axis["axis_index"])
    projection = relative[:, axis_index]
    raw_projection_min = float(projection.min())
    raw_projection_max = float(projection.max())
    height = max(raw_projection_max - raw_projection_min, MIN_DIMENSION * 2.0)
    half_height = height * 0.5
    center_projection = (raw_projection_min + raw_projection_max) * 0.5
    center = center + axes[:, axis_index] * center_projection
    radial_axes = [index for index in range(3) if index != axis_index]
    radial_distances = np.linalg.norm(relative[:, radial_axes], axis=1)
    clamped_projection_min = center_projection - half_height
    blend = np.clip((projection - clamped_projection_min) / height, 0.0, 1.0)
    bottom_radius, top_radius = _fit_linear_extent_pair(radial_distances, blend)
    volume = float(
        (pi * height / 3.0)
        * (top_radius**2 + top_radius * bottom_radius + bottom_radius**2)
    )
    axis = axes[:, axis_index]
    contains = _frustum_contains(points, center, axis, half_height, bottom_radius, top_radius)
    bottom_center = center - axis * half_height
    top_center = center + axis * half_height
    return _offline_paper_candidate_payload(
        paper_primitive="frustum",
        current_implementation_kind="offline_frustum_fit_audit",
        fit_model="paper_frustum_axis_from_min_cost_flat_cylinder",
        axis_selection_policy="min_volume_flat_cylinder_axis",
        center=center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_flat_cylinder_axis",
            "height": height,
            "half_height": half_height,
            "top_radius": top_radius,
            "bottom_radius": bottom_radius,
            "top_center": _vector(top_center),
            "bottom_center": _vector(bottom_center),
            "volume_formula": "pi*h/3*(rt^2 + rt*rb + rb^2)",
            "flat_cylinder_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
    )


def _paper_capsule_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    obb_center, _ = _obb_center_and_local(points, axes)
    axis_candidates = _paper_capsule_axis_candidates(points, obb_center, axes)
    selected = min(
        axis_candidates,
        key=lambda row: (float(row["capsule_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected["axis_index"])
    axis = axes[:, axis_index]
    radius = float(selected["radius"])
    half_height = float(selected["half_height"])
    height = float(selected["height"])
    capsule_center = np.asarray(selected["center"], dtype=np.float64)
    volume = float(selected["capsule_volume"])
    contains = _capsule_contains(points, axis, capsule_center, half_height, radius)
    return _offline_paper_candidate_payload(
        paper_primitive="capsule",
        current_implementation_kind="offline_paper_capsule_fit_audit",
        fit_model="paper_capsule_min_volume_over_axes_with_spherical_cap_height",
        axis_selection_policy="min_volume_capsule_axis",
        center=capsule_center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_capsule_axis",
            "radius": radius,
            "height": height,
            "half_height": half_height,
            "segment_start": _vector(capsule_center - axis * half_height),
            "segment_end": _vector(capsule_center + axis * half_height),
            "volume_formula": "pi*r^2*h + 4/3*pi*r^3",
            "paper_capsule_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="capsule",
    )


def _flat_capped_cylinder_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, local = _obb_center_and_local(points, axes)
    relative = local - ((local.min(axis=0) + local.max(axis=0)) * 0.5)
    axis_candidates = _flat_cylinder_axis_candidates(points, center, axes, relative)
    selected = min(
        axis_candidates,
        key=lambda row: (float(row["flat_cylinder_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected["axis_index"])
    axis = axes[:, axis_index]
    half_height = float(selected["half_height"])
    radius = float(selected["radius"])
    cylinder_center = np.asarray(selected["center"], dtype=np.float64)
    height = float(selected["height"])
    bottom_center = cylinder_center - axis * half_height
    top_center = cylinder_center + axis * half_height
    volume = float(selected["flat_cylinder_volume"])
    contains = _flat_cylinder_contains(points, cylinder_center, axis, half_height, radius)
    return _offline_paper_candidate_payload(
        paper_primitive="capped_cylinder",
        current_implementation_kind="offline_flat_capped_cylinder_fit_audit",
        fit_model="paper_flat_capped_cylinder_min_volume_over_axes",
        axis_selection_policy="min_volume_flat_cylinder_axis",
        center=cylinder_center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_flat_cylinder_axis",
            "cap_model": "flat_caps",
            "radius": radius,
            "height": height,
            "half_height": half_height,
            "top_center": _vector(top_center),
            "bottom_center": _vector(bottom_center),
            "volume_formula": "pi*r^2*h",
            "flat_cylinder_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
    )
def _trapezoidal_prism_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, _ = _obb_center_and_local(points, axes)
    axis_orders = (
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    )
    candidates = [
        _trapezoidal_prism_for_axis_order(points, center, axes, axis_order)
        for axis_order in axis_orders
    ]
    containing_candidates = [row for row in candidates if bool(row["contains_assigned_points"])]
    selected_pool = containing_candidates if containing_candidates else candidates
    selected = min(selected_pool, key=lambda row: (float(row["volume"]), row["axis_order"]))
    ordered_axes = axes[:, selected["axis_order"]]
    contains = _trapezoidal_prism_contains(
        points,
        center,
        ordered_axes,
        float(selected["h_x"]),
        float(selected["h_y"]),
        float(selected["h_zb"]),
        float(selected["h_zt"]),
    )
    return _offline_paper_candidate_payload(
        paper_primitive="trapezoidal_prism",
        current_implementation_kind="offline_trapezoidal_prism_fit_audit",
        fit_model="paper_isosceles_trapezoidal_prism_six_axis_orders",
        axis_selection_policy="min_volume_over_six_axis_orders",
        center=center,
        axes=ordered_axes,
        dimensions={
            "axis_order": [int(index) for index in selected["axis_order"]],
            "axis_order_attempt_count": len(axis_orders),
            "axis_order_attempts": [
                {
                    "axis_order": [int(index) for index in row["axis_order"]],
                    "h_x": float(row["h_x"]),
                    "h_y": float(row["h_y"]),
                    "h_zt": float(row["h_zt"]),
                    "h_zb": float(row["h_zb"]),
                    "volume": float(row["volume"]),
                    "contains_assigned_points": bool(row["contains_assigned_points"]),
                }
                for row in candidates
            ],
            "h_x": float(selected["h_x"]),
            "h_y": float(selected["h_y"]),
            "h_zt": float(selected["h_zt"]),
            "h_zb": float(selected["h_zb"]),
            "volume_formula": "4*h_x*h_y*(h_zt + h_zb)",
        },
        volume=float(selected["volume"]),
        contains_assigned_points=contains,
    )


def _trapezoidal_prism_for_axis_order(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    axis_order: tuple[int, int, int],
) -> dict[str, object]:
    ordered_axes = axes[:, axis_order]
    local = (points - center) @ ordered_axes
    h_x = max(float(np.abs(local[:, 0]).max(initial=0.0)), MIN_DIMENSION)
    h_y = max(float(np.abs(local[:, 1]).max(initial=0.0)), MIN_DIMENSION)
    z_abs = np.abs(local[:, 2])
    blend = np.clip((local[:, 1] + h_y) / (2.0 * h_y), 0.0, 1.0)
    h_zb, h_zt = _fit_linear_extent_pair(z_abs, blend)
    volume = float(4.0 * h_x * h_y * (h_zt + h_zb))
    contains = _trapezoidal_prism_contains(points, center, ordered_axes, h_x, h_y, h_zb, h_zt)
    return {
        "axis_order": axis_order,
        "h_x": h_x,
        "h_y": h_y,
        "h_zt": h_zt,
        "h_zb": h_zb,
        "volume": volume,
        "contains_assigned_points": contains,
    }


def _fit_linear_extent_pair(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
) -> tuple[float, float]:
    bottom = MIN_DIMENSION
    top = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if value <= ((1.0 - t) * bottom + t * top) + 1e-12:
            continue
        if t <= 0.5:
            bottom = max(bottom, (value - t * top) / max(1.0 - t, MIN_DIMENSION))
        else:
            top = max(top, (value - (1.0 - t) * bottom) / max(t, MIN_DIMENSION))

    bottom_fixed = bottom
    top_from_bottom = _required_top_extent(values, blend, bottom_fixed)
    top_fixed = top
    bottom_from_top = _required_bottom_extent(values, blend, top_fixed)
    if bottom_fixed + top_from_bottom <= bottom_from_top + top_fixed:
        return _containment_adjusted_linear_extent_pair(values, blend, bottom_fixed, top_from_bottom)
    return _containment_adjusted_linear_extent_pair(values, blend, bottom_from_top, top_fixed)


def _required_top_extent(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    bottom: float,
) -> float:
    top = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if t <= MIN_DIMENSION:
            top = max(top, value)
            continue
        top = max(top, (value - (1.0 - t) * bottom) / t)
    return float(max(top, MIN_DIMENSION))


def _required_bottom_extent(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    top: float,
) -> float:
    bottom = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if (1.0 - t) <= MIN_DIMENSION:
            bottom = max(bottom, value)
            continue
        bottom = max(bottom, (value - t * top) / (1.0 - t))
    return float(max(bottom, MIN_DIMENSION))


def _containment_adjusted_linear_extent_pair(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    bottom: float,
    top: float,
) -> tuple[float, float]:
    for _ in range(2):
        for value, t in zip(values, blend):
            value = max(float(value), MIN_DIMENSION)
            t = float(np.clip(t, 0.0, 1.0))
            allowed = (1.0 - t) * bottom + t * top
            if value <= allowed + 1e-12:
                continue
            gap = value - allowed
            if t <= 0.5:
                bottom += gap / max(1.0 - t, MIN_DIMENSION)
            else:
                top += gap / max(t, MIN_DIMENSION)
    return float(max(bottom, MIN_DIMENSION)), float(max(top, MIN_DIMENSION))


def _flat_cylinder_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axis: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    return bool(
        np.all(np.abs(projected) <= half_height + 1e-8)
        and np.all(radial_distances <= radius + 1e-8)
    )


def _flat_cylinder_axis_candidates(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    relative: NDArray[np.float64],
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for axis_index in range(3):
        projection = relative[:, axis_index]
        projection_min = float(projection.min())
        projection_max = float(projection.max())
        height = max(projection_max - projection_min, MIN_DIMENSION * 2.0)
        half_height = height * 0.5
        axis = axes[:, axis_index]
        axis_center = center + axis * ((projection_min + projection_max) * 0.5)
        radial_axes = [index for index in range(3) if index != axis_index]
        radial_distances = np.linalg.norm(relative[:, radial_axes], axis=1)
        radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
        volume = float(pi * radius**2 * height)
        candidates.append(
            {
                "axis_index": axis_index,
                "center": _vector(axis_center),
                "radius": radius,
                "height": height,
                "half_height": half_height,
                "flat_cylinder_volume": volume,
                "contains_assigned_points": _flat_cylinder_contains(
                    points,
                    axis_center,
                    axis,
                    half_height,
                    radius,
                ),
            }
        )
    return candidates


def _paper_capsule_axis_candidates(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> list[dict[str, object]]:
    relative = points - center
    candidates: list[dict[str, object]] = []
    for axis_index in range(3):
        axis = axes[:, axis_index]
        projected = relative @ axis
        axial_offsets = np.outer(projected, axis)
        radial_vectors = relative - axial_offsets
        radial_distances = np.linalg.norm(radial_vectors, axis=1)
        radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
        cap_allowance = np.sqrt(np.maximum(radius**2 - radial_distances**2, 0.0))
        cap_adjusted = projected - cap_allowance
        segment_min = float(cap_adjusted.min())
        segment_max = float(cap_adjusted.max())
        height = max(segment_max - segment_min, MIN_DIMENSION * 2.0)
        half_height = height * 0.5
        capsule_center = center + axis * ((segment_min + segment_max) * 0.5)
        volume = float(pi * radius**2 * height + (4.0 / 3.0) * pi * radius**3)
        candidates.append(
            {
                "axis_index": axis_index,
                "center": _vector(capsule_center),
                "radius": radius,
                "height": height,
                "half_height": half_height,
                "paper_height_min": segment_min,
                "paper_height_max": segment_max,
                "capsule_volume": volume,
                "contains_assigned_points": _capsule_contains(
                    points,
                    axis,
                    capsule_center,
                    half_height,
                    radius,
                ),
            }
        )
    return candidates


def _capsule_contains(
    points: NDArray[np.float64],
    axis: NDArray[np.float64],
    center: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    clamped = np.clip(projected, -half_height, half_height)
    closest = center + np.outer(clamped, axis)
    distances = np.linalg.norm(points - closest, axis=1)
    return bool(np.all(distances <= radius + 1e-8))


def _frustum_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axis: NDArray[np.float64],
    half_height: float,
    bottom_radius: float,
    top_radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    height = max(half_height * 2.0, MIN_DIMENSION)
    blend = np.clip((projected + half_height) / height, 0.0, 1.0)
    allowed = (1.0 - blend) * bottom_radius + blend * top_radius
    return bool(
        np.all(projected >= -half_height - 1e-8)
        and np.all(projected <= half_height + 1e-8)
        and np.all(radial_distances <= allowed + 1e-8)
    )


def _trapezoidal_prism_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    h_x: float,
    h_y: float,
    h_zb: float,
    h_zt: float,
) -> bool:
    local = (points - center) @ axes
    blend = np.clip((local[:, 1] + h_y) / (2.0 * h_y), 0.0, 1.0)
    allowed_z = (1.0 - blend) * h_zb + blend * h_zt
    return bool(
        np.all(np.abs(local[:, 0]) <= h_x + 1e-8)
        and np.all(np.abs(local[:, 1]) <= h_y + 1e-8)
        and np.all(np.abs(local[:, 2]) <= allowed_z + 1e-8)
    )


def _postprocess_audit_payload() -> dict[str, object]:
    axes = np.eye(3, dtype=np.float64)
    outer = _postprocess_obb_row(
        primitive_id=0,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([1.0, 1.0, 1.0], dtype=np.float64),
        axes=axes,
    )
    inner = _postprocess_obb_row(
        primitive_id=1,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([0.25, 0.25, 0.25], dtype=np.float64),
        axes=axes,
    )
    inner_corners = _obb_corners(
        center=np.asarray(inner["center"], dtype=np.float64),
        half_extents=np.asarray(inner["half_extents"], dtype=np.float64),
        axes=np.asarray(inner["axes"], dtype=np.float64),
    )
    containment_passed = _obb_contains_points(
        center=np.asarray(outer["center"], dtype=np.float64),
        half_extents=np.asarray(outer["half_extents"], dtype=np.float64),
        axes=np.asarray(outer["axes"], dtype=np.float64),
        points=inner_corners,
    )
    cull_records = [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": containment_passed,
            "tested_corner_count": int(len(inner_corners)),
        }
    ]
    return {
        "audit_scope": "enclosed_primitive_culling_fixture",
        "postprocess_input_source": "explicit_audit_primitives_not_search_trace",
        "input_primitive_count": 2,
        "output_primitive_count": 1,
        "postprocess_policy": "remove_primitives_enclosed_by_another_primitive",
        "containment_test_type": "obb_corners_inside_obb",
        "axis_policy": "shared_identity_axes",
        "input_primitives": [outer, inner],
        "cull_records": cull_records,
        "enclosed_primitive_ids": [1],
        "enclosing_primitive_ids": [0],
        "kept_primitive_ids": [0],
        "culled_primitive_ids": [1],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _source_face_intake_audit_payload(audit: _SourceFaceIntakeAudit) -> dict[str, object]:
    remap = _source_face_remap_payload(audit.source_face_remap)
    triangulated_count = sum(len(row["generated_triangle_face_ids"]) for row in remap)
    return {
        "audit_scope": "polygon_quad_source_face_intake_policy_fixture",
        "source_face_policy": "preserve_source_face_id_after_fan_triangulation",
        "triangulation_policy": "fan_from_first_vertex",
        "operator_ownership_policy": audit.operator_ownership_policy,
        "normal_policy": "triangle_normals_area_weighted_after_fan_triangulation",
        "tangent_policy": "triangle_edge_tangents_area_weighted_after_fan_triangulation",
        "source_face_count": len(audit.source_face_arities),
        "source_face_arities": list(audit.source_face_arities),
        "triangulated_face_count": triangulated_count,
        "executable_triangle_face_count": triangulated_count,
        "source_face_remap": remap,
        "source_face_preconditions": _source_face_preconditions(),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _unsupported_source_face_intake_audit_payload(
    audit: _UnsupportedSourceFaceIntakeAudit,
) -> dict[str, object]:
    return {
        "audit_scope": "unsupported_source_face_intake_policy_fixture",
        "source_face_policy": "reject_unsupported_concave_polygon",
        "triangulation_policy": "no_triangulation_for_unsupported_concave_polygon",
        "operator_ownership_policy": "no_executable_operator_rows_for_unsupported_face",
        "source_face_count": 1,
        "source_face_arities": [int(audit.source_face_arity)],
        "source_face_id": int(audit.source_face_id),
        "source_vertex_ids": [int(vertex_id) for vertex_id in audit.source_vertex_ids],
        "generated_triangle_face_ids": [],
        "generated_triangle_vertex_ids": [],
        "triangulated_face_count": 0,
        "executable_triangle_face_count": 0,
        "failure_label": audit.failure_label,
        "top_level_failure_label": False,
        "case_status": audit.case_status,
        "rejection_reason": audit.rejection_reason,
        "source_face_preconditions": [
            "planar",
            "concave",
            "non_degenerate",
            "consistently_wound",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _source_face_remap_payload(
    remaps: tuple[_SourceFaceRemap, ...],
) -> list[dict[str, object]]:
    return [
        {
            "source_face_id": int(remap.source_face_id),
            "source_face_arity": int(remap.source_face_arity),
            "source_vertex_ids": [int(index) for index in remap.source_vertex_ids],
            "generated_triangle_face_ids": [
                int(face_id) for face_id in remap.generated_triangle_face_ids
            ],
            "generated_triangle_vertex_ids": [
                [int(index) for index in triangle]
                for triangle in remap.generated_triangle_vertex_ids
            ],
        }
        for remap in remaps
    ]


def _source_face_preconditions() -> list[str]:
    return ["planar", "convex", "non_degenerate", "consistently_wound"]


def _source_face_operator_aggregates(
    mesh: TriangleMesh,
    audit: _SourceFaceIntakeAudit,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for remap in audit.source_face_remap:
        q_matrix = np.zeros((3, 3), dtype=np.float64)
        for face_id in remap.generated_triangle_face_ids:
            q_matrix += _face_operator_terms(mesh, int(face_id))[3]
        eigen_payload = _group_operator_payload(
            q_matrix,
            frozenset(int(face_id) for face_id in remap.generated_triangle_face_ids),
        )
        rows.append(
            {
                "source_face_id": int(remap.source_face_id),
                "source_face_arity": int(remap.source_face_arity),
                "source_vertex_ids": [int(index) for index in remap.source_vertex_ids],
                "generated_triangle_face_ids": [
                    int(face_id) for face_id in remap.generated_triangle_face_ids
                ],
                "generated_triangle_vertex_ids": [
                    [int(index) for index in triangle]
                    for triangle in remap.generated_triangle_vertex_ids
                ],
                "q_matrix": _matrix(q_matrix),
                "eigenvalues": eigen_payload["eigenvalues"],
                "eigenvectors": eigen_payload["eigenvectors"],
                "eigenvector_matrix_layout": eigen_payload["eigenvector_matrix_layout"],
                "degeneracy_labels": eigen_payload["degeneracy_labels"],
            }
        )
    return rows


def _postprocess_obb_row(
    *,
    primitive_id: int,
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> dict[str, object]:
    return {
        "primitive_id": primitive_id,
        "kind": "oriented_bounding_box",
        "center": _vector(center),
        "half_extents": _vector(half_extents),
        "axes": _matrix(axes),
    }


def _obb_corners(
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> NDArray[np.float64]:
    signs = np.array(
        [
            [-1.0, -1.0, -1.0],
            [-1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0],
            [1.0, 1.0, -1.0],
            [1.0, 1.0, 1.0],
        ],
        dtype=np.float64,
    )
    return center + (signs * half_extents) @ axes


def _obb_contains_points(
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
    points: NDArray[np.float64],
) -> bool:
    local = (points - center) @ axes.T
    return bool(np.all(np.abs(local) <= half_extents + 1e-8))


def _assigned_points(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    point_indices = sorted(
        {
            int(point_index)
            for face_id in face_group
            for point_index in mesh.faces[int(face_id)]
        }
    )
    return np.asarray(mesh.points[point_indices], dtype=np.float64)


def _candidate_axes(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    operator = _group_operator(mesh, face_group)
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    order = np.argsort(np.abs(eigenvalues))[::-1]
    axes = eigenvectors[:, order]
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1.0
    return axes


def _obb_center_and_local(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    local = points @ axes
    local_min = local.min(axis=0)
    local_max = local.max(axis=0)
    local_center = (local_min + local_max) * 0.5
    return axes @ local_center, local


def _collapse_cost_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    payload = _paper_merge_cost_payload(mesh, left, right)
    payload["priority_queue_policy"] = "greedy_single_pop_fixture"
    return payload


def _paper_merge_cost_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    left_audit = _primitive_fit_audit_payload(mesh, left)
    right_audit = _primitive_fit_audit_payload(mesh, right)
    merged_audit = _primitive_fit_audit_payload(mesh, frozenset(left | right))
    left_fit = left_audit["selected"]
    right_fit = right_audit["selected"]
    merged = merged_audit["selected"]
    paper_base_cost = float(merged["volume"] - (left_fit["volume"] + right_fit["volume"]))
    weighted_priority_cost = float(
        merged["weighted_volume"]
        - (left_fit["weighted_volume"] + right_fit["weighted_volume"])
    )
    return {
        "source_faces_left": sorted(int(face_id) for face_id in left),
        "source_faces_right": sorted(int(face_id) for face_id in right),
        "source_faces_merged": sorted(int(face_id) for face_id in left | right),
        "paper_base_cost": paper_base_cost,
        "weighted_priority_cost": weighted_priority_cost,
        "left_primitive": left_fit["paper_primitive"],
        "right_primitive": right_fit["paper_primitive"],
        "merged_primitive": merged["paper_primitive"],
        "left_volume": left_fit["volume"],
        "right_volume": right_fit["volume"],
        "merged_volume": merged["volume"],
        "left_weighted_volume": left_fit["weighted_volume"],
        "right_weighted_volume": right_fit["weighted_volume"],
        "merged_weighted_volume": merged["weighted_volume"],
        "left_fit_audit": left_audit,
        "right_fit_audit": right_audit,
        "merged_fit_audit": merged_audit,
        "paper_weights": PAPER_PRIMITIVE_WEIGHTS,
        "primary_cost_normalized_by_aabb": False,
        "intersection_volume_term_included": False,
        "newton_runtime_triggered": False,
    }


def _collapse_trace_payload(
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    return {
        "trace_scope": "single_greedy_priority_queue_pop_fixture",
        "edge_source": "topology",
        "initial_edge_count": 1,
        "popped_source_faces_left": sorted(int(face_id) for face_id in left),
        "popped_source_faces_right": sorted(int(face_id) for face_id in right),
        "stale_entry": False,
        "accepted": True,
        "lookahead_used": False,
        "current_primitive_count_after_pop": 1,
        "stop_reason": "target_count_reached",
        "package_generation_triggered": False,
    }


def _priority_queue_trace_payload(
    mesh: TriangleMesh,
    initial_groups: tuple[frozenset[int], ...],
    target_primitive_count: int,
    *,
    allow_component_pair_edges: bool = False,
    component_pair_excess_volume_threshold: float | None = None,
    component_pair_candidate_cap: int | None = None,
    preprocessing_boundary: str | None = None,
) -> dict[str, object]:
    if component_pair_excess_volume_threshold is not None and not np.isfinite(
        component_pair_excess_volume_threshold
    ):
        raise ValueError("component_pair_excess_volume_threshold must be finite")
    if component_pair_candidate_cap is not None and component_pair_candidate_cap < 1:
        raise ValueError("component_pair_candidate_cap must be positive")
    active_groups = set(initial_groups)
    insertion_order = 0
    queue: list[dict[str, object]] = []
    for left, right in _topology_adjacent_group_pairs(mesh, active_groups):
        queue.append(_queue_candidate_payload(mesh, left, right, insertion_order))
        insertion_order += 1

    initial_candidates = [_queue_candidate_summary(entry) for entry in queue]
    events: list[dict[str, object]] = []
    accepted_merge_count = 0
    stale_entry_skipped_count = 0
    blocked_merge_count = 0
    component_pair_edge_insertion_triggered = False
    topology_queue_exhausted_before_component_pair_insertion = False
    component_pair_candidate_count = 0
    component_pair_available_pair_count = 0
    component_pair_candidates: list[dict[str, object]] = []
    skipped_component_pair_keys: list[dict[str, object]] = []
    component_pair_attempted_pairs: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    threshold_blocked = False

    while len(active_groups) > target_primitive_count:
        if not queue:
            if not allow_component_pair_edges:
                break
            component_pairs = [
                (left, right)
                for left, right in _component_pair_group_pairs(active_groups)
                if _component_pair_key(left, right) not in component_pair_attempted_pairs
            ]
            if not component_pairs:
                break
            topology_queue_exhausted_before_component_pair_insertion = True
            component_pair_edge_insertion_triggered = True
            component_pair_available_pair_count += len(component_pairs)
            if component_pair_candidate_cap is None:
                admitted_component_pairs = component_pairs
                skipped_component_pairs: list[tuple[frozenset[int], frozenset[int]]] = []
            else:
                admitted_component_pairs = component_pairs[:component_pair_candidate_cap]
                skipped_component_pairs = component_pairs[component_pair_candidate_cap:]
            for left, right in skipped_component_pairs:
                skipped_component_pair_keys.append(
                    _skipped_component_pair_payload(left, right)
                )
            for left, right in admitted_component_pairs:
                entry = _queue_candidate_payload(
                    mesh,
                    left,
                    right,
                    insertion_order,
                    edge_source="component_pair",
                )
                queue.append(entry)
                component_pair_candidates.append(_queue_candidate_summary(entry))
                insertion_order += 1
                component_pair_candidate_count += 1
            continue

        queue.sort(key=lambda entry: entry["_sort_key"])
        entry = queue.pop(0)
        active_before = len(active_groups)
        left_group = entry["_left_group"]
        right_group = entry["_right_group"]
        if left_group not in active_groups or right_group not in active_groups:
            events.append(
                _queue_event_payload(
                    entry,
                    stale_entry=True,
                    accepted=False,
                    active_primitive_count_before=active_before,
                    active_primitive_count_after=len(active_groups),
                    event_kind="stale_pop",
                )
            )
            stale_entry_skipped_count += 1
            continue

        if entry["edge_source"] == "component_pair":
            component_pair_attempted_pairs.add(_component_pair_key(left_group, right_group))
            if (
                component_pair_excess_volume_threshold is not None
                and float(entry["paper_base_cost"]) > component_pair_excess_volume_threshold
            ):
                events.append(
                    _queue_event_payload(
                        entry,
                        stale_entry=False,
                        accepted=False,
                        blocked=True,
                        active_primitive_count_before=active_before,
                        active_primitive_count_after=active_before,
                        event_kind="blocked_by_threshold",
                        blocked_reason="component_pair_threshold_exceeded",
                        threshold_value=float(component_pair_excess_volume_threshold),
                        threshold_metric="paper_base_cost",
                    )
                )
                blocked_merge_count += 1
                threshold_blocked = True
                continue

        active_groups.remove(left_group)
        active_groups.remove(right_group)
        merged_group = frozenset(left_group | right_group)
        active_groups.add(merged_group)
        active_after = len(active_groups)

        retained_queue: list[dict[str, object]] = []
        stale_events: list[dict[str, object]] = []
        for queued_entry in queue:
            queued_left = queued_entry["_left_group"]
            queued_right = queued_entry["_right_group"]
            if queued_left in active_groups and queued_right in active_groups:
                retained_queue.append(queued_entry)
                continue
            stale_events.append(
                _queue_event_payload(
                    queued_entry,
                    stale_entry=True,
                    accepted=False,
                    active_primitive_count_before=active_after,
                    active_primitive_count_after=active_after,
                    event_kind="eager_stale_prune",
                )
            )
        queue = retained_queue
        stale_entry_skipped_count += len(stale_events)

        updated_insertions = 0
        for other_group in sorted(active_groups - {merged_group}, key=_group_sort_key):
            if not _groups_share_mesh_edge(mesh, merged_group, other_group):
                continue
            queue.append(_queue_candidate_payload(mesh, merged_group, other_group, insertion_order))
            insertion_order += 1
            updated_insertions += 1

        events.append(
            _queue_event_payload(
                entry,
                stale_entry=False,
                accepted=True,
                active_primitive_count_before=active_before,
                active_primitive_count_after=active_after,
                resulting_source_faces=sorted(int(face_id) for face_id in merged_group),
                updated_neighbor_insertion_count=updated_insertions,
                event_kind="accepted_merge",
            )
        )
        events.extend(stale_events)
        accepted_merge_count += 1

    if len(active_groups) <= target_primitive_count:
        stop_reason = "target_count_reached"
    elif threshold_blocked:
        stop_reason = "all_remaining_edges_blocked_by_threshold"
    else:
        stop_reason = "queue_exhausted_before_target_count"
    component_pair_edge_policy = (
        "insert_when_topology_queue_exhausted_before_target"
        if allow_component_pair_edges
        else "disabled"
    )
    component_pair_candidate_cap_value: int | str
    if allow_component_pair_edges and component_pair_candidate_cap is None:
        component_pair_candidate_cap_value = "all_pairs_for_fixture"
    elif allow_component_pair_edges:
        component_pair_candidate_cap_value = int(component_pair_candidate_cap)
    else:
        component_pair_candidate_cap_value = "disabled"
    if component_pair_excess_volume_threshold is None:
        excess_volume_threshold: float | str = "default_inf"
        threshold_policy = "disabled"
    else:
        excess_volume_threshold = float(component_pair_excess_volume_threshold)
        threshold_policy = "component_pair_paper_base_cost_lte_threshold"
    payload: dict[str, object] = {
        "trace_scope": (
            "component_pair_priority_queue_trace_fixture"
            if allow_component_pair_edges
            else "topology_priority_queue_trace_fixture"
        ),
        "priority_queue_policy": "paper_greedy_min_weighted_priority_cost",
        "target_primitive_count": int(target_primitive_count),
        "excess_volume_threshold": excess_volume_threshold,
        "threshold_policy": threshold_policy,
        "component_pair_edge_policy": component_pair_edge_policy,
        "component_pair_edge_insertion_triggered": component_pair_edge_insertion_triggered,
        "topology_queue_exhausted_before_component_pair_insertion": (
            topology_queue_exhausted_before_component_pair_insertion
        ),
        "component_pair_available_pair_count": component_pair_available_pair_count,
        "component_pair_candidate_count": component_pair_candidate_count,
        "component_pair_candidate_cap": component_pair_candidate_cap_value,
        "component_pair_candidates": component_pair_candidates,
        "component_pair_attempted_pair_count": len(component_pair_attempted_pairs),
        "skipped_component_pair_count": len(skipped_component_pair_keys),
        "skipped_component_pair_keys": skipped_component_pair_keys,
        "initial_active_groups": _sorted_group_payload(initial_groups),
        "initial_edge_count": len(initial_candidates),
        "initial_candidates": initial_candidates,
        "events": events,
        "accepted_merge_count": accepted_merge_count,
        "stale_entry_skipped_count": stale_entry_skipped_count,
        "blocked_merge_count": blocked_merge_count,
        "final_active_groups": _sorted_group_payload(active_groups),
        "stop_reason": stop_reason,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    return payload


def _queue_candidate_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
    insertion_order: int,
    *,
    edge_source: str = "topology",
) -> dict[str, object]:
    left, right = _ordered_group_pair(left, right)
    cost = _paper_merge_cost_payload(mesh, left, right)
    queue_key = [
        float(cost["weighted_priority_cost"]),
        float(cost["paper_base_cost"]),
        cost["source_faces_left"],
        cost["source_faces_right"],
        int(insertion_order),
    ]
    return {
        "_left_group": left,
        "_right_group": right,
        "_sort_key": (
            float(cost["weighted_priority_cost"]),
            float(cost["paper_base_cost"]),
            tuple(cost["source_faces_left"]),
            tuple(cost["source_faces_right"]),
            int(insertion_order),
        ),
        "source_faces_left": cost["source_faces_left"],
        "source_faces_right": cost["source_faces_right"],
        "source_faces_merged": cost["source_faces_merged"],
        "left_primitive": cost["left_primitive"],
        "right_primitive": cost["right_primitive"],
        "merged_primitive": cost["merged_primitive"],
        "paper_base_cost": cost["paper_base_cost"],
        "weighted_priority_cost": cost["weighted_priority_cost"],
        "queue_key": queue_key,
        "edge_source": edge_source,
        "insertion_order": int(insertion_order),
    }


def _queue_candidate_summary(entry: dict[str, object]) -> dict[str, object]:
    return {
        "source_faces_left": entry["source_faces_left"],
        "source_faces_right": entry["source_faces_right"],
        "source_faces_merged": entry["source_faces_merged"],
        "paper_base_cost": entry["paper_base_cost"],
        "weighted_priority_cost": entry["weighted_priority_cost"],
        "queue_key": entry["queue_key"],
        "edge_source": entry["edge_source"],
        "insertion_order": entry["insertion_order"],
        "left_primitive": entry["left_primitive"],
        "right_primitive": entry["right_primitive"],
        "merged_primitive": entry["merged_primitive"],
    }


def _queue_event_payload(
    entry: dict[str, object],
    *,
    stale_entry: bool,
    accepted: bool,
    active_primitive_count_before: int,
    active_primitive_count_after: int,
    event_kind: str,
    blocked: bool = False,
    blocked_reason: str | None = None,
    threshold_value: float | None = None,
    threshold_metric: str | None = None,
    resulting_source_faces: list[int] | None = None,
    updated_neighbor_insertion_count: int = 0,
) -> dict[str, object]:
    payload = _queue_candidate_summary(entry)
    payload.update(
        {
            "event_kind": event_kind,
            "stale_entry": bool(stale_entry),
            "accepted": bool(accepted),
            "blocked": bool(blocked),
            "active_primitive_count_before": int(active_primitive_count_before),
            "active_primitive_count_after": int(active_primitive_count_after),
            "updated_neighbor_insertion_count": int(updated_neighbor_insertion_count),
        }
    )
    if blocked_reason is not None:
        payload["blocked_reason"] = blocked_reason
    if threshold_value is not None:
        payload["threshold_value"] = float(threshold_value)
    if threshold_metric is not None:
        payload["threshold_metric"] = threshold_metric
    if resulting_source_faces is not None:
        payload["resulting_source_faces"] = resulting_source_faces
    return payload


def _topology_adjacent_group_pairs(
    mesh: TriangleMesh,
    groups: set[frozenset[int]],
) -> list[tuple[frozenset[int], frozenset[int]]]:
    pairs: list[tuple[frozenset[int], frozenset[int]]] = []
    sorted_groups = sorted(groups, key=_group_sort_key)
    for left_index, left in enumerate(sorted_groups):
        for right in sorted_groups[left_index + 1 :]:
            if _groups_share_mesh_edge(mesh, left, right):
                pairs.append(_ordered_group_pair(left, right))
    return pairs


def _component_pair_group_pairs(
    groups: set[frozenset[int]],
) -> list[tuple[frozenset[int], frozenset[int]]]:
    pairs: list[tuple[frozenset[int], frozenset[int]]] = []
    sorted_groups = sorted(groups, key=_group_sort_key)
    for left_index, left in enumerate(sorted_groups):
        for right in sorted_groups[left_index + 1 :]:
            pairs.append(_ordered_group_pair(left, right))
    return pairs


def _component_pair_key(
    left: frozenset[int],
    right: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left, right = _ordered_group_pair(left, right)
    return _group_sort_key(left), _group_sort_key(right)


def _skipped_component_pair_payload(
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    left, right = _ordered_group_pair(left, right)
    return {
        "source_faces_left": sorted(int(face_id) for face_id in left),
        "source_faces_right": sorted(int(face_id) for face_id in right),
        "source_faces_merged": sorted(int(face_id) for face_id in left | right),
        "skip_reason": "component_pair_candidate_cap_reached",
    }


def _groups_share_mesh_edge(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> bool:
    left_edges = _group_edges(mesh, left)
    right_edges = _group_edges(mesh, right)
    return bool(left_edges & right_edges)


def _group_edges(mesh: TriangleMesh, group: frozenset[int]) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for face_id in group:
        face = [int(index) for index in mesh.faces[int(face_id)]]
        for index, start in enumerate(face):
            end = face[(index + 1) % len(face)]
            edges.add(tuple(sorted((start, end))))
    return edges


def _ordered_group_pair(
    left: frozenset[int],
    right: frozenset[int],
) -> tuple[frozenset[int], frozenset[int]]:
    if _group_sort_key(left) <= _group_sort_key(right):
        return left, right
    return right, left


def _group_sort_key(group: frozenset[int]) -> tuple[int, ...]:
    return tuple(sorted(int(face_id) for face_id in group))


def _sorted_group_payload(groups) -> list[list[int]]:
    return [
        sorted(int(face_id) for face_id in group)
        for group in sorted(groups, key=_group_sort_key)
    ]


def _paper_toy_cases() -> tuple[_PaperToyCase, ...]:
    return (
        _PaperToyCase(
            case_id="paper_single_box",
            description="triangle-only asymmetric cuboid fixture for first OBB/sphere/capsule/capped-cylinder audit",
            mesh=_asymmetric_cuboid_surface_mesh(),
            face_groups=(frozenset(range(12)),),
        ),
        _PaperToyCase(
            case_id="paper_two_face_merge",
            description="two adjacent triangles for first paper base-cost and weighted-priority audit",
            mesh=_two_face_square_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({0, 1})),
            collapse_pair=(frozenset({0}), frozenset({1})),
        ),
        _PaperToyCase(
            case_id="paper_three_face_chain",
            description="three adjacent triangles for topology priority-queue trace audit",
            mesh=_three_face_chain_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=1,
        ),
        _PaperToyCase(
            case_id="paper_disconnected_components",
            description="two disconnected triangles for threshold-disabled component-pair edge insertion audit",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
        ),
        _PaperToyCase(
            case_id="paper_component_pair_threshold_blocked",
            description="two disconnected triangles for finite-threshold component-pair block audit",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
            component_pair_excess_volume_threshold=0.0,
        ),
        _PaperToyCase(
            case_id="paper_tiny_sphere_clamp",
            description="tiny triangle fixture exercising paper OBB/sphere primitive-parameter clamp",
            mesh=_tiny_sphere_clamp_mesh(),
            face_groups=(frozenset({0}),),
        ),
        _PaperToyCase(
            case_id="paper_duplicate_vertex_preprocessing",
            description="two triangles with exact-coordinate duplicate vertices for preprocessing audit",
            mesh=_duplicate_vertex_preprocessing_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            duplicate_vertex_preprocessing_audit=_duplicate_vertex_preprocessing_audit(),
        ),
        _PaperToyCase(
            case_id="paper_frustum_like",
            description="tapered triangle mesh for first offline frustum fit audit",
            mesh=_frustum_like_mesh(),
            face_groups=(frozenset(range(32)),),
        ),
        _PaperToyCase(
            case_id="paper_trapezoid_prism_like",
            description="roof-like triangle mesh for first offline trapezoidal-prism fit audit",
            mesh=_trapezoid_prism_like_mesh(),
            face_groups=(frozenset(range(12)),),
        ),
        _PaperToyCase(
            case_id="paper_nested_primitive",
            description="explicit nested OBB rows for enclosed-primitive postprocess culling audit",
            mesh=_nested_primitive_mesh(),
            face_groups=(frozenset(range(12)),),
            postprocess_fixture=True,
        ),
        _PaperToyCase(
            case_id="paper_quad_face_intake",
            description="one quad source face fan-triangulated for paper intake policy audit",
            mesh=_quad_face_intake_mesh(),
            face_groups=(frozenset({0, 1}),),
            source_face_intake_audit=_quad_face_intake_audit(),
        ),
        _PaperToyCase(
            case_id="paper_polygon_face_intake",
            description="one five-vertex polygon source face fan-triangulated for paper intake policy audit",
            mesh=_polygon_face_intake_mesh(),
            face_groups=(frozenset({0, 1, 2}),),
            source_face_intake_audit=_polygon_face_intake_audit(),
        ),
        _PaperToyCase(
            case_id="paper_mixed_face_preprocess_operator",
            description="Batch A mixed triangle/quad/polygon source-face fixture with exact-coordinate preprocessing",
            mesh=_mixed_face_preprocess_operator_mesh(),
            face_groups=(frozenset(range(6)),),
            source_face_intake_audit=_mixed_face_preprocess_operator_intake_audit(),
            duplicate_vertex_preprocessing_audit=_mixed_face_preprocess_operator_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
        ),
        _PaperToyCase(
            case_id="paper_degenerate_preprocess_face_drop",
            description="Batch A exact-coordinate preprocessing fixture that drops one degenerate source face",
            mesh=_degenerate_preprocess_face_drop_mesh(),
            face_groups=(frozenset({0}),),
            duplicate_vertex_preprocessing_audit=_degenerate_preprocess_face_drop_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
            executable_source_face_ids=(1,),
        ),
        _PaperToyCase(
            case_id="paper_concave_polygon_rejected",
            description="Batch A concave non-triangle source face rejected by conservative intake policy",
            mesh=_unsupported_source_face_placeholder_mesh(),
            face_groups=(frozenset({0}),),
            unsupported_source_face_intake_audit=_concave_polygon_rejected_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
        ),
        _PaperToyCase(
            case_id="paper_rotated_box_fit",
            description="Batch B rotated cuboid fixture for non-identity paper OBB axes",
            mesh=_paper_rotated_box_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_offset_sphere_fit",
            description="Batch B offset cuboid fixture for OBB-centered sphere audit",
            mesh=_paper_offset_sphere_fit_mesh(),
            face_groups=(frozenset(range(13)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_off_axis_capsule_fit",
            description="Batch B elongated off-axis fixture for capsule axis audit",
            mesh=_paper_off_axis_capsule_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_flat_capped_cylinder_axis_fit",
            description="Batch B off-axis flat-capped-cylinder primitive-fit audit",
            mesh=_paper_flat_capped_cylinder_axis_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_tapered_frustum_fit",
            description="Batch B tapered fixture for unequal frustum radii audit",
            mesh=_paper_tapered_frustum_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_asymmetric_trapezoid_fit",
            description="Batch B asymmetric wedge fixture for trapezoidal-prism axis-order audit",
            mesh=_paper_asymmetric_trapezoid_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_branching_cost_order",
            description="Batch C branching topology fixture for weighted priority cost ordering",
            mesh=_paper_branching_cost_order_mesh(),
            face_groups=(
                frozenset({0}),
                frozenset({1}),
                frozenset({2}),
                frozenset({3}),
            ),
            priority_queue_target_count=3,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_equal_cost_queue_tie",
            description="Batch C symmetric topology fixture for deterministic equal-cost queue ties",
            mesh=_paper_equal_cost_queue_tie_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=1,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_nonzero_threshold_block",
            description="Batch C positive finite component-pair threshold block fixture",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
            component_pair_excess_volume_threshold=1e-6,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_component_pair_multi_candidate_order",
            description="Batch D three disconnected components fixture for component-pair candidate ordering",
            mesh=_three_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=2,
            component_pair_edge_insertion=True,
            fixture_breadth_batch="paper_fixture_breadth_batch_d",
        ),
        _PaperToyCase(
            case_id="paper_component_pair_cap_skipped",
            description="Batch D four disconnected components fixture for capped skipped-pair accounting",
            mesh=_four_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2}), frozenset({3})),
            priority_queue_target_count=3,
            component_pair_edge_insertion=True,
            component_pair_candidate_cap=2,
            fixture_breadth_batch="paper_fixture_breadth_batch_d",
        ),
    )


def _asymmetric_cuboid_surface_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.5],
            [2.0, 0.0, 0.5],
            [2.0, 1.0, 0.5],
            [0.0, 1.0, 0.5],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 6, 5],
            [4, 7, 6],
            [0, 4, 5],
            [0, 5, 1],
            [1, 5, 6],
            [1, 6, 2],
            [2, 6, 7],
            [2, 7, 3],
            [3, 7, 4],
            [3, 4, 0],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _two_face_square_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [1, 3, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _three_face_chain_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [2.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 3, 2],
            [1, 4, 3],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _paper_branching_cost_order_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.732172, 0.0, -0.095874],
            [0.151284, 2.644561, -0.089303],
            [-0.431305, -1.498606, -1.144457],
            [2.581183, 2.350038, -1.790004],
            [10.0, 0.0, 0.0],
            [11.0, 0.0, 0.0],
            [10.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [2, 1, 4],
            [5, 6, 7],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _paper_equal_cost_queue_tie_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 3, 1],
            [0, 2, 4],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _three_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _four_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
            [3.0, 3.0, 0.0],
            [4.0, 3.0, 0.0],
            [3.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _tiny_sphere_clamp_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0001, 0.0, 0.0],
            [0.0, 0.0001, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _rotate_z_then_x(
    point: tuple[float, float, float],
    *,
    z_radians: float,
    x_radians: float,
) -> tuple[float, float, float]:
    x, y, z = point
    cos_z = float(np.cos(z_radians))
    sin_z = float(np.sin(z_radians))
    z_rotated = (cos_z * x - sin_z * y, sin_z * x + cos_z * y, z)
    cos_x = float(np.cos(x_radians))
    sin_x = float(np.sin(x_radians))
    return (
        z_rotated[0],
        cos_x * z_rotated[1] - sin_x * z_rotated[2],
        sin_x * z_rotated[1] + cos_x * z_rotated[2],
    )


def _cuboid_points(
    *,
    center: tuple[float, float, float],
    half_extents: tuple[float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    cx, cy, cz = center
    hx, hy, hz = half_extents
    return (
        (cx - hx, cy - hy, cz - hz),
        (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz),
        (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz),
        (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz),
        (cx - hx, cy + hy, cz + hz),
    )


def _box_surface_mesh_from_points(
    points: tuple[tuple[float, float, float], ...],
) -> TriangleMesh:
    return TriangleMesh(
        points=np.asarray(points, dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
            ],
            dtype=np.int64,
        ),
    )


def _paper_rotated_box_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.2, -0.3, 0.4), half_extents=(0.9, 0.35, 0.2))
    rotated = [_rotate_z_then_x(point, z_radians=0.6, x_radians=0.35) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_offset_sphere_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(1.1, -0.4, 0.3), half_extents=(0.75, 0.25, 0.18))
    rotated = [
        _rotate_z_then_x(point, z_radians=0.35, x_radians=-0.25)
        for point in base
    ]
    interior = _rotate_z_then_x((1.45, -0.28, 0.34), z_radians=0.35, x_radians=-0.25)
    return TriangleMesh(
        points=np.asarray(tuple(rotated) + (interior,), dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
                (0, 1, 8),
            ],
            dtype=np.int64,
        ),
    )


def _paper_off_axis_capsule_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.0, 0.0, 0.0), half_extents=(1.6, 0.18, 0.18))
    rotated = [_rotate_z_then_x(point, z_radians=0.7, x_radians=0.45) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_flat_capped_cylinder_axis_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(-0.2, 0.1, 0.0), half_extents=(0.28, 0.28, 1.1))
    rotated = [_rotate_z_then_x(point, z_radians=-0.55, x_radians=0.4) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_tapered_frustum_fit_mesh() -> TriangleMesh:
    bottom = [
        (-1.0, -0.65, -1.8),
        (1.0, -0.65, -1.8),
        (1.0, 0.65, -1.8),
        (-1.0, 0.65, -1.8),
    ]
    top = [
        (-0.22, -0.14, 1.8),
        (0.22, -0.14, 1.8),
        (0.22, 0.14, 1.8),
        (-0.22, 0.14, 1.8),
    ]
    rotated = [
        _rotate_z_then_x(point, z_radians=0.45, x_radians=0.25)
        for point in bottom + top
    ]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_asymmetric_trapezoid_fit_mesh() -> TriangleMesh:
    points = (
        (-0.9, -0.5, -0.35),
        (0.9, -0.5, -0.25),
        (0.65, 0.5, -0.12),
        (-0.55, 0.5, -0.28),
        (-0.45, -0.5, 0.62),
        (0.5, -0.5, 0.48),
        (0.35, 0.5, 0.22),
        (-0.25, 0.5, 0.52),
    )
    rotated = [
        _rotate_z_then_x(point, z_radians=-0.25, x_radians=0.3)
        for point in points
    ]
    return _box_surface_mesh_from_points(tuple(rotated))


def _duplicate_vertex_preprocessing_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
    )
    input_faces = ((0, 1, 2), (3, 4, 5))
    deduplicated_points: list[tuple[float, float, float]] = []
    coordinate_to_deduplicated_id: dict[tuple[float, float, float], int] = {}
    original_to_deduplicated_vertex_ids: list[int] = []
    duplicate_clusters_by_deduplicated_id: dict[int, list[int]] = {}
    for input_vertex_id, point in enumerate(input_points):
        if point not in coordinate_to_deduplicated_id:
            coordinate_to_deduplicated_id[point] = len(deduplicated_points)
            deduplicated_points.append(point)
        deduplicated_id = coordinate_to_deduplicated_id[point]
        original_to_deduplicated_vertex_ids.append(deduplicated_id)
        duplicate_clusters_by_deduplicated_id.setdefault(deduplicated_id, []).append(
            input_vertex_id
        )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    duplicate_clusters = tuple(
        tuple(vertex_ids)
        for vertex_ids in duplicate_clusters_by_deduplicated_id.values()
        if len(vertex_ids) > 1
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=tuple(deduplicated_points),
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=tuple(
            original_to_deduplicated_vertex_ids
        ),
        duplicate_clusters=duplicate_clusters,
    )


def _duplicate_vertex_preprocessing_mesh() -> TriangleMesh:
    audit = _duplicate_vertex_preprocessing_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(audit.deduplicated_faces, dtype=np.int64),
    )


def _frustum_like_mesh() -> TriangleMesh:
    segment_count = 8
    bottom_radius = 1.0
    top_radius = 0.35
    bottom_z = -1.0
    top_z = 1.0
    points: list[list[float]] = []
    for z, radius in ((bottom_z, bottom_radius), (top_z, top_radius)):
        for index in range(segment_count):
            theta = (2.0 * pi * index) / segment_count
            points.append([radius * np.cos(theta), radius * np.sin(theta), z])
    bottom_center = len(points)
    points.append([0.0, 0.0, bottom_z])
    top_center = len(points)
    points.append([0.0, 0.0, top_z])

    faces: list[list[int]] = []
    top_offset = segment_count
    for index in range(segment_count):
        next_index = (index + 1) % segment_count
        bottom_left = index
        bottom_right = next_index
        top_left = top_offset + index
        top_right = top_offset + next_index
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])
        faces.append([bottom_center, bottom_right, bottom_left])
        faces.append([top_center, top_left, top_right])
    return TriangleMesh(
        points=np.asarray(points, dtype=np.float64),
        faces=np.asarray(faces, dtype=np.int64),
    )


def _trapezoid_prism_like_mesh() -> TriangleMesh:
    points = np.array(
        [
            [-1.5, -1.0, -0.35],
            [1.5, -1.0, -0.35],
            [1.5, -1.0, 0.35],
            [-1.5, -1.0, 0.35],
            [-1.5, 1.0, -0.9],
            [1.5, 1.0, -0.9],
            [1.5, 1.0, 0.9],
            [-1.5, 1.0, 0.9],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 6, 5],
            [4, 7, 6],
            [0, 4, 5],
            [0, 5, 1],
            [1, 5, 6],
            [1, 6, 2],
            [2, 6, 7],
            [2, 7, 3],
            [3, 7, 4],
            [3, 4, 0],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _nested_primitive_mesh() -> TriangleMesh:
    return _asymmetric_cuboid_surface_mesh()


def _quad_face_intake_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _polygon_face_intake_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.25, 0.75, 0.0],
            [0.5, 1.25, 0.0],
            [-0.25, 0.75, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _quad_face_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(4,),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=4,
                source_vertex_ids=(0, 1, 2, 3),
                generated_triangle_face_ids=(0, 1),
                generated_triangle_vertex_ids=((0, 1, 2), (0, 2, 3)),
            ),
        ),
    )


def _polygon_face_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(5,),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=5,
                source_vertex_ids=(0, 1, 2, 3, 4),
                generated_triangle_face_ids=(0, 1, 2),
                generated_triangle_vertex_ids=((0, 1, 2), (0, 2, 3), (0, 3, 4)),
            ),
        ),
    )


def _mixed_face_preprocess_operator_input_points() -> tuple[tuple[float, float, float], ...]:
    return (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (2.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (3.0, 0.0, 0.0),
        (4.0, 0.0, 0.0),
        (4.4, 0.6, 0.0),
        (3.7, 1.2, 0.0),
        (3.0, 0.8, 0.0),
    )


def _deduplicate_exact_points(
    input_points: tuple[tuple[float, float, float], ...],
) -> tuple[
    tuple[tuple[float, float, float], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
]:
    deduplicated_points: list[tuple[float, float, float]] = []
    coordinate_to_deduplicated_id: dict[tuple[float, float, float], int] = {}
    original_to_deduplicated_vertex_ids: list[int] = []
    duplicate_clusters_by_deduplicated_id: dict[int, list[int]] = {}
    for input_vertex_id, point in enumerate(input_points):
        if point not in coordinate_to_deduplicated_id:
            coordinate_to_deduplicated_id[point] = len(deduplicated_points)
            deduplicated_points.append(point)
        deduplicated_id = coordinate_to_deduplicated_id[point]
        original_to_deduplicated_vertex_ids.append(deduplicated_id)
        duplicate_clusters_by_deduplicated_id.setdefault(deduplicated_id, []).append(
            input_vertex_id
        )
    duplicate_clusters = tuple(
        tuple(vertex_ids)
        for vertex_ids in duplicate_clusters_by_deduplicated_id.values()
        if len(vertex_ids) > 1
    )
    return (
        tuple(deduplicated_points),
        tuple(original_to_deduplicated_vertex_ids),
        duplicate_clusters,
    )


def _mixed_face_preprocess_operator_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = _mixed_face_preprocess_operator_input_points()
    input_faces = (
        (0, 1, 2),
        (3, 4, 5),
        (3, 5, 6),
        (7, 8, 9),
        (7, 9, 10),
        (7, 10, 11),
    )
    deduplicated_points, original_to_deduplicated_vertex_ids, duplicate_clusters = (
        _deduplicate_exact_points(input_points)
    )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=deduplicated_points,
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=original_to_deduplicated_vertex_ids,
        duplicate_clusters=duplicate_clusters,
    )


def _mixed_face_preprocess_operator_mesh() -> TriangleMesh:
    audit = _mixed_face_preprocess_operator_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(_executable_deduplicated_faces(audit), dtype=np.int64),
    )


def _mixed_face_preprocess_operator_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(3, 4, 5),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=3,
                source_vertex_ids=(0, 1, 2),
                generated_triangle_face_ids=(0,),
                generated_triangle_vertex_ids=((0, 1, 2),),
            ),
            _SourceFaceRemap(
                source_face_id=1,
                source_face_arity=4,
                source_vertex_ids=(3, 4, 5, 6),
                generated_triangle_face_ids=(1, 2),
                generated_triangle_vertex_ids=((1, 3, 4), (1, 4, 5)),
            ),
            _SourceFaceRemap(
                source_face_id=2,
                source_face_arity=5,
                source_vertex_ids=(7, 8, 9, 10, 11),
                generated_triangle_face_ids=(3, 4, 5),
                generated_triangle_vertex_ids=((6, 7, 8), (6, 8, 9), (6, 9, 10)),
            ),
        ),
    )


def _degenerate_preprocess_face_drop_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (0.0, 2.0, 0.0),
    )
    input_faces = ((0, 1, 2), (3, 4, 5))
    deduplicated_points, original_to_deduplicated_vertex_ids, duplicate_clusters = (
        _deduplicate_exact_points(input_points)
    )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=deduplicated_points,
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=original_to_deduplicated_vertex_ids,
        duplicate_clusters=duplicate_clusters,
    )


def _degenerate_preprocess_face_drop_mesh() -> TriangleMesh:
    audit = _degenerate_preprocess_face_drop_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(_executable_deduplicated_faces(audit), dtype=np.int64),
    )


def _unsupported_source_face_placeholder_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _concave_polygon_rejected_audit() -> _UnsupportedSourceFaceIntakeAudit:
    return _UnsupportedSourceFaceIntakeAudit(
        source_face_id=0,
        source_face_arity=5,
        source_vertex_ids=(0, 1, 2, 3, 4),
    )


def _face_operator_terms(
    mesh: TriangleMesh,
    face_id: int,
) -> tuple[float, NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    p0, p1, p2 = mesh.face_points(face_id)
    edge0 = p1 - p0
    edge1 = p2 - p0
    cross = np.cross(edge0, edge1)
    cross_norm = np.linalg.norm(cross)
    area = float(cross_norm * 0.5)
    normal = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    if cross_norm != 0.0:
        normal = cross / cross_norm
    edge0_norm = np.linalg.norm(edge0)
    tangent = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    if edge0_norm != 0.0:
        tangent = edge0 / edge0_norm
    operator = area * (
        np.outer(normal, normal) + PAPER_Q_EPSILON * np.outer(tangent, tangent)
    )
    return area, normal, tangent, operator


def _group_operator(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    operator = np.zeros((3, 3), dtype=np.float64)
    for face_id in face_group:
        operator += _face_operator_terms(mesh, int(face_id))[3]
    return operator


def _connected_component_count(mesh: TriangleMesh) -> int:
    adjacency = mesh.adjacent_faces()
    unseen = set(adjacency)
    component_count = 0
    while unseen:
        component_count += 1
        stack = [unseen.pop()]
        while stack:
            face_id = stack.pop()
            for neighbor in adjacency[face_id]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return component_count


def _operator_degeneracy_labels(operator: NDArray[np.float64]) -> list[str]:
    eigenvalues = np.linalg.eigvalsh(operator)
    if float(np.min(np.abs(eigenvalues))) <= 1e-12:
        return ["near_zero_eigenvalue"]
    return []


def _implementation_status(primitive_type: str) -> str:
    if primitive_type == "capped_cylinder":
        return "current_proxy_not_paper_faithful"
    return "current_surrogate_not_paper_faithful"


def _fit_model(primitive_type: str) -> str:
    if primitive_type == "capped_cylinder":
        return "current_axis_span_radial_proxy_with_hemisphere_caps"
    return "current_cpd_like_surrogate_fit"


def _axis_selection_policy(primitive_type: str) -> str:
    if primitive_type == "capsule":
        return "current_max_span_axis_surrogate"
    if primitive_type == "capped_cylinder":
        return "current_max_span_axis_proxy"
    return "operator_eigenvector_axes_from_current_triangle_operator"


def _matrix(values: NDArray[np.float64]) -> list[list[float]]:
    return [[float(value) for value in row] for row in values.tolist()]


def _vector(values: NDArray[np.float64]) -> list[float]:
    return [float(value) for value in values.tolist()]
