from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SECTION_RE = re.compile(r"^\\section(?:\{\\label\{[^}]+\}([^}]+)\}|\{([^}]+)\})")
SUBSECTION_RE = re.compile(r"^\\subsection\{([^}]+)\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.DOTALL)
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".pdf")
P_SEQUENCE_TYPES = {"paragraph", "caption", "latex_control"}

SECTION_TITLES = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "background": "Related Work",
    "method": "Method",
    "experiments": "Results And Ablations",
    "conclusion": "Discussion, Limitations, And Conclusion",
    "additional-results": "Additional Results",
}


def parse_latex_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    paragraph_lines: list[str] = []
    environment_lines: list[str] = []
    environment_stack: list[str] = []
    root_environment = ""

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        paragraph = clean_inline_latex(" ".join(paragraph_lines).strip())
        paragraph_lines.clear()
        if paragraph:
            blocks.append({"type": "paragraph", "text": paragraph})

    def flush_environment() -> None:
        nonlocal root_environment
        if not environment_lines:
            return
        environment_text = "\n".join(environment_lines).strip()
        blocks.append(
            {
                "type": "latex_block",
                "environment": root_environment,
                "text": environment_text,
            }
        )
        for caption in extract_captions(environment_text):
            blocks.append(
                {
                    "type": "caption",
                    "environment": root_environment,
                    "text": caption,
                }
            )
        environment_lines.clear()
        root_environment = ""

    def start_environment(line: str, begin_index: int) -> None:
        nonlocal root_environment
        flush_paragraph()
        environment_line = line[begin_index:].strip()
        environment_lines.append(environment_line)
        environment_stack.clear()
        root_environment = _update_environment_stack(environment_stack, environment_line) or ""
        if not environment_stack:
            flush_environment()

    for raw_line in text.splitlines():
        if environment_stack:
            environment_lines.append(raw_line.rstrip())
            _update_environment_stack(environment_stack, raw_line)
            if not environment_stack:
                flush_environment()
            continue

        line = strip_latex_comment(raw_line).strip()
        if not line or line.startswith("%"):
            flush_paragraph()
            continue
        section_match = SECTION_RE.match(line)
        subsection_match = SUBSECTION_RE.match(line)
        if section_match:
            flush_paragraph()
            title = section_match.group(1) or section_match.group(2) or ""
            blocks.append({"type": "section", "title": clean_inline_latex(title)})
            continue
        if subsection_match:
            flush_paragraph()
            blocks.append(
                {"type": "subsection", "title": clean_inline_latex(subsection_match.group(1))}
            )
            continue
        begin_match = BEGIN_RE.search(line)
        if begin_match:
            prefix = line[: begin_match.start()].strip()
            if prefix:
                if _looks_like_latex_control(prefix):
                    blocks.append({"type": "latex_control", "text": prefix})
                else:
                    paragraph_lines.append(prefix)
            start_environment(line, begin_match.start())
            continue
        if line in {"{", "}"}:
            if paragraph_lines:
                paragraph_lines.append(line)
            else:
                blocks.append({"type": "latex_control", "text": line})
            continue
        if _is_standalone_latex_control(line):
            flush_paragraph()
            blocks.append({"type": "latex_control", "text": line})
            continue
        paragraph_lines.append(line)

    flush_paragraph()
    if environment_lines:
        flush_environment()
    return blocks


def clean_inline_latex(value: str) -> str:
    value = value.replace("~", " ")
    value = re.sub(r"\\paragraph\*?\{([^}]+)\}", r"\1:", value)
    value = re.sub(r"\\label\{[^}]+\}", "", value)
    value = re.sub(r"\\(?:short)?cite\{([^}]+)\}", r"[\1]", value)
    value = re.sub(r"\\ref\{([^}]+)\}", r"ref:\1", value)
    value = re.sub(r"\\(?:emph|texttt|textbf|textit|mathrm|mathbf|mathbb)\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\num\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\vect\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\(?:ccby|ccbync|cczero)\s*([^.]*)", r"License: \1", value)
    value = value.replace("\\slash", "/")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def strip_latex_comment(value: str) -> str:
    escaped = False
    for index, char in enumerate(value):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return value[:index]
        escaped = False
    return value


def extract_captions(environment_text: str) -> list[str]:
    captions: list[str] = []
    index = 0
    while True:
        match = re.search(r"\\caption\*?\{", environment_text[index:])
        if not match:
            return captions
        start = index + match.end() - 1
        caption, end = _read_balanced_braces(environment_text, start)
        if caption:
            captions.append(clean_inline_latex(" ".join(caption.splitlines())))
        index = end


def _read_balanced_braces(text: str, open_brace_index: int) -> tuple[str, int]:
    if open_brace_index >= len(text) or text[open_brace_index] != "{":
        return "", open_brace_index
    depth = 0
    content: list[str] = []
    index = open_brace_index
    while index < len(text):
        char = text[index]
        if char == "{":
            depth += 1
            if depth > 1:
                content.append(char)
        elif char == "}":
            depth -= 1
            if depth == 0:
                return "".join(content).strip(), index + 1
            content.append(char)
        else:
            content.append(char)
        index += 1
    return "".join(content).strip(), index


def _update_environment_stack(environment_stack: list[str], line: str) -> str | None:
    first_environment = None
    matches: list[tuple[int, str, str]] = []
    matches.extend((match.start(), "begin", match.group(1)) for match in BEGIN_RE.finditer(line))
    matches.extend((match.start(), "end", match.group(1)) for match in END_RE.finditer(line))
    for _, kind, environment in sorted(matches):
        if kind == "begin":
            if first_environment is None:
                first_environment = environment
            environment_stack.append(environment)
        elif environment_stack:
            if environment_stack[-1] == environment:
                environment_stack.pop()
            elif environment in environment_stack:
                del environment_stack[environment_stack.index(environment) :]
    return first_environment


def paragraph_ids(section: dict[str, object]) -> list[str]:
    slug = str(section["slug"])
    blocks = section["blocks"]
    if not isinstance(blocks, list):
        raise ValueError("section blocks must be a list")
    count = sum(1 for block in blocks if is_p_sequence_block(block))
    return [f"{slug}-p{index:03d}" for index in range(1, count + 1)]


def latex_block_ids(section: dict[str, object]) -> list[str]:
    slug = str(section["slug"])
    blocks = section["blocks"]
    if not isinstance(blocks, list):
        raise ValueError("section blocks must be a list")
    count = sum(1 for block in blocks if isinstance(block, dict) and block.get("type") == "latex_block")
    return [f"{slug}-l{index:03d}" for index in range(1, count + 1)]


def is_translatable_block(block: object) -> bool:
    return isinstance(block, dict) and block.get("type") in {"paragraph", "caption"}


def is_p_sequence_block(block: object) -> bool:
    return isinstance(block, dict) and block.get("type") in P_SEQUENCE_TYPES


def render_section_mdx(section: dict[str, object], translations: dict[str, str]) -> str:
    lines = [
        "---",
        f'title: "{escape_frontmatter(str(section["title"]))}"',
        f'slug: "{section["slug"]}"',
        "---",
        'import PaperBlock from "../../components/PaperBlock.astro";',
        'import LatexBlock from "../../components/LatexBlock.astro";',
        "",
        f"# {section['title']}",
        "",
    ]
    for block in section["blocks"]:  # type: ignore[index]
        if is_translatable_block(block):
            paragraph_id = str(block["id"])
            block_kind = "caption" if block["type"] == "caption" else "paragraph"
            lines.extend(
                [
                    "<PaperBlock",
                    f'  id="{paragraph_id}"',
                    f'  section="{escape_attr(str(section["title"]))}"',
                    f'  original="{escape_attr(str(block["text"]))}"',
                    f'  translation="{escape_attr(translations.get(paragraph_id, ""))}"',
                    '  translationStatus="draft_ai_assisted"',
                    f'  explanationStatus="{block_kind}"',
                    '  reproductionStatus="not_started"',
                    '  sourceNamespace="cpd_paper_source_text"',
                    '  translationProvenance="codex_draft_2026-05-15"',
                    "/>",
                    "",
                ]
            )
        elif block["type"] in {"section", "subsection"}:
            heading = "##" if block["type"] == "section" else "###"
            lines.extend([f'{heading} {block["title"]}', ""])
        elif block["type"] == "latex_block":
            latex_id = str(block["id"])
            label = escape_attr(f'{section["title"]} / {block.get("environment", "latex")} / {latex_id}')
            lines.extend(
                [
                    f'<LatexBlock id="{latex_id}" label="{label}">',
                    "",
                    "```latex",
                    str(block["text"]),
                    "```",
                    "",
                    "</LatexBlock>",
                    "",
                ]
            )
        elif block["type"] == "latex_control":
            latex_id = str(block["id"])
            label = escape_attr(f'{section["title"]} / control / {latex_id}')
            lines.extend(
                [
                    f'<LatexBlock id="{latex_id}" label="{label}">',
                    "",
                    "```latex",
                    str(block["text"]),
                    "```",
                    "",
                    "</LatexBlock>",
                    "",
                ]
            )
        else:
            lines.extend(["```latex", str(block["text"]), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def load_translations(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    if path.is_dir():
        translations: dict[str, str] = {}
        for translation_file in sorted(path.glob("*.json")):
            loaded = json.loads(translation_file.read_text(encoding="utf-8"))
            overlap = sorted(set(translations).intersection(loaded))
            if overlap:
                raise ValueError(
                    f"duplicate translation ids in {translation_file}: {', '.join(overlap)}"
                )
            translations.update(loaded)
        return translations
    return {}


def missing_translation_ids(
    sections: list[dict[str, object]], translations: dict[str, str]
) -> list[str]:
    missing: list[str] = []
    for section in sections:
        for block in section["blocks"]:  # type: ignore[index]
            if is_translatable_block(block) and not translations.get(str(block["id"]), "").strip():
                missing.append(str(block["id"]))
    return missing


def expected_translation_ids(sections: list[dict[str, object]]) -> set[str]:
    expected: set[str] = set()
    for section in sections:
        for block in section["blocks"]:  # type: ignore[index]
            if is_translatable_block(block):
                expected.add(str(block["id"]))
    return expected


def extra_translation_ids(
    sections: list[dict[str, object]], translations: dict[str, str]
) -> list[str]:
    expected = expected_translation_ids(sections)
    return sorted(set(translations).difference(expected))


def resolve_asset_reference(source_root: Path, reference: str) -> Path | None:
    raw = source_root / reference
    candidates = [raw] if raw.suffix else [raw.with_suffix(ext) for ext in IMAGE_EXTENSIONS]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    lower_reference = reference.lower()
    if not Path(lower_reference).suffix:
        lower_targets = {f"{lower_reference}{ext}" for ext in IMAGE_EXTENSIONS}
    else:
        lower_targets = {lower_reference}
    for path in source_root.rglob("*"):
        if path.is_file() and path.relative_to(source_root).as_posix().lower() in lower_targets:
            return path
    return None


def extract_abstract(text: str) -> str:
    match = ABSTRACT_RE.search(text)
    if not match:
        return ""
    return clean_inline_latex(" ".join(line.strip() for line in match.group(1).splitlines()))


def section_slug_for_file(filename: str) -> str:
    return Path(filename).stem.replace("_", "-")


def section_title_for_slug(slug: str) -> str:
    return SECTION_TITLES.get(slug, slug.replace("-", " ").title())


def escape_attr(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def escape_frontmatter(value: str) -> str:
    return value.replace('"', '\\"')


def _section_from_file(source_file: Path) -> dict[str, object]:
    slug = section_slug_for_file(source_file.name)
    blocks = parse_latex_blocks(source_file.read_text(encoding="utf-8"))
    section: dict[str, object] = {
        "slug": slug,
        "title": section_title_for_slug(slug),
        "blocks": blocks,
    }
    ids = iter(paragraph_ids(section))
    latex_ids = iter(latex_block_ids(section))
    for block in blocks:
        if is_p_sequence_block(block):
            block["id"] = next(ids)
        elif block["type"] == "latex_block":
            block["id"] = next(latex_ids)
    return section


def _is_standalone_latex_control(line: str) -> bool:
    if _looks_like_latex_control(line):
        return True
    return line.startswith("{") and "\\setlength" in line


def _looks_like_latex_control(value: str) -> bool:
    stripped = value.strip()
    if re.fullmatch(r"[A-ZW]\s*=", stripped):
        return True
    return stripped.startswith(
        (
            "\\appendix",
            "\\newpage",
            "\\vfill",
            "\\setlength",
            "\\renewcommand",
            "\\centering",
            "\\scriptsize",
            "\\small",
            "\\footnotesize",
        )
    )


def _abstract_section_from_main(main_file: Path) -> dict[str, object]:
    abstract = extract_abstract(main_file.read_text(encoding="utf-8"))
    section: dict[str, object] = {
        "slug": "abstract",
        "title": "Abstract",
        "blocks": [{"type": "paragraph", "text": abstract}],
    }
    section["blocks"][0]["id"] = "abstract-p001"  # type: ignore[index]
    return section


def _section_files_from_main(source_root: Path) -> list[Path]:
    main_file = source_root / "main.tex"
    if not main_file.exists():
        return sorted(path for path in source_root.glob("*.tex") if path.name != "main.tex")
    section_files: list[Path] = []
    for match in INPUT_RE.finditer(main_file.read_text(encoding="utf-8")):
        candidate = source_root / f"{match.group(1)}.tex"
        if candidate.exists():
            section_files.append(candidate)
    return section_files


def import_sections(source_root: Path) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    main_file = source_root / "main.tex"
    if main_file.exists():
        sections.append(_abstract_section_from_main(main_file))
    sections.extend(_section_from_file(path) for path in _section_files_from_main(source_root))
    return sections


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import CPD paper LaTeX into MDX scaffolds.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--translations", type=Path)
    args = parser.parse_args(argv)

    translations = load_translations(args.translations)
    sections = import_sections(args.source)
    missing = missing_translation_ids(sections, translations)
    if missing:
        preview = ", ".join(missing[:12])
        suffix = "" if len(missing) <= 12 else f", ... ({len(missing)} total)"
        raise SystemExit(f"missing translations: {preview}{suffix}")
    extra = extra_translation_ids(sections, translations)
    if extra:
        preview = ", ".join(extra[:12])
        suffix = "" if len(extra) <= 12 else f", ... ({len(extra)} total)"
        raise SystemExit(f"extra translations: {preview}{suffix}")

    args.output.mkdir(parents=True, exist_ok=True)
    for section in sections:
        mdx = render_section_mdx(section, translations)
        (args.output / f"{section['slug']}.mdx").write_text(mdx, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
