from pathlib import Path

import pytest

from primitive_collision_compiler.baselines.cpd_like.usd import load_first_mesh


def _write_quad_usd(path: Path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    stage = Usd.Stage.CreateNew(str(path))
    mesh = UsdGeom.Mesh.Define(stage, "/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()


def test_load_first_mesh_triangulates_usd_mesh(tmp_path):
    asset_path = tmp_path / "quad.usda"
    _write_quad_usd(asset_path)

    loaded = load_first_mesh(asset_path, max_faces=8)

    assert loaded.face_count == 2
    assert loaded.points.shape == (4, 3)


def test_load_first_mesh_applies_face_cap(tmp_path):
    asset_path = tmp_path / "quad.usda"
    _write_quad_usd(asset_path)

    loaded = load_first_mesh(asset_path, max_faces=1)

    assert loaded.face_count == 1


def test_load_first_mesh_allows_face_cap_before_all_faces_are_read(tmp_path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "two_quads.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    mesh = UsdGeom.Mesh.Define(stage, "/TwoQuads")
    mesh.CreatePointsAttr(
        [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (2, 0, 0), (3, 0, 0), (3, 1, 0), (2, 1, 0)]
    )
    mesh.CreateFaceVertexCountsAttr([4, 4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3, 4, 5, 6, 7])
    stage.GetRootLayer().Save()

    loaded = load_first_mesh(asset_path, max_faces=1)

    assert loaded.face_count == 1


def test_load_first_mesh_applies_inherited_transform(tmp_path):
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "transformed_quad.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    root = UsdGeom.Xform.Define(stage, "/Root")
    root.AddTranslateOp().Set((10.0, 0.0, 0.0))
    root.AddScaleOp().Set((2.0, 3.0, 1.0))
    mesh = UsdGeom.Mesh.Define(stage, "/Root/Quad")
    mesh.CreatePointsAttr([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    mesh.CreateFaceVertexCountsAttr([4])
    mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    stage.GetRootLayer().Save()

    loaded = load_first_mesh(asset_path, max_faces=8)

    assert loaded.points.tolist() == [
        [10.0, 0.0, 0.0],
        [12.0, 0.0, 0.0],
        [12.0, 3.0, 0.0],
        [10.0, 3.0, 0.0],
    ]
