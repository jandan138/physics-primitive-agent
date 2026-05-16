import json
import math

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


def test_map_package_shapes_accepts_complete_newton_native_bundle_without_importing_newton():
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
            PrimitiveSpec(
                primitive_id="cylinder0",
                kind="cylinder",
                dimensions={"radius": 0.3, "half_height": 0.8, "axis_index": 1},
            ),
            PrimitiveSpec(
                primitive_id="cone0",
                kind="cone",
                dimensions={"radius": 0.4, "half_height": 0.9, "axis_index": 0},
            ),
            PrimitiveSpec(
                primitive_id="ellipsoid0",
                kind="ellipsoid",
                dimensions={"radii": [0.2, 0.4, 0.6]},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapped"] * 6
    assert [mapping.kind for mapping in mappings] == [
        "box",
        "sphere",
        "capsule",
        "cylinder",
        "cone",
        "ellipsoid",
    ]
    json.dumps([mapping.to_dict() for mapping in mappings], allow_nan=False)


def test_map_package_shapes_reports_mapping_gap_for_bad_dimensions():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(PrimitiveSpec(primitive_id="bad", kind="sphere", dimensions={}),),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "radius" in mappings[0].detail


def test_map_package_shapes_rejects_bad_native_bundle_dimensions():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="bad-cylinder-radius",
                kind="cylinder",
                dimensions={"radius": 0.0, "half_height": 1.0},
            ),
            PrimitiveSpec(
                primitive_id="bad-cylinder-axis",
                kind="cylinder",
                dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": 4},
            ),
            PrimitiveSpec(
                primitive_id="bad-cone-height",
                kind="cone",
                dimensions={"radius": 0.3, "half_height": -1.0},
            ),
            PrimitiveSpec(
                primitive_id="bad-capsule-axis-bool",
                kind="capsule",
                dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": True},
            ),
            PrimitiveSpec(
                primitive_id="bad-cylinder-axis-float",
                kind="cylinder",
                dimensions={"radius": 0.3, "half_height": 1.0, "axis_index": 1.0},
            ),
            PrimitiveSpec(
                primitive_id="bad-ellipsoid-radii",
                kind="ellipsoid",
                dimensions={"radii": [0.2, math.inf, 0.6]},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapping_gap"] * 6
    assert "cylinder radius" in mappings[0].detail
    assert "cylinder axis_index" in mappings[1].detail
    assert "cone half_height" in mappings[2].detail
    assert "capsule axis_index" in mappings[3].detail
    assert "cylinder axis_index" in mappings[4].detail
    assert "ellipsoid radii" in mappings[5].detail


def test_map_package_shapes_keeps_capped_cylinder_as_mapping_gap():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="capped-cylinder0",
                kind="capped_cylinder",
                dimensions={
                    "radius": 0.25,
                    "half_height": 1.0,
                    "axis_index": 0,
                    "cap_model": "hemisphere_caps",
                    "proxy_fit": "axis_span_radial_proxy",
                },
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "unsupported primitive kind: capped_cylinder" in mappings[0].detail


def test_map_package_shapes_keeps_paper_only_primitives_as_mapping_gaps():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="frustum0",
                kind="frustum",
                dimensions={"height": 1.0, "top_radius": 0.25, "bottom_radius": 0.5},
            ),
            PrimitiveSpec(
                primitive_id="trapezoid0",
                kind="trapezoidal_prism",
                dimensions={"h_x": 1.0, "h_y": 0.5, "h_zt": 0.25, "h_zb": 0.5},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapping_gap", "mapping_gap"]
    assert "unsupported primitive kind: frustum" in mappings[0].detail
    assert "unsupported primitive kind: trapezoidal_prism" in mappings[1].detail


def test_map_package_shapes_rejects_nonfinite_values_and_bad_axes():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="bad-dimension",
                kind="box",
                dimensions={"half_extents": [1.0, math.inf, 3.0]},
            ),
            PrimitiveSpec(
                primitive_id="bad-center",
                kind="sphere",
                center=(0.0, math.nan, 0.0),
                dimensions={"radius": 0.5},
            ),
            PrimitiveSpec(
                primitive_id="bad-axes",
                kind="capsule",
                axes=((1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
                dimensions={"radius": 0.25, "half_height": 1.0, "axis_index": 2},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert [mapping.status for mapping in mappings] == ["mapping_gap", "mapping_gap", "mapping_gap"]
    assert "finite" in mappings[0].detail
    assert "center" in mappings[1].detail
    assert "axes" in mappings[2].detail
    json.dumps([mapping.to_dict() for mapping in mappings], allow_nan=False)


def test_map_package_shapes_rejects_left_handed_axes():
    package = CollisionPackage(
        package_id="pkg",
        asset_id="asset",
        primitives=(
            PrimitiveSpec(
                primitive_id="left-handed",
                kind="box",
                axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)),
                dimensions={"half_extents": [1.0, 1.0, 1.0]},
            ),
        ),
    )

    mappings = map_package_shapes(package)

    assert mappings[0].status == "mapping_gap"
    assert "axes" in mappings[0].detail
