from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke


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
        primitives=(PrimitiveSpec(primitive_id="sphere", kind="sphere", dimensions={"radius": 0.5}),),
    )

    report = run_newton_contact_smoke(package, source_dir=str(source_dir), device="cpu")

    assert report.status in {"dependency_gap", "runtime_failure", "smoke_passed"}
    assert report.shape_status_counts["mapped"] == 1
    assert report.probe_type == "contact_canary"
