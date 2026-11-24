"""
ForgeAI Document Service.

Orchestrates document uploads, validation, storage, and database persistence.
"""

import uuid
from typing import Sequence
import asyncio

from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.repositories.document_repo import DocumentRepository
from app.db.session import async_session_factory
from app.models.document import Document
from app.services.storage_service import StorageService
from app.ai.rag.pipeline import DocumentPipeline

logger = get_logger(__name__)


class DocumentService:
    """Service orchestrating document operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session
        self.repo = DocumentRepository(session)
        self.settings = get_settings()

    async def upload_document(
        self, 
        user_id: uuid.UUID, 
        file: UploadFile,
        background_tasks: BackgroundTasks
    ) -> Document:
        """Validate, upload to storage, save metadata, and trigger background processing."""
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename missing")

        # Extract extension and validate
        ext = file.filename.split(".")[-1].lower()
        if ext not in self.settings.allowed_file_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {ext}. Allowed: {', '.join(self.settings.allowed_file_types)}"
            )

        # Read file and check size
        file_bytes = await file.read()
        file_size = len(file_bytes)
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        if file_size > self.settings.max_upload_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size ({self.settings.max_upload_size_mb}MB)"
            )

        # Sanitize filename: strip anything that isn't alphanumeric or in
        # "._- " (this also strips "/" and "\", which is what actually
        # prevents path traversal in the storage_path built below).
        safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ").strip()
        if not safe_filename:
            # Degenerate case: filename was entirely unicode/symbols (e.g. an
            # emoji-only name) and sanitized down to nothing. Fall back to a
            # generated name using the already-validated extension so the
            # storage path is never malformed.
            safe_filename = f"upload.{ext}"

        try:
            # Upload to Supabase Storage.
            # StorageService uses the synchronous supabase-py client, so run it
            # in a worker thread to avoid blocking the event loop.
            storage_path = await asyncio.to_thread(
                StorageService.upload_file,
                user_id,
                file_bytes,
                safe_filename,
            )

            # Save metadata to Database
            document = await self.repo.create_document(
                user_id=user_id,
                filename=safe_filename,
                original_filename=file.filename,
                file_type=ext,
                file_size=file_size,
                storage_path=storage_path,
            )
            
            logger.info("Document metadata saved", document_id=document.id)

            # Trigger background processing
            # We must pass the raw file bytes to avoid re-downloading from Supabase,
            # but we need a fresh DB session for the background task to avoid session conflicts.
            background_tasks.add_task(
                self._run_pipeline_in_background,
                document.id,
                file_bytes,
                ext,
            )

            return document

        except Exception as e:
            logger.error("Failed to process document upload", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document"
            ) from e

    async def _run_pipeline_in_background(
        self, 
        document_id: uuid.UUID, 
        file_bytes: bytes, 
        file_type: str
    ) -> None:
        """Wrapper to run the pipeline with a fresh database session."""
        async with async_session_factory() as bg_session:
            await DocumentPipeline.process_document(
                db_session=bg_session,
                document_id=document_id,
                file_bytes=file_bytes,
                file_type=file_type,
            )

    async def get_user_documents(self, user_id: uuid.UUID) -> Sequence[Document]:
        """Get all documents for a user."""
        return await self.repo.get_by_user(user_id)

    async def delete_document(self, user_id: uuid.UUID, document_id: uuid.UUID) -> None:
        """Delete a document and its storage file."""
        document = await self.repo.get_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if document.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this document")

        try:
            await asyncio.to_thread(StorageService.delete_file, document.storage_path)
        except Exception as e:
            logger.warning("Failed to delete file from storage, but continuing DB deletion", error=str(e))

        deleted = await self.repo.delete(document_id)
        if not deleted:
            raise HTTPException(status_code=500, detail="Failed to delete document metadata")
