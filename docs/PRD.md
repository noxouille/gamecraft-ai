# Product Requirements Document (PRD)
## AI-Powered YouTube Video Summary & Script Generator

**Version:** 1.3
**Date:** August 2025
**Status:** Draft

---

## Executive Summary

A web application that helps YouTube gaming content creators through a streamlined 3-agent AI system:

**Core Agents:**
1. **Script Writer Agent**: Creates production-ready video scripts with timestamps for games/events
2. **Research Agent**: Finds official YouTube trailer links and gathers comprehensive game/event data
3. **YouTube Coach Agent**: Generates 3 viral thumbnail prompts for image generation services

**Key Features:**
- Supports both game reviews and event coverage
- Bilingual support (English/French) with automatic language detection
- User-selectable AI models (6 options including GPT-4o, Claude, etc.)
- 4-tab output: Script, Research Data, YouTube Links, Thumbnail Ideas
- Target duration: 5-20 minutes with proper script structuring

Users input natural language queries and receive everything needed for video production: professional scripts, research data, video footage links, and viral thumbnail strategies.

## Problem Statement

Content creators face different challenges based on content type:

### Event Coverage Challenges:
- Manually watching 2-3 hour streams to extract key announcements
- Time-intensive research to find official trailers for featured games
- Difficulty structuring content to fit specific video lengths
- Missing important announcements in long presentations

### Individual Game Content Challenges:
- Researching comprehensive information about a specific game
- Finding all relevant trailers (announcement, gameplay, launch)
- Gathering review scores and critical reception
- Compiling developer interviews and behind-the-scenes content
- Structuring reviews/previews with proper pacing
- Keeping up with updates, DLCs, and patches

## Goals & Success Metrics

### Primary Goals
1. Reduce content production time by 70% for both event coverage and game reviews
2. Ensure comprehensive information gathering from multiple sources
3. Generate engaging, properly-paced scripts for any target duration
4. Automate trailer and gameplay footage discovery
5. Provide seamless bilingual support with automatic language matching

### Success Metrics
- Script generation time: <5 minutes for any content type
- Information accuracy: >95% for game details
- Trailer match rate: >90% for requested games
- User script acceptance rate: >80% (minimal edits needed)
- Time saved per video: >6 hours
- Query language detection accuracy: >99%

## User Personas

### Primary: Gaming Content Creator
- **Channel Size:** 10K - 1M subscribers
- **Content Types:** Event summaries, game reviews, first impressions, retrospectives
- **Language**: English OR French speaking
- **Upload Frequency:** 3-10 videos per week
- **Pain Points:** Research time, information accuracy, content structuring
- **Needs:** Fast turnaround, comprehensive coverage, engaging scripts, multiple content formats

### Secondary: Gaming Media Journalist
- **Organization:** Gaming news websites, podcasts, YouTube channels
- **Content Types:** News coverage, reviews, previews, analysis pieces
- **Use Case:** Quick research, script preparation, fact-checking
- **Needs:** Accurate information, multiple sources, professional tone options

## Functional Requirements

### Core Features (MVP)

#### 1. Query Type Detection

**Query Classification**
- **Event Summary**: Contains event name + video URL
- **Game Content**: Contains game name without event context

**Query Examples**
```
Event Summary:
- EN: "Make a 15-min summary of Xbox Showcase [URL]"
- FR: "Fais un résumé de 15 minutes du Nintendo Direct [URL]"

Game Content:
- EN: "Make a 10-minute review video about Baldur's Gate 3"
- EN: "Create a 15-minute video about Starfield"
- FR: "Crée une vidéo de 20 minutes sur Hogwarts Legacy"
- FR: "Fais une critique de 10 minutes de Spider-Man 2"
```

#### 2. AI Agent System (Simplified)

**Script Writer Agent**
- Generates production-ready video scripts based on query type and requirements
- Adapts content structure to target duration (5-20 minutes)
- Supports multiple formats:
  - Game review scripts
  - Game preview/first impressions scripts
  - Event summary scripts
  - "Everything you need to know" comprehensive guides
- Automatically matches query language (English/French)
- Creates timestamped script sections for easy video editing

**Research Agent**
- Retrieves official YouTube trailer links for games mentioned in queries
- For events/conferences: Finds all announced game trailers from that event
- Gathers comprehensive research data about games/events:
  - Game information (developer, publisher, release date, platforms)
  - Review scores and critical reception
  - Key features and gameplay mechanics
  - Technical specifications and performance data
  - DLC and update information
- Provides structured research output for script enhancement

**YouTube Coach Agent**
- Analyzes query content and generated script
- Suggests 3 specific thumbnail generation prompts for image AI services
- Focuses on viral video strategies and high click-through rates
- Considers current YouTube trends and gaming content best practices
- Adapts suggestions based on content type (review, preview, event coverage)
- Includes design elements for maximum engagement (emotions, text, colors)

#### 3. Content Type Templates

**Review Script Structure (10-15 minutes)**
```
[00:00-00:30] Hook - What makes this game special/controversial
[00:30-02:00] Overview - Genre, developer, basic premise
[02:00-04:00] Gameplay Deep Dive
[04:00-05:30] Story & Characters (spoiler-free)
[05:30-07:00] Graphics & Performance
[07:00-08:30] Sound & Music
[08:30-10:00] Pros and Cons Summary
[10:00-11:00] Comparison to Similar Games
[11:00-12:00] Value Proposition
[12:00-13:00] Final Verdict & Score
[13:00-13:30] Outro & CTA
```

**Preview/First Impressions Structure (5-10 minutes)**
```
[00:00-00:30] Hook - First reactions
[00:30-02:00] What we know so far
[02:00-04:00] Gameplay footage analysis
[04:00-06:00] Developer promises vs. reality
[06:00-07:30] Concerns and expectations
[07:30-08:30] Release information
[08:30-09:00] Final thoughts
[09:00-09:30] Outro
```

**"Everything You Need to Know" Structure (15-20 minutes)**
```
[00:00-00:30] Hook
[00:30-03:00] Development history
[03:00-06:00] Gameplay mechanics explained
[06:00-08:00] Story setup (no spoilers)
[08:00-10:00] Game modes and content
[10:00-12:00] Editions and pricing
[12:00-14:00] Platform differences
[14:00-16:00] DLC and post-launch plans
[16:00-17:30] Critical reception
[17:30-18:30] Should you buy it?
[18:30-19:00] Outro
```

#### 4. Output Formats

**For Event Coverage (Existing)**
- Event summary document with timestamps
- Chronological script with trailer cues
- List of announced games with details
- Trailer URLs compilation

**For Game Content (New)**
```markdown
## [Game Name] Video Resources

### 📜 Generated Script
[Production-ready timestamped script based on query]

### 🔍 Research Data
- Developer: [Name]
- Publisher: [Name]
- Release Date: [Date]
- Platforms: [List]
- Genre: [Type]
- Critical Reception Summary
- Key Features & Talking Points

### 🎥 YouTube Links
#### Official Trailers
- Announcement Trailer: [URL]
- Gameplay Trailer: [URL]
- Launch Trailer: [URL]

#### Review Videos
- Major outlet reviews and gameplay videos

### 🖼️ Thumbnail Suggestions
#### Viral Thumbnail Concepts (3 AI-Ready Prompts)
1. [Specific prompt for image generation service]
2. [Specific prompt for image generation service]
3. [Specific prompt for image generation service]

#### Design Tips
- High-CTR strategies
- Color schemes and text guidelines
- Mobile optimization tips
```

#### 5. Language Support (Enhanced)

Same automatic language detection, with terminology adapted for both content types:

**Game Review Terms (English)**
- "gameplay loop", "quality of life", "replayability"
- "framerate", "resolution", "ray tracing"
- "skill ceiling", "learning curve", "meta"

**Game Review Terms (French)**
- "boucle de gameplay", "qualité de vie", "rejouabilité"
- "fréquence d'images", "résolution", "ray tracing"
- "plafond de compétence", "courbe d'apprentissage", "méta"

#### 6. LLM Configuration

**Model Selection by Agent**
```javascript
const modelConfig = {
  // Script Writing
  scriptWriter: "gpt-4o-mini", // Default, user-selectable

  // Research & Data Gathering
  researchAgent: "gpt-4o-mini", // Default, user-selectable

  // YouTube Coaching
  youtubeCoach: "gpt-4o-mini", // Default, user-selectable

  // Available Models
  availableModels: [
    "gpt-4o-mini",     // Fast, cost-effective (default)
    "gpt-4o",          // Most capable OpenAI
    "gpt-4-turbo",     // Advanced reasoning
    "gpt-3.5-turbo",   // Legacy fast model
    "claude-3-5-sonnet-20241022", // Anthropic's best
    "claude-3-haiku-20240307"     // Fast Anthropic
  ]
};
```

#### 7. Authentication & Access Control
- Simple access code system
- Session management (24-hour validity)
- Usage quotas for different query types
- Rate limiting per user

## Technical Requirements

### Simplified Architecture

```
Input Layer:
├── Query Type Classifier
├── Language Detector
└── Parameter Extractor (game names, URLs, duration)

Agent Processing Layer:
├── Script Writer Agent
│   ├── Template Selector
│   ├── Content Structuring
│   ├── Language Optimizer
│   └── Script Formatter
├── Research Agent
│   ├── YouTube Search API
│   ├── Game Information API (IGDB, Steam)
│   ├── Review Aggregator
│   └── Event Analysis (for conferences)
└── YouTube Coach Agent
    ├── Thumbnail Strategy Analyzer
    ├── Trend Analysis
    └── Prompt Generator

Output Layer:
├── Script Generator
├── Research Data Formatter
├── YouTube Links Compiler
└── Thumbnail Suggestions Formatter
```

### External Dependencies
- YouTube Data API v3
- Steam Web API (for game info)
- IGDB API (game database)
- Metacritic/OpenCritic APIs or scrapers
- OpenAI/Anthropic APIs
- Whisper API (for video transcription)
- Redis for caching
- PostgreSQL for data storage

### Performance Requirements
- Query classification: <500ms
- Script Writer Agent: <30 seconds
- Research Agent: <20 seconds (info gathering + YouTube search)
- YouTube Coach Agent: <10 seconds (thumbnail suggestions)
- Total processing: <60 seconds for all agents
- Concurrent requests: 10

## User Flow

### Flow A: Event Summary (Existing)
```
1. User: "Make a 15-min summary of Nintendo Direct [URL]"
2. System analyzes video and extracts games
3. System finds trailers
4. System generates script
5. User receives summary + script + trailer links
```

### Flow B: Game Content (New)
```
1. User: "Make a 10-minute review video about Baldur's Gate 3"
2. System classifies query and extracts parameters
3. Script Writer Agent: Generates timestamped video script
4. Research Agent: Gathers game info + finds YouTube trailer links
5. YouTube Coach Agent: Creates 3 viral thumbnail prompts
6. User receives:
   - Production-ready script with timestamps
   - Comprehensive research data
   - Official trailer and gameplay video links
   - 3 AI-ready thumbnail generation prompts
   - Design tips for viral success
```

## Data Schema

```sql
-- Enhanced Analysis Jobs
CREATE TABLE analysis_jobs (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  query_text TEXT,
  query_type VARCHAR(20), -- 'event' or 'game'
  query_language VARCHAR(2),
  target_game VARCHAR(255), -- For game queries
  source_url TEXT, -- For event queries
  target_duration INTEGER,
  script_format VARCHAR(50), -- 'review', 'preview', 'summary', etc.
  status VARCHAR(50),
  created_at TIMESTAMP
);

-- Game Information Cache
CREATE TABLE game_info_cache (
  id UUID PRIMARY KEY,
  game_name VARCHAR(255) UNIQUE,
  developer VARCHAR(255),
  publisher VARCHAR(255),
  release_date DATE,
  platforms TEXT[],
  genre VARCHAR(100),
  price DECIMAL(10,2),
  metacritic_score INTEGER,
  opencritic_score INTEGER,
  steam_rating DECIMAL(3,2),
  last_updated TIMESTAMP
);

-- Media Assets
CREATE TABLE media_assets (
  id UUID PRIMARY KEY,
  game_name VARCHAR(255),
  asset_type VARCHAR(50), -- 'trailer', 'gameplay', 'interview'
  title VARCHAR(255),
  youtube_url TEXT,
  duration_seconds INTEGER,
  upload_date DATE,
  channel_name VARCHAR(255),
  language VARCHAR(2),
  quality_options TEXT[]
);

-- Review Scores Cache
CREATE TABLE review_scores (
  id UUID PRIMARY KEY,
  game_name VARCHAR(255),
  outlet_name VARCHAR(100),
  score VARCHAR(20), -- Can be "9/10", "90/100", "Amazing"
  review_url TEXT,
  review_date DATE,
  key_points TEXT[]
);
```

## MVP Scope

### In Scope
- **Script Writer Agent**: Production-ready video scripts for games/events
- **Research Agent**: Game information + official YouTube trailer links
- **YouTube Coach Agent**: 3 AI-ready thumbnail generation prompts per query
- Event summary from video URLs
- Individual game video script generation
- English and French support
- 5, 10, 15, 20-minute script options
- Multiple script templates (review, preview, summary)
- Model selection (6 available AI models)
- Simple authentication

### Out of Scope (MVP)
- Video editing features
- Automatic thumbnail generation
- Voice-over generation
- Direct upload to YouTube
- Real-time streaming analysis
- Community features
- Mobile app
- Browser extension
- More than 2 languages

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|---------|------------|
| API rate limits | High | Implement caching, use multiple API keys |
| Outdated game information | Medium | Cache with TTL, daily updates for popular games |
| Review score accuracy | Medium | Cross-reference multiple sources |
| Script quality variance | Medium | Multiple templates, user feedback loop |
| Game name ambiguity | Low | Fuzzy matching, user confirmation step |

## Success Criteria

1. **Query Classification**: 98% accuracy in detecting event vs. game queries
2. **Information Accuracy**: 95% accuracy for game details
3. **Media Discovery**: 90% of relevant trailers found
4. **Script Quality**: <10% editing needed before use
5. **Processing Speed**: <1 minute for game content, <5 minutes for events
6. **User Satisfaction**: 4.5/5 average rating

## Timeline

**MVP Development (8 weeks)**
- Week 1-2: Query classification & routing system + UI foundation
- Week 3-4: Script Writer Agent implementation
- Week 5: Research Agent (game info + YouTube trailer search)
- Week 6: YouTube Coach Agent (viral thumbnail prompts)
- Week 7: Agent integration and model selection
- Week 8: Testing, optimization, and language support

## Appendix

### Sample Queries

**Event Coverage:**
```
EN: "Make a 20-minute summary of E3 2025 showcase [URL]"
FR: "Crée un résumé de 15 minutes du PlayStation State of Play [URL]"
```

**Game Reviews:**
```
EN: "Create a 10-minute review of Elden Ring"
EN: "Make a video about Cyberpunk 2077 Phantom Liberty"
FR: "Fais une critique de 15 minutes de Zelda Tears of the Kingdom"
FR: "Crée une vidéo de 10 minutes sur Diablo 4"
```

**Game Previews:**
```
EN: "Make a preview video about GTA 6"
EN: "Create everything you need to know about Hollow Knight Silksong"
FR: "Fais un aperçu de Dragon Age Dreadwolf"
```

### Cost Estimates
- Event video analysis: ~$0.50
- Game information gathering: ~$0.30
- Media discovery: ~$0.20
- Review aggregation: ~$0.20
- Script generation: ~$0.30
- **Total per request**: ~$0.50-$1.50 depending on query type

---

**Next Steps:**
1. ✅ Implement query type classification (COMPLETED)
2. ✅ UI with model selection (COMPLETED)
3. Implement Script Writer Agent with multiple templates
4. Implement Research Agent with YouTube API integration
5. Implement YouTube Coach Agent for thumbnail suggestions
6. Test complete 3-agent workflow with various queries
