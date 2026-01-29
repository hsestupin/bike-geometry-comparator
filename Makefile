.DEFAULT_GOAL:=test

.PHONY: test
test: sync lint mypy
	@uv run pytest -s -vv

.PHONY: lint
lint:
	@uv run ruff check
	@uv run ruff format --check

.PHONY: format
format:
	@uv run ruff format

.PHONY: mypy
mypy:
	@uv run mypy . --exclude dist --exclude docs --exclude build

.PHONY: sync
sync:
	@uv sync --locked --all-extras --dev