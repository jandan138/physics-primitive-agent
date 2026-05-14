import sys
import types

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import (
    _import_newton_runtime,
    run_newton_contact_smoke,
)


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
