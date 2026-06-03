from __future__ import annotations

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
    combined = read_text(PAPER / "venues/accv/supplement.tex") + "\n" + supplement_source_text()
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
    assert manifest["manifest_path"] == str(output_dir / "manifest.json")
    assert all(item["claim_boundary"] for item in manifest["figures"])
    assert all(item["source_sha256"] for item in manifest["figures"])
