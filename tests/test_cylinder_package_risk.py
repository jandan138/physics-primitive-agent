import math

import pytest

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.diagnostics.cylinder_package_risk import (
    build_cylinder_package_body_state_risk_report,
    package_body_state_proxy,
)


def _box(primitive_id, *, center, half_extents, volume=None):
    if volume is None:
        volume = 8.0 * math.prod(half_extents)
    return PrimitiveSpec(
        kind="box",
        primitive_id=primitive_id,
        center=tuple(center),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={"half_extents": list(half_extents)},
        volume=volume,
        weighted_volume=volume,
    )


def _cylinder(primitive_id, *, center, radius, half_height, axis_index=0, volume=None):
    if volume is None:
        volume = 2.0 * math.pi * radius * radius * half_height
    return PrimitiveSpec(
        kind="cylinder",
        primitive_id=primitive_id,
        center=tuple(center),
        axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        dimensions={
            "axis_index": axis_index,
            "half_height": half_height,
            "radius": radius,
        },
        volume=volume,
        weighted_volume=volume,
    )


def _package(package_id, primitives):
    return CollisionPackage(
        asset_id=package_id,
        package_id=package_id,
        primitives=tuple(primitives),
        claim_boundary="test_package_not_collision_quality",
    )


def _drop(status, labels=(), speed=0.0):
    return {
        "status": status,
        "failure_labels": list(labels),
        "final_linear_speed_mps": speed,
    }


def test_package_body_state_proxy_uses_volume_weighted_geometry():
    package = _package(
        "two_boxes",
        (
            _box("left", center=(-1.0, 0.0, 0.0), half_extents=(0.5, 0.5, 0.5)),
            _box("right", center=(1.0, 0.0, 0.0), half_extents=(0.5, 0.5, 0.5)),
        ),
    )

    proxy = package_body_state_proxy(package)

    assert proxy["mass_proxy"] == pytest.approx(2.0)
    assert proxy["com_proxy"] == pytest.approx([0.0, 0.0, 0.0])
    assert proxy["inertia_proxy_trace"] > 0.0
    assert proxy["cylinder_summary"]["cylinder_count"] == 0
    assert proxy["evidence_inputs"]["uses_newton_model_arrays"] is False


def test_package_risk_report_flags_bed_like_case_not_franka_like():
    bed_native = _package(
        "bed_native",
        (
            _box(
                "bed_rest",
                center=(-53.5, 25.7, -64.0),
                half_extents=(4.0, 4.0, 4.0),
                volume=570.0,
            ),
            _box(
                "bed_target_box",
                center=(-77.5396449852579, 31.80276279341078, 89.88358058121636),
                half_extents=(0.21304234899546515, 2.312191407929859, 2.192086176186713),
                volume=8.638480063523374,
            ),
        ),
    )
    bed_opt_in = _package(
        "bed_opt_in",
        (
            bed_native.primitives[0],
            _cylinder(
                "bed_target_cylinder",
                center=(-77.31794835914295, 32.11800343592774, 89.83193356104442),
                radius=2.700938098039964,
                half_height=0.21304234899547225,
                volume=9.765063505799915,
            ),
        ),
    )
    franka_native = _package(
        "franka_native",
        (
            _box(
                "franka_rest",
                center=(-0.02, -0.06, 0.03),
                half_extents=(0.002, 0.002, 0.002),
            ),
            _box(
                "franka_target_box",
                center=(-0.018, -0.065, 0.033),
                half_extents=(0.001, 0.001, 0.00002),
            ),
        ),
    )
    franka_opt_in = _package(
        "franka_opt_in",
        (
            franka_native.primitives[0],
            _cylinder(
                "franka_target_cylinder",
                center=(-0.0172, -0.0651, 0.0331),
                radius=0.0019174147476461686,
                half_height=0.000012563167081109088,
            ),
        ),
    )

    report = build_cylinder_package_body_state_risk_report(
        cases={
            "bed": {
                "native": bed_native,
                "native_opt_in": bed_opt_in,
                "drop_evidence": _drop("runtime_failure", ["not_settled"], 0.082304),
            },
            "franka": {
                "native": franka_native,
                "native_opt_in": franka_opt_in,
                "drop_evidence": _drop("smoke_passed", speed=0.0007108),
            },
        },
    )

    assert report["stage"] == "cylinder_package_body_state_risk_probe"
    assert report["status"] == "diagnostic_recorded"
    assert report["evidence_inputs"]["uses_newton_model_arrays"] is False
    assert report["case_assessments"]["bed"]["package_risk_class"] == (
        "large_flat_cylinder_body_state_delta_risk"
    )
    assert report["case_assessments"]["bed"]["risk_flags"] == {
        "large_absolute_cylinder": True,
        "large_flat_cylinder": True,
        "package_com_delta": True,
        "package_inertia_delta": True,
    }
    assert report["case_assessments"]["franka"]["package_risk_class"] == "not_flagged"
    assert report["contrast_assessment"]["assessment"] == (
        "bed_flagged_franka_not_flagged_matches_recorded_drop_contrast"
    )
    assert "not a validated repair" in report["interpretation_boundary"]
