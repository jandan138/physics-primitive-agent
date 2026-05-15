# CPD Paper Companion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub Pages-ready Astro + MDX CPD paper companion with authorized English text, AI-assisted Chinese draft translation, source-paper claim namespacing, main-paper figures, and claim-bounded reproduction structure.

**Architecture:** Keep the paper site self-contained under `site/`, with Python import tooling tested by the existing pytest suite. LaTeX source remains in `docs/tmp/papers/arXiv-2602.07369v1/`; generated and edited site content lives under `site/src/content/paper/` and renders through reusable Astro components.

**Tech Stack:** Astro, MDX, TypeScript-light Astro components, CSS, Python import script, pytest.

---

## File Structure

- Create `site/package.json`: npm scripts and dependencies for Astro, MDX, and static build.
- Create `site/astro.config.mjs`: GitHub Pages-compatible static output configuration.
- Create `site/tsconfig.json`: Astro TypeScript configuration.
- Create `site/src/layouts/PaperLayout.astro`: shared paper reader shell.
- Create `site/src/components/PaperBlock.astro`: English/Chinese paragraph block.
- Create `site/src/components/FigurePanel.astro`: figure renderer for main-paper images and PDF source links.
- Create `site/src/components/StatusBadge.astro`: consistent status display.
- Create `site/src/styles/paper.css`: academic-reader styling.
- Create `site/src/pages/paper/*.astro`: generated route wrappers for section MDX files.
- Create `site/src/content/paper/*.mdx`: imported paper sections.
- Create `site/src/content/paper/manifest.json`: section order, source version, and claim-boundary metadata.
- Create `site/scripts/import_cpd_paper.py`: conservative LaTeX importer and asset copier.
- Create `site/scripts/translation_seed.py`: translation helper data model used by Codex/manual generation, without external API calls.
- Create `scripts/validate_site_claims.py`: site-specific claim/status validator.
- Create `tests/test_cpd_paper_importer.py`: importer unit tests.
- Create `tests/test_site_claims.py`: source-namespace validator tests.
- Create `docs/records/2026-05-15-cpd-paper-companion-mvp.md`: dated implementation record.
- Modify `docs/index.md`: add a link to the paper companion design/record.
- Modify `docs/records/README.md`: add record index entry.

## Task 1: Site Scaffold

**Files:**
- Create: `site/package.json`
- Create: `site/astro.config.mjs`
- Create: `site/tsconfig.json`
- Create: `site/src/env.d.ts`

- [ ] **Step 1: Add npm package metadata**

Create `site/package.json`:

```json
{
  "name": "physics-primitive-agent-paper-site",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev --host 0.0.0.0",
    "build": "astro build",
    "preview": "astro preview --host 0.0.0.0"
  },
  "dependencies": {
    "@astrojs/mdx": "^4.0.0",
    "astro": "^5.0.0"
  },
  "devDependencies": {}
}
```

- [ ] **Step 2: Add Astro config**

Create `site/astro.config.mjs`:

```js
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  output: "static",
  integrations: [mdx()],
  site: "https://physics-primitive-agent.github.io",
  base: "/physics-primitive-agent",
});
```

- [ ] **Step 3: Add TypeScript config**

Create `site/tsconfig.json`:

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": "."
  }
}
```

Create `site/src/env.d.ts`:

```ts
/// <reference types="astro/client" />
```

- [ ] **Step 4: Install dependencies**

Run:

```sh
cd site && npm install
```

Expected: `site/package-lock.json` is created and `npm` exits 0.

- [ ] **Step 5: Run initial build**

Run:

```sh
cd site && npm run build
```

Expected: build fails only because pages have not been created yet, or succeeds after Astro creates an empty site. Record the actual output in the implementation notes.

## Task 2: Core Reader Components

**Files:**
- Create: `site/src/components/StatusBadge.astro`
- Create: `site/src/components/PaperBlock.astro`
- Create: `site/src/components/FigurePanel.astro`
- Create: `site/src/layouts/PaperLayout.astro`
- Create: `site/src/styles/paper.css`

- [ ] **Step 1: Add status badge component**

Create `site/src/components/StatusBadge.astro`:

```astro
---
interface Props {
  label: string;
  tone?: "neutral" | "draft" | "partial" | "blocked";
}

const { label, tone = "neutral" } = Astro.props;
---

<span class={`status-badge status-badge--${tone}`}>{label}</span>
```

- [ ] **Step 2: Add paper block component**

Create `site/src/components/PaperBlock.astro`:

```astro
---
import StatusBadge from "./StatusBadge.astro";

interface Props {
  id: string;
  section?: string;
  original: string;
  translation: string;
  translationStatus?: string;
  explanationStatus?: string;
  reproductionStatus?: string;
  sourceNamespace?: string;
  translationProvenance?: string;
}

const {
  id,
  section = "",
  original,
  translation,
  translationStatus = "draft_ai_assisted",
  explanationStatus = "empty",
  reproductionStatus = "not_started",
  sourceNamespace = "cpd_paper_source_text",
  translationProvenance = "",
} = Astro.props;
---

<article class="paper-block" id={id} data-source-namespace={sourceNamespace}>
  <header class="paper-block__meta">
    <a href={`#${id}`} class="paper-block__anchor">{section ? `${section} / ` : ""}{id}</a>
    <div class="paper-block__badges">
      <StatusBadge label="AI 初译，待人工校对" tone="draft" />
      <StatusBadge label="源论文文本，不是项目证据" tone="partial" />
      <StatusBadge label={`解释: ${explanationStatus}`} />
      <StatusBadge label={`复现: ${reproductionStatus}`} />
    </div>
  </header>
  <div class="paper-block__original" lang="en">{original}</div>
  <div class="paper-block__translation" lang="zh-Hans">{translation}</div>
  <footer class="paper-block__status">
    translation_status: {translationStatus}
    {translationProvenance && <span> / provenance: {translationProvenance}</span>}
  </footer>
</article>
```

- [ ] **Step 3: Add figure panel component**

Create `site/src/components/FigurePanel.astro`:

```astro
---
interface Props {
  id: string;
  title: string;
  caption: string;
  images?: string[];
  source?: string;
}

const { id, title, caption, images = [], source = "" } = Astro.props;
---

<figure class="figure-panel" id={id}>
  <figcaption>
    <strong>{title}</strong>
    <span>{caption}</span>
  </figcaption>
  {images.length > 0 ? (
    <div class="figure-panel__grid">
      {images.map((image) => <img src={image} alt={`${title} image`} loading="lazy" />)}
    </div>
  ) : (
    <a class="figure-panel__source" href={source}>View source figure</a>
  )}
</figure>
```

- [ ] **Step 4: Add paper layout**

Create `site/src/layouts/PaperLayout.astro`:

```astro
---
import "../styles/paper.css";

interface NavItem {
  href: string;
  label: string;
}

interface Props {
  title: string;
  description?: string;
  navItems?: NavItem[];
}

const { title, description = "", navItems = [] } = Astro.props;
---

<!doctype html>
<html lang="zh-Hans">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content={description} />
    <title>{title}</title>
  </head>
  <body>
    <div class="paper-shell">
      <aside class="paper-nav" aria-label="Paper sections">
        <a class="paper-nav__home" href="/paper/">CPD Companion</a>
        {navItems.map((item) => <a href={item.href}>{item.label}</a>)}
      </aside>
      <main class="paper-main">
        <aside class="source-namespace-banner">
          The English paper text and translated text describe the CPD paper. They are not claims
          that this repository has reproduced the paper or achieved the paper's reported benchmark
          results.
        </aside>
        <slot />
      </main>
    </div>
  </body>
</html>
```

- [ ] **Step 5: Add reader CSS**

Create `site/src/styles/paper.css` with stable dimensions, readable typography, responsive rails, and status colors:

```css
:root {
  color-scheme: light;
  --paper-bg: #f7f7f4;
  --paper-surface: #ffffff;
  --paper-text: #1f2933;
  --paper-muted: #5f6b76;
  --paper-border: #d9ddd7;
  --paper-accent: #25636f;
  --paper-draft: #8a5a00;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
  margin: 0;
  background: var(--paper-bg);
  color: var(--paper-text);
}

.paper-shell {
  display: grid;
  grid-template-columns: minmax(180px, 260px) minmax(0, 1fr);
  min-height: 100vh;
}

.paper-nav {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  border-right: 1px solid var(--paper-border);
  background: #eef1ed;
  padding: 24px 18px;
}

.paper-nav a {
  display: block;
  color: var(--paper-text);
  text-decoration: none;
  padding: 7px 0;
}

.paper-nav__home {
  font-weight: 700;
  margin-bottom: 14px;
}

.paper-main {
  max-width: 1080px;
  width: min(100%, 1080px);
  margin: 0 auto;
  padding: 40px 28px 80px;
}

.paper-block,
.figure-panel {
  background: var(--paper-surface);
  border: 1px solid var(--paper-border);
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}

.paper-block__meta {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.paper-block__anchor {
  color: var(--paper-accent);
  font-weight: 700;
  text-decoration: none;
}

.paper-block__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: flex-end;
}

.status-badge {
  border: 1px solid var(--paper-border);
  border-radius: 999px;
  color: var(--paper-muted);
  font-size: 12px;
  line-height: 1;
  padding: 6px 8px;
  white-space: nowrap;
}

.status-badge--draft {
  border-color: #dfc06c;
  color: var(--paper-draft);
  background: #fff6dc;
}

.status-badge--partial {
  border-color: #8db5bd;
  color: var(--paper-accent);
  background: #e7f4f6;
}

.source-namespace-banner {
  background: #eef7f7;
  border: 1px solid #b7d7dc;
  border-radius: 8px;
  color: #244d57;
  line-height: 1.6;
  margin-bottom: 24px;
  padding: 14px 16px;
}

.paper-block__original {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.7;
}

.paper-block__translation {
  border-left: 3px solid var(--paper-accent);
  color: #263744;
  font-size: 17px;
  line-height: 1.85;
  margin-top: 14px;
  padding-left: 14px;
}

.paper-block__status {
  color: var(--paper-muted);
  font-size: 12px;
  margin-top: 12px;
}

.figure-panel img {
  max-width: 100%;
  height: auto;
  border: 1px solid var(--paper-border);
  border-radius: 6px;
}

.figure-panel__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 14px;
}

@media (max-width: 860px) {
  .paper-shell {
    display: block;
  }

  .paper-nav {
    position: static;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--paper-border);
  }

  .paper-main {
    padding: 24px 16px 56px;
  }

  .paper-block__meta {
    display: block;
  }

  .paper-block__badges {
    justify-content: flex-start;
    margin-top: 10px;
  }
}
```

## Task 3: Importer Tests

**Files:**
- Create: `tests/test_cpd_paper_importer.py`
- Create: `site/scripts/import_cpd_paper.py`

- [ ] **Step 1: Write importer test skeleton**

Create `tests/test_cpd_paper_importer.py`:

```python
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
        "\\section{Method}\\nFirst paragraph.\\n\\nSecond paragraph."
    )

    assert [block["type"] for block in blocks] == ["section", "paragraph", "paragraph"]
    assert blocks[0]["title"] == "Method"
    assert blocks[1]["text"] == "First paragraph."


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
    assert 'original="A primitive is fitted."' in mdx
    assert 'translation="拟合一个基本体。"' in mdx


def test_asset_resolver_handles_case_mismatch(tmp_path):
    importer = _load_importer()
    asset_root = tmp_path / "paper"
    asset_dir = asset_root / "assets"
    asset_dir.mkdir(parents=True)
    actual = asset_dir / "Dungeon_Level_coacd.jpg"
    actual.write_bytes(b"image")

    resolved = importer.resolve_asset_reference(asset_root, "assets/Dungeon_level_coacd")

    assert resolved == actual
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```sh
python -m pytest tests/test_cpd_paper_importer.py -q
```

Expected: FAIL because `site/scripts/import_cpd_paper.py` does not exist.

## Task 4: Importer Implementation

**Files:**
- Modify: `site/scripts/import_cpd_paper.py`
- Test: `tests/test_cpd_paper_importer.py`

- [ ] **Step 1: Add minimal importer implementation**

Create `site/scripts/import_cpd_paper.py`:

```python
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RE = re.compile(r"^\\section(?:\{\\label\{[^}]+\}([^}]+)\}|\{([^}]+)\})")
SUBSECTION_RE = re.compile(r"^\\subsection\{([^}]+)\}")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".pdf")


def parse_latex_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        paragraph = clean_inline_latex(" ".join(paragraph_lines).strip())
        paragraph_lines.clear()
        if paragraph:
            blocks.append({"type": "paragraph", "text": paragraph})

    for raw_line in text.splitlines():
        line = raw_line.strip()
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
            blocks.append({"type": "subsection", "title": clean_inline_latex(subsection_match.group(1))})
            continue
        if line.startswith("\\begin{figure") or line.startswith("\\begin{algorithm") or line.startswith("\\begin{table"):
            flush_paragraph()
            blocks.append({"type": "source_block", "text": line})
            continue
        if line.startswith("\\end{figure") or line.startswith("\\end{algorithm") or line.startswith("\\end{table"):
            flush_paragraph()
            blocks.append({"type": "source_block", "text": line})
            continue
        paragraph_lines.append(line)

    flush_paragraph()
    return blocks


def clean_inline_latex(value: str) -> str:
    value = value.replace("~", " ")
    value = re.sub(r"\\label\{[^}]+\}", "", value)
    value = re.sub(r"\\cite\{([^}]+)\}", r"[\1]", value)
    value = re.sub(r"\\ref\{([^}]+)\}", r"\1", value)
    value = re.sub(r"\\emph\{([^}]+)\}", r"\1", value)
    value = re.sub(r"\\texttt\{([^}]+)\}", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def paragraph_ids(section: dict[str, object]) -> list[str]:
    slug = str(section["slug"])
    count = sum(1 for block in section["blocks"] if block.get("type") == "paragraph")  # type: ignore[index]
    return [f"{slug}-p{index:03d}" for index in range(1, count + 1)]


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


def render_section_mdx(section: dict[str, object], translations: dict[str, str]) -> str:
    lines = [
        "---",
        f'title: "{escape_frontmatter(str(section["title"]))}"',
        f'slug: "{section["slug"]}"',
        "---",
        'import PaperBlock from "../../components/PaperBlock.astro";',
        "",
        f"# {section['title']}",
        "",
    ]
    for block in section["blocks"]:  # type: ignore[index]
        if block["type"] == "paragraph":
            paragraph_id = str(block["id"])
            lines.extend(
                [
                    "<PaperBlock",
                    f'  id="{paragraph_id}"',
                    f'  section="{section["title"]}"',
                    f'  original="{escape_attr(str(block["text"]))}"',
                    f'  translation="{escape_attr(translations.get(paragraph_id, ""))}"',
                    '  translationStatus="draft_ai_assisted"',
                    '  explanationStatus="empty"',
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
        else:
            lines.extend(["```latex", str(block["text"]), "```", ""])
    return "\n".join(lines)


def escape_attr(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def escape_frontmatter(value: str) -> str:
    return value.replace('"', '\\"')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import CPD paper LaTeX into MDX scaffolds.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--translations", type=Path)
    args = parser.parse_args(argv)

    translations = {}
    if args.translations and args.translations.exists():
      translations = json.loads(args.translations.read_text(encoding="utf-8"))

    args.output.mkdir(parents=True, exist_ok=True)
    for source_file in args.source.glob("*.tex"):
        if source_file.name == "main.tex":
            continue
        slug = source_file.stem.replace("_", "-")
        blocks = parse_latex_blocks(source_file.read_text(encoding="utf-8"))
        section = {"slug": slug, "title": slug.replace("-", " ").title(), "blocks": blocks}
        ids = iter(paragraph_ids(section))
        for block in blocks:
            if block["type"] == "paragraph":
                block["id"] = next(ids)
        mdx = render_section_mdx(section, translations)
        (args.output / f"{slug}.mdx").write_text(mdx + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run importer tests**

Run:

```sh
python -m pytest tests/test_cpd_paper_importer.py -q
```

Expected: PASS.

## Task 5: Site Claim Validator

**Files:**
- Create: `scripts/validate_site_claims.py`
- Create: `tests/test_site_claims.py`

- [ ] **Step 1: Add validator tests**

Create `tests/test_site_claims.py`:

```python
from pathlib import Path

from scripts.validate_site_claims import validate_site_text


def test_site_validator_requires_source_namespace_banner():
    issues = validate_site_text("src/pages/paper/example.astro", "<main>No banner</main>")

    assert any("missing source namespace banner" in issue for issue in issues)


def test_site_validator_allows_source_paper_benchmark_claim_when_namespaced():
    text = """
    The English paper text and translated text describe the CPD paper.
    <PaperBlock sourceNamespace="cpd_paper_source_text" original="The paper reports improved performance." />
    """

    assert validate_site_text("src/content/paper/method.mdx", text) == []
```

- [ ] **Step 2: Add site claim validator**

Create `scripts/validate_site_claims.py`:

```python
from __future__ import annotations

from pathlib import Path
import sys

SITE_ROOTS = (Path("site/src/pages/paper"), Path("site/src/content/paper"))
REQUIRED_BANNER = "The English paper text and translated text describe the CPD paper."


def validate_site_text(path: str, text: str) -> list[str]:
    issues: list[str] = []
    if "src/pages/paper" in path and REQUIRED_BANNER not in text:
        issues.append(f"{path}: missing source namespace banner")
    if "PaperBlock" in text and 'sourceNamespace="cpd_paper_source_text"' not in text:
        issues.append(f"{path}: PaperBlock missing cpd_paper_source_text namespace")
    if "translationStatus=" in text and 'translationStatus="draft_ai_assisted"' not in text:
        issues.append(f"{path}: unexpected translation status in MVP")
    return issues


def validate_site(root: Path) -> list[str]:
    issues: list[str] = []
    for site_root in SITE_ROOTS:
        path = root / site_root
        if not path.exists():
            continue
        for file_path in sorted(path.rglob("*")):
            if file_path.suffix not in {".astro", ".mdx", ".json"}:
                continue
            relative = file_path.relative_to(root).as_posix()
            issues.extend(validate_site_text(relative, file_path.read_text(encoding="utf-8")))
    return issues


def main() -> int:
    issues = validate_site(Path.cwd())
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print("site claim validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Run site validator tests**

Run:

```sh
python -m pytest tests/test_site_claims.py -q
```

Expected: PASS.

## Task 6: Paper Pages And Manifest

**Files:**
- Create: `site/src/content/paper/manifest.json`
- Create: `site/src/pages/paper/index.astro`
- Create: `site/src/pages/paper/[slug].astro`

- [ ] **Step 1: Add paper manifest**

Create `site/src/content/paper/manifest.json`:

```json
{
  "paper_id": "knodt_gao_2026_convex_primitive_decomposition_for_collision_detection",
  "source_version": "arxiv_2602.07369v1",
  "source_path": "docs/tmp/papers/arXiv-2602.07369v1",
  "translation_status": "draft_ai_assisted",
  "permission_status": "user_confirmed_private_permission",
  "permission_artifact_status": "pending_user_supplied_record_or_redacted_summary",
  "claim_boundary": "authorized_bilingual_companion_not_cpd_reproduction",
  "sections": [
    {"slug": "abstract", "title": "Abstract"},
    {"slug": "introduction", "title": "Introduction"},
    {"slug": "background", "title": "Related Work"},
    {"slug": "method", "title": "Method"},
    {"slug": "experiments", "title": "Results And Ablations"},
    {"slug": "conclusion", "title": "Discussion, Limitations, And Conclusion"},
    {"slug": "additional-results", "title": "Additional Results"}
  ]
}
```

- [ ] **Step 2: Add paper index page**

Create `site/src/pages/paper/index.astro`:

```astro
---
import PaperLayout from "../../layouts/PaperLayout.astro";
import manifest from "../../content/paper/manifest.json";

const navItems = manifest.sections.map((section) => ({
  href: `/paper/${section.slug}/`,
  label: section.title,
}));
---

<PaperLayout title="CPD Paper Companion" description="Authorized bilingual CPD paper companion" navItems={navItems}>
  <section class="paper-hero">
    <p class="paper-kicker">Authorized bilingual companion</p>
    <h1>Convex Primitive Decomposition for Collision Detection</h1>
    <p>
      English source text with AI-assisted Chinese draft translation. Translation is not yet
      human-reviewed. Project reproduction notes are claim-bounded and added only where records
      exist.
    </p>
  </section>
  <section class="paper-section-list">
    {manifest.sections.map((section) => (
      <a class="paper-section-link" href={`/paper/${section.slug}/`}>
        <span>{section.title}</span>
        <small>{manifest.translation_status}</small>
      </a>
    ))}
  </section>
</PaperLayout>
```

- [ ] **Step 3: Add dynamic section page**

Create `site/src/pages/paper/[slug].astro`:

```astro
---
import PaperLayout from "../../layouts/PaperLayout.astro";
import manifest from "../../content/paper/manifest.json";

export async function getStaticPaths() {
  return manifest.sections.map((section) => ({
    params: { slug: section.slug },
    props: { section },
  }));
}

const { section } = Astro.props;
const modules = import.meta.glob("../../content/paper/*.mdx");
const modulePath = `../../content/paper/${section.slug}.mdx`;
const Content = modules[modulePath] ? (await modules[modulePath]()).default : null;
const navItems = manifest.sections.map((item) => ({
  href: `/paper/${item.slug}/`,
  label: item.title,
}));
---

<PaperLayout title={`${section.title} | CPD Paper Companion`} navItems={navItems}>
  {Content ? <Content /> : (
    <section class="paper-block">
      <h1>{section.title}</h1>
      <p>This section route is present, but imported content has not been generated in this working tree.</p>
    </section>
  )}
</PaperLayout>
```

## Task 7: Initial Content And Translations

**Files:**
- Create/modify: `site/src/content/paper/*.mdx`
- Create: `site/scripts/translation_seed.py`

- [ ] **Step 1: Add translation seed helper**

Create `site/scripts/translation_seed.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationEntry:
    paragraph_id: str
    original: str
    translation: str
    status: str = "draft_ai_assisted"
    source_hash: str = ""
    translated_at: str = "2026-05-15"
    translator: str = "codex"
    prompt_policy: str = "faithful_technical_draft_translation"


def entries_to_dict(entries: tuple[TranslationEntry, ...]) -> dict[str, str]:
    return {entry.paragraph_id: entry.translation for entry in entries}
```

- [ ] **Step 2: Generate MDX scaffolds**

Run:

```sh
python site/scripts/import_cpd_paper.py \
  --source docs/tmp/papers/arXiv-2602.07369v1 \
  --output site/src/content/paper
```

Expected: MDX files exist for the imported LaTeX chapter files.

- [ ] **Step 3: Rename route files to match manifest**

Rename generated content files so they match the manifest route slugs:

```text
background.mdx -> background.mdx
experiments.mdx -> experiments.mdx
conclusion.mdx -> conclusion.mdx
additional-results.mdx -> additional-results.mdx
```

Create `abstract.mdx` manually from the abstract in `main.tex`, using `PaperBlock` with ID
`abstract-p001`.

- [ ] **Step 4: Fill AI-assisted Chinese draft translations**

For each generated `PaperBlock`, read the English `original` and write a faithful Chinese draft
translation into `translation`. Preserve technical terms consistently:

```text
primitive -> 基本体
collider/collision object -> 碰撞体/碰撞对象
convex hull -> 凸包
rigid-body simulation -> 刚体仿真
Hausdorff distance -> Hausdorff 距离
Chamfer distance -> Chamfer 距离
quadric -> 二次型/二次误差度量
```

Keep `translationStatus="draft_ai_assisted"` for every paragraph.

- [ ] **Step 5: Keep explanation and reproduction empty states**

Do not add unrecorded implementation claims. Existing `PaperBlock` fields should remain:

```mdx
explanationStatus="empty"
reproductionStatus="not_started"
```

Only change a paragraph to `reproductionStatus="partial"` when it links to an existing dated
record in a follow-up task.

## Task 8: Main Figures

**Files:**
- Modify/create assets under `site/public/paper-assets/`
- Modify: `site/src/content/paper/introduction.mdx`
- Modify: `site/src/content/paper/method.mdx`
- Modify: `site/src/content/paper/experiments.mdx`
- Modify: `site/src/content/paper/conclusion.mdx`

- [ ] **Step 1: Copy web-native main-paper image assets**

Copy PNG/JPG files referenced by main-paper figures from:

```text
docs/tmp/papers/arXiv-2602.07369v1/assets/
docs/tmp/papers/arXiv-2602.07369v1/plots/
docs/tmp/papers/arXiv-2602.07369v1/ablations/
```

into:

```text
site/public/paper-assets/
```

Keep directory prefixes in filenames to avoid collisions, for example:

```text
assets_shinto_watchtower_anim.jpg
plots_eigen_input.png
ablations_cube2_input_ablation.png
```

Use `resolve_asset_reference()` from `site/scripts/import_cpd_paper.py` before copying. If an
asset cannot be resolved, write its LaTeX reference into an import warning list and render a source
link instead of an image.

- [ ] **Step 2: Add figure panels to main-paper MDX**

For each main-paper figure whose assets are PNG/JPG, insert:

```mdx
<FigurePanel
  id="fig-teaser"
  title="Figure 1"
  caption="Convex primitive decomposition teaser from the CPD paper."
  images={["/physics-primitive-agent/paper-assets/assets_shinto_watchtower_anim.jpg"]}
/>
```

For PDF-only plots, insert source links:

```mdx
<FigurePanel
  id="fig-decomposition-time"
  title="Decomposition Time Plot"
  caption="PDF plot source retained for first MVP."
  source="/physics-primitive-agent/paper-assets/plots_decomposition_time.pdf"
/>
```

## Task 9: Documentation Record And Index

**Files:**
- Create: `docs/records/2026-05-15-cpd-paper-companion-mvp.md`
- Modify: `docs/records/README.md`
- Modify: `docs/index.md`

- [ ] **Step 1: Add dated record**

Create `docs/records/2026-05-15-cpd-paper-companion-mvp.md`:

```md
# 2026-05-15 CPD Paper Companion MVP

## Date

2026-05-15

## Status

In progress

## Changes

- Recorded user-confirmed private permission status for full paper text, draft translation,
  paragraph annotations, figures, and GitHub Pages publication.
- Added a planned Astro + MDX CPD paper companion site.
- Added LaTeX import tooling and draft bilingual paper content.
- Kept explanations and reproduction notes claim-bounded as empty or not-started states.

## Verification

- `python -m pytest tests/test_cpd_paper_importer.py -q`
- `python scripts/validate_docs.py`
- `python -m pytest -q`
- `git diff --check`
- `cd site && npm run build`

## Artifacts

- `site/`
- `docs/tmp/papers/arXiv-2602.07369v1/`
- `docs/superpowers/specs/2026-05-15-cpd-paper-companion-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-paper-companion.md`

## Claim Impact

This supports only the existence of an authorized bilingual paper companion scaffold with AI
draft translation. It does not support full CPD reproduction, benchmark claims, collision-quality
validation, production compiler readiness, or human-reviewed translation quality.

## Next Action

Review the generated bilingual pages, then incrementally add human translation review and
section-level reproduction notes tied to dated records.
```

- [ ] **Step 2: Add record index entry**

Add this line to `docs/records/README.md` near other 2026-05-15 records:

```md
- 2026-05-15 CPD Paper Companion MVP:
  Astro + MDX bilingual paper companion scaffold and claim-bounded reproduction-map structure.
```

- [ ] **Step 3: Add docs index entry**

Add this line to `docs/index.md` under source intake/planning or design references:

```md
- CPD Paper Companion MVP record:
  bilingual CPD paper companion scaffold and claim-bounded reproduction-map structure.
```

## Task 10: Verification And Review

**Files:**
- All created/modified files above.

- [ ] **Step 1: Run importer tests**

Run:

```sh
python -m pytest tests/test_cpd_paper_importer.py -q
```

Expected: PASS.

- [ ] **Step 2: Run site claim validator tests**

Run:

```sh
python -m pytest tests/test_site_claims.py -q
```

Expected: PASS.

- [ ] **Step 3: Run site claim validation**

Run:

```sh
python scripts/validate_site_claims.py
```

Expected: `site claim validation passed`.

- [ ] **Step 4: Run docs validation**

Run:

```sh
python scripts/validate_docs.py
```

Expected: `docs validation passed`.

- [ ] **Step 5: Run full pytest suite**

Run:

```sh
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 6: Run whitespace check**

Run:

```sh
git diff --check
```

Expected: no output and exit 0.

- [ ] **Step 7: Build site**

Run:

```sh
cd site && npm run build
```

Expected: Astro build exits 0 and writes `site/dist/`.

- [ ] **Step 8: Inspect generated HTML**

Run:

```sh
find site/dist -maxdepth 3 -type f | sort | head -40
```

Expected: routes exist under `site/dist/paper/`, including `index.html` and section pages.

- [ ] **Step 9: Commit implementation slice**

Stage only files belonging to this feature:

```sh
git add site scripts/validate_site_claims.py tests/test_cpd_paper_importer.py tests/test_site_claims.py docs/records/2026-05-15-cpd-paper-companion-mvp.md docs/records/README.md docs/index.md docs/superpowers/plans/2026-05-15-cpd-paper-companion.md
git commit -m "feat: add CPD paper companion MVP"
```

Expected: commit contains the site scaffold, importer, generated content, docs record, and plan.

## Self-Review

- Spec coverage: the plan covers Astro + MDX, LaTeX import, AI-assisted draft translation, main
  figures, claim boundaries, docs record, and verification.
- Placeholder scan: implementation statuses use explicit `empty`, `not_started`, and
  `draft_ai_assisted` values instead of vague completion claims.
- Type consistency: component prop names match the MDX examples and importer output.
