.DEFAULT_GOAL:=test
CLIENT_SRC:=src/client

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
	@pnpm -C $(CLIENT_SRC) install

.PHONY: clean
clean:
	rm -rf $(CLIENT_SRC)/node_modules

.PHONY: build
build:
	# building database.csv
	@uv run bgc
	mkdir -p $(CLIENT_SRC)/public && cp build/database.csv $(CLIENT_SRC)/public

.PHONY: dev
dev: build
	@pnpm -C $(CLIENT_SRC) dev

.PHONY: build-client
build-client: build
	@pnpm -C $(CLIENT_SRC) build
