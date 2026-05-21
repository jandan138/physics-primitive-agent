# Bed And Franka Native Probe Comparison

This page explains the completed real-USD old/new native primitive probe comparison for the bed
and Franka smoke roles. It is a diagnostic record guide, not a benchmark report.

## One-Sentence Summary

The repository can now run capped bed and capped Franka first-mesh USDs through an old/new
primitive fitting comparison, require full Newton shape mapping before contact canaries, and run
gated drop/settle plus sphere-rain task smokes after contact passes.

## The Pipeline

The completed path is:

```text
bed or Franka USD
-> legacy CPD-like proposal lane
-> native CPD-like proposal lane
-> CollisionPackage summaries
-> full Newton mapping gate
-> Newton contact canary
-> gated drop/settle and sphere-rain task smokes
```

The command config is:

```text
configs/experiments/bed_franka_native_probe_comparison.yaml
```

Generated JSON reports are written under:

```text
reports/generated/bed_franka_native_probe_comparison/
```

That directory is intentionally gitignored. The dated records link the paths and summarize the
important statuses.

## Old Lane And New Lane

For each real USD role, the comparison runs two lanes under the same face cap, merge policy, and
primitive budget.

Legacy lane:

```text
box, sphere, capsule
```

Native lane:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

The native lane is allowed to choose Newton-native `cylinder`, `cone`, or `ellipsoid`. After the
controlled cylinder-axis fitting update, bed still selected `box` primitives in both lanes, while
Franka's native lane selected `29` boxes plus `3` cylinders under the raw surrogate. The follow-up
support-aware admissibility rule now blocks those three low-support raw-cost cylinder wins, so the
current native lane selects `32` boxes and explains the blocked cylinders in candidate-loss
diagnosis.

That is useful selection/accounting evidence. It says the workbench can expose a native-lane
selection change and then constrain it with support accounting, but it still does not prove
collision-quality improvement.

The offline fitting report now also includes `candidate_audit_summary` for each lane, and the
candidate-loss diagnosis report adds per-cluster reasons for remaining box selections. These are
diagnostic explanation layers, not collision-quality metrics.

## Current Results

Offline fitting report after the support-aware admissibility update:

- `bed_dev_smoke`: legacy `32` boxes, native `32` boxes, mapping clean, normalized volume delta
  `0.0`.
- `franka_import_smoke`: legacy `32` boxes, native `32` boxes, mapping clean.
- real-USD candidate-loss diagnosis: bed has `32` box-selected clusters where extension
  candidates are more expensive under the surrogate; Franka has `29` such box-selected clusters
  and `3` clusters where cheaper raw-cost `cylinder` candidates are support-blocked.

Contact comparison:

- all four lanes passed the contact canary;
- all four packages had `32` mapped primitives;
- box-only lanes produced representative `box` canary contacts;
- capped Franka native is now also box-only after support-aware admissibility.

Task comparison:

- all four lanes passed drop/settle and sphere-rain under the recorded config;
- these are named smoke diagnostics for mapping/contact/task execution, not a collision-quality
  comparison.

2026-05-21 opt-in update:

- the default capped bed/Franka support-aware config remains box-only;
- `configs/experiments/franka_native_opt_in_probe.yaml` adds a separate capped Franka
  `native_opt_in` lane with a `cylinder: 0.5` score multiplier;
- the capped Franka opt-in package selected `24` boxes plus `8` cylinders, fully mapped, and
  passed representative `box`/`cylinder` contact canaries plus package-level drop/settle and
  sphere-rain;
- `configs/experiments/bed_native_opt_in_probe.yaml` adds a separate capped bed `native_opt_in`
  diagnostic with a `cylinder: 0.88` score multiplier;
- the capped bed opt-in package selected `31` boxes plus `1` cylinder, fully mapped, and passed
  representative `box`/`cylinder` contact canaries plus sphere-rain, but failed drop/settle with
  `not_settled`;
- a local cylinder-revert drop-attribution diagnostic changed only the selected cylinder package
  delta at primitive index `6` / source faces `[32..39]` back to the native box fallback. Under
  the same clean Newton settings, the original opt-in lane failed `not_settled`, while the
  reverted package passed drop/settle. This is counterfactual diagnostic attribution only;
- the primitive-6 center/shape off-diagonal diagnostic records `box_at_cylinder_center` passing
  drop/settle and `cylinder_at_box_center` still failing with `not_settled`; the package anchor is
  unchanged across variants. This supports only local attribution to the selected cylinder
  shape/dimensions rather than the center shift for this recorded package;
- the primitive-6 target-only diagnostic keeps only that one primitive in the package. The
  isolated box and cylinder variants all passed drop/settle with final speed `0.0 m/s`, so the
  selected cylinder alone did not reproduce the full-package blocker under one-primitive anchor
  recomputation;
- the primitive-6 nearest-neighbor local shell used six closest AABB-gap neighbors and passed with
  both the native-box target and opt-in-cylinder target. An anchor-preserved local subset kept the
  full package anchor fixed but failed for both the native-box and cylinder target variants, so it
  is recorded as a diagnostic-control failure rather than cylinder attribution evidence;
- `scripts/diagnostics/bed_native_opt_in_compound_trace.py` adds a reproducible full-compound
  Newton body/contact trace for the fixed primitive-6 variants. The dated trace records body mass,
  COM, inertia, pose/velocity, support height, and final contact details. The cylinder variants
  keep failing with residual final speeds about `0.079-0.082 m/s`, while the box variants pass at
  about `0.040-0.046 m/s`; final support-contact labels remain the same four support primitives
  against the ground plane;
- the same script with `--run-inertia-counterfactual` keeps the opt-in cylinder geometry but
  copies the native all-box Newton body mass, inverse mass, COM, inertia, and inverse inertia
  arrays into the opt-in cylinder model before solver creation. In the dated run the package
  anchors match, the inertial override is recorded before/after, and the counterfactual cylinder
  package passes drop/settle with final speed about `0.0404565 m/s`;
- the same script with `--run-inertia-field-ablation` keeps the opt-in cylinder geometry, mass,
  inverse mass, inertia, and inverse inertia unchanged while copying only the native all-box
  `body_com`. In the dated run this COM-only field ablation passes drop/settle with final speed
  about `0.0425127 m/s`;
- the same script with `--run-inertial-component-ablation` keeps the opt-in cylinder geometry and
  opt-in `body_com` while copying native all-box mass-only, inertia-only, and mass+inertia
  component groups. In the dated 360-frame run mass-only and mass+inertia remain `not_settled`
  while inertia-only passes; in the dated 361-frame run mass-only remains `not_settled` while
  inertia-only and mass+inertia pass;
- the same script with `--run-com-axis-ablation` keeps the opt-in cylinder geometry, mass,
  inverse mass, inertia, and inverse inertia unchanged while copying fixed single-axis and
  pairwise subsets of the native all-box `body_com`. In the dated run `x`, `y`, `z`, `xy`, and
  `yz` subsets remain `not_settled`, while the `xz` subset passes drop/settle with final speed
  about `0.0422074 m/s`; the original opt-in and all COM-axis subset variants share final contact
  count `4` and the same support-contact labels (`12`, `15`, `15`, and `26`) against the ground
  plane;
- the same script with `--run-com-blend-ablation` keeps the opt-in cylinder geometry, mass,
  inverse mass, inertia, and inverse inertia unchanged while applying fixed blends from the
  opt-in `body_com` toward native all-box `body_com` for full `xyz` and `xz` axes. In the dated
  run, `0.25`, `0.5`, and `0.75` blends remain `not_settled` for both axis sets; only the `1.0`
  endpoints clear the recorded `360`-frame final-speed gate label, with final speeds about
  `0.0425127 m/s` for full `xyz` and `0.0422074 m/s` for `xz`;
- the same script with `--run-com-blend-refinement` runs a fixed near-endpoint refinement between
  the recorded `0.75` failures and `1.0` label-clearing endpoints. In the dated run, full `xyz`
  clears the recorded `360`-frame final-speed gate label at `0.875`, `0.9375`, `0.96875`,
  `0.984375`, and `1.0`, while `xz` remains `not_settled` at `0.875` and clears the label at
  `0.9375`, `0.96875`, `0.984375`, and `1.0`. This is sensitivity accounting, not a COM
  threshold proof;
- a real Newton rerun of the same COM-blend refinement records `tail_linear_speed_summary` as
  late-window speed telemetry only. The listed pass/fail outcomes still come from the final-speed
  drop/settle gate: for example, the full `xyz` `0.875` pass has `473/481` one-second tail
  samples above the `0.05 m/s` threshold and only the final `8` sampled steps (`0.0166667 s`) at
  or below it. This is not sustained-settle evidence or a new pass/fail gate;
- a `361`/`362`/`363`/`364`/`365`/`375`/`385`/`390`/`420`/`450`/`480`/`600`/`720`-frame real
  Newton frame-window sweep of the same COM-blend refinement keeps the same capped bed first-mesh
  scope and `cylinder: 0.88` opt-in multiplier while changing only `drop_settle.frames`. In the
  dated runs, `361` keeps the native all-box and cylinder-reverted controls clean under the
  existing final-speed gate at about `0.0449881 m/s`, while the original opt-in cylinder remains
  `not_settled` at about `0.0631791 m/s`. The first swept dirty-control row is `362`, where the
  native/reverted controls fail at about `0.0639728 m/s`; the same controls then fail at about
  `0.0957800 m/s` at `363`, `0.1194928 m/s` at `364`, `0.1464434 m/s` at `365`,
  `0.3574153 m/s` at `375`, `0.5688495 m/s` at `385`, `0.6757393 m/s` at `390`,
  `0.5461583 m/s` at `420`, `0.4750371 m/s` at `450`, `0.1789031 m/s` at `480`,
  `0.1768281 m/s` at `600`, and `0.2896395 m/s` at `720`. Selected two-second tail summaries are
  not a sustained-settle criterion or new gate. These reruns are used only to bracket the observed
  native/reverted-control final-speed task-gate flip between the `361` clean-control context and
  the `362` failure context. Dirty-control rows are rejected as COM-blend fix, sustained-settle,
  or long-window stability evidence;
- `scripts/diagnostics/bed_native_opt_in_frame_transition_audit.py` adds a post-run `361`/`362`
  frame-transition audit for the native all-box and cylinder-reverted controls. In the dated
  audit, both controls keep matching Newton model arrays and matching final support-contact
  labels across the adjacent reports, while the `362` row adds `8` substeps and increases final
  linear speed by about `0.0189847 m/s`. The compact final-window rows are aligned by
  `steps_from_final`, not raw `step`;
- `scripts/diagnostics/bed_native_opt_in_clean_frame_blocker_audit.py` adds a post-run `361`
  clean-frame blocker audit inside the same clean-control report. In the dated audit, the native
  all-box and cylinder-reverted controls pass while the original opt-in cylinder remains
  `not_settled`; final support-contact primitive suffixes match (`12`, `15`, `15`, and `26`),
  while the original opt-in cylinder ends about `0.0181910 m/s` faster than either clean control
  and records mass `+1126.625` plus COM delta about
  `[-0.0427847, 0.0171919, 0.2960243]`;
- `scripts/diagnostics/bed_native_opt_in_compound_trace.py` with `--run-model-build-audit`
  records a pre-solver Newton model-build audit for full, target-only, and rest-without-target
  packages under full-package anchors. In the dated run the native and opt-in package anchors
  match; the full opt-in-minus-native body delta is mass
  `+1126.625` and COM about `[-0.0427847, 0.0171919, 0.2960243]`; the target-only
  opt-in-minus-native delta is mass about `+1126.5820`, COM about
  `[0.2216988, 0.3152409, -0.0516510]`, and inertia row-0 about
  `[2962.6045, -683.8531, 436.1219]`; the rest-without-target delta is zero for mass, COM, and
  inertia row-0;
- `scripts/diagnostics/bed_native_opt_in_model_build_delta_audit.py` adds a post-run JSON audit
  over that model-build report. It records the primitive-6 native target shape-scale row
  `[0.2130423, 2.3121915, 2.1920862]`, the opt-in target shape-scale row
  `[2.7009380, 0.2130423, 0.0]`, and the same rest/target/full model-build delta summary;
- the earlier temporary two-role capped bed opt-in stress run selected `25` boxes plus `7`
  cylinders and failed more strongly: drop/settle reported `not_settled` and `floor_breach`, and
  sphere-rain reported `no_contact_observed` and `insufficient_contact_density`.

2026-05-21 guarded selector update:

- the historical unguarded bed and Franka opt-in configs remain unchanged for reproducibility;
- `configs/experiments/bed_native_opt_in_guard_probe.yaml` adds a separate diagnostic
  `native_opt_in_selection_guard` that rejects large flat cylinder candidates only in the opt-in
  lane;
- the guarded capped bed fitting report selects `32` boxes, reports `23` diagnostic guard rejected
  cylinder candidates, and passes contact-gated drop/settle plus sphere-rain under the same clean
  Newton environment;
- `configs/experiments/franka_native_opt_in_guard_probe.yaml` runs the same guard on capped
  Franka; the opt-in lane remains `24` boxes plus `8` cylinders, reports `0` guard rejections,
  and passes contact-gated drop/settle plus sphere-rain;
- this is a controlled selector-diagnostic slice, not a default policy, collision-quality result,
  calibrated threshold, or proof that boxes are better than cylinders.

2026-05-21 Franka support-threshold opt-in update:

- `configs/experiments/franka_native_opt_in_support_threshold_probe.yaml` adds a separate
  capped Franka `native_opt_in` lane with `native_opt_in_extension_support_thresholds`;
- default capped Franka legacy/native lanes remain `32` boxes;
- the support-threshold opt-in lane lowers only configured `cylinder` extension support
  thresholds to `2` source faces and `4` unique points, selecting `29` boxes plus `3`
  cylinders;
- the changed opt-in package fully mapped and passed contact-gated drop/settle plus sphere-rain
  under the recorded clean Newton environment;
- this is a support-admissibility diagnostic, not a default support threshold, calibrated policy,
  collision-quality result, or whole-robot Franka collider-quality claim.

For the plain-language version of why this followed the earlier gate work, see
[Newton-in-the-loop selector story](newton-in-the-loop-selector-story.md).

## What This Means In The CPD Story

This moves the repository one step beyond synthetic native fitting:

```text
synthetic native fitting works on controlled toy meshes
-> real bed/Franka old/new reports run under face caps
-> Newton can consume the resulting mapped packages
-> named task smokes can run after contact canary passes
```

It does not mean the native lane is better. The pre-support-aware run produced three capped
Franka cylinder selections; the current support-aware run keeps capped Franka box-only and reports
those cylinders as cheaper raw-cost candidates blocked by support admissibility. The record is
still a diagnostic-gate and surrogate-accounting result, not a collision-quality result.

The simple mental model is:

```text
paper goal: choose better convex primitives for collision detection
current slice: record capped real-USD packages reaching named Newton diagnostics under recorded settings
current diagnostic add-on: expose why remaining real-USD clusters still select boxes
next algorithm slice: use diagnosis labels to target the next primitive-choice change
```

For a more detailed paper-story walkthrough, see
[Real USD native probe in the CPD paper story](real-usd-native-probe-paper-story-explainer.md).

## Claim Boundary

Allowed wording:

- "real-USD old/new diagnostic smoke";
- "capped bed and capped Franka first-mesh scope";
- "full Newton mapping gate";
- "contact-canary smoke";
- "drop/settle and sphere-rain task smokes under recorded settings."
- "real-USD per-cluster candidate audit summary."
- "real-USD per-cluster candidate-loss diagnosis."
- "explicit capped Franka opt-in native-exercising diagnostic."
- "capped bed opt-in task-gate blocker."
- "capped bed single-primitive cylinder-revert drop-attribution diagnostic."
- "capped bed primitive-6 center/shape separation diagnostic."
- "capped bed primitive-6 target-only drop/settle control."
- "capped bed primitive-6 local-context compound controls."
- "capped bed primitive-6 full-compound body/contact trace."
- "capped bed primitive-6 full-compound inertial-array counterfactual."
- "capped bed primitive-6 COM-only inertial-field ablation."
- "capped bed primitive-6 inertial-component ablation."
- "capped bed primitive-6 COM-axis subset field ablation."
- "capped bed primitive-6 COM-blend field ablation."
- "capped bed primitive-6 COM-blend refinement."
- "capped bed primitive-6 COM-blend refinement tail-speed telemetry."
- "capped bed primitive-6 COM-blend refinement 361/362/363/364/365/375/385/390/420/450/480/600/720-frame window sensitivity sweep."
- "capped bed primitive-6 361/362 frame-transition audit."
- "capped bed primitive-6 361 clean-frame blocker audit."
- "capped bed primitive-6 pre-solver model-build audit."
- "capped bed primitive-6 post-run model-build delta audit."
- "capped Franka opt-in support-threshold diagnostic."

Do not claim:

- collision-quality improvement;
- benchmark superiority;
- whole-robot Franka collider quality;
- paper-faithful CPD reproduction;
- safety certification or deployment readiness;
- that `cylinder`, `cone`, or `ellipsoid` improved bed/Franka collision quality in this run.
- that the capped bed opt-in lane passed package-level task smokes;
- that either cylinder score multiplier is calibrated, recommended, or suitable for default
  configs.
- that the capped bed cylinder-revert attribution run proves cylinders are worse than boxes,
  establishes a broad root cause, or implements an automatic repair policy.
- that the primitive-6 center/shape separation diagnostic validates a default multiplier or
  proves a general cylinder-quality problem.
- that the primitive-6 target-only control is equivalent to the full 32-primitive compound run.
- that any local-context subset proves cylinder attribution when the paired native-box control
  also fails.
- that the full-compound body/contact trace is a general root-cause proof, validated fix, or
  collision-quality metric.
- that the inertial-array counterfactual is a physically validated package, root-cause proof,
  scoring-policy evidence, or a default repair recipe.
- that the COM-only inertial-field ablation proves causality or validates a package fix.
- that the inertial-component ablation proves root cause, validates an inertial repair, provides a
  default repair recipe, or validates a package fix.
- that the COM-axis subset field ablation proves causality, proves the `y` component is
  irrelevant, or validates a package fix.
- that the COM-blend field ablation proves a COM threshold, causality, or a package fix.
- that the COM-blend refinement proves a minimum required COM fraction, threshold, causality, or
  package fix.
- that COM-blend refinement tail telemetry proves sustained settling or adds a new drop/settle
  gate.
- that the 361/362/363/364/365/375/385/390/420/450/480/600/720-frame window sweep proves
  sustained settling, validates a COM-blend fix, or strengthens the refinement claim. The `361`
  clean-control row is final-speed sensitivity accounting only; dirty-control rows are rejected
  when native all-box controls also fail in those swept windows.
- that the 361/362 frame-transition audit proves sustained settling, long-window stability,
  causality, a validated fix, scoring/default-policy evidence, or collision-quality validation.
- that the 361 clean-frame blocker audit proves sustained settling, long-window stability,
  causality, a validated fix, scoring/default-policy evidence, or collision-quality validation.
- that the pre-solver model-build audit or post-run model-build delta audit proves a Newton
  mapping bug, physical root cause, validated inertial repair, scoring evidence, default-policy
  behavior, or package-quality conclusion.
- that the capped Franka support-threshold opt-in probe calibrates support thresholds, changes
  default support-aware selection, validates cylinder collision quality, or proves whole-robot
  Franka collider quality.

## Commands

Offline fitting:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-fitting-comparison
```

Candidate-loss diagnosis:

```bash
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-candidate-loss-diagnosis
```

Contact canary:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-contact-comparison
```

Gated task smokes:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_franka_native_probe_comparison.yaml \
  --run-real-usd-native-task-comparison
```

Franka opt-in gated task smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/franka_native_opt_in_probe.yaml \
  --run-real-usd-native-task-comparison
```

Franka support-threshold opt-in gated task smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/franka_native_opt_in_support_threshold_probe.yaml \
  --run-real-usd-native-task-comparison
```

Bed opt-in gated task smoke, expected to exit `2` for the recorded blocker:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --run-real-usd-native-task-comparison
```

Bed opt-in full-compound body/contact trace:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_compound_trace_2026-05-21.stdout.json
```

Bed opt-in inertial-array counterfactual:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-inertia-counterfactual \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertia_counterfactual_2026-05-21.stdout.json
```

Bed opt-in COM-only inertial-field ablation:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-inertia-field-ablation \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_field_ablation_2026-05-21.stdout.json
```

Bed opt-in inertial-component ablation:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-inertial-component-ablation \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_inertial_component_ablation_2026-05-21.stdout.json
```

Bed opt-in COM-axis subset field ablation:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-com-axis-ablation \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_axis_subset_ablation_2026-05-21.stdout.json
```

Bed opt-in COM-blend field ablation:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-com-blend-ablation \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_ablation_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-com-blend-refinement \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement tail-summary rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_com_blend_refinement_tail_suffix_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 361-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame361_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 362-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame362_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json
```

Bed opt-in 361/362 frame-transition audit:

```bash
PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_frame_transition_audit.py \
  --clean-report reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json \
  --dirty-report reports/generated/bed_native_opt_in_frame362_probe/drop_primitive6_com_blend_refinement_frame362_2026-05-21.stdout.json \
  --variant-label native_control_box \
  --variant-label native_opt_in_cylinder_reverted \
  --output reports/generated/bed_native_opt_in_frame_transition_audit/native_reverted_frame361_362_audit_2026-05-21.stdout.json
```

Bed opt-in 361 clean-frame blocker audit:

```bash
PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_clean_frame_blocker_audit.py \
  --report reports/generated/bed_native_opt_in_frame361_probe/drop_primitive6_com_blend_refinement_frame361_2026-05-21.stdout.json \
  --baseline-label native_control_box \
  --baseline-label native_opt_in_cylinder_reverted \
  --target-label native_opt_in_cylinder \
  --output reports/generated/bed_native_opt_in_clean_frame_blocker_audit/native_opt_in_cylinder_frame361_blocker_audit_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 363-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame363_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame363_probe/drop_primitive6_com_blend_refinement_frame363_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 364-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame364_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame364_probe/drop_primitive6_com_blend_refinement_frame364_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 365-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame365_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame365_probe/drop_primitive6_com_blend_refinement_frame365_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 375-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame375_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame375_probe/drop_primitive6_com_blend_refinement_frame375_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 385-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame385_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame385_probe/drop_primitive6_com_blend_refinement_frame385_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 390-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame390_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame390_probe/drop_primitive6_com_blend_refinement_frame390_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 420-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame420_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame420_probe/drop_primitive6_com_blend_refinement_frame420_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 450-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame450_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame450_probe/drop_primitive6_com_blend_refinement_frame450_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 480-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame480_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame480_probe/drop_primitive6_com_blend_refinement_frame480_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 600-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_frame600_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_frame600_probe/drop_primitive6_com_blend_refinement_frame600_2026-05-21.stdout.json
```

Bed opt-in COM-blend refinement 720-frame window sensitivity rerun:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_long_window_probe.yaml \
  --source-dir /cpfs/user/zhuzihou/dev/newton \
  --run-com-blend-refinement \
  --sample-every-steps 480 \
  --tail-steps 960 \
  --output reports/generated/bed_native_opt_in_long_window_probe/drop_primitive6_com_blend_refinement_long_window_2026-05-21.stdout.json
```

Bed opt-in pre-solver model-build audit:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/diagnostics/bed_native_opt_in_compound_trace.py \
  --config configs/experiments/bed_native_opt_in_probe.yaml \
  --source-dir '$NEWTON_SOURCE_DIR' \
  --run-model-build-audit \
  --output reports/generated/bed_native_opt_in_probe/drop_primitive6_model_build_audit_2026-05-21.stdout.json
```

Bed opt-in post-run model-build delta audit:

```bash
PYTHONPATH=src python scripts/diagnostics/bed_native_opt_in_model_build_delta_audit.py \
  --report reports/generated/bed_native_opt_in_probe/drop_primitive6_model_build_audit_2026-05-21.stdout.json \
  --output reports/generated/bed_native_opt_in_model_build_delta_audit/primitive6_model_build_delta_audit_2026-05-21.stdout.json
```
