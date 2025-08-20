"""
YouTube Coach Agent - generates viral thumbnail prompts and strategies
"""
from typing import Any

from ..models import ScriptOutput, ThumbnailSuggestion
from ..services.llm import LLMService


class YouTubeCoachAgent:
    """Generates viral thumbnail prompts and YouTube optimization strategies"""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def generate_thumbnail_strategies(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate thumbnail prompts and viral strategies based on script and research"""
        try:
            script = state.get("script")
            research_type = state.get("research_type", "game")
            language = (
                state.get("query", {}).get("language", "en")
                if hasattr(state.get("query", {}), "get")
                else "en"
            )

            if not script:
                state["errors"].append("No script available for thumbnail generation")
                return state

            # Generate context-aware thumbnails
            if research_type == "game":
                thumbnails = self._generate_game_thumbnails(state, language)
            elif research_type == "event":
                thumbnails = self._generate_event_thumbnails(state, language)
            else:
                thumbnails = self._generate_default_thumbnails(script, language)

            # Add YouTube optimization tips
            optimization_tips = self._get_optimization_tips(research_type, language)

            state["thumbnail_suggestions"] = thumbnails
            state["youtube_tips"] = optimization_tips

            return state

        except Exception as e:
            state["errors"].append(f"Thumbnail generation failed: {str(e)}")
            return state

    def _generate_game_thumbnails(
        self, state: dict[str, Any], language: str
    ) -> list[ThumbnailSuggestion]:
        """Generate thumbnail suggestions for game content"""
        script = state.get("script")
        game_info = state.get("game_info")

        # Get script format from script object or metadata
        script_format = "review"
        if script and hasattr(script, "format_type"):
            script_format = script.format_type
        elif script and isinstance(script, dict):
            script_format = script.get("format_type", "review")
        else:
            script_format = state.get("query_metadata", {}).get("script_format", "review")

        # Extract game details
        if isinstance(game_info, list) and game_info:
            game_info = game_info[0]

        game_name = self._extract_value(game_info, "name", "Game")
        genre = self._extract_value(game_info, "genre", "Gaming")

        thumbnails = []

        # Thumbnail 1: Emotional Reaction Style
        emotion = "SHOCKED" if script_format == "review" else "HYPED"
        color_scheme = (
            "vibrant red and yellow" if script_format == "review" else "electric blue and purple"
        )

        thumbnails.append(
            ThumbnailSuggestion(
                style="Emotional Reaction",
                prompt=f"YouTube thumbnail: Person with {emotion.lower()} facial expression, mouth open, pointing at {game_name} logo. {color_scheme} gradient background. Bold white text '{game_name}' at top, 'THIS IS INSANE!' at bottom. High contrast, dramatic lighting. Ultra-realistic, 4K quality.",
                description=f"High-impact emotional thumbnail perfect for {script_format} content",
                target_ctr="8-12%",
                design_notes=[
                    f"Use {emotion.lower()} facial expression for maximum engagement",
                    f"Bold {color_scheme} colors stand out in YouTube feed",
                    "Large text readable on mobile devices",
                    "Pointing gesture creates clear focus direction",
                ],
            )
        )

        # Thumbnail 2: Game Visual Focus
        visual_element = (
            "epic boss battle" if genre.lower() in ["action", "rpg"] else "stunning landscape"
        )
        thumbnails.append(
            ThumbnailSuggestion(
                style="Game Visual Showcase",
                prompt=f"YouTube thumbnail: Split screen showing {visual_element} from {game_name} on left, excited gamer face on right. Neon green arrow pointing from person to game. Text: '{game_name}' (large, white with black outline), 'INCREDIBLE' (smaller, bright yellow). Dark background with subtle game-themed effects.",
                description="Showcases actual game visuals while maintaining personality",
                target_ctr="6-10%",
                design_notes=[
                    "Split-screen layout balances game content and personality",
                    "Neon arrows guide viewer attention flow",
                    "Dark background makes colors pop",
                    "Game screenshots build credibility",
                ],
            )
        )

        # Thumbnail 3: Question/Curiosity Hook
        hook_text = "WORTH IT?" if script_format == "review" else "THE HYPE REAL?"
        thumbnails.append(
            ThumbnailSuggestion(
                style="Curiosity Hook",
                prompt=f"YouTube thumbnail: {game_name} logo prominently displayed with question mark overlay. Thoughtful person chin-in-hand pose. Background: blurred game screenshots montage. Large yellow text '{hook_text}' with question mark. Blue and orange color scheme for high contrast.",
                description="Curiosity-driven thumbnail that encourages clicks",
                target_ctr="7-11%",
                design_notes=[
                    "Question format creates curiosity gap",
                    "Thoughtful pose suggests analytical content",
                    "Color contrast (blue/orange) maximizes visibility",
                    "Question mark symbol reinforces hook",
                ],
            )
        )

        return thumbnails

    def _generate_event_thumbnails(
        self, state: dict[str, Any], language: str
    ) -> list[ThumbnailSuggestion]:
        """Generate thumbnail suggestions for event content"""
        event_info = state.get("event_info")

        event_title = self._extract_value(event_info, "title", "Gaming Event")
        announced_games = event_info.get("announced_games", []) if event_info else []

        thumbnails = []

        # Thumbnail 1: Event Reaction Style
        thumbnails.append(
            ThumbnailSuggestion(
                style="Event Reaction",
                prompt=f"YouTube thumbnail: Person with shocked/excited expression, hands on head. Background: {event_title} logo with multiple game logos arranged around it. Red arrow pointing to biggest game announcement. White text '{event_title}' at top, 'MIND BLOWN!' at bottom. Explosive effect with bright colors (red, yellow, white).",
                description="High-energy reaction thumbnail for event coverage",
                target_ctr="9-13%",
                design_notes=[
                    "Shocked expression communicates exciting content",
                    "Multiple game logos show comprehensive coverage",
                    "Explosive effects match event excitement",
                    "Arrow highlights biggest announcement",
                ],
            )
        )

        # Thumbnail 2: Game Lineup Showcase
        game_count = len(announced_games)
        thumbnails.append(
            ThumbnailSuggestion(
                style="Game Lineup",
                prompt=f"YouTube thumbnail: Grid layout showing 4-6 major game logos from {event_title}. Center text: '{game_count} HUGE GAMES!' in bold white with red background. Bottom banner: 'EVERYTHING ANNOUNCED' in yellow. Dark background with subtle gaming pattern. Clean, organized layout.",
                description="Information-rich thumbnail showing content value",
                target_ctr="6-9%",
                design_notes=[
                    "Grid layout shows comprehensive coverage",
                    "Number emphasizes value proposition",
                    "Clean organization builds trust",
                    "Dark background prevents visual clutter",
                ],
            )
        )

        # Thumbnail 3: Before/After Hype Style
        thumbnails.append(
            ThumbnailSuggestion(
                style="Hype Meter",
                prompt=f"YouTube thumbnail: Split screen - left side shows calm person 'BEFORE {event_title}', right side shows same person extremely excited 'AFTER'. Progress bar at bottom filled to 100% labeled 'HYPE METER'. Bright green and red colors. Large text: 'THIS CHANGED EVERYTHING!'",
                description="Before/after concept showing transformative content",
                target_ctr="8-12%",
                design_notes=[
                    "Before/after creates story narrative",
                    "Progress bar visualizes impact",
                    "Transformation angle implies valuable content",
                    "Bright colors ensure visibility",
                ],
            )
        )

        return thumbnails

    def _generate_default_thumbnails(
        self, script: ScriptOutput, language: str
    ) -> list[ThumbnailSuggestion]:
        """Generate basic thumbnail suggestions as fallback"""
        title = script.title if hasattr(script, "title") else "Gaming Content"

        return [
            ThumbnailSuggestion(
                style="Bold Text",
                prompt=f"YouTube thumbnail: Large bold text '{title}' on bright gradient background. Excited person pointing at text. High contrast colors.",
                description="Simple, effective text-focused thumbnail",
                target_ctr="5-8%",
                design_notes=[
                    "Bold text ensures readability",
                    "High contrast maximizes visibility",
                ],
            ),
            ThumbnailSuggestion(
                style="Question Hook",
                prompt="YouTube thumbnail: Person with curious expression, question mark overlay, text 'WORTH WATCHING?' in large font.",
                description="Curiosity-driven engagement thumbnail",
                target_ctr="6-9%",
                design_notes=["Question format creates curiosity", "Clear emotional expression"],
            ),
            ThumbnailSuggestion(
                style="Reaction",
                prompt="YouTube thumbnail: Shocked facial expression, bright background, text 'UNBELIEVABLE!' in bold letters.",
                description="Emotional reaction thumbnail",
                target_ctr="7-10%",
                design_notes=[
                    "Strong emotion drives engagement",
                    "Bold text complements expression",
                ],
            ),
        ]

    def _get_optimization_tips(self, research_type: str, language: str) -> dict[str, list[str]]:
        """Get YouTube optimization tips based on content type"""
        base_tips = {
            "mobile_optimization": [
                "Text size must be readable on mobile screens (minimum 30pt font)",
                "Use high contrast colors (white text on dark background)",
                "Avoid small details that disappear at thumbnail size",
                "Keep important elements in center 80% of image",
            ],
            "color_psychology": [
                "Red/Orange: Creates urgency and excitement",
                "Blue/Purple: Suggests professionalism and trust",
                "Yellow/Green: Indicates positivity and success",
                "High contrast combinations perform best (blue/orange, red/white)",
            ],
            "facial_expressions": [
                "Shocked/surprised expressions increase CTR by 8-15%",
                "Pointing gestures direct attention and improve engagement",
                "Direct eye contact with camera builds connection",
                "Exaggerated emotions perform better than subtle ones",
            ],
        }

        if research_type == "game":
            base_tips["game_specific"] = [
                "Include recognizable game elements (logos, characters, UI)",
                "Use genre-appropriate color schemes (dark for horror, bright for adventure)",
                "Show gameplay screenshots for credibility",
                "Add rating/score elements for review content",
            ]
        elif research_type == "event":
            base_tips["event_specific"] = [
                "Show multiple game logos for comprehensive feel",
                "Use event branding colors when possible",
                "Include game count numbers for value proposition",
                "Highlight biggest announcements with arrows/emphasis",
            ]

        return base_tips

    def _extract_value(self, obj, attr: str, default: str) -> str:
        """Safely extract value from object or dict"""
        if hasattr(obj, attr):
            result = getattr(obj, attr)
            return str(result) if result is not None else default
        elif isinstance(obj, dict):
            result = obj.get(attr, default)
            return str(result) if result is not None else default
        return default
