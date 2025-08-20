#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="gamecraft-ai"
PYTHON_VERSION="3.12"
DEFAULT_DEPENDENCIES=(
    "fastapi"
    "uvicorn[standard]"
    "pydantic"
    "httpx"
    "pytest"
    "pytest-asyncio"
    "pytest-cov"
    "ruff"
    "mypy"
    "pre-commit"
)

# Function to print colored messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in correct directory
if [ ! -f "LICENSE" ]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

log_info "Starting project initialization for ${PROJECT_NAME}..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    log_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"

    if ! command -v uv &> /dev/null; then
        log_error "Failed to install uv. Please install manually: https://github.com/astral-sh/uv"
        exit 1
    fi
    log_info "uv installed successfully"
else
    log_info "uv is already installed ($(uv --version))"
fi

# Initialize Python project with uv
log_info "Initializing Python ${PYTHON_VERSION} project with uv..."
uv init --python "${PYTHON_VERSION}" --name "${PROJECT_NAME}" --no-readme --no-pin-python || {
    log_warn "Project might already be initialized, continuing..."
}

# Create virtual environment
log_info "Creating virtual environment..."
uv venv --python "${PYTHON_VERSION}"

# Activate virtual environment instructions
log_info "Virtual environment created at .venv"

# Install dependencies
log_info "Installing dependencies..."
for dep in "${DEFAULT_DEPENDENCIES[@]}"; do
    log_info "  Installing ${dep}..."
    uv pip install "${dep}"
done

# Create project structure
log_info "Creating project structure..."

# Create source directory (ensure underscore in name)
PROJECT_DIR_NAME=$(echo "${PROJECT_NAME}" | tr '-' '_')
mkdir -p src/${PROJECT_DIR_NAME}
mkdir -p tests
mkdir -p docs
mkdir -p scripts

# Create __init__.py files
touch src/${PROJECT_DIR_NAME}/__init__.py
touch tests/__init__.py

# Create main application file
if [ ! -f "src/${PROJECT_DIR_NAME}/main.py" ]; then
    cat > "src/${PROJECT_DIR_NAME}/main.py" << 'EOF'
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="GameCraft AI",
    description="AI-powered game development assistant",
    version="0.1.0"
)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Welcome to GameCraft AI"})

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
EOF
    log_info "Created main application file"
fi

# Create configuration file
if [ ! -f "src/${PROJECT_DIR_NAME}/config.py" ]; then
    cat > "src/${PROJECT_DIR_NAME}/config.py" << 'EOF'
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="GameCraft AI")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
EOF
    log_info "Created configuration file"
fi

# Create test file
if [ ! -f "tests/test_main.py" ]; then
    cat > "tests/test_main.py" << 'EOF'
import pytest
from fastapi.testclient import TestClient
from src.gamecraft_ai.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to GameCraft AI"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
EOF
    log_info "Created test file"
fi

# Create .gitignore
if [ ! -f ".gitignore" ]; then
    cat > ".gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/
*.egg-info/
dist/
build/

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/
.hypothesis/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
*.log

# UV
.python-version
EOF
    log_info "Created .gitignore"
fi

# Create pyproject.toml with proper configuration
if [ ! -f "pyproject.toml" ] || [ ! -s "pyproject.toml" ]; then
    cat > "pyproject.toml" << 'EOF'
[project]
name = "gamecraft-ai"
version = "0.1.0"
description = "AI-powered game development assistant"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.23.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"
select = ["E", "F", "I", "N", "W", "B", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --cov=src --cov-report=html --cov-report=term"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
]
EOF
    log_info "Created pyproject.toml"
fi

# Create Makefile for common tasks
if [ ! -f "Makefile" ]; then
    cat > "Makefile" << 'EOF'
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
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

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
EOF
    log_info "Created Makefile"
fi

# Create pre-commit configuration
if [ ! -f ".pre-commit-config.yaml" ]; then
    cat > ".pre-commit-config.yaml" << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]
EOF
    log_info "Created pre-commit configuration"
fi

# Install pre-commit hooks
log_info "Setting up pre-commit hooks..."
uv run pre-commit install || log_warn "Could not install pre-commit hooks"

# Create activation script
cat > "activate.sh" << 'EOF'
#!/usr/bin/env bash
source .venv/bin/activate
echo "Virtual environment activated. Run 'deactivate' to exit."
EOF
chmod +x activate.sh

# Sync dependencies from pyproject.toml
log_info "Syncing dependencies from pyproject.toml..."
uv pip install -e ".[dev]"

# Run initial tests
log_info "Running initial tests..."
uv run pytest tests/ -v || log_warn "Tests failed or no tests found"

# Final summary
echo ""
log_info "========================================="
log_info "Project initialization complete!"
log_info "========================================="
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo "     (or use: ./activate.sh)"
echo ""
echo "  2. Run the application:"
echo "     make run"
echo "     (or: uv run python -m src.gamecraft_ai.main)"
echo ""
echo "  3. Run tests:"
echo "     make test"
echo ""
echo "  4. Available make commands:"
echo "     make help"
echo ""
log_info "Happy coding with uv! 🚀"
EOF
