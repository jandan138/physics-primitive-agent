# Low-Support Native Extension Design

## Goal

Prevent Newton-native extension primitives such as `cylinder`, `cone`, and `ellipsoid` from
winning a CPD-like selection on very small face clusters unless the cluster has enough geometric
support to make that selection inspectable.

## Context

The current real-USD candidate-loss triage reports three capped Franka native-lane `cylinder`
selections where each selected cluster has only two source faces and four unique points. That is a
planning signal, not quality evidence. The next slice should turn that signal into a controlled
synthetic fixture and a narrow selection rule before rerunning bed/Franka diagnostics.

## Design

The selection rule belongs at primitive selection time, not only in reports. `fit_best_primitive`
will still build the same candidate list, but it will rank Newton-native extension candidates as
selection-inadmissible when they lack minimal source-face or unique-point support and a fallback
legacy primitive is available. Candidate audits will expose the admissibility decision so the report
can explain when a cheaper extension lost because it was under-supported rather than because its
volume proxy was higher.

The first support gate is deliberately small:

- `cylinder`, `cone`, and `ellipsoid` are extension candidates.
- An extension candidate needs at least three source faces.
- An extension candidate needs at least five unique assigned points.
- If the primitive subset contains only extension candidates, selection still returns the best
  available candidate instead of failing.

This is a diagnostic guardrail, not a paper-faithful CPD objective. It should preserve existing
synthetic fixtures that have enough support while changing low-support patch behavior.

## Testing

Add tests before production code:

- a low-support two-triangle patch where `cylinder` has lower weighted volume than `box`, but
  `box` wins because the cylinder is inadmissible;
- an audit/report test showing the cheaper extension is labeled as support-blocked;
- existing native synthetic fixtures continue to select `cylinder`, `cone`, and `ellipsoid` where
  they have sufficient support.

## Documentation

Update the CPD paper story docs, latest diagnostic loop explainer, claim boundaries, dated records,
and experiment registry to describe the new support-aware slice without claiming paper reproduction,
collision-quality validation, or broad Newton-native primitive superiority.
