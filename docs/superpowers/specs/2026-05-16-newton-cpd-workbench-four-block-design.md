# Newton CPD Workbench Four-Block Design

## Goal

Turn the current CPD-like diagnostic pipeline into a Newton-centered diagnostic workbench for
future CPD paper-story experiments, one claim-bounded slice at a time.

The four target blocks are:

1. better primitive fitting and selection;
2. better merge/search;
3. offline quality reports;
4. Newton task comparison.

This design does not declare those blocks complete. It defines the route for completing them and
the first executable slice after the current support-aware baseline: a
`cylinder_near_miss_cluster` fixture.

## Current Baseline

The repository can already run:

```text
USD or synthetic mesh
-> CPD-like primitive proposals
-> candidate audit and candidate-loss diagnosis
-> CollisionPackage
-> Newton mapping, contact canary, drop/settle, and sphere-rain smokes
```

The latest support-aware slice changed the current capped bed/Franka result to:

- `bed_dev_smoke`: native lane selects `32` boxes;
- `franka_import_smoke`: native lane selects `32` boxes;
- three capped Franka raw-cost cylinder candidates are reported as support-blocked;
- bed and Franka still expose cylinder near-miss targets.

That means the low-support branch is guarded. The next useful primitive-selection target is the
near-miss branch: clusters where `box` wins but `cylinder` is close under the current surrogate.

## Four-Block Deliverables

### Block 1: Primitive Fitting And Selection

Deliverable:

```text
synthetic fixtures that isolate primitive-selection weaknesses
-> candidate audit explains raw cost, support-aware rank, and selected primitive
-> one controlled fitting or selection change can be tested before real USD reruns
```

First slice:

```text
cylinder_near_miss_cluster
```

The fixture should intentionally preserve the current failure pattern:

- `box` is selected;
- `cylinder` is the best native extension candidate;
- `cylinder` is support-admissible;
- `cylinder` is close enough to be a near-miss, not support-blocked.

The first slice should not change production selection behavior relative to the current
support-aware baseline and should not be added to the native fitting success report yet. It
creates an inspectable primitive-ranking target for the next fitting or merge/search change.

### Block 2: Merge/Search

Deliverable:

```text
one controlled merge/search improvement
-> synthetic comparison explains why grouping changed
-> candidate-loss labels say whether primitive fitting or grouping is the likely bottleneck
```

This block should start only after the `cylinder_near_miss_cluster` fixture exists, because the
fixture tells whether the near miss is caused by cylinder fitting or by cluster grouping.

### Block 3: Offline Quality Reports

Deliverable:

```text
diagnostic report with explicit non-quality and quality-proxy fields
```

The first version should remain claim-bounded. It may report:

- selected primitive counts;
- raw-cost margin;
- support-admissibility status;
- containment proxy;
- geometric excess proxy;
- candidate-loss labels;
- Newton mapping completeness.

It must not call those fields benchmark quality or collision-quality validation.

### Block 4: Newton Task Comparison

Deliverable:

```text
old package vs new package
-> full mapping gate
-> contact canary
-> drop/settle and sphere-rain task smokes
-> task delta summary under recorded settings
```

The comparison must run only after a synthetic slice produces an interpretable package change. A
Newton task delta without an algorithmic explanation is not enough evidence for a CPD paper claim.

## First Slice Design: `cylinder_near_miss_cluster`

Add a deterministic synthetic fixture helper, direct primitive-ranking test, and dedicated
near-miss workbench report. It should model a supported cluster that is close to cylindrical, but
still loses to `box` under the current weighted-volume surrogate.

Expected current behavior:

```text
selected primitive: box
best extension candidate: cylinder
cylinder support: admissible
relative gap: <= 0.25
suggested next slice: primitive_fitting_near_miss_fixture
expectation status: matched
```

This fixture is an expected diagnostic target, not a successful native primitive selection. It
should live beside the existing synthetic mesh helpers and be exposed through the dedicated
near-miss workbench report, not through `_native_fitting_cases()`.

## Claim Boundaries

Allowed wording:

- "near-miss primitive-selection fixture";
- "synthetic diagnostic target";
- "candidate-loss planning metadata made reproducible";
- "support-admissible cylinder near miss";
- "next target for fitting or merge/search work."

Forbidden wording:

- "CPD reproduced";
- "cylinder improved collision quality";
- "Franka collider validated";
- "benchmark result";
- "paper-faithful optimizer";
- "Newton task quality improvement."

## Verification Strategy

The first slice requires:

1. a failing test that expects `_cylinder_near_miss_cluster_mesh()` to exist;
2. a failing test body that classifies the fixture as a support-admissible cylinder near miss;
3. minimal fixture implementation;
4. near-miss workbench report and CLI smoke;
5. targeted pytest;
6. docs validation and `git diff --check`;
7. read-only multi-agent review for code semantics and claim boundaries.

Full Newton task reruns are not required for the fixture-only slice because it does not change real
USD package generation. They become required when a later slice changes package selection or
grouping.
