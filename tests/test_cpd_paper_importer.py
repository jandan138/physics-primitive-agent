from pathlib import Path
import importlib.util


REPO_ROOT = Path(__file__).resolve().parents[1]
IMPORTER_PATH = REPO_ROOT / "site" / "scripts" / "import_cpd_paper.py"


def _load_importer():
    spec = importlib.util.spec_from_file_location("import_cpd_paper", IMPORTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_extract_section_commands_from_latex():
    importer = _load_importer()
    blocks = importer.parse_latex_blocks(
        "\\section{Method}\nFirst paragraph.\n\nSecond paragraph."
    )

    assert [block["type"] for block in blocks] == ["section", "paragraph", "paragraph"]
    assert blocks[0]["title"] == "Method"
    assert blocks[1]["text"] == "First paragraph."


def test_parser_preserves_environment_and_extracts_caption():
    importer = _load_importer()
    blocks = importer.parse_latex_blocks(
        "\\begin{figure}\n"
        "\\includegraphics{assets/example}\n"
        "\\caption{A source-paper result.}\n"
        "\\end{figure}\n"
        "\n"
        "Next paragraph."
    )

    assert [block["type"] for block in blocks] == ["latex_block", "caption", "paragraph"]
    assert blocks[0]["environment"] == "figure"
    assert "\\includegraphics{assets/example}" in blocks[0]["text"]
    assert blocks[1]["text"] == "A source-paper result."
    assert blocks[2]["text"] == "Next paragraph."


def test_parser_splits_inline_equation_environment():
    importer = _load_importer()
    blocks = importer.parse_latex_blocks(
        "We solve: \\begin{equation}\n"
        "x = y\n"
        "\\end{equation}\n"
        "Then continue."
    )

    assert [block["type"] for block in blocks] == ["paragraph", "latex_block", "paragraph"]
    assert blocks[0]["text"] == "We solve:"
    assert blocks[1]["environment"] == "equation"
    assert blocks[2]["text"] == "Then continue."


def test_parser_preserves_standalone_latex_controls_without_translation():
    importer = _load_importer()
    blocks = importer.parse_latex_blocks("\\appendix\n\n\\newpage\n\nBody paragraph.")

    assert [block["type"] for block in blocks] == ["latex_control", "latex_control", "paragraph"]
    assert blocks[0]["text"] == "\\appendix"
    assert blocks[1]["text"] == "\\newpage"


def test_p_sequence_ids_reserve_latex_control_slots():
    importer = _load_importer()
    section = {
        "slug": "method",
        "blocks": [
            {"type": "paragraph"},
            {"type": "latex_control"},
            {"type": "caption"},
        ],
    }

    ids = importer.paragraph_ids(section)

    assert ids == ["method-p001", "method-p002", "method-p003"]


def test_stable_paragraph_ids_are_slugged_by_section():
    importer = _load_importer()
    section = {"slug": "method", "blocks": [{"type": "paragraph"}, {"type": "paragraph"}]}

    ids = importer.paragraph_ids(section)

    assert ids == ["method-p001", "method-p002"]


def test_generate_mdx_uses_draft_translation_status():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [{"type": "paragraph", "id": "method-p001", "text": "A primitive is fitted."}],
    }
    translations = {"method-p001": "拟合一个基本体。"}

    mdx = importer.render_section_mdx(section, translations)

    assert 'translationStatus="draft_ai_assisted"' in mdx
    assert 'sourceNamespace="cpd_paper_source_text"' in mdx
    assert 'translationProvenance="codex_draft_2026-05-15"' in mdx
    assert 'reproductionStatus="not_started"' in mdx
    assert 'original="A primitive is fitted."' in mdx
    assert 'translation="拟合一个基本体。"' in mdx


def test_generate_mdx_renders_latex_blocks_with_gate_copy():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [
            {
                "type": "latex_block",
                "id": "method-l001",
                "environment": "algorithm",
                "text": "\\begin{algorithm}\n\\end{algorithm}",
            }
        ],
    }

    mdx = importer.render_section_mdx(section, {})

    assert 'import LatexBlock from "../../components/LatexBlock.astro";' in mdx
    assert '<LatexBlock id="method-l001"' in mdx
    assert "```latex" in mdx


def test_generate_mdx_renders_latex_control_without_paper_block():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [{"type": "latex_control", "id": "method-p002", "text": "\\setlength{\\intextsep}{0pt}"}],
    }

    mdx = importer.render_section_mdx(section, {})

    assert '<LatexBlock id="method-p002"' in mdx
    assert "<PaperBlock" not in mdx


def test_asset_resolver_handles_case_mismatch(tmp_path):
    importer = _load_importer()
    asset_root = tmp_path / "paper"
    asset_dir = asset_root / "assets"
    asset_dir.mkdir(parents=True)
    actual = asset_dir / "Dungeon_Level_coacd.jpg"
    actual.write_bytes(b"image")

    resolved = importer.resolve_asset_reference(asset_root, "assets/Dungeon_level_coacd")

    assert resolved == actual


def test_extract_main_tex_abstract():
    importer = _load_importer()
    text = "\\begin{abstract}\nCreation of collision objects.\n\\end{abstract}"

    assert importer.extract_abstract(text) == "Creation of collision objects."


def test_known_section_mapping():
    importer = _load_importer()

    assert importer.section_slug_for_file("background.tex") == "background"
    assert importer.section_title_for_slug("background") == "Related Work"
    assert importer.section_slug_for_file("additional_results.tex") == "additional-results"


def test_import_sections_includes_abstract_first(tmp_path):
    importer = _load_importer()
    source = tmp_path / "paper"
    source.mkdir()
    (source / "main.tex").write_text(
        "\\begin{abstract}\nAbstract body.\n\\end{abstract}\n\\input{introduction}",
        encoding="utf-8",
    )
    (source / "introduction.tex").write_text("\\section{Introduction}\nIntro body.", encoding="utf-8")

    sections = importer.import_sections(source)

    assert [section["slug"] for section in sections] == ["abstract", "introduction"]
    assert sections[0]["blocks"][0]["id"] == "abstract-p001"


def test_load_translations_from_directory(tmp_path):
    importer = _load_importer()
    translations = tmp_path / "translations"
    translations.mkdir()
    (translations / "a.json").write_text('{"abstract-p001": "摘要"}', encoding="utf-8")
    (translations / "b.json").write_text('{"method-p001": "方法"}', encoding="utf-8")

    loaded = importer.load_translations(translations)

    assert loaded == {"abstract-p001": "摘要", "method-p001": "方法"}


def test_missing_translation_ids_detects_empty_translations():
    importer = _load_importer()
    sections = [
        {
            "slug": "method",
            "blocks": [
                {"type": "paragraph", "id": "method-p001", "text": "A"},
                {"type": "caption", "id": "method-p002", "text": "B"},
                {"type": "latex_block", "id": "method-l001", "text": "C"},
            ],
        }
    ]

    missing = importer.missing_translation_ids(sections, {"method-p001": "译文"})

    assert missing == ["method-p002"]


def test_extra_translation_ids_rejects_unconsumed_translation_keys():
    importer = _load_importer()
    sections = [
        {
            "slug": "method",
            "blocks": [
                {"type": "paragraph", "id": "method-p001", "text": "A"},
                {"type": "latex_control", "id": "method-p002", "text": "\\appendix"},
            ],
        }
    ]

    extra = importer.extra_translation_ids(
        sections,
        {"method-p001": "译文", "method-p002": "不应消费"},
    )

    assert extra == ["method-p002"]
