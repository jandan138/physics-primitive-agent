# Newton Primitive Collision Compiler — Paper Workspace

Multi-venue LaTeX structure migrated from the `genesis-llm` paper workflow. **ACCV** is the
active submission-readiness candidate for the simulation-checked primitive collider compiler story. **arXiv**,
**ECCV**, and **NeurIPS** are transfer-candidate wrappers that share manuscript sections and
evidence registries.

## Layout

```text
paper/
  shared/                 # Cross-venue sections, figures, tables, references, evidence registries
  venues/accv/            # ACCV primary wrapper (Springer LNCS)
  venues/arxiv/           # arXiv transfer-candidate wrapper
  venues/eccv/            # ECCV transfer-candidate wrapper
  venues/neurips/         # NeurIPS transfer-candidate wrapper
```

## Build

```bash
cd paper && make list
cd paper && make accv          # primary submission candidate
cd paper && make check-template-accv
cd paper && make all           # every venue (fails clearly if a template is missing)
cd paper && make template-check # all venue template check, including transfer candidates
cd paper && make clean
```

Venue wrappers use `\bibliography{references}`. The shared bibliography is resolved by each
venue's `.latexmkrc` and the Makefile fallback, which set `BIBINPUTS` to `paper/shared/`; do not
encode `../../shared/` inside `\bibliography{...}`, because BibTeX may run from the venue
`build/` directory.

## Override Rule

Venue `main.tex` files explicitly choose shared or local sections. Shared inputs look like
`\input{../../shared/sections/method}`. A local override uses `\input{sections/method}` and must
be recorded in that venue's `STATUS.md`.

## Template Status

| Venue | Template source | Expected class | Readiness intent |
| --- | --- | --- | --- |
| accv | committed official ACCV 2026 template files | `accv.sty`, `accvabbrv.sty`, `llncs.cls`, `splncs04.bst` | submission-readiness candidate |
| arxiv | standard article | `article` | transfer-preparation |
| eccv | official ECCV class from TeX Live or committed file | `eccv.sty` + `eccvabbrv.bst` | transfer-preparation |
| neurips | copied NeurIPS 2026 style in repo | `neurips_2026.sty` | transfer-preparation |

Each venue records template provenance in `venues/<venue>/STATUS.md`.

## Evidence Rules

Claims and result provenance live under `shared/evidence/`. Any change to quantitative results,
figure values, table values, seed reporting, or venue-specific scientific claims must update
`claims.yaml` and, when applicable, `results_manifest.yaml` in the same change. Dated runtime
evidence remains canonical in `docs/records/`; the paper registry links to those records rather
than duplicating full logs.

## ACCV Visual Expansion Status

The active ACCV candidate is a 14-page submission-readiness draft for the scoped
simulation-checked diagnostic story. The visual expansion pass has been implemented with
deterministic Phase 0 figures, an AI-slot Fig. 1 protocol schematic, and ACCV main-PDF references
kept separate from appendix material.

The current figure set is evidence-first:

- deterministic Phase 0 asset and primitive-package overlay figures;
- diagnostic collision-probe scene panels for bowl, cup, tray, and Franka task smoke cases;
- a Phase 0 accept/failure/fallback outcome matrix;
- a capped bed/Franka mechanism diagnostic figure;
- a Franka link-aware generated-package consumption figure;
- an AI-slot Fig. 1 protocol schematic whose generated visuals are exposition only, not
  experimental evidence.

Use `docs/records/2026-05-26-accv-paper-visual-expansion-plan.md` and later dated records as the
source of truth for page-budget, figure-scope, artifact, and claim-boundary rules. Do not commit
raw USD assets, large generated render directories, videos, or logs; commit only small paper
figures, manifests, and reproducible scripts when needed.

## Claim Boundary

Paper sources must stay consistent with `docs/reference/claim-boundaries.md` and
`docs/deepdive/evidence-status.md`. Use scoped wording such as ``simulation-checked'',
``capped package smoke'', ``collision-only microbenchmark'', and ``diagnostic checker'' unless a
dated record supports a stronger claim.
