# Assets

This directory is for small manifests and hand-authored examples. Raw or generated 3D assets are
not committed by default.

## Policy

- Keep raw assets under `assets/raw/` and generated assets under `assets/generated/`.
- Commit only lightweight manifests, licenses, and tiny examples needed for tests.
- Record source, license, normalization, and task suitability before an asset enters a benchmark.
- Treat generated collision packages as safety-affecting artifacts that require review.
