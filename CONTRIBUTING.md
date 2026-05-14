# Contributing

## Development Commands

- `make install`: install the project in editable development mode with development tools.
- `make test`: run pytest.
- `make validate`: run the current documentation validator and pytest.
- `make docs-check`: run the current documentation validator.

Direct command equivalents:

```sh
python -m pip install -e ".[dev]"
python -m pytest
python scripts/validate_docs.py
```

## Claim Boundaries

Keep current claims aligned with the bootstrap status. The repository is a
proposal/bootstrap and does not implement real mesh processing yet. Prefer
simulation-checked for current documentation. Do not claim production readiness,
runtime mesh compilation, or simulation-verified results unless later evidence and review
records explicitly support those stronger statements.

## Artifact Policy

Large assets, generated assets, binary outputs, and experiment byproducts should not be
committed. Keep generated material outside the repository unless a later task defines a
small, reviewable fixture or documentation artifact.

## Source Layout

Source code lives under `src/primitive_collision_compiler/`. Early bootstrap code is limited
to command-surface stubs and typed contracts; real compiler behavior must wait for the task
that owns it. Tests live under `tests/`.

## Documentation Records

Keep research notes, DeepDive records, and planning documents in `docs/`. Documentation
should distinguish proposals, reviewed source notes, simulation-checked records, and future
implementation work.
