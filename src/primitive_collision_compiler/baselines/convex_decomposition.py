from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Mapping, Sequence

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.geometry.mesh import TriangleMesh

CONVEX_DECOMPOSITION_STAGE = "phase0_convex_decomposition"
CONVEX_DECOMPOSITION_CLAIM_BOUNDARY = (
    "phase0_coacd_vhacd_executable_baseline_not_collision_quality_or_safety_validation"
)
CONVEX_DECOMPOSITION_EVIDENCE_LEVEL = "phase0_convex_decomposition_executable_smoke"


class ConvexDecompositionUnavailable(ValueError):
    """Raised when no configured convex-decomposition backend can run."""


@dataclass(frozen=True)
class ConvexDecompositionResult:
    package: CollisionPackage
    metadata: dict[str, object]


def build_convex_decomposition_package(
    mesh: TriangleMesh,
    *,
    role: str,
    baseline_id: str,
    source_sha256: str,
    source_path: str,
    max_hulls: int,
    phase0_section: Mapping[str, object],
    preferred_backends: Sequence[str] | None = None,
) -> tuple[CollisionPackage, dict[str, object]]:
    options = _convex_decomposition_options(phase0_section, max_hulls=max_hulls)
    if preferred_backends is not None:
        options = {**options, "preferred_backends": tuple(preferred_backends)}
    errors: list[str] = []
    for backend in options["preferred_backends"]:
        try:
            if backend == "coacd":
                result = _run_coacd(mesh, options)
            elif backend == "vhacd":
                result = _run_vhacd(mesh, options)
            else:
                errors.append(f"{backend}: unsupported backend")
                continue
        except ConvexDecompositionUnavailable as exc:
            errors.append(f"{backend}: {exc}")
            continue
        primitives = _convex_mesh_primitives(
            result.hulls,
            package_asset_id=f"{role}_{baseline_id}",
        )
        if not primitives:
            raise ValueError(f"{backend}_returned_no_valid_convex_hulls")
        package = CollisionPackage(
            package_id=f"{role}_{baseline_id}:phase0_{backend}",
            asset_id=f"{role}_{baseline_id}",
            source_path=source_path,
            source_sha256=source_sha256,
            method=backend,
            stage=CONVEX_DECOMPOSITION_STAGE,
            status="smoke_passed",
            claim_boundary=CONVEX_DECOMPOSITION_CLAIM_BOUNDARY,
            mesh_point_count=int(len(mesh.points)),
            mesh_face_count=int(mesh.face_count),
            max_source_faces=int(mesh.face_count),
            primitive_subset=("convex_mesh",),
            primitives=tuple(primitives),
        )
        metadata = {
            **result.metadata,
            "backend": backend,
            "max_hulls": int(options["max_hulls"]),
            "hull_count": len(primitives),
            "artifact_policy": "generated_hulls_embedded_in_report",
            "claim_boundary": CONVEX_DECOMPOSITION_CLAIM_BOUNDARY,
            "evidence_level": CONVEX_DECOMPOSITION_EVIDENCE_LEVEL,
        }
        return package, metadata
    raise ConvexDecompositionUnavailable("; ".join(errors) or "no backend configured")


@dataclass(frozen=True)
class _RawConvexDecomposition:
    hulls: tuple[tuple[np.ndarray, np.ndarray], ...]
    metadata: dict[str, object]


def _run_coacd(
    mesh: TriangleMesh,
    options: Mapping[str, object],
) -> _RawConvexDecomposition:
    try:
        import coacd  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        executable = _discover_executable("coacd")
        if executable:
            return _run_coacd_executable(mesh, executable, options)
        raise ConvexDecompositionUnavailable("coacd module or executable not available") from None

    settings = {
        "threshold": float(options["coacd_threshold"]),
        "mcts_nodes": int(options["coacd_mcts_nodes"]),
        "mcts_iterations": int(options["coacd_mcts_iterations"]),
        "mcts_max_depth": int(options["coacd_mcts_max_depth"]),
        "merge": bool(options["coacd_merge"]),
        "max_convex_hull": int(options["max_hulls"]),
    }
    cmesh = coacd.Mesh(mesh.points, mesh.faces.reshape(-1, 3))
    raw = coacd.run_coacd(cmesh, **settings)
    return _RawConvexDecomposition(
        hulls=tuple(_normalize_hull(vertices, faces) for vertices, faces in raw),
        metadata={
            "backend_type": "python_module",
            "backend_version": str(getattr(coacd, "__version__", "unknown")),
            "settings": settings,
        },
    )


def _run_vhacd(
    mesh: TriangleMesh,
    options: Mapping[str, object],
) -> _RawConvexDecomposition:
    try:
        import trimesh  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise ConvexDecompositionUnavailable(f"trimesh module not available: {exc}") from exc

    settings = {
        "maxConvexHulls": int(options["max_hulls"]),
        "maxNumVerticesPerCH": int(options["vhacd_max_vertices_per_hull"]),
    }
    tmesh = trimesh.Trimesh(vertices=mesh.points, faces=mesh.faces, process=False)
    try:
        raw = trimesh.decomposition.convex_decomposition(tmesh, **settings)
    except ModuleNotFoundError as exc:
        raise ConvexDecompositionUnavailable(f"vhacdx module not available: {exc}") from exc
    except BaseException as exc:
        raise ValueError(f"vhacd_runtime_failure: {type(exc).__name__}: {exc}") from exc
    return _RawConvexDecomposition(
        hulls=tuple(
            _normalize_hull(item["vertices"], item["faces"])
            for item in raw
            if isinstance(item, Mapping)
        ),
        metadata={
            "backend_type": "python_module",
            "backend_version": "trimesh_vhacdx",
            "settings": settings,
        },
    )


def _run_coacd_executable(
    mesh: TriangleMesh,
    executable: str,
    options: Mapping[str, object],
) -> _RawConvexDecomposition:
    with tempfile.TemporaryDirectory(prefix="npc-coacd-") as tmp:
        input_path = Path(tmp) / "input.obj"
        output_path = Path(tmp) / "output.obj"
        _write_obj(input_path, mesh.points, mesh.faces)
        command = [
            executable,
            "-i",
            str(input_path),
            "-o",
            str(output_path),
            "--quiet",
            "-t",
            str(float(options["coacd_threshold"])),
            "-c",
            str(int(options["max_hulls"])),
            "-mi",
            str(int(options["coacd_mcts_iterations"])),
            "-md",
            str(int(options["coacd_mcts_max_depth"])),
            "-mn",
            str(int(options["coacd_mcts_nodes"])),
        ]
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=float(options["timeout_seconds"]),
        )
        if completed.returncode != 0:
            raise ValueError(
                "coacd_executable_failed: "
                f"exit={completed.returncode}, stderr={completed.stderr.strip()[:500]}"
            )
        hulls = _read_obj_hulls(output_path)
    return _RawConvexDecomposition(
        hulls=hulls,
        metadata={
            "backend_type": "executable",
            "backend_executable": executable,
            "exit_code": completed.returncode,
            "settings": {
                "threshold": float(options["coacd_threshold"]),
                "mcts_nodes": int(options["coacd_mcts_nodes"]),
                "mcts_iterations": int(options["coacd_mcts_iterations"]),
                "mcts_max_depth": int(options["coacd_mcts_max_depth"]),
                "max_convex_hull": int(options["max_hulls"]),
            },
        },
    )


def _convex_mesh_primitives(
    hulls: tuple[tuple[np.ndarray, np.ndarray], ...],
    *,
    package_asset_id: str,
) -> list[PrimitiveSpec]:
    primitives: list[PrimitiveSpec] = []
    for index, (vertices, faces) in enumerate(hulls):
        if len(vertices) < 4 or len(faces) < 4:
            continue
        bounds_min = np.min(vertices, axis=0)
        bounds_max = np.max(vertices, axis=0)
        center = (bounds_min + bounds_max) * 0.5
        local_vertices = vertices - center
        half_extents = np.maximum((bounds_max - bounds_min) * 0.5, 0.0)
        volume = float(8.0 * half_extents[0] * half_extents[1] * half_extents[2])
        primitives.append(
            PrimitiveSpec(
                primitive_id=f"{package_asset_id}:convex_mesh:{index}",
                kind="convex_mesh",
                center=tuple(float(value) for value in center),
                dimensions={
                    "vertices": _float_rows(local_vertices),
                    "faces": _int_rows(faces),
                },
                volume=volume,
                weighted_volume=volume,
                conversion_status="candidate",
            )
        )
    return primitives


def _convex_decomposition_options(
    phase0_section: Mapping[str, object],
    *,
    max_hulls: int,
) -> dict[str, object]:
    raw = phase0_section.get("convex_decomposition", {})
    if not isinstance(raw, Mapping):
        raw = {}
    preferred = raw.get("preferred_backends", ("coacd", "vhacd"))
    if isinstance(preferred, str):
        preferred_backends = (preferred,)
    elif isinstance(preferred, list | tuple):
        preferred_backends = tuple(str(item) for item in preferred)
    else:
        raise ValueError("phase0_defaults.convex_decomposition.preferred_backends must be a list")
    return {
        "preferred_backends": preferred_backends,
        "max_hulls": int(raw.get("max_hulls", max_hulls)),
        "timeout_seconds": float(raw.get("timeout_seconds", 120.0)),
        "coacd_threshold": float(raw.get("coacd_threshold", 0.5)),
        "coacd_mcts_nodes": int(raw.get("coacd_mcts_nodes", 20)),
        "coacd_mcts_iterations": int(raw.get("coacd_mcts_iterations", 5)),
        "coacd_mcts_max_depth": int(raw.get("coacd_mcts_max_depth", 1)),
        "coacd_merge": bool(raw.get("coacd_merge", False)),
        "vhacd_max_vertices_per_hull": int(raw.get("vhacd_max_vertices_per_hull", 64)),
    }


def _normalize_hull(vertices: object, faces: object) -> tuple[np.ndarray, np.ndarray]:
    vertices_array = np.asarray(vertices, dtype=np.float64)
    faces_array = np.asarray(faces, dtype=np.int64)
    if faces_array.ndim == 1:
        if len(faces_array) % 3 != 0:
            raise ValueError("convex hull faces must be triangle indices")
        faces_array = faces_array.reshape((-1, 3))
    if faces_array.ndim != 2 or faces_array.shape[1] != 3:
        raise ValueError("convex hull faces must be triangle indices")
    if vertices_array.ndim != 2 or vertices_array.shape[1] != 3:
        raise ValueError("convex hull vertices must be 3D points")
    return vertices_array, faces_array


def _discover_executable(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    sibling = Path(sys.executable).with_name(name)
    if sibling.exists() and os.access(sibling, os.X_OK):
        return str(sibling)
    return ""


def _write_obj(path: Path, vertices: np.ndarray, faces: np.ndarray) -> None:
    lines: list[str] = []
    for vertex in vertices:
        lines.append(f"v {float(vertex[0])} {float(vertex[1])} {float(vertex[2])}\n")
    for face in faces:
        lines.append(f"f {int(face[0]) + 1} {int(face[1]) + 1} {int(face[2]) + 1}\n")
    path.write_text("".join(lines), encoding="utf-8")


def _read_obj_hulls(path: Path) -> tuple[tuple[np.ndarray, np.ndarray], ...]:
    vertices: list[tuple[float, float, float]] = []
    faces_by_group: dict[str, list[tuple[int, int, int]]] = {"default": []}
    group = "default"
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] in {"o", "g"} and len(parts) > 1:
            group = parts[1]
            faces_by_group.setdefault(group, [])
        elif parts[0] == "v" and len(parts) >= 4:
            vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == "f" and len(parts) >= 4:
            face = tuple(_obj_index(part) for part in parts[1:4])
            faces_by_group.setdefault(group, []).append(face)  # type: ignore[arg-type]
    vertex_array = np.asarray(vertices, dtype=np.float64)
    hulls = []
    for faces in faces_by_group.values():
        if not faces:
            continue
        face_array = np.asarray(faces, dtype=np.int64)
        used = sorted(int(index) for index in np.unique(face_array))
        remap = {old: new for new, old in enumerate(used)}
        remapped_faces = np.asarray(
            [[remap[int(index)] for index in face] for face in face_array],
            dtype=np.int64,
        )
        hulls.append((vertex_array[used], remapped_faces))
    return tuple(hulls)


def _obj_index(token: str) -> int:
    return int(token.split("/")[0]) - 1


def _float_rows(values: np.ndarray) -> list[list[float]]:
    return [[float(component) for component in row] for row in values]


def _int_rows(values: np.ndarray) -> list[list[int]]:
    return [[int(component) for component in row] for row in values]
