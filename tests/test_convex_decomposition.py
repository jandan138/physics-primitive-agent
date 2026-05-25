import sys
import time
import types
import pickle
from pathlib import Path

import numpy as np
import pytest

from primitive_collision_compiler.baselines.convex_decomposition import (
    build_convex_decomposition_package,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh


def test_vhacd_backend_passes_configured_resolution(monkeypatch):
    class FakeTrimesh:
        def __init__(self, *, vertices, faces, process):
            self.vertices = vertices
            self.faces = faces
            self.process = process

    def fake_convex_decomposition(_mesh, **settings):
        assert settings["resolution"] == 12_345
        return [
            {
                "vertices": np.asarray(
                    [
                        [0.0, 0.0, 0.0],
                        [1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0],
                    ],
                    dtype=np.float64,
                ),
                "faces": np.asarray(
                    [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]],
                    dtype=np.int64,
                ),
            }
        ]

    fake_trimesh = types.SimpleNamespace(
        __version__="4.test",
        Trimesh=FakeTrimesh,
        decomposition=types.SimpleNamespace(convex_decomposition=fake_convex_decomposition),
    )
    monkeypatch.setitem(sys.modules, "trimesh", fake_trimesh)
    monkeypatch.setitem(sys.modules, "vhacdx", types.SimpleNamespace(__version__="0.0.test"))

    mesh = TriangleMesh(
        points=np.asarray(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        ),
        faces=np.asarray(
            [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]],
            dtype=np.int64,
        ),
    )

    package, metadata = build_convex_decomposition_package(
        mesh,
        role="fixture",
        baseline_id="vhacd_if_available",
        source_sha256="0" * 64,
        source_path="fixture.usd",
        max_hulls=8,
        phase0_section={
            "convex_decomposition": {
                "max_hulls": 8,
                "vhacd_max_vertices_per_hull": 32,
                "vhacd_resolution": 12_345,
            }
        },
        preferred_backends=("vhacd",),
    )

    assert package.method == "vhacd"
    assert metadata["backend"] == "vhacd"
    assert metadata["settings"]["maxConvexHulls"] == 8
    assert metadata["settings"]["maxNumVerticesPerCH"] == 32
    assert metadata["settings"]["resolution"] == 12_345
    assert metadata["trimesh_version"] == "4.test"
    assert metadata["vhacdx_version"] == "0.0.test"


def test_vhacd_backend_timeout_is_reported_as_runtime_failure(monkeypatch):
    import primitive_collision_compiler.baselines.convex_decomposition as convex_decomposition

    def slow_vhacd_worker(_points, _faces, _settings, _queue, _result_path):
        time.sleep(1.0)

    monkeypatch.setattr(convex_decomposition, "_vhacd_worker", slow_vhacd_worker)

    mesh = TriangleMesh(
        points=np.asarray(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        ),
        faces=np.asarray(
            [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]],
            dtype=np.int64,
        ),
    )

    with pytest.raises(ValueError, match="vhacd_runtime_timeout"):
        build_convex_decomposition_package(
            mesh,
            role="fixture",
            baseline_id="vhacd_if_available",
            source_sha256="0" * 64,
            source_path="fixture.usd",
            max_hulls=8,
            phase0_section={
                "convex_decomposition": {
                    "max_hulls": 8,
                    "timeout_seconds": 0.01,
                }
            },
            preferred_backends=("vhacd",),
        )


def test_vhacd_backend_reads_completed_worker_result_before_join_timeout(monkeypatch):
    import primitive_collision_compiler.baselines.convex_decomposition as convex_decomposition

    def file_result_vhacd_worker(_points, _faces, _settings, result_queue, result_path):
        payload = [
            {
                "vertices": np.asarray(
                    [
                        [0.0, 0.0, 0.0],
                        [1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0],
                    ],
                    dtype=np.float64,
                ),
                "faces": np.asarray(
                    [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]],
                    dtype=np.int64,
                ),
            }
        ]
        Path(result_path).write_bytes(pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL))
        result_queue.put(
            (
                "ok",
                {
                    "result_path": result_path,
                    "backend_version": "fixture",
                    "trimesh_version": "fixture",
                    "vhacdx_version": "fixture",
                },
            )
        )

    monkeypatch.setattr(convex_decomposition, "_vhacd_worker", file_result_vhacd_worker)

    mesh = TriangleMesh(
        points=np.asarray(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        ),
        faces=np.asarray(
            [[0, 1, 2], [0, 3, 1], [1, 3, 2], [2, 3, 0]],
            dtype=np.int64,
        ),
    )

    package, metadata = build_convex_decomposition_package(
        mesh,
        role="fixture",
        baseline_id="vhacd_if_available",
        source_sha256="0" * 64,
        source_path="fixture.usd",
        max_hulls=8,
        phase0_section={"convex_decomposition": {"max_hulls": 8, "timeout_seconds": 1.0}},
        preferred_backends=("vhacd",),
    )

    assert package.method == "vhacd"
    assert metadata["hull_count"] == 1
