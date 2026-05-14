# Newton Notes

These are working notes for Newton integration. They are not a replacement for versioned
experiment records.

## Current Assumptions

- The first compiler surface should produce explicit collision packages that can be inspected
  before any simulation run.
- Dry-run config parsing is the current executable contract.
- Newton checks should be treated as diagnostic probes over named tasks, not broad safety
  certification.

## Phase 0 Probe Shape

- Drop: measure whether an asset settles with plausible contacts and bounded penetration.
- Stack or slide: expose coarse collider overhangs, missing support, and solver jitter.
- Sphere rain or contact stress: stress-test dense contact regions and hidden holes.
- Precision rejection: record when no safe primitive approximation is found and fallback is used.

## Records Required For Any Newton Claim

- Config file and git commit.
- Asset identifier and source.
- Newton version or environment identifier.
- Solver settings that affect contacts.
- Summary metrics and failure taxonomy labels.
