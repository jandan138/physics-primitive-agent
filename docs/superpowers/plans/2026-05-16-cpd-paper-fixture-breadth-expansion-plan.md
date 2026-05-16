# CPD Paper Fixture Breadth Expansion Plan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a durable offline-only fixture-breadth expansion plan for the nine blocking
`paper_faithful_offline_scope_audit` rows.

**Architecture:** This is a documentation gate, not an algorithm slice. Create one reference page
that maps scope-audit blockers to planned synthetic fixtures, then update index/reference/record
docs so the next code slice is Batch A rather than bed/Franka, Newton, package generation, or
benchmark work.

**Tech Stack:** Markdown docs, docs validators, pytest.

---

### Task 1: Create The Reference Fixture Plan

**Files:**

- Create: `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`

- [ ] Add a status preamble:

```markdown
# CPD Paper Fixture Breadth Expansion Plan

This page turns the completed `paper_faithful_offline_scope_audit` blockers into planned
synthetic fixture coverage. It is a planning document, not experiment evidence, not a new
implementation, and not a claim that `paper_faithful_offline` is supported.
```

- [ ] Add a scope section with these boundaries:

```markdown
## Scope

The plan answers:

- which blocking paper-lane criteria need more synthetic fixture breadth;
- which future fixture ids should be added first;
- what each fixture must record when implemented;
- which claims remain blocked.

The plan does not:

- add new fixtures to `cpd_paper_offline_report`;
- generate a `CollisionPackage`;
- run Newton;
- load bed, Franka, or other real USD assets;
- run benchmarks;
- support collision-quality, deployment, or safety-certification claims.
```

- [ ] Add the five batch table from the design spec, exactly covering:

```text
Batch A: paper_mixed_face_preprocess_operator, paper_degenerate_preprocess_face_drop,
paper_concave_polygon_rejected
Batch B: paper_rotated_box_fit, paper_offset_sphere_fit, paper_off_axis_capsule_fit,
paper_flat_capped_cylinder_axis_fit, paper_tapered_frustum_fit,
paper_asymmetric_trapezoid_fit
Batch C: paper_branching_cost_order, paper_equal_cost_queue_tie,
paper_nonzero_threshold_block
Batch D: paper_component_pair_multi_candidate_order, paper_component_pair_cap_skipped
Batch E: paper_rotated_nested_primitive, paper_cross_type_enclosure_boundary
```

- [ ] Add one row per fixture with these columns:

```text
Fixture id | Covers | Geometry idea | Future report additions | Future tests | Non-goals | Claim boundary
```

- [ ] Add the recommended first implementation slice:

```text
paper_fixture_breadth_batch_a
-> source/preprocess/intake/operator fixture expansion
-> report remains partial
-> no package generation, Newton, real USD, or benchmark work
```

### Task 2: Update Existing Reference Docs

**Files:**

- Modify: `docs/index.md`
- Modify: `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- Modify: `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- Modify: `docs/reference/cpd-paper-story-status.md`
- Modify: `docs/reference/claim-boundaries.md`
- Modify: `docs/deepdive/evidence-status.md`

- [ ] Link `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md` from the CPD paper plan
  section in `docs/index.md`.

- [ ] Update the index current-status paragraph so the next paper-lane gate is:

```text
paper_fixture_breadth_batch_a
```

after the new fixture-breadth plan.

- [ ] Update the gap matrix recommended next slice so it says the fixture-breadth plan now exists
  and the next code slice is Batch A.

- [ ] Update the offline lane spec next implementation slice from
  `paper_fixture_breadth_expansion_plan` to `paper_fixture_breadth_batch_a`.

- [ ] Update the paper story status timeline and recommended next slices with the same Batch A
  wording.

- [ ] Update claim boundaries and DeepDive evidence status to say the fixture-breadth plan is a
  documentation-only planning artifact and not new executable evidence.

### Task 3: Add A Dated Record

**Files:**

- Create: `docs/records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md`
- Modify: `docs/records/README.md`

- [ ] Add a record with:

```markdown
# 2026-05-16 CPD Paper Fixture Breadth Expansion Plan

## Date

2026-05-16

## Status

Complete
```

- [ ] The record must state that this is documentation-only and does not implement fixtures.

- [ ] Add a verification section that initially lists exact commands and pending results:

```text
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

- [ ] Add the record link to `docs/records/README.md`.

### Task 4: Multi-Agent Review

**Files:**

- Review only; do not edit during this task.

- [ ] Dispatch at least two read-only review agents:

```text
Agent 1: fixture-plan completeness versus the nine blocking scope-audit rows.
Agent 2: docs/claim-boundary review for overclaims and stale next-gate wording.
```

- [ ] Fix Critical and Important findings.

- [ ] Record review findings and fixes in
  `docs/records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md`.

### Task 5: Verify And Commit

**Files:**

- All files changed in Tasks 1-4.

- [ ] Run:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
python -m pytest -q
```

- [ ] Update the dated record with exact pass results.

- [ ] Run the docs validators and whitespace check again after updating the record:

```bash
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```

- [ ] Commit and push:

```bash
git add docs/index.md docs/deepdive/evidence-status.md docs/reference/claim-boundaries.md docs/reference/cpd-paper-reproduction-gap-matrix.md docs/reference/cpd-paper-faithful-offline-lane-spec.md docs/reference/cpd-paper-story-status.md docs/reference/cpd-paper-fixture-breadth-expansion-plan.md docs/records/README.md docs/records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md docs/superpowers/specs/2026-05-16-cpd-paper-fixture-breadth-expansion-plan-design.md docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md
git commit -m "docs: plan CPD paper fixture breadth expansion"
git push
```
