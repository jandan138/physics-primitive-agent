# Documentation Index

Current status: this repository is a DeepDive application and project bootstrap for the Newton Primitive Collision Compiler. It now contains config dry-run reporting, USD asset-open smoke diagnostics, Newton source import diagnostics, local environment-readiness diagnostics, a geometry-only CPD-like face-merge primitive proposal smoke path, an opt-in CPD-like component-merge gate, an offline CPD-like objective report with structured Eq.4 alignment metadata, a synthetic objective comparison over deterministic toy meshes, a focused CPD-like cost-guided merge-search smoke over one deterministic toy mesh, a deterministic expected-failure synthetic workbench for known CPD-paper gaps, an opt-in offline `capped_cylinder` geometry proposal proxy, a contact-only Newton canary, and two named Newton task smokes: drop/settle and sphere-rain contact-density proxy. The clean local Newton Python environment has `smoke_passed` readiness evidence, and the capped bed USD smoke produces 32 restricted primitive proposals from 256 extracted triangles. The objective report summarizes primitive budget, volume proxy, raw Eq.4-like and AABB-normalized merge-excess accounting, assigned-point containment proxy, unsupported paper primitive gaps, component/fallback labels, and Eq.4 alignment metadata for that CPD-like output. The synthetic comparison reuses the same report on three in-memory fixtures to inspect topology-only versus component-merge accounting. The cost-guided smoke uses AABB-normalized merge-excess as a decision-making cost and reports old/new diagnostic accounting on `cost_guided_pair_choice`. The expected-failure workbench reports whether expected limitation flags are observed on three known-gap fixtures; `smoke_passed` means those expected limitations were reported, not that the decomposition succeeded. The capped-cylinder proxy has a named offline objective-report smoke where the unsupported paper primitive gap decreases from 3 to 2, with `frustum` and `trapezoidal_prism` still unsupported. The contact canary maps the historical 32 bed proposals to Newton box descriptors and produces one representative box contact; Newton mapping for `capped_cylinder` remains unsupported. The drop/settle smoke maps the historical 32 proposals, drops the compound package on a static plane, and records contact, final-speed, and support-height metrics. The sphere-rain smoke maps the historical 32 proposals as a static package, drops 9 probe spheres, and records package-probe contact-density proxy metrics. The Newton-native primitive bundle maps and constructs diagnostic shapes for a synthetic package containing `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`, with clean-env contact, drop/settle, and sphere-rain smokes passing under the dated native-bundle record. The opt-in Newton-native fitting comparison now lets the CPD-like fitter choose simple `cylinder`, `cone`, and `ellipsoid` proposals on three deterministic synthetic meshes and declares bed plus Franka as the next real-USD scope. A separate Franka/simple robot USD smoke opens the local Franka asset and runs capped first-mesh CPD-like geometry smoke. The component-merge gate reports merge policy, component counts, virtual merge attempts, and normalized excess-volume accounting while remaining below full CPD reproduction. It does not yet contain benchmark results, full CPD paper reproduction, broad asset/task evidence, whole-robot collider-quality evidence, real contact-stress measurement, or LLM/VLM research code.

Current next action: run the old/new native-fitting comparison on capped bed and capped Franka USD
meshes under explicit face caps, then use Newton contact canary before broader drop/settle or
sphere-rain task smokes. Keep `capped_cylinder`, `frustum`, and `trapezoidal_prism` in the
offline paper-alignment lane until separate mapping and diagnostic records exist.

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
- [CPD paper story status](reference/cpd-paper-story-status.md):
  plain-language map from the paper's reproduction story to the repository's current workbench
  status and next slices.
- [CPD objective report alignment](reference/cpd-objective-report-alignment.md):
  plain-language boundary between design-aligned surrogate objective accounting and a
  paper-faithful CPD objective implementation.
- [Newton-native primitive bundle explainer](reference/newton-native-primitive-bundle-explainer.md):
  plain-language explanation of what the latest `cylinder`/`cone`/`ellipsoid` runtime diagnostic
  bundle adds to the CPD paper story, and what it does not claim.
- [Newton-native fitting comparison](reference/newton-native-fitting-comparison.md):
  plain-language explanation of the opt-in synthetic comparison where simple native fitters emit
  `cylinder`, `cone`, and `ellipsoid`, while bed and Franka remain next-scope real USD assets.

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
- [Newton sphere-rain record](records/2026-05-15-newton-sphere-rain.md):
  second named task-level Newton smoke diagnostic using a contact-density proxy over the capped
  bed CPD-like collision package.
- [Franka CPD-like smoke record](records/2026-05-15-franka-cpd-like-smoke.md):
  Franka/simple robot USD-open and capped geometry-only CPD-like smoke evidence.
- [CPD-like component-merge gate record](records/2026-05-15-cpd-like-component-merge-gate.md):
  opt-in disconnected-component merge gate and merge-cost reporting evidence.
- [CPD-like objective report record](records/2026-05-15-cpd-like-objective-report.md):
  offline paper-aligned surrogate objective report evidence for the capped bed CPD-like baseline.
- [CPD-like synthetic comparison record](records/2026-05-15-cpd-like-synthetic-comparison.md):
  command-only deterministic synthetic objective comparison for topology-only versus
  component-merge accounting.
- [CPD-like cost-guided merge record](records/2026-05-15-cpd-like-cost-guided-merge.md):
  focused cost-guided merge-search smoke over one deterministic synthetic fixture.
- [CPD synthetic expected-failure workbench record](records/2026-05-15-cpd-synthetic-expected-failure-workbench.md):
  command-only deterministic expected-failure workbench that reports known CPD-paper gaps as
  diagnostic flags.
- [CPD expected-failure master verification record](records/2026-05-15-cpd-expected-failure-master-verification.md):
  post-merge master verification for the expected-failure workbench slice.
- [CPD capped-cylinder proxy record](records/2026-05-15-cpd-capped-cylinder-proxy.md):
  opt-in offline capped-cylinder geometry proposal proxy and reduced unsupported paper primitive
  gap evidence.
- [CPD capped-cylinder master verification record](records/2026-05-15-cpd-capped-cylinder-master-verification.md):
  post-merge master verification for the capped-cylinder proxy slice.
- [Big Goal 1 completion audit](records/2026-05-15-big-goal-1-completion-audit.md):
  completion audit for the minimal CPD-like diagnostic workbench goal.
- [Newton-native primitive policy record](records/2026-05-15-newton-native-primitive-policy.md):
  policy update that makes runtime primitive expansion Newton-native first.
- [Newton native primitive bundle record](records/2026-05-15-newton-native-primitive-bundle.md):
  mapping, builder dispatch, bounds, and clean-env synthetic smoke evidence for `cylinder`,
  `cone`, and `ellipsoid`.
- [Newton native bundle explainer docs record](records/2026-05-15-newton-native-bundle-explainer-docs.md):
  documentation update that explains the latest native runtime bundle in the CPD paper story.
- [Newton native fitting comparison record](records/2026-05-15-newton-native-fitting-comparison.md):
  opt-in synthetic native fitting comparison and bed/Franka next-scope declaration.
- [CPD objective alignment and next steps record](records/2026-05-15-cpd-objective-alignment-and-next-steps.md):
  documentation update that clarifies objective-report paper alignment and the next algorithmic
  slices.
- [Three-slice final verification record](records/2026-05-15-three-slice-final-verification.md):
  final verification for sphere-rain, Franka smoke, and component-merge gate.
- [CPD paper story status docs record](records/2026-05-15-cpd-paper-story-status-docs.md):
  documentation update that clarifies where the repository sits in the full CPD paper story.
- [CPD cost-guided story explainer record](records/2026-05-15-cpd-cost-guided-story-explainer.md):
  documentation update that explains the cost-guided merge smoke as the first restricted
  objective-guided decision hook in the CPD paper story.
- [AABB-normalized merge-excess explainer record](records/2026-05-15-aabb-normalized-merge-excess-explainer.md):
  documentation update that explains the merge-excess surrogate cost used by the CPD-like
  cost-guided smoke.
- [CPD Eq.4 alignment metadata record](records/2026-05-15-cpd-eq4-alignment-metadata.md):
  structured metadata update mapping current surrogate merge-excess terms to the CPD paper Eq.4
  role without claiming Eq.4 implementation.
- [Bootstrap plan](superpowers/plans/2026-05-14-deepdive-first-repo-bootstrap.md): implementation checklist.
- [Bootstrap design](superpowers/specs/2026-05-14-deepdive-first-repo-bootstrap-design.md): original design rationale.
- [Environment normalization design](superpowers/specs/2026-05-14-environment-normalization-design.md):
  Phase 1 environment-readiness scope and claim boundary.
- [Environment normalization plan](superpowers/plans/2026-05-14-environment-normalization.md):
  TDD implementation plan for the readiness checker and docs.
- [Newton-native primitive policy design](superpowers/specs/2026-05-15-newton-native-primitive-policy-design.md):
  design decision that separates the Newton-native runtime lane from the CPD paper-alignment
  offline lane.
- [Newton native primitive bundle plan](superpowers/plans/2026-05-15-newton-native-primitive-bundle.md):
  TDD implementation plan for the native `cylinder`, `cone`, and `ellipsoid` runtime bundle.
- [Newton native fitting comparison plan](superpowers/plans/2026-05-15-newton-native-fitting-comparison.md):
  TDD implementation plan for the opt-in native fitting comparison and bed/Franka scope update.

## Configs And Artifacts

- `configs/deepdive/mvp.yaml`: DeepDive-facing dry-run MVP config.
- `configs/experiments/phase0_baseline.yaml`: Phase 0 proof-point config scaffold.
- `configs/experiments/cpd_like_component_merge_gate.yaml`: opt-in CPD-like component-merge gate
  smoke config.
- `configs/experiments/cpd_like_objective_report.yaml`: offline CPD-like objective report smoke
  config.
- `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`: opt-in offline capped-cylinder
  proxy objective-report smoke config.
- `configs/experiments/newton_native_fitting_comparison.yaml`: opt-in synthetic native fitting
  comparison config that includes bed and Franka as next-scope real USD roles.
- `npc-compile --run-cpd-like-synthetic-comparison`: command-only deterministic synthetic
  objective comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-cost-guided-synthetic-comparison`: command-only deterministic
  cost-guided synthetic comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-expected-failure-workbench`: command-only deterministic
  expected-failure synthetic workbench, recorded in `experiments/registry.yaml` without a config
  file.
- `npc-compile --config configs/experiments/newton_native_fitting_comparison.yaml
  --run-newton-native-fitting-comparison`: deterministic synthetic old/new comparison for opt-in
  native `cylinder`, `cone`, and `ellipsoid` fitters, with bed and Franka listed as next-scope
  real USD roles.
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
and sphere-rain diagnostics can run two named task smokes for the capped bed CPD-like collision
package. The Franka/simple robot smoke can open a second asset class and run capped first-mesh
geometry-only proposals. The CPD-like component-merge gate can report disconnected-component
merge candidates and normalized excess-volume accounting. The offline CPD-like objective report
can summarize paper-aligned surrogate terms and Eq.4 alignment metadata for that baseline. The
synthetic objective comparison can inspect deterministic topology-only versus component-merge
accounting on toy meshes. The cost-guided merge-search smoke can inspect one old/new surrogate-cost
decision on a toy mesh. The expected-failure synthetic workbench can report whether expected
limitation flags are observed for known CPD-paper gaps; its `smoke_passed` status means expected
limitations were reported, not decomposition success. The capped-cylinder proxy can report an
opt-in offline objective smoke where the unsupported paper primitive gap decreases from 3 to 2,
with no Newton mapping or task-level improvement claim.
The runtime primitive roadmap is Newton-native first: the native `cylinder`, `cone`, and
`ellipsoid` bundle now has mapping, diagnostic construction, tests, and a dated synthetic runtime
smoke record. The opt-in native fitting comparison can emit those kinds on three deterministic
synthetic meshes, but this does not mean they are default asset behavior or real-USD improvement
evidence. It does not add support for paper-only `capped_cylinder`, `frustum`, or
`trapezoidal_prism` in Newton runtime.
These evidence layers are not benchmark, collision-quality, whole-robot quality, real
contact-stress, or CPD reproduction evidence.

Current non-goals: no safety guarantee, no real-world transfer claim, no deployment readiness claim, no benchmark superiority claim, no CPD reproduction claim, and no complete replacement of convex decomposition.
