"""
ForgeAI Security Utilities.

JWT validation, Supabase token verification, and security helpers.
"""

from datetime import datetime, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import Settings, get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Bearer token security scheme for OpenAPI docs
security_scheme = HTTPBearer(
    scheme_name="Supabase JWT",
    description="Supabase access token from authentication",
    auto_error=True,
)


def verify_supabase_token(
    token: str,
    settings: Settings,
) -> dict[str, Any]:
    """Verify a Supabase JWT and return the decoded payload.

    Args:
        token: The JWT access token from Supabase Auth.
        settings: Application settings containing Supabase config.

    Returns:
        Decoded JWT payload containing user information.

    Raises:
        HTTPException: If the token is invalid, expired, or malformed.
    """
    try:
        # Supabase user access tokens are signed with the project's JWT secret
        # (Supabase Dashboard > Project Settings > API > JWT Settings).
        # This is a distinct value from the service_role_key, which is itself
        # a JWT and cannot be used as an HMAC signing secret.
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )

        # Validate expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
            tz=timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        # Extract user ID
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )

        return payload

    except JWTError as e:
        logger.warning("JWT verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    settings: Settings = Depends(get_settings),
) -> str:
    """FastAPI dependency that extracts and validates the current user ID.

    Args:
        credentials: Bearer token from the Authorization header.
        settings: Application settings.

    Returns:
        The authenticated user's UUID as a string.
    """
    payload = verify_supabase_token(credentials.credentials, settings)
    user_id: str = payload["sub"]
    return user_id
