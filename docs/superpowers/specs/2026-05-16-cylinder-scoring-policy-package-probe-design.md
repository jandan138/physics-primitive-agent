# Cylinder Scoring Policy Package Probe Design

## Goal

Bridge the current synthetic opt-in scoring-policy selection probe into the package path without
changing default decomposition, real-USD configs, or Newton task execution.

The slice answers one narrow question:

```text
Can an explicitly requested cylinder score multiplier change a deterministic synthetic
CollisionPackage, and can that changed package map to Newton-supported shapes?
```

## Scope

In scope:

- thread `primitive_score_multipliers` through `decompose_mesh`;
- keep default `decompose_mesh` behavior unchanged;
- build a synthetic report over `cylinder_near_miss_cluster` and `boxy_cuboid_guardrail`;
- convert default and opt-in decompositions into `CollisionPackage` objects;
- record Newton shape-mapping summaries only.

Out of scope:

- changing config-driven real-USD package generation;
- changing default scoring policy;
- running Newton contact, drop/settle, or sphere-rain tasks;
- claiming the cylinder is better than box;
- claiming the multiplier is calibrated or safe.

## Expected Behavior

For `cylinder_near_miss_cluster`:

- default package contains one `box`;
- opt-in package with `primitive_score_multipliers={"cylinder": 0.88}` contains one `cylinder`;
- the opt-in package reports complete Newton shape-mapping coverage.

For `boxy_cuboid_guardrail`:

- default package contains one `box`;
- opt-in package still contains one `box`;
- the guardrail records that this clearly boxy fixture remains `box` under the opt-in multiplier.

## Claim Boundary

Allowed wording:

- "explicitly opt-in synthetic package probe";
- "changed synthetic `CollisionPackage`";
- "Newton shape-mapping summary";
- "default package generation unchanged";
- "no real-USD or Newton task evidence."

Boundary sentence to reuse:

```text
This is an explicitly opt-in synthetic package probe with a Newton shape-mapping summary only; it
does not change default package generation and does not run Newton contact or task diagnostics.
```

Forbidden wording:

- "default scoring policy changed";
- "cylinder improves collision quality";
- "Newton task checked";
- "simulation-checked";
- "bed/Franka improvement";
- "benchmark result";
- "CPD reproduced."

## Verification

The slice requires:

1. failing tests for the new `decompose_mesh` option and report builder;
2. focused GREEN tests for default unchanged, opt-in near-miss package changed, guardrail unchanged,
   and mapping coverage recorded;
3. CLI JSON smoke for `--run-cpd-like-cylinder-scoring-policy-package-probe`;
4. docs and claim-boundary updates;
5. multi-agent implementation and docs review before final verification.
