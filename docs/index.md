# Documentation Index

Current status: this repository is a DeepDive application and project bootstrap for the Newton Primitive Collision Compiler. It now contains config dry-run reporting, USD asset-open smoke diagnostics, repo-local ignored asset mirror materialization for the current bed/Franka smoke USDs, Newton source import diagnostics, local environment-readiness diagnostics, a geometry-only CPD-like face-merge primitive proposal smoke path, an opt-in CPD-like component-merge gate, an offline CPD-like objective report with structured Eq.4 alignment metadata, synthetic objective and expected-limitation workbenches, an opt-in offline `capped_cylinder` proxy, Newton contact canaries, and named Newton task smokes. The Newton-native primitive bundle maps and constructs diagnostic shapes for `box`, `sphere`, `capsule`, `cylinder`, `cone`, and `ellipsoid`, with clean-env contact, drop/settle, and sphere-rain smokes passing under the dated native-bundle record. The opt-in Newton-native fitting comparison chooses `cylinder`, `cone`, and `ellipsoid` on deterministic synthetic meshes and now includes candidate weighted-volume audit tables with explicit one-primitive fixture scope guards plus a squat-cylinder fixture for the controlled cylinder-axis search. The real-USD bed/Franka native probe comparison now runs capped bed and capped Franka first-mesh old/new lanes through offline reports, per-selected-cluster candidate audit and candidate-loss diagnosis summaries with next-slice triage metadata, contact canaries, and gated task smokes; bed and capped Franka both select boxes in the current support-aware lanes, while three capped Franka cheaper raw-cost cylinder candidates are reported as support-blocked. This is selection/accounting evidence rather than native primitive quality evidence. It does not yet contain benchmark results, full CPD paper reproduction, broad asset/task evidence, whole-robot collider-quality evidence, real contact-stress measurement, or LLM/VLM research code.

Current next action: the explicitly opt-in synthetic Newton task-smoke probe over the
lookahead-changed package pair is complete under recorded settings. The next step is not a capped
bed/Franka rerun unless a separate real package change is introduced and passes full mapping,
contact-canary, task-gate, and dated-record gates. The
completed cylinder branch remains useful context: the `cylinder_near_miss_cluster` fixture,
near-miss workbench, fit-ablation report, scoring-sensitivity report, report-only scoring-policy
ablation, and boxy guardrail extension show how synthetic changes are gated before broader runs.
The fit-ablation report shows this fixture cannot be flipped by radial-center refinement while
preserving containment; the sensitivity report quantifies the counterfactual cylinder scoring
change required to tie box; the report-only policy ablation applies a fixed hypothetical
multiplier only inside the synthetic report; and the boxy guardrail remains `box` under the same
multiplier. The synthetic offline opt-in
scoring-policy selection probe now routes the same multiplier through an explicit synthetic
candidate-selection path, flipping the near-miss but not the boxy guardrail. The explicit
synthetic package probe now pushes that opt-in choice through `decompose_mesh` into a changed
synthetic `CollisionPackage` and records a Newton shape-mapping summary only, while the default
package path and the boxy guardrail stay unchanged. It does not run Newton contact or task
diagnostics. The synthetic Newton probe now runs named contact, drop/settle, and sphere-rain task
smokes over the changed near-miss package pair only, with default package generation and all
real-USD packages unchanged. The controlled merge-search package probe now carries the existing
cost-guided toy merge/search behavior difference into synthetic `CollisionPackage` and Newton
shape-mapping accounting. The controlled merge-search Newton probe then runs named contact,
drop/settle, and sphere-rain task smokes over that changed synthetic package pair only. The
bounded synthetic `two_step_lookahead` diagnostic, follow-on package/mapping probe, follow-on
synthetic Newton task-smoke probe, and command-only four-block slice report for the
lookahead-changed package pair are now complete under recorded settings. The first
fixture-scoped `cpd_paper_offline_report` slice is now implemented as a command-only partial
offline paper-lane audit over `paper_single_box`, `paper_two_face_merge`, `paper_frustum_like`, and
`paper_trapezoid_prism_like`. It records paper operator, primitive-fit subset,
left/right/merged merge-cost inputs, offline-only frustum/trapezoidal-prism candidate rows, and
base-collapse-cost versus weighted-priority-cost fields while keeping Newton, bed/Franka, and
benchmark work out of scope. The audited primitive rows are explicitly current surrogate/proxy or
offline-only audit rows, not paper-faithful fitting. The next paper-lane gate is paper-flat
capped-cylinder fitting, not a capped bed/Franka rerun unless a separate real package change is
introduced and passes full mapping, contact-canary, task-gate, and dated-record gates. The
low-support branch is now guarded by support-aware admissibility, but that is still not
collision-quality evidence. Keep `capped_cylinder`, `frustum`, and
`trapezoidal_prism` in the offline paper-alignment lane until separate mapping and diagnostic
records exist.

## Current CPD Paper Plan

- [CPD paper reproduction gap matrix](reference/cpd-paper-reproduction-gap-matrix.md): current
  paper requirements versus repository surrogates, with Newton runtime boundaries.
- [CPD paper-faithful offline lane spec](reference/cpd-paper-faithful-offline-lane-spec.md):
  planned fixture-scoped offline lane for paper mechanics before real USD, Newton, or benchmark
  expansion.
- [Claim Boundaries](reference/claim-boundaries.md): current allowed wording and the boundary for
  the planned `paper_faithful_offline` status.
- [CPD paper gap matrix and offline lane spec record](records/2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md):
  dated record for this planning update and review status.
- [CPD paper offline first fixture slice record](records/2026-05-16-cpd-paper-offline-first-fixture-slice.md):
  dated implementation record for the partial `cpd_paper_offline_report` over two synthetic toy
  fixtures, with no Newton, real-USD, benchmark, or collision-quality claim.
- [CPD paper frustum/trapezoid audit record](records/2026-05-16-cpd-paper-frustum-trapezoid-audit.md):
  dated implementation record for offline-only frustum and trapezoidal-prism fit-audit rows in the
  partial `cpd_paper_offline_report`.

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
- [CPD pipeline step-by-step explainer](reference/cpd-pipeline-step-by-step-explainer.md):
  plain-language guide to the difference between the CPD algorithm steps, the Newton workbench
  steps, and benchmark/evaluation claims.
- [CPD paper reproduction gap matrix](reference/cpd-paper-reproduction-gap-matrix.md):
  row-by-row audit of paper requirements, current repository artifacts, surrogate status,
  offline-first work, Newton runtime admissibility, and claim boundaries.
- [CPD paper-faithful offline lane spec](reference/cpd-paper-faithful-offline-lane-spec.md):
  offline-only specification for the planned fixture-scoped paper operator, primitive-fit,
  collapse-cost, search, and postprocessing lane before any real-USD, Newton, or benchmark
  expansion.
- [CPD objective report alignment](reference/cpd-objective-report-alignment.md):
  plain-language boundary between design-aligned surrogate objective accounting and a
  paper-faithful CPD objective implementation.
- [Newton-native primitive bundle explainer](reference/newton-native-primitive-bundle-explainer.md):
  plain-language explanation of what the latest `cylinder`/`cone`/`ellipsoid` runtime diagnostic
  bundle adds to the CPD paper story, and what it does not claim.
- [Newton-native fitting comparison](reference/newton-native-fitting-comparison.md):
  plain-language explanation of the opt-in synthetic comparison where simple native fitters emit
  `cylinder`, `cone`, and `ellipsoid`, now with candidate weighted-volume audit tables, with bed
  and Franka handled by the separate real-USD probe comparison.
- [Synthetic native selection audit explainer](reference/synthetic-native-selection-audit-explainer.md):
  field-by-field guide to the candidate weighted-volume table and its claim boundary in the CPD
  paper story.
- [Bed and Franka native fitting next steps](reference/bed-franka-native-fitting-next-steps.md):
  historical execution-order guide for the now-completed move from synthetic native fitting to
  real-USD old/new reports and then Newton contact/task smokes.
- [Bed and Franka native probe comparison](reference/bed-franka-native-probe-comparison.md):
  completed real-USD diagnostic-smoke guide for capped bed and capped Franka old/new fitting,
  contact, and gated task probes.
- [Real USD native probe in the CPD paper story](reference/real-usd-native-probe-paper-story-explainer.md):
  plain-language explanation of why the latest bed/Franka slice is a downstream diagnostic
  milestone, not native primitive improvement or full CPD reproduction evidence.
- [CPD latest diagnostic loop explainer](reference/cpd-latest-diagnostic-loop-explainer.md):
  plain-language explanation of the candidate-loss diagnosis, controlled cylinder-axis fitting
  update, synthetic checks, and bed/Franka Newton-gated rerun as one repeatable CPD workbench loop.
- [Asset mirror materialization](reference/asset-mirror-materialization.md):
  guide to the ignored repo-local USD mirrors for bed and Franka, including material/texture
  closure status and claim boundaries.
- [CPD next steps after real USD mirrors](reference/cpd-next-steps-after-real-usd-mirrors.md):
  plain-language roadmap for locking the current real-USD baseline, diagnosing why boxes still
  win, and making the next primitive-fitting or merge-search change safely.

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
- [Cost-guided merge step trace record](records/2026-05-16-cost-guided-merge-step-trace.md):
  synthetic offline merge-step trace diagnostic accounting for the existing cost-guided fixture.
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
  opt-in synthetic native fitting comparison and pointer to the bed/Franka probe scope.
- [Synthetic native selection audit record](records/2026-05-15-synthetic-native-selection-audit.md):
  candidate weighted-volume audit tables explaining why the six-kind native lane selects
  `cylinder`, `cone`, and `ellipsoid` on deterministic toy meshes.
- [Synthetic native selection audit explainer docs record](records/2026-05-15-synthetic-native-selection-audit-explainer-docs.md):
  documentation update with a field-by-field explanation of the candidate audit table.
- [Bed Franka native fitting next steps docs record](records/2026-05-15-bed-franka-native-fitting-next-steps-docs.md):
  documentation update that clarifies the next real-USD old/new comparison sequence.
- [Real USD native fitting comparison record](records/2026-05-15-real-usd-native-fitting-comparison.md):
  capped bed and capped Franka old/new offline diagnostic report evidence.
- [Real USD candidate audit record](records/2026-05-15-real-usd-candidate-audit.md):
  pre-cylinder-axis per-selected-cluster candidate accounting, superseded for current status by
  the candidate-loss/cylinder-axis record.
- [Real USD native contact comparison record](records/2026-05-15-real-usd-native-contact-comparison.md):
  capped bed and capped Franka old/new contact-canary evidence under the clean Newton conda
  environment.
- [Real USD native task comparison record](records/2026-05-15-real-usd-native-task-comparison.md):
  gated drop/settle and sphere-rain task-smoke evidence for the capped bed and capped Franka
  old/new packages.
- [Bed Franka native probe completion audit](records/2026-05-15-bed-franka-native-probe-completion-audit.md):
  final checklist mapping the requested five-step objective to code, configs, reports, records,
  verification, and review fixes.
- [Real USD native probe story explainer docs record](records/2026-05-15-real-usd-native-probe-story-explainer-docs.md):
  documentation update that explains the latest real-USD native probe slice in the CPD paper
  reproduction story.
- [Real USD asset mirror materialization record](records/2026-05-15-real-usd-asset-mirror-materialization.md):
  ignored repo-local mirror materialization for the current bed and Franka smoke USDs.
- [Real USD mirrors next steps docs record](records/2026-05-15-real-usd-mirrors-next-steps-docs.md):
  documentation update that expands the asset mirror norm and records the next CPD-like
  candidate-loss diagnosis sequence.
- [Candidate loss diagnosis and cylinder axis record](records/2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md):
  controlled cylinder-axis fitting update, synthetic rerun, real-USD candidate-loss diagnosis,
  and bed/Franka Newton-gated rerun.
- [Candidate loss triage record](records/2026-05-15-candidate-loss-triage.md):
  next-slice triage metadata for near-miss extension candidates and low-support native-extension
  selections in the real-USD candidate-loss diagnosis.
- [Low-support native extension admissibility record](records/2026-05-15-low-support-native-extension-admissibility.md):
  support-aware admissibility guard for low-support native-extension candidates, with current
  bed/Franka support-aware rerun and Newton diagnostic-gate evidence.
- [Cylinder near-miss cluster fixture record](records/2026-05-16-cylinder-near-miss-cluster-fixture.md):
  synthetic support-admissible cylinder near-miss fixture for the next primitive-fitting or
  merge/search slice.
- [Cylinder near-miss fit ablation record](records/2026-05-16-cylinder-near-miss-fit-ablation.md):
  synthetic lower-bound diagnostic showing this fixture cannot be flipped by radial-center
  refinement while preserving containment.
- [Cylinder near-miss scoring sensitivity record](records/2026-05-16-cylinder-near-miss-scoring-sensitivity.md):
  synthetic counterfactual scoring-sensitivity diagnostic for the same near-miss fixture, without
  applying a scoring-policy change.
- [Cylinder near-miss scoring policy ablation record](records/2026-05-16-cylinder-near-miss-scoring-policy-ablation.md):
  synthetic report-only scoring-policy ablation for the same near-miss fixture, without changing
  default selection or Newton packages.
- [Cylinder scoring policy guardrail record](records/2026-05-16-cylinder-scoring-policy-guardrail.md):
  synthetic boxy cuboid negative-control extension for the report-only scoring-policy ablation.
- [Cylinder scoring policy selection probe record](records/2026-05-16-cylinder-scoring-policy-selection-probe.md):
  synthetic offline opt-in scoring-policy selection probe where the near-miss flips and the boxy
  guardrail remains box, without changing default packages or Newton tasks.
- [Cylinder scoring policy package probe record](records/2026-05-16-cylinder-scoring-policy-package-probe.md):
  explicitly opt-in synthetic package probe where the near-miss package changes to `cylinder`,
  the boxy guardrail remains `box`, and a Newton shape-mapping summary is recorded without
  running Newton contact or task diagnostics.
- [Cylinder scoring policy Newton probe record](records/2026-05-16-cylinder-scoring-policy-newton-probe.md):
  explicitly opt-in synthetic Newton diagnostic over the changed near-miss package pair, with
  contact-gated drop/settle and sphere-rain task-smoke status under recorded settings.
- [Controlled merge-search package probe record](records/2026-05-16-controlled-merge-search-package-probe.md):
  command-only synthetic package-path probe that carries the existing cost-guided merge-search
  fixture into `CollisionPackage` and Newton shape-mapping accounting.
- [Controlled merge-search Newton probe record](records/2026-05-16-controlled-merge-search-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe over the changed controlled merge/search package
  pair.
- [Cost-guided lookahead merge record](records/2026-05-16-cost-guided-lookahead-merge.md):
  command-only synthetic two-step lookahead merge/search diagnostic over one deterministic trap
  fixture.
- [Cost-guided lookahead package probe record](records/2026-05-16-cost-guided-lookahead-package-probe.md):
  command-only synthetic package-path and Newton shape-mapping probe for the lookahead-changed
  toy package pair.
- [Cost-guided lookahead Newton probe record](records/2026-05-16-cost-guided-lookahead-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe for the lookahead-changed toy package pair.
- [Four-block slice report record](records/2026-05-16-four-block-slice-report.md):
  command-only evidence map for the recorded cost-guided lookahead synthetic slice across
  primitive fitting/selection, merge/search, offline diagnostics, and Newton task comparison. It
  links existing dated records and does not rerun source reports, USD loading, or Newton tasks.
- [Newton CPD workbench four-block status audit](records/2026-05-16-newton-cpd-workbench-four-block-status-audit.md):
  status map for primitive fitting/selection, merge/search, offline reports, and Newton task
  comparison, including current gaps and the recommended next slice.
- [Four-block workbench completion audit](records/2026-05-16-four-block-workbench-completion-audit.md):
  completion audit that maps the bounded four-block workbench objective to the report, CLI, tests,
  dated records, review fixes, and verification evidence.
- [CPD pipeline step-by-step explainer record](records/2026-05-16-cpd-pipeline-step-by-step-explainer.md):
  documentation update that explains the whole mesh-to-benchmark pipeline and where the current
  Newton workbench fits relative to the CPD paper algorithm.
- [CPD paper gap matrix and offline lane spec record](records/2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md):
  documentation update that turns the paper reproduction gap into an offline-first paper-lane
  spec, without adding benchmark, Newton runtime, real-USD, or collision-quality evidence.
- [CPD paper offline first fixture slice record](records/2026-05-16-cpd-paper-offline-first-fixture-slice.md):
  partial command-only offline paper-lane audit over `paper_single_box` and `paper_two_face_merge`,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper frustum/trapezoid audit record](records/2026-05-16-cpd-paper-frustum-trapezoid-audit.md):
  partial command-only offline fit-audit row expansion for `frustum` and `trapezoidal_prism`,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD latest diagnostic loop explainer docs record](records/2026-05-15-cpd-latest-diagnostic-loop-explainer-docs.md):
  documentation update that explains the latest candidate-loss and cylinder-axis slice as a
  repeatable diagnostic loop in the CPD paper story.
- [CPD paper companion MVP record](records/2026-05-15-cpd-paper-companion-mvp.md):
  Astro + MDX bilingual CPD paper companion scaffold with source-paper claim namespacing,
  permission-record-pending status, and AI-assisted draft translation status.
- [CPD full text import and translation record](records/2026-05-15-cpd-full-text-import-translation.md):
  full-section CPD companion import with AI-assisted draft translations, gated source LaTeX
  blocks, and `not_started` reproduction states.
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
- [Bed Franka native probe completion plan](superpowers/plans/2026-05-15-bed-franka-native-probe-completion.md):
  TDD implementation plan for the real-USD old/new fitting, contact, and gated task comparison
  slice.

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
  comparison config that points to the real-USD probe comparison config.
- `configs/experiments/bed_franka_native_probe_comparison.yaml`: real-USD capped bed and capped
  Franka old/new fitting, contact, and gated task-smoke comparison config.
- `configs/experiments/cylinder_scoring_policy_newton_probe.yaml`: explicitly opt-in synthetic
  near-miss package-pair Newton task-smoke config.
- `npc-compile --run-cpd-like-synthetic-comparison`: command-only deterministic synthetic
  objective comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-cost-guided-synthetic-comparison`: command-only deterministic
  cost-guided synthetic comparison, recorded in `experiments/registry.yaml` without a config file.
- `npc-compile --run-cpd-like-controlled-merge-search-package-probe`: command-only synthetic
  package-path probe for the existing cost-guided merge-search fixture, with Newton shape-mapping
  coverage and no contact/task execution.
- `npc-compile --config configs/experiments/controlled_merge_search_newton_probe.yaml
  --run-cpd-like-controlled-merge-search-newton-probe`: synthetic-only contact-gated Newton
  task-smoke comparison for the controlled merge-search default and opt-in packages.
- `npc-compile --run-cpd-like-cost-guided-lookahead-merge-report`: command-only synthetic
  two-step lookahead merge/search diagnostic over one trap fixture, with no package or Newton task
  execution.
- `npc-compile --run-cpd-like-cost-guided-lookahead-package-probe`: command-only synthetic
  package-path and Newton shape-mapping probe for the lookahead-changed toy package pair, with no
  contact/task execution.
- `npc-compile --config configs/experiments/cost_guided_lookahead_newton_probe.yaml
  --run-cpd-like-cost-guided-lookahead-newton-probe`: synthetic contact-gated Newton task-smoke
  probe for the lookahead-changed toy package pair.
- `npc-compile --run-cpd-like-four-block-slice-report`: command-only evidence map for the
  recorded lookahead slice. It links existing dated records and does not rerun source reports,
  USD loading, real assets, or Newton tasks.
- `npc-compile --run-cpd-paper-offline-report`: command-only partial offline paper-lane audit over
  `paper_single_box`, `paper_two_face_merge`, `paper_frustum_like`, and
  `paper_trapezoid_prism_like`; exits successfully when the JSON report is emitted, returns
  `status: partial`, and does not run Newton, real USD, package generation, or benchmarks.
- `npc-compile --run-cpd-like-expected-failure-workbench`: command-only deterministic
  expected-failure synthetic workbench, recorded in `experiments/registry.yaml` without a config
  file.
- `npc-compile --config configs/experiments/newton_native_fitting_comparison.yaml
  --run-newton-native-fitting-comparison`: deterministic synthetic old/new comparison for opt-in
  native `cylinder`, `cone`, and `ellipsoid` fitters, including candidate audit tables.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-fitting-comparison`: capped bed and capped Franka real-USD old/new
  offline diagnostic report with candidate audit summaries.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-contact-comparison`: full-mapping-gated contact canary comparison.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --run-real-usd-native-task-comparison`: contact-gated drop/settle and sphere-rain comparison.
- `npc-compile --config configs/experiments/cylinder_scoring_policy_newton_probe.yaml
  --run-cpd-like-cylinder-scoring-policy-newton-probe`: synthetic-only contact-gated Newton
  task-smoke comparison for the default `box` and opt-in `cylinder` near-miss packages.
- `npc-compile --config configs/experiments/bed_franka_native_probe_comparison.yaml
  --materialize-assets`: ignored repo-local USD dependency-closure mirror for the current bed and
  Franka smoke assets.
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
smoke record. The opt-in native fitting comparison can emit those kinds on deterministic synthetic
meshes, but this does not mean they are default asset behavior or real-USD improvement evidence.
The synthetic cylinder scoring-policy Newton probe can run contact-gated task smokes over one
explicitly opt-in changed near-miss package pair. The controlled merge-search package probe can
carry one synthetic merge/search behavior difference into package and mapping accounting without
running Newton tasks. The controlled merge-search Newton probe can run contact-gated task smokes
over that changed synthetic merge/search package pair, still without default merge-policy,
real-USD, collision-quality, benchmark, or CPD reproduction claims. The synthetic two-step
lookahead merge report can record one bounded offline merge/search decision change. The follow-on
lookahead package probe adds package-path and mapping accounting, and the completed lookahead
Newton probe adds synthetic contact-gated task-smoke status under recorded settings. These
lookahead probes still do not add real-USD, collision-quality, benchmark, or CPD reproduction
evidence. The real-USD bed/Franka probe
comparison can run old/new lanes through offline reports, candidate
diagnostics, contact canaries, and gated task smokes; the current support-aware run keeps bed and
capped Franka at boxes while reporting three capped Franka raw-cost cylinder candidates as
support-blocked accounting, but it still does not prove native primitive quality improvement. It
does not add support for paper-only
`capped_cylinder`, `frustum`, or `trapezoidal_prism` in Newton runtime.
These evidence layers are not benchmark, collision-quality, whole-robot quality, real
contact-stress, or CPD reproduction evidence.

Current non-goals: no safety guarantee, no real-world transfer claim, no deployment readiness claim, no benchmark superiority claim, no CPD reproduction claim, and no complete replacement of convex decomposition.
