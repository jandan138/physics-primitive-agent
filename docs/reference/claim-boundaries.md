# Claim Boundaries

This file is the source of truth for reviewer-facing claims. If a stronger claim becomes
necessary, add the evidence requirement here before using it in the DeepDive package.

## Allowed Current Claims

- The repository is a DeepDive-first proposal and bootstrap, not a completed compiler.
- The intended direction is primitive-first, Newton-checker-planned, fallback-aware collision
  asset generation for Newton workflows, with named Newton diagnostic records required for any
  simulation-checked wording.
- The first proof point is diagnostic: measure whether primitive collision contracts expose
  failures that mesh-only or visual-only asset review would miss.
- The Physical Intelligence Center story is that AI models need physical safety constraints;
  physics engines provide an executable diagnostic layer for those constraints.
- The current code defines installable package contracts, config loading, dry-run reporting, USD
  asset-open smoke diagnostics, Newton source import diagnostics, and environment-readiness
  diagnostics.
- The current code can materialize manifest USD assets into ignored repo-local
  `assets/raw/mirrors/` paths and prefer those local paths at runtime when present. Current bed
  materialization records the material/texture closure; current Franka materialization records a
  USD layer mirror with unresolved `OmniPBR.mdl`. This is asset intake and reproducibility
  diagnostics, not benchmark evidence, collision-quality validation, compiler completeness,
  complete visual/material packaging, or deployment readiness.
- The current code can run a geometry-only CPD-like face-merge primitive proposal smoke path for
  a restricted primitive subset, when tied to a dated record and capped asset/config settings.
- The current code can run an opt-in geometry-only CPD-like component-merge gate that reports
  disconnected-component merge candidates and normalized excess-volume accounting for a restricted
  baseline. This is not full CPD paper reproduction or collision-quality evidence.
- The current code can run an offline paper-aligned surrogate objective report over a CPD-like
  decomposition. This reports primitive-budget pressure, AABB-normalized volume proxy,
  merge-excess accounting, assigned-point containment proxy, unsupported paper primitive gaps, and
  component/fallback labels. This is not full CPD paper reproduction, paper-faithful optimization,
  benchmark evidence, or collision-quality validation. "Paper-aligned" means design-aligned with
  the paper story's accounting categories, not the paper's collapse-cost rule, primitive
  weighting, or search procedure.
- The current objective report can include structured Eq.4 alignment metadata that maps current
  surrogate merge-excess fields to the CPD paper's collapse-cost role for audit. This is metadata,
  not Eq.4 implementation, paper-faithful scoring, benchmark evidence, or collision-quality
  validation.
- The documentation can define a planned `paper_faithful_offline` status for future
  fixture-scoped paper mechanics. That status is not currently supported by code. When implemented,
  it may only describe the declared offline fixture scope and must remain separate from full CPD
  paper reproduction, Newton runtime support, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The current code can run a command-only partial `cpd_paper_offline_report` over
  `paper_single_box`, `paper_two_face_merge`, `paper_three_face_chain`,
  `paper_disconnected_components`, `paper_component_pair_threshold_blocked`, `paper_frustum_like`,
  `paper_trapezoid_prism_like`, and `paper_nested_primitive` synthetic fixtures. It reports
  triangle-only mesh intake, paper-side operator audit fields, current surrogate OBB/sphere rows,
  an offline paper-shaped capsule axis fit-audit row, offline-only flat-capped-cylinder, frustum,
  and trapezoidal-prism fit-audit candidate rows, separate paper base collapse-cost versus
  weighted-priority-cost fields, a topology-only priority-queue trace with eager stale-pruning
  records, a threshold-disabled component-pair insertion trace, a finite-threshold component-pair
  blocked trace, and one explicit identity-axis OBB enclosed-primitive postprocess cull audit. The
  report remains `status: partial` with
  `paper_faithful_offline_supported: false`. This is fixture-scoped offline audit data, not
  `paper_faithful_offline`, not full CPD paper reproduction, not Newton runtime support, not
  package generation, not real-USD evidence, not benchmark evidence, and not collision-quality
  validation.
- The current code can run a command-only deterministic synthetic objective comparison over
  in-memory toy meshes. This compares topology-only and component-merge diagnostic accounting for
  inspection only. This is not benchmark evidence, broad asset evidence, full CPD paper
  reproduction, or collision-quality validation.
- The current code can run a focused geometry-only CPD-like cost-guided merge-search smoke that
  uses AABB-normalized merge-excess as a decision-making cost and compares old/new diagnostic
  accounting on a deterministic synthetic fixture. This is not full CPD paper reproduction,
  paper-faithful optimization, benchmark evidence, or collision-quality validation.
- The current code can run synthetic offline merge-step trace diagnostic accounting for the
  cost-guided merge-search smoke when `report_merge_trace: steps` is requested. The trace records
  accepted or blocked merge decisions, source faces/components, merged primitive type, and
  raw/normalized merge-excess for inspection. This is not a merge-policy improvement,
  collision-quality result, benchmark result, Newton task result, paper-faithful search trace, or
  CPD optimizer implementation.
- The current code can run a deterministic expected-failure synthetic workbench over in-memory
  fixtures that checks whether known CPD-like limitation flags remain visible. A `smoke_passed`
  result means expected limitation flags matched observed flags, not decomposition success,
  collision-quality validation, benchmark evidence, or full CPD paper reproduction.
- The current code can run an opt-in offline `capped_cylinder` geometry proposal proxy and report
  that the named objective smoke reduces unsupported paper primitive vocabulary from three types to
  two. This is primitive-vocabulary accounting for a restricted proposal baseline, not
  paper-faithful CPD primitive fitting, Newton support, benchmark evidence, or collision-quality
  validation.
- The current primitive roadmap is Newton-native first. The code can map and construct diagnostic
  Newton shapes for a synthetic package containing `box`, `sphere`, `capsule`, `cylinder`,
  `cone`, and `ellipsoid`, with dated clean-env contact, drop/settle, and sphere-rain smoke
  evidence. This is synthetic diagnostic-path evidence, not broad asset evidence or a claim that
  the CPD-like generator emits all six kinds by default.
- The current code can run an opt-in deterministic synthetic native fitting comparison where the
  six-kind Newton-native subset selects `cylinder`, `cone`, and `ellipsoid` on deterministic toy
  meshes, including a squat-cylinder fixture that exercises the controlled cylinder-axis search,
  and maps the resulting one-primitive packages through Newton shape mapping. This is synthetic
  fitting evidence, not collision-quality validation, default asset behavior, paper-faithful CPD
  primitive fitting, broad asset evidence, or completed bed/Franka evidence.
- The current synthetic native fitting comparison can include a candidate weighted-volume audit
  table that explains why the toy fixtures selected `cylinder`, `cone`, or `ellipsoid` under the
  current support-aware surrogate primitive-choice rule. This is synthetic diagnostic accounting,
  not a paper-faithful CPD optimizer, real-USD improvement evidence, benchmark evidence, or
  collision-quality validation.
- The current code can run a deterministic low-support native-extension admissibility fixture and
  can rank `cylinder`, `cone`, and `ellipsoid` candidates as selection-inadmissible when they have
  too few source faces or unique assigned points and a fallback primitive exists. This is a local
  diagnostic selection guard, not paper-faithful primitive fitting, not benchmark evidence, and not
  collision-quality validation.
- The current code can run a real-USD old/new native fitting diagnostic over capped
  `bed_dev_smoke` and capped `franka_import_smoke` first-mesh scope. The current support-aware
  dated run keeps bed at `32` boxes in both lanes and capped Franka at `32` boxes in both lanes,
  while reporting three Franka cheaper raw-cost cylinder candidates as support-blocked extension
  candidates. This is selection/accounting evidence, not evidence that boxes or cylinders improved
  those assets.
- The real-USD native fitting diagnostic can include a per-selected-cluster candidate audit
  summary that reports whether `cylinder`, `cone`, or `ellipsoid` was the cheapest raw-cost
  candidate and whether it was support-admissible under the current surrogate. This is diagnostic
  accounting for why the current lanes select their primitives, not a quality metric or native
  primitive improvement claim.
- The current code can run a real-USD candidate-loss diagnosis over capped bed and capped Franka
  native lanes. It reports per-cluster selected primitive ranks, extension-candidate margins,
  support-aware selection admissibility, simple cluster geometry hints, and likely surrogate
  bottleneck labels. This is diagnostic accounting, not collision-quality evidence, benchmark
  evidence, or a paper-faithful optimizer.
- The real-USD candidate-loss diagnosis can include next-slice triage metadata. It ranks
  near-miss extension candidates and low-support native-extension selections so the next synthetic
  fixture can be chosen from recorded accounting. This is planning metadata, not evidence that the
  ranked primitive kind is better.
- The current code can include a direct synthetic `cylinder_near_miss_cluster` fixture where `box`
  still wins, `cylinder` is support-admissible, and the relative weighted-volume gap is small.
  The fixture can be exposed through `cpd_like_near_miss_fixture_workbench`. This is a
  primitive-ranking diagnostic target for future fitting or merge/search work, not a native
  primitive success case and not collision-quality evidence.
- The current code can run `cpd_like_cylinder_near_miss_fit_ablation`, a synthetic offline report
  for the `cylinder_near_miss_cluster` fixture that records the current containing-cylinder radius
  and a pairwise radial lower bound. It can say that radial-center refinement cannot flip this
  fixture under containment and the current surrogate. This is diagnostic accounting, not a
  primitive-selection change, native primitive improvement, real-USD result, Newton task result,
  benchmark, collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_near_miss_scoring_sensitivity`, a synthetic offline
  report for the same fixture that computes the counterfactual cylinder score multiplier and cost
  reduction required to tie the selected box under the current weighted-volume surrogate. This is
  sensitivity accounting for planning, not a scoring-policy change, primitive-selection
  improvement, evidence that cylinder is better, real-USD result, Newton task result, benchmark,
  collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_near_miss_scoring_policy_ablation`, a synthetic
  offline report that applies a fixed counterfactual cylinder multiplier inside the report only.
  It records that the cylinder near-miss fixture would flip under that hypothetical scoring policy
  and that a clearly boxy cuboid guardrail fixture remains `box`. This is report-only
  sensitivity/guardrail accounting for planning, not a default scoring-policy change,
  primitive-selection improvement, evidence that cylinder is better, evidence the multiplier is
  safe or calibrated, real-USD result, Newton task result, benchmark, collision-quality validation,
  or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_selection_probe`, a synthetic offline
  opt-in selection probe that applies the same fixed cylinder multiplier to candidate selection
  only when explicitly requested by the probe. It records that the near-miss fixture flips while a
  clearly boxy cuboid guardrail remains `box`. This is a synthetic opt-in primitive-choice probe,
  not a default scoring-policy change, primitive-selection improvement, evidence that cylinder is
  better, evidence the multiplier is safe or calibrated, real-USD result, Newton task result,
  benchmark, collision-quality validation, or CPD paper reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_package_probe`, an explicitly opt-in
  synthetic package probe that passes `primitive_score_multipliers={"cylinder": 0.88}` through
  `decompose_mesh`, produces a changed synthetic `CollisionPackage` for the near-miss fixture,
  keeps the boxy guardrail package unchanged, and records Newton shape-mapping coverage. This is
  package-path and mapping-accounting evidence only, not default package behavior, scoring
  calibration, real-USD evidence, Newton contact/task evidence, collision-quality validation,
  benchmark evidence, or CPD paper reproduction.
- The current code can run `cpd_like_controlled_merge_search_package_probe`, a command-only
  synthetic package-path probe that carries the existing `cost_guided_pair_choice` fixture through
  `CollisionPackage` generation for `topology_then_virtual` versus `cost_guided_pairwise` lanes and
  records Newton shape-mapping coverage. This is package-path and mapping-accounting evidence only,
  not a default merge-policy change, merge-policy superiority result, real-USD evidence, Newton
  contact/task evidence, collision-quality validation, benchmark evidence, or CPD paper
  reproduction.
- The current code can run `cpd_like_controlled_merge_search_newton_probe`, a synthetic Newton
  diagnostic over the changed `cost_guided_pair_choice` package pair. It runs named
  `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind the contact
  gate and records task status under recorded settings. This is synthetic task-smoke execution
  evidence for one changed merge/search package pair, not default merge behavior, merge-policy
  superiority, real-USD evidence, collision-quality validation, benchmark evidence, real
  contact-stress measurement, safety certification, or CPD paper reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_merge_report`, a command-only
  synthetic two-step lookahead merge/search diagnostic over one deterministic trap fixture. It
  records that `two_step_lookahead` changes the toy grouping relative to greedy
  `cost_guided_pairwise` and lowers projected two-step normalized merge-excess under the current
  surrogate. This is offline synthetic merge/search accounting only, not default merge behavior,
  merge-policy superiority, package-path evidence, Newton contact/task evidence, real-USD evidence,
  collision-quality validation, benchmark evidence, or CPD paper reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_package_probe`, a command-only
  synthetic package-path probe over the existing `lookahead_merge_trap` fixture. It converts greedy
  `cost_guided_pairwise` and opt-in `two_step_lookahead` decompositions into `CollisionPackage`,
  compares source-face groupings, and records Newton shape-mapping coverage. This is package-path
  and mapping-accounting evidence only; it does not change default merge behavior, rank merge
  policies, run Newton runtime tasks, touch real assets, measure collision geometry quality,
  compare against a benchmark suite, or complete paper-level reproduction.
- The current code can run `cpd_like_cost_guided_lookahead_newton_probe`, an explicitly opt-in
  synthetic Newton diagnostic over the lookahead-changed `lookahead_merge_trap` package pair. It
  runs named `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind
  per-lane contact gates and records task status under recorded settings. This is synthetic
  task-smoke status only; it does not change default merge behavior, rank merge policies, touch
  real assets, report bed or Franka results, measure collision geometry quality, compare against a
  benchmark suite, support deployment or certification conclusions, find or rule out broad failure
  modes, or complete paper-level reproduction.
- The current code can run `cpd_like_four_block_slice_report`, a command-only evidence map for the
  already recorded `cost_guided_lookahead` synthetic slice. It summarizes primitive
  fitting/selection, merge/search, offline diagnostics, and recorded Newton task-smoke evidence by
  linking to dated records. This report does not invoke decomposition, USD loading, package
  builders, Newton runtime tasks, real assets, benchmark measurement, collision-quality
  evaluation, policy ranking, deployment/certification checks, or paper-level reproduction.
- The current code can run `cpd_like_cylinder_scoring_policy_newton_probe`, an explicitly opt-in
  synthetic Newton diagnostic over the changed `cylinder_near_miss_cluster` package pair. It runs
  named `newton_contact_smoke`, `newton_drop_settle`, and `newton_sphere_rain` smokes behind the
  contact gate and records task status under recorded settings. This is synthetic task-smoke
  execution evidence for one opt-in changed package, not default package behavior, scoring
  calibration, real-USD evidence, collision-quality validation, benchmark evidence, real
  contact-stress measurement, safety certification, or CPD paper reproduction.
- The current code can run a gated real-USD Newton probe comparison for capped bed and capped
  Franka first-mesh packages: full package mapping, contact canary, then drop/settle and
  sphere-rain only after contact passes. This is named diagnostic smoke evidence under recorded
  settings, not collision-quality validation, benchmark evidence, or whole-robot Franka collider
  quality evidence.
- The current code can run a contact-only Newton canary for representative Newton-mapped primitive
  types from a CPD-like collision package. This is not task-level simulation evidence.
- The current code can run the named `newton_drop_settle` task-level smoke diagnostic for the
  capped bed CPD-like collision package under the recorded config and environment. This is not
  collision quality validation, benchmark evidence, or CPD paper reproduction.
- The current code can run the named `newton_sphere_rain` task-level smoke diagnostic for the
  capped bed CPD-like collision package under the recorded config and environment. This is a
  contact-density proxy smoke, not a real contact-stress measurement, collision quality validation,
  benchmark evidence, or CPD paper reproduction.
- The current code can open the recorded local Franka USD and run a capped geometry-only CPD-like
  smoke over the first extracted mesh. This is robot asset import and geometry smoke only, not
  whole-robot collider quality, articulated dynamics, aggregate robot evidence, or benchmark
  evidence.
- The current clean local Python/Newton environment-readiness report can be described as
  `smoke_passed` evidence for the named environment path, Newton source checkout, and hardware
  environment in the dated record.

## Claims Requiring Phase 0 Evidence

Use these only after a dated record links them to Phase 0 assets, configs, logs, and reports.

- A non-LLM primitive baseline has been tested on the 5-10 asset proof point.
- Newton checker probes have found or ruled out specific failure modes for specific assets.
- Robot asset coverage beyond the recorded Franka USD-open and first-mesh geometry smoke.
- A baseline comparison includes primitive count, fallback ratio, step time, contact count, and
  penetration or jitter measurements.
- A generated collision package is simulation-checked for a named task in a named environment,
  beyond the recorded capped-bed, capped-Franka first-mesh, synthetic native-bundle, synthetic
  cylinder scoring-policy, synthetic controlled merge-search, and synthetic lookahead smokes.
- A DLC-worker or experiment-specific Python/Newton environment has passed readiness checks for a
  named source checkout and hardware environment.

## Claims Requiring Phase 1 Or Phase 2 Evidence

Use these only after broader benchmark records exist.

- The approach improves a metric relative to bounding primitives, convex hulls, decomposition
  baselines, or VisACD when available.
- Checker-guided repair reduces fallback rate on a documented asset set.
- The system supports a repeatable asset ingestion workflow beyond the DeepDive proof point.
- LLM/VLM planning adds value beyond deterministic baselines.

## Forbidden Claims

- Do not claim the repository guarantees real-world safety.
- Do not claim the compiler is deployment-ready.
- Do not claim any package is certified safe.
- Do not claim the method is proven safe.
- Do not claim the method fully replaces convex decomposition, SDFs, or human review.
- Do not claim benchmark superiority before the benchmark record exists.
- Do not treat environment-readiness diagnostics as Newton simulation checker results.
- Do not treat asset mirror materialization as dataset licensing review, benchmark evidence,
  complete visual/material packaging, collision-quality validation, or deployment readiness.
- Do not claim full CPD paper reproduction before paper-scope primitive coverage, benchmark
  settings, and dated experiment records exist.
- Do not describe the CPD-like component-merge gate as the CPD paper algorithm; it is a restricted
  baseline extension and report-audit slice.
- Do not describe the offline objective report as a collision-quality metric or proof that the
  decomposition is good; it is diagnostic accounting for future algorithm work.
- Do not describe "paper-aligned surrogate objective report" as equivalent to a paper-faithful
  objective implementation.
- Do not describe Eq.4 alignment metadata as Eq.4 implementation, paper-faithful objective
  scoring, or proof that the current merge search matches the paper.
- Do not describe the synthetic objective comparison as benchmark evidence or proof that one merge
  policy is better; it is fixture-level diagnostic accounting.
- Do not describe the cost-guided merge-search improvement as the CPD paper optimizer or as proof
  that one decomposition is better collision geometry; it is a restricted algorithmic smoke slice
  under diagnostic objective accounting.
- Do not describe the expected-failure synthetic workbench as a benchmark, validation, failure
  detector, proof that the baseline catches bad decompositions, collision-quality score, safe
  collider rejection step, or complete coverage of CPD-like limitations.
- Do not describe the capped-cylinder proxy as paper-faithful capped-cylinder support, CPD
  primitive fitting implementation, Newton capped-cylinder support, collision-quality improvement,
  benchmark evidence, or asset/task improvement.
- Do not claim broad Newton-native primitive quality for `cylinder`, `cone`, or `ellipsoid`
  beyond the dated synthetic diagnostic-path, opt-in synthetic fitting, and capped real-USD
  diagnostic records. Do not claim the CPD-like generator emits these kinds by default for normal
  asset configs. Do not claim bed or Franka native-fitting improvement from the current
  support-aware real-USD records; bed and Franka currently select boxes, and the three
  support-blocked Franka cylinder candidates are surrogate accounting, not quality evidence.
- Do not describe the synthetic native selection audit as a quality metric, paper-faithful
  optimizer, proof that native primitives are broadly better, real-USD improvement, or collision
  validation. It is a candidate-cost diagnostic table over toy meshes.
- Do not describe support-aware native-extension admissibility as a paper objective, learned
  classifier, safety filter, or proof that low-support native primitives are bad. It is a local
  face/point support guard for the current diagnostic workbench.
- Do not describe the real-USD native probe comparison as a benchmark, collision-quality
  validation, whole-robot Franka collider-quality result, or native primitive improvement result.
- Do not describe the real-USD candidate audit summary as proof that the selected primitives are
  good. It is a surrogate candidate-accounting summary over selected clusters.
- Do not describe the real-USD candidate-loss diagnosis as a quality metric, benchmark result,
  proof that boxes or cylinders are better, or evidence that the Franka collider is good.
- Do not describe candidate-loss triage as an optimizer or as proof of the next algorithmic
  direction. It is a deterministic sorting aid for choosing the next synthetic diagnostic target.
- Do not describe the `cylinder_near_miss_cluster` fixture as a resolved near miss, a native
  fitting improvement, or a real-USD package improvement. It is a synthetic limitation target.
- Do not describe `cpd_like_cylinder_near_miss_fit_ablation` as fixing cylinder fitting or proving
  cylinder quality. It is a containment-preserving lower-bound diagnostic that keeps default
  selection and Newton packages unchanged.
- Do not describe `cpd_like_cylinder_near_miss_scoring_sensitivity` as improving the objective,
  calibrating scoring, proving boxes are wrong, or recommending a cylinder bias. It is
  counterfactual sensitivity accounting and does not apply the multiplier it reports.
- Do not describe `cpd_like_cylinder_near_miss_scoring_policy_ablation` as a new default scoring
  policy, calibrated objective, selection improvement, recommended cylinder bias, or Newton-checked
  flip. It is a report-only counterfactual over deterministic synthetic fixtures.
- Do not describe `cpd_like_cylinder_scoring_policy_package_probe` as a default package change,
  calibrated scoring policy, Newton diagnostic run, simulation-checked package, real-USD package
  improvement, or collision-quality result. It is an explicitly opt-in synthetic package and
  Newton shape-mapping summary only.
- Do not describe `cpd_like_controlled_merge_search_package_probe` as a default merge-policy change,
  merge-policy superiority result, Newton diagnostic run, simulation-checked package, real-USD
  package improvement, or collision-quality result. It is a single-fixture synthetic package-path
  and Newton shape-mapping summary only.
- Do not use the synthetic `cpd_like_controlled_merge_search_newton_probe` as evidence that
  `cost_guided_pairwise` is better than `topology_then_virtual`, that merge policy was validated,
  that real-USD/bed/Franka packages improved, or that collision quality was validated. It is a named
  synthetic task-smoke diagnostic over one changed package pair.
- Do not use the synthetic `cpd_like_cylinder_scoring_policy_newton_probe` as evidence that the
  cylinder multiplier is calibrated, that cylinder is better than box, that real-USD/bed/Franka
  packages improved, that failure modes were found or ruled out, or that collision quality was
  validated. It is a named synthetic task-smoke diagnostic over one opt-in changed package pair.
- Do not use CPD paper primitive-vocabulary completeness as a runtime support claim. Paper-only
  primitives remain offline diagnostics unless separately mapped and verified.

## Wording Rules

- Use "simulation-checked" only for artifacts with a named task-level Newton diagnostic record.
  Contact-only canary records do not qualify. For the recorded capped-bed drop/settle and
  sphere-rain smokes, prefer the exact diagnostic names unless reviewer context specifically needs
  the "simulation-checked" term.
- Use "simulation-verified" only after a specific verification standard is documented.
- Say "measure whether" instead of "prove whether" for research questions.
- Say "fallback-aware" instead of "fallback-free" unless a record shows zero fallback.
- Treat generated collision packages as safety-affecting artifacts, not as safety-certified
  artifacts.
- Prefer "diagnostic checker" over "verifier" in leadership-facing material.
- Prefer "higher-fidelity reference comparison" over "oracle" unless a task-specific reference
  standard is defined.
