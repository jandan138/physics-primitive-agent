from pathlib import Path
import builtins

import pytest

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.robots.link_aware_package import (
    audit_link_boundaries,
    build_link_aware_robot_package,
)


def test_build_link_aware_robot_package_keeps_one_primitive_per_link(tmp_path):
    asset_path = _write_two_link_robot_usd(tmp_path)

    report = build_link_aware_robot_package(
        asset_path=str(asset_path),
        asset_id="two_link_robot",
        source_sha256="abc123",
    )

    assert report.status == "generated"
    assert [link.link_path for link in report.links] == [
        "/Robot/link0",
        "/Robot/link1",
    ]
    assert report.audit["status"] == "smoke_passed"
    assert report.audit["outcome"] == "accept"
    assert report.audit["metrics"]["cross_link_merge_count"] == 0
    assert report.audit["metrics"]["per_link_primitive_count"] == {
        "/Robot/link0": 1,
        "/Robot/link1": 1,
    }
    assert [primitive.frame for primitive in report.package.primitives] == [
        "/Robot/link0",
        "/Robot/link1",
    ]
    assert [primitive.source_links for primitive in report.package.primitives] == [
        ("/Robot/link0",),
        ("/Robot/link1",),
    ]
    assert report.package.to_dict()["primitives"][0]["source_links"] == ["/Robot/link0"]


def test_build_link_aware_robot_package_uses_link_local_coordinates(tmp_path):
    asset_path = _write_two_link_robot_usd(tmp_path, translate_link1=True)

    report = build_link_aware_robot_package(
        asset_path=str(asset_path),
        asset_id="translated_robot",
    )

    by_frame = {primitive.frame: primitive for primitive in report.package.primitives}

    assert by_frame["/Robot/link1"].center == pytest.approx((0.5, 0.5, 0.5))
    assert by_frame["/Robot/link1"].dimensions["half_extents"] == pytest.approx(
        [0.5, 0.5, 0.5]
    )


def test_audit_link_boundaries_rejects_cross_link_source_links():
    package = CollisionPackage(
        asset_id="robot",
        package_id="robot:bad",
        primitives=(
            PrimitiveSpec(
                "box",
                primitive_id="bad-cross-link",
                frame="/Robot/link0",
                dimensions={"half_extents": [0.1, 0.1, 0.1]},
                source_links=("/Robot/link0", "/Robot/link1"),
            ),
        ),
    )

    audit = audit_link_boundaries(package, link_paths=("/Robot/link0", "/Robot/link1"))

    assert audit["status"] == "runtime_failure"
    assert audit["outcome"] == "failure"
    assert audit["metrics"]["cross_link_merge_count"] == 1
    assert audit["failure_labels"] == ["cross_link_primitive_merge"]


def test_build_link_aware_robot_package_reports_dependency_gap_without_pxr(
    tmp_path,
    monkeypatch,
):
    asset_path = tmp_path / "robot.usda"
    asset_path.write_text("#usda 1.0\n", encoding="utf-8")
    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pxr":
            raise ModuleNotFoundError("No module named 'pxr'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    report = build_link_aware_robot_package(
        asset_path=str(asset_path),
        asset_id="robot",
    ).to_dict()

    assert report["status"] == "dependency_gap"
    assert report["outcome"] == "dependency_gap"
    assert report["link_boundary_audit"]["outcome"] == "dependency_gap"


def _write_two_link_robot_usd(tmp_path: Path, *, translate_link1: bool = False) -> Path:
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    UsdPhysics = pytest.importorskip("pxr.UsdPhysics")

    asset_path = tmp_path / "two_link_robot.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    root = UsdGeom.Xform.Define(stage, "/Robot")
    link0 = UsdGeom.Xform.Define(stage, "/Robot/link0")
    link1 = UsdGeom.Xform.Define(stage, "/Robot/link1")
    if translate_link1:
        UsdGeom.XformCommonAPI(link1).SetTranslate((10.0, 0.0, 0.0))
    UsdPhysics.RigidBodyAPI.Apply(link0.GetPrim())
    UsdPhysics.RigidBodyAPI.Apply(link1.GetPrim())
    link1_points = (
        [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        if translate_link1
        else [(2, 0, 0), (3, 0, 0), (2, 1, 0), (2, 0, 1)]
    )

    _define_mesh(
        stage,
        "/Robot/link0/visual_mesh",
        points=[
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ],
    )
    _define_mesh(
        stage,
        "/Robot/link1/visual_mesh",
        points=link1_points,
    )
    joint = UsdPhysics.RevoluteJoint.Define(stage, "/Robot/link0/joint01")
    joint.CreateBody0Rel().SetTargets([link0.GetPath()])
    joint.CreateBody1Rel().SetTargets([link1.GetPath()])
    stage.SetDefaultPrim(root.GetPrim())
    stage.GetRootLayer().Save()
    return asset_path


def _define_mesh(stage, path: str, *, points):
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    mesh = UsdGeom.Mesh.Define(stage, path)
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexCountsAttr([3, 3, 3, 3])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 0, 3, 1, 1, 3, 2, 2, 3, 0])
    return mesh
