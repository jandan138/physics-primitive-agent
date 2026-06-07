from __future__ import annotations

import json
import hashlib
import re
import time
from pathlib import Path

import pytest
import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
SUPPLEMENTAL = PAPER / "shared/supplemental"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def supplement_source_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(SUPPLEMENTAL.glob("*.tex"))
    )


def test_accv_supplement_entrypoint_is_separate_from_main() -> None:
    main = read_text(PAPER / "venues/accv/main.tex")
    supplement = PAPER / "venues/accv/supplement.tex"

    assert supplement.exists()
    supplement_text = read_text(supplement)
    assert r"\input{preamble}" in supplement_text
    assert r"\bibliography{references}" in supplement_text
    assert "supplement" not in main.lower()
    assert "supplemental" not in main.lower()
    assert "appendix" not in main.lower()


def test_makefile_has_accv_supplement_targets() -> None:
    makefile = read_text(PAPER / "Makefile")
    assert "accv-supplement:" in makefile
    assert "accv-supp:" in makefile
    assert "accv-all:" in makefile
    assert "supplement.pdf" in makefile
    assert "bibtex build/supplement" in makefile
    assert r"grep -q '\\citation' build/supplement.aux" in makefile
    assert "No citations in supplement; skipping bibtex." in makefile


def test_supplement_does_not_duplicate_main_figures_or_tables() -> None:
    supplement_text = supplement_source_text()
    forbidden_main_items = (
        "pipeline_schematic_ai_slot.pdf",
        "bed_franka_mechanism_diagnostic.pdf",
        "phase0_asset_package_overlays.pdf",
        "phase0_asset_package_control_overlays.pdf",
        "phase0_outcome_matrix.pdf",
        "phase0_collision_probe_scenes.pdf",
        "franka_link_aware_rtx_task_scene.pdf",
        "franka_link_aware_task_scene.pdf",
        r"fig:bed-franka-mechanism",
        r"fig:phase0-overlays",
        r"fig:phase0-control-overlays",
        r"fig:phase0-outcome-matrix",
        r"fig:phase0-collision-scenes",
        r"fig:franka-task-scene",
        r"tab:phase0-grscenes-rigid",
        r"tab:phase0-failure-labels",
    )
    for forbidden in forbidden_main_items:
        assert forbidden not in supplement_text


def test_supplement_records_hard_constraints_and_claim_boundaries() -> None:
    supplement_text = supplement_source_text()
    required = (
        "The main paper is self-contained",
        "not copies of main-paper figures",
        "not copies of main-paper tables",
        "not whole-robot collision quality",
        "not manipulation evidence",
        "not deployment readiness",
        "not safety certification",
        "diagnostic checker",
        "simulation-checked",
    )
    for phrase in required:
        assert phrase in supplement_text


def test_supplement_source_preserves_double_blind_review() -> None:
    manifest = PAPER / "shared/figures/generated/supplement/manifest.json"
    slot_manifest = PAPER / "shared/figures/assets/supplement_ai_slots/manifest.yaml"
    combined = (
        read_text(PAPER / "venues/accv/supplement.tex")
        + "\n"
        + supplement_source_text()
        + "\n"
        + read_text(manifest)
        + "\n"
        + read_text(slot_manifest)
    )
    forbidden = (
        "github.com",
        "zhuzihou",
        "/cpfs/",
        "Physical Intelligence Center",
        "Acknowledgements",
        "Acknowledgments",
    )
    for phrase in forbidden:
        assert phrase not in combined


def test_supplement_uses_flexible_float_layout_for_text_flow() -> None:
    supplement_entrypoint = read_text(PAPER / "venues/accv/supplement.tex")
    supplement_text = supplement_source_text()

    assert r"\raggedbottom" in supplement_entrypoint
    assert r"\usepackage{placeins}" in read_text(PAPER / "venues/accv/preamble.tex")
    assert r"\begin{figure}[H]" not in supplement_text
    assert r"\begin{table}[H]" not in supplement_text
    assert supplement_text.count(r"\begin{figure}[tbp]") >= 8


def test_failure_storyboards_cannot_form_a_float_only_page() -> None:
    visual_atlas = read_text(SUPPLEMENTAL / "06_visual_atlas.tex")
    robot_section = read_text(SUPPLEMENTAL / "05_link_aware_robot.tex")

    storyboards = re.findall(
        r"\\begin\{figure\}\[(?P<placement>[^\]]+)\].*?"
        r"\\label\{(?P<label>fig:supp-failure-storyboard-[^}]+)\}.*?"
        r"\\end\{figure\}",
        visual_atlas,
        flags=re.DOTALL,
    )
    assert {label for _, label in storyboards} == {
        "fig:supp-failure-storyboard-bowl",
        "fig:supp-failure-storyboard-cup-tray",
    }
    for placement, _label in storyboards:
        assert "p" not in placement
        assert "h" in placement

    assert visual_atlas.count(r"\FloatBarrier") >= 4
    assert robot_section.rstrip().endswith(r"\FloatBarrier")


def test_large_robot_scene_figures_are_bound_to_their_explanatory_text() -> None:
    robot_section = read_text(SUPPLEMENTAL / "05_link_aware_robot.tex")

    for label in (
        "fig:supp-franka-link-frames",
        "fig:supp-generated-package-consumption",
        "fig:supp-franka-source-suppression",
    ):
        match = re.search(
            rf"\\label\{{{re.escape(label)}\}}\s*\\end\{{figure\}}\s*\\FloatBarrier",
            robot_section,
        )
        assert match is not None, label


def test_supplement_figure_manifest_records_sources() -> None:
    manifest = PAPER / "shared/figures/generated/supplement/manifest.json"
    assert manifest.exists()
    text = read_text(manifest)
    assert "supplement_predicate_drop_settle" in text
    assert "source_sha256" in text
    assert "claim_boundary" in text
    data = json.loads(text)
    assert not Path(data["manifest_path"]).is_absolute()
    for figure in data["figures"]:
        for source_record in figure["source_records"]:
            assert (ROOT / source_record).exists(), source_record


def test_supplement_ai_slot_manifest_covers_every_generated_figure() -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        DEFAULT_SLOT_MANIFEST,
        NEWTON_RTX_SUPPLEMENT_RENDERER,
        SCENE_EXPLANATION_FIGURE_IDS,
        SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS,
        SUPPLEMENT_FIGURE_IDS,
        TUTORIAL_2D_RENDERER,
        load_supplement_slot_manifest,
    )

    slot_manifest = load_supplement_slot_manifest(DEFAULT_SLOT_MANIFEST)

    assert slot_manifest["mode"] == "visual_composition"
    assert set(slot_manifest["slots"]) == set(SUPPLEMENT_FIGURE_IDS)
    assert "not experimental evidence" in slot_manifest["claim_boundary"]
    assert "not benchmark" in slot_manifest["claim_boundary"]
    for figure_id, slot in slot_manifest["slots"].items():
        asset = ROOT / slot["asset"]
        assert asset.is_file(), figure_id
        assert slot["prompt_summary"]
        assert slot["replaceable_by_real_render"] is True
        if figure_id in SCENE_EXPLANATION_FIGURE_IDS:
            assert slot["renderer"] == NEWTON_RTX_SUPPLEMENT_RENDERER
            sidecar = slot.get("sidecar")
            assert sidecar, figure_id
            assert not Path(sidecar).is_absolute(), figure_id
            assert (ROOT / str(sidecar)).is_file(), figure_id
        elif figure_id in SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS:
            assert slot["renderer"] == TUTORIAL_2D_RENDERER
            sidecar = slot.get("sidecar")
            assert sidecar, figure_id
            assert not Path(sidecar).is_absolute(), figure_id
            assert (ROOT / str(sidecar)).is_file(), figure_id
        else:
            assert slot["renderer"].startswith("visual_panel")


def test_supplement_figure_generator_records_ai_slot_provenance(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        NEWTON_RTX_SUPPLEMENT_RENDERER,
        SCENE_EXPLANATION_FIGURE_IDS,
        SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS,
        SUPPLEMENT_FIGURE_IDS,
        TUTORIAL_2D_RENDERER,
        generate_supplement_figures,
    )

    slot_manifest = _write_test_slot_manifest(tmp_path, SUPPLEMENT_FIGURE_IDS)
    output_dir = tmp_path / "supplement"

    manifest = generate_supplement_figures(
        output_dir=output_dir,
        slot_manifest_path=slot_manifest,
    )

    assert manifest["mode"] == "visual_composition"
    assert manifest["slot_manifest"].endswith("manifest.yaml")
    assert {figure["figure_id"] for figure in manifest["figures"]} == set(SUPPLEMENT_FIGURE_IDS)
    for figure in manifest["figures"]:
        assert figure["slot_asset"].endswith("_slot.png")
        assert len(figure["slot_sha256"]) == 64
        assert figure["slot_prompt_summary"] == f"test slot for {figure['figure_id']}"
        if figure["figure_id"] in SCENE_EXPLANATION_FIGURE_IDS:
            assert figure["slot_renderer"] == NEWTON_RTX_SUPPLEMENT_RENDERER
            assert figure["slot_sidecar"].endswith("_slot.json")
            assert len(figure["slot_sidecar_sha256"]) == 64
        elif figure["figure_id"] in SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS:
            assert figure["slot_renderer"] == TUTORIAL_2D_RENDERER
            assert figure["slot_sidecar"].endswith("_slot.json")
            assert len(figure["slot_sidecar_sha256"]) == 64
        else:
            assert figure["slot_renderer"].startswith("visual_panel")
        assert figure["slot_replaceable_by_real_render"] is True
        assert "visual-panel composer" in figure["composer"]


def test_supplement_slot_manifest_accepts_newton_rtx_scene_slots(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        NEWTON_RTX_SUPPLEMENT_RENDERER,
        SCENE_EXPLANATION_FIGURE_IDS,
        SUPPLEMENT_FIGURE_IDS,
        load_supplement_slot_manifest,
    )

    slot_manifest = _write_test_slot_manifest(tmp_path, SUPPLEMENT_FIGURE_IDS)
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    scene_id = next(iter(SCENE_EXPLANATION_FIGURE_IDS))
    sidecar = tmp_path / "scene_sidecar.json"
    sidecar.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "figure_id": scene_id,
                "renderer": NEWTON_RTX_SUPPLEMENT_RENDERER,
                "newton": {"root": "external/newton", "commit": "test"},
                "rtx": {"renderer": NEWTON_RTX_SUPPLEMENT_RENDERER, "ovrtx_version": "test"},
                "claim_boundary": "Visual exposition only; not benchmark evidence.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    data["slots"][scene_id]["renderer"] = NEWTON_RTX_SUPPLEMENT_RENDERER
    data["slots"][scene_id]["sidecar"] = str(sidecar)
    slot_manifest.write_text(yaml.safe_dump(data, sort_keys=True), encoding="utf-8")

    loaded = load_supplement_slot_manifest(slot_manifest, required_ids=(scene_id,))

    assert loaded["slots"][scene_id]["renderer"] == NEWTON_RTX_SUPPLEMENT_RENDERER
    assert loaded["slots"][scene_id]["sidecar"] == str(sidecar)


def test_supplement_slot_manifest_accepts_2d_tutorial_slots(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS,
        TUTORIAL_2D_RENDERER,
        load_supplement_slot_manifest,
    )

    tutorial_id = next(iter(SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS))
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))

    loaded = load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))

    assert loaded["slots"][tutorial_id]["renderer"] == TUTORIAL_2D_RENDERER
    assert loaded["slots"][tutorial_id]["sidecar"].endswith("_slot.json")


def test_supplement_slot_manifest_rejects_mismatched_2d_tutorial_sidecar(
    tmp_path: Path,
) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        TUTORIAL_2D_RENDERER,
        load_supplement_slot_manifest,
    )

    tutorial_id = "supplement_candidate_lane_anatomy"
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    sidecar = Path(data["slots"][tutorial_id]["sidecar"])
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    payload["figure_id"] = "supplement_provenance_flow"
    payload["renderer"] = TUTORIAL_2D_RENDERER
    sidecar.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="sidecar figure_id"):
        load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))


def test_supplement_slot_manifest_rejects_stale_2d_tutorial_sidecar_hash(
    tmp_path: Path,
) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        load_supplement_slot_manifest,
    )

    tutorial_id = "supplement_candidate_lane_anatomy"
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    sidecar = Path(data["slots"][tutorial_id]["sidecar"])
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    payload["slot_sha256"] = "0" * 64
    sidecar.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="sidecar slot_sha256"):
        load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))


def test_supplement_slot_manifest_rejects_stale_2d_tutorial_panel_count(
    tmp_path: Path,
) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        load_supplement_slot_manifest,
    )

    tutorial_id = "supplement_provenance_flow"
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    sidecar = Path(data["slots"][tutorial_id]["sidecar"])
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    payload["panel_count"] = 3
    payload["panels"] = payload["panels"][:3]
    sidecar.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="sidecar panel_count"):
        load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))


def test_supplement_slot_manifest_rejects_bad_2d_tutorial_segment_bounds(
    tmp_path: Path,
) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        load_supplement_slot_manifest,
    )

    tutorial_id = "supplement_franka_source_suppression"
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    sidecar = Path(data["slots"][tutorial_id]["sidecar"])
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    payload["slot_composition"]["segment_bounds_x"] = [0.0, 0.5, 1.0]
    sidecar.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="sidecar segment bounds"):
        load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))


def test_supplement_slot_manifest_rejects_weak_2d_tutorial_claim_boundary(
    tmp_path: Path,
) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        load_supplement_slot_manifest,
    )

    tutorial_id = "supplement_candidate_lane_anatomy"
    slot_manifest = _write_test_slot_manifest(tmp_path, (tutorial_id,))
    data = yaml.safe_load(slot_manifest.read_text(encoding="utf-8"))
    sidecar = Path(data["slots"][tutorial_id]["sidecar"])
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    payload["claim_boundary"] = "Visual exposition only; not experimental evidence."
    sidecar.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing claim boundary"):
        load_supplement_slot_manifest(slot_manifest, required_ids=(tutorial_id,))


def test_supplement_figure_composer_uses_ai_slots_instead_of_program_scene_drawer() -> None:
    source = read_text(ROOT / "src/primitive_collision_compiler/paper/accv_supplement_figures.py")

    assert "class _PanelScenes" not in source
    assert "def _draw_panel_scene" not in source
    assert "load_supplement_slot_manifest" in source
    assert "_paste_slot_strip" in source


def test_supplement_figure_composer_preserves_slot_segments_without_center_crop() -> None:
    source = read_text(ROOT / "src/primitive_collision_compiler/paper/accv_supplement_figures.py")

    assert "ImageOps.fit" not in source
    assert "ImageOps.contain" in source
    assert "_slot_segments" in source


def test_supplement_figure_generator_outputs_non_main_figure_names(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        SUPPLEMENT_FIGURE_IDS,
        generate_supplement_figures,
    )

    output_dir = tmp_path / "supplement"
    manifest = generate_supplement_figures(output_dir=output_dir)

    assert len(SUPPLEMENT_FIGURE_IDS) >= 10
    assert all(path.name.startswith("supplement_") for path in output_dir.glob("*.pdf"))
    assert "phase0_outcome_matrix" not in "\n".join(SUPPLEMENT_FIGURE_IDS)
    assert manifest["schema_version"] == 1
    assert manifest["manifest_path"].endswith("manifest.json")
    assert not Path(manifest["manifest_path"]).is_absolute()
    assert all(item["claim_boundary"] for item in manifest["figures"])
    assert all(item["source_sha256"] for item in manifest["figures"])


def test_supplement_figure_generation_is_reproducible(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import generate_supplement_figures

    first = generate_supplement_figures(output_dir=tmp_path / "first")
    time.sleep(1.1)
    second = generate_supplement_figures(output_dir=tmp_path / "second")

    fields = ("figure_id", "png_sha256", "pdf_sha256", "source_sha256")
    assert [
        tuple(figure[field] for field in fields) for figure in first["figures"]
    ] == [
        tuple(figure[field] for field in fields) for figure in second["figures"]
    ]


def test_supplement_ai_slot_edges_are_preserved_in_panel_strip(tmp_path: Path) -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        SUPPLEMENT_FIGURE_IDS,
        _panel_boxes,
        generate_supplement_figures,
    )

    slot_manifest = _write_test_slot_manifest(
        tmp_path,
        SUPPLEMENT_FIGURE_IDS,
        edge_markers=True,
    )
    output_dir = tmp_path / "supplement"

    generate_supplement_figures(output_dir=output_dir, slot_manifest_path=slot_manifest)

    rendered = Image.open(output_dir / "supplement_predicate_drop_settle.png").convert("RGB")
    boxes = _panel_boxes(3)
    first_inner = (boxes[0][0] + 34, boxes[0][1] + 100, boxes[0][0] + 84, boxes[0][3] - 70)
    last_inner = (boxes[-1][2] - 84, boxes[-1][1] + 100, boxes[-1][2] - 34, boxes[-1][3] - 70)
    red_pixels = _count_pixels(rendered.crop(first_inner), lambda r, g, b: r > 180 and g < 90 and b < 90)
    blue_pixels = _count_pixels(rendered.crop(last_inner), lambda r, g, b: r < 90 and g < 140 and b > 180)

    assert red_pixels > 400
    assert blue_pixels > 400


def test_supplement_body_uses_new_figures_and_teaching_material() -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import SUPPLEMENT_FIGURE_IDS

    supplement_text = supplement_source_text()
    for figure_id in SUPPLEMENT_FIGURE_IDS:
        expected_path = f"figures/generated/supplement/{figure_id}.pdf"
        assert expected_path in supplement_text

    assert supplement_text.count(r"\includegraphics") >= len(SUPPLEMENT_FIGURE_IDS)
    assert supplement_text.count(r"\begin{table}") >= 5
    assert supplement_text.count(r"\paragraph{Reading note.}") >= 10
    for phrase in (
        "parallel-axis theorem",
        "cross-link merge",
        "source-shape suppression",
        "generated self-collision filter",
        "diagnostic parameter table",
        "artifact provenance table",
        "not a method comparison",
        "not a new quantitative result",
        "unsubmitted",
        "does not broaden what",
    ):
        assert phrase in supplement_text


def test_supplement_figure_panels_do_not_spill_into_gutters(tmp_path: Path) -> None:
    from PIL import Image

    from primitive_collision_compiler.paper.accv_supplement_figures import (
        _panel_boxes,
        generate_supplement_figures,
    )

    output_dir = tmp_path / "supplement"
    generate_supplement_figures(output_dir=output_dir)

    def dark_pixel_count(path: Path, box: tuple[int, int, int, int]) -> int:
        pixels = Image.open(path).convert("RGB").crop(box).getdata()
        return sum(1 for red, green, blue in pixels if max(red, green, blue) < 220)

    for figure_id, panel_count in (
        ("supplement_franka_link_frames", 3),
        ("supplement_provenance_flow", 4),
    ):
        png = output_dir / f"{figure_id}.png"
        boxes = _panel_boxes(panel_count)
        for left, right in zip(boxes, boxes[1:]):
            gutter = (left[2] + 4, left[1] + 95, right[0] - 4, left[3] - 70)
            assert dark_pixel_count(png, gutter) <= 100

    cup_tray = output_dir / "supplement_failure_storyboard_cup_tray.png"
    boxes = _panel_boxes(4)
    for box in (boxes[0], boxes[-1]):
        right_edge = (box[2] - 34, box[1] + 95, box[2] - 4, box[3] - 70)
        assert dark_pixel_count(cup_tray, right_edge) <= 150


def _write_test_slot_manifest(
    tmp_path: Path,
    figure_ids: tuple[str, ...],
    *,
    edge_markers: bool = False,
) -> Path:
    from primitive_collision_compiler.paper.accv_supplement_figures import (
        FIGURE_SPECS,
        NEWTON_RTX_SUPPLEMENT_RENDERER,
        SCENE_EXPLANATION_FIGURE_IDS,
        SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS,
        TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES,
        TUTORIAL_2D_RENDERER,
    )

    asset_dir = tmp_path / "assets"
    panel_counts = {spec.figure_id: len(spec.panels) for spec in FIGURE_SPECS}
    slots: dict[str, dict[str, object]] = {}
    for index, figure_id in enumerate(figure_ids):
        slot = asset_dir / f"{figure_id}_slot.png"
        if edge_markers:
            _edge_marker_slot(slot)
        else:
            color = ["#dae9ff", "#e6f4df", "#fff0d3", "#eee8ff"][index % 4]
            _solid_slot(slot, color)
        slots[figure_id] = {
            "asset": str(slot),
            "renderer": "visual_panel_slot",
            "prompt_summary": f"test slot for {figure_id}",
            "replaceable_by_real_render": True,
        }
        if figure_id in SCENE_EXPLANATION_FIGURE_IDS:
            sidecar = asset_dir / f"{figure_id}_slot.json"
            sidecar.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "figure_id": figure_id,
                        "renderer": NEWTON_RTX_SUPPLEMENT_RENDERER,
                        "newton": {"root": "external/newton", "commit": "test"},
                        "rtx": {
                            "renderer": NEWTON_RTX_SUPPLEMENT_RENDERER,
                            "ovrtx_version": "test",
                        },
                        "claim_boundary": "Visual exposition only; not benchmark evidence.",
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            slots[figure_id]["renderer"] = NEWTON_RTX_SUPPLEMENT_RENDERER
            slots[figure_id]["sidecar"] = str(sidecar)
        elif figure_id in SUPPLEMENT_2D_TUTORIAL_FIGURE_IDS:
            panel_count = panel_counts[figure_id]
            sidecar = asset_dir / f"{figure_id}_slot.json"
            sidecar.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "figure_id": figure_id,
                        "renderer": TUTORIAL_2D_RENDERER,
                        "style": "academic_2d_panel",
                        "slot_asset": slot.name,
                        "slot_sha256": _sha256_file(slot),
                        "slot_composition": {
                            "segment_bounds_x": [
                                index / panel_count for index in range(panel_count + 1)
                            ],
                        },
                        "panel_count": panel_count,
                        "panels": [{"label": f"panel {index}"} for index in range(panel_count)],
                        "claim_boundary": (
                            "Visual exposition only; "
                            + ", ".join(TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES)
                            + "."
                        ),
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            slots[figure_id]["renderer"] = TUTORIAL_2D_RENDERER
            slots[figure_id]["sidecar"] = str(sidecar)

    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "mode": "visual_composition",
                "slots": slots,
                "claim_boundary": "Visual panels explain the scoped diagnostic path; not experimental evidence and not benchmark evidence.",
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return manifest


def _solid_slot(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1200, 520), color).save(path)


def _edge_marker_slot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1200, 520), "#eef2f7")
    for x in range(0, 90):
        for y in range(image.height):
            image.putpixel((x, y), (220, 35, 35))
    for x in range(image.width - 90, image.width):
        for y in range(image.height):
            image.putpixel((x, y), (35, 95, 220))
    image.save(path)


def _count_pixels(image: Image.Image, predicate) -> int:
    return sum(1 for r, g, b in image.getdata() if predicate(r, g, b))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
