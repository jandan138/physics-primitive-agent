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
  the paper story's accounting categories, not the paper's exact objective formula or search
  procedure.
- The current objective report can include structured Eq.4 alignment metadata that maps current
  surrogate merge-excess fields to the CPD paper's collapse-cost role for audit. This is metadata,
  not Eq.4 implementation, paper-faithful scoring, benchmark evidence, or collision-quality
  validation.
- The current code can run a command-only deterministic synthetic objective comparison over
  in-memory toy meshes. This compares topology-only and component-merge diagnostic accounting for
  inspection only. This is not benchmark evidence, broad asset evidence, full CPD paper
  reproduction, or collision-quality validation.
- The current code can run a focused geometry-only CPD-like cost-guided merge-search smoke that
  uses AABB-normalized merge-excess as a decision-making cost and compares old/new diagnostic
  accounting on a deterministic synthetic fixture. This is not full CPD paper reproduction,
  paper-faithful optimization, benchmark evidence, or collision-quality validation.
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
  beyond the recorded capped-bed drop/settle and sphere-rain smokes.
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
