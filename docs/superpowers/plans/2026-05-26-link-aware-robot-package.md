# Link-Aware Robot Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Phase 0 link-aware robot package generation that emits per-link primitive packages and audits that primitives do not merge across joints.

**Architecture:** Add a focused robot package module that reads USD Physics link and joint structure, generates link-framed box primitives from each link's own meshes, and returns a package plus audit. Phase 0 articulated cases call this module before articulation smoke and expose the package/audit in the report.

**Tech Stack:** Python dataclasses, pxr.Usd/UsdGeom/UsdPhysics, existing `CollisionPackage` and `PrimitiveSpec`, pytest.

---

### Task 1: Primitive Link Metadata

**Files:**
- Modify: `src/primitive_collision_compiler/contracts.py`
- Test: `tests/test_contracts.py`

- [ ] Add a failing test that `PrimitiveSpec(..., source_links=("/robot/link0",)).to_dict()` includes `source_links`.
- [ ] Run `python -m pytest tests/test_contracts.py -q`; expect the new assertion to fail.
- [ ] Add `source_links: tuple[str, ...] = ()` to `PrimitiveSpec` and serialize it as a list.
- [ ] Run `python -m pytest tests/test_contracts.py -q`; expect pass.

### Task 2: Link-Aware Robot Package Module

**Files:**
- Create: `src/primitive_collision_compiler/robots/link_aware_package.py`
- Create: `src/primitive_collision_compiler/robots/__init__.py`
- Test: `tests/test_link_aware_robot_package.py`

- [ ] Add a synthetic USD helper that creates two `PhysicsRigidBodyAPI` link prims, one joint, and one mesh under each link.
- [ ] Add a failing test for `build_link_aware_robot_package`: two links, two primitives, each primitive has one matching `source_links` entry, and audit has `cross_link_merge_count == 0`.
- [ ] Add a failing test for `audit_link_boundaries`: a primitive with `source_links=("/Robot/link0", "/Robot/link1")` returns `status == "runtime_failure"` and `cross_link_merge_count == 1`.
- [ ] Implement USD link discovery, mesh-to-nearest-link assignment, per-link bounding box primitive generation, and audit.
- [ ] Run `python -m pytest tests/test_link_aware_robot_package.py -q`; expect pass.

### Task 3: Phase 0 Articulated Case Integration

**Files:**
- Modify: `src/primitive_collision_compiler/phase0.py`
- Test: `tests/test_phase0_benchmark.py`

- [ ] Replace the old articulated-case expectation that link-boundary audit is a fallback with a failing expectation for generated package evidence.
- [ ] Assert `robot_package_result.status == "generated"`, `primitive_or_hull_count` matches the package primitive count, and `link_boundary_audit.metrics.link_aware_package_generated is True`.
- [ ] Implement `_robot_package_result` handling inside `_articulation_case_report`.
- [ ] Set report scope `link_aware_robot_package_generation` from articulated case evidence.
- [ ] Run the focused Phase 0 tests.

### Task 4: Records And Verification

**Files:**
- Create: `docs/records/2026-05-26-link-aware-robot-package-generation.md`
- Modify current DeepDive/paper evidence files only after real report evidence exists.

- [ ] Run focused unit tests.
- [ ] Run the real Phase 0 benchmark in the clean Newton environment.
- [ ] Parse the generated report for Franka link package counts and link-boundary audit status.
- [ ] Update docs and paper evidence with only the supported claim: link-aware package generation and boundary audit evidence, not whole-robot collider quality.
- [ ] Run `python scripts/validate_docs.py`, `git diff --check`, `make test`, and `make test-paper`.
