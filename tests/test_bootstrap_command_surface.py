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
