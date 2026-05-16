# Cylinder Near-Miss Fit Ablation Design

## Goal

Add a diagnostic-only report for the completed `cylinder_near_miss_cluster` fixture that answers
whether a legal cylinder radial fitting refinement could plausibly make the cylinder beat the
selected box under the current weighted-volume surrogate.

## Scope

This slice is synthetic and offline only. It does not change default primitive selection, merge
search, real USD packages, or Newton task execution.

## Design

The report will compare three quantities on the existing fixture:

- current selected box weighted volume;
- current support-admissible cylinder weighted volume;
- a radial lower-bound cylinder volume computed from the widest pairwise radial distance in the
  cylinder cross-section.

If the current cylinder radius already matches the pairwise lower bound, then radial-center
refinement cannot reduce the cylinder enough on this fixture without relaxing containment or
changing the objective. The report should recommend the next component as scoring, merge/search,
or a different fitting fixture rather than forcing this fixture to select cylinder.

## Output

Create `build_cpd_like_cylinder_near_miss_fit_ablation_report()` with:

- `stage: cpd_like_cylinder_near_miss_fit_ablation`;
- `claim_boundary: synthetic_cylinder_fit_ablation_not_collision_quality_validation`;
- one case, `cylinder_near_miss_cluster`;
- current ranking rows for `box` and `cylinder`;
- an `ablation` block containing current cylinder radius, pairwise radius lower bound, current
  cylinder volume, lower-bound cylinder volume, selected box volume, and whether the lower bound
  could beat the selected primitive;
- a `decision` block explaining the recommended next component.

Add a CLI flag:

```bash
python -m primitive_collision_compiler.cli --run-cpd-like-cylinder-near-miss-fit-ablation
```

## Claim Boundaries

Allowed claims:

- a synthetic fixture was used to triage one cylinder fitting question;
- the current fixture does not justify a radial-center-only cylinder fitting change;
- Newton task comparison is not triggered because generated packages do not change.

Forbidden claims:

- CPD reproduction;
- collision-quality validation;
- bed/Franka improvement;
- benchmark superiority;
- Newton deployment readiness.

## Success Criteria

- The new report is strict JSON serializable.
- The CLI emits the report and returns zero on `smoke_passed`.
- The report records that the legal radial lower bound does not beat the selected box.
- Existing near-miss behavior remains unchanged.
