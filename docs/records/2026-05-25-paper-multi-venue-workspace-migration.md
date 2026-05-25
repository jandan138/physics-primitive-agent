# 2026-05-25 Paper Multi-Venue Workspace Migration

## Date

2026-05-25

## Status

Complete for repository layout, shared manuscript skeleton, evidence registries, and layout contract tests.
Not complete for ACCV camera-ready content, Phase 0 benchmark tables, or successful `make accv` on every machine.

## Decision

Migrate the `genesis-llm` multi-venue LaTeX workflow into this repository:

- `paper/shared/` holds cross-venue sections, bibliography, figure stubs, and evidence registries.
- `paper/venues/accv/` is the primary wrapper (LNCS / ACCV-facing).
- `paper/venues/{arxiv,eccv,neurips}/` are transfer-candidate wrappers.
- `make accv` builds the primary draft; `make all` attempts every venue.

## Genesis-LLM Pattern Preserved

- Explicit per-venue `main.tex` chooses shared vs local `\input{sections/...}` overrides.
- `STATUS.md` per venue records template provenance, readiness, overrides, and missing checks.
- `BIBINPUTS` points at `paper/shared/`; `\bibliography{references}` stays venue-local.
- `paper/shared/evidence/{claims.yaml,results_manifest.yaml}` links paper wording to `docs/records/`.
- `tests/test_paper_layout.py` guards the layout contract.

## Project-Specific Adaptation

- Primary venue is ACCV (not CGF/SIGGRAPH).
- Shared sections use simulation-checked primitive collider wording aligned with claim boundaries.
- Recorded metrics in `results_manifest.yaml` mirror 2026-05-22 bed/Franka and throughput records only.
- Phase 0 multi-asset and articulation claims remain `planned` in `claims.yaml`.

## Non-Goals

- Does not move `site/` MDX paper into LaTeX; site remains separate reviewer UI.
- Does not commit LaTeX build artifacts or submission ZIPs.
- Does not claim Phase 0 benchmark completion.

## Next Steps

1. Install `llncs.cls` (or commit vendor class) and run `cd paper && make accv`.
2. Fill Phase 0 table rows from `experiments/registry.yaml` and new records.
3. Add ECCV `eccv.sty` before `make eccv`.
4. Update `claims.yaml` whenever paper metrics or figures change.
