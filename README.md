# 🎮 GameCraft AI

**AI-powered YouTube video summary and script generator for gaming content creators**

Generate professional gaming content scripts from simple queries in English or French. Built with LangGraph, Gradio, and Pydantic for a minimal but powerful architecture.

## ✨ Features

- **🎯 Dual Mode**: Event summaries or game reviews
- **🌍 Bilingual**: English and French support with automatic language detection
- **🔍 Smart Research**: Automatic game info, media, and review aggregation
- **📝 Multiple Formats**: Review, preview, complete guide templates
- **⚡ Fast Processing**: Results in under 60 seconds
- **🎨 Modern UI**: Clean Gradio interface with real-time progress

## 🏗️ Architecture

**Minimal Agent Design (4 agents total):**
- **Classifier Agent**: Query type and language detection
- **Game Researcher Agent**: Combined game info + media + reviews
- **Event Analyzer Agent**: Video analysis for gaming events
- **Script Writer Agent**: Multi-format script generation

**Tech Stack:**
- **LangGraph**: Multi-agent orchestration
- **Gradio**: Web UI
- **Pydantic**: Data validation and modeling
- **httpx**: HTTP client for external APIs

## 🚀 Quick Start

### 1. Project Setup

```bash
# Clone and setup
git clone <your-repo>
cd gamecraft-ai

# Install dependencies with uv
uv sync
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys:
# - OPENAI_API_KEY (required)
# - YOUTUBE_API_KEY (required)
# - IGDB_CLIENT_ID & IGDB_ACCESS_TOKEN (required)
# - ANTHROPIC_API_KEY (optional)
```

### 3. Run the Application

**Method 1: Direct uv command (Recommended)**
```bash
# Default start (port 8000)
uv run python -m src.gamecraft_ai.main

# Custom port and debug mode
uv run python -m src.gamecraft_ai.main --port 7860 --debug
```

**Method 2: Convenient launcher**
```bash
# Simple start
./gamecraft

# With options
./gamecraft --port 7860 --debug
```

**Method 3: Legacy python script**
```bash
python run.py  # Uses uv internally
```

**Method 4: Using Make**
```bash
make run  # Uses uv internally
```

### 4. Test the System

Open your browser to `http://localhost:8000` and try:

**Game Review Example:**
```
Make a 10-minute review video about Baldur's Gate 3
```

**Event Summary Example:**
```
Make a 15-minute summary of Xbox Showcase [YouTube URL]
```

**French Example:**
```
Fais une critique de 10 minutes de Spider-Man 2
```

## 📁 Project Structure

```
src/gamecraft_ai/
├── models/           # Pydantic data models
│   ├── query.py     # Input validation
│   ├── content.py   # Game/event data structures
│   └── output.py    # Script output format
├── agents/          # LangGraph agent nodes
│   ├── classifier.py    # Query classification
│   ├── game_researcher.py  # Combined game research
│   ├── event_analyzer.py   # Event video analysis
│   └── script_writer.py    # Script generation
├── services/        # External API clients
│   ├── youtube.py   # YouTube Data API
│   ├── igdb.py     # Game database
│   └── llm.py      # OpenAI/Anthropic
├── graph/           # LangGraph workflow
│   ├── state.py    # State management
│   ├── nodes.py    # Node implementations
│   └── workflow.py # Workflow orchestration
├── ui/              # Gradio interface
│   ├── app.py      # UI components
│   └── handlers.py # Event handling
├── utils/           # Shared utilities
│   ├── cache.py    # Caching (memory/Redis)
│   ├── helpers.py  # Common functions
│   └── logging.py  # Logging setup
├── config.py        # Settings management
└── main.py         # Application entry point
```

## 🔧 Configuration

**Key Environment Variables:**

```bash
# Required API Keys
OPENAI_API_KEY=sk-...           # OpenAI for LLM processing
YOUTUBE_API_KEY=AIza...         # YouTube Data API v3
IGDB_CLIENT_ID=...              # IGDB game database
IGDB_ACCESS_TOKEN=...           # IGDB access token

# Optional
ANTHROPIC_API_KEY=sk-ant-...    # Alternative LLM
REDIS_URL=redis://localhost:6379/0  # Cache (uses memory if not set)

# App Settings
DEBUG=false
HOST=0.0.0.0
PORT=7860
LOG_LEVEL=INFO
```

## 🎯 Usage Examples

### Query Types

**Game Review/Content:**
- "Make a 10-minute review video about [Game Name]"
- "Create a 15-minute preview of [Game Name]"
- "Everything you need to know about [Game Name]"

**Event Summaries:**
- "Make a 20-minute summary of [Event Name] [YouTube URL]"
- "Summarize the Nintendo Direct [YouTube URL]"

**French Support:**
- "Fais une critique de 15 minutes de [Nom du Jeu]"
- "Crée un résumé de 10 minutes du [Event] [URL]"

### Generated Output

Each query produces:
- **📜 Script**: Timestamped, production-ready script
- **ℹ️ Metadata**: Processing info, language, timing
- **🔍 Research Data**: Game info, media assets, review scores

## 🛠️ Development

### Dependencies Management

```bash
# Install all dependencies (including dev)
uv sync

# Install production only
uv sync --no-dev

# Add new dependencies
uv add package-name

# Add development dependencies
uv add --dev package-name

# Update dependencies
uv sync --upgrade
```

### Code Quality

```bash
make lint      # Run ruff linting
make format    # Auto-format code
make type-check # Run mypy
make test      # Run test suite
```

### Testing

```bash
# Run all tests
make test

# Run specific test
uv run pytest tests/test_classifier.py -v

# Test with coverage
uv run pytest --cov=src --cov-report=html
```

## 🔄 LangGraph Workflow

Simple linear flow with conditional routing:

```
START → Classifier → [Game Research | Event Analysis] → Script Writer → END
```

**State Management:**
- Pydantic models ensure type safety
- All data flows through unified state
- Error handling at each node
- Caching for performance

## 🚨 Troubleshooting

**Common Issues:**

1. **Missing API Keys**
   ```bash
   # Check environment
   python -c "from src.gamecraft_ai.config import settings; print(settings.openai_api_key)"
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   make clean && make dev
   ```

3. **Port Already in Use**
   ```bash
   python run.py --port 8080
   ```

4. **Memory Issues**
   ```bash
   # Enable Redis caching
   export REDIS_URL=redis://localhost:6379/0
   ```

## 📈 Performance

**Target Metrics (MVP):**
- Query classification: <500ms
- Game content generation: <60 seconds
- Event processing: <5 minutes
- Information accuracy: >95%
- Concurrent users: 10

## 🤝 Contributing

1. Follow the modular structure
2. Use Pydantic for all data models
3. Add type hints everywhere
4. Write tests for new features
5. Run `make lint` before committing

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for gaming content creators**
