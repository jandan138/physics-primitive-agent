.PHONY: install test validate docs-check

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

validate:
	python scripts/validate_docs.py
	python -m pytest

docs-check:
	python scripts/validate_docs.py
