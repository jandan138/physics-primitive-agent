# CPD Paper Companion Design

## Goal

Build a GitHub Pages-ready companion site for the CPD paper that presents the authorized full
English text, AI-assisted Chinese draft translation, main-paper figures, and a stable structure
for later explanations and project reproduction notes.

## Audience

The site serves three audiences at once:

- DeepDive and technical reviewers who need to see disciplined claim boundaries.
- Chinese readers who want a readable bilingual version of the CPD paper.
- Future developers who need a paragraph-level map from the paper to project code, configs,
  records, figures, and reproduction status.

The first version prioritizes full bilingual reading and site structure. Deeper explanation and
project reproduction notes are added incrementally after the structure is working.

## Source Material

The input source is the local LaTeX paper bundle:

```text
docs/tmp/papers/arXiv-2602.07369v1/
```

The top-level source file is:

```text
docs/tmp/papers/arXiv-2602.07369v1/main.tex
```

The imported chapter files are:

```text
introduction.tex
background.tex
method.tex
experiments.tex
conclusion.tex
additional_results.tex
```

`docs/tmp/` remains raw source intake and is not the canonical webpage content. The generated and
edited companion content should live under the site source tree, with a record linking it back to
the original LaTeX bundle and the private republication permission that the user will provide.

Before any full paper text or paper asset copy is committed for public release, the repository must
contain a dated record with at least this permission metadata:

```text
permission_status: user_confirmed_private_permission
permission_artifact_status: pending_user_supplied_record_or_redacted_summary
allowed_uses: English full text, Chinese translation, paragraph annotations, figures, GitHub Pages
```

The private permission artifact itself does not need to be committed if it contains private
correspondence. A redacted record is enough for repository governance until the user chooses to add
the full permission artifact.

## Technology

Use:

- Astro for the static site.
- MDX for paper content pages.
- A small import script for LaTeX-to-MDX scaffolding.
- Lightweight Astro components for paper blocks, figures, status badges, navigation, and
  reproduction empty states.

The deployed output is static HTML suitable for GitHub Pages. The repository should not depend on
a server process for the published site.

Because the site will contain source-paper claims that are stronger than this repository's current
claims, the implementation must add site-aware claim validation. The validator may not treat
authorized CPD paper text as this project's claim, but it must verify that every paper page carries
a visible "source paper text, not project evidence" namespace banner and draft-translation status.

## Site Structure

Create a self-contained site directory:

```text
site/
  package.json
  astro.config.mjs
  tsconfig.json
  src/
    components/
    content/
      paper/
    layouts/
    pages/
    styles/
  public/
    paper-assets/
  scripts/
```

Recommended routes:

```text
/paper/
/paper/abstract/
/paper/introduction/
/paper/related-work/
/paper/method/
/paper/results/
/paper/ablations/
/paper/discussion/
/paper/limitations/
/paper/conclusion/
/paper/additional-results/
/paper/reproduction-map/
```

The landing route `/paper/` is a reader index, not a marketing page. It should show the paper
title, authors, source version, translation status, claim boundary, section progress, and direct
links into the reading pages.

Every paper route must display a source-namespace notice:

```text
The English paper text and translated text describe the CPD paper. They are not claims that this
repository has reproduced the paper or achieved the paper's reported benchmark results.
```

## Page Layout

Use a restrained academic-reader layout with enough visual affordance to feel like a project
artifact:

- Sticky left navigation for sections.
- Center reading column for paragraph blocks.
- Right rail for page-level status, figure list, and reproduction map links on desktop.
- Collapsed drawer or top segmented navigation on mobile.
- Clear previous/next section navigation.
- Stable paragraph anchors for every imported paragraph.

The visual tone should be quiet and readable: white or near-white background, dark text, modest
accent colors for statuses, and no decorative gradients or marketing hero layout.

## Paper Block Model

Every imported natural-language paragraph becomes a block with a stable ID:

```mdx
<PaperBlock
  id="method-p012"
  section="3.2"
  original="..."
  translation="..."
  translationStatus="draft_ai_assisted"
  explanationStatus="empty"
  reproductionStatus="not_started"
/>
```

Semantics:

- `original`: authorized English source text after safe LaTeX cleanup.
- `translation`: AI-assisted Chinese draft produced in this repository workflow.
- `translationStatus`: initially `draft_ai_assisted`.
- `explanationStatus`: initially `empty`.
- `reproductionStatus`: initially `not_started`, except existing project-aligned sections may be
  marked `partial` only when a dated record and code path already exist.
- `sourceNamespace`: always `cpd_paper_source_text` for imported paper paragraphs.
- `translationProvenance`: records date, source hash, translating agent, and status.

The UI must make draft translation status visible. It must not imply human-reviewed translation
quality until a reviewer changes the status.

Original CPD paper claims about performance, benchmarks, quality, or strong reported results must be rendered
inside this source namespace. The site can say the paper reports those results. It must not say
that this repository has reproduced those results unless a separate project reproduction record
exists.

## Equations, Algorithms, Tables, And References

The MVP should preserve equations and algorithm blocks well enough for reading. If a LaTeX fragment
is too complex for clean automatic conversion, keep it as a fenced LaTeX block with an explicit
rendering status rather than silently dropping it.

References such as `Fig.~\ref{...}`, `Eq.~\ref{...}`, and citations should be preserved as text in
the first version. A later pass may resolve them into clickable cross-links.

Large tables in `additional_results.tex` can be imported as compact source-linked blocks for the
first version. The page should be structurally complete even when some appendix table rendering is
minimal.

## Figures

The first version displays all main-paper figures from:

```text
introduction.tex
method.tex
experiments.tex
conclusion.tex
```

Additional-results figures and large appendix galleries are represented by links or compact
empty-state panels in the MVP, then expanded after the main paper reading experience is stable.

Image assets should be copied or converted into:

```text
site/public/paper-assets/
```

PNG and JPG assets can be reused directly. PDF plots should be listed with source links first; a
later implementation pass may convert selected PDF plots to web-native images.

Asset import must use a resolver that handles extension inference and case-sensitive mismatches in
the LaTeX source. For example, a LaTeX reference such as `assets/Dungeon_level_coacd` must resolve
to the actual checked-in source file when the bundle contains a differently cased
`assets/Dungeon_Level_coacd.jpg`. Missing assets should produce a structured import warning, not a
silent broken image.

## Import Script

Add a script under `site/scripts/` that:

1. Reads `main.tex` and the included chapter files.
2. Extracts title, authors, abstract, sections, subsections, captions, figures, and natural
   paragraphs.
3. Generates MDX pages with stable IDs.
4. Keeps source file and source line metadata where practical.
5. Does not overwrite manually edited translations unless explicitly run in a refresh mode.
6. Emits structured warnings for unresolved images, complex tables, unresolved references, and
   skipped appendix galleries.

The first implementation may use conservative parsing rather than a full LaTeX AST. It should be
predictable and testable: section commands, paragraph boundaries, figure references, and captions
are the required extraction surface.

## Translation Workflow

The first version uses AI-assisted draft translation produced by Codex while reading the imported
paragraphs. It does not call an external translation API from the repository code.

Each translation block must preserve:

- source paragraph ID;
- English original;
- Chinese draft translation;
- translation status;
- source text hash;
- translation date;
- translating agent label;
- prompt policy label;
- optional reviewer note field;
- optional reviewed-by field for later manual review.

Translation text is content, not evidence. It must not be used to strengthen project claims.

## Reproduction Layer

The MVP includes the structure for reproduction notes without pretending they are complete.

Allowed initial statuses:

```text
not_started
planned
partial
out_of_scope
```

Use `partial` only where the current repository already has matching code and dated records. For
example, Eq.4-aligned objective accounting may link to the existing objective-report docs, while
full CPD reproduction remains outside the current evidence boundary.

Future reproduction cards may link to:

- `src/primitive_collision_compiler/...`
- `configs/experiments/...`
- `docs/records/...`
- `docs/reference/...`
- generated screenshots or figures

Every reproduction note must respect `docs/reference/claim-boundaries.md`.

## Claim Boundary

The site may claim:

```text
This is an authorized bilingual CPD paper companion and project reproduction map.
```

The site must not claim:

- full CPD paper reproduction;
- benchmark superiority;
- collision-quality validation;
- production compiler readiness;
- safety certification;
- human-reviewed translation before review records exist;
- that the Newton Primitive Collision Compiler implements the paper algorithm unless code and
  dated records support the specific section-level claim.

## Testing And Validation

The implementation should include:

- unit tests for the LaTeX import script;
- unit tests for asset resolution, including case-sensitive mismatch handling;
- tests that generated paragraph IDs are stable;
- tests that pages expose draft translation status;
- tests or validation that paper pages expose the source-namespace banner;
- claim validation covering site-authored text and site metadata, while treating source paper
  paragraphs as namespaced source content rather than project claims;
- docs validation remains passing;
- repository whitespace check remains passing;
- a static site build command that must pass before completion.

Expected verification commands:

```sh
python scripts/validate_docs.py
python -m pytest -q
git diff --check
cd site && npm run build
```

If the environment cannot install Node dependencies, the implementation must still verify Python
import-script tests and document the missing Node dependency as a setup gap.

## First Implementation Slice

The first implementation slice should produce a claim-safe scaffold and importer:

- the Astro site scaffold;
- core components and layout;
- importer tests;
- a generated paper index;
- permission/provenance record with private-permission status;
- source-namespace and draft-translation banners;
- asset resolver and import warnings;
- one generated sample section with English source and AI-assisted Chinese draft translations;
- one main-paper figure displayed or linked.

The second implementation slice should expand the same structure to the full paper text,
translations, main-paper figures, and appendix/additional-results linked route.

The slice is complete only when a local static build succeeds or the remaining blocker is a
documented missing local Node/npm dependency.
