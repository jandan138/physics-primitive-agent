# 2026-05-22 Cylinder Clean-Control Probe

## Date

2026-05-22

## Status

Compact clean-control probe recorded. The new evidence narrows the current bed-vs-Franka cylinder
story in one direction: the large flat bed cylinder geometry by itself is insufficient to reproduce
the recorded `not_settled` label, while the full compound package context is required for that
recorded failure.

The current strongest hypothesis remains full-compound COM/inertia body-state sensitivity, with
pair-level contact/floor interaction still open as a secondary factor. This is not root-cause
proof, a validated repair, selector-policy evidence, collision-quality validation, or safety
evidence.

## Changes

- Added `primitive_collision_compiler.diagnostics.cylinder_clean_controls`, a small report
  synthesis helper for compact cylinder clean controls.
- Added `scripts/diagnostics/cylinder_clean_control_probe.py`, an executable Newton probe over
  selected single-primitive and two-primitive compact controls.
- Added unit coverage for the report synthesis and script command surface.
- Generated ignored local report:
  `reports/generated/cylinder_clean_controls/compact_probe.json`.

## Verification

- RED: `python -m pytest tests/test_cylinder_clean_controls.py -q` initially failed because
  `primitive_collision_compiler.diagnostics.cylinder_clean_controls` did not exist.
- GREEN: `python -m pytest tests/test_cylinder_clean_controls.py -q`:
  exit `0`, `1 passed`.
- RED: `python -m pytest tests/test_bootstrap_command_surface.py::test_cylinder_clean_control_probe_script_has_bounded_help_and_default_pairs -q`
  initially failed because `scripts/diagnostics/cylinder_clean_control_probe.py` did not exist.
- GREEN: the same command:
  exit `0`, `1 passed`.
- Real Newton compact probe:
  `NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton PYTHONPATH=src:$PYTHONPATH timeout 600s /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python scripts/diagnostics/cylinder_clean_control_probe.py --bed-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/bed_task.json --franka-task-report /cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/cylinder_stability_mechanism/franka_cost_guided_task.json --source-dir /cpfs/user/zhuzihou/dev/newton --output reports/generated/cylinder_clean_controls/compact_probe.json`:
  exit `0`, report `status: diagnostic_recorded`.
- `python -m json.tool reports/generated/cylinder_clean_controls/compact_probe.json >/dev/null`:
  exit `0`.

## Key Results

- Single-primitive controls all passed the same recorded `360` frame, `8` substep,
  `2` iteration drop gate:
  - bed target cylinder only: `smoke_passed`, final speed `0.0 m/s`, final contacts `3`;
  - bed target box only: `smoke_passed`, final speed `0.0 m/s`, final contacts `4`;
  - largest recorded Franka cylinder only: `smoke_passed`, final speed `0.0 m/s`, final contacts
    `3`.
- Six representative two-primitive bed pair controls were mixed:
  - rest indices `0`, `10`, and `16`: both target-box and target-cylinder pairs failed
    `not_settled`;
  - rest indices `3` and `24`: target-box pairs passed, while target-cylinder pairs failed
    `floor_breach`;
  - rest index `17`: both target-box and target-cylinder pairs passed.
- The compact report records:
  - `geometry_alone`: `insufficient_as_sole_cause`;
  - `compound_context`: `required_for_recorded_not_settled`;
  - `pair_context`: `mixed`;
  - `contact_or_floor_interaction`: `open_for_pair_controls_not_recorded_full_failure`;
  - `com_inertia_body_state`: `still_strongest_current_hypothesis`.

## Interpretation

The clean-control evidence moves the answer forward:

1. Geometry ratio alone is not enough: the exact bed target cylinder shape, with its actual axes,
   settles when run as a single primitive.
2. Categorical Newton cylinder instability is still unlikely: the largest recorded Franka cylinder
   also settles when run alone, and the capped Franka cylinder-containing package passes.
3. Full package context is necessary for the recorded bed `not_settled` label: the single target
   cylinder passes while the full opt-in bed package fails.
4. Pair controls show that two-piece compound context can itself create instability, sometimes for
   both box and cylinder target variants. That means pair-level `not_settled` is not clean proof of
   cylinder-specific failure.
5. Some pair controls produce cylinder-only `floor_breach`, so contact/floor interaction remains
   open, but those labels differ from the full bed package's recorded `not_settled` label.
6. Given the prior COM-only and inertia-only clearing controls, the strongest current explanation
   remains full-compound COM/inertia body-state sensitivity, with contact/floor effects retained as
   a secondary open factor.

## Claim Impact

- This strengthens the boundary around the current mechanism story: say geometry alone is
  insufficient and full-compound context is required for the recorded bed `not_settled` failure.
- Do not claim physical root-cause proof, a validated COM/inertia repair, broad cylinder stability
  or instability, selector calibration, collision-quality validation, benchmark behavior,
  deployment readiness, safety certification, or real-world transfer.

