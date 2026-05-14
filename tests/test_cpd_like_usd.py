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
