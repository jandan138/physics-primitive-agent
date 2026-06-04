from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TUTORIAL_IDS = {
    "supplement_candidate_lane_anatomy",
    "supplement_compound_body_state_teaching",
    "supplement_franka_link_frames",
    "supplement_generated_package_consumption",
    "supplement_franka_source_suppression",
    "supplement_provenance_flow",
}

EXPECTED_PANEL_COUNTS = {
    "supplement_candidate_lane_anatomy": 3,
    "supplement_compound_body_state_teaching": 3,
    "supplement_franka_link_frames": 3,
    "supplement_generated_package_consumption": 3,
    "supplement_franka_source_suppression": 3,
    "supplement_provenance_flow": 4,
}


def test_supplement_tutorial_2d_slot_ids_are_explicit() -> None:
    from primitive_collision_compiler.paper.supplement_tutorial_2d_slots import (
        SUPPLEMENT_2D_TUTORIAL_SLOT_IDS,
    )

    assert set(SUPPLEMENT_2D_TUTORIAL_SLOT_IDS) == EXPECTED_TUTORIAL_IDS


def test_supplement_ai_tutorial_sidecar_writer_records_checked_assets(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.supplement_tutorial_2d_slots import (
        TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES,
        TUTORIAL_2D_RENDERER,
        write_supplement_ai_tutorial_sidecars,
    )

    for figure_id, panel_count in EXPECTED_PANEL_COUNTS.items():
        Image.new("RGB", (640 * panel_count, 480), "#eef2f7").save(
            tmp_path / f"{figure_id}_slot.png"
        )

    outputs = write_supplement_ai_tutorial_sidecars(output_dir=tmp_path)

    assert {path.stem.removesuffix("_slot") for path in outputs} == EXPECTED_TUTORIAL_IDS
    for sidecar in outputs:
        figure_id = sidecar.stem.removesuffix("_slot")
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        serialized = json.dumps(payload, sort_keys=True)
        assert payload["renderer"] == TUTORIAL_2D_RENDERER
        assert payload["figure_id"] == figure_id
        assert payload["style"] == "ai_generated_academic_2d_tutorial"
        assert payload["panel_count"] == EXPECTED_PANEL_COUNTS[figure_id]
        assert len(payload["panels"]) == EXPECTED_PANEL_COUNTS[figure_id]
        segment_bounds = payload["slot_composition"]["segment_bounds_x"]
        assert len(segment_bounds) == EXPECTED_PANEL_COUNTS[figure_id] + 1
        assert segment_bounds[0] == 0.0
        assert segment_bounds[-1] == 1.0
        assert payload["slot_sha256"]
        for phrase in TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES:
            assert phrase in payload["claim_boundary"]
        assert "/cpfs/" not in serialized
        assert "zhuzihou" not in serialized


def test_supplement_tutorial_slot_module_does_not_program_draw_panels() -> None:
    source = (ROOT / "src/primitive_collision_compiler/paper/supplement_tutorial_2d_slots.py").read_text(
        encoding="utf-8"
    )

    assert "ImageDraw" not in source
    assert "rounded_rectangle" not in source
    assert "draw." not in source


def test_checked_in_franka_tutorial_slots_are_not_reused_images() -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        DEFAULT_SLOT_MANIFEST,
        load_supplement_slot_manifest,
    )

    manifest = load_supplement_slot_manifest(DEFAULT_SLOT_MANIFEST)
    figure_ids = (
        "supplement_franka_link_frames",
        "supplement_generated_package_consumption",
        "supplement_franka_source_suppression",
    )
    slot_hashes = {
        figure_id: _sha256_file(ROOT / manifest["slots"][figure_id]["asset"])
        for figure_id in figure_ids
    }

    assert len(set(slot_hashes.values())) == len(slot_hashes)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
