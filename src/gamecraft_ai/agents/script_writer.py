from typing import Any

from ..models import ReviewScore, ScriptOutput
from ..services.llm import LLMService
from .base_agent import ScriptWriterAgentBase


class ScriptWriterAgent(ScriptWriterAgentBase):
    """Enhanced script generation agent that uses research data"""

    def __init__(self, llm_service: LLMService):
        super().__init__("ScriptWriter", llm_service)
        self.llm = llm_service

    def write_script(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate script based on research data"""
        # Use base agent's process method for enhanced logging
        return self.process(state)

    def _write_script_internal(self, state: dict[str, Any]) -> dict[str, Any]:
        """Internal script writing logic with base agent architecture"""
        query = state["query"]
        language = query.language
        duration = query.duration_minutes
        script_format = state["query_metadata"].get("script_format", "review")
        research_type = state.get("research_type", "game")

        # Update processing step
        state = self._update_processing_step(state, "script_generation")

        try:
            if research_type == "game":
                script = self._write_game_script(state, language, duration, script_format)
            elif research_type == "event":
                script = self._write_event_script(state, language, duration)
            else:
                error_msg = f"Unknown research type: {research_type}"
                return self._add_error(state, error_msg)

            if script:
                state["script"] = script
            else:
                error_msg = "Failed to generate script"
                return self._add_error(state, error_msg)

        except Exception as e:
            error_msg = f"Script generation failed: {str(e)}"
            return self._add_error(state, error_msg)

        return state

    def _write_game_script(
        self, state: dict[str, Any], language: str, duration: int, script_format: str
    ) -> ScriptOutput | None:
        """Write script for game content using research data"""
        try:
            game_info = state.get("game_info")
            media_assets = state.get("media_assets", [])
            review_scores = state.get("review_scores", [])

            if not game_info:
                return None

            # Handle both single GameInfo and list of GameInfo
            if isinstance(game_info, list) and game_info:
                game_info = game_info[0]  # Use first game for primary script

            # Create script template based on format
            template = self._get_script_template(script_format, language, duration)

            # Create timestamps for template
            timestamps = self._create_timestamps(script_format, duration)
            end_gameplay = min(duration - 3, int(duration * 0.6))
            end_review = min(duration - 1, int(duration * 0.9))

            # Prepare context data from research
            game_name = self._extract_value(game_info, "name", "Unknown Game")
            developer = self._extract_value(game_info, "developer", "Unknown Developer")
            publisher = self._extract_value(game_info, "publisher", "Unknown Publisher")
            platforms = self._extract_platforms(game_info)
            genre = self._extract_value(game_info, "genre", "Gaming")
            description = self._extract_value(game_info, "description", "")

            # Build trailer information from media assets
            trailers = [asset for asset in media_assets if "trailer" in asset.asset_type]
            trailer_info = (
                f"{len(trailers)} official trailers available" if trailers else "Trailers available"
            )

            # Build review summary
            review_summary = self._build_review_summary(review_scores)

            context = {
                "game_name": game_name,
                "developer": developer,
                "publisher": publisher,
                "platforms": platforms,
                "genre": genre,
                "description": description,
                "media_count": len(media_assets),
                "trailer_info": trailer_info,
                "review_scores": review_summary,
                "duration": duration,
                "end_gameplay": f"{end_gameplay:02d}:00",
                "end_review": f"{end_review:02d}:00",
            }

            # Generate script content
            script_content = template.format(**context)

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

    def _extract_value(self, obj, attr: str, default: str) -> str:
        """Safely extract value from object or dict"""
        if hasattr(obj, attr):
            result = getattr(obj, attr)
            return str(result) if result is not None else default
        elif isinstance(obj, dict):
            result = obj.get(attr, default)
            return str(result) if result is not None else default
        return default

    def _extract_platforms(self, game_info) -> str:
        """Extract and format platforms"""
        if not game_info:
            return "Various platforms"

        # Handle both dict and Pydantic model formats
        if hasattr(game_info, "platforms"):
            platforms = game_info.platforms
        elif isinstance(game_info, dict):
            platforms = game_info.get("platforms", [])
        else:
            return "Various platforms"

        if isinstance(platforms, list) and platforms:
            return ", ".join(str(p) for p in platforms)
        elif platforms:
            return str(platforms)
        return "Various platforms"

    def _build_review_summary(self, review_scores: list[ReviewScore]) -> str:
        """Build a summary of review scores"""
        if not review_scores:
            return "Reviews pending"

        summaries = []
        for score in review_scores[:3]:  # Top 3 reviews
            # Handle both Pydantic model and dict formats
            if hasattr(score, "outlet_name"):
                outlet = score.outlet_name
                score_val = score.score
            elif isinstance(score, dict):
                outlet = score.get("outlet_name", "Review")
                score_val = score.get("score", "N/A")
            else:
                outlet = "Review"
                score_val = "N/A"

            summaries.append(f"{outlet}: {score_val}")

        return ", ".join(summaries)

    def _write_event_script(
        self, state: dict[str, Any], language: str, duration: int
    ) -> ScriptOutput | None:
        """Write script for event content using research data"""
        try:
            event_info = state.get("event_info")
            game_info_list = state.get("game_info", [])
            media_assets = state.get("media_assets", [])

            if not event_info:
                return None

            # Create event script template
            template = self._get_event_template(language, duration)

            # Create timestamps for template
            timestamps = self._create_event_timestamps(duration)
            end_highlights = min(duration - 2, int(duration * 0.8))

            # Extract event data
            event_title = self._extract_value(event_info, "title", "Gaming Event")
            announced_games = event_info.get("announced_games", []) if event_info else []
            highlights = event_info.get("highlights", []) if event_info else []

            # Build game details from research
            game_details = []
            for game in game_info_list[:3]:  # Top 3 researched games
                name = self._extract_value(game, "name", "Unknown Game")
                developer = self._extract_value(game, "developer", "Unknown Developer")
                game_details.append(f"{name} by {developer}")

            context = {
                "event_title": event_title,
                "game_count": len(announced_games),
                "announced_games": ", ".join(announced_games[:5])
                if announced_games
                else "Various games",
                "game_details": ", ".join(game_details) if game_details else "Exciting new titles",
                "highlights": ". ".join(highlights[:3])
                if highlights
                else "Major announcements and reveals",
                "trailer_count": len(media_assets),
                "duration": duration,
                "end_highlights": f"{end_highlights:02d}:00",
            }

            script_content = template.format(**context)

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

[00:30-02:00] {game_name} est développé par {developer} et édité par {publisher}, disponible sur {platforms}. {description}

[02:00-{end_gameplay}] Côté gameplay, {game_name} propose une expérience unique dans le genre {genre}. On a {trailer_info} pour vous montrer le jeu en action.

[{end_gameplay}-{end_review}] Les critiques donnent {review_scores}. La communauté semble vraiment apprécier l'expérience.

[{end_review}-{duration}:00] En conclusion, {game_name} mérite définitivement votre attention. Dites-moi en commentaire si vous comptez y jouer !"""
            elif script_format == "preview":
                return """[00:00-00:30] Salut ! Aujourd'hui, on découvre {game_name} de {developer} - un {genre} qui s'annonce prometteur !

[00:30-02:00] Développé par {developer} pour {publisher}, {game_name} sortira sur {platforms}. {description}

[02:00-{end_gameplay}] D'après {trailer_info}, le gameplay semble innovant pour un {genre}. Les mécaniques ont l'air vraiment intéressantes.

[{end_gameplay}-{end_review}] Les premières impressions sont {review_scores}. L'attente monte dans la communauté !

[{end_review}-{duration}:00] {game_name} pourrait bien être le {genre} de l'année. Qu'en pensez-vous ?"""
            elif script_format == "complete_guide":
                return """[00:00-00:30] Salut ! Guide complet de {game_name} de {developer} - tout ce que vous devez savoir !

[00:30-03:00] {game_name} est développé par {developer}, édité par {publisher}, disponible sur {platforms}. {description}

[03:00-{end_gameplay}] Gameplay détaillé : {game_name} propose une expérience {genre} complète. On a {trailer_info} pour tout vous montrer.

[{end_gameplay}-{end_review}] Critiques et avis : {review_scores}. La réception est globalement positive.

[{end_review}-{duration}:00] Guide d'achat complet : {game_name} vaut-il le coup ? Tout dépend de vos goûts en {genre} !"""
        else:
            if script_format == "review":
                return """[00:00-00:30] Hey everyone! Today we're diving deep into {game_name} from {developer}. This {genre} has been making serious waves.

[00:30-02:00] {game_name} is developed by {developer} and published by {publisher}, available on {platforms}. {description}

[02:00-{end_gameplay}] The gameplay in {game_name} offers a unique experience in the {genre} space. We've got {trailer_info} showcasing what makes this special.

[{end_gameplay}-{end_review}] Critics are rating it {review_scores}, and the community response has been fantastic.

[{end_review}-{duration}:00] Overall, {game_name} is absolutely worth your time and money. Drop a comment and let me know your thoughts!"""
            elif script_format == "preview":
                return """[00:00-00:30] What's up everyone! Today we're previewing {game_name} from {developer} - a {genre} that's generating serious buzz!

[00:30-02:00] Developed by {developer} for {publisher}, {game_name} is coming to {platforms}. {description}

[02:00-{end_gameplay}] From {trailer_info}, the gameplay looks incredibly promising for a {genre}. The mechanics seem really innovative.

[{end_gameplay}-{end_review}] Early impressions show {review_scores}. The hype is building in the community!

[{end_review}-{duration}:00] {game_name} could be the {genre} of the year. What do you think?"""
            elif script_format == "complete_guide":
                return """[00:00-00:30] What's up everyone! Complete {game_name} guide from {developer} - everything you need to know!

[00:30-03:00] {game_name} is developed by {developer}, published by {publisher}, available on {platforms}. {description}

[03:00-{end_gameplay}] Complete gameplay breakdown: {game_name} offers a comprehensive {genre} experience. We've got {trailer_info} showing you everything.

[{end_gameplay}-{end_review}] Critical reception: {review_scores}. The overall response has been really positive.

[{end_review}-{duration}:00] Complete buying guide: Is {game_name} worth it? It all depends on your taste for {genre} games!"""

        # Default template
        return "Generated script content for {game_name} - {duration} minute {script_format}"

    def _get_event_template(self, language: str, duration: int) -> str:
        """Get event script template with research data"""
        if language == "fr":
            return """[00:00-00:30] Salut ! Résumé complet de {event_title} aujourd'hui !

[00:30-02:00] Cet événement nous a apporté {game_count} annonces majeures : {announced_games}.

[02:00-{end_highlights}] Les jeux phares incluent {game_details}. On a trouvé {trailer_count} bandes-annonces officielles ! Moments forts : {highlights}

[{end_highlights}-{duration}:00] Un événement exceptionnel ! Quel jeu vous a le plus marqué ? Dites-le moi en commentaire !"""
        else:
            return """[00:00-00:30] Hey everyone! Complete {event_title} breakdown coming your way!

[00:30-02:00] This showcase delivered {game_count} major announcements including: {announced_games}.

[02:00-{end_highlights}] Featured games include {game_details}. We've got {trailer_count} official trailers to show you! Key highlights: {highlights}

[{end_highlights}-{duration}:00] What an incredible event! Which announcement got you most hyped? Drop it in the comments!"""

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
