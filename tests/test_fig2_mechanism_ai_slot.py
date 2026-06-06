from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from PIL import Image

from primitive_collision_compiler.paper.fig2_mechanism_ai_slot import (
    FIG2_OUTPUT_SIZE,
    REQUIRED_SLOTS,
    compose_fig2_mechanism_ai_slot,
    load_fig2_slot_manifest,
)


def test_load_fig2_slot_manifest_requires_ai_slot_contract(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)

    payload = load_fig2_slot_manifest(manifest)

    assert payload["figure_id"] == "bed_franka_mechanism_diagnostic"
    assert payload["mode"] == "visual_composition"
    assert set(payload["slots"]) == set(REQUIRED_SLOTS)
    assert "not experimental evidence" in payload["claim_boundary"]


def test_load_fig2_slot_manifest_rejects_missing_slot(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    payload = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    payload["slots"].pop("mechanism_audit")
    manifest.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")

    with pytest.raises(ValueError, match="missing slots"):
        load_fig2_slot_manifest(manifest)


def test_compose_fig2_mechanism_ai_slot_creates_png_pdf_and_metadata(tmp_path: Path) -> None:
    manifest = _write_manifest(tmp_path)
    output = tmp_path / "bed_franka_mechanism_diagnostic.pdf"

    metadata = compose_fig2_mechanism_ai_slot(
        output,
        manifest_path=manifest,
        metrics={
            "bed_final_speed_mps": 0.0824,
            "franka_final_speed_mps": 0.00071,
            "settle_gate_mps": 0.01,
        },
    )

    assert output.is_file()
    assert output.with_suffix(".png").is_file()
    with Image.open(output.with_suffix(".png")) as image:
        assert image.size == FIG2_OUTPUT_SIZE
    assert metadata["mode"] == "visual_composition"
    assert metadata["composer"] == "primitive_collision_compiler.paper.fig2_mechanism_ai_slot"
    assert set(metadata["slot_sha256"]) == set(REQUIRED_SLOTS)
    assert "not experimental evidence" in metadata["claim_boundary"]


def _write_manifest(tmp_path: Path) -> Path:
    asset_dir = tmp_path / "slots"
    asset_dir.mkdir()
    slots: dict[str, dict[str, object]] = {}
    colors = {
        "isolated_target_pass": "#d7efe3",
        "full_package_fail": "#f6d1ce",
        "mechanism_audit": "#fff2cf",
    }
    for slot_name in REQUIRED_SLOTS:
        asset = asset_dir / f"{slot_name}.png"
        Image.new("RGB", (640, 420), colors[slot_name]).save(asset)
        slots[slot_name] = {
            "asset": str(asset),
            "renderer": "visual_panel_test_slot",
            "prompt_summary": f"test slot for {slot_name}",
            "replaceable_by_real_render": True,
        }
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "figure_id": "bed_franka_mechanism_diagnostic",
                "mode": "visual_composition",
                "slots": slots,
                "replaceable_by_real_render": list(REQUIRED_SLOTS),
                "claim_boundary": (
                    "Fig.2 visual panels explain the recorded mechanism; not experimental evidence and not benchmark evidence."
                ),
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return manifest
