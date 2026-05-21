# Newton-In-The-Loop Selector Story

This page explains the current real-USD selector slice in the CPD paper story. It is a
plain-language map, not new evidence beyond the dated records.

## Short Version

The paper story is:

```text
mesh
-> compact convex primitive decomposition
-> primitive collision detection
-> quality and speed evaluation
```

The repository has not reproduced that full paper story. The current real-USD slice is narrower:

```text
capped bed/Franka USD
-> CPD-like primitive package
-> Newton mapping/contact/task diagnostics
-> one opt-in selector guard derived from a Newton blocker
-> guarded package rerun through the same Newton diagnostics
-> one opt-in Franka support-threshold slice rerun through the same Newton diagnostics
-> one combined bed/Franka opt-in slice composing the guard and support-threshold controls
```

So the important status is: Newton-in-the-loop selector/fitting cycles now run end to end under
recorded, claim-bounded settings. They are diagnostic evidence, not benchmark or
collision-quality evidence.

## Why The Gates Came First

The earlier gates were not the final research claim. They made the later Newton run interpretable:

- config gates fixed which USD, face cap, lane, score multiplier, Newton source, and device were
  being used;
- mapping gates prevented task smokes from running on partially unmapped packages;
- contact gates made drop/settle and sphere-rain downstream of a simple contact canary;
- claim gates separated paper-lane offline work from real Newton evidence;
- dated records kept historical failing and passing configs reproducible.

That is why the work could move from many small gates to a real Newton run without changing the
claim boundary.

## What Actually Happened

The latest package-changing loop was:

```text
default support-aware bed/Franka lanes
-> historical opt-in Franka package with 8 cylinders passes Newton task smokes
-> historical opt-in bed package with 1 large flat cylinder fails drop/settle
-> bed diagnostics localize the blocker to the selected cylinder package delta
-> opt-in selector guard rejects large flat cylinder candidates
-> guarded bed package returns to 32 boxes and passes the recorded task smokes
-> guarded Franka keeps 8 smaller cylinders and also passes the recorded task smokes
-> support-threshold opt-in Franka admits 3 previously support-blocked cylinders and passes the
   same recorded Newton task smokes
-> combined guarded support-threshold bed/Franka config keeps bed at 32 boxes, admits the same 3
   Franka cylinders without a score multiplier, and passes the same recorded Newton task smokes
```

The selector guard is deliberately narrow. It applies only to explicitly configured
`native_opt_in` guard configs and rejects large flat cylinder candidates with the recorded
diagnostic reason `large_flat_cylinder_quarantine`.

The support-threshold probe is also deliberately narrow. It applies only to the configured
Franka `native_opt_in` lane and only lowers the extension support thresholds for `cylinder`
candidates from the default support-aware rule to `2` source faces and `4` unique points.

The combined probe composes those two opt-in controls in one two-role config. It is useful for the
DeepDive story because it keeps the bed blocker guarded while still allowing the three capped
Franka support-threshold cylinders, and it does so without a score multiplier. It is still only an
explicit diagnostic config.

## Current Evidence Table

| Slice | Package Result | Newton Task-Smoke Status | Interpretation |
| --- | --- | --- | --- |
| Default support-aware bed | `32` boxes | Passed in recorded runs | Baseline diagnostic path, not quality evidence. |
| Default support-aware Franka | `32` boxes | Passed in recorded runs | Baseline diagnostic path; raw cylinder near-wins are support-blocked. |
| Historical Franka opt-in | `24` boxes + `8` cylinders | Passed | Cylinders can appear in one capped Franka opt-in package and reach the task smokes. |
| Historical bed opt-in | `31` boxes + `1` cylinder | Drop/settle failed `not_settled` | A selected large flat cylinder exposed a Newton task blocker. |
| Guarded bed opt-in | `32` boxes; `23` guard-rejected cylinder candidates | Passed | One Newton-diagnosis-informed selector guard clears the recorded bed blocker. |
| Guarded Franka opt-in | `24` boxes + `8` cylinders; `0` guard rejections | Passed | The same guard does not erase the recorded small Franka cylinders. |
| Franka support-threshold opt-in | `29` boxes + `3` cylinders | Passed | The three previously support-blocked raw-cost cylinder candidates can be admitted in one opt-in lane and still pass recorded task smokes. |
| Combined guarded support-threshold bed/Franka opt-in | Bed: `32` boxes; Franka: `29` boxes + `3` cylinders | Passed | One two-role opt-in config composes the guard and support-threshold controls without a score multiplier. |

## What This Does Not Prove

This does not prove:

- full CPD paper reproduction;
- primitive collision quality improvement;
- benchmark superiority;
- a calibrated cylinder threshold;
- a calibrated support-threshold relaxation;
- a default selector policy;
- a score-free production recipe;
- broad bed, Franka, robot, or asset coverage;
- deployment readiness, safety certification, or real-world transfer.

## Current Position

The practical story is now:

```text
paper-lane gates made the contracts explicit
-> real bed/Franka packages reached Newton diagnostics
-> one opt-in cylinder choice failed a task gate
-> diagnostics produced one narrow selector rule
-> the guarded packages passed the same recorded task smokes
-> the support-blocked Franka candidates were admitted in one separate opt-in lane
-> that changed Franka package also passed the same recorded task smokes
-> the guard and support-threshold controls were composed in one bed/Franka opt-in config
-> the combined package kept bed guarded and Franka changed, with the same recorded smokes passing
```

That is a real Newton-in-the-loop diagnostic loop. The next useful work is not more gate
scaffolding for its own sake and not broad asset expansion. The next useful work is one more
controlled selector or fitting slice that changes a package for a clear reason, followed by the
same mapping/contact/task-smoke checks.

## Related Records

- [2026-05-21 native selector diagnostic guard](../records/2026-05-21-native-selector-diagnostic-guard.md)
- [2026-05-21 Franka native opt-in support threshold probe](../records/2026-05-21-franka-native-opt-in-support-threshold-probe.md)
- [2026-05-21 bed/Franka guarded support-threshold probe](../records/2026-05-21-bed-franka-guarded-support-threshold-probe.md)
- [2026-05-21 Franka native opt-in probe](../records/2026-05-21-franka-native-opt-in-probe.md)
- [2026-05-21 bed native opt-in probe](../records/2026-05-21-bed-native-opt-in-probe.md)
- [Bed and Franka native probe comparison](bed-franka-native-probe-comparison.md)
- [Claim boundaries](claim-boundaries.md)
