import sys
import types

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import (
    _add_static_shape,
    _import_newton_runtime,
    _probe_radius,
    run_newton_contact_smoke,
)
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


def test_newton_contact_smoke_reports_mapping_gap_without_supported_shapes():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="bad", kind="mesh", dimensions={}),),
    )

    report = run_newton_contact_smoke(package, source_dir="/missing/newton", device="cpu")

    assert report.stage == "newton_contact_smoke"
    assert report.status == "mapping_gap"
    assert report.asset_id == "asset"
    assert report.shape_status_counts["mapping_gap"] == 1


def test_newton_contact_smoke_reports_dependency_gap_after_mapping_passes(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.5}),
        ),
    )

    report = run_newton_contact_smoke(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.shape_status_counts["mapped"] == 1
    assert report.probe_type == "contact_canary"


def test_newton_runtime_import_prefers_source_dir_over_cached_module(tmp_path, monkeypatch):
    wrong_newton = types.ModuleType("newton")
    wrong_newton.__file__ = "/tmp/wrong-newton/newton/__init__.py"
    monkeypatch.setitem(sys.modules, "newton", wrong_newton)
    monkeypatch.setitem(sys.modules, "warp", types.ModuleType("warp"))
    source_dir = tmp_path / "source-newton"
    package_dir = source_dir / "newton"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text("MARKER = 'source-dir-newton'\n", encoding="utf-8")

    runtime = _import_newton_runtime(str(source_dir))

    assert runtime.status == "smoke_passed"
    assert runtime.newton is not wrong_newton
    assert getattr(runtime.newton, "MARKER") == "source-dir-newton"
    assert str(source_dir) in str(runtime.newton.__file__)


def test_newton_contact_smoke_maps_import_error_to_runtime_failure(tmp_path):
    source_dir = tmp_path / "broken-newton"
    package_dir = source_dir / "newton"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.5}),
        ),
    )

    report = run_newton_contact_smoke(package, source_dir=str(source_dir), device="cpu")

    assert report.status == "runtime_failure"
    assert report.fallback_reason == "import_error"


def test_newton_contact_smoke_reports_representative_canary_scope(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="box",
                kind="box",
                dimensions={"half_extents": [1.0, 1.0, 1.0]},
            ),
            PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.5}),
            PrimitiveSpec(primitive_id="sphere-2", kind="sphere", dimensions={"radius": 0.25}),
        ),
    )

    report = run_newton_contact_smoke(package, source_dir=str(source_dir), device="cpu")

    payload = report.to_dict()
    assert payload["metrics"]["contact_canary_scope"] == "one_representative_per_mapped_type"
    assert payload["metrics"]["mapped_primitive_count"] == 3
    assert payload["metrics"]["mapped_type_count"] == 2
    assert payload["metrics"]["full_package_contact_coverage"] is False


def test_contact_canary_builds_newton_native_static_shapes():
    builder = _RecordingBuilder()
    wp = _FakeWarp()
    mappings = (
        _mapping(
            "cylinder0",
            "cylinder",
            {"radius": 0.3, "half_height": 0.8, "axis_index": 1},
        ),
        _mapping(
            "cone0",
            "cone",
            {"radius": 0.4, "half_height": 0.9, "axis_index": 0},
        ),
        _mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]}),
    )

    for mapping in mappings:
        _add_static_shape(builder, mapping, wp)

    assert [call[0] for call in builder.calls] == ["cylinder", "cone", "ellipsoid"]
    assert builder.calls[0][1]["body"] == -1
    assert builder.calls[0][1]["radius"] == 0.3
    assert builder.calls[1][1]["half_height"] == 0.9
    assert builder.calls[2][1]["rx"] == 0.2
    assert builder.calls[2][1]["ry"] == 0.4
    assert builder.calls[2][1]["rz"] == 0.6


def test_contact_canary_probe_radius_uses_native_bundle_dimensions():
    assert _probe_radius(
        _mapping("cylinder0", "cylinder", {"radius": 0.3, "half_height": 0.8})
    ) == 0.15
    assert _probe_radius(_mapping("cone0", "cone", {"radius": 0.4, "half_height": 0.9})) == 0.2
    assert _probe_radius(_mapping("ellipsoid0", "ellipsoid", {"radii": [0.2, 0.4, 0.6]})) == 0.1


def _mapping(
    primitive_id: str,
    kind: str,
    dimensions: dict[str, object],
    *,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> NewtonShapeMapping:
    return NewtonShapeMapping(
        primitive_id=primitive_id,
        kind=kind,
        status="mapped",
        detail="mapped",
        center=center,
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions=dimensions,
    )


class _RecordingBuilder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def add_shape_cylinder(self, **kwargs):
        self.calls.append(("cylinder", kwargs))

    def add_shape_cone(self, **kwargs):
        self.calls.append(("cone", kwargs))

    def add_shape_ellipsoid(self, **kwargs):
        self.calls.append(("ellipsoid", kwargs))


class _FakeWarp:
    def vec3(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        return (x, y, z)

    def matrix_from_cols(self, *cols):
        return cols

    def quat_from_matrix(self, matrix):
        return ("quat", matrix)

    def transform(self, position, rotation):
        return {"position": position, "rotation": rotation}
