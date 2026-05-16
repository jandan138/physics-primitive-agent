# Four-Block Slice Report Design

## Goal

Add a command-only report that summarizes one already recorded slice across the four Newton CPD
workbench blocks:

1. primitive fitting and selection;
2. merge/search;
3. offline diagnostic reports;
4. Newton task comparison.

This is a workbench-integration report. It does not run new geometry algorithms, Newton tasks, real
assets, benchmarks, or quality measurements.

## First Supported Slice

The first supported slice is:

```text
cost_guided_lookahead
```

It summarizes the already recorded synthetic lookahead lane:

```text
two-step lookahead merge report
-> package/mapping probe
-> contact-gated Newton task-smoke probe
```

## Report Shape

The report stage is:

```text
cpd_like_four_block_slice_report
```

Top-level fields:

- `status`;
- `claim_boundary`;
- `evidence_level`;
- `status_semantics`;
- `slice_id`;
- `command_only: true`;
- `synthetic_only: true`;
- `real_usd_rerun_triggered: false`;
- `newton_task_comparison_triggered: false`;
- `report_newton_task_comparison_triggered: false`;
- `blocks`;
- `summary`;
- `next_action`.

Block entries:

- `block_id`;
- `status`;
- `summary`;
- `evidence_records`;
- `command_surface`;
- `claim_boundary`;
- `claim_supported`;
- `claim_not_supported`.

The first slice should emit four block entries:

- `primitive_fitting_selection`: `not_changed_for_this_slice`;
- `merge_search`: `complete`;
- `offline_diagnostic_reports`: `complete`;
- `newton_task_comparison`: `complete`.

## Status Rules

Top-level `status` is `smoke_passed` only when:

- the `slice_id` is supported;
- all required evidence record paths exist;
- merge/search, offline diagnostics, and Newton task comparison blocks are complete;
- primitive fitting/selection is explicitly marked as unchanged for this slice;
- no real-asset rerun is triggered;
- next action is claim-bounded.

If a required record path is missing, return `partial` with the missing paths.

The report must resolve record paths from the repository root, not from the process current working
directory. It must not call decomposition helpers, package builders, USD loaders, or Newton runtime
helpers. It should include compact block summaries and record links only, not source package,
contact, drop/settle, or sphere-rain payloads.

## CLI

Add:

```text
--run-cpd-like-four-block-slice-report
```

The command should be config-free for the first slice. It emits strict JSON and returns 0 only when
the report status is `smoke_passed`.

## Claim Boundary

Allowed wording:

- "four-block slice status report";
- "command-only workbench integration report";
- "evidence map for an already recorded synthetic slice";
- "next legal gate summary."

Forbidden wording:

- "new benchmark result";
- "new Newton task result";
- "real asset result";
- "bed or Franka result";
- "collision geometry quality result";
- "policy ranking";
- "paper reproduction complete";
- "deployment or certification conclusion."

## Verification Strategy

Use TDD:

1. RED report-builder test for the `cost_guided_lookahead` slice.
2. RED missing-record test that returns `partial`.
3. RED strict JSON serialization test.
4. RED CLI JSON and non-finite JSON tests.
5. GREEN implementation with no Newton/runtime calls.
6. Dated record, registry, index, evidence, claim-boundary, CPD story, and latest-loop updates.
7. Multi-agent implementation and documentation review.
8. Focused tests, full tests, docs validation, site claim validation, and `git diff --check`.

## Self-Review

No placeholders remain. The report summarizes existing evidence and does not add algorithmic,
runtime, real-asset, benchmark, quality, deployment, certification, or paper-reproduction claims.
