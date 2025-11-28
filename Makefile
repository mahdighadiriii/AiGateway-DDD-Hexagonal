.PHONY: help install install-dev format lint type-check test test-cov clean run-gateway

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	poetry install --only main

install-dev: ## Install all dependencies including dev
	poetry install
	poetry run pre-commit install

format: ## Format code with black and isort
	poetry run black services
	poetry run isort services

lint: ## Run ruff linter
	poetry run ruff check services

lint-fix: ## Run ruff linter with auto-fix
	poetry run ruff check --fix services

type-check: ## Run mypy type checker
	poetry run mypy services

test: ## Run all tests from all services
	@echo "Running tests for all bounded contexts..."
	@for dir in services/*/tests; do \
		if [ -d "$$dir" ]; then \
			echo "Testing $$(dirname $$dir)..."; \
			poetry run pytest "$$dir" -v; \
		fi \
	done

test-completion: ## Run tests for completion context
	poetry run pytest services/completion_context/tests -v

test-billing: ## Run tests for billing context
	poetry run pytest services/billing_context/tests -v

test-workflow: ## Run tests for workflow context
	poetry run pytest services/workflow_context/tests -v

test-gateway: ## Run tests for gateway service
	poetry run pytest services/gateway_service/tests -v

test-cov: ## Run tests with coverage report for all services
	poetry run pytest services/ --cov=services --cov-report=html --cov-report=term

test-cov-completion: ## Run tests with coverage for completion context
	poetry run pytest services/completion_context/tests --cov=services/completion_context --cov-report=html --cov-report=term

check-all: format lint type-check ## Run all checks (format, lint, type-check)

clean: ## Clean up cache and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

run-gateway: ## Run the gateway service
	poetry run uvicorn services.gateway_service.gateway_service.main:app --reload --host 0.0.0.0 --port 8000

run-completion: ## Run completion context service (if standalone)
	poetry run uvicorn services.completion_context.completion_context.main:app --reload --host 0.0.0.0 --port 8001

shell: ## Start IPython shell with project context
	poetry run ipython

update: ## Update all dependencies
	poetry update

lock: ## Update lock file without installing
	poetry lock --no-update

export-requirements: ## Export requirements.txt
	poetry export -f requirements.txt --output requirements.txt --without-hashes

export-requirements-dev: ## Export requirements-dev.txt
	poetry export -f requirements.txt --output requirements-dev.txt --without-hashes --with dev

# Service-specific commands
init-tests: ## Initialize test directories for all bounded contexts
	@echo "Creating test directories for bounded contexts..."
	mkdir -p services/completion_context/tests
	mkdir -p services/billing_context/tests
	mkdir -p services/workflow_context/tests
	mkdir -p services/gateway_service/tests
	mkdir -p services/platform/tests
	@echo "Creating __init__.py files..."
	touch services/completion_context/tests/__init__.py
	touch services/billing_context/tests/__init__.py
	touch services/workflow_context/tests/__init__.py
	touch services/gateway_service/tests/__init__.py
	touch services/platform/tests/__init__.py
	@echo "Creating conftest.py files..."
	touch services/completion_context/tests/conftest.py
	touch services/billing_context/tests/conftest.py
	touch services/workflow_context/tests/conftest.py
	touch services/gateway_service/tests/conftest.py
	touch services/platform/tests/conftest.py
	@echo "✅ Test directories initialized!"
