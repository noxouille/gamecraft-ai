from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="GameCraft AI")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
