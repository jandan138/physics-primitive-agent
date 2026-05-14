import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_package_from_cpd_like_report_preserves_primitive_metadata():
    mesh = TriangleMesh(
        points=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2]]),
    )
    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box", "sphere", "capsule"))

    package = package_from_cpd_like_report(
        report,
        asset_id="tiny_tri",
        source_path="/tmp/tiny.usda",
        claim_boundary="internal_baseline_not_reproduction_claim",
        max_source_faces=8,
    )

    assert package.package_id == "tiny_tri:cpd_like_face_merge"
    assert package.asset_id == "tiny_tri"
    assert package.source_path == "/tmp/tiny.usda"
    assert package.method == "cpd_like_baseline"
    assert package.status == "smoke_passed"
    assert package.mesh_face_count == 1
    assert package.max_source_faces == 8
    assert package.primitives[0].primitive_id == "tiny_tri:primitive:0"
    assert package.primitives[0].kind in {"box", "sphere", "capsule"}
    assert package.primitives[0].source_faces == (0,)
    assert package.primitives[0].contains_assigned_points is True
    assert package.to_dict()["primitives"][0]["source_faces"] == [0]


def test_package_from_partial_report_marks_runtime_probe_blocked():
    mesh = TriangleMesh(
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
    report = decompose_mesh(mesh, max_primitives=1, primitive_subset=("box",))

    package = package_from_cpd_like_report(
        report,
        asset_id="two_tri",
        source_path="/tmp/two.usda",
        claim_boundary="internal_baseline_not_reproduction_claim",
    )

    assert package.status == "partial"
    assert package.fallback is not None
    assert package.fallback.reason == "no_adjacent_clusters_remaining"
