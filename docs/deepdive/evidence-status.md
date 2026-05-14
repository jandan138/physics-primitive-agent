# Evidence Status

This file separates current evidence from future claims. See [message-map.md](message-map.md) for canonical DeepDive wording.

## Current Supported Claims

- The repository is a DeepDive-first bootstrap for a Newton Primitive Collision Compiler proposal.
- The safe project framing is primitive-first, simulation-checked, fallback-aware collision asset compilation.
- The first milestone is a non-LLM primitive baseline plus Newton diagnostic checker.
- LLM/VLM should be deferred until the non-LLM baseline shows value.
- The proposal requires explicit fallback to convex decomposition, SDF, hydroelastic, convex mesh, or manual review.
- The current executable surface can report config dry-runs, USD asset-open smoke diagnostics,
  Newton source import diagnostics, and environment-readiness diagnostics.
- The current executable surface can run a geometry-only CPD-like face-merge smoke path that
  extracts a USD mesh, fits restricted `box`/`sphere`/`capsule` primitive candidates, greedily
  merges adjacent face groups by weighted excess volume, and emits a JSON diagnostic report.
- The current clean local Python/Newton environment-readiness evidence is `smoke_passed` for
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`, Newton source commit
  `96713fa965463b69c229a4d30582c733ff3526bb`, and local RTX 4090 hardware.
- The 2026-05-14 CPD-like bed smoke record reports `smoke_passed` for the first 256 extracted bed
  mesh triangles, reduced to 32 restricted primitives, using the clean Newton Python environment.

## Current Unsupported Claims

- General primitive fitting quality across arbitrary assets has not been evaluated.
- Newton simulation checker results exist for CPD-like primitive proposals.
- The method beats CoACD, V-HACD, CPD-like decomposition, manual primitive colliders, or Newton-native approximate mesh modes.
- The approach improves robot policy training, real robot behavior, or deployment safety.
- LLM/VLM improves primitive generation.
- The compiler can replace convex decomposition.
- Full CPD paper reproduction has been implemented or evaluated.
- Environment-readiness diagnostics imply Newton simulation readiness.

## Future Evidence Needed

For the 0-4 week proof point:

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

The first local clean Newton runtime readiness gap is resolved, and a geometry-only CPD-like
primitive proposal smoke path exists. Next connect that proposal output to a named Newton
diagnostic checker before adding LLM/VLM. Report failures and fallback behavior as first-class
evidence.

## Current Non-Goals

No safety guarantee, real-world transfer claim, deployment readiness, benchmark superiority claim, primitive-only sufficiency claim, or complete replacement of convex decomposition.
