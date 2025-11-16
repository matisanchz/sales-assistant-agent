from dotenv import load_dotenv
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """
    Global application configuration.
    Automatically loads variables from environment variables and `.env`.
    """
    # -------------------------
    # General App Config
    # -------------------------
    APP_NAME: str = "Sales Assistant Agent"
    APP_VERSION: str = "0.1.0"
    ENV: str = Field("development", description="Environment: dev | prod | test")

    # -------------------------
    # LLM / AI Providers
    # -------------------------
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    DEFAULT_MODEL: str = "gemini-2.0-flash-lite"

    # -------------------------
    # Database config
    # -------------------------
    REDIS_URL: str | None = None

    # -------------------------
    # TTL Indexes
    # -------------------------
    TTL_CHAT: int = 2592000

    # -------------------------
    # Logging config
    # -------------------------
    LOG_LEVEL: str = "INFO"

    # -------------------------
    # Security
    # -------------------------
    SECRET_KEY: str = Field("dev-secret-key", description="JWT / signing key")

    # -------------------------
    # CORS
    # -------------------------
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:8501", "http://localhost:3000"],
        description="Allowed origins for UI requests"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()