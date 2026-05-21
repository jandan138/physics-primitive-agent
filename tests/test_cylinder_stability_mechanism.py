from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.diagnostics.cylinder_stability import (
    build_cylinder_stability_mechanism_report,
    cylinder_geometry_from_package,
)


def _task_report(*, asset_role, lane_counts, lane_statuses):
    case = {
        "asset_role": asset_role,
        "asset_path": f"assets/{asset_role}.usd",
    }
    for lane, counts in lane_counts.items():
        case[lane] = {"primitive_kind_counts": counts}
        case[f"{lane}_contact"] = {"status": "smoke_passed"}
        drop_status, final_speed, failure_labels, final_contact_count = lane_statuses[lane]
        case[f"{lane}_tasks"] = {
            "drop_settle": {
                "status": drop_status,
                "drop_settle_runs": [
                    {
                        "failure_labels": failure_labels,
                        "final_linear_speed_mps": final_speed,
                        "final_contact_count": final_contact_count,
                        "final_support_height": -0.00001,
                    }
                ],
            },
            "sphere_rain": {"status": "smoke_passed"},
        }
    return {"stage": "newton_real_usd_native_task_comparison", "cases": [case]}


def test_cylinder_stability_report_narrows_bed_failure_to_full_compound_body_state():
    bed_report = _task_report(
        asset_role="bed_dev_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 31, "cylinder": 1},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.0404, [], 4),
            "native": ("smoke_passed", 0.0404, [], 4),
            "native_opt_in": ("runtime_failure", 0.0823, ["not_settled"], 4),
        },
    )
    franka_report = _task_report(
        asset_role="franka_import_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 25, "cylinder": 7},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.00075, [], 128),
            "native": ("smoke_passed", 0.00075, [], 128),
            "native_opt_in": ("smoke_passed", 0.00071, [], 117),
        },
    )

    report = build_cylinder_stability_mechanism_report(
        bed_task_report=bed_report,
        franka_task_report=franka_report,
        bed_cylinders=[
            {
                "primitive_index": 6,
                "radius": 2.700938098039964,
                "half_height": 0.21304234899547225,
                "half_height_radius_ratio": 0.07887716832535864,
                "source_faces": [32, 33, 34, 35, 36, 37, 38, 39],
            }
        ],
        franka_cylinders=[
            {
                "primitive_index": 16,
                "radius": 0.0019174147476461686,
                "half_height": 0.000012563167081109088,
                "half_height_radius_ratio": 0.0065521385482883755,
                "source_faces": [28, 29],
            }
        ],
        prior_evidence={
            "target_only_cylinder_reproduces_failure": False,
            "center_shift_alone_reproduces_failure": False,
            "final_support_contact_labels_match_controls": True,
            "native_body_com_clears_bed_failure": True,
            "native_inertia_only_clears_bed_failure": True,
            "mass_only_clears_bed_failure": False,
        },
    )

    assert report["stage"] == "cylinder_stability_mechanism_diagnosis"
    assert report["status"] == "diagnostic_recorded"
    assert report["observed_pattern"]["bed"]["native_opt_in_drop"]["status"] == (
        "runtime_failure"
    )
    assert report["observed_pattern"]["bed"]["native_opt_in_drop"]["failure_labels"] == [
        "not_settled"
    ]
    assert report["observed_pattern"]["franka"]["native_opt_in_drop"]["status"] == (
        "smoke_passed"
    )
    assert report["geometry_contrast"]["bed_max_cylinder_radius_m"] > 2.7
    assert report["geometry_contrast"]["franka_max_cylinder_radius_m"] < 0.002
    assert report["cause_assessment"]["mapping_or_contact_gap"]["assessment"] == "unlikely"
    assert report["cause_assessment"]["full_compound_context"]["assessment"] == "supported"
    assert report["cause_assessment"]["com_inertia_body_state"]["assessment"] == (
        "strongest_current_hypothesis"
    )
    assert report["current_hypothesis_status"] == "strongest_current_hypothesis"
    assert "not a validated repair" in report["interpretation_boundary"]


def test_cylinder_geometry_from_package_reports_mapped_cylinder_dimensions():
    package = CollisionPackage(
        asset_id="asset",
        package_id="pkg",
        primitives=(
            PrimitiveSpec(
                kind="box",
                primitive_id="asset:primitive:0",
                dimensions={"half_extents": [1.0, 1.0, 1.0]},
            ),
            PrimitiveSpec(
                kind="cylinder",
                primitive_id="asset:primitive:1",
                dimensions={"radius": 2.0, "half_height": 0.5, "axis_index": 1},
                source_faces=(3, 4),
            ),
        ),
    )

    assert cylinder_geometry_from_package(package) == [
        {
            "primitive_index": 1,
            "primitive_id": "asset:primitive:1",
            "source_faces": [3, 4],
            "radius": 2.0,
            "half_height": 0.5,
            "half_height_radius_ratio": 0.25,
            "axis_index": 1,
            "mapping_status": "mapped",
        }
    ]


def test_cylinder_stability_report_treats_missing_kind_counts_as_empty():
    bed_report = _task_report(
        asset_role="bed_dev_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 31, "cylinder": 1},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.0404, [], 4),
            "native": ("smoke_passed", 0.0404, [], 4),
            "native_opt_in": ("runtime_failure", 0.0823, ["not_settled"], 4),
        },
    )
    bed_report["cases"][0]["native_opt_in"]["primitive_kind_counts"] = None
    bed_report["cases"][0]["native_opt_in_tasks"]["drop_settle"]["drop_settle_runs"][0][
        "failure_labels"
    ] = "not_settled"
    franka_report = _task_report(
        asset_role="franka_import_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 25, "cylinder": 7},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.00075, [], 128),
            "native": ("smoke_passed", 0.00075, [], 128),
            "native_opt_in": ("smoke_passed", 0.00071, [], 117),
        },
    )

    report = build_cylinder_stability_mechanism_report(
        bed_task_report=bed_report,
        franka_task_report=franka_report,
        bed_cylinders=[],
        franka_cylinders=[],
    )

    assert report["observed_pattern"]["bed"]["native_opt_in_primitive_kind_counts"] == {}
    assert report["observed_pattern"]["bed"]["native_opt_in_drop"]["failure_labels"] == []


def test_cylinder_stability_report_selects_matching_asset_role_case():
    wrong_first_bed_report = _task_report(
        asset_role="franka_import_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 25, "cylinder": 7},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.00075, [], 128),
            "native": ("smoke_passed", 0.00075, [], 128),
            "native_opt_in": ("smoke_passed", 0.00071, [], 117),
        },
    )
    matching_bed_report = _task_report(
        asset_role="bed_dev_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 31, "cylinder": 1},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.0404, [], 4),
            "native": ("smoke_passed", 0.0404, [], 4),
            "native_opt_in": ("runtime_failure", 0.0823, ["not_settled"], 4),
        },
    )
    bed_report = {
        "stage": "newton_real_usd_native_task_comparison",
        "cases": [
            wrong_first_bed_report["cases"][0],
            matching_bed_report["cases"][0],
        ],
    }
    franka_report = _task_report(
        asset_role="franka_import_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 25, "cylinder": 7},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.00075, [], 128),
            "native": ("smoke_passed", 0.00075, [], 128),
            "native_opt_in": ("smoke_passed", 0.00071, [], 117),
        },
    )

    report = build_cylinder_stability_mechanism_report(
        bed_task_report=bed_report,
        franka_task_report=franka_report,
        bed_cylinders=[],
        franka_cylinders=[],
    )

    assert report["observed_pattern"]["bed"]["asset_role"] == "bed_dev_smoke"


def test_cylinder_stability_report_keeps_hypothesis_open_when_evidence_is_incomplete():
    bed_report = _task_report(
        asset_role="bed_dev_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 31, "cylinder": 1},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.0404, [], 4),
            "native": ("smoke_passed", 0.0404, [], 4),
            "native_opt_in": ("smoke_passed", 0.0400, [], 4),
        },
    )
    franka_report = _task_report(
        asset_role="franka_import_smoke",
        lane_counts={
            "legacy": {"box": 32},
            "native": {"box": 32},
            "native_opt_in": {"box": 25, "cylinder": 7},
        },
        lane_statuses={
            "legacy": ("smoke_passed", 0.00075, [], 128),
            "native": ("smoke_passed", 0.00075, [], 128),
            "native_opt_in": ("smoke_passed", 0.00071, [], 117),
        },
    )

    report = build_cylinder_stability_mechanism_report(
        bed_task_report=bed_report,
        franka_task_report=franka_report,
        bed_cylinders=[
            {
                "primitive_index": 6,
                "radius": 2.700938098039964,
                "half_height": 0.21304234899547225,
                "half_height_radius_ratio": 0.07887716832535864,
            }
        ],
        franka_cylinders=[],
    )

    assert report["cause_assessment"]["geometry_large_flat_cylinder"]["assessment"] == "open"
    assert report["current_hypothesis_status"] == "open"
    assert "best explained" not in report["current_hypothesis"]
