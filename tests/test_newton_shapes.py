from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.newton.shapes import map_package_shapes


def test_map_package_shapes_accepts_box_sphere_capsule_without_importing_newton():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="box0",
                kind="box",
                dimensions={"half_extents": [1.0, 2.0, 3.0]},
            ),
            PrimitiveSpec(
                primitive_id="sphere0",
                kind="sphere",
                dimensions={"radius": 0.5},
            ),
            PrimitiveSpec(
                primitive_id="capsule0",
                kind="capsule",
                dimensions={"radius": 0.25, "half_height": 1.0, "axis_index": 2},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapped", "mapped", "mapped"]
    assert [mapping.kind for mapping in mappings] == ["box", "sphere", "capsule"]


def test_map_package_shapes_reports_mapping_gap_for_bad_dimensions():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="bad", kind="sphere", dimensions={}),),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "radius" in mappings[0].detail
