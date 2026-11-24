"""
ForgeAI Document Processing Pipeline.

Orchestrates the loading, chunking, embedding, and saving of documents.
"""

import asyncio
import uuid
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.document_processing.chunker import DocumentChunker
from app.ai.document_processing.loader import DocumentLoader
from app.ai.embeddings.service import EmbeddingService
from app.core.logging import get_logger
from app.db.supabase import get_supabase_admin_client
from app.models.document import Document, DocumentChunk

logger = get_logger(__name__)


class DocumentPipeline:
    """End-to-end pipeline for processing documents."""

    @classmethod
    async def process_document(
        cls,
        db_session: AsyncSession,
        document_id: uuid.UUID,
        file_bytes: bytes,
        file_type: str,
    ) -> None:
        """Process a document in the background.

        1. Extract text
        2. Chunk text
        3. Generate embeddings
        4. Save chunks to database
        5. Update document status

        Args:
            db_session: Database session.
            document_id: The UUID of the document record.
            file_bytes: The raw file bytes.
            file_type: The file extension.
        """
        logger.info("Starting document processing pipeline", document_id=str(document_id))

        try:
            # Update status to processing
            await cls._update_status(db_session, document_id, "processing")

            # 1. Load / Extract text
            # DocumentLoader (PyMuPDF/python-docx/openpyxl) and EmbeddingService
            # (sentence-transformers) are CPU-bound and synchronous; run them in
            # worker threads so they don't block the event loop for the whole
            # process (this task still runs on the app's shared event loop).
            text = await asyncio.to_thread(DocumentLoader.load, file_bytes, file_type)
            if not text.strip():
                raise ValueError("No text could be extracted from the document.")

            # 2. Chunk text
            chunks = DocumentChunker.chunk_text(text)
            if not chunks:
                raise ValueError("Document yielded no text chunks.")

            # 3. Generate embeddings
            embeddings = await asyncio.to_thread(EmbeddingService.generate_embeddings, chunks)

            # 4. Save chunks to database
            db_chunks = []
            for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                db_chunk = DocumentChunk(
                    document_id=document_id,
                    chunk_index=i,
                    content=chunk_text,
                    embedding=embedding,
                    doc_metadata={"source": "document_pipeline", "index": i},
                )
                db_chunks.append(db_chunk)

            db_session.add_all(db_chunks)
            await db_session.commit()

            # 5. Update document status to completed
            await cls._update_status(
                db_session, 
                document_id, 
                "completed", 
                chunk_count=len(chunks)
            )

            logger.info(
                "Document processing pipeline completed successfully",
                document_id=str(document_id),
                chunk_count=len(chunks),
            )

        except Exception as e:
            logger.error(
                "Document processing pipeline failed",
                document_id=str(document_id),
                error=str(e),
            )
            # Update status to failed
            await cls._update_status(
                db_session, 
                document_id, 
                "failed", 
                error=str(e)
            )

    @staticmethod
    async def _update_status(
        db_session: AsyncSession,
        document_id: uuid.UUID,
        status: str,
        chunk_count: int = 0,
        error: str | None = None,
    ) -> None:
        """Helper to update document status in the database."""
        stmt = (
            update(Document)
            .where(Document.id == document_id)
            .values(
                status=status,
                chunk_count=chunk_count,
                processing_error=error,
            )
        )
        await db_session.execute(stmt)
        await db_session.commit()
