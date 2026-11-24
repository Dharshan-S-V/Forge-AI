"""
Regression tests for app.core.security.verify_supabase_token.

Covers Issue #2: verification must use settings.supabase_jwt_secret,
NOT settings.supabase_service_role_key (a JWT is not a valid HMAC key).
"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import jwt

from app.core.config import Settings
from app.core.security import verify_supabase_token

JWT_SECRET = "test-jwt-secret"
SERVICE_ROLE_KEY = "not-the-jwt-secret"


def _make_settings() -> Settings:
    return Settings(
        supabase_jwt_secret=JWT_SECRET,
        supabase_service_role_key=SERVICE_ROLE_KEY,
    )


def _make_token(secret: str, sub: str = "user-123", expired: bool = False) -> str:
    exp = datetime.now(timezone.utc) + (
        timedelta(minutes=-5) if expired else timedelta(hours=1)
    )
    return jwt.encode(
        {"sub": sub, "aud": "authenticated", "exp": exp},
        secret,
        algorithm="HS256",
    )


def test_verify_supabase_token_accepts_token_signed_with_jwt_secret():
    """A token signed with the real JWT secret must verify successfully."""
    settings = _make_settings()
    token = _make_token(JWT_SECRET)

    payload = verify_supabase_token(token, settings)

    assert payload["sub"] == "user-123"


def test_verify_supabase_token_rejects_token_if_checked_against_service_role_key():
    """Regression guard: a token signed with the JWT secret must NOT verify
    against the service_role_key. This is the exact bug that was fixed —
    if this test ever passes with SERVICE_ROLE_KEY, the bug has returned.
    """
    token = _make_token(JWT_SECRET)

    broken_settings = Settings(
        supabase_jwt_secret=SERVICE_ROLE_KEY,  # simulates the old, wrong wiring
        supabase_service_role_key=SERVICE_ROLE_KEY,
    )

    with pytest.raises(HTTPException) as exc_info:
        verify_supabase_token(token, broken_settings)
    assert exc_info.value.status_code == 401


def test_verify_supabase_token_rejects_expired_token():
    settings = _make_settings()
    token = _make_token(JWT_SECRET, expired=True)

    with pytest.raises(HTTPException) as exc_info:
        verify_supabase_token(token, settings)
    assert exc_info.value.status_code == 401
