from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
VENUES = ("accv", "arxiv", "eccv", "neurips")
ACTIVE_DOCS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_shared_tree_and_evidence_registry() -> None:
    required_paths = (
        "shared/sections/abstract.tex",
        "shared/sections/intro.tex",
        "shared/sections/related.tex",
        "shared/sections/background.tex",
        "shared/sections/method.tex",
        "shared/sections/experiments.tex",
        "shared/sections/discussion.tex",
        "shared/sections/conclusion.tex",
        "shared/sections/appendix.tex",
        "shared/figures/sources.yaml",
        "shared/figures/pipeline_schematic.tex",
        "shared/tables/templates.tex",
        "shared/references.bib",
        "shared/math_commands.tex",
        "shared/venue_macros.tex",
        "shared/evidence/claims.yaml",
        "shared/evidence/results_manifest.yaml",
        "shared/supplemental/README.md",
        "shared/video/README.md",
    )
    for relative_path in required_paths:
        assert (PAPER / relative_path).exists(), relative_path

    claims = read_text(PAPER / "shared/evidence/claims.yaml")
    results = read_text(PAPER / "shared/evidence/results_manifest.yaml")
    assert "schema_version:" in claims
    assert "claims:" in claims
    assert "bed_franka_cylinder_mechanism" in claims
    assert "schema_version:" in results
    assert "results:" in results
    assert "bed_box_contact_throughput_microbenchmark" in results


def test_venue_entrypoints_status_and_preambles() -> None:
    for venue in VENUES:
        venue_dir = PAPER / "venues" / venue
        assert (venue_dir / "STATUS.md").exists(), venue
        assert (venue_dir / "main.tex").exists(), venue
        assert (venue_dir / "preamble.tex").exists(), venue
        assert (venue_dir / ".latexmkrc").exists(), venue
        assert (venue_dir / "sections/README.md").exists(), venue
        assert (venue_dir / "rebuttal/README.md").exists(), venue

        status = read_text(venue_dir / "STATUS.md")
        for marker in (
            "Template provenance:",
            "Readiness:",
            "Local section overrides:",
            "Known missing checks:",
        ):
            assert marker in status, f"{venue}: {marker}"

        preamble = read_text(venue_dir / "preamble.tex")
        for snippet in (
            r"\def\input@path{{../../shared/}{./}}",
            r"\graphicspath{{../../shared/}{./}}",
            r"\input{../../shared/math_commands}",
            r"\input{../../shared/venue_macros}",
        ):
            assert snippet in preamble, f"{venue}: {snippet}"

        main = read_text(venue_dir / "main.tex")
        assert r"\input{preamble}" in main, venue
        assert "../../shared/sections/" in main, venue
        assert r"\bibliography{references}" in main, venue
        assert r"\bibliography{../../shared/references}" not in main, venue

        latexmkrc = read_text(venue_dir / ".latexmkrc")
        assert "abs_path('../../shared')" in latexmkrc, venue
        assert "BIBINPUTS" in latexmkrc, venue

    assert (PAPER / "venues/neurips/neurips_2026.sty").exists()


def test_makefile_and_paper_gitignore_contract() -> None:
    makefile = read_text(PAPER / "Makefile")
    for snippet in (
        "VENUES := accv arxiv eccv neurips",
        "template-check:",
        "check-template-accv:",
        "check-template-eccv:",
        "check-template-neurips:",
        "pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex",
        "bibtex build/main",
        "BIBINPUTS=",
        "Primary: accv",
    ):
        assert snippet in makefile, snippet

    gitignore = read_text(PAPER / ".gitignore")
    for pattern in (
        "venues/*/build/",
        "submissions/",
        "arxiv-submission/",
        "camera-ready/",
        "*.fdb_latexmk",
    ):
        assert pattern in gitignore, pattern

    readme = read_text(PAPER / "README.md")
    assert r"\bibliography{references}" in readme
    assert "ACCV primary" in readme


def test_active_docs_describe_multi_venue_workflow() -> None:
    combined = "\n".join(read_text(path) for path in ACTIVE_DOCS)
    for required in (
        "ACCV primary",
        "transfer-candidate",
        "make accv",
        "paper/",
    ):
        assert required in combined, required


def test_experiments_section_avoids_unsupported_superiority_claims() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")
    negation_markers = ("not a ", "not ", "do not ", "does not ", "no ")
    for forbidden in (
        "broad benchmark superiority",
        "full-simulation speedup",
        "safety certification",
        "whole-robot manipulation",
    ):
        for line in experiments.splitlines():
            lower = line.lower()
            if forbidden not in lower:
                continue
            if any(marker in lower for marker in negation_markers):
                continue
            assert False, forbidden
