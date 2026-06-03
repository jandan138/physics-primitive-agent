from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image

from primitive_collision_compiler.paper.fig1_ai_slot import (
    FIG1_OUTPUT_SIZE,
    compose_fig1_ai_slot,
    load_fig1_slot_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
FIGURE_ROOT = ROOT / "paper/shared/figures"
FIG1_MANIFEST = FIGURE_ROOT / "assets/fig1_ai_slots/manifest.yaml"
FIG1_OUTPUT = FIGURE_ROOT / "generated/pipeline_schematic_ai_slot.pdf"


def _solid_slot(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (320, 240), color).save(path)


def _edge_marker_slot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (360, 240), "#d7dde7")
    for x in range(0, 40):
        for y in range(image.height):
            image.putpixel((x, y), (220, 30, 30))
    for x in range(image.width - 40, image.width):
        for y in range(image.height):
            image.putpixel((x, y), (30, 90, 220))
    image.save(path)


def test_compose_fig1_ai_slot_uses_manifest_slots_and_writes_pdf(tmp_path: Path) -> None:
    asset_dir = tmp_path / "assets"
    slots = {
        "asset_intake": asset_dir / "asset.png",
        "candidate_package": asset_dir / "candidate.png",
        "newton_diagnostics": asset_dir / "diagnostic.png",
        "decision_report": asset_dir / "decision.png",
    }
    for index, path in enumerate(slots.values()):
        _solid_slot(path, ["#d9e8ff", "#e6f3de", "#fff0d2", "#ebe5ff"][index])
    overview = asset_dir / "overview.png"
    _solid_slot(overview, "#f4f6f8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "figure_id": "pipeline_schematic_ai_slot",
                "mode": "hybrid_newton_ai_slot_composition",
                "overview_candidates": [str(overview)],
                "selected_overview": str(overview),
                "slots": {key: str(path) for key, path in slots.items()},
                "slot_sources": {
                    "asset_intake": {"renderer": "newton_sensor_tiled_camera"},
                    "candidate_package": {"renderer": "newton_sensor_tiled_camera"},
                    "newton_diagnostics": {"renderer": "newton_sensor_tiled_camera"},
                    "decision_report": {
                        "renderer": "built_in_imagegen_slots_plus_deterministic_pil_composition"
                    },
                },
                "replaceable_by_real_render": ["asset_intake", "newton_diagnostics"],
                "claim_boundary": "Exposition only; not experimental evidence.",
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "fig1.pdf"

    composed = compose_fig1_ai_slot(manifest_path=manifest, output_path=output)

    assert composed.path == output
    assert output.is_file()
    assert output.stat().st_size > 1_000
    assert composed.figure_id == "pipeline_schematic_ai_slot"
    assert composed.evidence == "Hybrid Newton/AI protocol schematic; exposition only"
    assert composed.renderer_metadata["mode"] == "hybrid_newton_ai_slot_composition"
    assert composed.renderer_metadata["output_size_px"] == list(FIG1_OUTPUT_SIZE)
    assert composed.renderer_metadata["slot_sources"]["asset_intake"]["renderer"] == "newton_sensor_tiled_camera"
    assert composed.renderer_metadata["slot_sources"]["decision_report"]["renderer"].startswith("built_in_imagegen")


def test_compose_fig1_ai_slot_preserves_full_slot_image_edges(tmp_path: Path) -> None:
    asset_dir = tmp_path / "assets"
    slots = {
        "asset_intake": asset_dir / "asset.png",
        "candidate_package": asset_dir / "candidate.png",
        "newton_diagnostics": asset_dir / "diagnostic.png",
        "decision_report": asset_dir / "decision.png",
    }
    for path in slots.values():
        _edge_marker_slot(path)
    overview = asset_dir / "overview.png"
    _solid_slot(overview, "#f4f6f8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "figure_id": "pipeline_schematic_ai_slot",
                "mode": "hybrid_newton_ai_slot_composition",
                "overview_candidates": [str(overview)],
                "selected_overview": str(overview),
                "slots": {key: str(path) for key, path in slots.items()},
                "slot_sources": {
                    "asset_intake": {"renderer": "newton_sensor_tiled_camera"},
                    "candidate_package": {"renderer": "newton_sensor_tiled_camera"},
                    "newton_diagnostics": {"renderer": "newton_sensor_tiled_camera"},
                    "decision_report": {
                        "renderer": "built_in_imagegen_slots_plus_deterministic_pil_composition"
                    },
                },
                "replaceable_by_real_render": list(slots),
                "claim_boundary": "Exposition only; not experimental evidence.",
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "fig1.pdf"

    compose_fig1_ai_slot(manifest_path=manifest, output_path=output)

    rendered = Image.open(output.with_suffix(".png")).convert("RGB")
    panel_w = 475
    top = 120
    left = 92
    gap = 88
    xs = [left + index * (panel_w + gap) for index in range(4)]
    for x in xs:
        slot_crop = rendered.crop((x + 34, top + 150, x + panel_w - 34, top + 590))
        colors = slot_crop.getdata()
        red_pixels = sum(1 for r, g, b in colors if r > 180 and g < 80 and b < 80)
        blue_pixels = sum(1 for r, g, b in colors if r < 80 and g < 130 and b > 180)
        assert red_pixels > 800
        assert blue_pixels > 800


def test_fig1_ai_slot_manifest_is_replaceable_and_claim_bounded() -> None:
    manifest = load_fig1_slot_manifest(FIG1_MANIFEST)

    assert manifest["mode"] == "hybrid_newton_ai_slot_composition"
    assert manifest["figure_id"] == "pipeline_schematic_ai_slot"
    assert set(manifest["slots"]) == {
        "asset_intake",
        "candidate_package",
        "newton_diagnostics",
        "decision_report",
    }
    slot_sources = manifest["slot_sources"]
    for slot in ("asset_intake", "candidate_package", "newton_diagnostics"):
        assert slot_sources[slot]["renderer"] == "newton_sensor_tiled_camera"
        assert "fig1_newton_slots" in manifest["slots"][slot]
    assert slot_sources["decision_report"]["renderer"].startswith("built_in_imagegen")
    assert "decision_report_ai.png" in manifest["slots"]["decision_report"]
    assert "decision_report" in manifest["replaceable_by_real_render"]
    assert "experimental evidence" in manifest["claim_boundary"]
    for path in manifest["slots"].values():
        assert (ROOT / path).is_file(), path


def test_fig1_ai_slot_is_integrated_into_accv_sources() -> None:
    schematic = (FIGURE_ROOT / "pipeline_schematic.tex").read_text(encoding="utf-8")
    sources = (FIGURE_ROOT / "sources.yaml").read_text(encoding="utf-8")

    assert FIG1_OUTPUT.is_file()
    assert "generated/pipeline_schematic_ai_slot.pdf" in schematic
    assert "pipeline_schematic_ai_slot" in sources
    assert "hybrid_newton_ai_slot_composition" in sources
    assert "newton_sensor_tiled_camera" in sources
    assert "not experimental evidence" in sources
