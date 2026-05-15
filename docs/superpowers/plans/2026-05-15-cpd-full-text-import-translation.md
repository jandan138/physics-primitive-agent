# CPD Full Text Import And Translation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a claim-bounded full-paper CPD companion slice with complete source-paper prose import, AI-assisted draft Chinese translation scaffolding, and gated figure/reproduction placeholders.

**Architecture:** Keep full-paper content under `site/src/content/paper/` and render every imported prose/caption block through `PaperBlock`. Preserve equations, algorithms, tables, and figures as source-paper LaTeX blocks, while preventing paper figures from being published until permission evidence is attached. Keep all reproduction states `not_started` unless a dated record is linked.

**Tech Stack:** Python LaTeX importer, MDX, Astro components, pytest, `scripts/validate_site_claims.py`, Astro static build.

---

## Tasks

- [ ] Upgrade `site/scripts/import_cpd_paper.py` so it imports `main.tex` abstract, body section files, paragraph/caption blocks, and raw LaTeX environment blocks without treating table rows or algorithm lines as translatable prose.
- [ ] Add importer tests for full-paper section ordering, abstract inclusion, caption extraction, raw LaTeX block preservation, and stable `not_started` reproduction status.
- [ ] Generate `site/src/content/paper/*.mdx` for all paper sections from the CPD source tree using stable IDs and draft translation metadata.
- [ ] Fill AI-assisted Chinese draft translations for imported prose/caption blocks; keep raw equations/tables/algorithms as source-paper LaTeX blocks with untranslated source preservation.
- [ ] Add gated figure/reproduction placeholder rendering and validation so source-paper assets and reproduction claims cannot appear before permission/evidence records exist.
- [ ] Verify with focused tests, full tests, docs validation, site claim validation, npm audit, and Astro build.
