# =============================================================================
# Marketing Assistant AI - Embedding Service (Cohere Version)
# =============================================================================
# This module provides text embedding functionality using Cohere.
#
# REQUIRES COHERE API KEY
# =============================================================================

import logging
from typing import List, Optional

import cohere

from backend.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using Cohere.
    
    Cohere provides high-quality embeddings via API.
    
    Attributes:
        client: Cohere API client
        model_name: Embedding model name
        dimension: Output vector dimension
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the embedding service.
        
        Args:
            model_name: Cohere embedding model. If None, uses settings.
        """
        self.api_key = settings.cohere_api_key
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required for embeddings")
        
        self.model_name = model_name or settings.cohere_embed_model
        self.dimension = settings.embedding_dimension
        self.client = cohere.Client(self.api_key)
        
        logger.info(f"Using Cohere embedding model: {self.model_name}")
    
    def _check_dimension(self, embedding: List[float]) -> None:
        """Update configured dimension if it doesn't match the API response."""
        actual_dim = len(embedding)
        if actual_dim != self.dimension:
            logger.warning(
                f"Cohere embedding dimension ({actual_dim}) doesn't match config "
                f"({self.dimension}). Using actual dimension: {actual_dim}"
            )
            self.dimension = actual_dim
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batch."""
        if not texts:
            raise ValueError("texts list cannot be empty")
        
        try:
            logger.debug(f"Generating embeddings for {len(texts)} texts")
            response = self.client.embed(
                texts=texts,
                model=self.model_name,
                input_type="search_document"
            )
            
            embeddings = response.embeddings
            if embeddings:
                self._check_dimension(embeddings[0])
            
            return [list(embedding) for embedding in embeddings]
        
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate embeddings: {e}")
    
    async def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a search query."""
        if not query:
            raise ValueError("query cannot be empty")
        
        try:
            response = self.client.embed(
                texts=[query],
                model=self.model_name,
                input_type="search_query"
            )
            embedding = response.embeddings[0]
            self._check_dimension(embedding)
            return list(embedding)
        
        except Exception as e:
            logger.error(f"Query embedding failed: {e}")
            raise RuntimeError(f"Failed to embed search query: {e}")
    
    async def embed_document(self, document: str) -> List[float]:
        """Generate embedding for a document to be indexed."""
        return await self.embed_text(document)


# =============================================================================
# Module-level singleton
# =============================================================================

_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the singleton embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
