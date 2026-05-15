# Newton-Native Primitive Policy Design

## Context

The capped-cylinder proxy slice clarified a useful but risky boundary. It reduced one offline
paper primitive-vocabulary gap, but it did not add Newton mapping or task-level evidence. After
reviewing Newton's source API and the CPD paper's engine discussion, the project should not use
paper primitive vocabulary as the runtime roadmap.

The runtime roadmap should be Newton-native first. Paper-alignment remains useful for diagnostics,
but it should not force `frustum` or `trapezoidal_prism` into Newton task probes before there is
clear engine support and evidence.

## Decision

Split primitive work into two lanes:

1. **Newton-native runtime lane**: primitives that can be mapped into Newton and exercised by
   named Newton diagnostics.
2. **Paper-alignment offline lane**: primitives or accounting terms that explain CPD-paper gaps
   without implying runtime support.

The capped-cylinder proxy stays in the offline lane. The next runtime implementation should target
a native analytic primitive bundle instead of one primitive at a time.

## Native Bundle Scope

The next implementation slice may add runtime support for this bundle together:

```text
box, sphere, capsule, cylinder, cone, ellipsoid
```

`box`, `sphere`, and `capsule` are already mapped. The new runtime work is therefore:

```text
cylinder, cone, ellipsoid
```

This is intentionally different from the CPD paper primitive vocabulary. The paper includes
frustums and isosceles trapezoidal prisms; those should remain offline diagnostics or future
fallback research targets unless a separate Newton mapping and task-level diagnostic record exists.

## Why One Bundle Is Reasonable

Adding these three native primitives together is reasonable because they share the same integration
surface:

- `map_package_shapes` validation and schema reporting;
- contact canary representative shape coverage;
- drop/settle dynamic package construction;
- sphere-rain static package construction;
- bounds and support-height calculations;
- claim-boundary documentation and records.

Doing one primitive at a time would repeat the same plumbing and review overhead. Doing all native
analytic additions in one slice is acceptable if the tests and records prove each primitive kind
individually.

## Why Not Add Every Newton Shape

Do not include every Newton builder shape in this bundle.

Out of scope for the next runtime bundle:

- `plane`: environment/ground primitive, not an object collision package primitive.
- `heightfield`: terrain representation, not a compact object primitive.
- `mesh`: fallback or source geometry path, not a primitive-first analytic target.
- `convex_hull`: fallback baseline, not an analytic primitive.
- `gaussian`: not part of the current rigid collision primitive-first target.
- `frustum` and `trapezoidal_prism`: CPD-paper vocabulary, but not native runtime targets for the
  current Newton lane.

## Implementation Boundary For The Future Slice

The future runtime bundle should not only mark new kinds as "mapped." It must also update every
Newton diagnostic path that consumes mapped shapes:

- shape validation;
- Newton builder calls;
- world-bound estimates;
- support-height estimates;
- contact canary probes;
- tests for valid and invalid dimensions;
- one synthetic package containing all supported native kinds;
- one named runtime diagnostic record after the clean Newton environment runs.

If a primitive maps but a diagnostic path cannot build or bound it, that primitive is not supported.

## Claim Boundary

Before the future implementation exists, the repository supports only this planning claim:

```text
The next runtime primitive roadmap is Newton-native first: add cylinder, cone, and ellipsoid
mapping as one verified bundle, while keeping CPD-only frustum and trapezoidal-prism work in the
offline paper-alignment lane.
```

It does not yet support claiming Newton runtime support for cylinder, cone, or ellipsoid from this
repository's collision package path.

## Recommended Next Step

Write an implementation plan for the native analytic primitive bundle. The first tests should prove
that `cylinder`, `cone`, and `ellipsoid` are rejected today, then implement mapping and diagnostic
construction together with separate per-kind assertions.
