# Agent Rules

## Project Context

This repository is a DeepDive-first bootstrap for the Newton Primitive Collision Compiler. The
current objective is an internal DeepDive application package for simulation-checked primitive
collider generation, not completed research or a production compiler.

The strategic frame is Physical Intelligence Center infrastructure: AI models that generate
assets, scenes, or robot behaviors need physical safety constraints. Physics engines are the
executable diagnostic layer for those constraints, and collision proxies are one of the critical
inputs to that layer. Primitive collider packages are candidates until Newton diagnostics check
body state, contact behavior, and robot-operation constraints.

## Priority Order

1. Preserve DeepDive application readiness.
2. Preserve claim boundaries from `docs/reference/claim-boundaries.md`.
3. Keep configs, records, and reports reproducible.
4. Keep executable code minimal until the 0-4 week proof point starts.

## Claim Boundary Rules

- Do not claim real compiler functionality until implementation and records exist.
- Do not claim benchmark superiority before benchmark reports exist.
- Do not claim deployment readiness, real-world transfer, or safety certification.
- Do not claim novelty in automatic primitive collider generation itself; CPD-style work is
  related work and a candidate generator/baseline.
- Do not claim whole-robot Franka or articulated robot performance before link-aware package and
  articulation-smoke records exist.
- Prefer "diagnostic checker" over formal-verification language in reviewer-facing docs.
- Prefer "simulation-checked" over stronger validation wording unless a verification standard is
  documented.
- Treat generated collision packages as safety-affecting artifacts that require review.

## Source And Documentation Rules

- Canonical DeepDive wording lives in `docs/deepdive/message-map.md`.
- Current evidence boundaries live in `docs/deepdive/evidence-status.md`.
- Rough source intake stays in `docs/tmp/` and is not canonical.
- Durable decisions and evidence changes need dated records under `docs/records/`.

## Artifact Policy

- Do not commit raw or generated 3D assets, large logs, videos, or run directories.
- Small manifests, configs, and Markdown summaries are commit-safe.
- Link large artifacts from records or reports by path/manifest instead of committing them.

## Config Policy

- Config examples live under `configs/`.
- DeepDive-facing MVP config: `configs/deepdive/mvp.yaml`.
- Phase 0 experiment config: `configs/experiments/phase0_baseline.yaml`.
- Do not hardcode experiment parameters in docs when a config should own them.

## Commands

- Install locally: `python -m pip install -e ".[dev]"`
- Run fast tests: `make test`
- Run CPD paper offline tests: `make test-paper`
- Validate before merge: `make validate-full`
- Validate docs and claims with fast tests: `make validate`
- Build paper (ACCV primary): `cd paper && make accv` or `cd paper && make all`
- Whitespace check: `git diff --check`

## Paper Workspace

Multi-venue LaTeX sources live under `paper/` (migrated from the `genesis-llm` workflow):

- `paper/shared/`: cross-venue sections, figures, bibliography, and evidence registries
- `paper/venues/accv/`: ACCV primary wrapper (LNCS)
- `paper/venues/{arxiv,eccv,neurips}/`: transfer-candidate wrappers

ACCV is the active draft venue. Quantitative claims in paper sources must stay aligned with
`paper/shared/evidence/claims.yaml`, `docs/reference/claim-boundaries.md`, and dated records under
`docs/records/`. The Astro site under `site/` is separate reviewer-facing material, not the LaTeX
build source of truth.
