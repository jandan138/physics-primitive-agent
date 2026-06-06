from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pytest

import primitive_collision_compiler.paper.accv_visuals as accv_visuals
from primitive_collision_compiler.paper.accv_visuals import (
    PDF_METADATA,
    PROBE_SHORT_LABELS,
    _phase0_probe_scene_panel_specs,
    _phase0_probe_scene_payload,
    Phase0RenderedProbePanel,
    _render_phase0_probe_scene_panels,
    _render_vec3_y_up,
    _run_newton_render_phase0_panel,
    _save_collision_probe_scenes_from_rendered_panels,
    _write_phase0_probe_scene_bundle,
    _collision_scene_package_max_primitives,
    _collision_scene_subset_label,
    _collision_scene_width_ratios,
    _franka_label_indices,
    _franka_metric_color,
    _mechanism_failure_callout_positions,
    _mechanism_scene_title,
    _mechanism_visual_labels,
    _minimum_projected_marker_bounds,
    _overlay_max_primitives,
    _outcome_cell_label,
    _outcome_matrix_group_label,
    _outcome_matrix_title,
    _package_context_mesh_style,
    _primitive_overlay_wire_style,
    _projected_overlay_max_primitives,
    _projected_package_label_position,
    _projected_package_marker_label,
    _surface_overlay_face_limit,
    _keyboard_component_style,
    _load_mesh,
    _load_result_entry,
    _split_evidence_sources,
    _source_record_hashes,
    outcome_matrix,
    primitive_vertices,
    summarize_probe_outcomes,
)


def _vhacd_probe_case(asset_role: str, asset_id: str = "grscenes_bowl_fixture") -> dict:
    package = {
        "package_id": f"{asset_role}_vhacd_if_available:phase0_vhacd",
        "asset_id": asset_id,
        "status": "generated",
        "primitives": [
            {
                "primitive_id": "p0",
                "kind": "convex_mesh",
                "center": [1.0, 2.0, 3.0],
                "axes": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
                "dimensions": {
                    "vertices": [[0.0, 1.0, 2.0], [1.0, 1.0, 2.0], [0.0, 2.0, 3.0]],
                    "faces": [[0, 1, 2]],
                },
            }
        ],
    }
    return {
        "asset_id": asset_id,
        "asset_role": asset_role,
        "local_path": "assets/raw/example.usd",
        "baseline_results": {
            "vhacd_if_available": {
                "collision_package": package,
                "outcome": "accept",
            }
        },
        "probe_results": {
            "vhacd_if_available": {
                "body_state_drop_settle": {
                    "outcome": "failure",
                    "initial_conditions": {"height_m": 0.25},
                    "drop_settle_runs": [
                        {
                            "final_height": 0.50,
                            "min_height": -0.10,
                            "failure_labels": ["not_settled", "floor_breach"],
                        }
                    ],
                },
                "stack_or_slide": {
                    "outcome": "failure",
                    "initial_conditions": {
                        "probe_half_extents_m": [0.05, 0.06, 0.07],
                    },
                    "stack_slide_runs": [
                        {
                            "initial_probe_position": [1.0, 2.0, 3.0],
                            "final_probe_position": [4.0, 5.0, 6.0],
                            "horizontal_displacement_m": 1.25,
                            "support_top_height": 2.75,
                            "failure_labels": ["excess_horizontal_slide"],
                        }
                    ],
                },
            }
        },
    }


def _franka_task_report_fixture() -> dict:
    return {
        "articulation_cases": [
            {
                "robot_package_result": {
                    "primitive_or_hull_count": 12,
                    "links": [
                        {"link_path": "/panda/panda_link0", "placeholder_primitive_count": 0},
                        {"link_path": "/panda/panda_link8", "placeholder_primitive_count": 1},
                        {"link_path": "/panda/panda_rightfinger", "placeholder_primitive_count": 0},
                    ],
                    "link_boundary_audit": {"metrics": {"link_count": 12}},
                },
                "probe_results": {
                    "generated_package_robot_task_if_robot": {
                        "outcome": "accept",
                        "metrics": {
                            "package_consumption": {
                                "missing_body_link_count": 0,
                                "source_usd_shape_count": 0,
                                "generated_self_collision_filter_pair_count": 66,
                            }
                        },
                    }
                },
            }
        ]
    }


def test_phase0_probe_scene_panel_specs_cover_selected_vhacd_panels() -> None:
    report = {
        "cases": [
            _vhacd_probe_case("container", "grscenes_bowl_fixture"),
            _vhacd_probe_case("contact_affordance", "grscenes_cup_fixture"),
            _vhacd_probe_case("stackable", "grscenes_tray_fixture"),
            _vhacd_probe_case("precision_negative_control", "grscenes_keyboard_fixture"),
        ]
    }

    specs = _phase0_probe_scene_panel_specs(report)

    assert [spec.case["asset_role"] for spec in specs] == [
        "container",
        "container",
        "container",
        "contact_affordance",
        "contact_affordance",
        "contact_affordance",
        "stackable",
        "stackable",
        "stackable",
    ]
    assert [spec.panel_kind for spec in specs[:3]] == ["package_overlay", "drop_settle", "stack_slide"]


def test_case_label_keeps_role_asset_name_for_contact_affordance_cup() -> None:
    label = accv_visuals.case_label(_vhacd_probe_case("contact_affordance", "grscenes_cup_fixture"))

    assert label == "contact affordance\ncup"


def test_phase0_probe_scene_case_label_uses_visual_description_for_contact_prop() -> None:
    label = accv_visuals._phase0_probe_scene_case_label(
        _vhacd_probe_case("contact_affordance", "grscenes_cup_fixture")
    )

    assert label == "cylindrical contact\nprop"


def test_phase0_probe_scene_payload_converts_stack_coordinates_to_renderer_y_up() -> None:
    case = _vhacd_probe_case("container")
    spec = _phase0_probe_scene_panel_specs({"cases": [case]})[2]

    payload = _phase0_probe_scene_payload(
        spec,
        report_path=Path("reports/generated/phase0.json"),
        report_sha256="abc123",
    )

    metrics = payload["recorded_metrics"]
    assert _render_vec3_y_up([1.0, 2.0, 3.0]) == [1.0, 3.0, 2.0]
    assert metrics["initial_probe_position"] == [1.0, 3.0, 2.0]
    assert metrics["final_probe_position"] == [4.0, 6.0, 5.0]
    assert metrics["support_top_height"] == 2.75
    assert payload["reconstruction_semantics"]["mode"] == "recorded_probe_position_reconstruction"


def test_write_phase0_probe_scene_bundle_uses_newton_render_contract(tmp_path: Path) -> None:
    yaml = pytest.importorskip("yaml")
    case = _vhacd_probe_case("container")
    spec = _phase0_probe_scene_panel_specs({"cases": [case]})[0]
    mesh = type(
        "Mesh",
        (),
        {
            "points": np.asarray([[0.0, 1.0, 2.0], [1.0, 1.0, 2.0], [0.0, 2.0, 3.0]], dtype=float),
            "faces": np.asarray([[0, 1, 2]], dtype=int),
        },
    )()

    bundle_dir = tmp_path / "bundle"
    _write_phase0_probe_scene_bundle(
        spec,
        mesh=mesh,
        bundle_dir=bundle_dir,
        report_path=Path("reports/generated/phase0.json"),
        report_sha256="abc123",
    )

    meta = yaml.safe_load((bundle_dir / "meta.yaml").read_text(encoding="utf-8"))
    probe_scene = __import__("json").loads((bundle_dir / "probe_scene.json").read_text(encoding="utf-8"))
    package = __import__("json").loads((bundle_dir / "collision_package.json").read_text(encoding="utf-8"))
    obj_text = (bundle_dir / "mesh.obj").read_text(encoding="utf-8")

    assert meta["recipe"] == "phase0_probe_scene"
    assert meta["panel_kind"] == "package_overlay"
    assert meta["camera"]["elev"] == 38
    assert meta["camera"]["azim"] == 10
    assert meta["camera"]["zoom"] == 1.35
    assert probe_scene["source_report_sha256"] == "abc123"
    assert package["primitives"][0]["center"] == [1.0, 3.0, 2.0]
    assert "v 0.000000000 2.000000000 1.000000000" in obj_text
    assert "f 1 2 3" in obj_text


def test_phase0_probe_scene_camera_keeps_stackable_label_clearance() -> None:
    specs = _phase0_probe_scene_panel_specs(
        {"cases": [_vhacd_probe_case("stackable", "grscenes_tray_fixture")]}
    )

    camera = accv_visuals._phase0_probe_scene_camera(specs[0].case)

    assert camera["zoom"] == 1.22


def test_run_newton_render_phase0_panel_invokes_recipe_cli(tmp_path: Path) -> None:
    fake_root = tmp_path / "newton-render"
    package_dir = fake_root / "src/newton_render"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (package_dir / "cli.py").write_text(
        """
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("--output") + 1])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("rendered", encoding="utf-8")
output.with_suffix(".json").write_text(json.dumps({"args": args, "pythonpath": os.environ.get("PYTHONPATH", "")}), encoding="utf-8")
""".strip(),
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    output = tmp_path / "panel.png"

    path = _run_newton_render_phase0_panel(
        newton_render_root=fake_root,
        bundle_dir=bundle,
        output_png=output,
        python_executable=sys.executable,
    )

    sidecar = __import__("json").loads(output.with_suffix(".json").read_text(encoding="utf-8"))
    assert path == output
    assert output.read_text(encoding="utf-8") == "rendered"
    assert "--recipe" in sidecar["args"]
    assert "phase0_probe_scene" in sidecar["args"]
    assert str(fake_root / "src") in sidecar["pythonpath"]


def test_render_phase0_probe_scene_panels_exports_ordered_bundles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report = {"cases": [_vhacd_probe_case("container", "grscenes_bowl_fixture")]}
    report_path = tmp_path / "phase0.json"
    report_path.write_text("{}", encoding="utf-8")
    mesh = type(
        "Mesh",
        (),
        {
            "points": np.asarray([[0.0, 1.0, 2.0], [1.0, 1.0, 2.0], [0.0, 2.0, 3.0]], dtype=float),
            "faces": np.asarray([[0, 1, 2]], dtype=int),
        },
    )()

    def fake_render(**kwargs):
        output_png = kwargs["output_png"]
        output_png.write_text("rendered", encoding="utf-8")
        return output_png

    monkeypatch.setattr(accv_visuals, "_load_mesh", lambda path, max_faces: mesh)
    monkeypatch.setattr(accv_visuals, "_run_newton_render_phase0_panel", fake_render)

    panels = _render_phase0_probe_scene_panels(
        report,
        asset_root=tmp_path,
        report_path=report_path,
        bundle_root=tmp_path / "bundles",
        panel_output_dir=tmp_path / "panels",
        newton_render_root=tmp_path / "newton-render",
    )

    assert [panel.spec.panel_kind for panel in panels] == ["package_overlay", "drop_settle", "stack_slide"]
    assert all(panel.output_png.read_text(encoding="utf-8") == "rendered" for panel in panels)
    assert (tmp_path / "bundles/container_bowl_package_overlay/meta.yaml").is_file()
    assert (tmp_path / "bundles/container_bowl_stack_slide/collision_package.json").is_file()


def test_save_collision_probe_scenes_from_rendered_panels_creates_pdf(tmp_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    specs = _phase0_probe_scene_panel_specs({"cases": [_vhacd_probe_case("container")]})
    panels = []
    for index, spec in enumerate(specs):
        png = tmp_path / f"panel_{index}.png"
        plt.imsave(png, np.ones((12, 16, 3), dtype=float) * (0.25 + index * 0.2))
        panels.append(Phase0RenderedProbePanel(spec=spec, output_png=png, bundle_dir=tmp_path / f"bundle_{index}"))

    figure = _save_collision_probe_scenes_from_rendered_panels(panels, tmp_path, plt)

    assert figure.figure_id == "phase0_collision_probe_scenes"
    assert figure.path.is_file()
    assert figure.path.suffix == ".pdf"
    assert "newton-render" in figure.evidence


def test_save_collision_probe_scenes_from_rendered_panels_keeps_panel_rows_readable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    specs = _phase0_probe_scene_panel_specs({"cases": [_vhacd_probe_case("container")]})
    panels = []
    for index, spec in enumerate(specs):
        png = tmp_path / f"panel_{index}.png"
        plt.imsave(png, np.ones((12, 16, 3), dtype=float) * (0.25 + index * 0.2))
        panels.append(Phase0RenderedProbePanel(spec=spec, output_png=png, bundle_dir=tmp_path / f"bundle_{index}"))

    saved_sizes: list[tuple[float, float]] = []

    def capture_save(fig, path):
        saved_sizes.append(tuple(float(value) for value in fig.get_size_inches()))
        fig.savefig(path)

    monkeypatch.setattr(accv_visuals, "_save_pdf", capture_save)

    _save_collision_probe_scenes_from_rendered_panels(panels, tmp_path, plt)

    assert saved_sizes == [(12.6, 3.05)]


def test_box_primitive_vertices_uses_center_and_half_extents() -> None:
    primitive = {
        "kind": "box",
        "center": [10.0, 20.0, 30.0],
        "dimensions": {"half_extents": [1.0, 2.0, 3.0]},
    }

    vertices = primitive_vertices(primitive)

    assert vertices.shape == (8, 3)
    np.testing.assert_allclose(vertices.min(axis=0), [9.0, 18.0, 27.0])
    np.testing.assert_allclose(vertices.max(axis=0), [11.0, 22.0, 33.0])


def test_convex_mesh_primitive_vertices_passes_report_vertices_through() -> None:
    primitive = {
        "kind": "convex_mesh",
        "dimensions": {"vertices": [[0, 0, 0], [1, 2, 3], [-1, 0, 4]]},
    }

    vertices = primitive_vertices(primitive)

    assert vertices.shape == (3, 3)
    np.testing.assert_allclose(vertices[1], [1, 2, 3])


def test_unknown_primitive_kind_returns_empty_vertices() -> None:
    vertices = primitive_vertices({"kind": "capsule", "dimensions": {"radius": 1.0}})

    assert vertices.shape == (0, 3)


def test_outcome_matrix_and_summary_count_selected_probe_outcomes() -> None:
    report = {
        "cases": [
            {
                "asset_role": "container",
                "asset_id": "grscenes_bowl_fixture",
                "probe_results": {
                    "bounding_primitive": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "accept"},
                        "stack_or_slide": {"outcome": "failure"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                    "cpd_style_primitive_candidate_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "failure"},
                        "stack_or_slide": {"outcome": "failure"},
                    },
                    "coacd_or_vhacd_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "fallback"},
                        "stack_or_slide": {"outcome": "fallback"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                    "single_convex_hull": {
                        "contact_canary": {"outcome": "fallback"},
                        "body_state_drop_settle": {"outcome": "fallback"},
                        "stack_or_slide": {"outcome": "fallback"},
                        "sphere_rain": {"outcome": "fallback"},
                    },
                    "vhacd_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "failure"},
                        "stack_or_slide": {"outcome": "failure"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                },
            }
        ]
    }

    rows, columns, matrix = outcome_matrix(report)
    summary = summarize_probe_outcomes(report)

    assert rows == ["container\nbowl"]
    assert len(columns) == 20
    assert matrix.shape == (1, 20)
    assert summary["accept"] == 8
    assert summary["failure"] == 5
    assert summary["fallback"] == 6
    assert summary["not_applicable"] == 1


def test_load_mesh_failure_is_not_silent(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="failed to load source mesh"):
        _load_mesh(tmp_path / "missing.usd", max_faces=1)


def test_load_mesh_combines_usd_components_for_visual_context(tmp_path: Path) -> None:
    Usd = pytest.importorskip("pxr.Usd")
    UsdGeom = pytest.importorskip("pxr.UsdGeom")
    asset_path = tmp_path / "two_components.usda"
    stage = Usd.Stage.CreateNew(str(asset_path))
    for path, x_offset, purpose in (
        ("/Root/Left", 0.0, None),
        ("/Root/Right", 2.0, None),
        ("/Root/Proxy", 100.0, UsdGeom.Tokens.proxy),
    ):
        mesh = UsdGeom.Mesh.Define(stage, path)
        mesh.CreatePointsAttr(
            [
                (x_offset, 0.0, 0.0),
                (x_offset + 1.0, 0.0, 0.0),
                (x_offset + 1.0, 1.0, 0.0),
                (x_offset, 1.0, 0.0),
            ]
        )
        mesh.CreateFaceVertexCountsAttr([4])
        mesh.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
        if purpose is not None:
            mesh.CreatePurposeAttr(purpose)
    stage.GetRootLayer().Save()

    loaded = _load_mesh(asset_path, max_faces=10)

    assert loaded.face_count == 4
    np.testing.assert_allclose(loaded.points.min(axis=0), [0.0, 0.0, 0.0])
    np.testing.assert_allclose(loaded.points.max(axis=0), [3.0, 1.0, 0.0])


def test_mechanism_result_entry_is_structured_for_figure_generation() -> None:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    metrics = entry["metrics"]

    assert metrics["bed_final_speed_mps"] == pytest.approx(0.082304)
    assert metrics["franka_final_speed_mps"] == pytest.approx(0.0007108)
    assert metrics["settle_gate_mps"] == pytest.approx(0.05)
    assert len(metrics["audit_rows"]) == 5


def test_mechanism_visual_labels_name_scene_and_root_cause() -> None:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    labels = _mechanism_visual_labels(entry["metrics"])

    assert "capped bed: full package fails" in labels
    assert "isolated target passes" in labels
    assert "Franka link-local package passes" in labels
    assert "COM/inertia sensitivity supported" in labels


def test_mechanism_scene_payload_preserves_recorded_metrics() -> None:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    payload = accv_visuals._mechanism_scene_payload(entry["metrics"])

    assert [scene["id"] for scene in payload["subscenes"]] == [
        "bed_full_package_fail",
        "isolated_target_pass",
        "franka_link_local_pass",
    ]
    assert payload["annotations"]["bed_speed_label"] == "0.082 > 0.05 m/s"
    assert payload["claim_boundary_note"] == "Diagnostic rendering; not a new Newton run."
    assert payload["status_label_entries"] == ["failure", "accept"]
    assert payload["labels"] == {
        "failure": "",
        "accept": "",
    }


def test_franka_task_scene_payload_preserves_consumption_metrics() -> None:
    payload = accv_visuals._franka_task_scene_payload(_franka_task_report_fixture())

    assert payload["metrics"]["detected_links"] == 12
    assert payload["metrics"]["generated_primitives"] == 12
    assert payload["metrics"]["missing_body_links"] == 0
    assert payload["metrics"]["source_usd_shapes"] == 0
    assert payload["metrics"]["self_collision_filters"] == 66
    assert payload["metrics"]["task_outcome"] == "accept"
    assert "panda_link8" in payload["sentinel_links"]
    assert payload["labels"] == {
        "failure": "",
        "accept": "",
        "meshless_sentinel": "",
    }


def test_write_paper_scene_bundle_uses_newton_render_contract(tmp_path: Path) -> None:
    yaml = pytest.importorskip("yaml")
    bundle = accv_visuals._write_paper_scene_bundle(
        tmp_path / "bundle",
        figure_id="franka_task_scene",
        recipe="franka_task_scene",
        scene_payload={"links": [], "metrics": {"task_outcome": "accept"}},
    )

    assert (bundle / "meta.yaml").is_file()
    assert (bundle / "scene.json").is_file()
    meta = yaml.safe_load((bundle / "meta.yaml").read_text(encoding="utf-8"))
    assert meta["recipe"] == "franka_task_scene"
    assert meta["figure_id"] == "franka_task_scene"


def test_collision_scene_layout_gives_package_panel_more_width() -> None:
    ratios = _collision_scene_width_ratios()

    assert ratios[0] > ratios[1]
    assert ratios[1] == pytest.approx(ratios[2])


def test_collision_scene_uses_sparse_package_context_for_dense_vhacd() -> None:
    assert _collision_scene_package_max_primitives({"primitives": [{}] * 16}) == 3
    assert _collision_scene_package_max_primitives({"primitives": [{}] * 2}) == 2


def test_collision_scene_labels_representative_primitive_subset() -> None:
    label = _collision_scene_subset_label({"primitives": [{}] * 16}, shown_count=3)

    assert label == "repr. prim. +13"


def test_projected_package_markers_keep_minimum_visible_size() -> None:
    left, bottom, right, top = _minimum_projected_marker_bounds(
        np.asarray([0.49, 0.49]),
        np.asarray([0.51, 0.51]),
        xlim=(0.0, 10.0),
        ylim=(0.0, 20.0),
        min_fraction=0.10,
    )

    assert right - left == pytest.approx(1.0)
    assert top - bottom == pytest.approx(2.0)
    assert (left + right) / 2.0 == pytest.approx(0.5)
    assert (bottom + top) / 2.0 == pytest.approx(0.5)


def test_high_count_overlay_lanes_use_sparse_representative_subset() -> None:
    package = {"primitives": [{}] * 16}

    assert _overlay_max_primitives(package, surface=True) == 1
    assert _overlay_max_primitives(package, surface=False) == 2
    assert _overlay_max_primitives({"primitives": [{}] * 3}, surface=True) == 3


def test_surface_overlays_use_reduced_face_budget_for_paper_legibility() -> None:
    assert _surface_overlay_face_limit(surface=True) < _surface_overlay_face_limit(surface=False)
    assert _surface_overlay_face_limit(surface=True) <= 12


def test_package_context_mesh_style_is_quiet_for_overlay_cells() -> None:
    input_alpha, input_edge = _package_context_mesh_style(lane=None)
    package_alpha, package_edge = _package_context_mesh_style(lane="vhacd_if_available")

    assert input_alpha > package_alpha
    assert input_edge > package_edge
    assert package_alpha <= 0.06


def test_surface_primitive_wire_style_stays_readable_after_scaling() -> None:
    linewidth, alpha = _primitive_overlay_wire_style(surface=True, kind="convex_mesh")

    assert linewidth >= 0.46
    assert alpha >= 0.44


def test_keyboard_context_style_is_quieter_than_input_style() -> None:
    input_style = _keyboard_component_style(context=False, is_base=False)
    context_style = _keyboard_component_style(context=True, is_base=False)

    assert context_style["alpha"] < input_style["alpha"]
    assert context_style["linewidth"] <= 0.40


def test_outcome_matrix_short_labels_expand_contact_for_readability() -> None:
    assert PROBE_SHORT_LABELS["contact_canary"] == "Contact"


def test_outcome_matrix_cell_labels_do_not_rely_only_on_color() -> None:
    assert _outcome_cell_label(0) == "FB"
    assert _outcome_cell_label(1) == "NA"
    assert _outcome_cell_label(2) == "Fail"
    assert _outcome_cell_label(3) == "OK"


def test_outcome_matrix_group_label_marks_fallback_lane_without_cell_overlay() -> None:
    assert _outcome_matrix_group_label("single_convex_hull") == "Single hull\nfallback lane"
    assert _outcome_matrix_group_label("vhacd_if_available") == "V-HACD"


def test_outcome_matrix_omits_crowding_title_above_group_labels() -> None:
    assert _outcome_matrix_title() == ""


def test_projected_package_markers_get_local_labels() -> None:
    assert _projected_package_marker_label(0, total=1) == "pkg"
    assert _projected_package_marker_label(1, total=3) == "pkg 2"


def test_projected_package_label_position_stays_outside_marker_bounds() -> None:
    label_x, label_y, ha = _projected_package_label_position(
        left=0.40,
        bottom=0.35,
        right=0.50,
        top=0.45,
        xlim=(0.0, 1.0),
        ylim=(0.0, 1.0),
    )

    assert label_x > 0.50
    assert label_y == pytest.approx(0.40)
    assert ha == "left"


def test_high_count_projected_control_overlays_use_labeled_representative_marker() -> None:
    assert _projected_overlay_max_primitives({"primitives": [{}] * 16}) == 1
    assert _projected_overlay_max_primitives({"primitives": [{}] * 3}) == 3


def test_franka_metric_colors_are_value_aware() -> None:
    assert _franka_metric_color("missing body links", 0) == "#2e7d59"
    assert _franka_metric_color("missing body links", 2) == "#b94b48"
    assert _franka_metric_color("source USD shapes", 0) == "#2e7d59"
    assert _franka_metric_color("source USD shapes", 1) == "#b94b48"
    assert _franka_metric_color("task outcome", "accept") == "#2e7d59"
    assert _franka_metric_color("task outcome", "failure") == "#b94b48"
    assert _franka_metric_color("generated primitives", 12) == "#333333"


def test_franka_schematic_labels_are_derived_from_link_metadata() -> None:
    links = [
        {"link_path": "/panda/panda_rightfinger", "placeholder_primitive_count": 0},
        {"link_path": "/panda/panda_hand", "placeholder_primitive_count": 0},
        {"link_path": "/panda/panda_link0", "placeholder_primitive_count": 0},
        {"link_path": "/panda/panda_link8", "placeholder_primitive_count": 1},
    ]

    assert _franka_label_indices(links) == {
        0: "right finger",
        2: "base link",
        3: "sentinel link8",
    }


def test_mechanism_layout_keeps_title_short_for_single_visual_plate() -> None:
    assert _mechanism_scene_title() == "Mechanism diagnostic: package context matters"


def test_mechanism_failure_callouts_are_spaced_from_top_geometry() -> None:
    positions = _mechanism_failure_callout_positions()

    assert positions["com_label"][0] >= 0.54
    assert positions["settle_label"][0] >= 0.62
    assert positions["settle_label"][1] < positions["com_label"][1] - 0.10


def test_save_mechanism_diagnostic_from_rendered_panel_creates_pdf(tmp_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    image[:, :, 0] = 0.92
    panel = tmp_path / "mechanism.png"
    plt.imsave(panel, image)

    figure = accv_visuals._save_mechanism_diagnostic_from_rendered_panel(panel, tmp_path, plt)

    assert figure.figure_id == "bed_franka_mechanism_diagnostic"
    assert figure.path.is_file()
    assert "newton-render" in figure.evidence


def test_save_mechanism_diagnostic_from_rendered_panel_uses_single_visual_plate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    panel = tmp_path / "mechanism.png"
    plt.imsave(panel, image)
    saved_axes_counts: list[int] = []
    saved_sizes: list[tuple[float, float]] = []

    def capture_save(fig, path):
        saved_axes_counts.append(len(fig.axes))
        saved_sizes.append(tuple(float(value) for value in fig.get_size_inches()))
        fig.savefig(path)

    monkeypatch.setattr(accv_visuals, "_save_pdf", capture_save)

    accv_visuals._save_mechanism_diagnostic_from_rendered_panel(panel, tmp_path, plt)

    assert saved_axes_counts == [1]
    assert saved_sizes == [(12.2, 3.25)]


def test_save_mechanism_diagnostic_uses_ai_slot_even_when_renderer_available(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import primitive_collision_compiler.paper.fig2_mechanism_ai_slot as fig2_ai_slot

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    compose_calls: list[dict[str, Any]] = []

    def fake_compose(output_path: Path, *, metrics: Mapping[str, Any]) -> dict[str, Any]:
        Path(output_path).write_bytes(b"%PDF-1.4\n")
        Path(output_path).with_suffix(".png").write_bytes(b"png")
        compose_calls.append(dict(metrics))
        return {"mode": "visual_composition", "composer": "fake-fig2-composer"}

    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: fake_root)
    monkeypatch.setattr(
        accv_visuals,
        "_run_newton_render_paper_scene",
        lambda **kwargs: pytest.fail("Fig.2 should not call the old Newton renderer"),
    )
    monkeypatch.setattr(fig2_ai_slot, "compose_fig2_mechanism_ai_slot", fake_compose)

    figure = accv_visuals._save_mechanism_diagnostic(tmp_path, plt)

    assert compose_calls
    assert figure.path.is_file()
    assert figure.renderer_metadata["mode"] == "visual_composition"
    assert "Mechanism diagnostic" in figure.evidence


def test_save_mechanism_diagnostic_records_ai_slot_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import primitive_collision_compiler.paper.fig2_mechanism_ai_slot as fig2_ai_slot

    def fake_compose(output_path: Path, *, metrics: Mapping[str, Any]) -> dict[str, Any]:
        Path(output_path).write_bytes(b"%PDF-1.4\n")
        return {
            "mode": "visual_composition",
            "composer": "primitive_collision_compiler.paper.fig2_mechanism_ai_slot",
            "claim_boundary": "Fig.2 visual panels explain the recorded mechanism; not experimental evidence.",
        }

    monkeypatch.setattr(fig2_ai_slot, "compose_fig2_mechanism_ai_slot", fake_compose)

    figure = accv_visuals._save_mechanism_diagnostic(tmp_path, plt)

    assert figure.path.is_file()
    assert figure.renderer_metadata["composer"] == "primitive_collision_compiler.paper.fig2_mechanism_ai_slot"
    assert "not experimental evidence" in figure.renderer_metadata["claim_boundary"]
    assert "paper/shared/evidence/results_manifest.yaml" in figure.source_records


def test_save_mechanism_diagnostic_propagates_ai_slot_composer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import primitive_collision_compiler.paper.fig2_mechanism_ai_slot as fig2_ai_slot

    def fake_compose(output_path: Path, *, metrics: Mapping[str, Any]) -> dict[str, Any]:
        raise RuntimeError("visual composer failed")

    monkeypatch.setattr(fig2_ai_slot, "compose_fig2_mechanism_ai_slot", fake_compose)

    with pytest.raises(RuntimeError, match="visual composer failed"):
        accv_visuals._save_mechanism_diagnostic(tmp_path, plt)


def test_paper_scene_newton_render_root_raises_for_explicit_missing_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing_root = tmp_path / "missing-newton-render"
    monkeypatch.setenv("NEWTON_RENDER_ROOT", str(missing_root))

    with pytest.raises(RuntimeError, match="paper_diagnostic_scenes.py"):
        accv_visuals._paper_scene_newton_render_root()


def test_paper_scene_newton_render_root_requires_explicit_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NEWTON_RENDER_ROOT", raising=False)
    monkeypatch.delenv("PPA_DISABLE_NEWTON_RENDER", raising=False)

    with pytest.raises(RuntimeError, match="NEWTON_RENDER_ROOT is required"):
        accv_visuals._paper_scene_newton_render_root()


def test_paper_scene_newton_render_root_can_be_explicitly_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NEWTON_RENDER_ROOT", raising=False)
    monkeypatch.setenv("PPA_DISABLE_NEWTON_RENDER", "1")

    assert accv_visuals._paper_scene_newton_render_root() is None


def test_paper_scene_newton_render_root_raises_for_explicit_missing_recipe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/phase0_probe_scene.py").write_text("", encoding="utf-8")
    monkeypatch.setenv("NEWTON_RENDER_ROOT", str(fake_root))

    with pytest.raises(RuntimeError, match="paper_diagnostic_scenes.py"):
        accv_visuals._paper_scene_newton_render_root()


def test_save_mechanism_diagnostic_ignores_stale_auto_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import primitive_collision_compiler.paper.fig2_mechanism_ai_slot as fig2_ai_slot

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: fake_root)
    monkeypatch.setattr(
        accv_visuals,
        "_run_newton_render_paper_scene",
        lambda **kwargs: pytest.fail("Fig.2 should ignore the stale auto-renderer path"),
    )

    def fake_compose(output_path: Path, *, metrics: Mapping[str, Any]) -> dict[str, Any]:
        Path(output_path).write_bytes(b"%PDF-1.4\n")
        return {"mode": "visual_composition"}

    monkeypatch.setattr(fig2_ai_slot, "compose_fig2_mechanism_ai_slot", fake_compose)

    figure = accv_visuals._save_mechanism_diagnostic(tmp_path, plt)

    assert figure.path.is_file()
    assert figure.renderer_metadata["mode"] == "visual_composition"


def test_save_franka_task_scene_from_rendered_panel_creates_pdf(tmp_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    image[:, :, 1] = 0.92
    panel = tmp_path / "franka.png"
    plt.imsave(panel, image)

    figure = accv_visuals._save_franka_task_scene_from_rendered_panel(
        _franka_task_report_fixture(),
        panel,
        tmp_path,
        plt,
    )

    assert figure.figure_id == "franka_link_aware_task_scene"
    assert figure.path.is_file()
    assert "newton-render" in figure.evidence


def test_save_franka_task_scene_from_rendered_panel_uses_single_visual_plate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    image = np.ones((240, 420, 3), dtype=np.float32)
    panel = tmp_path / "franka.png"
    plt.imsave(panel, image)
    saved_axes_counts: list[int] = []
    saved_sizes: list[tuple[float, float]] = []

    def capture_save(fig, path):
        saved_axes_counts.append(len(fig.axes))
        saved_sizes.append(tuple(float(value) for value in fig.get_size_inches()))
        fig.savefig(path)

    monkeypatch.setattr(accv_visuals, "_save_pdf", capture_save)

    accv_visuals._save_franka_task_scene_from_rendered_panel(
        _franka_task_report_fixture(),
        panel,
        tmp_path,
        plt,
    )

    assert saved_axes_counts == [1]
    assert saved_sizes == [(12.2, 3.25)]


def test_save_franka_task_scene_invokes_renderer_when_available(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    calls: list[str] = []
    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    def fake_run(**kwargs: Any) -> Path:
        calls.append(kwargs["recipe"])
        out = kwargs["output_png"]
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.imsave(out, np.ones((100, 160, 3)))
        out.with_suffix(".json").write_text(
            json.dumps(
                {
                    "recipe": kwargs["recipe"],
                    "output_png_sha256": "fake-panel-sha",
                    "input_hashes": {"scene.json": "fake-scene-sha"},
                    "source_claim_boundary_note": "Task-smoke rendering; not whole-robot quality evidence.",
                    "franka_visual_mode": "link_chain_task_smoke",
                    "link_count": 12,
                    "sentinel_link_names": ["panda_link8"],
                    "status_label_layout": {"entries": [{"key": "failure"}, {"key": "accept"}]},
                }
            ),
            encoding="utf-8",
        )
        return out

    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: fake_root)
    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    figure = accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)

    assert calls == ["franka_task_scene"]
    assert figure.path.is_file()
    assert figure.renderer_metadata["recipe"] == "franka_task_scene"


def test_save_franka_task_scene_falls_back_without_renderer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    monkeypatch.setattr(accv_visuals, "_phase0_newton_render_root", lambda: None)
    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: None)
    saved_axes_counts: list[int] = []
    saved_sizes: list[tuple[float, float]] = []
    saved_titles: list[list[str]] = []

    def capture_save(fig, path):
        saved_axes_counts.append(len(fig.axes))
        saved_sizes.append(tuple(float(value) for value in fig.get_size_inches()))
        saved_titles.append([axis.get_title() for axis in fig.axes])
        fig.savefig(path)

    monkeypatch.setattr(accv_visuals, "_save_pdf", capture_save)

    figure = accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)

    assert figure.path.is_file()
    assert figure.evidence == "link-aware package and generated-package robot task records"
    assert saved_axes_counts == [1]
    assert saved_sizes == [(12.2, 3.25)]
    assert saved_titles == [["Franka generated-package task smoke"]]
    assert "Package consumption metrics" not in saved_titles[0]


def test_save_franka_task_scene_raises_for_explicit_renderer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    monkeypatch.setenv("NEWTON_RENDER_ROOT", str(fake_root))
    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: fake_root)

    def fake_run(**kwargs: Any) -> Path:
        raise RuntimeError("renderer failed")

    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    with pytest.raises(RuntimeError, match="renderer failed"):
        accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)


def test_save_franka_task_scene_raises_when_auto_renderer_invocation_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    fake_root = tmp_path / "newton-render"
    (fake_root / "src/newton_render/render").mkdir(parents=True)
    (fake_root / "src/newton_render/render/paper_diagnostic_scenes.py").write_text("", encoding="utf-8")

    monkeypatch.setattr(accv_visuals, "_paper_scene_newton_render_root", lambda: fake_root)

    def fake_run(**kwargs: Any) -> Path:
        raise RuntimeError("auto renderer failed")

    monkeypatch.setattr(accv_visuals, "_run_newton_render_paper_scene", fake_run)

    with pytest.raises(RuntimeError, match="auto renderer failed"):
        accv_visuals._save_franka_task_scene(_franka_task_report_fixture(), tmp_path, plt)


def test_manifest_helpers_keep_source_records_and_pdf_metadata_stable() -> None:
    records = _split_evidence_sources("a.md; b.md; ; c.md")

    assert records == ("a.md", "b.md", "c.md")
    assert PDF_METADATA["Creator"] == "primitive_collision_compiler.paper.accv_visuals"
    assert PDF_METADATA["CreationDate"] == PDF_METADATA["ModDate"]


def test_write_manifest_preserves_renderer_provenance(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text('{"cases": []}\n', encoding="utf-8")
    figure_pdf = tmp_path / "figure.pdf"
    figure_pdf.write_bytes(b"%PDF-1.4\n")
    manifest = tmp_path / "manifest.json"

    accv_visuals._write_manifest(
        manifest,
        report_path=report,
        asset_root=tmp_path,
        figures=[
            accv_visuals.FigureOutput(
                "rendered_figure",
                figure_pdf,
                "newton-render test evidence",
                renderer_metadata={
                    "recipe": "mechanism_diagnostic_scene",
                    "renderer_source_hashes": {
                        "src/newton_render/render/paper_diagnostic_scenes.py": "abc123",
                    },
                    "sidecar": {"source_claim_boundary_note": "Diagnostic rendering; not a new Newton run."},
                },
            )
        ],
    )

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    rendered = payload["figures"][0]
    assert rendered["renderer_metadata"]["recipe"] == "mechanism_diagnostic_scene"
    assert (
        rendered["renderer_metadata"]["renderer_source_hashes"]["src/newton_render/render/paper_diagnostic_scenes.py"]
        == "abc123"
    )
    assert rendered["renderer_metadata"]["sidecar"]["source_claim_boundary_note"].startswith("Diagnostic rendering")


def test_source_record_hashes_fail_closed_for_missing_records() -> None:
    with pytest.raises(RuntimeError, match="missing source record"):
        _source_record_hashes(("docs/records/does-not-exist.md",))
