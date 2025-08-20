from pydantic import BaseModel, Field

from .content import EventInfo, GameInfo, MediaAsset, ReviewScore


class ScriptOutput(BaseModel):
    title: str = Field(..., description="Script title")
    duration_minutes: int = Field(..., description="Target duration")
    script_content: str = Field(..., description="Generated script content")
    timestamps: dict[str, str] = Field(default_factory=dict, description="Section timestamps")
    format_type: str = Field(..., description="Script format (review, preview, event)")
    language: str = Field(..., description="Script language")


class ThumbnailSuggestion(BaseModel):
    """YouTube thumbnail suggestion with AI prompt"""

    style: str = Field(..., description="Thumbnail style category")
    prompt: str = Field(..., description="AI image generation prompt")
    description: str = Field(..., description="Human-readable description")
    target_ctr: str = Field(..., description="Expected click-through rate")
    design_notes: list[str] = Field(default_factory=list, description="Design tips and rationale")

    class Config:
        example = {
            "title": "Baldur's Gate 3 - Complete Review",
            "duration_minutes": 10,
            "script_content": "[00:00-00:30] Welcome back to the channel...",
            "timestamps": {
                "hook": "00:00-00:30",
                "overview": "00:30-02:00",
                "gameplay": "02:00-04:00",
            },
            "format_type": "review",
            "language": "en",
        }


class ProcessingResult(BaseModel):
    success: bool = Field(..., description="Processing success status")
    query_type: str = Field(..., description="Detected query type")
    language: str = Field(..., description="Detected language")

    # Content data
    game_info: GameInfo | None = Field(None, description="Game information")
    media_assets: list[MediaAsset] = Field(default_factory=list, description="Found media")
    review_scores: list[ReviewScore] = Field(default_factory=list, description="Review scores")
    event_info: EventInfo | None = Field(None, description="Event information")

    # Generated output
    script: ScriptOutput | None = Field(None, description="Generated script")

    # Processing metadata
    processing_time: float | None = Field(None, description="Processing time in seconds")
    cached: bool = Field(default=False, description="Result was cached")
    errors: list[str] = Field(default_factory=list, description="Processing errors")
    warnings: list[str] = Field(default_factory=list, description="Processing warnings")

    class Config:
        example = {
            "success": True,
            "query_type": "game",
            "language": "en",
            "processing_time": 45.2,
            "cached": False,
            "errors": [],
            "warnings": ["Some review scores unavailable"],
        }
