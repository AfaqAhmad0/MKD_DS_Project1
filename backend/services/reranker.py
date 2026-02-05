# =============================================================================
# Marketing Assistant AI - Re-ranking Service (Cohere Version)
# =============================================================================
# This module provides semantic re-ranking using Cohere.
#
# REQUIRES COHERE API KEY
# =============================================================================

import logging
from typing import List, Optional

import cohere

from backend.config import settings
from backend.models.schemas import RetrievedContent

# Configure logging
logger = logging.getLogger(__name__)


class RerankerService:
    """
    Service for re-ranking search results using Cohere.
    
    Cohere's rerank endpoint provides high-quality relevance scores.
    
    Attributes:
        client: Cohere API client
        model_name: Rerank model name
        top_n: Default number of results to return
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the re-ranking service."""
        self.api_key = settings.cohere_api_key
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required for re-ranking")
        
        self.model_name = model_name or settings.cohere_rerank_model
        self.top_n = settings.rerank_top_n
        self.client = cohere.Client(self.api_key)
        
        logger.info(f"Using Cohere rerank model: {self.model_name}")
    
    async def rerank(
        self,
        query: str,
        results: List[RetrievedContent],
        top_n: Optional[int] = None
    ) -> List[RetrievedContent]:
        """Re-rank search results for improved relevance."""
        if not results:
            logger.debug("No results to re-rank")
            return []
        
        top_n = top_n or self.top_n
        
        try:
            documents = [
                f"{r.content.title}\n\n{r.content.content}"
                for r in results
            ]
            
            logger.debug(f"Re-ranking {len(documents)} documents with Cohere")
            response = self.client.rerank(
                model=self.model_name,
                query=query,
                documents=documents,
                top_n=top_n
            )
            
            reranked_results = []
            for r in response.results:
                original = results[r.index]
                reranked_results.append(
                    RetrievedContent(
                        content=original.content,
                        similarity_score=original.similarity_score,
                        rerank_score=float(r.relevance_score)
                    )
                )
            
            return reranked_results
        
        except Exception as e:
            logger.error(f"Re-ranking failed: {e}")
            logger.warning("Falling back to original result order")
            return results[:top_n]
    
    async def rerank_with_scores(
        self,
        query: str,
        texts: List[str],
        top_n: Optional[int] = None
    ) -> List[dict]:
        """Re-rank arbitrary texts and return scores."""
        if not texts:
            return []
        
        top_n = top_n or self.top_n
        
        try:
            response = self.client.rerank(
                model=self.model_name,
                query=query,
                documents=texts,
                top_n=top_n
            )
            
            results = []
            for r in response.results:
                results.append(
                    {"text": texts[r.index], "index": r.index, "score": float(r.relevance_score)}
                )
            
            return results
        
        except Exception as e:
            logger.error(f"Re-ranking failed: {e}")
            return [{"text": t, "index": i, "score": 0.0} for i, t in enumerate(texts[:top_n])]


# =============================================================================
# Module-level singleton
# =============================================================================

_reranker_service: Optional[RerankerService] = None


def get_reranker_service() -> RerankerService:
    """Get or create the singleton re-ranker service instance."""
    global _reranker_service
    if _reranker_service is None:
        _reranker_service = RerankerService()
    return _reranker_service
