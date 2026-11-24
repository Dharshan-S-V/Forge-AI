"""
ForgeAI Common Schemas.

Shared Pydantic models used across the application.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
    environment: str


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
    detail: str | None = None


class ErrorResponse(BaseModel):
    """Error response with details."""

    error: str
    detail: str | None = None
    status_code: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: list[T]
    total: int
    page: int
    page_size: int
    has_more: bool


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""

    created_at: datetime
    updated_at: datetime


class IDSchema(BaseSchema):
    """Schema with UUID id field."""

    id: UUID
