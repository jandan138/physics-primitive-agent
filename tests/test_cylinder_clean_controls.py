from primitive_collision_compiler.diagnostics.cylinder_clean_controls import (
    build_cylinder_clean_control_report,
)


def _run(status, labels=(), speed=0.0, support=-0.00001):
    return {
        "status": status,
        "failure_labels": list(labels),
        "final_linear_speed_mps": speed,
        "final_support_height": support,
    }


def test_clean_control_report_marks_geometry_alone_insufficient_and_compound_required():
    report = build_cylinder_clean_control_report(
        single_controls={
            "bed_cylinder_only_actual_axes": _run("smoke_passed"),
            "bed_box_only_actual_axes": _run("smoke_passed"),
            "franka_largest_cylinder_only": _run("smoke_passed"),
        },
        pair_controls=[
            {
                "rest_index": 0,
                "box": _run("runtime_failure", ["not_settled"], 9.5),
                "cylinder": _run("runtime_failure", ["not_settled"], 10.1),
            },
            {
                "rest_index": 3,
                "box": _run("smoke_passed"),
                "cylinder": _run("runtime_failure", ["floor_breach"], 0.0004, -0.2),
            },
            {
                "rest_index": 17,
                "box": _run("smoke_passed"),
                "cylinder": _run("smoke_passed"),
            },
        ],
        full_package_evidence={
            "bed_native_opt_in_drop": _run("runtime_failure", ["not_settled"], 0.0823),
            "bed_native_drop": _run("smoke_passed", speed=0.0404),
            "franka_native_opt_in_drop": _run("smoke_passed", speed=0.00071),
        },
        prior_evidence={
            "native_body_com_clears_bed_failure": True,
            "native_inertia_only_clears_bed_failure": True,
            "mass_only_clears_bed_failure": False,
        },
    )

    assert report["stage"] == "cylinder_clean_control_probe"
    assert report["status"] == "diagnostic_recorded"
    assert report["cause_assessment"]["geometry_alone"]["assessment"] == (
        "insufficient_as_sole_cause"
    )
    assert report["cause_assessment"]["compound_context"]["assessment"] == (
        "required_for_recorded_not_settled"
    )
    assert report["cause_assessment"]["pair_context"]["assessment"] == "mixed"
    assert report["cause_assessment"]["contact_or_floor_interaction"]["assessment"] == (
        "open_for_pair_controls_not_recorded_full_failure"
    )
    assert report["cause_assessment"]["com_inertia_body_state"]["assessment"] == (
        "still_strongest_current_hypothesis"
    )
    assert "not root-cause proof" in report["interpretation_boundary"]

