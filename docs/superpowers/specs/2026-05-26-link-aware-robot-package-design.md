# Link-Aware Robot Package Design

## Date

2026-05-26

## Goal

Generate a reviewable primitive collision package for articulated USD robot assets where collider
primitives are assigned to exactly one robot link and the report explicitly rejects or records any
cross-link merge.

## Scope

This design covers the first Phase 0 link-aware package path:

- inspect a USD articulation asset for rigid-body link prims and joint relationships;
- collect mesh geometry under each link prim;
- generate bounded box primitives per link from that link's own mesh points;
- generate a clearly flagged placeholder box for rigid-body links with no mesh points;
- record a link-boundary audit with per-link primitive counts and cross-link merge count;
- integrate the package and audit into Phase 0 articulated robot cases.

This does not claim whole-robot collider quality, manipulation performance, safety validation, or a
calibrated primitive selector policy. The first generated package is a link-aware diagnostic
candidate, not an accepted production collider.

## Approach

Use USD Physics structure rather than path-name heuristics:

1. A robot link is any prim with `PhysicsRigidBodyAPI`.
2. A joint edge comes from USD Physics joint relationships `physics:body0` and `physics:body1`.
3. A mesh belongs to the nearest ancestor link prim that contains it.
4. A generated primitive must carry `frame=<link path>` and `source_links=(<link path>,)`.
5. The audit fails if a primitive names zero links, more than one source link, or a source link that
   does not match its frame.
6. The audit also fails if any detected link has zero primitives. Meshless links may satisfy this
   coverage gate only through a deterministic placeholder primitive with
   `conversion_status="placeholder_meshless_link"`.

Fixed joints are still kept as separate links for this first package. This is conservative: it
prevents accidental cross-joint merges until a later, explicitly recorded fixed-joint-collapse
policy exists.

Meshless placeholder primitives are coverage artifacts, not geometry-quality evidence. They are
small link-local boxes at the link origin, counted separately in the audit, and keep the package
reviewable without borrowing geometry across fixed or articulated joints.

## Interfaces

Create `primitive_collision_compiler.robots.link_aware_package` with:

- `build_link_aware_robot_package(asset_path, asset_id, source_sha256="")`
  returning a `RobotLinkPackageReport`;
- `audit_link_boundaries(package, link_paths)` returning a JSON-safe audit dict;
- small dataclasses for link summaries and the package report.

Extend `PrimitiveSpec` with `source_links: tuple[str, ...] = ()` and include it in `to_dict()`.
Existing rigid packages leave this empty.

## Phase 0 Integration

For each articulated robot case:

- keep the current asset smoke gate;
- if the asset gate passes, build a link-aware robot package;
- store the generated package under `robot_package_result`;
- replace the previous `link_boundary_audit` fallback with the package audit;
- keep the existing Newton articulation smoke as a separate probe over the source USD.

The Phase 0 `report_scope.link_aware_robot_package_generation` becomes true only when at least one
articulated case generated a link-aware package and its link-boundary audit passed.

## Testing

Tests must be written first and cover:

- a synthetic USD robot with two rigid-body links and one joint produces one primitive per link;
- a synthetic meshless rigid-body link still receives a flagged placeholder primitive and the audit
  reports full link coverage;
- the audit rejects a synthetic primitive with `source_links` spanning two links;
- the audit rejects packages where any detected link has zero primitives;
- Phase 0 articulated robot case records `link_aware_package_generated: true`,
  `cross_link_merge_count: 0`, and per-link counts while articulation smoke remains separate.

Real Franka evidence should be recorded after unit tests pass by running the Phase 0 benchmark in
the clean Newton environment or a smaller link-package inspection command if available.
