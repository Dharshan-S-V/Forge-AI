"""
ForgeAI Auth Schemas.

Pydantic models for authentication request/response payloads.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255)


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class AuthResponse(BaseModel):
    """Authentication response with tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserProfile"


class UserProfile(BaseModel):
    """User profile information."""

    id: str
    email: str
    full_name: str | None = None
    avatar_url: str | None = None


# Resolve forward reference
AuthResponse.model_rebuild()
