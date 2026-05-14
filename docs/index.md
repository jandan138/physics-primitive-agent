# Documentation Index

Current status: this repository is a DeepDive application and project bootstrap for the Newton Primitive Collision Compiler. It now contains config dry-run reporting, USD asset-open smoke diagnostics, Newton source import diagnostics, local environment-readiness diagnostics, a geometry-only CPD-like face-merge primitive proposal smoke path, a contact-only Newton canary, and the first named Newton drop/settle task smoke. The clean local Newton Python environment has `smoke_passed` readiness evidence, and the capped bed USD smoke produces 32 restricted primitive proposals from 256 extracted triangles. The contact canary maps those 32 proposals to Newton box descriptors and produces one representative box contact. The drop/settle smoke maps all 32 proposals, drops the compound package on a static plane, and records contact, final-speed, and support-height metrics. It does not yet contain benchmark results, full CPD paper reproduction, broad asset/task evidence, or LLM/VLM research code.

Current next action: review the drop/settle slice, then add one more narrow Newton diagnostic probe
or asset class while keeping fallback decisions and unsupported primitive types explicit.

## DeepDive Package

- [DeepDive README](deepdive/README.md): reviewer-facing navigation and editing rules.
- [Message Map](deepdive/message-map.md): canonical story, safe wording, unsafe claims, proof point, and support request.
- [Application Draft](deepdive/application.md): realistic DeepDive application text.
- [One-Page Summary](deepdive/one-page-summary.md): concise leadership and reviewer brief.
- [Pitch Outline](deepdive/pitch-outline.md): 20-30 minute talk structure.
- [Review Q&A](deepdive/review-qa.md): preparation for Taste, Benchmark, User Experience, and Value Delivering.
- [Evidence Status](deepdive/evidence-status.md): what is supported now, what is future evidence, and what must not be claimed.

## Design References

- [Project Scope](design/project-scope.md): project boundaries, current non-goals, and staged ambition.
- [System Architecture](design/system-architecture.md): intended compiler components and current skeleton status.
- [Research Roadmap](design/research-roadmap.md): Phase 0 through Phase 4 route.
- [Evaluation Plan](design/evaluation-plan.md): baselines, tasks, metrics, reporting, phase gates, and no-go criteria.
- [Benchmark Protocol](design/benchmark-protocol.md): asset categories, license policy, normalization, splits, task templates, and failure taxonomy.
- [CPD-like face-merge explainer](reference/cpd-like-face-merge-explainer.md):
  plain-language explanation of the current geometry-only baseline and why it is not a full CPD
  paper reproduction.

## Source Intake And Planning

- [Temporary source documents](tmp/): quarantined source intake used during bootstrap; not
  canonical reviewer-facing claims.
- [Environment readiness operations](operations/environment.md): local runtime contract, required
  variables, readiness command, status meanings, and artifact policy.
- [Clean Newton environment readiness record](records/2026-05-14-clean-newton-environment-readiness.md):
  current clean local Python/Newton environment readiness evidence.
- [Geometry-only CPD-like smoke record](records/2026-05-14-cpd-like-geometry-smoke-slice.md):
  capped bed USD primitive proposal smoke evidence.
- [CPD-like face-merge explainer record](records/2026-05-14-cpd-like-face-merge-explainer.md):
  documentation clarification for the current baseline's role in the CPD paper story.
- [Current CPD-like status and Newton probe next step](records/2026-05-14-current-cpd-like-status-and-newton-probe-next-step.md):
  separates environment readiness, geometry-only evidence, and the unimplemented Newton simulation
  probe layer.
- [Newton contact smoke record](records/2026-05-14-newton-contact-smoke.md):
  first contact-only Newton canary consuming CPD-like primitive proposals.
- [Newton drop/settle record](records/2026-05-14-newton-drop-settle.md):
  first named task-level Newton smoke diagnostic consuming the CPD-like collision package.
- [Bootstrap plan](superpowers/plans/2026-05-14-deepdive-first-repo-bootstrap.md): implementation checklist.
- [Bootstrap design](superpowers/specs/2026-05-14-deepdive-first-repo-bootstrap-design.md): original design rationale.
- [Environment normalization design](superpowers/specs/2026-05-14-environment-normalization-design.md):
  Phase 1 environment-readiness scope and claim boundary.
- [Environment normalization plan](superpowers/plans/2026-05-14-environment-normalization.md):
  TDD implementation plan for the readiness checker and docs.

## Configs And Artifacts

- `configs/deepdive/mvp.yaml`: DeepDive-facing dry-run MVP config.
- `configs/experiments/phase0_baseline.yaml`: Phase 0 proof-point config scaffold.
- `scripts/env/readiness_check.py`: local environment-readiness JSON checker.
- `experiments/registry.yaml`: experiment registry and claim-support status.
- `assets/`, `reports/`, and `archive/`: artifact boundaries; large/generated outputs stay out
  of git.
- `AGENTS.md`: repo-local rules for future agentic work.

## Claim Boundary

Safe current claim: proposal for primitive-first, Newton-checker-planned, fallback-aware collision asset compilation.

Additional current evidence: executable environment-readiness diagnostics can record dependency
gaps, source provenance, and the current clean local env `smoke_passed` status. The CPD-like
geometry path can produce a restricted primitive proposal smoke report. The Newton contact canary
can confirm representative primitive ingestion and contact pipeline output. The Newton drop/settle
diagnostic can run one named task smoke for the capped bed CPD-like collision package. These
evidence layers are not benchmark, broad collision-quality, or CPD reproduction evidence.

Current non-goals: no safety guarantee, no real-world transfer claim, no deployment readiness claim, no benchmark superiority claim, no CPD reproduction claim, and no complete replacement of convex decomposition.
