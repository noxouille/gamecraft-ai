from ..agents import ClassifierAgent, EventAnalyzerAgent, GameResearcherAgent, ScriptWriterAgent
from ..models import QueryType
from .state import GameCraftState


class NodeManager:
    """Manages all workflow nodes"""

    def __init__(
        self,
        classifier: ClassifierAgent,
        game_researcher: GameResearcherAgent,
        event_analyzer: EventAnalyzerAgent,
        script_writer: ScriptWriterAgent,
    ):
        self.classifier = classifier
        self.game_researcher = game_researcher
        self.event_analyzer = event_analyzer
        self.script_writer = script_writer

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

    def game_research_node(self, state: GameCraftState) -> GameCraftState:
        """Game research node"""
        try:
            state["current_step"] = "game_research"
            updated_state = self.game_researcher.research_game(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("game_research")
            return state
        except Exception as e:
            state["errors"].append(f"Game research error: {str(e)}")
            return state

    def event_analysis_node(self, state: GameCraftState) -> GameCraftState:
        """Event analysis node"""
        try:
            state["current_step"] = "event_analysis"
            updated_state = self.event_analyzer.analyze_event(dict(state))
            state.update(updated_state)  # type: ignore[typeddict-item]
            state["completed_steps"].append("event_analysis")
            return state
        except Exception as e:
            state["errors"].append(f"Event analysis error: {str(e)}")
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


def should_process_game(state: GameCraftState) -> str:
    """Conditional edge function for game processing"""
    if state["query"].query_type == QueryType.GAME:
        return "game_research"
    else:
        return "event_analysis"


def should_continue_to_script(state: GameCraftState) -> str:
    """Conditional edge function for script generation"""
    if state["errors"]:
        # Skip to finish if there are errors
        return "finish"
    else:
        return "script_generation"
