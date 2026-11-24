"""
ForgeAI Chat Service.

Orchestrates RAG retrieval, LLM generation, and conversation history.
"""

import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.rag.agent import RagAgent
from app.ai.rag.retriever import VectorRetriever
from app.core.logging import get_logger
from app.db.repositories.chat_repo import ChatRepository
from app.models.chat import ChatSession, ChatMessage

logger = get_logger(__name__)


class ChatService:
    """Service orchestrating chat and RAG operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ChatRepository(session)
        self.retriever = VectorRetriever(session)
        self.agent = RagAgent()

    async def create_chat(self, user_id: uuid.UUID, title: str) -> ChatSession:
        """Create a new chat session."""
        return await self.repo.create_chat(user_id, title)

    async def get_user_chats(self, user_id: uuid.UUID) -> list[ChatSession]:
        """Get all chats for a user."""
        return await self.repo.get_chats_by_user(user_id)

    async def get_chat_history(self, user_id: uuid.UUID, chat_id: uuid.UUID) -> ChatSession:
        """Get chat history with validation."""
        chat = await self.repo.get_chat_with_messages(chat_id, user_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    async def process_message(self, user_id: uuid.UUID, chat_id: uuid.UUID, query: str) -> ChatMessage:
        """Process a user message through the RAG pipeline.

        1. Save user message.
        2. Retrieve relevant context.
        3. Generate answer.
        4. Save AI response with sources.
        """
        # Ensure chat exists and belongs to user
        chat = await self.get_chat_history(user_id, chat_id)

        # 1. Save user message
        await self.repo.add_message(chat_id, "user", query)

        # 2. Retrieve context
        context_chunks = await self.retriever.search(user_id, query)

        # Build chat history for context (exclude the message we just added)
        chat_history = [{"role": msg.role, "content": msg.content} for msg in chat.messages]

        # 3. Generate answer
        answer, sources = await self.agent.generate_answer(query, context_chunks, chat_history)

        # 4. Save AI response
        ai_message = await self.repo.add_message(chat_id, "assistant", answer, sources)
        
        return ai_message
