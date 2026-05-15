# CPD Latest Diagnostic Loop Explainer

This page explains the latest candidate-loss and cylinder-axis slice in the story of reproducing
Convex Primitive Decomposition for Collision Detection. It is a teaching note and navigation aid,
not new experiment evidence.

## One-Sentence Version

The latest work did not reproduce the CPD paper algorithm. It built a small, repeatable diagnostic
loop that can explain a primitive-selection weakness, make one controlled fitting change, verify
that change on toy meshes, and then rerun capped bed/Franka through Newton gates without changing
the claim boundary.

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
- Franka native lane selects `29` boxes and `3` cylinders;
- the remaining bed box clusters and Franka box clusters usually have extension candidates, but
  those candidates are more expensive under the current weighted-volume surrogate.

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
| `franka_import_smoke` | `32` boxes | `29` boxes + `3` cylinders | The native lane can now select cylinder on three capped Franka clusters. |

The Franka result is a primitive-selection change, not a quality result.

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
| many high-aspect-ratio box clusters | The current local primitive candidates may be too box-biased. | Add a synthetic fixture that matches the shape, then improve fitting or merge search. |
| disconnected or wrapper-like clusters | The grouping may be the problem rather than the primitive kind. | Try a controlled merge-search change before changing primitive formulas. |

This keeps the next change grounded in evidence instead of guessing.

## Recommended Next Sequence

The next few steps should be:

1. Pick one candidate-loss pattern as the next target.
2. Build or extend one synthetic fixture that reproduces that pattern.
3. Improve exactly one fitting or merge-search component.
4. Rerun the synthetic native fitting/audit reports.
5. Rerun capped bed/Franka fitting only if the synthetic result is explainable.
6. If fitting changes, rerun candidate-loss diagnosis.
7. If real packages still fully map, rerun Newton contact and task gates.
8. Record the result and update claim boundaries before making stronger wording.

Good first targets are:

- cylinder fitting beyond axis search, if the candidate-loss rows show near-cylinder clusters that
  still lose to boxes;
- ellipsoid fitting or scoring, if smooth blob-like clusters are consistently over-penalized;
- merge-search changes, if box selections look caused by bad cluster grouping rather than bad
  primitive fitting.

The safest immediate recommendation is to start with candidate-loss triage and a synthetic fixture
that mirrors one remaining high-confidence real-USD box-selection pattern.

## Related Pages

- [CPD paper story status](cpd-paper-story-status.md)
- [Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md)
- [Bed and Franka native probe comparison](bed-franka-native-probe-comparison.md)
- [CPD next steps after real USD mirrors](cpd-next-steps-after-real-usd-mirrors.md)
- [Claim boundaries](claim-boundaries.md)
