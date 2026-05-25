.PHONY: install test test-fast test-full test-paper validate validate-full docs-check

install:
	python -m pip install -e ".[dev]"

test: test-fast

test-fast:
	python -m pytest -q -m "not paper_offline"

test-full:
	python -m pytest -q

test-paper:
	python -m pytest -q -m "paper_offline"

validate:
	python scripts/validate_docs.py
	python -m pytest -q -m "not paper_offline"

validate-full:
	python scripts/validate_docs.py
	python -m pytest -q

docs-check:
	python scripts/validate_docs.py
