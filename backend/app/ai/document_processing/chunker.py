"""
ForgeAI Document Chunker.

Splits large text into smaller semantic chunks for embedding.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class DocumentChunker:
    """Splits text into chunks using LangChain's recursive splitter."""

    @classmethod
    def chunk_text(cls, text: str) -> list[str]:
        """Split text into semantic chunks.

        Args:
            text: The full plain text of the document.

        Returns:
            A list of text chunks.
        """
        settings = get_settings()
        
        logger.info(
            "Chunking text", 
            chunk_size=settings.chunk_size, 
            chunk_overlap=settings.chunk_overlap
        )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
            is_separator_regex=False,
        )

        chunks = splitter.split_text(text)
        logger.info("Text chunked successfully", num_chunks=len(chunks))
        
        return chunks
