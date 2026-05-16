# CPD Latest Diagnostic Loop Explainer

This page explains the latest candidate-loss, cylinder-axis, and support-aware admissibility loop
in the story of reproducing Convex Primitive Decomposition for Collision Detection. It is a
teaching note and navigation aid, not new experiment evidence.

## One-Sentence Version

The latest work did not reproduce the CPD paper algorithm. It built a small, repeatable diagnostic
loop that can explain a primitive-selection weakness, gate a report-only scoring idea through
synthetic selection/package probes, and run synthetic contact-gated Newton task smokes without
changing the claim boundary.

## The Paper Story In Plain Terms

The CPD paper's high-level story is:

```text
complex mesh
-> decompose it into a small set of convex primitives
-> use those primitives for collision detection
-> evaluate whether collision detection is better
```

The repository is still below that goal. The latest repository story is:

```text
real USD or synthetic mesh
-> simple CPD-like primitive proposals
-> candidate-cost accounting
-> one controlled fitting change
-> CollisionPackage
-> Newton contact/task smoke gates
-> dated record and claim-boundary update
```

The difference matters. The paper is about finding a high-quality decomposition. The current
repository workbench is about building the machinery needed to inspect and improve a future
decomposition method without overclaiming.

## What Was Added In This Slice

### 1. Candidate-Loss Diagnosis

The candidate-loss diagnosis asks, for each selected real-USD cluster:

```text
What primitive was selected?
What other Newton-native candidates were available?
Did cylinder/cone/ellipsoid lose because their surrogate cost was higher?
Did any extension candidate actually win?
What label should guide the next change?
```

In the current capped real-USD run:

- bed native lane selects `32` boxes;
- Franka native lane selects `32` boxes after support-aware admissibility blocks three low-support
  raw-cost cylinder wins;
- the remaining bed box clusters and Franka box clusters usually have extension candidates, but
  those candidates are either more expensive under the current weighted-volume surrogate or
  blocked by the support-aware guard.

This is useful because it turns "why are we still seeing boxes?" into reviewable rows. It does not
say the boxes are correct, only that the current local surrogate prefers them.

### 2. Controlled Cylinder-Axis Fitting

Before this slice, a `cylinder` candidate was fit with a narrower axis assumption. That can make a
cylinder look artificially expensive when the candidate axis is not the best axis for the point
set.

The update is small:

```text
try x-axis cylinder
try y-axis cylinder
try z-axis cylinder
choose the containing cylinder with the lowest weighted-volume proxy
```

Only the `cylinder` fitter changed. The slice did not introduce a full optimizer, did not change
the paper objective, and did not claim better collision geometry.

### 3. Synthetic Squat-Cylinder Fixture

A new deterministic toy mesh, `squat_cylinder`, was added to make the cylinder-axis change
inspectable. The synthetic native fitting comparison now has four expected native selections:

| Synthetic fixture | Expected native selection | What it checks |
| --- | --- | --- |
| `cylindrical_rod` | `cylinder` | Long cylinder-like shape. |
| `tapered_cone` | `cone` | Cone-like shape. |
| `ellipsoid_blob` | `ellipsoid` | Smooth ellipsoid-like blob. |
| `squat_cylinder` | `cylinder` | Axis search for a short/wide cylinder case. |

This synthetic step is important because it gives a controlled place to see that the fitting
change has the intended local effect before real USDs are rerun.

### 4. Real-USD Bed/Franka Rerun

After the synthetic check, the capped real-USD probe reran:

```text
bed old lane vs bed native lane
Franka old lane vs Franka native lane
```

with the same capped first-mesh scope and the same claim boundaries.

Current summary:

| Asset role | Legacy lane result | Native lane result | Interpretation |
| --- | --- | --- | --- |
| `bed_dev_smoke` | `32` boxes | `32` boxes | No native extension selected under the current surrogate. |
| `franka_import_smoke` | `32` boxes | `32` boxes | Three cheaper raw-cost cylinders are now support-blocked instead of selected. |

The Franka result is a primitive-selection/accounting change, not a quality result.

### 5. Newton Contact And Task Gates

The real-USD packages then went through the downstream diagnostic gates:

```text
full Newton mapping
-> representative contact canary
-> drop/settle smoke
-> sphere-rain smoke
```

All four capped packages passed these smokes in the recorded run. This means the packages can be
mapped and exercised by small Newton diagnostics. It does not mean the collider is accurate,
safe, benchmarked, or production-ready.

## Why This Is A Useful Step Toward CPD

CPD reproduction needs more than one algorithmic patch. It needs a disciplined loop:

1. choose a primitive-selection weakness;
2. isolate the weakness on a synthetic fixture;
3. make one controlled change;
4. inspect the candidate-cost table;
5. rerun real assets only after the synthetic result is interpretable;
6. gate real assets through Newton without claiming quality;
7. record exactly what changed.

The latest slice shows that this loop can run end to end. That gives future algorithmic changes a
clear diagnostic path to compare against before stronger claims are considered.

## What The Latest Result Does Not Prove

Do not read the latest slice as any of the following:

- the CPD paper has been reproduced;
- the CPD paper objective is implemented;
- the current primitive set is better for collision detection;
- Franka's whole-robot collider is validated;
- cylinders are broadly better than boxes;
- the generated collision package is safe outside this diagnostic workbench.

The correct reading is narrower:

```text
The repository can diagnose primitive-selection losses, make one controlled native-fitting
change, and rerun capped bed/Franka through Newton diagnostic gates under dated records.
```

## How To Use The Candidate-Loss Report Next

The candidate-loss report should drive the next algorithmic slice. Read it like a triage table:

| Report signal | Plain meaning | Reasonable next action |
| --- | --- | --- |
| `selected_box` + `extension_fit_cost_higher_than_selected` | The native extension was available but cost more under the surrogate. | Improve fitting quality or the surrogate before expecting a different selection. |
| `native_extension_selected` | A Newton-native extension won locally. | Check whether the selection is stable under synthetic and Newton gates. |
| `extension_candidate_blocked_by_support` | An extension was cheaper by raw surrogate cost, but had too little face/point support to replace the fallback primitive. | Keep the guardrail, then inspect whether fitting or clustering should improve on a richer fixture. |
| many high-aspect-ratio box clusters | The current local primitive candidates may be too box-biased. | Add a synthetic fixture that matches the shape, then improve fitting or merge search. |
| disconnected or wrapper-like clusters | The grouping may be the problem rather than the primitive kind. | Try a controlled merge-search change before changing primitive formulas. |

This keeps the next change grounded in evidence instead of guessing.

## What The Triage Metadata Adds

The candidate-loss report now includes a small `triage` block. It does not change primitive
selection. It just sorts the existing candidate-loss rows into two useful buckets:

```text
near-miss extension targets
low-support native-extension selections
```

The near-miss bucket means:

```text
box won, but cylinder/cone/ellipsoid was close under the surrogate
```

The low-support bucket means:

```text
cylinder/cone/ellipsoid won, but the cluster has very little geometric support
```

Before the support-aware admissibility slice, the capped bed/Franka report showed:

- bed has one `cylinder` near-miss target, with the best cylinder about `13%` more expensive than
  the selected box under the surrogate;
- Franka has three low-support `cylinder` selections, each from only two source faces and four
  points;
- Franka also has three `cylinder` near-miss box-selected clusters.

That made the next decision clearer. There were two defensible next synthetic fixtures:

- `low_support_native_extension_patch`, to test whether a native extension should require more
  geometric support before it can replace a box;
- `cylinder_near_miss_cluster`, to test whether cylinder fitting can be improved for a real
  box-selected cluster where cylinder is close but still loses.

The triage recommendation is still planning metadata. It is not an optimizer, not a quality score,
and not proof that cylinder is better or worse.

## What The Support-Aware Slice Adds

The follow-up slice executed the low-support branch. It adds a selection-time admissibility rule:

```text
fit all candidates as before
-> rank admissible candidates before under-supported native extensions
-> still expose raw cost rank so the report can explain what was blocked
```

The first support gate is deliberately narrow:

- it only applies to Newton-native extension candidates `cylinder`, `cone`, and `ellipsoid`;
- it requires at least three source faces and five unique assigned points when a fallback
  primitive is available;
- if a primitive subset contains only extension candidates, the best extension is still returned
  instead of failing the smoke path.

On the current support-aware capped bed/Franka rerun:

- bed still selects `32` boxes;
- Franka now selects `32` boxes instead of `29` boxes plus `3` cylinders;
- the three formerly selected Franka cylinders now appear as cheaper raw-cost extension
  candidates with `extension_candidate_blocked_by_support`;
- both bed and Franka still have `cylinder` near-miss targets, so the next algorithmic target moves
  from low-support admissibility to cylinder near-miss fitting or clustering.

This is not a quality result. It only says the workbench can stop a low-support native extension
from replacing a fallback primitive under the current surrogate and can explain that decision in
the candidate-loss report.

## Completed Sequence And Current Next Step

After the support-aware slice, the near-miss branch moved through these steps:

1. Build a `cylinder_near_miss_cluster` fixture from the recorded bed/Franka near-miss pattern.
2. Add a fit-ablation report that asks whether a containment-preserving cylinder fit can reduce
   the surrogate gap on that fixture.
3. Add a scoring-sensitivity report that asks how large a counterfactual cylinder score change
   would need to be after fitting is ruled out.
4. Add a report-only scoring-policy ablation that applies a fixed hypothetical multiplier inside
   the synthetic report and checks whether the fixture would flip.
5. Route the same multiplier through explicit synthetic selection and package probes.
6. Run a synthetic Newton task-smoke probe over the changed near-miss package pair.
7. Carry the existing cost-guided merge-search behavior difference into synthetic package and
   mapping accounting.
8. Run a synthetic Newton task-smoke probe over the changed controlled merge/search package pair.
9. Add a bounded synthetic two-step lookahead merge/search diagnostic over one trap fixture.
10. Carry the lookahead-changed package pair into synthetic package and Newton shape-mapping
    accounting.
11. Run an explicitly opt-in synthetic Newton task-smoke probe over the lookahead-changed package
    pair.
12. Add a command-only four-block slice report that links the recorded lookahead evidence across
    primitive fitting/selection, merge/search, offline diagnostics, and Newton task comparison.

The current next step is not another claim update on that same multiplier. For the merge/search
branch, the next narrow gate is to use the four-block report as the checklist for one bounded
paper-aligned objective, primitive-fitting, or merge/search change. Capped bed/Franka
candidate-loss diagnosis and Newton gates should rerun only if real packages change and pass full
mapping, contact-canary, task-gate, and dated-record gates.

The 2026-05-16 near-miss fixture slice starts step 1. It adds a direct synthetic primitive-ranking
fixture and a dedicated near-miss workbench report where `box` still wins and `cylinder` is close,
support-admissible, and ready to drive the next controlled fitting or merge/search change. It is
not a native fitting success case.

The 2026-05-16 fit-ablation slice starts step 2. It records that the fixture's containing-cylinder
radius already matches the pairwise radial lower bound, so radial-center refinement cannot flip the
selection without relaxing containment or changing the objective. It does not change the generated
package, so no Newton task rerun is triggered by this slice.

The 2026-05-16 scoring-sensitivity slice starts step 3. It reports that the support-admissible
cylinder would need a counterfactual score multiplier of about `0.8869`, or about an `11.31%`
cost reduction, to tie the selected box on this fixture. The multiplier is not applied; default
selection and Newton packages remain unchanged.

The 2026-05-16 report-only scoring-policy ablation starts step 4. It applies a fixed hypothetical
cylinder multiplier of `0.88` inside the synthetic report and records that the counterfactual
ranking would flip to `cylinder` for the near-miss fixture. The 2026-05-16 guardrail extension
adds a clearly boxy cuboid negative control that remains `box` under the same report-only
multiplier. This does not change default selection or generated packages, so no Newton task rerun
is triggered.

The 2026-05-16 synthetic offline opt-in scoring-policy selection probe is the next small step after
the report-only ablation. It routes the same multiplier through an explicit candidate-selection
path for synthetic fixtures only: the near-miss flips to `cylinder`, while the boxy guardrail
remains `box`. Default package generation and Newton task gates remain unchanged.

The 2026-05-16 synthetic package probe is the next bridge after selection. It routes the same
explicit multiplier through `decompose_mesh` and `CollisionPackage` generation for synthetic
fixtures only. The near-miss package changes from `box` to `cylinder`, the boxy guardrail package
stays `box`, and the report records Newton shape-mapping coverage. This is still not a Newton
contact or task diagnostic: no contact canary, drop/settle, or sphere-rain task is run by this
slice.

The 2026-05-16 synthetic Newton probe is the follow-on task-smoke slice. It leaves the package
probe's mapping-only boundary intact, then runs named contact, drop/settle, and sphere-rain smokes
over the changed near-miss package pair only. This is synthetic execution evidence under recorded
settings, not proof that the scoring policy is calibrated or that the cylinder package has better
collision quality.

The 2026-05-16 controlled merge-search package and Newton probes repeat the same discipline for
the merge/search branch. The package probe first records that `cost_guided_pairwise` changes the
toy package grouping from `[[0, 1], [2]]` to `[[0, 2], [1]]` and that both lanes map to Newton
shapes. The Newton probe then runs contact, drop/settle, and sphere-rain smokes over that changed
synthetic package pair. This is task-smoke execution for one toy merge/search pair, not a default
merge-policy change, real-USD result, merge-policy superiority result, or collision-quality
validation.

The 2026-05-16 cost-guided lookahead merge report is the next direct merge/search algorithmic
slice, but it stays offline. It adds `two_step_lookahead` for tiny synthetic fixtures and records
that the `lookahead_merge_trap` grouping changes from greedy `[[0, 2, 3], [1]]` to
`[[0, 1], [2, 3]]` with lower projected two-step normalized merge-excess. This is not package
evidence, Newton task evidence, real-USD evidence, merge-policy superiority, or collision-quality
validation.

The 2026-05-16 cost-guided lookahead package probe carries that offline grouping change one gate
farther. It converts the greedy and `two_step_lookahead` decompositions into synthetic
`CollisionPackage` lanes, compares their source-face groupings, and records Newton shape-mapping
coverage. It still does not run Newton runtime tasks, touch real assets, rank merge policies, or
measure collision geometry quality.

The 2026-05-16 cost-guided lookahead Newton probe is the follow-on task-smoke gate for that same
synthetic package pair. It runs contact first for each lane, then runs drop/settle and sphere-rain
only for lanes whose contact canary passes. This records named synthetic Newton task status under
recorded settings; it still does not touch real assets, rank merge policies, or measure collision
geometry quality.

Good first targets are:

- cylinder fitting beyond axis search, if the candidate-loss rows show near-cylinder clusters that
  still lose to boxes;
- ellipsoid fitting or scoring, if smooth blob-like clusters are consistently over-penalized;
- merge-search changes, if box selections look caused by bad cluster grouping rather than bad
  primitive fitting.

The safest immediate recommendation is now to use the four-block slice report as the review
checklist for the next bounded paper-aligned objective, primitive-fitting, or merge/search change.
Bed/Franka Newton task reruns should wait until a default or explicitly experimental real-asset
package actually changes and passes full mapping, contact-canary, task-gate, and dated-record
gates.

## Related Pages

- [CPD paper story status](cpd-paper-story-status.md)
- [Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md)
- [Bed and Franka native probe comparison](bed-franka-native-probe-comparison.md)
- [CPD next steps after real USD mirrors](cpd-next-steps-after-real-usd-mirrors.md)
- [Claim boundaries](claim-boundaries.md)
