# Sphere-Rain, Franka Smoke, And CPD-Like Component Merge Gate Design

## Date

2026-05-15

## Status

In progress.

## Context

The repository already has a geometry-only CPD-like face-merge baseline, a contact-only Newton
canary, and a named `newton_drop_settle` task smoke for the capped bed asset. The next work should
broaden the executable diagnostic surface without crossing the current claim boundaries.

This design covers three linked but separable slices:

- add `newton_sphere_rain` as a second named Newton task smoke;
- add a Franka/simple robot asset smoke path from the existing local manifest entry;
- add an opt-in CPD-like component-merge gate that makes disconnected-component merge behavior
  reviewable while still naming it as a baseline, not a reproduction.

## Claim Boundary

Allowed after this slice, if records and commands exist:

- `newton_sphere_rain` is a named task-level Newton smoke diagnostic for the recorded capped bed
  CPD-like collision package.
- Franka is a second asset-class import and CPD-like geometry smoke, not broad robot evidence.
- CPD-like reports expose opt-in component-merge and merge-audit metrics for a restricted baseline.

Still not allowed:

- full CPD paper reproduction;
- collision quality validation;
- benchmark superiority;
- deployment readiness or safety certification;
- broad asset/task coverage.

## Step 1: Newton Sphere-Rain

The probe should reuse the existing CPD-like report to `CollisionPackage` conversion and Newton
shape mapping. It should then build:

- static package shapes with `body=-1`, using the same mapping helpers as the contact canary;
- multiple dynamic spheres placed above the package footprint;
- XPBD solver settings owned by config;
- no committed run directory or large log.

The first version should be intentionally small and deterministic:

- one seed;
- a small grid such as 3x3 spheres;
- CPU device by default;
- JSON report only.

The report needs enough information to review failure modes:

- sphere count, radius, grid dimensions, spawn height, drop spacing;
- completed steps and finite-state status;
- max and final contact count;
- package-probe contact-density proxy, plus min-height fields for review; the MVP does not infer
  a per-sphere interaction count from final height;
- failure labels such as `no_contact_observed`, `no_final_contact`, `non_finite_state`, and
  `insufficient_contact_density`.

The safe evidence level is `newton_sphere_rain_task_smoke`.

## Step 2: Franka Asset Smoke

The manifest already records `franka_import_smoke`. This slice should add a small config that
selects that role and runs the same geometry-only CPD-like path with capped source faces.

Franka should remain excluded from aggregate claims for now because:

- it is a robot asset class, not the same distribution as the bed smoke;
- the current loader extracts the first mesh only;
- the current CPD-like baseline has no robot-joint or articulated-body semantics;
- there is no Newton task record for Franka yet.

The supported claim is only that this repository can open the Franka USD and run the capped
geometry-only CPD-like primitive proposal smoke path under the recorded environment.

## Step 3: CPD-Like Component Merge Gate

The current baseline already fits `box`, `sphere`, and `capsule` candidates and greedily merges
adjacent face clusters by weighted excess volume. The next paper-story slice should not attempt
full CPD primitive coverage. It should add an opt-in stage that keeps the default topology-only
behavior unchanged and, when enabled, tries pairwise disconnected-component merges after
topological adjacency merges are exhausted.

The report should expose:

- per-primitive source face count;
- per-primitive source component IDs;
- per-primitive merge cost weight;
- report-level mesh AABB volume;
- report-level target primitive count;
- report-level initial and final component count;
- topology merge count;
- virtual component merge count;
- blocked merge count;
- optional AABB-normalized excess-volume threshold;
- merge-cost summary;
- normalized total weighted volume.

This is valuable because it makes one CPD-like decomposition decision visible: whether disconnected
components can be merged, and at what normalized excess-volume cost. The stage should be named
`cpd_like_component_merge_gate`, not CPD reproduction.

## Verification Strategy

Use TDD for executable changes:

- schema tests for any new report dataclass or JSON fields;
- pure evaluation tests for sphere-rain failure labels;
- CLI tests for stdout JSON cleanliness and config parsing;
- config tests to keep machine paths in manifests, not configs;
- smoke commands in the clean Newton Python environment for real USD/Newton evidence.

Final verification must include:

- `python -m pytest -q`;
- `python scripts/validate_docs.py`;
- `git diff --check`;
- real clean-env smoke commands for the new configs where the local assets and Newton runtime are
  available.
