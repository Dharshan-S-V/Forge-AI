"""
ForgeAI Auth API Routes.

Handles user registration, login, logout, and profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.config import Settings, get_settings
from app.core.limiter import limiter
from app.core.logging import get_logger
from app.core.security import get_current_user_id
from app.db.supabase import get_supabase_admin_client
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserProfile,
)
from app.schemas.common import MessageResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    payload: RegisterRequest,
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    """Register a new user with Supabase Auth.

    Creates both a Supabase Auth user and a public.users profile row
    (the profile row is auto-created by the database trigger).
    """
    try:
        supabase = get_supabase_admin_client()
        result = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
                "options": {
                    "data": {
                        "full_name": payload.full_name,
                    }
                },
            }
        )

        if not result.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed. Please try again.",
            )

        if not result.session:
            # Email confirmation may be enabled — user created but no session
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration successful. Please check your email to confirm your account.",
            )

        logger.info("User registered", user_id=result.user.id, email=payload.email)

        return AuthResponse(
            access_token=result.session.access_token,
            refresh_token=result.session.refresh_token,
            token_type="bearer",
            expires_in=result.session.expires_in or 3600,
            user=UserProfile(
                id=str(result.user.id),
                email=result.user.email or payload.email,
                full_name=payload.full_name,
                avatar_url=None,
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}",
        ) from e


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login with email and password",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    payload: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    """Authenticate a user and return access tokens."""
    try:
        supabase = get_supabase_admin_client()
        result = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )

        if not result.user or not result.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Get user metadata for full_name
        user_meta = result.user.user_metadata or {}

        logger.info("User logged in", user_id=result.user.id)

        return AuthResponse(
            access_token=result.session.access_token,
            refresh_token=result.session.refresh_token,
            token_type="bearer",
            expires_in=result.session.expires_in or 3600,
            user=UserProfile(
                id=str(result.user.id),
                email=result.user.email or payload.email,
                full_name=user_meta.get("full_name"),
                avatar_url=user_meta.get("avatar_url"),
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from e


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout current user",
)
async def logout(
    user_id: str = Depends(get_current_user_id),
) -> MessageResponse:
    """Logout the current user (client should discard tokens)."""
    logger.info("User logged out", user_id=user_id)
    return MessageResponse(message="Logged out successfully")


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current user profile",
)
async def get_me(
    user_id: str = Depends(get_current_user_id),
    settings: Settings = Depends(get_settings),
) -> UserProfile:
    """Get the current authenticated user's profile."""
    try:
        supabase = get_supabase_admin_client()
        result = supabase.auth.admin.get_user_by_id(user_id)

        if not result.user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_meta = result.user.user_metadata or {}

        return UserProfile(
            id=str(result.user.id),
            email=result.user.email or "",
            full_name=user_meta.get("full_name"),
            avatar_url=user_meta.get("avatar_url"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get user profile", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile",
        ) from e
