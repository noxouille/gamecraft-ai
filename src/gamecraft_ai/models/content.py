from pydantic import BaseModel, Field, HttpUrl


class GameInfo(BaseModel):
    name: str = Field(..., description="Game name")
    developer: str | None = Field(None, description="Developer name")
    publisher: str | None = Field(None, description="Publisher name")
    release_date: str | None = Field(None, description="Release date")
    platforms: list[str] = Field(default_factory=list, description="Available platforms")
    genre: str | None = Field(None, description="Game genre")
    price: float | None = Field(None, description="Current price")
    description: str | None = Field(None, description="Game description")

    class Config:
        example = {
            "name": "Baldur's Gate 3",
            "developer": "Larian Studios",
            "publisher": "Larian Studios",
            "release_date": "2023-08-03",
            "platforms": ["PC", "PS5", "Xbox Series X/S"],
            "genre": "RPG",
            "price": 59.99,
        }


class MediaAsset(BaseModel):
    title: str = Field(..., description="Media title")
    url: HttpUrl = Field(..., description="Media URL")
    asset_type: str = Field(..., description="Type: trailer, gameplay, interview")
    duration_seconds: int | None = Field(None, description="Duration in seconds")
    channel_name: str | None = Field(None, description="YouTube channel name")
    upload_date: str | None = Field(None, description="Upload date")
    language: str | None = Field(None, description="Content language")

    class Config:
        example = {
            "title": "Baldur's Gate 3 - Official Launch Trailer",
            "url": "https://www.youtube.com/watch?v=example",
            "asset_type": "trailer",
            "duration_seconds": 180,
            "channel_name": "Larian Studios",
        }


class ReviewScore(BaseModel):
    outlet_name: str = Field(..., description="Review outlet name")
    score: str = Field(..., description="Review score")
    max_score: str | None = Field(None, description="Maximum possible score")
    review_url: HttpUrl | None = Field(None, description="Review URL")
    summary: str | None = Field(None, description="Review summary")

    class Config:
        example = {
            "outlet_name": "IGN",
            "score": "96",
            "max_score": "100",
            "review_url": "https://www.ign.com/articles/baldurs-gate-3-review",
            "summary": "An exceptional RPG that sets a new standard",
        }


class EventInfo(BaseModel):
    title: str = Field(..., description="Event title")
    video_url: HttpUrl = Field(..., description="Event video URL")
    duration_seconds: int | None = Field(None, description="Video duration")
    announced_games: list[str] = Field(default_factory=list, description="Games announced")
    highlights: list[str] = Field(default_factory=list, description="Key highlights")
    timestamps: dict[str, str] = Field(default_factory=dict, description="Important timestamps")

    class Config:
        example = {
            "title": "Xbox Games Showcase 2025",
            "video_url": "https://www.youtube.com/watch?v=example",
            "duration_seconds": 7200,
            "announced_games": ["Starfield DLC", "Halo Infinite Season 3"],
            "highlights": ["Major Starfield expansion announced", "New Halo content revealed"],
        }
