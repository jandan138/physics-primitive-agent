# Experiments

This directory tracks experiment definitions and registries. Heavy run outputs are not committed.

## Policy

- Commit small configs, registry entries, and summary records.
- Do not commit `experiments/runs/`; keep generated logs and raw outputs there or in external
  storage.
- Every experiment that supports a claim needs a dated record under `docs/records/`.
