# Records

Records are durable dated notes for decisions, verification, failures, and evidence changes.
Every record should be short enough to read during review and concrete enough to reproduce the
state it describes.

## Record Template

```md
# YYYY-MM-DD Short Title

## Date

YYYY-MM-DD

## Status

Proposed | In progress | Complete | Failed | Superseded

## Changes

- What changed.

## Verification

- Commands run and exit status.

## Artifacts

- Paths to configs, reports, logs, or asset manifests.

## Claim Impact

- Claims now supported, unchanged, or explicitly not supported.

## Next Action

- The next concrete step.
```

## Rules

- Link claims to records before using them in DeepDive updates.
- Record failures and fallback decisions; do not only record successful runs.
- Keep large logs and generated artifacts outside git and link their manifest path instead.

## Current Record Index

- [2026-05-14 Project Bootstrap](2026-05-14-project-bootstrap.md): DeepDive-first repository
  bootstrap.
- [2026-05-14 CPD-Like Newton Source And Assets](2026-05-14-cpd-like-newton-source-and-assets.md):
  Newton source and initial asset choices.
- [2026-05-14 CPD-Like Newton Slice](2026-05-14-cpd-like-newton-slice.md): CPD-like
  planning slice.
- [2026-05-14 Newton USD Smoke](2026-05-14-newton-usd-smoke.md): USD asset-open smoke
  diagnostics.
- [2026-05-14 Environment Normalization](2026-05-14-environment-normalization.md): Phase 1
  environment-readiness checker, docs, and tests.
- [2026-05-14 Environment Readiness Master Verification](2026-05-14-environment-readiness-master-verification.md):
  post-merge `master` readiness status and verification evidence.
- [2026-05-14 Clean Newton Environment Readiness](2026-05-14-clean-newton-environment-readiness.md):
  clean external conda environment creation and `smoke_passed` readiness evidence.
- [2026-05-14 CPD-Like Geometry Smoke Slice](2026-05-14-cpd-like-geometry-smoke-slice.md): geometry-only
  CPD-like face-merge primitive proposal smoke evidence.
- [2026-05-14 CPD-Like Face-Merge Explainer](2026-05-14-cpd-like-face-merge-explainer.md):
  plain-language clarification of the current baseline and its CPD paper-story boundary.
- [2026-05-14 Current CPD-Like Status And Newton Probe Next Step](2026-05-14-current-cpd-like-status-and-newton-probe-next-step.md):
  separates clean environment readiness, geometry-only CPD-like evidence, and the unimplemented
  Newton simulation probe layer.
- [2026-05-14 Newton Contact Smoke](2026-05-14-newton-contact-smoke.md): first contact-only
  Newton canary consuming CPD-like primitive proposals.
- [2026-05-14 Newton Drop/Settle](2026-05-14-newton-drop-settle.md): first named task-level
  Newton smoke diagnostic consuming the CPD-like collision package.
- [2026-05-15 Newton Sphere-Rain](2026-05-15-newton-sphere-rain.md): second named task-level
  Newton smoke diagnostic, using a sphere-rain contact-density proxy over the capped bed CPD-like
  collision package.
- [2026-05-15 Franka CPD-Like Smoke](2026-05-15-franka-cpd-like-smoke.md): Franka/simple robot
  USD-open and capped geometry-only CPD-like smoke evidence.
- [2026-05-15 CPD-Like Component Merge Gate](2026-05-15-cpd-like-component-merge-gate.md):
  opt-in disconnected-component merge gate and merge-cost reporting for the CPD-like baseline.
- [2026-05-15 CPD-Like Objective Report](2026-05-15-cpd-like-objective-report.md):
  offline paper-aligned surrogate objective report for the capped bed CPD-like baseline.
- [2026-05-15 CPD-Like Synthetic Comparison](2026-05-15-cpd-like-synthetic-comparison.md):
  command-only deterministic synthetic objective comparison for topology-only versus
  component-merge accounting.
- [2026-05-15 CPD-Like Cost-Guided Merge](2026-05-15-cpd-like-cost-guided-merge.md):
  focused CPD-like cost-guided merge-search smoke over one deterministic synthetic fixture.
- [2026-05-16 Cost-Guided Merge Step Trace](2026-05-16-cost-guided-merge-step-trace.md):
  synthetic offline merge-step trace diagnostic accounting for the existing cost-guided fixture.
- [2026-05-15 CPD Synthetic Expected-Failure Workbench](2026-05-15-cpd-synthetic-expected-failure-workbench.md):
  deterministic expected-failure workbench that reports known CPD-paper gaps as diagnostic
  limitation flags.
- [2026-05-15 CPD Expected-Failure Master Verification](2026-05-15-cpd-expected-failure-master-verification.md):
  post-merge master verification for the expected-failure workbench slice.
- [2026-05-15 CPD Capped-Cylinder Proxy](2026-05-15-cpd-capped-cylinder-proxy.md):
  opt-in offline capped-cylinder geometry proposal proxy and reduced unsupported paper primitive
  gap evidence.
- [2026-05-15 CPD Capped-Cylinder Master Verification](2026-05-15-cpd-capped-cylinder-master-verification.md):
  post-merge master verification for the capped-cylinder proxy slice.
- [2026-05-15 Big Goal 1 Completion Audit](2026-05-15-big-goal-1-completion-audit.md):
  completion audit for the minimal CPD-like diagnostic workbench goal.
- [2026-05-15 Newton-Native Primitive Policy](2026-05-15-newton-native-primitive-policy.md):
  policy update that makes runtime primitive expansion Newton-native first.
- [2026-05-15 Newton Native Primitive Bundle](2026-05-15-newton-native-primitive-bundle.md):
  mapping, builder dispatch, bounds, and clean-env synthetic smoke evidence for the native
  `cylinder`, `cone`, and `ellipsoid` runtime bundle.
- [2026-05-15 Newton Native Bundle Explainer Docs](2026-05-15-newton-native-bundle-explainer-docs.md):
  plain-language documentation update for the latest native runtime bundle in the CPD paper story.
- [2026-05-15 Newton Native Fitting Comparison](2026-05-15-newton-native-fitting-comparison.md):
  opt-in synthetic comparison where the six-kind native subset selects `cylinder`, `cone`, and
  `ellipsoid`, with bed and Franka declared as next-scope real USD assets.
- [2026-05-15 Synthetic Native Selection Audit](2026-05-15-synthetic-native-selection-audit.md):
  candidate weighted-volume audit tables explaining why the six-kind native lane selects
  `cylinder`, `cone`, and `ellipsoid` on deterministic toy meshes.
- [2026-05-15 Synthetic Native Selection Audit Explainer Docs](2026-05-15-synthetic-native-selection-audit-explainer-docs.md):
  field-by-field documentation for the synthetic native selection audit table.
- [2026-05-15 Bed Franka Native Fitting Next Steps Docs](2026-05-15-bed-franka-native-fitting-next-steps-docs.md):
  documentation update that makes the next real-USD old/new comparison sequence explicit.
- [2026-05-15 Real USD Native Fitting Comparison](2026-05-15-real-usd-native-fitting-comparison.md):
  capped bed and capped Franka old/new offline diagnostic report.
- [2026-05-15 Real USD Candidate Audit](2026-05-15-real-usd-candidate-audit.md):
  pre-cylinder-axis per-selected-cluster candidate accounting, superseded for current status by
  the candidate-loss/cylinder-axis record.
- [2026-05-15 Real USD Native Contact Comparison](2026-05-15-real-usd-native-contact-comparison.md):
  full-mapping-gated Newton contact canary comparison for the capped bed and capped Franka old/new
  packages.
- [2026-05-15 Real USD Native Task Comparison](2026-05-15-real-usd-native-task-comparison.md):
  contact-gated drop/settle and sphere-rain task-smoke comparison for the capped bed and capped
  Franka old/new packages.
- [2026-05-15 Bed Franka Native Probe Completion Audit](2026-05-15-bed-franka-native-probe-completion-audit.md):
  completion audit mapping the requested five-step real-USD native probe objective to code,
  configs, reports, records, verification, and review fixes.
- [2026-05-15 Real USD Native Probe Story Explainer Docs](2026-05-15-real-usd-native-probe-story-explainer-docs.md):
  plain-language documentation update that explains the latest bed/Franka real-USD native probe
  slice in the CPD paper reproduction story.
- [2026-05-15 Real USD Asset Mirror Materialization](2026-05-15-real-usd-asset-mirror-materialization.md):
  ignored repo-local USD dependency-closure mirrors for the current bed and Franka smoke
  manifests, including the unresolved Franka `OmniPBR.mdl` boundary.
- [2026-05-15 Real USD Mirrors Next Steps Docs](2026-05-15-real-usd-mirrors-next-steps-docs.md):
  documentation update that expands the asset mirror materialization norm and records the next
  CPD-like candidate-loss diagnosis sequence after local bed/Franka mirrors.
- [2026-05-15 Candidate Loss Diagnosis And Cylinder Axis](2026-05-15-candidate-loss-diagnosis-and-cylinder-axis.md):
  controlled cylinder-axis fitting update, synthetic rerun, real-USD candidate-loss diagnosis,
  and bed/Franka Newton-gated rerun.
- [2026-05-15 Candidate Loss Triage](2026-05-15-candidate-loss-triage.md):
  next-slice triage metadata for near-miss extension candidates and low-support native-extension
  selections in the real-USD candidate-loss diagnosis.
- [2026-05-15 Low-Support Native Extension Admissibility](2026-05-15-low-support-native-extension-admissibility.md):
  support-aware primitive-selection guard for low-support Newton-native extension candidates,
  with capped bed/Franka candidate-loss and Newton smoke reruns.
- [2026-05-16 Cylinder Near-Miss Cluster Fixture](2026-05-16-cylinder-near-miss-cluster-fixture.md):
  synthetic support-admissible cylinder near-miss fixture for the next primitive-fitting or
  merge/search slice.
- [2026-05-16 Cylinder Near-Miss Fit Ablation](2026-05-16-cylinder-near-miss-fit-ablation.md):
  diagnostic lower-bound report showing the current cylinder near-miss fixture cannot be flipped
  by radial-center refinement while preserving containment.
- [2026-05-16 Cylinder Near-Miss Scoring Sensitivity](2026-05-16-cylinder-near-miss-scoring-sensitivity.md):
  counterfactual scoring-sensitivity report for the synthetic cylinder near-miss fixture, without
  changing default selection or Newton packages.
- [2026-05-16 Cylinder Near-Miss Scoring Policy Ablation](2026-05-16-cylinder-near-miss-scoring-policy-ablation.md):
  report-only counterfactual scoring-policy ablation for the synthetic cylinder near-miss fixture,
  without changing default selection or Newton packages.
- [2026-05-16 Cylinder Scoring Policy Guardrail](2026-05-16-cylinder-scoring-policy-guardrail.md):
  extension of the report-only scoring-policy ablation with a clearly boxy cuboid negative-control
  fixture.
- [2026-05-16 Cylinder Scoring Policy Selection Probe](2026-05-16-cylinder-scoring-policy-selection-probe.md):
  synthetic offline opt-in scoring-policy selection probe where the near-miss flips and the boxy
  guardrail remains box, without changing default packages or Newton tasks.
- [2026-05-16 Cylinder Scoring Policy Package Probe](2026-05-16-cylinder-scoring-policy-package-probe.md):
  explicitly opt-in synthetic package probe where the near-miss package changes to `cylinder`,
  the boxy guardrail remains `box`, and Newton shape-mapping coverage is recorded without running
  Newton contact or task diagnostics.
- [2026-05-16 Cylinder Scoring Policy Newton Probe](2026-05-16-cylinder-scoring-policy-newton-probe.md):
  explicitly opt-in synthetic Newton diagnostic over the changed near-miss package pair, with
  contact-gated drop/settle and sphere-rain task-smoke status under recorded settings.
- [2026-05-16 Controlled Merge-Search Package Probe](2026-05-16-controlled-merge-search-package-probe.md):
  command-only synthetic package-path probe that carries the existing `cost_guided_pair_choice`
  merge/search behavior difference into `CollisionPackage` and Newton shape-mapping accounting.
- [2026-05-16 Controlled Merge-Search Newton Probe](2026-05-16-controlled-merge-search-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe over the changed controlled merge/search package
  pair.
- [2026-05-16 Cost-Guided Lookahead Merge](2026-05-16-cost-guided-lookahead-merge.md):
  command-only synthetic two-step lookahead merge/search diagnostic over one deterministic trap
  fixture.
- [2026-05-16 Cost-Guided Lookahead Package Probe](2026-05-16-cost-guided-lookahead-package-probe.md):
  command-only synthetic package-path and Newton shape-mapping probe for the lookahead-changed
  package pair.
- [2026-05-16 Cost-Guided Lookahead Newton Probe](2026-05-16-cost-guided-lookahead-newton-probe.md):
  synthetic contact-gated Newton task-smoke probe for the lookahead-changed package pair.
- [2026-05-16 Four-Block Slice Report](2026-05-16-four-block-slice-report.md):
  command-only evidence map that summarizes the recorded cost-guided lookahead synthetic slice
  across primitive fitting/selection, merge/search, offline diagnostics, and Newton task
  comparison by linking existing dated records without rerunning source reports, USD loading, or
  Newton tasks.
- [2026-05-16 Newton CPD Workbench Four-Block Status Audit](2026-05-16-newton-cpd-workbench-four-block-status-audit.md):
  status audit mapping primitive fitting/selection, merge/search, offline reports, and Newton task
  comparison to current evidence and remaining gaps.
- [2026-05-16 Four-Block Workbench Completion Audit](2026-05-16-four-block-workbench-completion-audit.md):
  completion audit for the bounded Newton CPD workbench slice, mapping the four-block objective to
  code, CLI, tests, dated records, review fixes, and verification evidence.
- [2026-05-16 CPD Pipeline Step-By-Step Explainer](2026-05-16-cpd-pipeline-step-by-step-explainer.md):
  documentation update that explains the full mesh-to-benchmark pipeline and separates CPD
  algorithm work from Newton workbench and evaluation claims.
- [2026-05-16 CPD Paper Gap Matrix And Offline Lane Spec](2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md):
  documentation update that maps paper requirements to current surrogates and defines the next
  planned fixture-scoped offline paper-faithful lane before any real-USD, Newton runtime, or
  benchmark expansion.
- [2026-05-16 CPD Paper Offline First Fixture Slice](2026-05-16-cpd-paper-offline-first-fixture-slice.md):
  partial command-only offline paper-lane audit over `paper_single_box` and `paper_two_face_merge`,
  including operator, primitive-fit subset, and collapse-cost fields.
- [2026-05-16 CPD Paper Frustum Trapezoid Audit](2026-05-16-cpd-paper-frustum-trapezoid-audit.md):
  partial command-only offline primitive-fit audit row expansion for frustum and trapezoidal-prism
  candidates on deterministic toy fixtures.
- [2026-05-16 CPD Paper Flat Capped-Cylinder Audit](2026-05-16-cpd-paper-flat-capped-cylinder-audit.md):
  partial command-only offline primitive-fit audit row expansion for paper flat capped-cylinder
  candidates on deterministic toy fixtures.
- [2026-05-16 CPD Paper Capsule Axis Audit](2026-05-16-cpd-paper-capsule-axis-audit.md):
  partial command-only offline primitive-fit audit row expansion for paper-shaped capsule axis
  candidates on deterministic toy fixtures.
- [2026-05-16 CPD Paper Priority Queue Trace Audit](2026-05-16-cpd-paper-priority-queue-trace-audit.md):
  partial command-only topology priority-queue trace audit with stale-pruning records on
  deterministic toy fixtures.
- [2026-05-16 CPD Paper Component-Pair Edge Insertion](2026-05-16-cpd-paper-component-pair-edge-insertion.md):
  partial command-only threshold-disabled component-pair insertion audit on a deterministic
  disconnected toy fixture.
- [2026-05-16 CPD Paper Component-Pair Threshold Blocking](2026-05-16-cpd-paper-component-pair-threshold-blocking.md):
  partial command-only finite-threshold component-pair block audit on a deterministic disconnected
  toy fixture.
- [2026-05-16 CPD Paper Postprocess Audit](2026-05-16-cpd-paper-postprocess-audit.md):
  partial command-only enclosed-primitive postprocess cull audit on a deterministic nested toy
  fixture.
- [2026-05-16 CPD Paper Polygon Quad Intake Policy](2026-05-16-cpd-paper-polygon-quad-intake-policy.md):
  partial command-only source-face intake policy audit on deterministic quad and polygon toy
  fixtures.
- [2026-05-16 CPD Paper OBB Sphere Fit Faithfulness](2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md):
  partial command-only paper-shaped OBB/sphere fit audit on deterministic toy fixtures.
- [2026-05-16 CPD Paper Duplicate Vertex Preprocessing](2026-05-16-cpd-paper-duplicate-vertex-preprocessing.md):
  partial command-only exact-coordinate duplicate-vertex preprocessing audit on one deterministic
  toy fixture.
- [2026-05-16 CPD Paper Faithful Offline Scope Audit](2026-05-16-cpd-paper-faithful-offline-scope-audit.md):
  partial command-only scope-audit criteria table that keeps the offline paper lane partial and
  advances the next gate to fixture-breadth expansion.
- [2026-05-16 CPD Paper Fixture Breadth Expansion Plan](2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md):
  documentation-only plan that maps the nine scope-audit blockers to future synthetic fixture
  batches and recommends Batch A as the next code slice.
- [2026-05-16 CPD Paper Fixture Breadth Batch A](2026-05-16-cpd-paper-fixture-breadth-batch-a.md):
  partial command-only source/preprocess/intake/operator fixture-breadth audit inside
  `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Fixture Breadth Batch B](2026-05-16-cpd-paper-fixture-breadth-batch-b.md):
  partial command-only primitive-fit fixture-breadth audit inside `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Fixture Breadth Batch C](2026-05-16-cpd-paper-fixture-breadth-batch-c.md):
  partial command-only cost/search/stop fixture-breadth audit inside
  `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Fixture Breadth Batch D](2026-05-16-cpd-paper-fixture-breadth-batch-d.md):
  partial command-only component-pair fixture-breadth audit inside
  `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Fixture Breadth Batch E](2026-05-16-cpd-paper-fixture-breadth-batch-e.md):
  partial command-only postprocess fixture-breadth audit inside
  `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Fixture Breadth Completion Review](2026-05-16-cpd-paper-fixture-breadth-completion-review.md):
  command-only synthetic fixture-breadth completion review for planned Batches A-E inside the
  partial `cpd_paper_offline_report`.
- [2026-05-16 CPD Paper Faithful Offline Generalization Plan](2026-05-16-cpd-paper-faithful-offline-generalization-plan.md):
  command-only planning table for offline CPD paper-lane generalization beyond named toy fixtures.
- [2026-05-16 CPD Paper Generalization Batch A Source Policy](2026-05-16-cpd-paper-generalization-batch-a-source-policy.md):
  partial command-only source-policy generalization matrix inside
  `cpd_paper_offline_report`.
- [2026-05-15 CPD Latest Diagnostic Loop Explainer Docs](2026-05-15-cpd-latest-diagnostic-loop-explainer-docs.md):
  documentation update that explains the latest candidate-loss and cylinder-axis slice as a
  repeatable diagnostic loop in the CPD paper story.
- [2026-05-15 CPD Paper Companion MVP](2026-05-15-cpd-paper-companion-mvp.md):
  Astro + MDX bilingual paper companion scaffold with source-paper claim namespacing and
  permission-record-pending AI-assisted draft translation status.
- [2026-05-15 CPD Paper Companion Permission Assertion](2026-05-15-cpd-paper-permission-assertion.md):
  source-paper companion permission assertion note that keeps draft translation and reproduction
  claims separated until formal authorization evidence is supplied.
- [2026-05-15 CPD Full Text Import And Translation](2026-05-15-cpd-full-text-import-translation.md):
  full-section CPD companion import with AI-assisted draft translations, gated source LaTeX
  blocks, and `not_started` reproduction states.
- [2026-05-16 Paper Site Visual QA](2026-05-16-paper-site-visual-qa.md):
  browser-rendered paper companion visual QA for formula overflow, figure readability, image
  upscaling, preserved source blocks, and responsive layout.
- [2026-05-16 Paper Equation Rendering Fix](2026-05-16-paper-equation-rendering-fix.md):
  reader-facing display-equation rendering fix for source-paper `equation` and `align`
  environments on the paper companion pages.
- [2026-05-16 Paper Reference Numbering Fix](2026-05-16-paper-reference-numbering-fix.md):
  reader-facing paper companion reference-numbering fix that hides internal source labels and
  resolves figure, table, algorithm, equation, and section references to paper numbers.
- [2026-05-16 Paper Reader Chrome And Permission Validator](2026-05-16-paper-reader-chrome-and-permission-validator.md):
  reader-facing paper companion cleanup that removes internal review chrome and tightens paper
  asset permission-evidence validation.
- [2026-05-15 CPD Objective Alignment And Next Steps](2026-05-15-cpd-objective-alignment-and-next-steps.md):
  documentation clarification for objective-report paper alignment and the next algorithmic
  sequence.
- [2026-05-15 Three-Slice Final Verification](2026-05-15-three-slice-final-verification.md):
  final verification and review-fix record for sphere-rain, Franka smoke, and component-merge
  gate.
- [2026-05-15 CPD Paper Story Status Docs](2026-05-15-cpd-paper-story-status-docs.md):
  documentation update that maps the current CPD-like workbench onto the full CPD paper
  reproduction story.
- [2026-05-15 CPD Cost-Guided Story Explainer](2026-05-15-cpd-cost-guided-story-explainer.md):
  documentation update that explains the latest cost-guided merge change in the full CPD paper
  story.
- [2026-05-15 AABB-Normalized Merge-Excess Explainer](2026-05-15-aabb-normalized-merge-excess-explainer.md):
  documentation update that explains the surrogate merge cost used by the CPD-like cost-guided
  smoke.
- [2026-05-15 CPD Eq.4 Alignment Metadata](2026-05-15-cpd-eq4-alignment-metadata.md):
  structured objective-report metadata that maps current surrogate merge-excess terms to the CPD
  paper Eq.4 role without claiming Eq.4 implementation.
