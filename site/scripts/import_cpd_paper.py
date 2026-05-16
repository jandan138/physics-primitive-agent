from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

SECTION_RE = re.compile(r"^\\section(?:\{\\label\{[^}]+\}([^}]+)\}|\{([^}]+)\})")
SUBSECTION_RE = re.compile(r"^\\subsection\{([^}]+)\}")
ABSTRACT_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.DOTALL)
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".pdf")
WEB_IMAGE_EXTENSION = ".webp"
WEB_IMAGE_MAX_DIMENSION = 1600
WEB_IMAGE_QUALITY = 78
PDF_RASTER_DPI = 240
P_SEQUENCE_TYPES = {"paragraph", "caption"}
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
DISPLAY_MATH_ENVIRONMENTS = {"equation", "equation*", "align", "align*"}
ALGORITHM_ENVIRONMENTS = {"algorithm", "algorithm*"}
TABLE_ENVIRONMENTS = {"table", "table*"}

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
        captions = extract_captions(environment_text)
        latex_block = {
            "type": "latex_block",
            "environment": root_environment,
            "text": environment_text,
        }
        if captions:
            latex_block["caption"] = " ".join(captions)
        blocks.append(latex_block)
        for caption in captions:
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
        begin_match = None
        if not _has_open_inline_math(" ".join(paragraph_lines)):
            begin_match = _find_display_environment_begin(line)
        if begin_match is not None:
            prefix = line[:begin_match].strip()
            if prefix:
                if _looks_like_latex_control(prefix):
                    blocks.append({"type": "latex_control", "text": prefix})
                else:
                    paragraph_lines.append(prefix)
            start_environment(line, begin_match)
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
    value = _replace_href_commands(value)
    value = re.sub(r"\$?\^\s*\\?downarrow\$?", " ↓", value)
    value = re.sub(r"\$?\^\s*\\?uparrow\$?", " ↑", value)
    value = _remove_nested_script_math_markers(value)
    cleaned_parts: list[str] = []
    for kind, part in _split_inline_math(value):
        if kind == "math":
            cleaned_parts.append(f"${_clean_inline_math_latex(part)}$")
        else:
            cleaned_parts.append(_clean_plain_latex(part))
    value = "".join(cleaned_parts)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _remove_nested_script_math_markers(value: str) -> str:
    value = re.sub(r"(?<=[A-Za-z0-9}])\$_([^$]+)\$", r"_\1", value)
    value = re.sub(r"(?<=[A-Za-z0-9}])\$\^([^$]+)\$", r"^\1", value)
    return value


def _clean_plain_latex(value: str) -> str:
    value = re.sub(r"\\paragraph\*?\{([^}]+)\}", r"\1:", value)
    value = re.sub(r"\\label\{[^}]+\}", "", value)
    value = re.sub(r"\\color\{[^}]+\}\s*", "", value)
    value = re.sub(r"\\url\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\(?:short)?cite\{([^}]+)\}", r"[\1]", value)
    value = re.sub(r"\\(?:auto)?ref\{([^}]+)\}", lambda match: _clean_ref_label(match.group(1)), value)
    value = re.sub(r"\\eqref\{([^}]+)\}", lambda match: f"Eq. {_clean_ref_label(match.group(1))}", value)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(
            r"\\(?:emph|texttt|textbf|textit|text|mathrm|mathbf|mathbb|mathcal|mathsf)\{([^{}]+)\}",
            r"\1",
            value,
        )
        value = re.sub(r"\\num\{([^{}]+)\}", r"\1", value)
        value = re.sub(r"\\vect\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\(?:ccby|ccbync|cczero)\s*([^.]*)", r"License: \1", value)
    value = value.replace("\\slash", "/")
    value = value.replace("\\&", "&")
    value = value.replace("\\_", "_")
    value = value.replace("\\%", "%")
    value = value.replace("\\#", "#")
    value = value.replace("\\{", "{")
    value = value.replace("\\}", "}")
    value = value.replace("``", '"').replace("''", '"')
    replacements = {
        "\\leq": "<=",
        "\\geq": ">=",
        "\\neq": "!=",
        "\\approx": "~",
        "\\times": "x",
        "\\cdot": "*",
        "\\inR": "in R",
        "\\infty": "infinity",
        "\\downarrow": "↓",
        "\\uparrow": "↑",
        "\\rightarrow": "→",
        "\\Delta": "Delta",
        "\\delta": "delta",
        "\\alpha": "alpha",
        "\\beta": "beta",
        "\\gamma": "gamma",
        "\\lambda": "lambda",
        "\\theta": "theta",
        "\\mu": "mu",
        "\\sigma": "sigma",
        "\\pi": "pi",
        "\\omega": "omega",
        "\\ell": "ell",
    }
    for latex, replacement in replacements.items():
        value = value.replace(latex, replacement)
    value = re.sub(r"\bref:[A-Za-z]+:([A-Za-z0-9_.-]+)", r"\1", value)
    value = re.sub(r"\bref:([A-Za-z0-9_.:-]+)", lambda match: _clean_ref_label(match.group(1)), value)
    value = re.sub(r"\\([A-Za-z]+)", r"\1", value)
    return value


def _clean_inline_math_latex(value: str) -> str:
    value = value.replace("$", "")
    value = value.replace("\\slash", "/")
    value = value.replace("\\_", "_")
    value = value.replace("\\%", "%")
    value = re.sub(r"\\num\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\inR(?=[^A-Za-z]|$)", r"\\in\\mathbb{R}", value)
    value = re.sub(r"\\inZ(?=[^A-Za-z]|$)", r"\\in\\mathbb{Z}", value)
    value = re.sub(r"\\top(?=[A-Za-z])", r"\\top ", value)
    value = re.sub(r"\\textbf\{([A-Za-z]+)_([A-Za-z0-9]+)\}", r"\\mathbf{\1}_{\2}", value)
    value = _clean_text_macros_inside_math(value)
    value = _wrap_scientific_notation_literals(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _wrap_scientific_notation_literals(value: str) -> str:
    return re.sub(
        r"((?:\\(?!text\b)[A-Za-z]+)|^|[^A-Za-z0-9{.])(\d+(?:\.\d+)?e[+-]\d+)",
        r"\1\\text{\2}",
        value,
    )


def _clean_text_macros_inside_math(value: str) -> str:
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\\text\{([^{}]*)\}", lambda match: f"\\text{{{_clean_math_text_content(match.group(1))}}}", value)
    return value


def _clean_math_text_content(value: str) -> str:
    return (
        value.replace("\\slash", "/")
        .replace("\\rightarrow", "→")
        .replace("\\leftarrow", "←")
        .replace("\\&", "&")
    )


def _split_inline_math(value: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    text_start = 0
    math_start: int | None = None
    brace_depth = 0
    escaped = False
    index = 0
    while index < len(value):
        char = value[index]
        if char == "\\" and not escaped:
            escaped = True
            index += 1
            continue
        if math_start is not None and not escaped:
            if char == "{":
                brace_depth += 1
            elif char == "}" and brace_depth > 0:
                brace_depth -= 1
        if char == "$" and not escaped:
            if math_start is None:
                if text_start < index:
                    parts.append(("text", value[text_start:index]))
                math_start = index + 1
                brace_depth = 0
            elif brace_depth == 0:
                parts.append(("math", value[math_start:index]))
                math_start = None
                text_start = index + 1
        escaped = False
        index += 1
    if math_start is not None:
        parts.append(("text", value[text_start:]))
    elif text_start < len(value):
        parts.append(("text", value[text_start:]))
    return parts


def _find_display_environment_begin(line: str) -> int | None:
    math = False
    brace_depth = 0
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == "\\" and not escaped:
            if not math and BEGIN_RE.match(line, index):
                return index
            escaped = True
            index += 1
            continue
        if math and not escaped:
            if char == "{":
                brace_depth += 1
            elif char == "}" and brace_depth > 0:
                brace_depth -= 1
        if char == "$" and not escaped:
            if not math:
                math = True
                brace_depth = 0
            elif brace_depth == 0:
                math = False
        escaped = False
        index += 1
    return None


def _has_open_inline_math(value: str) -> bool:
    math = False
    brace_depth = 0
    escaped = False
    for char in value:
        if char == "\\" and not escaped:
            escaped = True
            continue
        if math and not escaped:
            if char == "{":
                brace_depth += 1
            elif char == "}" and brace_depth > 0:
                brace_depth -= 1
        if char == "$" and not escaped:
            if not math:
                math = True
                brace_depth = 0
            elif brace_depth == 0:
                math = False
        escaped = False
    return math


def _replace_href_commands(value: str) -> str:
    command = "\\href"
    index = value.find(command)
    while index != -1:
        first_start = index + len(command)
        if first_start >= len(value) or value[first_start] != "{":
            index = value.find(command, index + len(command))
            continue
        _, first_end = _read_balanced_braces(value, first_start)
        if first_end >= len(value) or value[first_end] != "{":
            index = value.find(command, first_end)
            continue
        label, second_end = _read_balanced_braces(value, first_end)
        value = f"{value[:index]}{clean_inline_latex(label)}{value[second_end:]}"
        index = value.find(command, index + len(label))
    return value


def _clean_ref_label(label: str) -> str:
    return label.split(":")[-1].replace("_", "-")


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


def extract_graphic_references(environment_text: str) -> list[str]:
    uncommented = "\n".join(strip_latex_comment(line) for line in environment_text.splitlines())
    return [match.group(1).strip() for match in GRAPHICS_RE.finditer(uncommented)]


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


def _read_command_arguments(text: str, command: str, arity: int) -> tuple[list[str], int] | None:
    prefix = f"\\{command}"
    if not text.startswith(prefix):
        return None
    args: list[str] = []
    index = len(prefix)
    for _ in range(arity):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text) or text[index] != "{":
            return None
        arg, index = _read_balanced_braces(text, index)
        args.append(arg)
    return args, index


def _replace_command_with_arguments(
    value: str,
    command: str,
    arity: int,
    formatter,
) -> str:
    prefix = f"\\{command}"
    output: list[str] = []
    index = 0
    while True:
        start = value.find(prefix, index)
        if start == -1:
            output.append(value[index:])
            return "".join(output)
        output.append(value[index:start])
        parsed = _read_command_arguments(value[start:], command, arity)
        if parsed is None:
            output.append(prefix)
            index = start + len(prefix)
            continue
        args, end = parsed
        output.append(formatter(args))
        index = start + end


def clean_reader_latex(value: str) -> str:
    value = _replace_command_with_arguments(value, "textcolor", 2, lambda args: args[1])
    value = _replace_command_with_arguments(value, "Call", 2, lambda args: f"{args[0]}({args[1]})")
    value = _replace_command_with_arguments(value, "Comment", 1, lambda args: args[0])
    value = re.sub(r"\\(?:cellcolor|rowcolor)\{[^}]+\}", "", value)
    value = re.sub(r"\\(?:small|scriptsize|footnotesize|normalsize)\b", "", value)
    value = value.replace("\\greencheck", "Yes").replace("\\redX", "No")
    value = value.replace("\\\\", " ")
    return clean_inline_latex(value)


def parse_algorithm_block(environment_text: str) -> dict[str, object]:
    captions = extract_captions(environment_text)
    title = captions[0] if captions else "Algorithm"
    body = _extract_environment_body(environment_text, "algorithmic") or environment_text
    steps: list[dict[str, object]] = []
    depth = 0
    for raw_line in body.splitlines():
        line = strip_latex_comment(raw_line).strip()
        if not line or line.startswith("\\begin") or line.startswith("\\end"):
            continue
        normalized = _parse_algorithm_line(line, depth)
        if normalized["kind"] == "end":
            depth = max(0, depth - 1)
            continue
        if normalized["kind"] in {"for", "while", "if", "procedure"}:
            steps.append({"kind": normalized["kind"], "depth": depth, "text": normalized["text"]})
            depth += 1
            continue
        steps.append({"kind": normalized["kind"], "depth": depth, "text": normalized["text"]})
    return {"title": title, "steps": steps}


def _parse_algorithm_line(line: str, depth: int) -> dict[str, str | int]:
    for command, label in (
        ("EndFor", "end"),
        ("EndWhile", "end"),
        ("EndIf", "end"),
        ("EndProcedure", "end"),
    ):
        if line.startswith(f"\\{command}"):
            return {"kind": label, "text": "", "depth": depth}
    for command, kind, label in (
        ("For", "for", "For"),
        ("While", "while", "While"),
        ("If", "if", "If"),
    ):
        parsed = _read_command_arguments(line, command, 1)
        if parsed:
            args, end = parsed
            condition = clean_reader_latex(args[0])
            remainder = clean_reader_latex(line[end:].strip())
            text = f"{label} {condition}"
            if remainder:
                text = f"{text}: {remainder}"
            return {"kind": kind, "text": text, "depth": depth}
    parsed_procedure = _read_command_arguments(line, "Procedure", 2)
    if parsed_procedure:
        args, end = parsed_procedure
        name = clean_reader_latex(args[0])
        params = clean_reader_latex(args[1])
        suffix = clean_reader_latex(line[end:].strip(" :"))
        text = f"Procedure {name}({params})"
        if suffix:
            text = f"{text}: {suffix}"
        return {"kind": "procedure", "text": text, "depth": depth}
    for command, kind, label in (
        ("Statex", "note", ""),
        ("State", "step", ""),
        ("Return", "return", "Return "),
    ):
        prefix = f"\\{command}"
        if line.startswith(prefix):
            text = clean_reader_latex(line[len(prefix) :].strip())
            return {"kind": kind, "text": f"{label}{text}".strip(), "depth": depth}
    return {"kind": "step", "text": clean_reader_latex(line), "depth": depth}


def parse_table_block(environment_text: str) -> dict[str, object]:
    captions = extract_captions(environment_text)
    body = _extract_environment_body(environment_text, "tabular") or ""
    body = re.sub(r"^\{[^{}]*\}", "", body, count=1).strip()
    rows: list[list[dict[str, object]]] = []
    for raw_row in _split_table_rows(body):
        row_text = re.sub(r"\\(?:hline|cline\{[^}]+\})", "", raw_row).strip()
        if not row_text:
            continue
        cells = [_parse_table_cell(cell) for cell in _split_latex_cells(row_text)]
        if any(str(cell.get("text", "")).strip() or cell.get("colspan", 1) != 1 for cell in cells):
            rows.append(cells)
    return {
        "caption": captions[0] if captions else "",
        "headerRows": _infer_table_header_rows(rows),
        "rows": rows,
    }


def _extract_environment_body(environment_text: str, environment: str) -> str | None:
    match = re.search(
        rf"\\begin\{{{re.escape(environment)}\}}(?:\[[^\]]*\])?(.*?)\\end\{{{re.escape(environment)}\}}",
        environment_text,
        re.DOTALL,
    )
    if not match:
        return None
    return match.group(1).strip()


def _split_table_rows(body: str) -> list[str]:
    uncommented = "\n".join(strip_latex_comment(line) for line in body.splitlines())
    return [
        row.strip()
        for row in re.split(r"\\\\(?:\s*(?:\\hline|\\cline\{[^}]+\}))*", uncommented)
    ]


def _split_latex_cells(row: str) -> list[str]:
    cells: list[str] = []
    start = 0
    depth = 0
    math = False
    escaped = False
    for index, char in enumerate(row):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "$" and not escaped:
            math = not math
        elif not math and not escaped:
            if char == "{":
                depth += 1
            elif char == "}" and depth > 0:
                depth -= 1
            elif char == "&" and depth == 0:
                cells.append(row[start:index].strip())
                start = index + 1
        escaped = False
    cells.append(row[start:].strip())
    return cells


def _parse_table_cell(value: str) -> dict[str, object]:
    parsed = _read_command_arguments(value.strip(), "multicolumn", 3)
    colspan = 1
    if parsed:
        args, end = parsed
        colspan = int(args[0]) if args[0].isdigit() else 1
        value = f"{args[2]} {value[end:]}".strip()
    return {"text": clean_reader_latex(value), "colspan": colspan}


def _infer_table_header_rows(rows: list[list[dict[str, object]]]) -> int:
    if not rows:
        return 0
    first = str(rows[0][0].get("text", "")).strip() if rows[0] else ""
    if first == "" and any(int(cell.get("colspan", 1)) > 1 for cell in rows[0]):
        return min(2, len(rows))
    if first.startswith("1-way"):
        return min(2, len(rows))
    if first == "Model Name":
        return min(3, len(rows))
    return 1


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
        'import FigurePanel from "../../components/FigurePanel.astro";',
        'import LatexBlock from "../../components/LatexBlock.astro";',
        'import EquationBlock from "../../components/EquationBlock.astro";',
        'import AlgorithmBlock from "../../components/AlgorithmBlock.astro";',
        'import TableBlock from "../../components/TableBlock.astro";',
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
                    f'  original="{escape_attr(clean_inline_latex(str(block["text"])))}"',
                    f'  translation="{escape_attr(clean_inline_latex(translations.get(paragraph_id, "")))}"',
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
            images = block.get("images", [])
            if isinstance(images, list) and images:
                caption = clean_inline_latex(str(block.get("caption", "Source-paper figure.")))
                lines.extend(
                    [
                        f'<FigurePanel id="{latex_id}-figure"',
                        f'  title="{label}"',
                        f'  caption="{escape_attr(caption)}"',
                        f"  images={{{format_mdx_string_array([str(image) for image in images])}}}",
                        "/>",
                        "",
                    ]
                )
            elif block.get("environment") in DISPLAY_MATH_ENVIRONMENTS:
                lines.extend(
                    [
                        f'<EquationBlock id="{latex_id}"',
                        f'  label="{label}"',
                        f"  latex={{{json.dumps(str(block['text']), ensure_ascii=False)}}}",
                        "/>",
                        "",
                    ]
                )
            elif block.get("environment") in ALGORITHM_ENVIRONMENTS:
                algorithm = parse_algorithm_block(str(block["text"]))
                lines.extend(
                    [
                        f'<AlgorithmBlock id="{latex_id}"',
                        f'  label="{label}"',
                        f'  title="{escape_attr(str(algorithm["title"]))}"',
                        f"  steps={{{json.dumps(algorithm['steps'], ensure_ascii=False)}}}",
                        "/>",
                        "",
                    ]
                )
            elif block.get("environment") in TABLE_ENVIRONMENTS:
                table = parse_table_block(str(block["text"]))
                lines.extend(
                    [
                        f'<TableBlock id="{latex_id}"',
                        f'  label="{label}"',
                        f'  caption="{escape_attr(str(table["caption"]))}"',
                        f'  headerRows={{{int(table["headerRows"])}}}',
                        f"  rows={{{json.dumps(table['rows'], ensure_ascii=False)}}}",
                        "/>",
                        "",
                    ]
                )
            else:
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
            continue
        else:
            lines.extend(["```latex", str(block["text"]), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def format_mdx_string_array(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False)


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


def _section_from_file(
    source_file: Path, source_root: Path, asset_output: Path | None = None
) -> dict[str, object]:
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
            _attach_graphic_assets(block, source_root, asset_output)
    return section


def _attach_graphic_assets(
    block: dict[str, object], source_root: Path, asset_output: Path | None
) -> None:
    if asset_output is None:
        return
    references = extract_graphic_references(str(block["text"]))
    images: list[str] = []
    missing: list[str] = []
    for reference in references:
        resolved = resolve_asset_reference(source_root, reference)
        if resolved is None:
            missing.append(reference)
            continue
        images.append(materialize_paper_asset(source_root, resolved, asset_output))
    if images:
        block["images"] = images
    if missing:
        block["missing_images"] = missing


def public_asset_path(source_root: Path, asset_path: Path) -> str:
    relative = optimized_asset_relative_path(source_root, asset_path)
    return f"paper-assets/{relative.as_posix()}"


def optimized_asset_relative_path(source_root: Path, asset_path: Path) -> Path:
    return asset_path.relative_to(source_root).with_suffix(WEB_IMAGE_EXTENSION)


def materialize_paper_asset(source_root: Path, asset_path: Path, asset_output: Path) -> str:
    public_relative = optimized_asset_relative_path(source_root, asset_path)
    target = asset_output / public_relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if asset_path.suffix.lower() == ".pdf":
        with tempfile.TemporaryDirectory() as tmp_dir:
            prefix = Path(tmp_dir) / "page"
            subprocess.run(
                [
                    "pdftoppm",
                    "-singlefile",
                    "-png",
                    "-r",
                    str(PDF_RASTER_DPI),
                    str(asset_path),
                    str(prefix),
                ],
                check=True,
            )
            optimize_raster_asset(prefix.with_suffix(".png"), target)
    else:
        optimize_raster_asset(asset_path, target)
    return f"paper-assets/{public_relative.as_posix()}"


def optimize_raster_asset(source: Path, target: Path) -> None:
    from PIL import Image, ImageOps

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        image.thumbnail(
            (WEB_IMAGE_MAX_DIMENSION, WEB_IMAGE_MAX_DIMENSION),
            Image.Resampling.LANCZOS,
        )
        if image.mode in {"RGBA", "LA"}:
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.getchannel("A"))
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        image.save(target, "WEBP", quality=WEB_IMAGE_QUALITY, method=6)


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


def import_sections(source_root: Path, asset_output: Path | None = None) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    main_file = source_root / "main.tex"
    if main_file.exists():
        sections.append(_abstract_section_from_main(main_file))
    sections.extend(
        _section_from_file(path, source_root, asset_output) for path in _section_files_from_main(source_root)
    )
    return sections


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import CPD paper LaTeX into MDX scaffolds.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--translations", type=Path)
    parser.add_argument("--asset-output", type=Path)
    args = parser.parse_args(argv)

    translations = load_translations(args.translations)
    if args.asset_output is not None:
        shutil.rmtree(args.asset_output, ignore_errors=True)
        args.asset_output.mkdir(parents=True, exist_ok=True)
    sections = import_sections(args.source, args.asset_output)
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
