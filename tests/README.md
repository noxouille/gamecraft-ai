# GameCraft AI Tests

This directory contains all test files for the GameCraft AI project.

## Test Files

- **`test_main.py`**: Tests for the main application entry point and Gradio interface
- **`test_classifier_agent.py`**: Comprehensive tests for the ClassifierAgent functionality

## Running Tests

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Specific Test File
```bash
uv run pytest tests/test_classifier_agent.py -v
uv run pytest tests/test_main.py -v
```

### Run Tests with Coverage
```bash
uv run pytest tests/ -v --cov=src --cov-report=html
```

## Test Coverage

Current test coverage focuses on:
- ✅ **ClassifierAgent (100% coverage)**: Language detection, query type classification, format detection, game name extraction, URL extraction
- ✅ **Main application (100% coverage)**: Entry point functions and error handling
- 📊 **Overall project coverage**: 36% (focused on core functionality)

## Test Structure

### ClassifierAgent Tests (`test_classifier_agent.py`)

- **Query Classification**: Tests for GAME vs EVENT detection
- **Language Detection**: English/French detection with edge cases
- **Format Detection**: Review, preview, summary, complete_guide formats
- **Game Name Extraction**: Pattern matching for various game name formats
- **URL Extraction**: YouTube URL detection for event queries
- **State Preservation**: Ensures proper state management through processing

### Main Application Tests (`test_main.py`)

- **Function Import**: Verifies main functions can be imported
- **CLI Argument Parsing**: Tests command-line interface with various options
- **Gradio App Lifecycle**: Tests app startup and error handling
- **Configuration**: Tests settings management

## Notes

- Tests use the real LLM service (no mocking) to ensure authentic behavior
- All tests are designed to be deterministic and repeatable
- Coverage report is generated in `htmlcov/index.html` when running with coverage
