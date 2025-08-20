from typing import Any, TypedDict

from ..models import EventInfo, GameInfo, MediaAsset, QueryInput, ReviewScore, ScriptOutput


class GameCraftState(TypedDict):
    """LangGraph state schema for GameCraft AI workflow"""

    # Input query information
    query: QueryInput
    query_metadata: dict[str, Any]

    # Research results
    game_info: GameInfo | None
    media_assets: list[MediaAsset]
    review_scores: list[ReviewScore]
    event_info: EventInfo | None

    # Generated output
    script: ScriptOutput | None

    # Processing metadata
    processing_time: float
    cached: bool
    errors: list[str]
    warnings: list[str]

    # Internal workflow state
    current_step: str
    completed_steps: list[str]


def create_initial_state(query_text: str, duration_minutes: int = 10) -> GameCraftState:
    """Create initial state from user input"""
    return GameCraftState(
        query=QueryInput(text=query_text, duration_minutes=duration_minutes),
        query_metadata={},
        game_info=None,
        media_assets=[],
        review_scores=[],
        event_info=None,
        script=None,
        processing_time=0.0,
        cached=False,
        errors=[],
        warnings=[],
        current_step="start",
        completed_steps=[],
    )
