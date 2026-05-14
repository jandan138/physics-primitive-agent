# Newton Notes

These are working notes for Newton integration. They are not a replacement for versioned
experiment records.

## Current Assumptions

- The first compiler surface should produce explicit collision packages that can be inspected
  before any simulation run.
- Dry-run config parsing, USD asset-open smoke diagnostics, Newton source import diagnostics, and
  environment-readiness diagnostics are the current executable contracts.
- Newton checks should be treated as diagnostic probes over named tasks, not broad safety
  certification.
- Newton source is expected as an external sibling checkout, not vendored into this repository.
- The current clean local Python/Newton readiness state is `smoke_passed`; this is environment and
  provenance evidence, not an algorithm or simulation result.
- The first named task-level Newton smoke diagnostic is `newton_drop_settle` for the capped bed
  CPD-like collision package. It is diagnostic evidence for one recorded asset/config/environment,
  not collision quality validation.
- The second named task-level Newton smoke diagnostic is `newton_sphere_rain`, a sphere-rain
  contact-density proxy over the capped bed CPD-like collision package. The density is based on
  unique contacted probe spheres, while raw contact-row counts remain available for review. It is
  not a calibrated contact-stress measurement.

## Environment Readiness Before Newton Claims

Before any Newton simulation claim, record:

- `NPC_ENV_ROOT`, `NPC_PYTHON`, `NPC_CODE_ROOT`, `NEWTON_SOURCE_DIR`, and `NPC_OUTPUT_DIR`;
- Python executable, realpath, prefix, site packages, and module provenance;
- Newton source remote, branch, commit, dirty state, and submodule status;
- GPU visibility and output directory writability;
- setup-script fingerprint when configured, without sourcing or storing script contents.

## Phase 0 Probe Shape

- Drop: measure whether an asset ends with plausible contact, bounded final speed, and bounded
  penetration.
- Drop/settle status now uses estimated support height, not only body-origin height, for
  ground-plane breach decisions.
- Stack or slide: expose coarse collider overhangs, missing support, and solver jitter.
- Sphere rain or contact-density proxy: stress-test dense contact regions and hidden holes without
  claiming calibrated physical stress.
- Precision rejection: record when no safe primitive approximation is found and fallback is used.

## Records Required For Any Newton Claim

- Config file and git commit.
- Asset identifier and source.
- Newton version or environment-readiness identifier.
- Solver settings that affect contacts.
- Summary metrics and failure taxonomy labels.
