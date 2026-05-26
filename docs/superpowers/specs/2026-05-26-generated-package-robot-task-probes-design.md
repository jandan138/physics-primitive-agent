# Generated-Package Robot Task Probes Design

## Goal

Add a Phase 0 robot probe that proves the generated link-aware collider package is consumed by Newton during a robot task smoke, instead of only proving that the package was generated and audited.

## Current Gap

Phase 0 already builds a `robot_package_result` for the Franka USD and audits link boundaries. The existing `articulation_smoke_if_robot` still imports the source USD collision shapes and runs the hold/trajectory smoke on that source import. That means the report can show robot import success without proving that the generated collision package was used by the task.

## Recommended Approach

Use a generated-package runtime path beside the existing source-USD articulation smoke:

- import the robot body and joint tree from the source USD;
- suppress source geometry/collision shape paths where they are separate from rigid body prims;
- attach one generated box primitive to the Newton body for each package primitive frame;
- require fixed joints not to be collapsed for this probe, so each source link remains addressable;
- run the same gravity-hold and kinematic trajectory smoke used by the source articulation probe;
- report both task-smoke metrics and package-consumption metrics.

This keeps the existing source articulation smoke as a baseline import check while adding a stronger generated-package consumption check.

## Requirements

1. The new probe id is `generated_package_robot_task_if_robot`.
2. The probe must accept a generated `collision_package` and attach package primitives to Newton bodies by package `frame`.
3. The probe must report `generated_package_consumed: true` only when:
   - the package has at least one primitive;
   - every package primitive is a supported box primitive;
   - every primitive frame resolves to a Newton body;
   - the number of generated Newton collision shapes equals the package primitive count;
   - source USD geometry/collision shapes were suppressed for the run;
   - the articulation hold/trajectory smoke passes.
4. The generated-package probe must run with `collapse_fixed_joints: false` in Phase 0 so meshless or fixed-link placeholders such as `/panda/panda_link8` remain addressable.
5. Phase 0 must record the probe under each articulated robot case and include it in articulation outcome counts.
6. `report_scope` must expose `generated_package_robot_task_checks: true` only when at least one articulated robot case has a passing generated-package task probe.
7. Claim wording must stay bounded: this is a diagnostic smoke that a generated package is consumed by Newton, not whole-robot collision quality, safety validation, or deployment readiness.

## Report Shape

The new report stage is `newton_generated_package_robot_task_probe`. Its metrics include:

- `generated_package_consumed`;
- `package_consumption.package_id`;
- `package_consumption.package_primitive_count`;
- `package_consumption.source_link_count`;
- `package_consumption.generated_collision_shape_count`;
- `package_consumption.consumed_primitive_count`;
- `package_consumption.missing_body_link_count`;
- `package_consumption.source_usd_shape_count`;
- the existing articulation import, gravity-hold, and trajectory metrics.

Failure labels should distinguish package-consumption failures from task failures, including missing body links, unsupported primitive kinds, invalid box dimensions, source USD shapes not being suppressed, and ordinary articulation smoke failures.

## Testing

Add unit tests for generated-package report evaluation, dependency-gap reporting, and Phase 0 integration. The Phase 0 integration test should monkeypatch the generated-package runner and assert that the generated collision package is passed through, fixed-joint collapse is disabled for this probe, and `report_scope.generated_package_robot_task_checks` becomes true.

Full completion still requires the real Franka Phase 0 run to show that generated package shapes are attached and consumed by Newton.
