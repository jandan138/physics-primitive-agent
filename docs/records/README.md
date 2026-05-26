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

- [2026-05-26 ACCV Submission Readiness Pass](2026-05-26-accv-submission-readiness-pass.md):
  ACCV policy check, related-work/citation update, method/experiment narrative alignment, and
  final preflight record for the scoped Phase 0 submission candidate.
- [2026-05-26 Link-Aware Robot Package Generation](2026-05-26-link-aware-robot-package-generation.md):
  first Phase 0 Franka link-aware package generation record; 12 rigid-body links detected, 12
  link-framed box primitives generated, zero cross-link merges, and `/panda/panda_link8` recorded
  as a meshless placeholder.
- [2026-05-26 Phase 0 V-HACD Runtime Follow-Up](2026-05-26-phase0-vhacd-runtime-followup.md):
  scoped follow-up run after installing `vhacdx`; V-HACD generates hull packages for all five
  GRScenes rigid assets, records V-HACD probe failures on bowl/cup/tray, and has zero dependency
  gaps.
- [2026-05-25 Phase 0 Stack CoACD Articulation Follow-Up](2026-05-25-phase0-stack-coacd-articulation-followup.md):
  scoped follow-up run that adds dedicated stack-or-slide execution, CoACD executable convex-mesh
  baseline packages, initial V-HACD dependency-gap records, and Franka articulation smoke while
  preserving the link-aware robot package boundary; superseded for V-HACD status by the 2026-05-26
  runtime follow-up.
- [2026-05-25 Phase 0 GRScenes Rigid Benchmark](2026-05-25-phase0-grscenes-rigid-benchmark.md):
  scoped five-asset GRScenes rigid diagnostic run with bounding-primitive and CPD-style first-mesh
  candidate lanes, Newton contact/drop/sphere outcomes, and explicit fallback/dependency-gap
  labels.
- [2026-05-25 Phase 0 GRScenes Asset Intake](2026-05-25-phase0-grscenes-asset-intake.md):
  five selected GRScenes rigid assets materialized into ignored repo-local mirrors with tracked
  source/local hashes and USD/MDL/texture dependency metadata; this is asset intake evidence, not
  Phase 0 benchmark evidence.
- [2026-05-22 DeepDive Direction Shift To Simulation-Checked Robotics](2026-05-22-deepdive-direction-shift-to-simulation-checked-robotics.md):
  current-facing documentation alignment that shifts the DeepDive story from CPD-like
  reproduction toward simulation-checked primitive collider acceptance, with robot articulation
  gates as the next evidence target.
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
- [2026-05-21 Real Newton Smoke Rerun](2026-05-21-real-newton-smoke-rerun.md): confirms the
  documented clean conda Newton environment still runs contact, drop/settle, and sphere-rain smoke
  diagnostics for the capped bed CPD-like package.
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
- [2026-05-21 Real USD Native Task Rerun](2026-05-21-real-usd-native-task-rerun.md):
  clean-env rerun of the capped bed and capped Franka real-USD old/new contact-gated task smokes.
- [2026-05-21 Franka Native Opt-In Probe](2026-05-21-franka-native-opt-in-probe.md):
  explicit capped Franka opt-in native package containing selected `cylinder` primitives; package
  mapping, representative contact canaries, drop/settle, and sphere-rain passed.
- [2026-05-21 Bed Native Opt-In Probe](2026-05-21-bed-native-opt-in-probe.md):
  explicit capped bed opt-in native package containing one selected `cylinder` primitive;
  mapping, representative contact canaries, and sphere-rain passed, while drop/settle failed
  `not_settled`; a local cylinder-revert drop-attribution diagnostic cleared the blocker by
  replacing only that selected cylinder package delta with the native box fallback, and a
  center/shape separation diagnostic kept `cylinder_at_box_center` failing while
  `box_at_cylinder_center` passed. A target-only control did not reproduce the full-package
  blocker with the isolated cylinder, and local compound controls did not produce a valid compact
  cylinder-only reproducer. A worktree full-compound trace script now records body mass, COM,
  inertia, body pose/velocity, support height, and contact details for the fixed primitive-6
  variants, and its inertial-array counterfactual clears the recorded `360`-frame drop/settle
  label in one sensitivity control after applying native all-box inertial arrays to the opt-in
  cylinder geometry. A COM-only field ablation also clears the recorded `360`-frame final-speed
  gate label in one sensitivity control
  while retaining cylinder mass and inertia, and a
  COM-axis subset ablation records `x`, `y`, `z`, `xy`, and `yz` still `not_settled` while `xz`
  clears that recorded label in the same fixed full-compound gate. A COM-blend ablation records `0.25`,
  `0.5`, and `0.75` blends still `not_settled` for full `xyz` and `xz`, while the `1.0` endpoint
  clears that recorded label in the same sensitivity-control scope. A near-endpoint COM-blend
  refinement records full `xyz` clearing that label at `0.875` and above in this run, while `xz`
  remains `not_settled` at `0.875` and clears the label at `0.9375` and above in the same fixed
  gate; this is not a COM threshold
  proof. A tail-summary rerun records `tail_linear_speed_summary` as late-window speed telemetry
  only; pass/fail remains final-speed gated, not a sustained-settle proof. A
  `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720`-frame window
  sweep records the native/reverted-control final-speed task-gate bracket as `361` clean versus
  `362` failing; dirty-control rows are rejected as COM-blend stability or fix evidence. A pre-solver
  model-build audit records zero
  rest-without-target delta and nonzero primitive-6 target/full mass/COM/inertia deltas under
  matching anchors. These are not validated fixes or root-cause proof.
- [2026-05-22 Cylinder Repair-Candidate Controls](2026-05-22-cylinder-repair-candidate-controls.md):
  full-compound Newton controls retaining the opt-in cylinder geometry while applying selected
  native all-box pre-solver body-state arrays. COM-only, inertia-only, and full inertial-array
  overrides clear the recorded 360-frame `not_settled` label; mass-only does not. This is
  one-config sensitivity evidence, not a validated repair.
- [2026-05-22 Cylinder Mechanism Decision Matrix](2026-05-22-cylinder-mechanism-decision-matrix.md):
  claim-bounded synthesis table for the active bed-vs-Franka cylinder question across geometry,
  COM, inertia, mass, contact/floor, and full-compound context.
- [2026-05-22 Cylinder Goal Completion Audit](2026-05-22-cylinder-goal-completion-audit.md):
  strict completion audit for the active bed-vs-Franka cylinder mechanism goal. It records that
  the diagnostic answer was strong before contact/floor closure, but the goal remained active at
  that point because root-cause proof, validated repair/policy evidence, and stronger
  contact/floor closure were not yet recorded.
- [2026-05-22 Cylinder Contact/Floor Closure Audit](2026-05-22-cylinder-contact-floor-closure-audit.md):
  same-report contact/support audit over the capped-bed full-compound controls; failing and
  passing variants share the final contact count and primitive suffixes, so contact/floor is no
  longer the likely full-package primary mechanism, while pair-level floor controls remain
  secondary local-context evidence.
- [2026-05-22 Cylinder Goal Completion Audit After Contact Closure](2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md):
  final requirement-by-requirement audit for the active bed-vs-Franka cylinder mechanism goal; it
  records the diagnostic answer as complete for the recorded capped bed/Franka scope while keeping
  repair, calibration, benchmark, collision-quality, and safety claims unsupported.
- [2026-05-22 Cylinder Package Body-State Risk Probe](2026-05-22-cylinder-package-body-state-risk-probe.md):
  package-geometry COM/inertia proxy that flags the recorded capped bed large-flat-cylinder
  package and does not flag the recorded capped Franka cost-guided cylinder package, without
  reading or copying Newton model arrays.
- [2026-05-22 Cylinder Package Body-State Guard Candidate](2026-05-22-cylinder-package-body-state-guard-candidate.md):
  opt-in package-level guard-candidate decision over the same bed/Franka reports; it recommends
  fallback to the recorded passing native package for flagged bed and keeping the recorded passing
  native-opt-in package for unflagged Franka, plus a fresh real Newton rerun of the existing
  guarded support-threshold task smoke.
- [2026-05-22 Package Body-State Guard Task Path](2026-05-22-package-body-state-guard-task-path.md):
  explicitly opt-in real-USD task path that first creates cylinder-bearing native-opt-in
  candidates for capped bed and capped Franka, then falls back only the flagged bed package while
  preserving the unflagged Franka cylinder package through real Newton task smokes.
- [2026-05-21 Native Selector Diagnostic Guard](2026-05-21-native-selector-diagnostic-guard.md):
  opt-in selector guard derived from the capped-bed Newton blocker; guarded bed rejects large flat
  cylinder candidates and passes the recorded task smokes, while guarded Franka keeps its smaller
  selected cylinders and also passes.
- [2026-05-21 Franka Native Opt-In Support Threshold Probe](2026-05-21-franka-native-opt-in-support-threshold-probe.md):
  opt-in capped Franka support-threshold diagnostic; the changed package selects `29` boxes plus
  `3` cylinders and passes contact-gated drop/settle plus sphere-rain.
- [2026-05-21 Bed Franka Guarded Support Threshold Probe](2026-05-21-bed-franka-guarded-support-threshold-probe.md):
  two-role opt-in diagnostic that composes the large-flat-cylinder guard with relaxed cylinder
  support thresholds and no score multiplier; guarded bed stays at `32` boxes, while guarded
  support-threshold Franka selects `29` boxes plus `3` cylinders and passes contact-gated
  drop/settle plus sphere-rain.
- [2026-05-21 Newton-In-The-Loop Selector Story Docs](2026-05-21-newton-in-the-loop-selector-story-docs.md):
  plain-language documentation update that explains why the guarded selector slice followed the
  earlier gates and what it does, and does not, prove in the CPD paper story.
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
- [2026-05-16 CPD Paper Generalization Batch B Primitive Fit Engine](2026-05-16-cpd-paper-generalization-batch-b-primitive-fit-engine.md):
  partial command-only primitive-fit engine generalization matrix inside
  `cpd_paper_offline_report`.
- [2026-05-17 CPD Paper Generalization Batch C Search Engine](2026-05-17-cpd-paper-generalization-batch-c-search-engine.md):
  partial command-only search-engine generalization matrix inside `cpd_paper_offline_report`.
- [2026-05-17 CPD Paper Generalization Batch D Postprocess Policy](2026-05-17-cpd-paper-generalization-batch-d-postprocess-policy.md):
  partial command-only postprocess-policy generalization matrix inside
  `cpd_paper_offline_report`.
- [2026-05-17 CPD Paper Generalization Batch E Package Boundary Readiness](2026-05-17-cpd-paper-generalization-batch-e-package-boundary-readiness.md):
  partial command-only package-boundary readiness matrix inside `cpd_paper_offline_report`.
- [2026-05-17 CPD Paper Changed-Decomposition Output Contract](2026-05-17-cpd-paper-changed-decomposition-output-contract.md):
  partial offline changed-decomposition output contract inside `cpd_paper_offline_report`, not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Package-Adapter Contract](2026-05-17-cpd-paper-package-adapter-contract.md):
  partial command-only offline package-adapter contract inside `cpd_paper_offline_report`, not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Package-Adapter Unsupported Primitive Policy](2026-05-17-cpd-paper-package-adapter-unsupported-primitive-policy.md):
  partial command-only offline unsupported-primitive policy inside `cpd_paper_offline_report`, not
  a `CollisionPackage`.
- [2026-05-17 CPD Paper Package Conversion Mapped-Subset Plan](2026-05-17-cpd-paper-package-conversion-mapped-subset-plan.md):
  partial command-only offline mapped-subset package-conversion planning table inside
  `cpd_paper_offline_report`, not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset Conversion Candidate Matrix](2026-05-17-cpd-paper-mapped-subset-conversion-candidate-matrix.md):
  partial command-only offline mapped-subset conversion candidate matrix inside
  `cpd_paper_offline_report`, not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset Adapter Preflight Contract](2026-05-17-cpd-paper-mapped-subset-adapter-preflight-contract.md):
  partial command-only offline mapped-subset adapter-preflight contract inside
  `cpd_paper_offline_report`, not `PrimitiveSpec` generation and not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Dry-Run Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md):
  partial command-only offline mapped-subset PrimitiveSpec dry-run contract inside
  `cpd_paper_offline_report`, not real `PrimitiveSpec` generation and not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Validation Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md):
  partial command-only offline mapped-subset PrimitiveSpec validation contract inside
  `cpd_paper_offline_report`, not real `PrimitiveSpec` generation and not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Generation Preflight Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md):
  partial command-only offline mapped-subset PrimitiveSpec generation-preflight contract inside
  `cpd_paper_offline_report`, not real `PrimitiveSpec` generation and not a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Generation Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-contract.md):
  partial command-only offline mapped-subset PrimitiveSpec generation contract inside
  `cpd_paper_offline_report`, not runtime `PrimitiveSpec` generation and not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Candidate-Source Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md):
  partial command-only offline mapped-subset PrimitiveSpec candidate-source audit inside
  `cpd_paper_offline_report`, not runtime `PrimitiveSpec` generation and not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset Native-Current Fixture Contract](2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md):
  partial command-only offline mapped-subset native-current fixture source-row contract inside
  `cpd_paper_offline_report`, not runtime `PrimitiveSpec` generation and not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Generation Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-generation-contract.md):
  partial command-only offline mapped-subset native-fixture PrimitiveSpec-like dict generation
  contract inside `cpd_paper_offline_report`, not runtime `PrimitiveSpec` object creation and not
  a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Native-Fixture Serialization Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-native-fixture-serialization-contract.md):
  partial command-only offline mapped-subset native-fixture serialization/schema-stability
  contract inside `cpd_paper_offline_report`, not runtime `PrimitiveSpec` object creation and not
  a `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Runtime-Boundary Preflight Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract.md):
  partial command-only offline mapped-subset runtime-boundary preflight contract inside
  `cpd_paper_offline_report`, not runtime `PrimitiveSpec` construction and not a
  `CollisionPackage`.
- [2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Runtime-Construction Contract](2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract.md):
  partial single-fixture offline mapped-subset runtime-construction contract inside
  `cpd_paper_offline_report`. It constructs exactly one runtime `PrimitiveSpec` object from the
  canonical synthetic `paper_single_box` OBB/box preflight JSON, stores only
  `PrimitiveSpec.to_dict()` in the report, and remains not package generation, not Newton
  execution, not real-USD evidence, not benchmark evidence, and not collision-quality evidence.
- [2026-05-17 CPD Paper Mapped-Subset CollisionPackage Generation Preflight Contract](2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md):
  partial single-fixture offline mapped-subset package-generation preflight contract inside
  `cpd_paper_offline_report`. It records exactly one later package-generation candidate from the
  runtime `PrimitiveSpec.to_dict()` payload, keeps generated CollisionPackages and
  runtime-admissibility checks at zero, and remains not package readiness, not Newton execution,
  not real-USD evidence, not benchmark evidence, and not collision-quality evidence.
- [2026-05-17 CPD Paper Mapped-Subset CollisionPackage Generation Contract](2026-05-17-cpd-paper-mapped-subset-collision-package-generation-contract.md):
  partial single-fixture offline mapped-subset CollisionPackage generation contract inside
  `cpd_paper_offline_report`. It constructs exactly one synthetic `CollisionPackage.to_dict()`
  artifact for `paper_single_box`, keeps runtime-admissibility checks and Newton execution at
  zero or false, and remains not package readiness, not real-USD evidence, not benchmark evidence,
  not collision-quality evidence, and not paper primitive vocabulary coverage.
- [2026-05-17 CPD Paper Mapped-Subset Runtime-Admissibility Preflight Contract](2026-05-17-cpd-paper-mapped-subset-runtime-admissibility-preflight-contract.md):
  partial single-fixture offline mapped-subset runtime-admissibility preflight contract inside
  `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box`
  `CollisionPackage.to_dict()` artifact, records exactly one later runtime-admissibility candidate
  row without copying the full package dict, keeps runtime-admissibility checks and Newton
  execution at zero or false, and remains not package readiness, not runtime admissibility, not
  Newton support, not real-USD evidence, not benchmark evidence, not collision-quality evidence,
  not paper primitive vocabulary coverage, not `paper_faithful_offline`, not full CPD reproduction,
  not deployment readiness, and not safety certification.
- [2026-05-18 CPD Paper Mapped-Subset Runtime-Admissibility Contract](2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract.md):
  partial single-fixture offline/static mapped-subset runtime-admissibility contract inside
  `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box`
  runtime-admissibility preflight row, records exactly one finite-geometry and box-schema static
  check, keeps Newton shape mapping and Newton execution at zero or false, and remains not package
  readiness, not Newton readiness, not real-USD evidence, not benchmark evidence, not
  collision-quality evidence, not paper primitive vocabulary coverage, not `paper_faithful_offline`,
  not full CPD reproduction, not deployment readiness, and not safety certification.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape-Mapping Preflight Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-preflight-contract.md):
  partial single-fixture offline/static mapped-subset Newton shape-mapping preflight contract
  inside `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box`
  runtime-admissibility row, records exactly one static mapper-handoff row, keeps mapping attempts,
  Newton mapping records, and Newton execution at zero or false, and remains not Newton readiness,
  not Newton support, not real-USD evidence, not benchmark evidence, not collision-quality
  evidence, not paper primitive vocabulary coverage, not `paper_faithful_offline`, not full CPD
  reproduction, not deployment readiness, and not safety certification.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape-Mapping Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-mapping-contract.md):
  partial single-fixture offline/static mapped-subset Newton shape descriptor contract inside
  `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box` shape-mapping
  preflight row, records exactly one report-scoped `newton_shape_descriptor_dict` for target kind
  `box`, keeps mapping attempts, Newton mapping records, Newton shape object construction, and
  Newton execution at zero or false, and remains not Newton readiness, not Newton support, not
  real-USD evidence, not benchmark evidence, not collision-quality evidence, not paper primitive
  vocabulary coverage, not `paper_faithful_offline`, not full CPD
  reproduction, not deployment readiness, and not safety certification.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime-Boundary Preflight Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-boundary-preflight-contract.md):
  partial single-fixture offline/static mapped-subset Newton shape runtime-boundary preflight
  contract inside `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box`
  descriptor row, records exactly one later runtime-construction candidate, keeps Newton shape
  object construction and Newton execution at zero or false, and remains not Newton readiness, not
  Newton support, not real-USD evidence, not benchmark evidence, not collision-quality evidence,
  not paper primitive vocabulary coverage, not `paper_faithful_offline`, not full CPD
  reproduction, not deployment readiness, and not safety certification.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime-Construction Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-construction-contract.md):
  partial single-fixture offline/report-scoped mapped-subset Newton shape runtime-construction
  contract inside `cpd_paper_offline_report`. It consumes the one synthetic `paper_single_box`
  runtime-boundary candidate, records exactly one repo-local `NewtonShapeMapping.to_dict()` mapping
  record, keeps Newton engine shape objects, builder shape calls, Newton runtime, real-USD,
  benchmark, and collision-quality evidence at zero or false, and advances the runtime-lane next
  gate to `paper_mapped_subset_newton_shape_runtime_builder_preflight_contract`.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Builder-Preflight Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-preflight-contract.md):
  partial single-fixture offline/static mapped-subset Newton shape runtime builder-preflight
  contract inside `cpd_paper_offline_report`. It consumes the one repo-local
  `NewtonShapeMapping.to_dict()` mapping record, records exactly one JSON-safe future box builder
  call plan, keeps builder calls, Newton engine shape objects, Newton runtime, real-USD,
  benchmark, and collision-quality evidence at zero or false, and advances the runtime-lane next
  gate to `paper_mapped_subset_newton_shape_runtime_builder_construction_contract`.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Builder-Construction Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-builder-construction-contract.md):
  partial single-fixture offline/report-only mapped-subset Newton shape runtime
  builder-construction contract inside `cpd_paper_offline_report`. It consumes the builder
  preflight row, records exactly one JSON-safe repo-local recording-builder `add_shape_box` call
  artifact through the repo-local static shape helper and fake Warp-like module, keeps real Newton
  imports, Newton `ModelBuilder` instantiation, Newton engine shape objects, real Newton builder
  shape calls, Newton runtime, real-USD, benchmark, and collision-quality evidence at zero or
  false, and at that stage advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract`.
- [2026-05-18 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Boundary Preflight Contract](2026-05-18-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-boundary-preflight-contract.md):
  single-fixture offline/static Newton engine-builder boundary-preflight contract inside
  `cpd_paper_offline_report`. It consumes the repo-local recording-builder call artifact, records
  one future-boundary checklist row for the later real `newton.ModelBuilder` / `add_shape_box`
  environment boundary, keeps real Newton imports, Newton `ModelBuilder` instantiation, real
  builder shape calls, model finalization, collision pipeline calls, Newton runtime, real-USD,
  benchmark, and collision-quality evidence at zero or false, and advances the runtime-lane next
  gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract`.
- [2026-05-19 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder Environment Probe Contract](2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-environment-probe-contract.md):
  single-fixture bounded Newton/Warp environment-provenance contract inside
  `cpd_paper_offline_report`. It consumes the engine-builder boundary-preflight row, records
  configured-source-dir status and JSON-safe `find_spec` provenance shape, keeps real runtime
  imports, Newton `ModelBuilder` instantiation, real builder shape calls, model finalization,
  collision pipeline calls, Newton runtime, real-USD, benchmark, and collision-quality evidence at
  zero or false, and advances the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract`.
- [2026-05-19 CPD Paper Mapped-Subset Newton Shape Runtime Engine-Builder API-Surface Contract](2026-05-19-cpd-paper-mapped-subset-newton-shape-runtime-engine-builder-api-surface-contract.md):
  single-fixture bounded source-AST API-surface contract inside `cpd_paper_offline_report`. It
  consumes the environment-probe row, records default no-config API-surface status for the future
  `newton.ModelBuilder` / `add_shape_box` boundary, keeps real runtime imports, Newton
  `ModelBuilder` instantiation, real builder shape calls, model finalization, collision pipeline
  calls, Newton runtime, real-USD, benchmark, and collision-quality evidence at zero or false, and
  at that stage advanced the stage-local runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract`.
- [2026-05-19 CPD Paper Newton Engine-Builder Entry Contract](2026-05-19-cpd-paper-newton-engine-builder-entry-contract.md):
  single-fixture report-only Newton engine-builder entry decision inside
  `cpd_paper_offline_report`. It consumes the API-surface row, records
  `entry_decision: defer_real_runtime_entry`, keeps real runtime imports, Newton
  `ModelBuilder` instantiation, Newton engine shape objects, real builder shape calls, model
  finalization, collision pipeline calls, Newton runtime, real-USD, benchmark, and
  collision-quality evidence at zero or false, and at that stage advanced the stage-local
  runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract`.
- [2026-05-19 CPD Paper Newton Engine-Builder Smoke Contract](2026-05-19-cpd-paper-newton-engine-builder-smoke-contract.md):
  single-fixture report-only Newton engine-builder skipped-smoke decision inside
  `cpd_paper_offline_report`. It consumes the entry row, records
  `smoke_decision: skip_real_runtime_smoke`, keeps runtime-smoke attempts, real runtime imports,
  Newton `ModelBuilder` instantiation, Newton engine shape objects, real builder shape calls, model
  finalization, collision pipeline calls, Newton runtime, real-USD, benchmark, and
  collision-quality evidence at zero or false, and at that stage advanced the runtime-lane next
  gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract`.
- [2026-05-20 CPD Paper Newton Engine-Builder Runtime-Execution Contract](2026-05-20-cpd-paper-newton-engine-builder-runtime-execution-contract.md):
  single-fixture report-only Newton engine-builder skipped-runtime-execution decision inside
  `cpd_paper_offline_report`. It consumes the smoke row, records
  `runtime_execution_decision: skip_real_runtime_execution`, keeps runtime-execution attempts,
  real runtime imports, Newton `ModelBuilder` instantiation, Newton engine shape objects, real
  builder shape calls, model finalization, collision pipeline calls, Newton runtime, real-USD,
  benchmark, and collision-quality evidence at zero or false, and advances the runtime-lane next
  gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract`.
- [2026-05-20 CPD Paper Newton Engine-Builder Runtime-Lane Review Contract](2026-05-20-cpd-paper-newton-engine-builder-runtime-lane-review-contract.md):
  single-fixture report-only Newton engine-builder runtime-lane claim-boundary review inside
  `cpd_paper_offline_report`. It consumes the skipped-runtime-execution row, records
  `runtime_lane_review_decision: keep_real_runtime_execution_blocked`, keeps runtime compatibility
  unvalidated, keeps runtime/import/builder/finalization/collision counters at zero, and advances
  the runtime-lane next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract`.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Design Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-design-contract.md):
  single-fixture report-only Newton engine-builder configured-runtime input design inside
  `cpd_paper_offline_report`. It consumes the runtime-lane review row, records
  `configured_runtime_design_decision: define_configured_runtime_inputs_keep_real_runtime_blocked`,
  keeps runtime config validation false, keeps runtime/import/builder/finalization/collision
  counters at zero, and advanced the stage-local next gate to
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract`.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Preflight Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-preflight-contract.md):
  single-fixture report-only configured-runtime preflight inside `cpd_paper_offline_report`. It
  consumes the configured-runtime design row, reads no config, resolves no runtime source/device,
  and advances the stage-local next gate to configured-runtime validation.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Validation Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-validation-contract.md):
  single-fixture report-only missing-config validation inside `cpd_paper_offline_report`. It reads
  no config file or environment, keeps runtime source/device resolution false, and advances the
  stage-local next gate to configured-runtime source resolution.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Source-Resolution Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-source-resolution-contract.md):
  single-fixture report-only missing-source resolution inside `cpd_paper_offline_report`. It
  performs no filesystem probe, keeps all real runtime counters at zero, and advances the
  stage-local next gate to configured-runtime device resolution.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Device-Resolution Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-device-resolution-contract.md):
  single-fixture report-only missing-device resolution inside `cpd_paper_offline_report`. It
  creates no runtime device object, keeps all real runtime counters at zero, and advances the
  stage-local next gate to configured-runtime entry decision.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Entry-Decision Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-entry-decision-contract.md):
  single-fixture report-only no-runtime-entry decision inside `cpd_paper_offline_report`. It
  consumes the configured-runtime device-resolution row, keeps runtime entry false, keeps all real
  runtime counters at zero, and at that stage advanced the next gate to configured-runtime smoke.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Smoke Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-smoke-contract.md):
  single-fixture report-only skipped-smoke decision inside `cpd_paper_offline_report`. It consumes
  the configured-runtime entry-decision row, keeps runtime smoke false, keeps all real runtime
  counters at zero, and at that stage advanced the next gate to configured-runtime execution.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Execution Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-execution-contract.md):
  single-fixture report-only skipped-execution decision inside `cpd_paper_offline_report`. It
  consumes the configured-runtime smoke row, keeps runtime execution false, keeps all real runtime
  counters at zero, and at that stage advanced the next gate to configured-runtime lane review.
- [2026-05-20 CPD Paper Newton Engine-Builder Configured-Runtime Lane-Review Contract](2026-05-20-cpd-paper-newton-engine-builder-configured-runtime-lane-review-contract.md):
  single-fixture report-only claim-boundary review inside `cpd_paper_offline_report`. It consumes
  the configured-runtime execution row, keeps real runtime evidence and runtime compatibility
  false, keeps all real runtime counters at zero, and advances the current next gate to
  configured-runtime run.
- [2026-05-19 CPD Paper Newton Engine-Builder Gate Consolidation](2026-05-19-cpd-paper-newton-engine-builder-gate-consolidation.md):
  anti-overdesign decision record for the Newton engine-builder lane. It keeps the already closed
  boundary-preflight, environment-probe, and API-surface slices as evidence, retires separate
  future import-boundary-preflight/import-contract gates from the plan, and defined
  `paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract` as the consolidated
  post-API-surface gate.
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
