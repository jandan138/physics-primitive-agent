from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from primitive_collision_compiler.geometry.mesh import TriangleMesh


class USDMeshLoadError(ValueError):
    """Raised when a USD asset cannot provide a smoke-test triangle mesh."""


def load_first_mesh(path: str | Path, max_faces: int | None = None) -> TriangleMesh:
    if max_faces is not None and max_faces < 1:
        raise USDMeshLoadError("max_faces must be at least 1")

    try:
        from pxr import Usd, UsdGeom
    except ModuleNotFoundError as exc:
        raise USDMeshLoadError(f"pxr_usd_dependency_gap: {exc}") from exc

    asset_path = Path(path)
    if not asset_path.exists():
        raise USDMeshLoadError(f"asset_missing: {asset_path}")

    stage = Usd.Stage.Open(str(asset_path))
    if stage is None:
        raise USDMeshLoadError(f"usd_open_failed: {asset_path}")

    for prim in stage.Traverse():
        if not prim.IsA(UsdGeom.Mesh):
            continue
        mesh = UsdGeom.Mesh(prim)
        return _mesh_to_triangle_mesh(mesh, max_faces=max_faces)

    raise USDMeshLoadError("no_usd_mesh_found")


def _mesh_to_triangle_mesh(mesh: Any, max_faces: int | None) -> TriangleMesh:
    points_attr = mesh.GetPointsAttr().Get()
    counts_attr = mesh.GetFaceVertexCountsAttr().Get()
    indices_attr = mesh.GetFaceVertexIndicesAttr().Get()
    if points_attr is None or counts_attr is None or indices_attr is None:
        raise USDMeshLoadError("usd_mesh_missing_required_topology")

    points = np.asarray([[float(coord) for coord in point] for point in points_attr], dtype=np.float64)
    counts = [int(count) for count in counts_attr]
    indices = [int(index) for index in indices_attr]
    triangles: list[tuple[int, int, int]] = []
    cursor = 0
    for count in counts:
        face_indices = indices[cursor : cursor + count]
        cursor += count
        if count < 3:
            continue
        anchor = face_indices[0]
        for offset in range(1, count - 1):
            triangles.append((anchor, face_indices[offset], face_indices[offset + 1]))
            if max_faces is not None and len(triangles) >= max_faces:
                break
        if max_faces is not None and len(triangles) >= max_faces:
            break

    if not triangles:
        raise USDMeshLoadError("usd_mesh_has_no_triangulatable_faces")
    return TriangleMesh(points=points, faces=np.asarray(triangles, dtype=np.int64))
