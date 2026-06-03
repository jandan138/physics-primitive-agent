from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image

from primitive_collision_compiler.paper.franka_rtx_task_scene import (
    FRANKA_RTX_TASK_CLAIM_BOUNDARY,
    build_franka_rtx_task_worker_command,
    compose_franka_rtx_task_scene_from_verified_slot,
    compose_franka_rtx_task_scene_plate,
    franka_rtx_task_summary,
    load_franka_rtx_task_sidecar,
)


ROOT = Path(__file__).resolve().parents[1]


def _franka_case() -> dict[str, object]:
    return {
        "asset_id": "franka_import_smoke",
        "asset_role": "franka_import_smoke",
        "local_path": "assets/raw/mirrors/franka/franka.usd",
        "robot_package_result": {
            "status": "generated",
            "primitive_or_hull_count": 12,
            "links": [
                {"link_path": f"/panda/panda_link{index}", "placeholder_primitive_count": 0}
                for index in range(12)
            ],
            "collision_package": {"method": "link_aware_bounding_boxes", "primitives": [{}] * 12},
            "link_boundary_audit": {
                "status": "smoke_passed",
                "metrics": {
                    "link_count": 12,
                    "primitive_count": 12,
                    "cross_link_merge_count": 0,
                    "meshless_link_placeholder_count": 1,
                },
            },
        },
        "probe_results": {
            "generated_package_robot_task_if_robot": {
                "outcome": "accept",
                "status": "smoke_passed",
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


def test_worker_command_uses_shared_newton_and_source_root(tmp_path: Path) -> None:
    command, env = build_franka_rtx_task_worker_command(
        output_png=tmp_path / "figure.png",
        output_pdf=tmp_path / "figure.pdf",
        sidecar=tmp_path / "figure.json",
        source_artifact_root=Path("/source/root"),
        python_executable=Path("/env/bin/python"),
        newton_root=Path("/shared/newton"),
        phase0_report=Path("reports/generated/phase0.json"),
        asset_manifest=Path("assets/manifests/franka.yaml"),
    )

    assert command[:3] == [
        "/env/bin/python",
        "-m",
        "primitive_collision_compiler.paper.franka_rtx_task_scene",
    ]
    assert "--worker-render" in command
    assert str(tmp_path / "figure.png") in command
    assert str(tmp_path / "figure.pdf") in command
    assert str(tmp_path / "figure.json") in command
    assert env["PPA_FRANKA_RTX_TASK_SOURCE_ARTIFACT_ROOT"] == "/source/root"
    pythonpath_parts = env["PYTHONPATH"].split(os.pathsep)
    assert pythonpath_parts[0] == "/shared/newton"
    assert str(ROOT / "src") in pythonpath_parts
    assert str(ROOT) in pythonpath_parts


def test_franka_rtx_task_summary_preserves_link_consumption_metrics() -> None:
    summary = franka_rtx_task_summary(_franka_case())

    assert summary["asset_role"] == "franka_import_smoke"
    assert summary["link_count"] == 12
    assert summary["primitive_count"] == 12
    assert summary["missing_body_link_count"] == 0
    assert summary["source_usd_shape_count"] == 0
    assert summary["self_collision_filter_pair_count"] == 66
    assert summary["task_outcome"] == "accept"
    assert "not whole-robot collision quality" in summary["claim_boundary"]


def test_compose_plate_writes_pdf_png_and_traceable_sidecar(tmp_path: Path) -> None:
    raw_render = tmp_path / "raw.png"
    Image.new("RGB", (320, 200), "#53606d").save(raw_render)
    output_png = tmp_path / "franka_link_aware_rtx_task_scene.png"
    output_pdf = tmp_path / "franka_link_aware_rtx_task_scene.pdf"
    sidecar = tmp_path / "franka_link_aware_rtx_task_scene.json"

    compose_franka_rtx_task_scene_plate(
        raw_render=raw_render,
        output_png=output_png,
        output_pdf=output_pdf,
        sidecar=sidecar,
        case=_franka_case(),
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/franka.yaml"),
        source_asset=Path("/source/franka.usd"),
        source_artifact_root=Path("/source"),
        newton_root=Path("/shared/newton"),
        newton_commit="abc123def456",
        ovrtx_version="0.3.0.312915",
    )

    assert output_png.is_file()
    assert output_pdf.is_file()
    payload = load_franka_rtx_task_sidecar(sidecar)
    assert payload["renderer"] == "newton_viewer_rtx_ovrtx"
    assert payload["raw_render"] == str(raw_render)
    assert payload["output_pdf"] == str(output_pdf)
    assert payload["summary"]["task_outcome"] == "accept"
    assert payload["summary"]["self_collision_filter_pair_count"] == 66
    assert payload["claim_boundary"] == FRANKA_RTX_TASK_CLAIM_BOUNDARY
    assert "not manipulation" in payload["claim_boundary"]


def test_compose_plate_records_repo_relative_rtx_source_when_available(tmp_path: Path) -> None:
    raw_render = ROOT / "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.png"
    output_png = tmp_path / "franka_link_aware_rtx_task_scene.png"
    output_pdf = tmp_path / "franka_link_aware_rtx_task_scene.pdf"
    sidecar = tmp_path / "franka_link_aware_rtx_task_scene.json"

    compose_franka_rtx_task_scene_plate(
        raw_render=raw_render,
        output_png=output_png,
        output_pdf=output_pdf,
        sidecar=sidecar,
        case=_franka_case(),
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/franka.yaml"),
        source_asset=Path("/source/franka.usd"),
        source_artifact_root=Path("/source"),
        newton_root=Path("/shared/newton"),
        newton_commit="abc123def456",
        ovrtx_version="0.3.0.312915",
        source_rtx_sidecar=ROOT / "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.json",
    )

    payload = load_franka_rtx_task_sidecar(sidecar)
    assert payload["raw_render"] == "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.png"
    assert payload["source_rtx_sidecar"] == "paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.json"
    assert payload["source_rtx_sidecar_sha256"]
    assert payload["output_pdf"] == str(output_pdf)


def test_default_compose_path_uses_verified_rtx_slot_metadata(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    report = source_root / "reports/generated/phase0.json"
    manifest = source_root / "assets/manifests/franka.yaml"
    report.parent.mkdir(parents=True)
    manifest.parent.mkdir(parents=True)
    report.write_text(json.dumps({"articulation_cases": [_franka_case()]}), encoding="utf-8")
    manifest.write_text("assets: []\n", encoding="utf-8")
    verified_render = tmp_path / "verified.png"
    Image.new("RGB", (640, 420), "#4f667c").save(verified_render)
    verified_sidecar = tmp_path / "verified.json"
    verified_sidecar.write_text(
        json.dumps(
            {
                "renderer": "newton_viewer_rtx_ovrtx",
                "newton": {"commit": "verified123"},
                "rtx": {"ovrtx_version": "0.3.0.312915"},
            }
        ),
        encoding="utf-8",
    )
    output_png = tmp_path / "franka_link_aware_rtx_task_scene.png"
    output_pdf = tmp_path / "franka_link_aware_rtx_task_scene.pdf"
    sidecar = tmp_path / "franka_link_aware_rtx_task_scene.json"

    output = compose_franka_rtx_task_scene_from_verified_slot(
        output_png=output_png,
        output_pdf=output_pdf,
        sidecar=sidecar,
        verified_rtx_render=verified_render,
        verified_rtx_sidecar=verified_sidecar,
        source_artifact_root=source_root,
        phase0_report=Path("reports/generated/phase0.json"),
        asset_manifest=Path("assets/manifests/franka.yaml"),
        newton_root=Path("/shared/newton"),
    )

    payload = load_franka_rtx_task_sidecar(sidecar)
    assert output == output_pdf
    assert payload["newton"]["commit"] == "verified123"
    assert payload["rtx"]["ovrtx_version"] == "0.3.0.312915"
    assert payload["source_rtx_sidecar"] == str(verified_sidecar)
    assert payload["source_report"] == "reports/generated/phase0.json"
    assert payload["source_manifest"] == "assets/manifests/franka.yaml"
    assert payload["source_asset"] == "assets/raw/mirrors/franka/franka.usd"
    assert payload["summary"]["missing_body_link_count"] == 0


def test_experiments_registers_rtx_franka_body_figure() -> None:
    experiments = (ROOT / "paper/shared/sections/experiments.tex").read_text(encoding="utf-8")
    sources = (ROOT / "paper/shared/figures/sources.yaml").read_text(encoding="utf-8")

    assert "figures/generated/franka_link_aware_rtx_task_scene.pdf" in experiments
    assert "RTX view" in experiments
    assert "franka_link_aware_rtx_task_scene" in sources
    assert "not whole-robot collision-quality or manipulation evidence" in sources
