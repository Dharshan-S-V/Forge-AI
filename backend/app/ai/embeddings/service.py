"""
ForgeAI Embedding Service.

Generates vector embeddings for text chunks using Sentence Transformers.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache()
def get_embedding_model() -> SentenceTransformer:
    """Get or load the SentenceTransformer model (cached)."""
    settings = get_settings()
    logger.info(f"Loading embedding model: {settings.embedding_model}")
    # Initialize the model. This downloads the model on first run.
    return SentenceTransformer(settings.embedding_model)


class EmbeddingService:
    """Service for generating text embeddings."""

    @classmethod
    def generate_embeddings(cls, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a list of texts.

        Args:
            texts: List of text chunks.

        Returns:
            List of embedding vectors (lists of floats).
        """
        if not texts:
            return []

        logger.info("Generating embeddings", num_texts=len(texts))
        
        model = get_embedding_model()
        
        # Output is a numpy array, convert to standard Python lists
        embeddings = model.encode(texts, show_progress_bar=False)
        
        # Convert numpy floats to native python floats for JSON serializability / DB insertion
        return [embedding.tolist() for embedding in embeddings]
