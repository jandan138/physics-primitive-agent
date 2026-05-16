from pathlib import Path
import importlib.util
import re


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


def test_p_sequence_ids_skip_latex_control_slots():
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

    assert ids == ["method-p001", "method-p002"]


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


def test_generate_mdx_renders_display_math_blocks_as_equations():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [
            {
                "type": "latex_block",
                "id": "method-l001",
                "environment": "equation",
                "text": "\\begin{equation}\\label{eq:cost}\nC(p_0, p_1) = V(p_0 \\cap p_1)\n\\end{equation}",
            },
            {
                "type": "latex_block",
                "id": "method-l002",
                "environment": "align",
                "text": "\\begin{align}\na &= b \\\\\nc &= d\n\\end{align}",
            },
        ],
    }

    mdx = importer.render_section_mdx(section, {})

    assert 'import EquationBlock from "../../components/EquationBlock.astro";' in mdx
    assert '<EquationBlock id="method-l001"' in mdx
    assert '<EquationBlock id="method-l002"' in mdx
    assert 'label="Method / equation / method-l001"' in mdx
    assert 'latex={"\\\\begin{equation}\\\\label{eq:cost}\\nC(p_0, p_1) = V(p_0 \\\\cap p_1)\\n\\\\end{equation}"}' in mdx
    assert '<LatexBlock id="method-l001"' not in mdx
    assert "```latex" not in mdx


def test_generate_mdx_renders_figure_panel_for_graphic_blocks():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [
            {
                "type": "latex_block",
                "id": "method-l001",
                "environment": "figure",
                "text": "\\begin{figure}\n\\includegraphics{assets/example}\n\\end{figure}",
                "images": ["paper-assets/assets/example.jpg"],
            },
            {
                "type": "caption",
                "id": "method-p001",
                "text": "A source-paper figure.",
            },
        ],
    }

    mdx = importer.render_section_mdx(section, {"method-p001": "论文图。"})

    assert 'import FigurePanel from "../../components/FigurePanel.astro";' in mdx
    assert '<FigurePanel id="method-l001-figure"' in mdx
    assert 'images={["paper-assets/assets/example.jpg"]}' in mdx
    assert '<LatexBlock id="method-l001"' not in mdx


def test_extract_graphic_references_ignores_latex_comments():
    importer = _load_importer()
    text = (
        "\\begin{figure}\n"
        "% \\includegraphics{assets/commented}\n"
        "\\includegraphics[width=0.5\\linewidth]{assets/visible}\n"
        "\\end{figure}"
    )

    assert importer.extract_graphic_references(text) == ["assets/visible"]


def test_generate_mdx_omits_latex_control_from_reader_output():
    importer = _load_importer()
    section = {
        "slug": "method",
        "title": "Method",
        "blocks": [{"type": "latex_control", "id": "method-p002", "text": "\\setlength{\\intextsep}{0pt}"}],
    }

    mdx = importer.render_section_mdx(section, {})

    assert "\\setlength" not in mdx
    assert '<LatexBlock id="method-p002"' not in mdx
    assert "<PaperBlock" not in mdx


def test_clean_inline_latex_removes_reader_hostile_tokens():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"See Fig.~\ref{fig:maze} and \href{https://rapier.rs/}{\color{blue} Rapier}. "
        r"\ccby Authors. Values satisfy x \leq y and V_i \inR^3. A \& B ``quoted''."
    )

    assert (
        cleaned
        == 'See Fig. maze and Rapier. License: Authors. Values satisfy x <= y and V_i in R^3. A & B "quoted".'
    )


def test_clean_inline_latex_renders_direction_markers():
    importer = _load_importer()

    assert importer.clean_inline_latex(r"frame times$^\downarrow$") == "frame times ↓"
    assert importer.clean_inline_latex(r"帧时间$^\downarrow$") == "帧时间 ↓"


def test_clean_inline_latex_preserves_nested_inline_math_for_renderer():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"Given $\mathbb{M} = (V, F), \textbf{V$_i$} \in\mathrm{R}^3, "
        r"F_i \subseteq V, |F_i| \geq 3$ and $N\in\mathbb{Z}_+$."
    )

    assert r"\mathbb{M}" in cleaned
    assert r"\mathbf{V}_{i}" in cleaned
    assert r"\in\mathrm{R}^3" in cleaned
    assert r"\subseteq V" in cleaned
    assert r"N\in\mathbb{Z}_+" in cleaned
    assert "V$_i$" not in cleaned
    assert r"\textbf{V_i}" not in cleaned
    assert "NinZ_+" not in cleaned
    assert cleaned.count("$") == 4


def test_clean_inline_latex_normalizes_math_aliases_for_renderer():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"Use $N\inZ_+$, $(h_x, h_y \inR)$, $a^\topa = 1$, $p^\topx$, and $v_i^\topp$."
    )

    assert r"N\in\mathbb{Z}_+" in cleaned
    assert r"h_y \in\mathbb{R}" in cleaned
    assert r"a^\top a = 1" in cleaned
    assert r"p^\top x" in cleaned
    assert r"v_i^\top p" in cleaned
    assert r"\inR" not in cleaned
    assert r"\inZ" not in cleaned
    assert r"\topa" not in cleaned
    assert r"\topx" not in cleaned
    assert r"\topp" not in cleaned


def test_clean_inline_latex_normalizes_nested_subscript_dollars_inside_math():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(r"给定输入网格 $M = (V, F), V$_i$ \inR^3$.")

    assert r"$M = (V, F), V_i \in\mathbb{R}^3$" in cleaned
    assert "V$_i$" not in cleaned
    assert cleaned.count("$") == 2


def test_clean_inline_latex_keeps_math_commands_for_renderer():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"Distance is $\frac{\text{Hausdorff\slash Chamfer New $\rightarrow$ Input}}"
        r"{\lVert\text{Bounding Box Diag}\rVert_2}$ and runtime is O($n\log n$)."
    )

    assert r"\frac" in cleaned
    assert r"\lVert" in cleaned
    assert r"\text{Hausdorff/ Chamfer New → Input}" in cleaned
    assert r"n\log n" in cleaned
    assert re.search(r"(?<!\\)\bfrac\{", cleaned) is None
    assert re.search(r"(?<!\\)\blVert", cleaned) is None
    assert "$→$" not in cleaned


def test_clean_inline_latex_strips_unsupported_num_macro_inside_math():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"The half-extent is $h_i = \max(\frac{1}{2}(u_i - l_i), \num{1e-3})$."
    )

    assert r"\num" not in cleaned
    assert r"1e-3" in cleaned
    assert r"\frac" in cleaned


def test_clean_inline_latex_keeps_scientific_notation_compact_after_latex_commands():
    importer = _load_importer()

    cleaned = importer.clean_inline_latex(
        r"Thresholds are $\leq1e-4$ and $\textbf{6.95e-3}, 9.91e-3$."
    )

    assert r"\leq\text{1e-4}" in cleaned
    assert r"\textbf{6.95e-3}" in cleaned
    assert r"\text{9.91e-3}" in cleaned
    assert r"6.\text{95e-3}" not in cleaned


def test_parser_does_not_split_inline_bmatrix_from_paragraph():
    importer = _load_importer()

    blocks = importer.parse_latex_blocks(
        r"We use $Q = W\Lambda W^{-1}, \Lambda = \text{diag}("
        r"\begin{bmatrix}\lambda_2 & \lambda_1 & \lambda_0 \end{bmatrix})$ "
        "before continuing."
    )

    assert [block["type"] for block in blocks] == ["paragraph"]
    assert r"\begin{bmatrix}" in blocks[0]["text"]
    assert "before continuing" in blocks[0]["text"]


def test_imported_reader_text_has_no_known_broken_math_artifacts():
    importer = _load_importer()
    source = REPO_ROOT / "docs" / "tmp" / "papers" / "arXiv-2602.07369v1"
    translations = importer.load_translations(REPO_ROOT / "site" / "src" / "data" / "translations")
    sections = importer.import_sections(source)

    rendered_reader_strings = []
    for section in sections:
        for block in section["blocks"]:
            if not importer.is_translatable_block(block):
                continue
            rendered_reader_strings.append(importer.clean_inline_latex(str(block["text"])))
            rendered_reader_strings.append(
                importer.clean_inline_latex(translations.get(str(block["id"]), ""))
            )

    combined = "\n".join(rendered_reader_strings)
    broken_artifact_patterns = [
        r"NinZ_\+",
        r"(?<!\\)nn\^top",
        r"(?<!\\)Sigma pp\^top",
        r"(?<!\\)\bfrac\{",
        r"(?<!\\)\blVert",
        r"(?<!\\)\brVert",
        r"(?<!\\)nlog n",
        r"\$→\$",
        r"(?<!\\)WLambda",
        r"\\num",
        r"\\inR",
        r"\\inZ",
        r"\\top[A-Za-z]",
        r"\\textbf\{[^}]*_",
    ]
    for artifact_pattern in broken_artifact_patterns:
        assert re.search(artifact_pattern, combined) is None


def test_imported_experiment_translation_ids_stay_semantically_aligned():
    importer = _load_importer()
    source = REPO_ROOT / "docs" / "tmp" / "papers" / "arXiv-2602.07369v1"
    translations = importer.load_translations(REPO_ROOT / "site" / "src" / "data" / "translations")
    sections = importer.import_sections(source)
    experiments = next(section for section in sections if section["slug"] == "experiments")
    blocks_by_id = {
        str(block["id"]): block
        for block in experiments["blocks"]
        if importer.is_translatable_block(block)
    }

    assert "frame duration" in blocks_by_id["experiments-p017"]["text"]
    assert "帧耗时" in translations["experiments-p017"]
    assert "1.63" not in translations["experiments-p017"]
    assert "许可" not in translations["experiments-p017"]
    assert "maximum allowed volume" in blocks_by_id["experiments-p022"]["text"]
    assert "允许增加的最大体积" in translations["experiments-p022"]
    assert "Limiting Excess Volume:" in blocks_by_id["experiments-p023"]["text"]
    assert "限制额外体积" in translations["experiments-p023"]
    assert "Timing:" in blocks_by_id["experiments-p024"]["text"]
    assert "计时" in translations["experiments-p024"]
    assert "ablate" in blocks_by_id["experiments-p026"]["text"]
    assert "消融" in translations["experiments-p026"]
    assert "Coplanar Vertices" in blocks_by_id["experiments-p028"]["text"]
    assert "共面顶点" in translations["experiments-p028"]


def test_asset_resolver_handles_case_mismatch(tmp_path):
    importer = _load_importer()
    asset_root = tmp_path / "paper"
    asset_dir = asset_root / "assets"
    asset_dir.mkdir(parents=True)
    actual = asset_dir / "Dungeon_Level_coacd.jpg"
    actual.write_bytes(b"image")

    resolved = importer.resolve_asset_reference(asset_root, "assets/Dungeon_level_coacd")

    assert resolved == actual


def test_public_asset_paths_use_web_optimized_images():
    importer = _load_importer()
    source_root = REPO_ROOT / "docs/tmp/papers/arXiv-2602.07369v1"

    assert (
        importer.public_asset_path(source_root, source_root / "assets/example.jpg")
        == "paper-assets/assets/example.webp"
    )
    assert (
        importer.public_asset_path(source_root, source_root / "plots/example.pdf")
        == "paper-assets/plots/example.webp"
    )


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
