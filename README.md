# GameCraft AI

AI-Powered YouTube Video Summary & Script Generator

## Quick Start

### Prerequisites

- Linux/macOS/WSL environment
- Bash shell
- Internet connection (for package downloads)

### Project Initialization

1. **Run the initialization script:**
   ```bash
   ./init_project.sh
   ```

   This script will automatically:
   - Install `uv` package manager if not present
   - Create a Python 3.12 virtual environment
   - Install all required dependencies
   - Set up the project structure
   - Configure development tools (linting, testing, pre-commit)
   - Run initial tests to verify setup

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
   Or use the convenience script:
   ```bash
   ./activate.sh
   ```

3. **Run the application:**
   ```bash
   make run
   ```
   Or directly with uv:
   ```bash
   uv run python -m src.gamecraft_ai.main
   ```

   The API will be available at `http://localhost:8000`

### Available Commands

After initialization, you can use these make commands:

- `make install` - Install production dependencies
- `make dev` - Install all dependencies including development tools
- `make test` - Run tests with coverage
- `make lint` - Run code linting
- `make format` - Auto-format code
- `make type-check` - Run type checking
- `make run` - Start the application
- `make clean` - Clean generated files
- `make help` - Show all available commands

### Project Structure

```
gamecraft-ai/
├── src/
│   └── gamecraft_ai/
│       ├── __init__.py
│       ├── main.py         # FastAPI application
│       └── config.py       # Configuration management
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Test suite
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── .venv/                  # Virtual environment (created by init)
├── pyproject.toml          # Project configuration
├── Makefile                # Common tasks
├── .gitignore             # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
└── init_project.sh        # Initialization script
```

### Troubleshooting

If the initialization script fails:

1. **uv installation issues:** Install manually from https://github.com/astral-sh/uv
2. **Permission denied:** Run `chmod +x init_project.sh`
3. **Python version issues:** The script uses Python 3.12 by default. Modify the `PYTHON_VERSION` variable in the script if needed.

### Fresh Environment Setup

The `init_project.sh` script is designed to be portable. To set up in a fresh environment:

1. Clone/copy the repository
2. Run `./init_project.sh`
3. Everything will be configured automatically

The script is idempotent - you can run it multiple times safely without breaking existing setup.
