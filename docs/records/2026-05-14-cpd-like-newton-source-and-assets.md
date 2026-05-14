# 2026-05-14 CPD-Like Newton Source And Assets

## Date

2026-05-14

## Status

Complete; historical source and smoke-asset intake.

## Changes

- Decided that Newton should be used from the official source repository as a sibling checkout,
  not vendored into this repository.
- Selected the user-provided GRScenes bed USD as a development smoke asset only.
- Selected a local GRScenes Franka USD candidate as a Newton import compatibility smoke asset only.
- Kept the robot asset out of the first CPD-like rigid-object aggregate.

## Verification

- Confirmed the bed USD exists at the user-provided path and is about 40M.
- Computed bed SHA-256:
  `1bc5a26ddb2551de4ac7acbc13a39d118beda10db503419da65ce82528322265`.
- Found a local Franka USD candidate at
  `/cpfs/user/zhuzihou/assets/zzh-grscenes/robots/franka/franka.usd`.
- Computed Franka USD SHA-256:
  `2bfd004928d4157ca2fdca3e79bcfb913b4008eef3ec16f839ad89314141976b`.
- Attempted `git clone --depth 1 https://github.com/newton-physics/newton.git /cpfs/user/zhuzihou/dev/newton`;
  the command failed with `Proxy CONNECT aborted`.
- Checked that `python -c "import newton"` currently fails with `ModuleNotFoundError`.

## Artifacts

- Design spec:
  `docs/superpowers/specs/2026-05-14-cpd-like-newton-baseline-design.md`
- Official Newton source URL:
  `https://github.com/newton-physics/newton`
- Preferred local Newton source directory:
  `/cpfs/user/zhuzihou/dev/newton`

## Claim Impact

- No Newton run, primitive decomposition result, benchmark result, or compiler functionality is
  supported by this record.
- The clone failure is a dependency setup gap, not an algorithm result.
- The bed and Franka assets are smoke candidates only until provenance, license, unit, dependency,
  and normalization metadata are complete.

## Next Action

- Historical next action superseded. Newton source and clean Python/Newton import readiness later
  passed in the clean environment record; current next action is the first named Newton diagnostic
  probe consuming the geometry-only primitive proposal output.
