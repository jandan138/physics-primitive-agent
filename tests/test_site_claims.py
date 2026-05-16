from pathlib import Path

from scripts.validate_site_claims import validate_site, validate_site_text


def test_site_validator_requires_source_namespace_banner():
    issues = validate_site_text("site/src/pages/paper/example.astro", "<main>No banner</main>")

    assert any("missing source namespace banner" in issue for issue in issues)


def test_site_validator_allows_source_paper_benchmark_claim_when_namespaced():
    text = """
    The English paper text and translated text describe the CPD paper.
    <PaperBlock sourceNamespace="cpd_paper_source_text" original="The paper reports improved performance." />
    """

    assert validate_site_text("site/src/content/paper/method.mdx", text) == []


def test_site_validator_rejects_paper_block_without_source_namespace():
    text = """
    <PaperBlock original="The paper reports improved performance." />
    """

    issues = validate_site_text("site/src/content/paper/method.mdx", text)

    assert any("PaperBlock missing cpd_paper_source_text namespace" in issue for issue in issues)


def test_site_validator_rejects_root_relative_paper_links():
    issues = validate_site_text("site/src/pages/paper/index.astro", '<a href="/paper/abstract/">')

    assert any("hardcoded root-relative paper href" in issue for issue in issues)


def test_site_validator_rejects_hardcoded_github_pages_base():
    issues = validate_site_text(
        "site/src/content/paper/introduction.mdx",
        'images={["/physics-primitive-agent/paper-assets/example.jpg"]}',
    )

    assert any("hardcoded GitHub Pages base path" in issue for issue in issues)


def test_site_validator_rejects_authorized_wording_without_permission_record():
    issues = validate_site_text(
        "site/src/pages/paper/index.astro",
        "<p>Authorized bilingual companion</p>",
    )

    assert any("permission wording must stay record-pending" in issue for issue in issues)


def test_site_validator_rejects_partial_reproduction_without_record():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<PaperBlock sourceNamespace="cpd_paper_source_text" reproductionStatus="partial" />',
    )

    assert any("reproduction status 'partial' requires a dated reproduction record" in issue for issue in issues)


def test_site_validator_rejects_published_paper_assets_without_permission_record():
    issues = validate_site_text(
        "site/src/content/paper/introduction.mdx",
        'images={["paper-assets/example.jpg"]}',
    )

    assert any("paper asset publication requires attached permission evidence" in issue for issue in issues)


def test_site_validator_ignores_placeholder_permission_record_for_paper_assets(tmp_path):
    content_root = tmp_path / "site/src/content/paper"
    content_root.mkdir(parents=True)
    (content_root / "introduction.mdx").write_text(
        'images={["paper-assets/example.jpg"]}',
        encoding="utf-8",
    )
    record_root = tmp_path / "docs/records"
    record_root.mkdir(parents=True)
    (record_root / "2026-05-15-cpd-paper-permission-placeholder.md").write_text(
        "This record is not the formal authorization artifact.",
        encoding="utf-8",
    )

    issues = validate_site(tmp_path)

    assert any("paper asset publication requires attached permission evidence" in issue for issue in issues)


def test_site_validator_accepts_user_asserted_permission_record_for_paper_assets(tmp_path):
    content_root = tmp_path / "site/src/content/paper"
    content_root.mkdir(parents=True)
    (content_root / "introduction.mdx").write_text(
        'images={["paper-assets/example.jpg"]}',
        encoding="utf-8",
    )
    record_root = tmp_path / "docs/records"
    record_root.mkdir(parents=True)
    (record_root / "2026-05-15-cpd-paper-permission-assertion.md").write_text(
        "source-paper figures based on the user's assertion that permission has been granted",
        encoding="utf-8",
    )

    assert validate_site(tmp_path) == []


def test_site_validator_rejects_empty_generated_translation():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<PaperBlock sourceNamespace="cpd_paper_source_text" translation="" />',
    )

    assert any("empty draft translation is not allowed" in issue for issue in issues)


def test_site_validator_rejects_stale_publication_waiting_copy():
    issues = validate_site_text(
        "site/src/pages/paper/index.astro",
        "Public full-text expansion should wait for the private permission record.",
    )

    assert any("stale publication gating copy" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_latex_controls():
    issues = validate_site_text(
        "site/src/content/paper/additional-results.mdx",
        '<LatexBlock id="additional-results-p001" label="Additional Results / control / additional-results-p001">',
    )

    assert any("reader-visible LaTeX control" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_latex_blocks():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<LatexBlock id="method-l001" label="Method / algorithm / method-l001">',
    )

    assert any("reader-visible LaTeX source block" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_internal_paper_labels():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<FigurePanel id="method-l002-figure" title="Method / figure / method-l002" />',
    )

    assert any("reader-visible internal paper block label" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_generic_equation_labels():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<EquationBlock id="method-l005" label="Display equation" />',
    )

    assert any("reader-visible generic equation label" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_generic_figure_labels():
    issues = validate_site_text(
        "site/src/content/paper/experiments.mdx",
        '<FigurePanel id="experiments-l006-figure" title="Figure" />',
    )

    assert any("reader-visible generic figure label" in issue for issue in issues)


def test_site_validator_rejects_reader_visible_placeholder_figure_captions():
    issues = validate_site_text(
        "site/src/content/paper/experiments.mdx",
        '<FigurePanel id="experiments-l006-figure" caption="Source-paper figure." />',
    )

    assert any("reader-visible placeholder figure caption" in issue for issue in issues)


def test_site_validator_rejects_unresolved_paper_reference_tokens():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<PaperBlock original="We ablate Eq. exact-cost in Fig. ablate-isect." />',
    )

    assert any("unresolved paper reference token" in issue for issue in issues)


def test_generated_paper_blocks_do_not_expose_raw_ref_tokens():
    content_root = Path(__file__).resolve().parents[1] / "site/src/content/paper"
    leaked = [
        path.name
        for path in sorted(content_root.glob("*.mdx"))
        if "ref:" in path.read_text(encoding="utf-8")
    ]

    assert leaked == []


def test_section_route_passes_nonempty_description_to_layout():
    route = Path(__file__).resolve().parents[1] / "site/src/pages/paper/[slug].astro"
    text = route.read_text(encoding="utf-8")

    assert "description=" in text
    assert "content.description" in text


def test_fraction_math_stays_inline_on_mobile():
    layout = Path(__file__).resolve().parents[1] / "site/src/layouts/PaperLayout.astro"
    text = layout.read_text(encoding="utf-8")

    assert "math-display" not in text
    assert "math-fraction" in text
    assert ".algorithm-block math" in text
    assert "paper-block__original" in text


def test_paper_block_keeps_internal_review_metadata_out_of_reader_chrome():
    component = Path(__file__).resolve().parents[1] / "site/src/components/PaperBlock.astro"
    text = component.read_text(encoding="utf-8")

    assert "section?: string" not in text
    assert "paper-block__badges" not in text
    assert "{section ? `${section} / ` : \"\"}{id}" not in text
    assert "Draft translation provenance" not in text


def test_paper_reader_css_drops_internal_review_chrome_styles():
    css = Path(__file__).resolve().parents[1] / "site/src/styles/paper.css"
    text = css.read_text(encoding="utf-8")

    assert ".paper-block__meta" not in text
    assert ".paper-block__anchor" not in text
    assert ".paper-block__badges" not in text
    assert ".paper-block__status" not in text
    assert ".status-badge" not in text


def test_figure_panel_separates_plots_from_thumbnail_grid():
    component = Path(__file__).resolve().parents[1] / "site/src/components/FigurePanel.astro"
    text = component.read_text(encoding="utf-8")

    assert "visualImages" in text
    assert "insetImages" in text
    assert "plotImages" in text
    assert "figure-panel__media" in text
    assert "figure-panel__insets" in text
    assert "figure-panel__plots" in text


def test_figure_panel_grid_has_breathing_room_without_page_scroll():
    stylesheet = Path(__file__).resolve().parents[1] / "site/src/styles/paper.css"
    text = stylesheet.read_text(encoding="utf-8")

    assert "minmax(220px, 1fr)" in text
    assert "gap: 18px" in text
    assert "overflow-x: visible" in text
