from enum import Enum

from pydantic import BaseModel, Field, validator


class QueryType(str, Enum):
    EVENT = "event"
    GAME = "game"


class Language(str, Enum):
    ENGLISH = "en"
    FRENCH = "fr"


class QueryInput(BaseModel):
    text: str = Field(..., description="User query text")
    duration_minutes: int = Field(default=10, ge=5, le=20, description="Target script duration")
    query_type: QueryType | None = Field(None, description="Detected query type")
    language: Language | None = Field(None, description="Detected language")
    confidence: float | None = Field(None, ge=0.0, le=1.0, description="Classification confidence")

    # Extracted information
    game_name: str | None = Field(None, description="Extracted game name")
    video_url: str | None = Field(None, description="Event video URL")
    script_format: str | None = Field(None, description="Script format (review, preview, etc.)")

    @validator("text")
    def text_must_not_be_empty(cls, v):  # noqa: N805
        if not v.strip():
            raise ValueError("Query text cannot be empty")
        return v.strip()

    class Config:
        example = {
            "text": "Make a 10-minute review video about Baldur's Gate 3",
            "duration_minutes": 10,
            "query_type": "game",
            "language": "en",
        }
