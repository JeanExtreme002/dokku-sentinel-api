RED=\033[0;31m
YELLOW=\033[0;33m
GREEN=\033[0;32m
NC=\033[0m # No Color

.PHONY: run
run:  ## Run the API locally
	@poetry run python -m src

.PHONY: install
install:  ## Install the API dependencies locally
	@command -v poetry >/dev/null 2>&1 || (echo "$(YELLOW)Installing Poetry...$(NC)" && pip install poetry)
	@poetry install --with dev --no-root

.PHONY: lint
lint:  ## Run lint
	@poetry run flake8 src && poetry run black --check src

.PHONY: lint-fix
lint-fix:  ## Run lint fix
	@{ \
		poetry run isort src; \
		\
		poetry run black src; \
	}
