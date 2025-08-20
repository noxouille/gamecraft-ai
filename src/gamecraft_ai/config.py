from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = Field(default="GameCraft AI")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # API Keys (set via environment variables)
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")
    youtube_api_key: str | None = Field(default=None, description="YouTube Data API key")
    igdb_client_id: str | None = Field(default=None, description="IGDB Client ID")
    igdb_access_token: str | None = Field(default=None, description="IGDB Access Token")

    # Cache settings
    redis_url: str | None = Field(default=None, description="Redis connection URL")
    cache_ttl: int = Field(default=3600, description="Default cache TTL in seconds")

    # Processing settings
    max_concurrent_requests: int = Field(default=10, description="Max concurrent requests")
    request_timeout: int = Field(default=60, description="Request timeout in seconds")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str | None = Field(default="logs/gamecraft_ai.log", description="Log file path")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
