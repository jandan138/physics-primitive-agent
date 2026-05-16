from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.baselines.cpd_like.primitives import (
    MIN_DIMENSION,
    PrimitiveFit,
    fit_primitive_candidates,
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
PAPER_PRIMITIVE_WEIGHTS = {
    "oriented_bounding_box": 1.0,
    "sphere": 1.0,
    "capsule": 1.0,
    "capped_cylinder": 1.05,
    "frustum": 2.1,
    "trapezoidal_prism": 1.4,
}
_AUDITED_PRIMITIVE_SUBSET = ("box", "sphere", "capsule", "capped_cylinder")
_PAPER_PRIMITIVE_NAMES = {
    "box": "oriented_bounding_box",
    "sphere": "sphere",
    "capsule": "capsule",
    "capped_cylinder": "capped_cylinder",
}
_NEWTON_RUNTIME_KIND = {
    "box": "box",
    "sphere": "sphere",
    "capsule": "capsule",
    "capped_cylinder": "unmapped_current_proxy",
}


@dataclass(frozen=True)
class _PaperToyCase:
    case_id: str
    description: str
    mesh: TriangleMesh
    face_groups: tuple[frozenset[int], ...]
    collapse_pair: tuple[frozenset[int], frozenset[int]] | None = None


def build_cpd_paper_offline_report() -> dict[str, object]:
    """Build the first fixture-scoped offline CPD paper mechanics audit."""

    cases = [_case_payload(case) for case in _paper_toy_cases()]
    missing_before_paper_faithful = [
        "polygon_and_quad_face_policy",
        "paper_flat_capped_cylinder_fit",
        "frustum_fit",
        "trapezoidal_prism_fit",
        "full_priority_queue_trace",
        "component_pair_edge_insertion",
        "postprocess_enclosed_primitive_culling",
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
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
        "failure_labels": [
            f"{missing_item}_missing"
            for missing_item in missing_before_paper_faithful
        ],
        "next_required_gate": "frustum_and_trapezoidal_prism_fit_audit",
        "paper_faithfulness": {
            "status": "partial",
            "implemented_fixture_scope": [
                "triangle_only_mesh_intake",
                "operator_audit",
                "primitive_fit_audit_subset",
                "single_pop_collapse_cost_audit",
            ],
            "missing_before_paper_faithful_offline": missing_before_paper_faithful,
        },
        "paper_weights": PAPER_PRIMITIVE_WEIGHTS,
        "cases": cases,
    }


def _case_payload(case: _PaperToyCase) -> dict[str, object]:
    primitive_fit_audits = [
        _primitive_fit_audit_payload(case.mesh, face_group)
        for face_group in case.face_groups
    ]
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "description": case.description,
        "source_mesh": _source_mesh_payload(case.mesh),
        "operator_audit": _operator_audit_payload(case.mesh, case.face_groups),
        "primitive_fit_audit": primitive_fit_audits[-1],
        "primitive_fit_audits": primitive_fit_audits,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if case.collapse_pair is not None:
        left, right = case.collapse_pair
        payload["collapse_cost_audit"] = _collapse_cost_payload(case.mesh, left, right)
        payload["collapse_trace"] = _collapse_trace_payload(left, right)
    return payload


def _source_mesh_payload(mesh: TriangleMesh) -> dict[str, object]:
    return {
        "fixture_scope": "synthetic_toy_mesh",
        "face_arity_policy": "triangle_only_fixture",
        "vertex_count": int(len(mesh.points)),
        "face_count": mesh.face_count,
        "source_face_remap": "identity",
        "connected_component_count": _connected_component_count(mesh),
        "duplicate_vertex_preprocessing": "not_applied_fixture_has_unique_vertices",
    }


def _operator_audit_payload(
    mesh: TriangleMesh,
    face_groups: tuple[frozenset[int], ...],
) -> dict[str, object]:
    merged_group = face_groups[-1]
    merged_operator = _group_operator(mesh, merged_group)
    return {
        "operator": "area_weighted_normal_plus_tangent_outer_product",
        "epsilon": PAPER_Q_EPSILON,
        "face_scope": "triangle_only",
        "faces": [_face_operator_payload(mesh, face_id) for face_id in range(mesh.face_count)],
        "merged_group": _group_operator_payload(merged_operator, merged_group),
    }


def _face_operator_payload(mesh: TriangleMesh, face_id: int) -> dict[str, object]:
    area, normal, tangent, operator = _face_operator_terms(mesh, face_id)
    return {
        "face_id": int(face_id),
        "area": area,
        "normal": _vector(normal),
        "tangent": _vector(tangent),
        "q_matrix": _matrix(operator),
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }


def _group_operator_payload(
    operator: NDArray[np.float64],
    face_group: frozenset[int],
) -> dict[str, object]:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    order = np.argsort(eigenvalues)[::-1]
    sorted_values = eigenvalues[order]
    sorted_vectors = eigenvectors[:, order]
    if np.linalg.det(sorted_vectors) < 0:
        sorted_vectors[:, -1] *= -1.0
    return {
        "source_faces": sorted(int(face_id) for face_id in face_group),
        "q_matrix": _matrix(operator),
        "eigenvalues": [float(value) for value in sorted_values],
        "eigenvectors": _matrix(sorted_vectors),
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }


def _primitive_fit_audit_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    candidates = fit_primitive_candidates(mesh, face_group, _AUDITED_PRIMITIVE_SUBSET)
    rows = [_candidate_payload(candidate) for candidate in candidates]
    selected = min(rows, key=lambda row: (float(row["weighted_volume"]), row["candidate_order"]))
    return {
        "source_faces": sorted(int(face_id) for face_id in face_group),
        "candidate_scope": "paper_subset_first_slice",
        "selection_rule": "min_paper_weighted_volume_for_fixture_audit",
        "missing_paper_primitives": ["frustum", "trapezoidal_prism"],
        "candidates": rows,
        "selected": selected,
    }


def _candidate_payload(candidate: PrimitiveFit) -> dict[str, object]:
    paper_primitive = _PAPER_PRIMITIVE_NAMES[candidate.primitive_type]
    weight = PAPER_PRIMITIVE_WEIGHTS[paper_primitive]
    return {
        "candidate_order": _AUDITED_PRIMITIVE_SUBSET.index(candidate.primitive_type),
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


def _collapse_cost_payload(
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
        "priority_queue_policy": "greedy_single_pop_fixture",
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
    }


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
