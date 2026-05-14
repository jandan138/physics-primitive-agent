# Evidence Status

This file separates current evidence from future claims. See [message-map.md](message-map.md) for canonical DeepDive wording.

## Current Supported Claims

- The repository is a DeepDive-first bootstrap for a Newton Primitive Collision Compiler proposal.
- The safe project framing is primitive-first, simulation-checked, fallback-aware collision asset compilation.
- The first milestone is a non-LLM primitive baseline plus Newton checker/verifier.
- LLM/VLM should be deferred until the non-LLM baseline shows value.
- The project explicitly preserves fallback to convex decomposition, SDF, hydroelastic, convex mesh, or manual review.

## Current Unsupported Claims

- Primitive fitting works.
- Newton checker results exist.
- The method beats CoACD, V-HACD, CPD-like decomposition, manual primitive colliders, or Newton-native approximate mesh modes.
- The approach improves robot policy training, real robot behavior, or deployment safety.
- LLM/VLM improves primitive generation.
- The compiler can replace convex decomposition.

## Future Evidence Needed

For the 0-4 week proof point:

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

Build a non-LLM primitive baseline and Newton checker/verifier before adding LLM/VLM. Report failures and fallback behavior as first-class evidence.

## Current Non-Goals

No safety guarantee, real-world transfer claim, deployment readiness, benchmark superiority claim, primitive-only sufficiency claim, or complete replacement of convex decomposition.
