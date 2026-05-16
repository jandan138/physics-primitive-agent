from __future__ import annotations

from dataclasses import dataclass
from math import pi

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.baselines.cpd_like.primitives import (
    MIN_DIMENSION,
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
_CURRENT_PRIMITIVE_SUBSET = ("box", "sphere", "capsule", "capped_cylinder")
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
        "next_required_gate": "paper_flat_capped_cylinder_fit_audit",
        "paper_faithfulness": {
            "status": "partial",
            "implemented_fixture_scope": [
                "triangle_only_mesh_intake",
                "operator_audit",
                "primitive_fit_audit_all_paper_names_with_surrogate_rows",
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
    candidates = fit_primitive_candidates(mesh, face_group, _CURRENT_PRIMITIVE_SUBSET)
    rows = [_candidate_payload(candidate) for candidate in candidates]
    rows.append(_frustum_candidate_payload(mesh, face_group))
    rows.append(_trapezoidal_prism_candidate_payload(mesh, face_group))
    selected = min(rows, key=lambda row: (float(row["weighted_volume"]), row["candidate_order"]))
    return {
        "source_faces": sorted(int(face_id) for face_id in face_group),
        "candidate_scope": "paper_primitive_set_offline_audit_slice",
        "selection_rule": "min_paper_weighted_volume_for_fixture_audit",
        "missing_paper_primitives": [],
        "candidates": rows,
        "selected": selected,
    }


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
        "primitive_parameter_lower_clamp": MIN_DIMENSION,
        "containment_tolerance": 1e-8,
        "fit_failure_reason": None if contains_assigned_points else "assigned_points_not_contained",
        "newton_runtime_kind": "offline_only_unmapped",
        "center": _vector(center),
        "axes": _matrix(axes.T),
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
    axis_candidates: list[dict[str, object]] = []
    for axis_index in range(3):
        projection = relative[:, axis_index]
        height = max(float(projection.max() - projection.min()), MIN_DIMENSION * 2.0)
        half_height = height * 0.5
        axis_center = center + axes[:, axis_index] * (
            (float(projection.min()) + float(projection.max())) * 0.5
        )
        radial_axes = [index for index in range(3) if index != axis_index]
        radial_distances = np.linalg.norm(relative[:, radial_axes], axis=1)
        radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
        axis_candidates.append(
            {
                "axis_index": axis_index,
                "radius": radius,
                "height": height,
                "flat_cylinder_volume": float(pi * radius**2 * height),
                "contains_assigned_points": _flat_cylinder_contains(
                    points,
                    axis_center,
                    axes[:, axis_index],
                    half_height,
                    radius,
                ),
            }
        )
    selected_axis = min(
        axis_candidates,
        key=lambda row: (float(row["flat_cylinder_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected_axis["axis_index"])
    projection = relative[:, axis_index]
    raw_projection_min = float(projection.min())
    raw_projection_max = float(projection.max())
    raw_height = raw_projection_max - raw_projection_min
    height = max(raw_height, MIN_DIMENSION * 2.0)
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
    _, eigenvectors = np.linalg.eigh(operator)
    axes = eigenvectors[:, ::-1]
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
