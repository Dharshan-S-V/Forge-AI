"""
ForgeAI Chat API Routes.

Endpoints for managing chats and sending messages.
"""

import uuid

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db
from app.core.limiter import limiter
from app.schemas.chat import (
    ChatMessageResponse,
    ChatSessionDetailResponse,
    ChatSessionResponse,
    CreateSessionRequest,
    SendMessageRequest,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chats", tags=["Chat"])


@router.post(
    "",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat",
)
async def create_chat(
    req: CreateSessionRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new chat session."""
    service = ChatService(db)
    chat = await service.create_chat(uuid.UUID(user_id), req.title)
    return chat


@router.get(
    "",
    response_model=list[ChatSessionResponse],
    summary="List all chats",
)
async def list_chats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all chats for the current user."""
    service = ChatService(db)
    return await service.get_user_chats(uuid.UUID(user_id))


@router.get(
    "/{chat_id}",
    response_model=ChatSessionDetailResponse,
    summary="Get chat history",
)
async def get_chat(
    chat_id: uuid.UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history with messages."""
    service = ChatService(db)
    return await service.get_chat_history(uuid.UUID(user_id), chat_id)


@router.post(
    "/{chat_id}/messages",
    response_model=ChatMessageResponse,
    summary="Send a message",
)
@limiter.limit("20/minute")
async def send_message(
    request: Request,
    chat_id: uuid.UUID,
    req: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to a chat and get the AI response."""
    service = ChatService(db)
    # The service automatically saves the user message and generates/saves the AI response
    ai_msg = await service.process_message(uuid.UUID(user_id), chat_id, req.content)
    return ai_msg
