from typing import Any

from ..models import QueryType, ScriptOutput
from ..services.llm import LLMService


class ScriptWriterAgent:
    """Script generation agent"""

    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def write_script(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate script based on collected information"""
        query = state["query"]
        query_type = query.query_type
        language = query.language
        duration = query.duration_minutes
        script_format = state["query_metadata"].get("script_format", "review")

        if query_type == QueryType.GAME:
            script = self._write_game_script(state, language, duration, script_format)
        elif query_type == QueryType.EVENT:
            script = self._write_event_script(state, language, duration)
        else:
            state["errors"].append("Unknown query type for script generation")
            return state

        if script:
            state["script"] = script
        else:
            state["errors"].append("Failed to generate script")

        return state

    def _write_game_script(
        self, state: dict[str, Any], language: str, duration: int, script_format: str
    ) -> ScriptOutput | None:
        """Write script for game content"""
        try:
            game_info = state.get("game_info")
            media_assets = state.get("media_assets", [])
            review_scores = state.get("review_scores", [])

            if not game_info:
                return None

            # Create script prompt based on format
            template = self._get_script_template(script_format, language, duration)

            # Create timestamps for template
            timestamps = self._create_timestamps(script_format, duration)
            end_gameplay = min(duration - 3, int(duration * 0.6))
            end_review = min(duration - 1, int(duration * 0.9))

            # Prepare context data
            context = {
                "game_name": game_info.name
                if hasattr(game_info, "name")
                else game_info.get("name", "Unknown Game"),
                "developer": game_info.developer
                if hasattr(game_info, "developer")
                else game_info.get("developer", "Unknown Developer"),
                "publisher": game_info.publisher
                if hasattr(game_info, "publisher")
                else game_info.get("publisher", "Unknown Publisher"),
                "platforms": ", ".join(
                    game_info.platforms
                    if hasattr(game_info, "platforms")
                    else game_info.get("platforms", [])
                )
                or "Various",
                "genre": (
                    game_info.genre if hasattr(game_info, "genre") else game_info.get("genre")
                )
                or "Gaming",
                "description": (
                    game_info.description
                    if hasattr(game_info, "description")
                    else game_info.get("description")
                )
                or "",
                "media_count": len(media_assets),
                "review_scores": ", ".join(
                    [f"{score.outlet_name}: {score.score}" for score in review_scores[:3]]
                )
                or "No reviews available",
                "duration": duration,
                "end_gameplay": f"{end_gameplay:02d}:00",
                "end_review": f"{end_review:02d}:00",
            }

            # Generate script content
            script_content = template.format(**context)

            game_name = (
                game_info.name
                if hasattr(game_info, "name")
                else game_info.get("name", "Unknown Game")
            )
            return ScriptOutput(
                title=f"{game_name} - {script_format.replace('_', ' ').title()}",
                duration_minutes=duration,
                script_content=script_content,
                timestamps=timestamps,
                format_type=script_format,
                language=language,
            )

        except Exception as e:
            print(f"Error writing game script: {e}")
            return None

    def _write_event_script(
        self, state: dict[str, Any], language: str, duration: int
    ) -> ScriptOutput | None:
        """Write script for event content"""
        try:
            event_info = state.get("event_info")
            if not event_info:
                return None

            # Simple event script template
            template = self._get_event_template(language, duration)

            # Create timestamps for template
            timestamps = self._create_event_timestamps(duration)
            end_highlights = min(duration - 2, int(duration * 0.8))

            context = {
                "event_title": event_info.title
                if hasattr(event_info, "title")
                else event_info.get("title", "Gaming Event"),
                "game_count": len(
                    event_info.announced_games
                    if hasattr(event_info, "announced_games")
                    else event_info.get("announced_games", [])
                ),
                "announced_games": ", ".join(
                    (
                        event_info.announced_games
                        if hasattr(event_info, "announced_games")
                        else event_info.get("announced_games", [])
                    )[:5]
                )
                or "Various games",
                "highlights": ". ".join(
                    (
                        event_info.highlights
                        if hasattr(event_info, "highlights")
                        else event_info.get("highlights", [])
                    )[:3]
                )
                or "Exciting announcements and reveals",
                "duration": duration,
                "end_highlights": f"{end_highlights:02d}:00",
            }

            script_content = template.format(**context)

            event_title = (
                event_info.title
                if hasattr(event_info, "title")
                else event_info.get("title", "Gaming Event")
            )
            return ScriptOutput(
                title=f"{event_title} - Summary",
                duration_minutes=duration,
                script_content=script_content,
                timestamps=timestamps,
                format_type="event_summary",
                language=language,
            )

        except Exception as e:
            print(f"Error writing event script: {e}")
            return None

    def _get_script_template(self, script_format: str, language: str, duration: int) -> str:
        """Get script template based on format and language"""

        if language == "fr":
            if script_format == "review":
                return """[00:00-00:30] Salut tout le monde ! Aujourd'hui on parle de {game_name}, développé par {developer}. Ce {genre} a fait beaucoup parler de lui récemment.

[00:30-02:00] {game_name} est un jeu développé par {developer} et édité par {publisher}, disponible sur {platforms}. {description}

[02:00-{end_gameplay}] Côté gameplay, {game_name} propose une expérience unique dans le genre {genre}. Le jeu se distingue par ses mécaniques innovantes et son attention aux détails.

[{end_gameplay}-{end_review}] Les critiques sont {review_scores} et la communauté semble apprécier l'expérience globale.

[{end_review}-{duration}:00] En conclusion, {game_name} est un excellent ajout à votre ludothèque. N'hésitez pas à me dire en commentaire ce que vous en pensez !"""
        else:
            if script_format == "review":
                return """[00:00-00:30] Hey everyone! Today we're diving into {game_name} from {developer}. This {genre} has been making waves lately.

[00:30-02:00] {game_name} is developed by {developer} and published by {publisher}, available on {platforms}. {description}

[02:00-{end_gameplay}] The gameplay in {game_name} offers a unique experience in the {genre} space. What sets it apart are the innovative mechanics and attention to detail.

[{end_gameplay}-{end_review}] Critics have rated it {review_scores} and the community response has been overwhelmingly positive.

[{end_review}-{duration}:00] Overall, {game_name} is a solid addition to your gaming library. Let me know what you think in the comments below!"""

        # Default template
        return "Generated script content for {game_name} - {duration} minute {script_format}"

    def _get_event_template(self, language: str, duration: int) -> str:
        """Get event script template"""
        if language == "fr":
            return """[00:00-00:30] Salut ! Résumé complet de {event_title} aujourd'hui !

[00:30-02:00] Cet événement nous a apporté {game_count} annonces majeures : {announced_games}.

[02:00-{end_highlights}] Les moments forts : {highlights}

[{end_highlights}-{duration}:00] C'était un événement riche en surprises ! Dites-moi quel jeu vous attend le plus !"""
        else:
            return """[00:00-00:30] Hey everyone! Complete {event_title} summary coming right up!

[00:30-02:00] This showcase brought us {game_count} major announcements including: {announced_games}.

[02:00-{end_highlights}] Key highlights include: {highlights}

[{end_highlights}-{duration}:00] What an event! Let me know which announcement excited you most in the comments!"""

    def _create_timestamps(self, script_format: str, duration: int) -> dict[str, str]:
        """Create section timestamps for game scripts"""
        if script_format == "review":
            end_gameplay = min(duration - 3, int(duration * 0.6))
            end_review = min(duration - 1, int(duration * 0.9))

            return {
                "hook": "00:00-00:30",
                "overview": "00:30-02:00",
                "gameplay": f"02:00-{end_gameplay:02d}:00",
                "review_scores": f"{end_gameplay:02d}:00-{end_review:02d}:00",
                "conclusion": f"{end_review:02d}:00-{duration:02d}:00",
            }

        return {"full_content": f"00:00-{duration:02d}:00"}

    def _create_event_timestamps(self, duration: int) -> dict[str, str]:
        """Create section timestamps for event scripts"""
        end_highlights = min(duration - 2, int(duration * 0.8))

        return {
            "intro": "00:00-00:30",
            "announcements": "00:30-02:00",
            "highlights": f"02:00-{end_highlights:02d}:00",
            "conclusion": f"{end_highlights:02d}:00-{duration:02d}:00",
        }
