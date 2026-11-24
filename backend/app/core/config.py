"""
ForgeAI Backend Configuration.

Centralized configuration using Pydantic Settings.
All values are loaded from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────
    app_name: str = "ForgeAI"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    secret_key: str = "change-me-in-production"
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"

    # ── Supabase ─────────────────────────────────────────────────
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    # JWT Secret used by Supabase Auth to SIGN user access tokens.
    # Found in: Supabase Dashboard > Project Settings > API > JWT Settings.
    # NOTE: this is NOT the same value as supabase_service_role_key.
    supabase_jwt_secret: str = ""
    database_url: str = ""

    # ── AI / LLM ─────────────────────────────────────────────────
    gemini_api_key: str = ""
    hf_token: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # ── Document Processing ──────────────────────────────────────
    max_upload_size_mb: int = 50
    allowed_file_types: list[str] = ["pdf", "docx", "txt", "xlsx"]
    chunk_size: int = 512
    chunk_overlap: int = 50

    # ── RAG ──────────────────────────────────────────────────────
    top_k_results: int = 5
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384

    @property
    def max_upload_size_bytes(self) -> int:
        """Maximum upload size in bytes."""
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def cors_origins(self) -> list[str]:
        """Allowed CORS origins based on environment."""
        if self.is_development:
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        return [self.frontend_url]


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings (singleton)."""
    return Settings()
