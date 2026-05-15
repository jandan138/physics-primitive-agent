from dataclasses import replace
import math

import numpy as np
import pytest

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def _square_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )


def _disconnected_triangles_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [4.0, 0.0, 0.0],
                [5.0, 0.0, 0.0],
                [4.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [3, 4, 5]]),
    )


def test_objective_report_summarizes_smoke_passed_decomposition():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
        max_source_faces=8,
    )
    payload = report.to_dict()

    assert payload["stage"] == "cpd_like_offline_objective"
    assert payload["status"] == "smoke_passed"
    assert payload["asset_id"] == "square"
    assert payload["source_path"] == "tests/generated/square.usda"
    assert payload["decomposition_stage"] == "cpd_like_face_merge"
    assert payload["objective_version"] == "cpd_paper_aligned_surrogate_v0"
    assert payload["claim_boundary"] == (
        "offline_objective_report_not_collision_quality_validation"
    )
    assert payload["evidence_level"] == "offline_cpd_like_objective_smoke"
    assert payload["failure_labels"] == []
    assert payload["metrics"]["primitive_budget"]["within_budget"] is True
    assert payload["metrics"]["primitive_budget"]["primitive_count"] == 1
    assert payload["metrics"]["containment"]["uncontained_primitive_count"] == 0
    assert payload["metrics"]["paper_primitive_gap"]["unsupported_paper_primitive_count"] == 3
    assert math.isfinite(payload["metrics"]["geometric_excess_proxy"]["normalizer_volume"])
    assert payload["decomposition"]["primitive_count"] == 1


def test_objective_report_preserves_stable_schema_keys():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
        max_source_faces=8,
    ).to_dict()

    assert set(payload) == {
        "stage",
        "status",
        "asset_id",
        "source_path",
        "decomposition_stage",
        "objective_version",
        "claim_boundary",
        "evidence_level",
        "metrics",
        "failure_labels",
        "decomposition",
    }
    assert set(payload["metrics"]) == {
        "primitive_budget",
        "geometric_excess_proxy",
        "merge_excess_terms",
        "paper_alignment",
        "containment",
        "paper_primitive_gap",
        "component_accounting",
        "primitive_type_weights",
    }
    assert set(payload["metrics"]["primitive_budget"]) == {
        "primitive_count",
        "target_primitive_count",
        "within_budget",
        "over_budget_count",
        "primitive_count_pressure",
    }
    assert set(payload["metrics"]["geometric_excess_proxy"]) == {
        "total_primitive_volume",
        "weighted_primitive_volume",
        "mesh_aabb_volume",
        "normalizer_volume",
        "normalized_total_primitive_volume",
        "normalized_weighted_primitive_volume",
        "source_normalized_total_weighted_volume",
    }
    assert set(payload["metrics"]["merge_excess_terms"]) == {
        "accepted_merge_count",
        "accepted_normalized_excess_sum",
        "accepted_normalized_excess_max",
        "accepted_eq4_cost_sum",
        "accepted_eq4_cost_min",
        "accepted_eq4_cost_max",
        "blocked_merge_count",
        "blocked_normalized_excess_max",
        "blocked_eq4_cost_sum",
        "blocked_eq4_cost_min",
        "blocked_eq4_cost_max",
        "normalization",
    }
    assert set(payload["metrics"]["paper_alignment"]) == {
        "alignment_version",
        "metadata_scope",
        "paper_id",
        "paper_version",
        "paper_pdf_sha256",
        "paper_section",
        "paper_equation_id",
        "paper_reference",
        "paper_cost_name",
        "paper_cost_formula_reference",
        "implemented_term_path",
        "current_report_terms",
        "current_cost_units",
        "cost_unit_terms",
        "normalizer",
        "merge_cost_volume_basis",
        "uses_primitive_type_weights",
        "objective_report_weights_applied_to_merge_history",
        "paper_weighting_status",
        "threshold_scope",
        "uses_intersection_term",
        "computes_paper_eq4",
        "paper_faithfulness",
        "claim_boundary",
        "matches_paper_story",
        "non_faithful_gaps",
    }


def test_objective_report_maps_merge_excess_to_cpd_eq4_boundary():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
    ).to_dict()

    merge_terms = payload["metrics"]["merge_excess_terms"]
    assert merge_terms["accepted_eq4_cost_sum"] == pytest.approx(
        decomposition.merge_cost_summary["accepted_eq4_cost_sum"]
    )
    assert merge_terms["accepted_eq4_cost_min"] == pytest.approx(
        decomposition.merge_cost_summary["accepted_eq4_cost_min"]
    )
    assert merge_terms["accepted_eq4_cost_max"] == pytest.approx(
        decomposition.merge_cost_summary["accepted_eq4_cost_max"]
    )

    alignment = payload["metrics"]["paper_alignment"]
    assert alignment["alignment_version"] == "cpd_eq4_alignment_metadata_v0"
    assert alignment["metadata_scope"] == "term_category_mapping_not_eq4_implementation"
    assert alignment["paper_id"] == (
        "knodt_gao_2026_convex_primitive_decomposition_for_collision_detection"
    )
    assert alignment["paper_version"] == "arxiv_2602.07369v1"
    assert alignment["paper_pdf_sha256"] == (
        "847c069dafec31e3873a6bdf9b65fa01e1058f4b34036982eaefcefe0e696f95"
    )
    assert alignment["paper_section"] == "3.3 Optimal Primitive Selection"
    assert alignment["paper_equation_id"] == "Eq.4"
    assert "Eq.4" in alignment["paper_reference"]
    assert alignment["paper_cost_name"] == "collapse_excess_volume"
    assert alignment["paper_cost_formula_reference"] == (
        "C(p0,p1)=V(merge(p0,p1))-(V(p0)+V(p1))"
    )
    assert alignment["implemented_term_path"] == "metrics.merge_excess_terms"
    assert "metrics.merge_excess_terms" in alignment["current_report_terms"]
    assert alignment["current_cost_units"] == (
        "mixed_raw_and_aabb_normalized_weighted_primitive_volume"
    )
    assert alignment["cost_unit_terms"] == {
        "metrics.merge_excess_terms.accepted_eq4_cost_*": (
            "raw_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.blocked_eq4_cost_*": (
            "raw_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.accepted_normalized_excess_*": (
            "aabb_normalized_weighted_primitive_volume_delta"
        ),
        "metrics.merge_excess_terms.blocked_normalized_excess_*": (
            "aabb_normalized_weighted_primitive_volume_delta"
        ),
        "metrics.geometric_excess_proxy.normalized_*": (
            "aabb_normalized_weighted_primitive_volume"
        ),
    }
    assert alignment["normalizer"] == "source_mesh_aabb_volume_with_minimum_epsilon"
    assert alignment["merge_cost_volume_basis"] == "decomposition.weighted_volume"
    assert alignment["uses_primitive_type_weights"] is False
    assert alignment["objective_report_weights_applied_to_merge_history"] is False
    assert alignment["paper_weighting_status"] == "metadata_only_or_partial"
    assert alignment["threshold_scope"] == "virtual_component_merges_only"
    assert alignment["uses_intersection_term"] is False
    assert alignment["computes_paper_eq4"] is False
    assert alignment["paper_faithfulness"] == "surrogate_not_paper_faithful"
    assert alignment["claim_boundary"] == (
        "offline_objective_report_not_collision_quality_validation"
    )
    assert "excess_volume_difference_shape" in alignment["matches_paper_story"]
    assert "paper_scope_priority_queue_collapse_search" in alignment["non_faithful_gaps"]
    assert "no_surface_distance_or_collision_benchmark" in alignment["non_faithful_gaps"]


def test_objective_report_alignment_notes_report_weights_when_configured():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    payload = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
        options=CPDLikeObjectiveOptions(primitive_type_weights={"box": 2.0}),
    ).to_dict()

    alignment = payload["metrics"]["paper_alignment"]
    assert alignment["uses_primitive_type_weights"] is True
    assert alignment["objective_report_weights_applied_to_merge_history"] is False


def test_objective_report_preserves_partial_decomposition_failure_labels():
    decomposition = decompose_mesh(
        _disconnected_triangles_mesh(),
        max_primitives=1,
        primitive_subset=("box",),
    )

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="disconnected",
        source_path="tests/generated/disconnected.usda",
    )
    payload = report.to_dict()

    assert payload["status"] == "partial"
    assert payload["failure_labels"] == [
        "source_decomposition_partial",
        "primitive_budget_not_met",
        "unmerged_components",
    ]
    assert payload["metrics"]["primitive_budget"]["over_budget_count"] == 1
    assert payload["metrics"]["component_accounting"]["fallback_reason"] == (
        "no_adjacent_clusters_remaining"
    )
    assert payload["metrics"]["component_accounting"]["final_component_count"] == 2


def test_objective_report_labels_blocked_component_merge():
    decomposition = decompose_mesh(
        _disconnected_triangles_mesh(),
        max_primitives=1,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        excess_volume_threshold_fraction=0.0,
    )

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="disconnected",
        source_path="tests/generated/disconnected.usda",
    )
    payload = report.to_dict()

    assert payload["status"] == "partial"
    assert "component_merge_blocked" in payload["failure_labels"]
    assert payload["metrics"]["component_accounting"]["blocked_merge_count"] == 1
    assert payload["metrics"]["merge_excess_terms"]["blocked_merge_count"] == 1
    assert payload["metrics"]["merge_excess_terms"]["blocked_normalized_excess_max"] > 0.0
    assert payload["metrics"]["merge_excess_terms"]["blocked_eq4_cost_sum"] > 0.0
    assert payload["metrics"]["merge_excess_terms"]["blocked_eq4_cost_min"] > 0.0
    assert payload["metrics"]["merge_excess_terms"]["blocked_eq4_cost_max"] > 0.0


def test_objective_report_labels_uncontained_primitives():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))
    primitive = replace(decomposition.primitives[0], contains_assigned_points=False)
    decomposition = replace(decomposition, primitives=(primitive,))

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
    )
    payload = report.to_dict()

    assert payload["status"] == "partial"
    assert "uncontained_primitives" in payload["failure_labels"]
    assert payload["metrics"]["containment"]["uncontained_primitive_count"] == 1


def test_objective_report_applies_primitive_type_weights_without_changing_decomposition():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
        options=CPDLikeObjectiveOptions(primitive_type_weights={"box": 2.0}),
    )
    payload = report.to_dict()
    volume_terms = payload["metrics"]["geometric_excess_proxy"]

    assert volume_terms["total_primitive_volume"] == pytest.approx(decomposition.total_weighted_volume)
    assert volume_terms["weighted_primitive_volume"] == pytest.approx(
        decomposition.total_weighted_volume * 2.0
    )
    assert payload["metrics"]["primitive_type_weights"] == {"box": 2.0}
    assert decomposition.primitives[0].weighted_volume == decomposition.primitives[0].volume


@pytest.mark.parametrize(
    "weights",
    [
        {"box": -1.0},
        {"box": float("inf")},
        {"": 1.0},
        {"box": "not-a-number"},
    ],
)
def test_objective_report_rejects_invalid_primitive_type_weights(weights):
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    with pytest.raises(ValueError):
        build_cpd_like_objective_report(
            decomposition,
            asset_id="square",
            source_path="tests/generated/square.usda",
            options=CPDLikeObjectiveOptions(primitive_type_weights=weights),
        )


def test_objective_report_planar_mesh_uses_finite_normalizer():
    decomposition = decompose_mesh(_square_mesh(), max_primitives=1, primitive_subset=("box",))

    report = build_cpd_like_objective_report(
        decomposition,
        asset_id="square",
        source_path="tests/generated/square.usda",
    )
    volume_terms = report.to_dict()["metrics"]["geometric_excess_proxy"]

    assert decomposition.mesh_aabb_volume == 0.0
    assert volume_terms["mesh_aabb_volume"] == 0.0
    assert volume_terms["normalizer_volume"] > 0.0
    assert math.isfinite(volume_terms["normalized_weighted_primitive_volume"])
