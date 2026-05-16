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
offline paper-lane audit over `paper_single_box`, `paper_two_face_merge`,
`paper_three_face_chain`, `paper_disconnected_components`, `paper_component_pair_threshold_blocked`,
`paper_tiny_sphere_clamp`, `paper_duplicate_vertex_preprocessing`, `paper_frustum_like`,
`paper_trapezoid_prism_like`, `paper_nested_primitive`,
`paper_quad_face_intake`, and `paper_polygon_face_intake`. It records paper operator,
primitive-fit subset, left/right/merged merge-cost inputs, offline paper-shaped OBB/sphere fit
audit rows, an offline paper-shaped capsule axis audit row, offline-only flat
capped-cylinder/frustum/trapezoidal-prism candidate rows,
base-collapse-cost versus weighted-priority-cost fields, a topology-only priority-queue trace with
eager stale pruning, a threshold-disabled component-pair insertion trace, a finite-threshold
component-pair blocked trace, an explicit identity-axis OBB enclosed-primitive postprocess cull
audit, a fan-triangulated quad/polygon source-face intake policy audit, and an exact-coordinate
duplicate-vertex preprocessing audit while keeping Newton, bed/Franka, package generation, and
benchmark work out of scope. The audited primitive rows, postprocess cull, intake policy, and
duplicate-vertex preprocessing fixture are fixture-scoped audit data, not a full decomposition. It
now also records `paper_faithful_offline_scope_audit`, a criteria table that keeps the lane
`partial`, leaves `paper_faithful_offline_supported: false`, and previously advanced the
scope-audit gate to
`paper_fixture_breadth_expansion_plan`.
The fixture-breadth Batch A source/preprocess/intake/operator slice is now implemented with
`paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, and
`paper_concave_polygon_rejected`, while keeping the report partial and advancing the next
required gate to `paper_fixture_breadth_batch_b`. Batch B primitive-fit breadth is now also
implemented with synthetic offline fixtures for OBB, sphere, capsule, capped cylinder, frustum,
and trapezoidal prism. Batch B previously advanced the next required gate to
`paper_fixture_breadth_batch_c`; Batch C cost/search/stop breadth is now implemented with synthetic
offline fixtures for weighted-priority ordering, deterministic queue tie/eager-stale-prune
behavior, and one positive finite component-pair threshold block. Batch D component-pair breadth is
now implemented with multi-candidate component-pair ordering and deterministic capped skipped-pair
accounting. Batch E postprocess breadth is now implemented with rotated nested OBB containment and
explicit cross-type unsupported no-cull accounting. The command-only synthetic fixture-breadth
completion review for planned Batches A-E is now also implemented, while keeping the report
partial and keeping `paper_faithful_offline_supported: false`. Its nested review payload records
the planning-only `paper_faithful_offline_generalization_plan` as the follow-up gate for that
closed review. The report now also includes a command-only planning table for offline CPD
paper-lane generalization beyond named toy fixtures. That table closes only the planning gate,
keeps the report partial, keeps
`paper_faithful_offline_supported: false`, and advances the next required gate to
`paper_generalization_batch_a_source_policy`. This review and planning table are not
`paper_faithful_offline` support, and they are not a capped bed/Franka rerun unless a separate real
package change is introduced and passes full mapping, contact-canary, task-gate, and dated-record
gates. The
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
- [CPD paper fixture-breadth expansion plan](reference/cpd-paper-fixture-breadth-expansion-plan.md):
  documentation-only plan that maps the nine blocking scope-audit rows to future synthetic
  fixture batches; Batch A, Batch B, Batch C, Batch D, and Batch E are now implemented and
  the completion review is now implemented.
- [CPD paper faithful offline generalization plan](reference/cpd-paper-faithful-offline-lane-spec.md):
  command-only planning table for offline generalization beyond named toy fixtures. The next gate
  is `paper_generalization_batch_a_source_policy`.
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
- [CPD paper flat capped-cylinder audit record](records/2026-05-16-cpd-paper-flat-capped-cylinder-audit.md):
  dated implementation record for the offline-only flat capped-cylinder fit-audit row in the
  partial `cpd_paper_offline_report`.
- [CPD paper capsule axis audit record](records/2026-05-16-cpd-paper-capsule-axis-audit.md):
  dated implementation record for the offline paper-shaped capsule axis fit-audit row in the
  partial `cpd_paper_offline_report`.
- [CPD paper priority-queue trace audit record](records/2026-05-16-cpd-paper-priority-queue-trace-audit.md):
  dated implementation record for the topology-only offline priority-queue trace audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper component-pair edge insertion record](records/2026-05-16-cpd-paper-component-pair-edge-insertion.md):
  dated implementation record for the threshold-disabled offline component-pair insertion audit in
  the partial `cpd_paper_offline_report`.
- [CPD paper component-pair threshold blocking record](records/2026-05-16-cpd-paper-component-pair-threshold-blocking.md):
  dated implementation record for the finite-threshold offline component-pair block audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper postprocess audit record](records/2026-05-16-cpd-paper-postprocess-audit.md):
  dated implementation record for the explicit offline enclosed-primitive postprocess cull audit in
  the partial `cpd_paper_offline_report`.
- [CPD paper polygon/quad intake policy record](records/2026-05-16-cpd-paper-polygon-quad-intake-policy.md):
  dated implementation record for the offline fan-triangulated quad and polygon source-face intake
  policy audit in the partial `cpd_paper_offline_report`.
- [CPD paper OBB/sphere fit-faithfulness record](records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md):
  dated implementation record for the offline paper-shaped OBB/sphere fit audit in the partial
  `cpd_paper_offline_report`.
- [CPD paper duplicate-vertex preprocessing record](records/2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md):
  dated implementation record for the exact-coordinate duplicate-vertex preprocessing audit in the
  partial `cpd_paper_offline_report`.
- [CPD paper faithful offline scope audit record](records/2026-05-16-cpd-paper-faithful-offline-scope-audit.md):
  dated implementation record for the offline scope-audit criteria table that keeps the lane
  partial and points the next gate to fixture-breadth expansion.
- [CPD paper fixture-breadth expansion plan record](records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md):
  dated documentation record for the offline-only synthetic fixture-breadth plan.
- [CPD paper fixture-breadth Batch A record](records/2026-05-16-cpd-paper-fixture-breadth-batch-a.md):
  dated implementation record for the source/preprocess/intake/operator fixture-breadth slice.
- [CPD paper fixture-breadth Batch B record](records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md):
  dated implementation record for the primitive-fit fixture-breadth slice.
- [CPD paper fixture-breadth Batch C record](records/2026-05-16-cpd-paper-fixture-breadth-batch-c.md):
  dated implementation record for the cost/search/stop fixture-breadth slice.
- [CPD paper fixture-breadth Batch D record](records/2026-05-16-cpd-paper-fixture-breadth-batch-d.md):
  dated implementation record for the component-pair fixture-breadth slice.
- [CPD paper fixture-breadth Batch E record](records/2026-05-16-cpd-paper-fixture-breadth-batch-e.md):
  dated implementation record for the postprocess fixture-breadth slice.
- [CPD paper fixture-breadth completion review record](records/2026-05-16-cpd-paper-fixture-breadth-completion-review.md):
  dated implementation record for the command-only synthetic completion review over planned
  Batches A-E.
- [CPD paper faithful offline generalization plan record](records/2026-05-16-cpd-paper-faithful-offline-generalization-plan.md):
  dated implementation record for the command-only planning table beyond named toy fixtures.
- [Paper reader chrome and permission validator record](records/2026-05-16-paper-reader-chrome-and-permission-validator.md):
  reader-facing CPD paper companion cleanup that removes internal review chrome and tightens paper
  asset permission-evidence validation without changing reproduction or benchmark evidence.

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
- [CPD paper fixture-breadth expansion plan](reference/cpd-paper-fixture-breadth-expansion-plan.md):
  offline-only planning artifact that maps the current scope-audit blockers to the next planned
  synthetic fixture batches.
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
- [CPD paper flat capped-cylinder audit record](records/2026-05-16-cpd-paper-flat-capped-cylinder-audit.md):
  partial command-only offline fit-audit row expansion for paper flat capped cylinders, without
  Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper capsule axis audit record](records/2026-05-16-cpd-paper-capsule-axis-audit.md):
  partial command-only offline fit-audit row expansion for paper-shaped capsule axis candidates,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [CPD paper priority-queue trace audit record](records/2026-05-16-cpd-paper-priority-queue-trace-audit.md):
  partial command-only offline topology priority-queue trace audit with stale-pruning records,
  without Newton, real-USD, package, benchmark, or collision-quality claims.
- [Paper reference numbering fix record](records/2026-05-16-paper-reference-numbering-fix.md):
  reader-facing CPD paper companion import fix that resolves internal source references into paper
  numbers and does not change reproduction or benchmark evidence.
- [Paper reader chrome and permission validator record](records/2026-05-16-paper-reader-chrome-and-permission-validator.md):
  reader-facing CPD paper companion cleanup that removes internal review chrome and tightens paper
  asset permission-evidence validation without changing reproduction or benchmark evidence.
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
  `paper_single_box`, `paper_two_face_merge`, `paper_three_face_chain`,
  `paper_disconnected_components`, `paper_component_pair_threshold_blocked`,
  `paper_tiny_sphere_clamp`, `paper_duplicate_vertex_preprocessing`, `paper_frustum_like`,
  `paper_trapezoid_prism_like`, `paper_nested_primitive`, `paper_quad_face_intake`, and
  `paper_polygon_face_intake`; exits successfully when the JSON report is emitted, returns
  `status: partial`, records offline paper-shaped OBB/sphere rows, an offline paper-shaped capsule
  axis row, offline-only flat capped-cylinder/frustum/trapezoidal-prism rows, topology-only
  priority-queue trace fields, a threshold-disabled component-pair insertion trace, a
  finite-threshold component-pair blocked trace, one explicit enclosed-primitive postprocess cull
  audit, one quad plus one five-vertex polygon intake policy audit, and one exact-coordinate
  duplicate-vertex preprocessing audit, Batch A fixture-breadth source/preprocess/intake/operator
  cases, Batch B primitive-fit breadth cases for all six paper primitive names, Batch C
  cost/search/stop breadth cases for weighted-priority ordering, equal-cost queue
  tie/eager-stale-prune behavior, and one positive finite component-pair threshold block, plus
  Batch D component-pair breadth cases for multi-candidate ordering and capped skipped-pair
  accounting, plus Batch E postprocess breadth cases for rotated nested OBB containment and
  explicit cross-type unsupported no-cull accounting, plus a fixture-breadth completion review
  that closes only the planned synthetic Batch A-E breadth gate, plus a command-only
  generalization planning table that closes only the planning gate. It also records a scope-audit
  table with `decision: remain_partial`, reports
  `next_required_gate: paper_generalization_batch_a_source_policy`, keeps
  `paper_faithful_offline_supported: false`, and does not run Newton, real USD, package
  generation, or benchmarks.
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
