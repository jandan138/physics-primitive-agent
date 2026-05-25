from primitive_collision_compiler.contracts import (
    CollisionPackage,
    CompileConfig,
    CompileReport,
    FallbackSpec,
    PrimitiveSpec,
)


def test_compile_config_defaults_are_conservative():
    config = CompileConfig(asset_path="assets/example.usda", task="grasping")

    assert config.method == "primitive_first"
    assert config.max_primitives == 16
    assert config.allowed_fallback == ("coacd", "sdf")


def test_compile_report_marks_dry_run_not_compiled():
    report = CompileReport(asset_id="example", task="grasping", dry_run=True).to_dict()

    assert report["status"] == "dry_run"
    assert report["compiled"] is False


def test_collision_package_preserves_legacy_positional_construction():
    primitive = PrimitiveSpec("box")
    fallback = FallbackSpec("convex_hull", "unsupported primitive")

    package = CollisionPackage("asset", (primitive,), fallback)

    assert package.asset_id == "asset"
    assert package.primitives == (primitive,)
    assert package.fallback == fallback
    assert package.package_id == ""


def test_primitive_spec_serializes_source_links_for_robot_packages():
    primitive = PrimitiveSpec(
        "box",
        primitive_id="robot:link0:box0",
        frame="/Robot/link0",
        source_links=("/Robot/link0",),
    )

    payload = primitive.to_dict()

    assert payload["frame"] == "/Robot/link0"
    assert payload["source_links"] == ["/Robot/link0"]


def test_primitive_spec_omits_empty_source_links_for_legacy_schema():
    payload = PrimitiveSpec("box").to_dict()

    assert "source_links" not in payload
