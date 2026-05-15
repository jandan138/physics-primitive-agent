# Candidate Loss Diagnosis Design

## Goal

Complete the five-step post-mirror CPD-like slice: lock the current real-USD baseline, explain why
remaining native real-USD box selections beat extension candidates, make one controlled primitive-fitting improvement,
verify it on synthetic fixtures, and re-run bed/Franka through the existing Newton-gated probes.

## Scope

This slice adds diagnostic and algorithmic smoke evidence only. It does not claim full CPD paper
reproduction, benchmark quality, native primitive improvement on bed/Franka, whole-robot Franka
collider quality, or safety certification.

## Design

Add a new real-USD report stage:

```text
cpd_like_real_usd_candidate_loss_diagnosis
```

It reuses the existing real-USD native comparison artifacts and adds per-cluster native-lane
diagnostics:

- selected primitive kind and rank;
- ranked candidate costs for the native subset;
- best Newton-native extension candidate and selected-minus-extension cost margin;
- cluster geometry hints such as face count, point count, AABB extents, and aspect ratios;
- simple diagnosis labels for box-selected clusters where extension candidates lose.

The report also records a baseline-lock summary for the current old/new real-USD lanes. After the
controlled cylinder-axis update, bed remains a box-only native lane, while capped Franka's native
lane selects three cylinders under the current surrogate.

## Controlled Algorithm Change

The current cylinder fitter uses the longest span axis. That is good for rods but bad for squat
cylinders or disk-like meshes, where the cylinder axis should be the short thickness direction.

Change only the `cylinder` proxy fit so it evaluates each candidate axis and picks the containing
cylinder with the lowest weighted volume. This keeps the existing conservative containment model,
does not alter Newton mapping, and is testable on an inspectable synthetic squat-cylinder fixture.

## Verification

Required checks:

- targeted pytest for primitive fitting, synthetic native fitting, real-USD diagnosis, and CLI;
- strict JSON serialization for the new report;
- generated synthetic native fitting report includes the new squat-cylinder fixture;
- generated bed/Franka reports use local mirrors and preserve the current claim boundary;
- existing Newton contact/task gates remain unchanged;
- docs validation and whitespace checks pass.

## Claim Boundary

Allowed wording: candidate-loss diagnosis, controlled cylinder fitting smoke, synthetic fixture
improvement, capped bed/Franka diagnostic rerun.

Disallowed wording: CPD reproduced, benchmark improvement, collision-quality validation, native
primitive improvement on bed/Franka unless a dated report actually shows it, whole-robot Franka
collider quality, safety certification.
