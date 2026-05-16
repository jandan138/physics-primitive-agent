# Cylinder Scoring Policy Selection Probe Design

## Goal

Add a synthetic, offline, strictly opt-in selection probe for the cylinder near-miss branch.

The previous report-only ablation copied candidate rows and changed scores only inside the report.
This slice adds a small reusable selection path that can apply a primitive-kind multiplier before
candidate ranking, while keeping the default `fit_best_primitive()` and default decomposition path
unchanged.

## Scope

The probe covers two deterministic synthetic cases:

- `cylinder_near_miss_cluster`: default selection is `box`; opt-in cylinder multiplier selects
  `cylinder`.
- `boxy_cuboid_guardrail`: default selection is `box`; opt-in cylinder multiplier still selects
  `box`.

The multiplier is fixed at the existing report-only value `0.88` for this slice. It is not a
calibrated score, not a learned policy, and not applied to real USD package generation.

## Architecture

Add an optional primitive multiplier path to candidate ranking. The default public path keeps the
current behavior by using no multipliers. The probe report calls the opt-in path explicitly and
records both default and opt-in rankings for each synthetic case.

The report should include:

- default selected primitive;
- opt-in selected primitive;
- whether the default behavior changed;
- whether the opt-in probe changed the selection;
- per-candidate default rank, raw-cost rank, effective multiplier, effective score, and opt-in
  rank;
- a decision block that says Newton task comparison is not triggered because no default package
  changed.

## CLI

Add:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-scoring-policy-selection-probe
```

Expected status:

```text
smoke_passed
```

The CLI returns nonzero for `partial`, following the existing synthetic report convention.

## Claim Boundaries

Allowed wording:

- "synthetic opt-in scoring-policy selection probe";
- "candidate primitive-choice probe";
- "default package generation unchanged";
- "Newton task gate not triggered."

Forbidden wording:

- "default scoring policy changed";
- "cylinder is better";
- "scoring policy is safe or calibrated";
- "real-USD package improved";
- "Newton task quality improved";
- "CPD paper objective implemented."

## Verification

Required checks:

1. RED test that expects the opt-in ranking helper to flip `cylinder_near_miss_cluster` while
   default `fit_best_primitive()` still returns `box`.
2. RED test that expects the same helper to keep `boxy_cuboid_guardrail` at `box`.
3. RED report test that expects both cases, explicit opt-in/default separation, and no Newton
   task trigger.
4. RED CLI test for the new flag.
5. Green implementation with default paths unchanged.
6. JSON serialization check.
7. Docs, claim-boundary, registry, and record updates.
8. Multi-agent review before final status.
