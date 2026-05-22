# 2026-05-22 DeepDive Direction Shift To Simulation-Checked Robotics

## Date

2026-05-22

## Status

Complete for current-facing documentation alignment. Not complete as implementation, benchmark
evidence, whole-robot robot-operation evidence, default selector policy, collision-quality
validation, or safety evidence.

## Decision

The DeepDive story shifts from "primitive-first CPD-like collision compiler" toward
"simulation-checked primitive collider compiler."

The new framing treats CPD-style primitive decomposition as a related candidate generator and
baseline. The proposed contribution is the downstream acceptance layer:

- generated primitive packages remain candidates until Newton diagnostics run;
- body-state, contact, and task behavior decide accept/reject/fallback;
- robot packages require link-aware boundaries and articulation smoke checks before any whole-robot
  claim;
- fallback is an expected compiler output, not a hidden failure.

## Evidence Basis

The direction is motivated by the capped bed/Franka cylinder mechanism records:

- the bed cylinder failure is a full-compound package effect;
- the strongest recorded mechanism is COM/inertia body-state sensitivity from one large flat
  cylinder;
- recorded Franka cylinder packages pass in their smaller package context;
- an opt-in package body-state guard falls back only the flagged bed package while preserving the
  unflagged Franka cylinder package in the recorded Newton task smoke.

## Documentation Changes

- Rewrote the DeepDive message map, application draft, one-page summary, pitch outline, review Q&A,
  README, and evidence-status documents around simulation-checked acceptance.
- Rewrote the design scope, roadmap, evaluation plan, benchmark protocol, and architecture docs to
  include body-state, contact, and articulation gates.
- Replaced the long claim-boundaries page with the current canonical claim boundary for the new
  direction.
- Added `docs/reference/simulation-checked-primitive-collider-direction.md`.
- Updated the related-work and literature notes to position CPD-style work as adjacent related work
  rather than the project identity.
- Updated the DeepDive and Phase 0 config examples to name body-state and robot articulation gates.

## Claim Impact

Supported wording:

- "simulation-checked primitive collider generation" as the current direction;
- "CPD-style primitive decomposition is a candidate generator/baseline";
- "capped bed/Franka cylinder records motivate body-state package diagnostics";
- "robot-operation claims require future link-aware and articulation-smoke records."

Unsupported wording remains:

- full CPD reproduction;
- benchmark superiority;
- calibrated default selector policy;
- validated COM/inertia repair;
- whole-robot Franka performance;
- do not claim deployment readiness, real-world transfer, or a safety guarantee.

## Verification

- `python scripts/validate_docs.py`: passed.
- `python -m pytest tests/test_configs.py -q`: `4 passed`.
- `git diff --check`: passed.

## Next Action

Run docs validation, whitespace checks, and then start a new implementation goal for the
articulation-aware proof point if the direction is accepted.
