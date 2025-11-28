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
	poetry run black services tests
	poetry run isort services tests

lint: ## Run ruff linter
	poetry run ruff check services tests

lint-fix: ## Run ruff linter with auto-fix
	poetry run ruff check --fix services tests

type-check: ## Run mypy type checker
	poetry run mypy services

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage report
	poetry run pytest --cov=services --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	poetry run pytest-watch

check-all: format lint type-check test ## Run all checks (format, lint, type-check, test)

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