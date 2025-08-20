# Product Requirements Document (PRD)
## AI-Powered YouTube Video Summary & Script Generator

**Version:** 1.3
**Date:** August 2025
**Status:** Draft

---

## Executive Summary

A web application that helps YouTube gaming content creators by providing two core functionalities:
1. **Event Coverage**: Transform long-form gaming events (showcases, conferences) into structured summaries and production-ready scripts
2. **Game Reviews/Videos**: Generate comprehensive video scripts about individual games with trailer compilation and key information gathering

The platform supports both English and French languages, with output automatically matching the query language. Users provide either an event video URL or a game name with desired output length, and receive summaries, trailer links, and production-ready scripts through AI-powered analysis.

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

#### 2. Dual-Mode AI Agent System

##### Mode A: Event Analysis (Existing)
- **Video Analyzer Agent**: Extracts announcements from event video
- **Trailer Finder Agent**: Finds trailers for announced games
- **Script Writer Agent**: Creates event summary script

##### Mode B: Game Research (New)
**Game Information Agent**
- Searches for comprehensive game information:
  - Release date, platforms, developer, publisher
  - Genre, gameplay mechanics, key features
  - Story synopsis (spoiler-free option)
  - Technical specifications
  - DLC and update information
  - Price information

**Media Collector Agent**
- Finds all related media:
  - Announcement trailer
  - Gameplay trailers
  - Launch trailer
  - Developer interviews
  - Behind-the-scenes content
  - Review/preview videos from major outlets

**Review Aggregator Agent**
- Collects critical reception:
  - Metacritic scores
  - OpenCritic scores
  - Major outlet review scores
  - User ratings
  - Common praise points
  - Common criticisms
  - Technical performance reports

**Script Writer Agent (Enhanced)**
- Generates scripts based on content type:
  - Review format
  - Preview/first impressions format
  - Retrospective format
  - News/announcement format
  - "Everything you need to know" format

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

### Game Information
- Developer: [Name]
- Publisher: [Name]
- Release Date: [Date]
- Platforms: [List]
- Genre: [Type]
- Price: [Amount]

### Media Assets
1. Announcement Trailer: [URL] (Length: X:XX)
2. Gameplay Trailer: [URL] (Length: X:XX)
3. Launch Trailer: [URL] (Length: X:XX)
4. Developer Interview: [URL] (Length: X:XX)

### Critical Reception
- Metacritic: XX/100 (PC), XX/100 (PS5), XX/100 (Xbox)
- OpenCritic: XX/100 - "Mighty"
- IGN: X/10 - "Amazing"
- GameSpot: X/10
- User Score: X.X/10

### Key Talking Points
- Strengths: [List]
- Weaknesses: [List]
- Unique Features: [List]
- Technical Performance: [Summary]

### Generated Script
[Full script based on selected template]
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

**Model Selection by Task**
```javascript
const modelConfig = {
  // Event Coverage
  eventAnalyzer: "gpt-4",

  // Game Research
  infoGatherer: "gpt-4",
  mediaCollector: "gpt-3.5-turbo",
  reviewAggregator: "claude-3",

  // Script Writing (both modes)
  scriptWriter: "claude-3",

  // Language-specific
  frenchOptimizer: "gpt-4"
};
```

#### 7. Authentication & Access Control
- Simple access code system
- Session management (24-hour validity)
- Usage quotas for different query types
- Rate limiting per user

## Technical Requirements

### Enhanced Architecture

```
Input Layer:
├── Query Type Classifier
├── Language Detector
├── Event URL Parser (Mode A)
└── Game Name Extractor (Mode B)

Mode A: Event Processing
├── Video Transcript Extractor
├── Event Analyzer
├── Announcement Detector
└── Trailer Finder

Mode B: Game Research
├── Game Information API
├── Media Search Engine
├── Review Aggregator API
├── YouTube Search API
├── Steam API Integration
├── Metacritic Scraper
└── Gaming News RSS Feeds

Script Generation Layer:
├── Template Selector
├── Content Structuring
├── Language Optimizer
└── Script Formatter

Output Layer:
├── Summary Generator
├── Asset Compiler
└── Export Formatter
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
- Game information gathering: <10 seconds
- Media discovery: <15 seconds
- Review aggregation: <10 seconds
- Script generation: <30 seconds
- Total processing: <60 seconds for game content
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
2. System identifies query type (game review)
3. System gathers game information from multiple sources
4. System finds all relevant media (trailers, gameplay)
5. System aggregates review scores and opinions
6. System generates review script with selected template
7. User receives:
   - Complete game information
   - All media links with timestamps
   - Review scores summary
   - Production-ready script
   - B-roll suggestions
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
- Event summary from video URLs
- Individual game video script generation
- Game information aggregation
- Media asset discovery
- Review score compilation
- English and French support
- 5, 10, 15, 20-minute script options
- Multiple script templates (review, preview, summary)
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
- Week 1-2: Query classification & routing system
- Week 3-4: Game information aggregation APIs
- Week 5: Media discovery and review aggregation
- Week 6: Script template system
- Week 7: Integration and language support
- Week 8: Testing and optimization

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
1. Implement query type classification
2. Integrate game information APIs (IGDB, Steam)
3. Build review aggregation system
4. Create script template library
5. Test with various game titles and events
