"""
ForgeAI Chat Repository.

Handles database operations for Chats and Messages.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat import ChatSession, ChatMessage


class ChatRepository:
    """Repository for chat database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, user_id: uuid.UUID, title: str) -> ChatSession:
        """Create a new chat session."""
        chat = ChatSession(user_id=user_id, title=title)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def get_chats_by_user(self, user_id: uuid.UUID) -> Sequence[ChatSession]:
        """Get all chats for a user."""
        stmt = select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_chat_with_messages(self, chat_id: uuid.UUID, user_id: uuid.UUID) -> ChatSession | None:
        """Get a specific chat with its messages."""
        stmt = (
            select(ChatSession)
            .where(ChatSession.id == chat_id, ChatSession.user_id == user_id)
            .options(selectinload(ChatSession.messages))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_message(
        self, 
        chat_id: uuid.UUID, 
        role: str, 
        content: str, 
        sources: list[dict] | None = None
    ) -> ChatMessage:
        """Add a message to a chat."""
        message = ChatMessage(
            session_id=chat_id,
            role=role,
            content=content,
            sources=sources or []
        )
        self.session.add(message)
        
        # Update chat updated_at
        chat = await self.session.get(ChatSession, chat_id)
        if chat:
            chat.updated_at = message.created_at
            
        await self.session.commit()
        await self.session.refresh(message)
        return message
