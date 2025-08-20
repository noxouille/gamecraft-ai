# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GameCraft AI is an AI-powered YouTube video summary and script generator for gaming content creators. It provides two core functionalities:
1. **Event Coverage**: Transforms gaming events/showcases into summaries and scripts
2. **Game Reviews/Videos**: Generates comprehensive video scripts about individual games

The application supports English and French with automatic language detection and aims to reduce content production time by 70%.

## Development Commands

### Environment Setup
```bash
# Initialize project (first time)
./init_project.sh

# Activate virtual environment
source .venv/bin/activate
# OR
./activate.sh
```

### Core Development Commands
```bash
# Run the application
make run
# OR
uv run python -m src.gamecraft_ai.main

# Run tests with coverage
make test
# OR
uv run pytest

# Run single test file
uv run pytest tests/test_main.py -v

# Linting and formatting
make lint       # Check code style
make format     # Auto-format code
make type-check # Run type checking

# Install dependencies
make install    # Production only
make dev        # All including dev tools
```

### Pre-commit hooks
```bash
# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

## Architecture Overview

### Agent-Based System Design
The project uses a dual-mode AI agent system with specialized agents for different tasks:

**Mode A: Event Analysis**
- Video Analyzer Agent: Extracts announcements from event videos
- Trailer Finder Agent: Locates trailers for announced games
- Script Writer Agent: Creates event summary scripts

**Mode B: Game Research**
- Game Information Agent: Gathers comprehensive game data
- Media Collector Agent: Finds all related media (trailers, gameplay)
- Review Aggregator Agent: Collects critical reception data
- Script Writer Agent (Enhanced): Generates scripts based on content type

### Project Structure
```
src/gamecraft_ai/
├── agents/          # AI agent implementations
├── services/        # Business logic (query classification, etc.)
├── clients/         # External API clients
├── models/          # Database models
├── config.py        # Configuration management
└── main.py          # FastAPI application
```

### Agent Handoff Context
Critical file: `docs/agent_handoff_context.md`
- Must be consulted by every agent before starting work
- Must be updated by every agent after completing work
- Contains current project phase, completed work, blockers, and next steps

## Key Technical Requirements

### Performance Targets
- Query classification: <500ms
- Query language detection accuracy: >99%
- Total processing: <60s (game content), <5 min (events)
- Concurrent requests: 10 users
- Script generation time: <5 minutes

### External APIs to Integrate
- YouTube Data API v3 (video analysis, media discovery)
- Steam Web API (game information)
- IGDB API (comprehensive game database)
- OpenAI/Anthropic APIs (LLM processing)
- Whisper API (video transcription)
- Metacritic/OpenCritic (review scores)

### Database & Infrastructure
- PostgreSQL for data storage
- Redis for caching
- FastAPI framework
- Python 3.12+

## Current Development Phase

**Phase:** Foundation Setup (Week 1-2 of 8-week timeline)
**Focus:** Query classification and routing system

### Immediate Priorities
1. Implement query type detection (event vs. game)
2. Build language detection (English/French)
3. Create modular agent architecture
4. Set up API client framework
5. Design database schema

## Testing Strategy

### Test Coverage Requirements
- Unit tests: >90% coverage required
- Performance benchmarks for classification speed
- Integration tests for API clients

### Running Tests
```bash
# Run all tests with coverage
make test

# Run specific test file
uv run pytest tests/test_main.py -v

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
```

## Important Files

- `docs/PRD.md`: Complete Product Requirements Document
- `docs/agent_handoff_context.md`: Inter-agent communication and project tracking
- `pyproject.toml`: Project dependencies and tool configuration
- `Makefile`: Common development tasks
- For this project I want the @agent-product-launch-strategist to be the go-to person to initiate and continue the development by suggesting which agent should do the work and delegate the task. If the required agent does not exist, provide the description of the agent and I will create it manually. There needs to be a single file to handoff context between agents in the @docs/ directory, which is @docs/agent_handoff_context.md . Everytime an agent starts to do the work, they need to consult all the context files, and everytime an agent finishes their work, @docs/agent_handoff_context.md MUST BE UPDATED.
