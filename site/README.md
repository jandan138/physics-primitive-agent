# CPD Paper Companion Site

This directory is an isolated Astro static site for the CPD paper companion. It is separate from
the Python package under `src/` and must not become a home for compiler, experiment, or DeepDive
runtime code.

## Tech Stack

- Astro 6 with the MDX integration.
- Hand-written Astro components and CSS.
- No React, Vue, Svelte, Tailwind, or component-library dependency is part of this site.
- GitHub Pages deploys the static output from `site/dist/` through
  `.github/workflows/deploy-paper-site.yml`.

## Directory Contract

- `src/pages/paper/`: route entry points for the paper reader.
- `src/layouts/`: page-level shells and source-namespace banners.
- `src/components/`: reusable reader components such as paper blocks, status badges, and LaTeX
  blocks.
- `src/content/paper/`: generated MDX pages for the imported paper sections.
- `src/data/paper-manifest.json`: generated navigation/order metadata for paper sections.
- `src/data/translations/`: editable translation source shards keyed by stable paper block IDs.
- `src/styles/`: site-specific CSS only.
- `scripts/import_cpd_paper.py`: importer that regenerates `src/content/paper/` from the local
  source intake plus translation shards.

## Generated And Local-Only Files

Do not commit these directories:

- `node_modules/`
- `.astro/`
- `dist/`
- `scripts/__pycache__/`

The raw paper intake under `docs/tmp/papers/` is local source material and is not part of the
site's tracked tree. The generated MDX pages may contain source-paper text, but copied paper images
or other paper assets must not be published from `site/public/` until a dated permission record is
attached.

## Claim And Permission Boundaries

- Every source-paper prose or caption block must use `sourceNamespace="cpd_paper_source_text"`.
- Source-paper claims must remain visibly marked as `source-paper-not-project-evidence`.
- Draft translations must stay marked `translationStatus="draft_ai_assisted"` until human review is
  recorded.
- Reproduction status must stay `reproductionStatus="not_started"` unless a dated reproduction
  record exists.
- Public permission wording must stay record-pending until the authorization record is committed.

The site validator enforces these boundaries:

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/validate_site_claims.py
```

## Regeneration

Regenerate paper pages after editing translations or importer logic:

```bash
PYTHONDONTWRITEBYTECODE=1 python site/scripts/import_cpd_paper.py \
  --source docs/tmp/papers/arXiv-2602.07369v1 \
  --output site/src/content/paper \
  --translations site/src/data/translations
```

Then run the focused checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_cpd_paper_importer.py tests/test_site_claims.py
PYTHONDONTWRITEBYTECODE=1 python scripts/validate_site_claims.py
npm --prefix site run build
```

## Visual QA

Browser review is required after changing paper rendering, figure handling, generated assets, or
reader CSS. The current visual QA record is:

```text
docs/records/2026-05-16-paper-site-visual-qa.md
```

The review must use the built site through Astro preview, not only source inspection:

```bash
npm --prefix site run build
npm --prefix site run preview -- --host 127.0.0.1 --port 4321
```

At minimum, check `/paper/` and every manifest section at desktop, tablet, and mobile widths for:

- page-wide horizontal overflow;
- broken images or HTTP errors after scrolling lazy images into view;
- over-compressed, undersized, distorted, or upscaled figures;
- raw LaTeX leakage outside intentional source blocks;
- formula overflow, cramped fractions, and scientific-notation spacing regressions;
- unreadable preserved LaTeX/table source blocks.

## Deployment

The public page is served from GitHub Pages at:

```text
https://jandan138.github.io/physics-primitive-agent/paper/
```

The site config must keep:

- `site: "https://jandan138.github.io"`
- `base: "/physics-primitive-agent"`

Changing either value requires rebuilding the site and verifying the public `/paper/` URL.
