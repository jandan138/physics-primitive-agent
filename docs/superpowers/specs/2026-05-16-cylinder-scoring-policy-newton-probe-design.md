# Cylinder Scoring Policy Newton Probe Design

## Goal

Run a named Newton diagnostic over the synthetic package that changed in the cylinder
scoring-policy package probe, without changing default package generation or touching real USD.

The slice answers one narrow question:

```text
Can the explicitly opt-in synthetic box->cylinder package change pass the existing Newton contact,
drop/settle, and sphere-rain smoke gates under recorded settings?
```

## Scope

In scope:

- build the default `box` package and opt-in `cylinder` package for `cylinder_near_miss_cluster`;
- run `newton_contact_smoke` for each synthetic package;
- run `newton_drop_settle` and `newton_sphere_rain` only when contact passes;
- record blocked task payloads when contact does not pass;
- expose a config-required CLI command that reads only `newton.source_dir`, `device`, and Newton
  diagnostic task options.

Out of scope:

- changing the existing package-probe record, which remains mapping-only;
- changing default scoring policy or default package generation;
- running bed, Franka, or any real-USD package;
- claiming collision quality, safety, benchmark performance, scoring calibration, or CPD
  reproduction.

## Expected Behavior

For `cylinder_near_miss_cluster`:

- default package contains one `box`;
- opt-in package contains one `cylinder`;
- contact canary runs for both packages;
- drop/settle and sphere-rain run for a package only if that package's contact canary returns
  `smoke_passed`;
- aggregate status is `smoke_passed` only if all contact and task smokes pass.

## Claim Boundary

Allowed wording:

- "explicitly opt-in synthetic Newton diagnostic";
- "named contact, drop/settle, and sphere-rain task smokes";
- "synthetic task-smoke execution evidence";
- "not collision-quality validation";
- "default package generation and real-USD packages unchanged."

Forbidden wording:

- "validated cylinder scoring policy";
- "cylinder is better than box";
- "bed/Franka improved";
- "benchmark result";
- "real contact-stress measurement";
- "CPD reproduced";
- "simulation-verified" or safety-certification language.

## Verification

The slice requires:

1. RED tests for the missing report builder and CLI flag;
2. focused GREEN tests for contact-gated tasks and blocked task payloads;
3. a config example under `configs/experiments/`;
4. a real clean-env CLI smoke when the local Newton source is available;
5. docs and claim-boundary updates;
6. implementation and docs review before final status is marked complete.
