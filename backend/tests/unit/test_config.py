"""
Regression tests for app.core.config.Settings.

Covers: SUPABASE_JWT_SECRET must exist as a distinct setting from
SUPABASE_SERVICE_ROLE_KEY (see security.py fix — using the service role
key to verify JWTs is a bug that silently rejects every valid token).
"""

from app.core.config import Settings


def test_supabase_jwt_secret_is_a_distinct_setting():
    """SUPABASE_JWT_SECRET must be configurable independently of the
    service role key. Regression guard for the JWT-verification bug where
    the service role key (itself a JWT) was mistakenly used as the HMAC
    signing secret.
    """
    settings = Settings(
        supabase_service_role_key="service-role-value",
        supabase_jwt_secret="jwt-secret-value",
    )
    assert settings.supabase_jwt_secret == "jwt-secret-value"
    assert settings.supabase_jwt_secret != settings.supabase_service_role_key


def test_supabase_jwt_secret_defaults_to_empty_string():
    """Should not raise if unset (matches other optional Supabase settings),
    but should be present as an attribute at all.
    """
    settings = Settings()
    assert hasattr(settings, "supabase_jwt_secret")
    assert settings.supabase_jwt_secret == ""
