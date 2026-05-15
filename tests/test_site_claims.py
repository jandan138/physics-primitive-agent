from scripts.validate_site_claims import validate_site_text


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


def test_site_validator_rejects_empty_generated_translation():
    issues = validate_site_text(
        "site/src/content/paper/method.mdx",
        '<PaperBlock sourceNamespace="cpd_paper_source_text" translation="" />',
    )

    assert any("empty draft translation is not allowed" in issue for issue in issues)
