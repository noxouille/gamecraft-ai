import time
from typing import Any

from langgraph.graph import END, StateGraph

from ..agents import ClassifierAgent, ResearchAgent, ScriptWriterAgent, YouTubeCoachAgent
from ..services import IGDBService, LLMService, YouTubeService
from ..utils.cache import CacheService
from .nodes import (
    NodeManager,
    should_continue_to_research,
    should_continue_to_script,
    should_continue_to_thumbnails,
)
from .state import GameCraftState, create_initial_state


class WorkflowManager:
    """Manages the complete GameCraft AI workflow"""

    def __init__(self, model: str | None = "gpt-4o-mini"):
        # Initialize services
        self.youtube_service = YouTubeService()
        self.igdb_service = IGDBService()
        self.llm_service = LLMService(model=model or "gpt-4o-mini")
        self.cache_service = CacheService()

        # Initialize agents
        self.classifier = ClassifierAgent(self.llm_service)
        self.researcher = ResearchAgent(self.igdb_service, self.youtube_service, self.cache_service)
        self.script_writer = ScriptWriterAgent(self.llm_service)
        self.youtube_coach = YouTubeCoachAgent(self.llm_service)

        # Initialize node manager
        self.node_manager = NodeManager(
            self.classifier, self.researcher, self.script_writer, self.youtube_coach
        )

        # Create workflow
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        # Create workflow
        workflow = StateGraph(GameCraftState)

        # Add nodes
        workflow.add_node("classify", self.node_manager.classify_node)
        workflow.add_node("research", self.node_manager.research_node)
        workflow.add_node("script_generation", self.node_manager.script_generation_node)
        workflow.add_node("thumbnail_generation", self.node_manager.thumbnail_generation_node)
        workflow.add_node("finish", self.node_manager.finish_node)

        # Set entry point
        workflow.set_entry_point("classify")

        # Add conditional edges
        workflow.add_conditional_edges(
            "classify",
            should_continue_to_research,
            {"research": "research", "finish": "finish"},
        )

        # Research goes to script generation
        workflow.add_conditional_edges(
            "research",
            should_continue_to_script,
            {"script_generation": "script_generation", "finish": "finish"},
        )

        # Script generation goes to thumbnail generation
        workflow.add_conditional_edges(
            "script_generation",
            should_continue_to_thumbnails,
            {"thumbnail_generation": "thumbnail_generation", "finish": "finish"},
        )

        # Thumbnail generation always goes to finish
        workflow.add_edge("thumbnail_generation", "finish")

        # Finish is terminal
        workflow.add_edge("finish", END)

        return workflow.compile()

    def process_query(
        self, query_text: str, duration_minutes: int = 10, model: str | None = None
    ) -> dict[str, Any]:
        """Process a user query through the complete workflow"""
        start_time = time.time()

        # If model is provided and different from current, reinitialize
        if model and model != self.llm_service.model:
            # Reinitialize with new model
            self.llm_service = LLMService(model=model)
            self.classifier = ClassifierAgent(self.llm_service)
            self.researcher = ResearchAgent(
                self.igdb_service, self.youtube_service, self.cache_service
            )
            self.script_writer = ScriptWriterAgent(self.llm_service)
            self.youtube_coach = YouTubeCoachAgent(self.llm_service)

        # Create initial state
        initial_state = create_initial_state(query_text, duration_minutes)

        try:
            # Run workflow
            final_state = self.workflow.invoke(initial_state)

            # Calculate processing time
            processing_time = time.time() - start_time
            final_state["processing_time"] = processing_time

            return self._format_result(final_state)

        except Exception as e:
            # Handle workflow errors
            error_result = {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time,
                "query_type": getattr(initial_state["query"], "query_type", None),
                "language": getattr(initial_state["query"], "language", None),
            }
            return error_result

    def _format_result(self, state: GameCraftState) -> dict[str, Any]:
        """Format final state into user-friendly result"""
        success = bool(state["script"] and not state["errors"])

        result = {
            "success": success,
            "query_type": getattr(state["query"], "query_type", None),
            "language": getattr(state["query"], "language", None),
            "processing_time": state["processing_time"],
            "cached": state["cached"],
            "errors": state["errors"],
            "warnings": state["warnings"],
        }

        # Add content data if available
        if state["game_info"]:
            result["game_info"] = state["game_info"]
        if state["media_assets"]:
            result["media_assets"] = state["media_assets"]
        if state["review_scores"]:
            result["review_scores"] = state["review_scores"]
        if state["event_info"]:
            result["event_info"] = state["event_info"]
        if state["script"]:
            result["script"] = state["script"]

        return result


def create_workflow() -> WorkflowManager:
    """Factory function to create workflow manager"""
    return WorkflowManager()
