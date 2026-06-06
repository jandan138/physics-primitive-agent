# ACCV Visual Wording Audit

Date: 2026-06-05

## Scope

The ACCV main paper, supplement, figure-source registry, and generated figure manifests were checked for reviewer-facing visual wording. The pass removes internal production terms from visible paper text and from compact figure provenance fields that may be inspected with the submission artifacts.

## Changes

- Main-paper Fig. 2 now explains the mechanism directly: isolated primitive passes, full package fails, scoped Franka package stays below the gate, and paired checks point to COM/inertia sensitivity.
- The main-paper discussion now uses a short evidence-scope paragraph: figures summarize package geometry, probe outcomes, body-state mechanisms, and link ownership, but do not add unrecorded runtime, benchmark, robot-operation, or safety-certification evidence.
- Supplement frontmatter, reviewer guide, visual atlas, and reproducibility notes now describe what each visual plate shows rather than how the plate was produced.
- Figure source registries and generated manifests use neutral `visual_composition` / `visual_panel` wording for compact provenance fields.

## Boundary

These edits do not change thresholds, results, source records, or experimental claims. They are wording and provenance-string changes only. Evidence remains limited to the dated records, configs, manifests, and reports cited by the paper.

## Verification Targets

- Build the ACCV main and supplement PDFs.
- Extract PDF text and search for the removed internal production terms.
- Run focused paper and figure tests.
- Run `git diff --check`.
