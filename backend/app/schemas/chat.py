"""
ForgeAI Chat Schemas.

Pydantic models for chat session and message payloads.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class ChatMessageResponse(BaseSchema):
    """A single chat message."""

    id: UUID
    role: str
    content: str
    sources: list[dict] = []
    created_at: datetime


class ChatSessionResponse(BaseSchema):
    """Chat session metadata."""

    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatSessionDetailResponse(ChatSessionResponse):
    """Chat session with messages."""

    messages: list[ChatMessageResponse] = []


class ChatSessionListResponse(BaseModel):
    """List of chat sessions."""

    sessions: list[ChatSessionResponse]
    total: int


class CreateSessionRequest(BaseModel):
    """Create a new chat session."""

    title: str = Field(default="New Chat", max_length=255)


class SendMessageRequest(BaseModel):
    """Send a message in a chat session."""

    content: str = Field(..., min_length=1, max_length=4096)


class SendMessageResponse(BaseModel):
    """Response after sending a message (includes AI reply)."""

    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
