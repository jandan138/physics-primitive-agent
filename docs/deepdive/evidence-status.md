# Evidence Status

This file separates current evidence from future claims. See [message-map.md](message-map.md) for canonical DeepDive wording.

## Current Supported Claims

- The repository is a DeepDive-first bootstrap for a Newton Primitive Collision Compiler proposal.
- The safe intended framing is primitive-first, Newton-checker-planned, fallback-aware collision
  asset compilation; current executable evidence is config/USD/env diagnostics plus a
  geometry-only CPD-like smoke path.
- The first milestone is a non-LLM primitive baseline plus Newton diagnostic checker.
- LLM/VLM should be deferred until the non-LLM baseline shows value.
- The proposal requires explicit fallback to convex decomposition, SDF, hydroelastic, convex mesh, or manual review.
- The current executable surface can report config dry-runs, USD asset-open smoke diagnostics,
  Newton source import diagnostics, and environment-readiness diagnostics.
- The current executable surface can run a geometry-only CPD-like face-merge smoke path that
  extracts a USD mesh, fits restricted `box`/`sphere`/`capsule` primitive candidates plus an
  opt-in offline `capped_cylinder` proposal proxy, greedily merges adjacent face groups by
  weighted excess volume, and emits a JSON diagnostic report.
  The plain-language explanation is in
  [CPD-like face-merge explainer](../reference/cpd-like-face-merge-explainer.md).
- The current executable surface can run an opt-in geometry-only CPD-like component-merge gate
  that tries disconnected-component pairwise merge candidates after topology adjacency merges are
  exhausted, and reports AABB-normalized excess-volume accounting.
- The current executable surface can run `cpd_like_offline_objective`, an offline
  paper-aligned surrogate objective report over the CPD-like baseline. It reports primitive-budget
  pressure, AABB-normalized volume proxy, raw Eq.4-like and AABB-normalized merge-excess
  accounting, assigned-point containment proxy, unsupported paper primitive gaps,
  component/fallback labels, and structured Eq.4 alignment metadata. This is diagnostic
  accounting, not Eq.4 implementation, collision-quality evidence, or full CPD reproduction. The
  alignment boundary is documented in
  [CPD objective report alignment](../reference/cpd-objective-report-alignment.md): design-aligned
  with the paper story, not mathematically paper-faithful.
- The current executable surface can run `cpd_like_synthetic_objective_comparison`, a command-only
  deterministic synthetic comparison over three in-memory toy meshes. It compares topology-only
  and component-merge objective accounting for inspection. This is not benchmark evidence,
  collision-quality evidence, or full CPD reproduction.
- The current executable surface can run `cpd_like_cost_guided_synthetic_objective_comparison`, a
  focused CPD-like cost-guided merge-search smoke that turns AABB-normalized merge-excess into a
  decision-making cost and compares old/new diagnostic accounting on deterministic synthetic
  fixture. This is not benchmark evidence, collision-quality evidence, paper-faithful
  optimization, or full CPD reproduction.
- The current executable surface can run `cpd_like_expected_failure_synthetic_workbench`, a
  command-only deterministic expected-failure synthetic workbench over known CPD-paper gaps. It
  reports expected, observed, missing, and unexpected diagnostic flags for each fixture.
  `smoke_passed` means expected limitations were reported, not decomposition success, benchmark
  evidence, collision-quality validation, or full CPD reproduction.
- The current executable surface can run an opt-in offline capped-cylinder proxy objective smoke.
  In that named report, the unsupported paper primitive gap decreases from 3 to 2:
  `frustum` and `trapezoidal_prism` remain unsupported. This is not Newton support,
  collision-quality evidence, paper-faithful primitive fitting, or full CPD reproduction.
- The current CPD paper-story position is documented as a reproduction workbench, not as a
  paper-faithful implementation. See
  [CPD paper story status](../reference/cpd-paper-story-status.md).
- The current executable surface can convert the CPD-like geometry report into a common collision
  package and run `newton_contact_smoke`, a contact-only Newton canary for representative
  Newton-mapped primitive types.
- The current executable surface can run `newton_drop_settle`, a named task-level Newton smoke
  diagnostic over the capped bed CPD-like collision package, with explicit solver settings,
  final-contact, final-speed, support-height metrics, and failure labels.
- The current executable surface can run `newton_sphere_rain`, a named task-level Newton smoke
  diagnostic over the capped bed CPD-like collision package, with explicit solver settings,
  sphere-grid initial conditions, package-probe contact-density proxy metrics, and failure labels.
- The current executable surface can map and construct Newton diagnostic shapes for a synthetic
  native primitive bundle containing `box`, `sphere`, `capsule`, `cylinder`, `cone`, and
  `ellipsoid`, and can run clean-env contact, drop/settle, and sphere-rain smokes for that
  synthetic package. This is diagnostic-path evidence, not broad asset evidence or proof that the
  CPD-like generator emits the new native kinds by default.
- The current clean local Python/Newton environment-readiness evidence is `smoke_passed` for
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`, Newton source commit
  `96713fa965463b69c229a4d30582c733ff3526bb`, and local RTX 4090 hardware.
- The 2026-05-14 CPD-like bed smoke record reports `smoke_passed` for the first 256 extracted bed
  mesh triangles, reduced to 32 restricted primitives, using the clean Newton Python environment.
- The 2026-05-14 Newton drop/settle record reports `smoke_passed` for the capped bed CPD-like
  collision package in the clean Newton Python environment, with all 32 primitives mapped and no
  floor-breach or unsettled failure label under the recorded `0.05m` support-height tolerance and
  `0.05m/s` final-speed threshold.
- The 2026-05-15 Newton sphere-rain record reports `smoke_passed` for the capped bed CPD-like
  collision package in the clean Newton Python environment, with all 32 primitives mapped, 9 probe
  spheres, max package-probe contact count 1, max contacted probe spheres 1, contact density proxy
  `0.1111111111111111`, and no failure labels under the recorded `0.05` minimum contact-density
  threshold.
- The 2026-05-15 Franka record reports `smoke_passed` for local Franka USD-open smoke and capped
  geometry-only CPD-like first-mesh smoke: 10384 mesh points, 128 capped faces, and 16 restricted
  primitive proposals. It remains excluded from aggregate claims.
- The 2026-05-15 CPD-like component-merge gate record reports `smoke_passed` for the capped bed
  geometry-only smoke: 1898 mesh points, 256 capped faces, 32 restricted primitive proposals,
  224 topology merges, 0 virtual component merges, and 0 blocked merges. Focused tests cover the
  virtual disconnected-component merge behavior.
- The 2026-05-15 CPD-like objective report record reports `smoke_passed` for the capped bed
  offline objective smoke: 32/32 primitive budget, 32/32 assigned-point containment proxy,
  accepted normalized merge-excess sum `0.000996148870132146`, normalized weighted primitive
  volume `0.0009961811821648128`, and 3 unsupported paper primitive types still outside the
  baseline.
- The 2026-05-15 CPD-like synthetic comparison record reports `smoke_passed` for three
  deterministic in-memory fixtures: adjacent square, disconnected pair, and blocked disconnected
  pair. It records fixture-level topology-only versus component-merge objective accounting without
  adding benchmark or collision-quality claims.
- The 2026-05-15 CPD-like cost-guided merge record reports `smoke_passed` for one deterministic
  in-memory fixture, `cost_guided_pair_choice`: the default topology-then-virtual policy takes one
  topology merge with accepted normalized merge-excess sum `0.010062106570764756`, while
  `cost_guided_pairwise` takes one virtual component merge with accepted normalized merge-excess
  sum `0.000055121`. This is old/new diagnostic accounting on a toy mesh, not collision-quality
  evidence.
- The 2026-05-15 CPD synthetic expected-failure workbench record reports `smoke_passed` for three
  deterministic known-gap fixtures: `restricted_primitive_vocabulary_gap`,
  `single_proxy_wraps_disconnected_components`, and `threshold_blocks_component_merge`. All three
  fixtures matched their expected diagnostic flags with no missing or unexpected flags.
- The 2026-05-15 CPD capped-cylinder proxy record reports `smoke_passed` for the opt-in offline
  capped bed objective smoke: 32/32 primitive budget, 32/32 assigned-point containment proxy,
  unsupported paper primitive count 2, and remaining unsupported paper primitive types
  `frustum` and `trapezoidal_prism`.
- The 2026-05-15 Newton native primitive bundle record reports `smoke_passed` for a synthetic
  six-primitive package in the clean Newton environment: contact canaries passed for all six
  representative kinds, drop/settle completed 480 steps with max contact count 10 and no failure
  labels, and sphere-rain completed 480 steps with contact density proxy 1.0 and no failure labels.

## Current Unsupported Claims

- General primitive fitting quality across arbitrary assets has not been evaluated.
- Task-level Newton diagnostic evidence beyond the recorded capped bed drop/settle and
  sphere-rain contact-density proxy smokes plus the synthetic native bundle smoke has not been
  evaluated.
- Real contact-stress measurement has not been implemented or calibrated.
- Whole-robot collider quality, articulation-aware robot simulation, and aggregate robot-class
  evidence have not been evaluated.
- The method beats CoACD, V-HACD, CPD-like decomposition, manual primitive colliders, or Newton-native approximate mesh modes.
- The approach improves robot policy training, real robot behavior, or deployment safety.
- LLM/VLM improves primitive generation.
- The compiler can replace convex decomposition.
- Full CPD paper reproduction has been implemented or evaluated.
- The face-merge baseline is the CPD paper algorithm.
- The component-merge gate is the CPD paper algorithm.
- The expected-failure synthetic workbench is a general failure detector, benchmark, validation
  suite, or proof that all bad decompositions are caught.
- The capped-cylinder proxy is paper-faithful primitive fitting, Newton capped-cylinder support,
  collision-quality evidence, benchmark evidence, or an asset/task improvement.
- The CPD-like generator emits `cylinder`, `cone`, or `ellipsoid` by default.
- The synthetic native primitive bundle proves broad asset quality, collision quality, benchmark
  performance, or paper-scope primitive coverage.
- Environment-readiness diagnostics imply Newton simulation readiness.

## Future Evidence Needed

For the 0-4 week proof point:

- broader small synthetic meshes with inspectable expected decompositions;
- per-run or DLC-worker readiness report with status `smoke_passed` from the selected worker
  Python;
- asset list with source, license, scale, and hashes;
- baseline parameters and versions;
- Newton version, solver settings, hardware, and deterministic seeds;
- task-level metrics for each asset;
- failure examples, fallback reasons, and unsupported regions;
- artifact paths for reports and configs.

For any LLM/VLM claim:

- non-LLM baseline results first;
- ablation comparing planner/critic/repair roles;
- evidence that LLM/VLM adds value beyond geometry and task heuristics;
- failure cases where language or vision semantics changes the decision.

## Strategic Story

Physical intelligence requires model outputs to be checked against physical constraints. Physics engines provide an executable diagnostic layer, and collision proxies are one of the first contracts that layer depends on.

## Narrow First Milestone

The first local clean Newton runtime readiness gap is resolved, a geometry-only CPD-like primitive
proposal smoke path exists, a contact-only Newton canary exists, and the first two named task
smokes exist for the capped bed asset: drop/settle and sphere-rain contact-density proxy. A narrow
Franka USD-open and first-mesh CPD-like geometry smoke now broadens asset-class intake without
making robot-quality claims. The first CPD-like algorithmic extension is an opt-in
component-merge gate with explicit merge-cost reporting, still below full CPD reproduction. The
first synthetic objective comparison now gives deterministic inspection cases for topology-only
versus component-merge accounting. A focused cost-guided merge-search smoke now turns
AABB-normalized merge-excess into an opt-in synthetic merge decision. A deterministic
expected-failure workbench now converts three known CPD-paper gaps into diagnostic flags. Next use
those expected limitations, the capped-cylinder proxy report, and the synthetic native primitive
bundle to compare native-supported packages against the current `box`/`sphere`/`capsule` generator
path before changing asset claims or adding LLM/VLM. Report failures and fallback behavior as
first-class evidence.

## Current Non-Goals

No safety guarantee, real-world transfer claim, deployment readiness, benchmark superiority claim, primitive-only sufficiency claim, or complete replacement of convex decomposition.
