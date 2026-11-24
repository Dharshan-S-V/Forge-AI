"""
ForgeAI Test Configuration.

Shared fixtures for unit and integration tests.
"""

import pytest


@pytest.fixture
def app_settings():
    """Override settings for testing."""
    from app.core.config import Settings

    return Settings(
        environment="development",
        supabase_url="http://localhost:54321",
        supabase_anon_key="test-anon-key",
        supabase_service_role_key="test-service-role-key",
        database_url="postgresql://test:test@localhost:5432/test_forgeai",
        gemini_api_key="test-gemini-key",
    )
