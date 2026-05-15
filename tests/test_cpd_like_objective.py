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


def test_objective_report_scores_smoke_passed_decomposition():
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
