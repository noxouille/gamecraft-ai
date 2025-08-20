from typing import Any

from ..graph.workflow import WorkflowManager


class UIHandlers:
    """Handles UI interactions and workflows"""

    def __init__(self):
        self.workflow_manager = None  # Will be created per request to handle model selection

    def process_query(
        self, query_text: str, duration_minutes: int, model: str = "gpt-4o-mini"
    ) -> tuple[str, str, str, str]:
        """Process user query and return results for Gradio interface"""

        if not query_text.strip():
            return "Error: Please enter a query", "", "", ""

        try:
            # Create or reuse workflow manager with selected model
            if not self.workflow_manager or (
                hasattr(self.workflow_manager, "llm_service")
                and self.workflow_manager.llm_service.model != model
            ):
                self.workflow_manager = WorkflowManager(model=model)

            # Process through workflow
            result = self.workflow_manager.process_query(query_text, duration_minutes)

            if result["success"] and result.get("script"):
                script = result["script"]

                # Format script output
                script_content = self._format_script_output(script)

                # Format research data
                research_data = self._format_research_data(result)

                # Format YouTube links
                youtube_links = self._format_youtube_links(result)

                # Format thumbnail suggestions
                thumbnail_ideas = self._format_thumbnail_suggestions(script, query_text, result)

                return script_content, research_data, youtube_links, thumbnail_ideas
            else:
                error_msg = (
                    f"Processing failed: {', '.join(result.get('errors', ['Unknown error']))}"
                )
                return error_msg, "", "", ""

        except Exception as e:
            return f"Error: {str(e)}", "", "", ""

    def _format_script_output(self, script) -> str:
        """Format script for display"""
        # Handle both Pydantic model and dict formats
        if hasattr(script, "title"):
            # Pydantic model
            title = script.title
            duration = script.duration_minutes
            format_type = script.format_type
            language = script.language
            content = script.script_content
            timestamps = script.timestamps
        else:
            # Dictionary format
            title = script["title"]
            duration = script["duration_minutes"]
            format_type = script["format_type"]
            language = script["language"]
            content = script["script_content"]
            timestamps = script.get("timestamps", {})

        output = f"# {title}\n\n"
        output += f"**Duration:** {duration} minutes\n"
        output += f"**Format:** {format_type.replace('_', ' ').title()}\n"
        output += f"**Language:** {language}\n\n"

        output += "## Script Content\n\n"
        output += content

        if timestamps:
            output += "\n\n## Timestamps\n\n"
            for section, time_range in timestamps.items():
                output += f"- **{section.replace('_', ' ').title()}:** {time_range}\n"

        return output

    def _format_research_data(self, result: dict[str, Any]) -> str:
        """Format research data for display"""
        output = ""

        # Game information
        if result.get("game_info"):
            game = result["game_info"]
            output += "## Game Information\n\n"

            # Handle both Pydantic model and dict formats
            if hasattr(game, "name"):
                # Pydantic model
                output += f"- **Name:** {game.name or 'N/A'}\n"
                output += f"- **Developer:** {game.developer or 'N/A'}\n"
                output += f"- **Publisher:** {game.publisher or 'N/A'}\n"
                output += f"- **Release Date:** {game.release_date or 'N/A'}\n"
                output += (
                    f"- **Platforms:** {', '.join(game.platforms) if game.platforms else 'N/A'}\n"
                )
                output += f"- **Genre:** {game.genre or 'N/A'}\n"

                if game.description:
                    output += f"\n**Description:** {game.description}\n"
            else:
                # Dictionary format
                output += f"- **Name:** {game.get('name', 'N/A')}\n"
                output += f"- **Developer:** {game.get('developer', 'N/A')}\n"
                output += f"- **Publisher:** {game.get('publisher', 'N/A')}\n"
                output += f"- **Release Date:** {game.get('release_date', 'N/A')}\n"
                output += f"- **Platforms:** {', '.join(game.get('platforms', [])) or 'N/A'}\n"
                output += f"- **Genre:** {game.get('genre', 'N/A')}\n"

                if game.get("description"):
                    output += f"\n**Description:** {game['description']}\n"

        # Event information
        if result.get("event_info"):
            event = result["event_info"]
            output += "## Event Information\n\n"

            # Handle both Pydantic model and dict formats
            if hasattr(event, "title"):
                # Pydantic model
                output += f"- **Title:** {event.title or 'N/A'}\n"
                output += f"- **Duration:** {(event.duration_seconds or 0) // 60} minutes\n"

                if event.announced_games:
                    output += "\n**Announced Games:**\n"
                    for game in event.announced_games:
                        output += f"- {game}\n"

                if event.highlights:
                    output += "\n**Key Highlights:**\n"
                    for highlight in event.highlights:
                        output += f"- {highlight}\n"
            else:
                # Dictionary format
                output += f"- **Title:** {event.get('title', 'N/A')}\n"
                output += f"- **Duration:** {event.get('duration_seconds', 0) // 60} minutes\n"

                if event.get("announced_games"):
                    output += "\n**Announced Games:**\n"
                    for game in event["announced_games"]:
                        output += f"- {game}\n"

                if event.get("highlights"):
                    output += "\n**Key Highlights:**\n"
                    for highlight in event["highlights"]:
                        output += f"- {highlight}\n"

        # Media assets
        if result.get("media_assets"):
            output += "\n## Media Assets Found\n\n"
            for i, media in enumerate(result["media_assets"][:5], 1):  # Limit to 5
                # Handle both Pydantic model and dict formats
                if hasattr(media, "title"):
                    # Pydantic model
                    output += f"{i}. **{media.title or 'Untitled'}**\n"
                    output += f"   - Type: {media.asset_type or 'N/A'}\n"
                    output += f"   - Channel: {media.channel_name or 'N/A'}\n"
                    if media.duration_seconds:
                        duration = media.duration_seconds // 60
                        output += f"   - Duration: {duration} minutes\n"
                    output += f"   - URL: {media.url or 'N/A'}\n\n"
                else:
                    # Dictionary format
                    output += f"{i}. **{media.get('title', 'Untitled')}**\n"
                    output += f"   - Type: {media.get('asset_type', 'N/A')}\n"
                    output += f"   - Channel: {media.get('channel_name', 'N/A')}\n"
                    if media.get("duration_seconds"):
                        duration = media["duration_seconds"] // 60
                        output += f"   - Duration: {duration} minutes\n"
                    output += f"   - URL: {media.get('url', 'N/A')}\n\n"

        # Review scores
        if result.get("review_scores"):
            output += "\n## Review Scores\n\n"
            for review in result["review_scores"]:
                # Handle both Pydantic model and dict formats
                if hasattr(review, "outlet_name"):
                    # Pydantic model
                    output += f"- **{review.outlet_name}:** {review.score}\n"
                    if review.summary:
                        output += f"  - {review.summary}\n"
                else:
                    # Dictionary format
                    output += f"- **{review.get('outlet_name')}:** {review.get('score')}\n"
                    if review.get("summary"):
                        output += f"  - {review['summary']}\n"

        return output if output else "No research data available."

    def _format_youtube_links(self, result: dict[str, Any]) -> str:
        """Format YouTube video links for display"""
        output = "# 🎥 Video Footage Links\n\n"

        # Extract video links from media assets
        if result.get("media_assets"):
            media_assets = result["media_assets"]

            categories: dict[str, list] = {
                "Official Trailers": [],
                "Gameplay Videos": [],
                "Launch Trailers": [],
                "Review Videos": [],
            }

            for asset in media_assets:
                if hasattr(asset, "asset_type"):
                    # Pydantic model
                    asset_type = asset.asset_type
                    title = asset.title
                    url = asset.url
                else:
                    # Dictionary format
                    asset_type = asset.get("asset_type", "")
                    title = asset.get("title", "Untitled")
                    url = asset.get("url", "#")

                # Categorize videos
                if "trailer" in asset_type.lower() and "official" in asset_type.lower():
                    categories["Official Trailers"].append((title, url))
                elif "gameplay" in asset_type.lower():
                    categories["Gameplay Videos"].append((title, url))
                elif "launch" in asset_type.lower() or "release" in asset_type.lower():
                    categories["Launch Trailers"].append((title, url))
                elif "review" in asset_type.lower():
                    categories["Review Videos"].append((title, url))
                else:
                    categories["Official Trailers"].append((title, url))

            # Format output
            for category, videos in categories.items():
                if videos:
                    output += f"## {category}\n\n"
                    for title, url in videos:
                        output += f"- **[{title}]({url})**\n"
                    output += "\n"

        # If no media assets, show placeholder
        if not result.get("media_assets"):
            output += "No video footage links available for this query.\n\n"
            output += "💡 **Tip:** Try queries about specific games to get trailer and gameplay video links!"

        return output

    def _format_thumbnail_suggestions(self, script, query_text: str, result: dict[str, Any]) -> str:
        """Generate viral thumbnail suggestions based on script and game info"""
        output = "# 🖼️ Viral Thumbnail Ideas\n\n"

        # Extract game name for context
        game_name = "the game"
        if result.get("game_info"):
            if hasattr(result["game_info"], "name"):
                game_name = result["game_info"].name
            else:
                game_name = result["game_info"].get("name", "the game")

        # Extract script format for context
        script_format = "review"
        if hasattr(script, "format_type"):
            script_format = script.format_type
        elif isinstance(script, dict):
            script_format = script.get("format_type", "review")

        # Generate thumbnail suggestions based on content type
        suggestions = []

        if script_format == "review":
            suggestions = [
                f"**Shocked Face + Game Logo**: You with an exaggerated surprised expression, {game_name} logo prominent, bright arrows pointing at your face. Text: 'THIS CHANGED EVERYTHING!'",
                f"**Before/After Split**: Split screen showing 'boring games' vs {game_name} gameplay, with your face reacting. Text: 'Why I Quit Everything For This'",
                f"**Rating Visual**: Large score (9/10 or 5 stars) with your thumbs up, {game_name} character in background. Text: 'FINALLY! A Perfect Game?'",
                f"**Comparison Thumbnail**: {game_name} vs other popular games with VS in the middle, question marks. Text: 'Better Than [Popular Game]?'",
                f"**Emotional Reaction**: You crying/laughing with {game_name} screenshot behind. Text: 'This Game Made Me Cry' or 'I Couldn't Stop Playing'",
            ]
        elif script_format == "preview":
            suggestions = [
                f"**First Look Style**: Your eyes wide with {game_name} reflected in them. Text: 'FIRST LOOK - Mind Blown!'",
                f"**Sneak Peek**: Partially revealed {game_name} artwork with your finger to lips (shh gesture). Text: 'What They Don't Want You To Know'",
                f"**Countdown Style**: Big '2024' or release year with {game_name} logo, excited face. Text: 'Everything We Know So Far'",
                f"**Hype Building**: You pointing at amazing {game_name} graphics, mouth open. Text: 'THIS Looks INSANE!'",
                f"**Question Hook**: Big question mark, {game_name} logo, confused expression. Text: 'Will This Live Up To The Hype?'",
            ]
        elif script_format == "summary":
            suggestions = [
                "**Event Highlights**: Collage of best moments with your excited face in corner. Text: 'EVERYTHING Announced!'",
                "**Winner/Loser**: You with crown next to best announcement, trash can for worst. Text: 'Best & Worst of [Event]'",
                "**Ranking Style**: Numbers 1-10 with game logos, your face judging. Text: 'Ranking Every Announcement'",
                "**Reaction Compilation**: Multiple emotions (excited, disappointed, shocked) with event logo. Text: 'My HONEST Reactions'",
                "**Too Many Games**: You overwhelmed with game logos floating around. Text: 'Too Many Good Games!'",
            ]
        else:
            suggestions = [
                f"**Attention Grabber**: Bright colors, your shocked face, {game_name} logo. Text: 'YOU NEED TO SEE THIS!'",
                "**Question Hook**: Big bold question, your thinking pose. Text: 'Is This Worth Your Time?'",
                f"**Bold Statement**: Your confident pointing gesture, {game_name} in background. Text: 'The Truth About [Game]'",
                "**Emotional Hook**: Strong emotion (excited/angry/surprised) with relevant visuals. Text: 'This Changes Everything!'",
            ]

        output += "## 🎯 High-CTR Thumbnail Concepts\n\n"
        for i, suggestion in enumerate(suggestions, 1):
            output += f"### Option {i}\n{suggestion}\n\n"

        output += "## 🎨 Design Tips\n\n"
        output += "- **Colors**: Use high contrast (red, yellow, blue) backgrounds\n"
        output += "- **Text**: Large, bold fonts (50px+) with stroke/shadow for readability\n"
        output += "- **Face**: Your expression should match the video's energy and emotion\n"
        output += "- **Rule of Thirds**: Place key elements along the grid lines\n"
        output += "- **Mobile Optimization**: Ensure text is readable on small screens\n"
        output += "- **A/B Testing**: Create 2-3 versions and test which performs better\n"

        output += "\n## 📱 Viral Elements\n\n"
        output += "- **Arrows**: Point to surprising elements or your reaction\n"
        output += "- **Circles/Highlights**: Draw attention to key game features\n"
        output += "- **Emojis**: Use sparingly but effectively (😱🔥💯)\n"
        output += "- **Cliffhanger Text**: Create curiosity gaps ('You Won't Believe...', 'What Happens Next...')\n"

        return output
