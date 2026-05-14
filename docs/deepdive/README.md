# DeepDive Documentation

This folder is the primary package for applying to DeepDive. The current goal is to earn support for a focused first milestone, not to claim completed research.

Use [message-map.md](message-map.md) as the canonical message source. Other DeepDive files should link back to it when wording could drift.

## Reading Order

1. [Message Map](message-map.md): canonical leadership story, technical thesis, safe one-liner, unsafe claims, 4-week proof point, and support request.
2. [Application Draft](application.md): the direct DeepDive application.
3. [One-Page Summary](one-page-summary.md): concise reviewer brief.
4. [Pitch Outline](pitch-outline.md): 20-30 minute talk plan.
5. [Review Q&A](review-qa.md): hard questions organized by review dimension.
6. [Evidence Status](evidence-status.md): supported and unsupported claims.

## Strategic Story

Physical intelligence needs AI models that respect physical safety constraints. Physics engines matter because they provide executable diagnostic layers: under specified simulator assumptions, tasks, and metrics, they can expose candidate collision-proxy failures before expensive physical trials or deployment decisions.

Collision geometry is a low-level safety interface. If the collision proxy is under-conservative, a policy can appear to move through objects; if it is over-conservative, valid grasps or paths may be rejected. The project frames collision asset compilation as infrastructure for finding those errors, not as a safety guarantee.

## Narrow First Milestone

The first 0-4 week proof point is a non-LLM primitive baseline plus Newton checker/verifier:

- generate simple primitive proposals for a small asset set;
- run Newton checks for named tasks and metrics;
- reject or flag failures;
- record when fallback to CoACD, SDF, or other existing methods is required.

LLM/VLM work starts only after this non-LLM baseline shows measurable value.

## Current Non-Goals

- No claim of physical safety guarantee.
- No real-world transfer or deployment readiness claim.
- No benchmark superiority claim.
- No complete replacement of convex decomposition.
- No claim that primitive-only assets are sufficient for precision tasks.
- No LLM/VLM claim before the non-LLM baseline is evaluated.
