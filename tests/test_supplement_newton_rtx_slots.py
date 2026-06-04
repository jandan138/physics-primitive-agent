from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_SCENE_IDS = {
    "supplement_predicate_drop_settle",
    "supplement_predicate_stack_slide",
    "supplement_predicate_sphere_rain",
    "supplement_generated_package_consumption",
    "supplement_compound_body_state_teaching",
    "supplement_franka_link_frames",
    "supplement_franka_source_suppression",
    "supplement_failure_storyboard_bowl",
    "supplement_failure_storyboard_cup_tray",
}


def test_scene_explanation_slot_ids_are_explicit() -> None:
    from primitive_collision_compiler.paper.supplement_newton_rtx_slots import (
        SUPPLEMENT_NEWTON_RTX_SLOT_IDS,
    )

    assert set(SUPPLEMENT_NEWTON_RTX_SLOT_IDS) == EXPECTED_SCENE_IDS


def test_build_supplement_newton_rtx_worker_command_sets_isolated_environment(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.supplement_newton_rtx_slots import (
        build_supplement_newton_rtx_worker_command,
    )

    command, env = build_supplement_newton_rtx_worker_command(
        output_dir=tmp_path / "slots",
        python_executable="/env/bin/python",
        newton_root="/external/newton",
    )

    assert command[:3] == ["/env/bin/python", "-m", "primitive_collision_compiler.paper.supplement_newton_rtx_slots"]
    assert "--worker-render" in command
    assert "--output-dir" in command
    assert str(tmp_path / "slots") in command
    assert env["PYTHONPATH"].split(":")[:3] == ["/external/newton", str(ROOT / "src"), str(ROOT)]


def test_compose_slot_strip_contains_each_rtx_panel_without_center_crop(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.supplement_newton_rtx_slots import (
        RTX_PANEL_SIZE,
        SLOT_TILE_SIZE,
        compose_slot_strip,
    )

    assert SLOT_TILE_SIZE[0] == RTX_PANEL_SIZE[0]
    assert SLOT_TILE_SIZE[1] > RTX_PANEL_SIZE[1]

    panel_dir = tmp_path / "panels"
    panel_dir.mkdir()
    panels = []
    for index, color in enumerate(("#d8e8ff", "#e6f3dd", "#fff0d0")):
        panel = Image.new("RGB", (320, 260), color)
        for y in range(panel.height):
            panel.putpixel((0, y), (220, 30, 30))
            panel.putpixel((panel.width - 1, y), (35, 95, 220))
        path = panel_dir / f"panel_{index}.png"
        panel.save(path)
        panels.append(path)

    output = tmp_path / "slot.png"
    compose_slot_strip(panels, output=output, panel_size=(300, 280))

    rendered = Image.open(output).convert("RGB")
    assert rendered.size == (900, 280)
    for index in range(3):
        crop = rendered.crop((index * 300, 0, (index + 1) * 300, 280))
        red_pixels = sum(1 for r, g, b in crop.crop((0, 0, 24, 280)).getdata() if r > 180 and g < 80 and b < 80)
        blue_pixels = sum(
            1 for r, g, b in crop.crop((276, 0, 300, 280)).getdata() if r < 90 and g < 140 and b > 180
        )
        assert red_pixels > 80
        assert blue_pixels > 80


def test_write_supplement_newton_rtx_sidecar_is_anonymous(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.supplement_newton_rtx_slots import (
        NEWTON_RTX_SUPPLEMENT_RENDERER,
        SLOT_TILE_SIZE,
        write_supplement_newton_rtx_sidecar,
    )

    slot = tmp_path / "slot.png"
    panel = tmp_path / "panel.png"
    Image.new("RGB", (80, 80), "#d8e8ff").save(slot)
    Image.new("RGB", (80, 80), "#e6f3dd").save(panel)
    sidecar = tmp_path / "slot.json"

    write_supplement_newton_rtx_sidecar(
        figure_id="supplement_predicate_drop_settle",
        output_sidecar=sidecar,
        slot_asset=slot,
        panel_assets=[panel],
        newton_root="/cpfs/shared/simulation/zhuzihou/dev/newton",
        newton_commit="9f544c81e460",
        ovrtx_version="0.3.0",
        recipe="unit_test_scene",
    )

    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    serialized = json.dumps(payload, sort_keys=True)
    assert payload["renderer"] == NEWTON_RTX_SUPPLEMENT_RENDERER
    assert payload["figure_id"] == "supplement_predicate_drop_settle"
    assert payload["slot_sha256"]
    assert payload["slot_composition"]["tile_size"] == list(SLOT_TILE_SIZE)
    assert payload["panel_count"] == 1
    assert "/cpfs/" not in serialized
    assert "zhuzihou" not in serialized
