from ..agents import ClassifierAgent, ResearchAgent, ScriptWriterAgent, YouTubeCoachAgent
from .state import GameCraftState


class NodeManager:
    """Manages all workflow nodes"""

    def __init__(
        self,
        classifier: ClassifierAgent,
        researcher: ResearchAgent,
        script_writer: ScriptWriterAgent,
        youtube_coach: YouTubeCoachAgent,
    ):
        self.classifier = classifier
        self.researcher = researcher
        self.script_writer = script_writer
        self.youtube_coach = youtube_coach

    def classify_node(self, state: GameCraftState) -> GameCraftState:
        """Query classification node"""
        try:
            state["current_step"] = "classify"
            updated_state = self.classifier.classify_query(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("classify")
            return state
        except Exception as e:
            state["errors"].append(f"Classification error: {str(e)}")
            return state

    def research_node(self, state: GameCraftState) -> GameCraftState:
        """Research node (handles both game and event research)"""
        try:
            state["current_step"] = "research"
            updated_state = self.researcher.conduct_research(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("research")
            return state
        except Exception as e:
            state["errors"].append(f"Research error: {str(e)}")
            return state

    def script_generation_node(self, state: GameCraftState) -> GameCraftState:
        """Script generation node"""
        try:
            state["current_step"] = "script_generation"
            updated_state = self.script_writer.write_script(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("script_generation")
            return state
        except Exception as e:
            state["errors"].append(f"Script generation error: {str(e)}")
            return state

    def thumbnail_generation_node(self, state: GameCraftState) -> GameCraftState:
        """Thumbnail generation node"""
        try:
            state["current_step"] = "thumbnail_generation"
            updated_state = self.youtube_coach.generate_thumbnails(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("thumbnail_generation")
            return state
        except Exception as e:
            state["errors"].append(f"Thumbnail generation error: {str(e)}")
            return state

    def finish_node(self, state: GameCraftState) -> GameCraftState:
        """Final processing node"""
        state["current_step"] = "finished"
        state["completed_steps"].append("finished")

        # Set success status
        if not state["errors"] and state["script"]:
            # Processing completed successfully
            pass
        elif state["errors"]:
            state["warnings"].append("Processing completed with errors")

        return state


def should_continue_to_research(state: GameCraftState) -> str:
    """Conditional edge function for research processing"""
    if state["errors"]:
        return "finish"
    else:
        return "research"


def should_continue_to_script(state: GameCraftState) -> str:
    """Conditional edge function for script generation"""
    if state["errors"]:
        # Skip to finish if there are errors
        return "finish"
    else:
        return "script_generation"


def should_continue_to_thumbnails(state: GameCraftState) -> str:
    """Conditional edge function for thumbnail generation"""
    if state["errors"]:
        # Skip to finish if there are errors
        return "finish"
    else:
        return "thumbnail_generation"
