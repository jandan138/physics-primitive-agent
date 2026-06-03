from __future__ import annotations

import json
import time
from pathlib import Path


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
    combined = (
        read_text(PAPER / "venues/accv/supplement.tex")
        + "\n"
        + supplement_source_text()
        + "\n"
        + read_text(manifest)
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


def test_supplement_body_uses_new_figures_and_teaching_material() -> None:
    from primitive_collision_compiler.paper.accv_supplement_figures import SUPPLEMENT_FIGURE_IDS

    supplement_text = supplement_source_text()
    for figure_id in SUPPLEMENT_FIGURE_IDS:
        expected_path = f"figures/generated/supplement/{figure_id}.pdf"
        assert expected_path in supplement_text

    assert supplement_text.count(r"\includegraphics") >= len(SUPPLEMENT_FIGURE_IDS)
    assert supplement_text.count(r"\begin{table}") >= 5
    assert supplement_text.count(r"\paragraph{What this shows.}") >= 10
    assert supplement_text.count(r"\paragraph{What this does not show.}") >= 10
    for phrase in (
        "parallel-axis theorem",
        "cross-link merge",
        "source-shape suppression",
        "generated self-collision filter",
        "diagnostic parameter table",
        "artifact provenance table",
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
