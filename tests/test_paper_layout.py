import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
VENUES = ("accv", "arxiv", "eccv", "neurips")
ACTIVE_DOCS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
)
ACCV_MAIN_SECTIONS = (
    "abstract.tex",
    "intro.tex",
    "related.tex",
    "background.tex",
    "method.tex",
    "experiments.tex",
    "discussion.tex",
    "conclusion.tex",
)
NON_PAPER_REFERENCE_KEYS = {
    "ericson2004",
    "newton2026",
    "openusd2026",
    "vhacd",
    "warp2022",
}
MIN_ACCV_MAIN_PAPER_REFERENCES = 30
CITATION_RE = re.compile(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\]){0,2}\{([^}]+)\}")
BIB_ENTRY_RE = re.compile(r"^@(?P<entry_type>\w+)\{(?P<key>[^,]+),", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def citation_keys(tex: str) -> set[str]:
    keys: set[str] = set()
    for match in CITATION_RE.finditer(tex):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def bibliography_keys() -> set[str]:
    references = read_text(PAPER / "shared/references.bib")
    return {match.group("key") for match in BIB_ENTRY_RE.finditer(references)}


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


def test_accv_related_work_uses_scoped_literature_themes() -> None:
    related = read_text(PAPER / "shared/sections/related.tex")
    for heading in (
        "Collision queries and proxy data structures",
        "Primitive and convex collision proxies",
        "Physics-engine validation and robot simulators",
        "Robot collision authoring",
    ):
        assert heading in related


def test_accv_main_cites_at_least_thirty_paper_references() -> None:
    bib_keys = bibliography_keys()
    main_citations: set[str] = set()
    for section in ACCV_MAIN_SECTIONS:
        main_citations.update(citation_keys(read_text(PAPER / "shared/sections" / section)))

    assert main_citations <= bib_keys

    paper_citations = main_citations - NON_PAPER_REFERENCE_KEYS
    assert len(paper_citations) >= MIN_ACCV_MAIN_PAPER_REFERENCES


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


def test_accv_status_and_main_pdf_boundary_are_current() -> None:
    status = read_text(PAPER / "venues/accv/STATUS.md")
    main = read_text(PAPER / "venues/accv/main.tex")
    experiments = read_text(PAPER / "shared/sections/experiments.tex")

    assert "at 7 pages" not in status
    assert "13 main-content pages" in status
    assert "reference-only page" in status
    assert r"\raggedbottom" in main
    assert r"\setlength{\@fptop}{0pt}" in main
    assert r"\input{../../shared/sections/appendix}" not in main
    assert r"\bibliography{references}" in main
    assert experiments.count(r"\label{tab:phase0-failure-labels}") == 1


def test_accv_main_avoids_forced_experiment_table_floats() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")

    assert r"\begin{table}[H]" not in experiments
    assert experiments.count(r"\begin{table}[tbp]") >= 1
    assert r"\begin{table}[!htbp]" in experiments
    assert r"\renewcommand{\arraystretch}{0.92}" in experiments


def test_accv_main_keeps_experiment_float_groups_bounded() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")

    for marker in (
        r"\subsection{Collision-probe scene renderings}",
        r"\subsection{Failure labels and measured symptoms}",
        r"\subsection{Franka articulation smoke}",
    ):
        before_marker = experiments.split(marker, 1)[0].rstrip()
        assert before_marker.endswith(r"\FloatBarrier"), marker


def test_shared_float_barriers_are_available_in_all_venues() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")

    assert r"\FloatBarrier" in experiments
    for venue in VENUES:
        preamble = read_text(PAPER / "venues" / venue / "preamble.tex")
        assert r"\usepackage{placeins}" in preamble, venue


def test_shared_listing_macros_are_available_in_all_venues() -> None:
    venue_macros = read_text(PAPER / "shared/venue_macros.tex")

    assert r"\lstdefinelanguage" in venue_macros
    for venue in VENUES:
        preamble = read_text(PAPER / "venues" / venue / "preamble.tex")
        assert r"\usepackage{listings}" in preamble, venue


def test_shared_table_column_macros_are_available_in_all_venues() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")

    assert r"\arraybackslash" in experiments
    for venue in VENUES:
        preamble = read_text(PAPER / "venues" / venue / "preamble.tex")
        assert r"\usepackage{array}" in preamble, venue


def test_accv_main_keeps_outcome_matrix_with_its_explanatory_text() -> None:
    experiments = read_text(PAPER / "shared/sections/experiments.tex")
    before_label = experiments.split(r"\label{fig:phase0-outcome-matrix}", 1)[0]
    begin_index = before_label.rfind(r"\begin{figure}")
    outcome_matrix = re.search(
        r"\\begin\{figure\}\[(?P<placement>[^\]]+)\]",
        before_label[begin_index:],
    )

    assert outcome_matrix is not None
    assert outcome_matrix.group("placement") == "H"
