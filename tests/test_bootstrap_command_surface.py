import importlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from primitive_collision_compiler.contracts import CollisionPackage, PrimitiveSpec
from primitive_collision_compiler.reports.schema import NewtonShapeMapping


def _load_bed_native_opt_in_trace_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "diagnostics"
        / "bed_native_opt_in_compound_trace.py"
    )
    spec = importlib.util.spec_from_file_location("bed_native_opt_in_compound_trace", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_bed_native_opt_in_frame_transition_audit_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "diagnostics"
        / "bed_native_opt_in_frame_transition_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "bed_native_opt_in_frame_transition_audit", script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_bed_native_opt_in_clean_frame_blocker_audit_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "diagnostics"
        / "bed_native_opt_in_clean_frame_blocker_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "bed_native_opt_in_clean_frame_blocker_audit", script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_bed_native_opt_in_model_build_delta_audit_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "diagnostics"
        / "bed_native_opt_in_model_build_delta_audit.py"
    )
    spec = importlib.util.spec_from_file_location(
        "bed_native_opt_in_model_build_delta_audit", script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_package_imports():
    package = importlib.import_module("primitive_collision_compiler")

    assert package.__version__ == "0.1.0"


def test_docs_validation_stub_returns_success():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "validate_docs.py"
    spec = importlib.util.spec_from_file_location("validate_docs", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.main() in (0, None)


def test_bed_native_opt_in_compound_trace_script_has_bounded_help():
    module = _load_bed_native_opt_in_trace_module()

    help_text = module.build_parser().format_help()

    assert "full-compound Newton body/contact trace" in help_text
    assert "bed_native_opt_in_probe.yaml" in help_text
    assert "--run-inertia-counterfactual" in help_text
    assert "--run-inertia-field-ablation" in help_text
    assert "--run-com-axis-ablation" in help_text
    assert "--run-com-blend-ablation" in help_text
    assert "--run-com-blend-refinement" in help_text
    assert "--run-model-build-audit" in help_text
    assert module._COM_AXIS_VARIANTS[
        "native_opt_in_cylinder_with_native_box_com_xz"
    ] == (0, 2)
    assert module._COM_BLEND_FRACTIONS == (0.0, 0.25, 0.5, 0.75, 1.0)
    assert module._COM_BLEND_VARIANTS[
        "native_opt_in_cylinder_with_native_box_com_xz_blend_050"
    ] == {"axes": (0, 2), "fraction": 0.5}
    assert module._COM_BLEND_REFINEMENT_FRACTIONS == (
        0.75,
        0.875,
        0.9375,
        0.96875,
        0.984375,
        1.0,
    )
    assert module._COM_BLEND_REFINEMENT_VARIANTS[
        "native_opt_in_cylinder_with_native_box_com_xz_refine_0875"
    ] == {"axes": (0, 2), "fraction": 0.875}
    assert module._COM_BLEND_REFINEMENT_VARIANTS[
        "native_opt_in_cylinder_with_native_box_com_refine_09375"
    ] == {"axes": (0, 1, 2), "fraction": 0.9375}
    expected_refinement_keys = {
        f"native_opt_in_cylinder_with_native_box_com_refine_{token}"
        for token in ("075", "0875", "09375", "096875", "0984375", "1")
    } | {
        f"native_opt_in_cylinder_with_native_box_com_xz_refine_{token}"
        for token in ("075", "0875", "09375", "096875", "0984375", "1")
    }
    assert set(module._COM_BLEND_REFINEMENT_VARIANTS) == expected_refinement_keys


def test_body_com_blend_array_interpolates_selected_axes():
    module = _load_bed_native_opt_in_trace_module()

    blended = module._body_com_blend_array(
        target_array=[[10.0, 20.0, 30.0]],
        source_array=[[2.0, 4.0, 6.0]],
        axes=(0, 2),
        fraction=0.25,
    )

    assert blended.tolist() == [[8.0, 20.0, 24.0]]


def test_com_blend_override_leaves_mass_and_inertia_fields_unchanged():
    module = _load_bed_native_opt_in_trace_module()

    class FakeArray:
        def __init__(self, values):
            self.values = np.asarray(values, dtype=float)

        def numpy(self):
            return self.values.copy()

        def assign(self, values):
            self.values = np.asarray(values, dtype=float)

    fake_model = SimpleNamespace(
        body_count=1,
        shape_count=1,
        body_mass=FakeArray([11.0]),
        body_inv_mass=FakeArray([0.09090909]),
        body_com=FakeArray([[10.0, 20.0, 30.0]]),
        body_inertia=FakeArray([[[1.0, 2.0, 3.0], [2.0, 5.0, 6.0], [3.0, 6.0, 9.0]]]),
        body_inv_inertia=FakeArray([[[9.0, 8.0, 7.0], [8.0, 5.0, 4.0], [7.0, 4.0, 1.0]]]),
        shape_body=FakeArray([0.0]),
        shape_scale=FakeArray([[1.0, 1.0, 1.0]]),
        shape_material_mu=FakeArray([0.5]),
    )
    before = {
        "body_mass": fake_model.body_mass.numpy().tolist(),
        "body_inv_mass": fake_model.body_inv_mass.numpy().tolist(),
        "body_inertia": fake_model.body_inertia.numpy().tolist(),
        "body_inv_inertia": fake_model.body_inv_inertia.numpy().tolist(),
    }

    report = module._apply_inertial_override(
        fake_model,
        inertial_override={
            "source_variant": "native_control_box",
            "source_package_id": "native",
            "source_anchor": [0.0, 0.0, 0.0],
            "arrays": {
                "body_com": np.asarray([[2.0, 4.0, 6.0]]),
                "body_mass": np.asarray([99.0]),
                "body_inv_mass": np.asarray([99.0]),
                "body_inertia": np.asarray([[[99.0, 0.0, 0.0]]]),
                "body_inv_inertia": np.asarray([[[99.0, 0.0, 0.0]]]),
            },
        },
        target_anchor=(0.0, 0.0, 0.0),
        fields=("body_com",),
        body_com_axes=(0, 2),
        body_com_blend_fraction=0.25,
    )

    assert fake_model.body_com.numpy().tolist() == [[8.0, 20.0, 24.0]]
    assert fake_model.body_mass.numpy().tolist() == before["body_mass"]
    assert fake_model.body_inv_mass.numpy().tolist() == before["body_inv_mass"]
    assert fake_model.body_inertia.numpy().tolist() == before["body_inertia"]
    assert fake_model.body_inv_inertia.numpy().tolist() == before["body_inv_inertia"]
    assert report["fields"] == ["body_com"]
    assert report["body_com_axes"] == [0, 2]
    assert report["body_com_blend_fraction"] == 0.25


def test_com_blend_ablation_and_refinement_wire_body_com_only(monkeypatch):
    module = _load_bed_native_opt_in_trace_module()
    native_package = CollisionPackage(
        asset_id="asset",
        package_id="native",
        primitives=(
            PrimitiveSpec(
                kind="box",
                primitive_id="native:p0",
                source_faces=(0,),
                center=(0.0, 0.0, 0.0),
            ),
        ),
    )
    opt_in_package = CollisionPackage(
        asset_id="asset",
        package_id="opt_in",
        primitives=(
            PrimitiveSpec(
                kind="cylinder",
                primitive_id="opt_in:p0",
                source_faces=(0,),
                center=(0.0, 0.0, 0.0),
            ),
        ),
    )
    artifact = SimpleNamespace(
        native=SimpleNamespace(package=native_package),
        native_opt_in=SimpleNamespace(package=opt_in_package),
    )

    class FakeDropOptions:
        step_dt_seconds = 0.01

        def to_solver_dict(self):
            return {"solver": "fake"}

        def to_initial_conditions(self):
            return {"initial": "fake"}

    captured = []

    def fake_trace_package(package, **kwargs):
        captured.append((package, kwargs))
        return {
            "status": "smoke_passed",
            "type_counts": {"fake": 1},
            "model_summary": {"body_mass": [1.0], "body_com": [[0.0, 0.0, 0.0]]},
            "drop_settle_run": {
                "status": "smoke_passed",
                "failure_labels": [],
                "final_linear_speed_mps": 0.0,
                "final_contact_count": 1,
                "final_support_height": 0.0,
                "max_contact_count": 1,
            },
        }

    monkeypatch.setattr(module, "load_compile_config", lambda path: SimpleNamespace(protocol={}))
    monkeypatch.setattr(module, "_real_usd_native_comparison_options", lambda config: {})
    monkeypatch.setattr(module, "build_real_usd_native_artifacts", lambda **kwargs: (artifact,))
    monkeypatch.setattr(module, "_newton_drop_settle_options", lambda section: {"options": FakeDropOptions()})
    monkeypatch.setattr(module, "_import_newton_runtime", lambda source_dir: SimpleNamespace(status="smoke_passed"))
    monkeypatch.setattr(module, "_snapshot_inertial_override", lambda *args, **kwargs: {"arrays": {}})
    monkeypatch.setattr(module, "_trace_package", fake_trace_package)

    report = module.build_compound_trace_report(
        config_path=Path("fake.yaml"),
        source_dir="/fake/newton",
        device="cpu",
        target_index=0,
        sample_every_steps=1,
        tail_steps=0,
        max_contact_details=0,
        run_com_blend_ablation=True,
    )

    blend_calls = {
        name: payload
        for name, (_, payload) in zip(report["variants"], captured, strict=True)
        if name in module._COM_BLEND_VARIANTS
    }
    assert report["counterfactuals"]["com_blend_ablation_enabled"] is True
    assert report["counterfactuals"]["com_blend_ablation_variants"][
        "native_opt_in_cylinder_with_native_box_com_xz_blend_050"
    ] == {"field": "body_com", "axes": [0, 2], "fraction": 0.5}
    assert blend_calls
    for package, kwargs in captured:
        if kwargs["inertial_override_com_blend_fraction"] is not None:
            assert package is opt_in_package
            assert kwargs["inertial_override_fields"] == ("body_com",)
            assert kwargs["inertial_override_fields"] != module._INERTIAL_FIELDS

    captured.clear()
    refinement_report = module.build_compound_trace_report(
        config_path=Path("fake.yaml"),
        source_dir="/fake/newton",
        device="cpu",
        target_index=0,
        sample_every_steps=1,
        tail_steps=0,
        max_contact_details=0,
        run_com_blend_refinement=True,
    )

    refinement_calls = {
        name: payload
        for name, (_, payload) in zip(refinement_report["variants"], captured, strict=True)
        if name in module._COM_BLEND_REFINEMENT_VARIANTS
    }
    assert refinement_report["counterfactuals"]["com_blend_refinement_enabled"] is True
    assert refinement_report["counterfactuals"]["com_blend_ablation_enabled"] is False
    assert refinement_report["counterfactuals"]["com_blend_ablation_variants"] == {}
    assert refinement_report["counterfactuals"]["com_blend_refinement_variants"][
        "native_opt_in_cylinder_with_native_box_com_xz_refine_0875"
    ] == {"field": "body_com", "axes": [0, 2], "fraction": 0.875}
    assert refinement_calls
    for package, kwargs in captured:
        if kwargs["inertial_override_com_blend_fraction"] is not None:
            assert package is opt_in_package
            assert kwargs["inertial_override_fields"] == ("body_com",)
            assert kwargs["inertial_override_fields"] != module._INERTIAL_FIELDS


def test_com_blend_refinement_main_forwards_flag(monkeypatch, tmp_path, capsys):
    module = _load_bed_native_opt_in_trace_module()
    captured = {}

    def fake_build_compound_trace_report(**kwargs):
        captured.update(kwargs)
        return {
            "stage": "bed_native_opt_in_compound_trace_diagnostic",
            "status": "diagnostic_recorded",
        }

    monkeypatch.setenv("NEWTON_SOURCE_DIR", "/fake/newton")
    monkeypatch.setattr(module, "build_compound_trace_report", fake_build_compound_trace_report)

    output = tmp_path / "report.json"
    assert module.main(["--run-com-blend-refinement", "--output", str(output)]) == 0

    assert captured["run_com_blend_refinement"] is True
    assert captured["run_com_blend_ablation"] is False
    assert json.loads(output.read_text())["status"] == "diagnostic_recorded"
    assert json.loads(capsys.readouterr().out)["status"] == "diagnostic_recorded"


def test_tail_linear_speed_summary_filters_tail_window():
    module = _load_bed_native_opt_in_trace_module()

    summary = module._tail_linear_speed_summary(
        [
            {"step": 0, "linear_speed_mps": 9.0},
            {"step": 10, "linear_speed_mps": 0.06},
            {"step": 11, "linear_speed_mps": 0.04},
            {"step": 12, "linear_speed_mps": 0.02},
            {"step": 12, "linear_speed_mps": "bad"},
        ],
        tail_start_step=10,
        step_dt_seconds=0.25,
        max_settle_linear_speed_mps=0.05,
    )

    assert summary == {
        "sample_count": 3,
        "max_linear_speed_mps": 0.06,
        "mean_linear_speed_mps": 0.04,
        "min_linear_speed_mps": 0.02,
        "over_settle_threshold_count": 1,
        "final_below_settle_threshold_sample_count": 2,
        "final_below_settle_threshold_seconds": 0.5,
        "max_settle_linear_speed_mps": 0.05,
    }


def test_compound_trace_main_json_safes_non_finite_report_values(monkeypatch, tmp_path, capsys):
    module = _load_bed_native_opt_in_trace_module()

    def fake_build_compound_trace_report(**kwargs):
        return {
            "stage": "bed_native_opt_in_compound_trace_diagnostic",
            "status": "diagnostic_recorded",
            "trace_samples": [
                {
                    "linear_speed_mps": float("nan"),
                    "body_position": [1.0, float("inf"), -float("inf")],
                }
            ],
        }

    monkeypatch.setenv("NEWTON_SOURCE_DIR", "/fake/newton")
    monkeypatch.setattr(module, "build_compound_trace_report", fake_build_compound_trace_report)

    output = tmp_path / "report.json"
    assert module.main(["--output", str(output)]) == 0

    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text())
    assert stdout_payload == file_payload
    assert stdout_payload["trace_samples"] == [
        {"body_position": [1.0, None, None], "linear_speed_mps": None}
    ]
    json.dumps(stdout_payload, allow_nan=False)


def test_model_build_delta_summary_blocks_anchor_mismatch():
    module = _load_bed_native_opt_in_trace_module()

    summary = module._model_build_delta_summary(
        {},
        anchor_match=False,
        native_anchor=[0.0, 0.0, 0.0],
        opt_in_anchor=[1.0, 0.0, 0.0],
    )

    assert summary == {
        "status": "anchor_mismatch",
        "fallback_reason": "model_build_delta_requires_matching_package_anchors",
        "native_anchor": [0.0, 0.0, 0.0],
        "native_opt_in_anchor": [1.0, 0.0, 0.0],
    }


def test_model_build_audit_returns_nested_mapping_gap(monkeypatch):
    module = _load_bed_native_opt_in_trace_module()
    package = CollisionPackage(
        asset_id="asset",
        package_id="pkg",
        primitives=(PrimitiveSpec(kind="capped_cylinder", primitive_id="p0"),),
    )
    mapping = NewtonShapeMapping(
        primitive_id="p0",
        kind="capped_cylinder",
        status="mapping_gap",
        detail="unsupported primitive",
        center=(0.0, 0.0, 0.0),
        dimensions={},
    )
    runtime = SimpleNamespace(
        status="smoke_passed",
        environment=SimpleNamespace(
            status="smoke_passed",
            to_dict=lambda: {"status": "smoke_passed"},
        ),
    )
    monkeypatch.setattr(module, "map_package_shapes", lambda package: (mapping,))

    audit = module._build_model_build_audit(
        native_package=package,
        opt_in_package=package,
        target_index=0,
        runtime=runtime,
        device="cpu",
    )

    assert audit["status"] == "mapping_gap"
    assert audit["fallback_reason"] == "full_package_shape_coverage_required"
    assert audit["native_mapping_status_counts"] == {"mapping_gap": 1}
    assert audit["native_opt_in_mapping_status_counts"] == {"mapping_gap": 1}


def test_model_piece_delta_is_json_serializable():
    module = _load_bed_native_opt_in_trace_module()

    delta = module._model_piece_delta(
        {
            "model_summary": {
                "body_mass": [3.0],
                "body_com": [[1.0, 2.0, 3.0]],
                "body_inertia": [[[4.0, 5.0, 6.0]]],
            },
        },
        {
            "model_summary": {
                "body_mass": [1.0],
                "body_com": [[0.5, 1.5, 2.5]],
                "body_inertia": [[[3.0, 2.0, 1.0]]],
            },
        },
    )

    assert delta == {
        "body_mass_delta": 2.0,
        "body_com_delta": [0.5, 0.5, 0.5],
        "body_inertia_row0_delta": [1.0, 3.0, 5.0],
    }
    json.dumps(delta, allow_nan=False)


def test_frame_transition_audit_records_clean_to_dirty_control_with_matching_model_and_contacts(tmp_path):
    module = _load_bed_native_opt_in_frame_transition_audit_module()

    def report(frame, status, failure_labels, speed, velocity, position):
        penultimate_speed = round(speed - 0.01, 2)
        penultimate_velocity = [value - 0.01 for value in velocity]
        penultimate_position = [position[0] - 0.5, position[1] + 0.5, position[2]]
        return {
            "status": "diagnostic_recorded",
            "drop_settle_options": {"frames": frame},
            "variants": {
                "native_control_box": {
                    "status": status,
                    "type_counts": {"box": 32},
                    "package_anchor": [1.0, 2.0, 3.0],
                    "model_summary": {
                        "body_mass": [10.0],
                        "body_inv_mass": [0.1],
                        "body_com": [[1.0, 2.0, 3.0]],
                        "body_inertia": [[[4.0, 0.0, 0.0]]],
                        "body_inv_inertia": [[[0.25, 0.0, 0.0]]],
                    },
                    "drop_settle_run": {
                        "status": status,
                        "failure_labels": failure_labels,
                        "completed_steps": frame * 8,
                        "final_linear_speed_mps": speed,
                        "final_linear_velocity": velocity,
                        "final_support_height": -0.001,
                        "final_contact_count": 2,
                    },
                    "trace_samples": [
                        {
                            "step": frame * 8 - 1,
                            "phase": "post_step",
                            "linear_speed_mps": penultimate_speed,
                            "linear_velocity_mps": penultimate_velocity,
                            "angular_velocity_raw": [0.1, 0.2, 0.3],
                            "body_position": penultimate_position,
                            "support_height": -0.002,
                            "contact_count": 2,
                            "contact_details": [
                                {"shape1_label": "bed_dev_smoke_native:primitive:12"},
                                {"shape1_label": "bed_dev_smoke_native:primitive:15"},
                            ],
                        },
                        {
                            "step": frame * 8,
                            "phase": "post_step",
                            "linear_speed_mps": speed,
                            "linear_velocity_mps": velocity,
                            "angular_velocity_raw": [0.0, 0.0, 0.0],
                            "body_position": position,
                            "support_height": -0.001,
                            "contact_count": 2,
                            "contact_details": [
                                {"shape1_label": "bed_dev_smoke_native:primitive:12"},
                                {"shape1_label": "bed_dev_smoke_native:primitive:15"},
                            ],
                        }
                    ],
                }
            },
        }

    clean_path = tmp_path / "frame361.json"
    dirty_path = tmp_path / "frame362.json"
    clean_path.write_text(
        json.dumps(report(361, "smoke_passed", [], 0.04, [0.01, 0.02, 0.03], [0.0, 0.0, -1.0])),
        encoding="utf-8",
    )
    dirty_path.write_text(
        json.dumps(
            report(
                362,
                "runtime_failure",
                ["not_settled"],
                0.07,
                [0.04, 0.01, 0.05],
                [0.1, -0.1, -1.1],
            )
        ),
        encoding="utf-8",
    )

    audit = module.build_frame_transition_audit_report(
        clean_report_path=clean_path,
        dirty_report_path=dirty_path,
        variant_labels=("native_control_box",),
    )

    assert audit["status"] == "frame_transition_audit_recorded"
    assert audit["claim_boundary"] == (
        "bed_native_opt_in_frame_transition_audit_not_root_cause_or_fix_or_stability_evidence"
    )
    assert audit["clean_frame"] == 361
    assert audit["dirty_frame"] == 362
    assert audit["transition_summary"] == {
        "status": "clean_to_dirty_control_transition_recorded",
        "variant_count": 1,
        "all_model_invariants_equal": True,
        "all_final_contact_shape_labels_equal": True,
    }
    variant_audit = audit["variant_audits"]["native_control_box"]
    assert variant_audit["clean"]["status"] == "smoke_passed"
    assert variant_audit["dirty"]["status"] == "runtime_failure"
    assert variant_audit["dirty"]["failure_labels"] == ["not_settled"]
    assert variant_audit["deltas"]["completed_steps_delta"] == 8
    assert variant_audit["deltas"]["final_linear_speed_delta_mps"] == 0.03
    assert variant_audit["deltas"]["final_linear_velocity_delta"] == [0.03, -0.01, 0.02]
    assert variant_audit["aligned_final_window_rows"] == [
        {
            "steps_from_final": -1,
            "clean_step": 2887,
            "dirty_step": 2895,
            "clean_linear_speed_mps": 0.03,
            "dirty_linear_speed_mps": 0.06,
            "linear_speed_delta_mps": 0.03,
            "clean_support_height": -0.002,
            "dirty_support_height": -0.002,
            "support_height_delta": 0.0,
            "clean_contact_count": 2,
            "dirty_contact_count": 2,
            "clean_body_position": [-0.5, 0.5, -1.0],
            "dirty_body_position": [-0.4, 0.4, -1.1],
            "body_position_delta": [0.1, -0.1, -0.1],
        },
        {
            "steps_from_final": 0,
            "clean_step": 2888,
            "dirty_step": 2896,
            "clean_linear_speed_mps": 0.04,
            "dirty_linear_speed_mps": 0.07,
            "linear_speed_delta_mps": 0.03,
            "clean_support_height": -0.001,
            "dirty_support_height": -0.001,
            "support_height_delta": 0.0,
            "clean_contact_count": 2,
            "dirty_contact_count": 2,
            "clean_body_position": [0.0, 0.0, -1.0],
            "dirty_body_position": [0.1, -0.1, -1.1],
            "body_position_delta": [0.1, -0.1, -0.1],
        },
    ]
    assert variant_audit["model_invariants"] == {
        "body_mass_equal": True,
        "body_inv_mass_equal": True,
        "body_com_equal": True,
        "body_inertia_equal": True,
        "body_inv_inertia_equal": True,
        "package_anchor_equal": True,
        "type_counts_equal": True,
    }
    assert variant_audit["contact_invariants"] == {
        "final_contact_count_equal": True,
        "final_contact_shape1_labels_equal": True,
        "clean_final_contact_shape1_labels": [
            "bed_dev_smoke_native:primitive:12",
            "bed_dev_smoke_native:primitive:15",
        ],
        "dirty_final_contact_shape1_labels": [
            "bed_dev_smoke_native:primitive:12",
            "bed_dev_smoke_native:primitive:15",
        ],
    }
    json.dumps(audit, allow_nan=False)


def test_frame_transition_audit_main_writes_json(tmp_path, capsys):
    module = _load_bed_native_opt_in_frame_transition_audit_module()
    clean_path = tmp_path / "clean.json"
    dirty_path = tmp_path / "dirty.json"
    output_path = tmp_path / "audit.json"
    minimal_variant = {
        "native_control_box": {
            "status": "smoke_passed",
            "model_summary": {},
            "drop_settle_run": {
                "status": "smoke_passed",
                "failure_labels": [],
                "completed_steps": 1,
                "final_linear_speed_mps": 0.01,
            },
            "trace_samples": [],
        }
    }
    clean_path.write_text(
        json.dumps({"status": "diagnostic_recorded", "drop_settle_options": {"frames": 1}, "variants": minimal_variant}),
        encoding="utf-8",
    )
    dirty_variant = json.loads(json.dumps(minimal_variant))
    dirty_variant["native_control_box"]["status"] = "runtime_failure"
    dirty_variant["native_control_box"]["drop_settle_run"]["status"] = "runtime_failure"
    dirty_variant["native_control_box"]["drop_settle_run"]["failure_labels"] = ["not_settled"]
    dirty_path.write_text(
        json.dumps({"status": "diagnostic_recorded", "drop_settle_options": {"frames": 2}, "variants": dirty_variant}),
        encoding="utf-8",
    )

    assert module.main(
        [
            "--clean-report",
            str(clean_path),
            "--dirty-report",
            str(dirty_path),
            "--variant-label",
            "native_control_box",
            "--output",
            str(output_path),
        ]
    ) == 0

    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output_path.read_text())
    assert stdout_payload == file_payload
    assert file_payload["status"] == "frame_transition_audit_recorded"


def test_clean_frame_blocker_audit_compares_target_to_clean_controls(tmp_path):
    module = _load_bed_native_opt_in_clean_frame_blocker_audit_module()

    def variant(
        status,
        failure_labels,
        speed,
        velocity,
        position,
        mass,
        com,
        label_prefix,
        type_counts,
    ):
        return {
            "status": status,
            "type_counts": type_counts,
            "package_anchor": [1.0, 2.0, 3.0],
            "model_summary": {
                "body_mass": [mass],
                "body_inv_mass": [1.0 / mass],
                "body_com": [com],
                "body_inertia": [[[4.0 + mass, 5.0, 6.0]]],
                "body_inv_inertia": [[[0.25, 0.2, 0.1]]],
            },
            "drop_settle_run": {
                "status": status,
                "failure_labels": failure_labels,
                "completed_steps": 2888,
                "final_linear_speed_mps": speed,
                "final_linear_velocity": velocity,
                "final_support_height": -0.001,
                "final_contact_count": 2,
            },
            "tail_linear_speed_summary": {
                "sample_count": 3,
                "over_settle_threshold_count": 1 if status == "smoke_passed" else 3,
            },
            "trace_samples": [
                {
                    "step": 2887,
                    "linear_speed_mps": round(speed - 0.01, 2),
                    "body_position": [position[0] - 0.5, position[1] + 0.5, position[2]],
                    "support_height": -0.002,
                    "contact_count": 2,
                    "contact_details": [
                        {"shape1_label": f"{label_prefix}:primitive:12"},
                        {"shape1_label": f"{label_prefix}:primitive:15"},
                    ],
                },
                {
                    "step": 2888,
                    "linear_speed_mps": speed,
                    "body_position": position,
                    "angular_velocity_raw": [0.0, 0.0, 0.0],
                    "support_height": -0.001,
                    "contact_count": 2,
                    "contact_details": [
                        {"shape1_label": f"{label_prefix}:primitive:12"},
                        {"shape1_label": f"{label_prefix}:primitive:15"},
                    ],
                },
            ],
        }

    report_path = tmp_path / "frame361.json"
    report_path.write_text(
        json.dumps(
            {
                "status": "diagnostic_recorded",
                "drop_settle_options": {"frames": 361},
                "variants": {
                    "native_control_box": variant(
                        "smoke_passed",
                        [],
                        0.04,
                        [0.01, 0.02, 0.03],
                        [0.0, 0.0, -1.0],
                        10.0,
                        [1.0, 2.0, 3.0],
                        "native",
                        {"box": 32},
                    ),
                    "native_opt_in_cylinder_reverted": variant(
                        "smoke_passed",
                        [],
                        0.04,
                        [0.01, 0.02, 0.03],
                        [0.0, 0.0, -1.0],
                        10.0,
                        [1.0, 2.0, 3.0],
                        "opt_in",
                        {"box": 32},
                    ),
                    "native_opt_in_cylinder": variant(
                        "runtime_failure",
                        ["not_settled"],
                        0.07,
                        [0.04, 0.01, 0.05],
                        [0.1, -0.1, -1.1],
                        12.0,
                        [1.5, 2.25, 2.75],
                        "opt_in",
                        {"box": 31, "cylinder": 1},
                    ),
                },
            }
        ),
        encoding="utf-8",
    )

    audit = module.build_clean_frame_blocker_audit_report(report_path=report_path)

    assert audit["status"] == "clean_frame_blocker_audit_recorded"
    assert audit["claim_boundary"] == (
        "bed_native_opt_in_clean_frame_blocker_audit_not_root_cause_or_fix_or_stability_evidence"
    )
    assert audit["frame"] == 361
    assert audit["summary"] == {
        "target_status": "runtime_failure",
        "target_failure_labels": ["not_settled"],
        "baseline_count": 2,
        "all_baselines_smoke_passed": True,
        "all_final_contact_counts_equal": True,
        "all_final_contact_primitive_suffixes_equal": True,
    }
    control_audit = audit["baseline_audits"]["native_control_box"]
    assert control_audit["deltas"]["final_linear_speed_delta_mps"] == 0.03
    assert control_audit["deltas"]["final_linear_velocity_delta"] == [0.03, -0.01, 0.02]
    assert control_audit["model_deltas"]["body_mass_delta"] == 2.0
    assert control_audit["model_deltas"]["body_com_delta"] == [0.5, 0.25, -0.25]
    assert control_audit["contact_invariants"] == {
        "final_contact_count_equal": True,
        "final_contact_primitive_suffixes_equal": True,
        "baseline_final_contact_shape1_labels": [
            "native:primitive:12",
            "native:primitive:15",
        ],
        "target_final_contact_shape1_labels": [
            "opt_in:primitive:12",
            "opt_in:primitive:15",
        ],
        "baseline_final_contact_primitive_suffixes": ["12", "15"],
        "target_final_contact_primitive_suffixes": ["12", "15"],
    }
    assert control_audit["aligned_final_window_rows"][-1] == {
        "steps_from_final": 0,
        "baseline_step": 2888,
        "target_step": 2888,
        "baseline_linear_speed_mps": 0.04,
        "target_linear_speed_mps": 0.07,
        "linear_speed_delta_mps": 0.03,
        "baseline_support_height": -0.001,
        "target_support_height": -0.001,
        "support_height_delta": 0.0,
        "baseline_contact_count": 2,
        "target_contact_count": 2,
        "baseline_body_position": [0.0, 0.0, -1.0],
        "target_body_position": [0.1, -0.1, -1.1],
        "body_position_delta": [0.1, -0.1, -0.1],
    }
    json.dumps(audit, allow_nan=False)


def test_clean_frame_blocker_audit_main_writes_json(tmp_path, capsys):
    module = _load_bed_native_opt_in_clean_frame_blocker_audit_module()
    report_path = tmp_path / "report.json"
    output_path = tmp_path / "audit.json"
    minimal_variant = {
        "status": "smoke_passed",
        "model_summary": {},
        "drop_settle_run": {
            "status": "smoke_passed",
            "failure_labels": [],
            "completed_steps": 1,
            "final_linear_speed_mps": 0.01,
        },
        "trace_samples": [],
    }
    target_variant = json.loads(json.dumps(minimal_variant))
    target_variant["status"] = "runtime_failure"
    target_variant["drop_settle_run"]["status"] = "runtime_failure"
    target_variant["drop_settle_run"]["failure_labels"] = ["not_settled"]
    report_path.write_text(
        json.dumps(
            {
                "status": "diagnostic_recorded",
                "drop_settle_options": {"frames": 361},
                "variants": {
                    "native_control_box": minimal_variant,
                    "native_opt_in_cylinder_reverted": minimal_variant,
                    "native_opt_in_cylinder": target_variant,
                },
            }
        ),
        encoding="utf-8",
    )

    assert module.main(["--report", str(report_path), "--output", str(output_path)]) == 0

    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output_path.read_text())
    assert stdout_payload == file_payload
    assert file_payload["status"] == "clean_frame_blocker_audit_recorded"


def test_model_build_delta_audit_records_target_shape_and_delta_context(tmp_path):
    module = _load_bed_native_opt_in_model_build_delta_audit_module()
    report_path = tmp_path / "model_build.json"
    report_path.write_text(
        json.dumps(
            {
                "status": "diagnostic_recorded",
                "target_index": 6,
                "target_source_faces": [32, 33],
                "model_build_audit": {
                    "status": "diagnostic_recorded",
                    "anchor_match": True,
                    "target_index": 6,
                    "target_source_faces": [32, 33],
                    "delta_summary": {
                        "full_opt_in_minus_native": {
                            "body_mass_delta": 5.0,
                            "body_com_delta": [0.1, 0.2, 0.3],
                            "body_inertia_row0_delta": [10.0, 20.0, 30.0],
                        },
                        "target_opt_in_minus_native": {
                            "body_mass_delta": 5.0,
                            "body_com_delta": [1.0, 2.0, 3.0],
                            "body_inertia_row0_delta": [100.0, 200.0, 300.0],
                        },
                        "rest_opt_in_minus_native": {
                            "body_mass_delta": 0.0,
                            "body_com_delta": [0.0, 0.0, 0.0],
                            "body_inertia_row0_delta": [0.0, 0.0, 0.0],
                        },
                    },
                    "pieces": {
                        "native_target_full_anchor": {
                            "primitive_count": 1,
                            "primitive_ids": ["native:primitive:6"],
                            "anchor": [0.0, 0.0, 0.0],
                            "model_summary": {
                                "body_mass": [8.0],
                                "body_com": [[1.0, 2.0, 3.0]],
                                "body_inertia": [[[4.0, 5.0, 6.0]]],
                                "shape_scale": [[0.2, 2.3, 2.2]],
                            },
                        },
                        "native_opt_in_target_full_anchor": {
                            "primitive_count": 1,
                            "primitive_ids": ["opt:primitive:6"],
                            "anchor": [0.0, 0.0, 0.0],
                            "model_summary": {
                                "body_mass": [13.0],
                                "body_com": [[2.0, 4.0, 6.0]],
                                "body_inertia": [[[104.0, 205.0, 306.0]]],
                                "shape_scale": [[2.7, 0.2, 0.0]],
                            },
                        },
                    },
                },
            }
        ),
        encoding="utf-8",
    )

    audit = module.build_model_build_delta_audit_report(report_path=report_path)

    assert audit["status"] == "model_build_delta_audit_recorded"
    assert audit["claim_boundary"] == (
        "bed_native_opt_in_model_build_delta_audit_not_root_cause_or_fix_or_stability_evidence"
    )
    assert audit["summary"] == {
        "anchor_match": True,
        "target_index": 6,
        "target_source_faces": [32, 33],
        "rest_without_target_delta_zero": True,
        "target_delta_nonzero": True,
        "full_delta_nonzero": True,
    }
    assert audit["target_shape_audit"] == {
        "native_target_primitive_id": "native:primitive:6",
        "native_opt_in_target_primitive_id": "opt:primitive:6",
        "native_target_shape_scale": [0.2, 2.3, 2.2],
        "native_opt_in_target_shape_scale": [2.7, 0.2, 0.0],
        "target_shape_scale_delta": [2.5, -2.1, -2.2],
    }
    assert audit["piece_summaries"]["native_target_full_anchor"] == {
        "primitive_count": 1,
        "primitive_ids": ["native:primitive:6"],
        "body_mass": 8.0,
        "body_com": [1.0, 2.0, 3.0],
        "body_inertia_row0": [4.0, 5.0, 6.0],
        "shape_scale": [0.2, 2.3, 2.2],
    }
    assert audit["delta_summary"]["target_opt_in_minus_native"]["body_mass_delta"] == 5.0
    json.dumps(audit, allow_nan=False)


def test_model_build_delta_audit_main_writes_json(tmp_path, capsys):
    module = _load_bed_native_opt_in_model_build_delta_audit_module()
    report_path = tmp_path / "model_build.json"
    output_path = tmp_path / "audit.json"
    report_path.write_text(
        json.dumps(
            {
                "status": "diagnostic_recorded",
                "model_build_audit": {
                    "status": "diagnostic_recorded",
                    "anchor_match": True,
                    "target_index": 1,
                    "target_source_faces": [4],
                    "delta_summary": {
                        "full_opt_in_minus_native": {"body_mass_delta": 1.0},
                        "target_opt_in_minus_native": {"body_mass_delta": 1.0},
                        "rest_opt_in_minus_native": {"body_mass_delta": 0.0},
                    },
                    "pieces": {
                        "native_target_full_anchor": {
                            "primitive_count": 1,
                            "primitive_ids": ["native:primitive:1"],
                            "model_summary": {"shape_scale": [[1.0, 1.0, 1.0]]},
                        },
                        "native_opt_in_target_full_anchor": {
                            "primitive_count": 1,
                            "primitive_ids": ["opt:primitive:1"],
                            "model_summary": {"shape_scale": [[2.0, 1.0, 1.0]]},
                        },
                    },
                },
            }
        ),
        encoding="utf-8",
    )

    assert module.main(["--report", str(report_path), "--output", str(output_path)]) == 0

    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output_path.read_text())
    assert stdout_payload == file_payload
    assert file_payload["status"] == "model_build_delta_audit_recorded"


def test_cli_help_mentions_project(capsys):
    cli = importlib.import_module("primitive_collision_compiler.cli")

    assert cli.main([]) == 0

    output = capsys.readouterr().out
    assert "Newton Primitive Collision Compiler" in output


def test_cli_rejects_non_dry_run_compile(capsys):
    cli = importlib.import_module("primitive_collision_compiler.cli")

    assert cli.main(["--config", "tests/fixtures/dry_run_mvp.yaml"]) == 2

    error = capsys.readouterr().err
    assert "non-dry-run compilation is not implemented yet" in error
