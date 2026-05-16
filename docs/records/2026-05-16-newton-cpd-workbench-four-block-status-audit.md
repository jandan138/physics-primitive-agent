# 2026-05-16 Newton CPD Workbench Four-Block Status Audit

## Date

2026-05-16

## Status

Complete

## Current Status Note

This audit captured the status before `2026-05-16-four-block-slice-report.md` and
`2026-05-16-four-block-workbench-completion-audit.md` were completed. Treat its "single
four-block report is missing" language as historical. The current follow-on status is that the
bounded `cost_guided_lookahead` four-block report exists as a command-only evidence map.

## Objective Restatement

The four-block workbench objective is not full CPD paper reproduction. It is a claim-bounded
Newton-centered diagnostic workbench with four inspectable blocks:

1. primitive fitting and selection;
2. merge/search;
3. offline diagnostic reports;
4. Newton task comparison.

The workbench is useful only if each block has executable commands, dated records, and explicit
claim boundaries. Passing a block means "usable for the next diagnostic slice," not "paper-level
algorithm complete."

## Prompt-To-Artifact Checklist

| Block | Success criterion | Current evidence | Audit result |
| --- | --- | --- | --- |
| Primitive fitting and selection | Synthetic and capped real-asset runs can expose why a primitive was selected, including candidate-loss rows and support-aware guards. | `configs/experiments/newton_native_fitting_comparison.yaml`, `configs/experiments/bed_franka_native_probe_comparison.yaml`, records `2026-05-15-low-support-native-extension-admissibility.md`, `2026-05-15-real-usd-native-fitting-comparison.md`, `2026-05-15-candidate-loss-triage.md`, and the near-miss/scoring-policy records from 2026-05-16. | Usable workbench block. Still not primitive-quality evidence or paper-faithful fitting. |
| Merge/search | At least one controlled grouping change can be explained on a synthetic fixture before it enters package and Newton gates. | Records `2026-05-16-controlled-merge-search-package-probe.md`, `2026-05-16-controlled-merge-search-newton-probe.md`, `2026-05-16-cost-guided-lookahead-merge.md`, `2026-05-16-cost-guided-lookahead-package-probe.md`, and `2026-05-16-cost-guided-lookahead-newton-probe.md`. | Usable workbench block for synthetic merge/search slices. Still not global search or the CPD paper optimizer. |
| Offline diagnostic reports | The system can report reviewable diagnostic fields before Newton tasks: candidate audits, objective terms, merge excess, package mapping, and failure labels. | `cpd_like_objective_report`, synthetic comparison reports, candidate-loss diagnosis, package/mapping probes, and records `2026-05-15-cpd-like-objective-report.md`, `2026-05-15-cpd-eq4-alignment-metadata.md`, `2026-05-16-cost-guided-merge-step-trace.md`, and package-probe records. | Partially usable. The fields exist, but there is no single four-block workbench report that summarizes all gates for one slice. |
| Newton task comparison | A changed synthetic package pair can be gated by mapping, contact canary, drop/settle, and sphere-rain under recorded settings; capped real-asset first-mesh packages can exercise the same gate execution path. | Synthetic task-smoke records for cylinder scoring policy, controlled merge-search, and lookahead merge/search package pairs, plus real-USD native task comparison records for capped bed/Franka gate execution. | Usable for named synthetic changed-package probes and capped first-mesh gate execution. Still not benchmark, broad asset evidence, or contact-stress measurement. |

## Current Distance To A Newton CPD Workbench

The repository is past the "pieces exist" stage. It can already execute the main diagnostic loop:

```text
USD or synthetic fixture
-> CPD-like / native primitive proposal lane
-> offline objective or candidate-loss accounting
-> CollisionPackage
-> Newton mapping
-> contact-gated Newton task smokes
-> dated record and claim boundary
```

For an internal Newton CPD diagnostic workbench MVP, the remaining gap is mostly integration and
report ergonomics, not missing primitives or missing Newton plumbing.

Approximate status:

- internal diagnostic workbench MVP: about 70-75 percent;
- paper-aligned algorithm reproduction: about 30-40 percent;
- benchmark/evaluation story: still early.

The biggest missing MVP piece is a single slice-level workbench report that shows the four blocks
together. Today, a reviewer has to read several records and commands to answer:

```text
What changed?
Which block changed it?
Did the package change?
Did the package map?
Did Newton contact/tasks run?
What claim is allowed?
What is still out of scope?
```

## Missing But Not Yet Claimable

The following remain outside the current claim boundary:

- paper-faithful primitive fitting and full objective implementation;
- global primitive-set search;
- broad real-asset or whole-robot evidence;
- collision geometry quality measurement;
- benchmark-suite comparison;
- deployment or certification conclusions;
- paper-level reproduction.

## Recommended Next Slice

Do not rerun capped bed/Franka merely because the synthetic lookahead task smoke passed. A real
rerun needs a separate real package change plus full mapping, contact-canary, task-gate, and
dated-record gates.

The next best engineering slice is:

```text
four-block slice report
```

This should be a command-only diagnostic that takes one already recorded slice, such as the
lookahead synthetic lane, and emits a compact report with:

- block coverage status;
- linked record paths;
- package-change status;
- mapping/task gate status;
- allowed claim boundary;
- next legal gate.

That report would make the workbench feel like a workbench rather than a collection of separate
probes, while avoiding new algorithmic or quality claims.

## Verification

This is a documentation audit. It does not add executable code or experiment evidence. It was
prepared from the dated records and current docs listed above and should be reviewed as a status
map, not as a new benchmark or result.
