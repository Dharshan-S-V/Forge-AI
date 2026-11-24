"""
ForgeAI Document Repository.

Handles database operations for Documents and DocumentChunks.
"""

import uuid
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.schemas.document import DocumentUploadResponse


class DocumentRepository:
    """Repository for document database operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create_document(
        self,
        user_id: uuid.UUID,
        filename: str,
        original_filename: str,
        file_type: str,
        file_size: int,
        storage_path: str,
    ) -> Document:
        """Create a new document record."""
        document = Document(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            file_type=file_type,
            file_size=file_size,
            storage_path=storage_path,
            status="uploaded",
        )
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def get_by_user(self, user_id: uuid.UUID) -> Sequence[Document]:
        """Get all documents for a specific user."""
        stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, document_id: uuid.UUID) -> Document | None:
        """Get document by ID."""
        return await self.session.get(Document, document_id)

    async def delete(self, document_id: uuid.UUID) -> bool:
        """Delete a document."""
        stmt = delete(Document).where(Document.id == document_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
