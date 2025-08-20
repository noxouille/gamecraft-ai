.PHONY: help install dev test lint format type-check run clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install production dependencies"
	@echo "  make dev        - Install all dependencies including dev"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make type-check - Run type checking"
	@echo "  make run        - Run the application"
	@echo "  make clean      - Clean up generated files"

install:
	uv sync --no-dev

dev:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

type-check:
	uv run mypy src

run:
	uv run python -m src.gamecraft_ai.main

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
