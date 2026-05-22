# DeepDive Documentation

This folder is the primary package for applying to DeepDive. The current goal is to earn support
for a focused simulation-checked proof point, not to claim completed research.

Use [message-map.md](message-map.md) as the canonical message source. Other DeepDive files should
link back to it when wording could drift.

## Reading Order

1. [Message Map](message-map.md): canonical leadership story, technical thesis, safe one-liner,
   proof point, support request, and unsafe claims.
2. [Application Draft](application.md): the direct DeepDive application.
3. [One-Page Summary](one-page-summary.md): concise reviewer brief.
4. [Pitch Outline](pitch-outline.md): 20-30 minute talk plan.
5. [Review Q&A](review-qa.md): hard questions organized by review dimension.
6. [Evidence Status](evidence-status.md): supported and unsupported claims.

## Strategic Story

Collision packages are safety-affecting artifacts for physical-intelligence simulation. Primitive
collider generation should be treated as candidate generation; Newton diagnostics decide whether a
package can be accepted, rejected, or routed to fallback.

## Narrow First Milestone

The first proof point is a non-LLM candidate generator plus Newton checker loop:

- generate or import primitive candidates;
- run body-state, drop/settle, and contact-stress checks;
- preserve robot link/joint boundaries when robot assets are in scope;
- run articulation smoke gates for a reproducible robot asset if available;
- record fallback decisions.

LLM/VLM work starts only after this deterministic loop shows measurable value.

## Current Non-Goals

- No claim of physical safety guarantee.
- No real-world transfer or deployment readiness claim.
- No broad benchmark superiority or full-simulation speedup claim.
- No novelty claim for primitive collider generation itself.
- No complete replacement of convex decomposition.
- No whole-robot articulated-dynamics claim before dedicated records exist.
