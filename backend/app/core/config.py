from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    app_name: str = "TraceRoot"
    app_env: str = "development"
    secret_key: str = "development-only-change-me"
    database_url: str = "sqlite:///./traceroot.db"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    llm_provider: str = "demo"
    llm_model: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""
    demo_mode: bool = True
    sandbox_root: Path = Path("../evaluation_cases")
    access_token_minutes: int = 30
    refresh_token_days: int = 7
    max_agent_iterations: int = Field(default=4, ge=1, le=10)
    max_tool_calls: int = Field(default=20, ge=1, le=100)
    llm_timeout_seconds: int = Field(default=45, ge=5, le=180)

    @property
    def cors_origin_list(self) -> list[str]:
        return [part.strip() for part in self.cors_origins.split(",") if part.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
