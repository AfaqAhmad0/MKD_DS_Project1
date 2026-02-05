# =============================================================================
# Marketing Assistant AI - Vector Store Service
# =============================================================================
# This module implements the FAISS-based vector store for semantic search.
# =============================================================================

import json
import logging
import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

import faiss
import numpy as np

from backend.config import settings
from backend.models.schemas import MarketingContent, ContentType, RetrievedContent
from backend.services.embeddings import EmbeddingService, get_embedding_service

# Configure logging
logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    FAISS-based vector store for marketing content retrieval.
    """
    INDEX_FILENAME = "faiss.index"
    METADATA_FILENAME = "metadata.pkl"
    
    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        store_path: Optional[str] = None
    ):
        self.embedding_service = embedding_service or get_embedding_service()
        self.store_path = Path(store_path or settings.vector_store_path)
        self.dimension = settings.embedding_dimension
        
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: Dict[str, MarketingContent] = {}
        self.id_to_idx: Dict[str, int] = {}
        self.idx_to_id: Dict[int, str] = {}
        
        self._ensure_store_directory()
        self._initialize_index()
        
        logger.info(
            f"VectorStoreService initialized. "
            f"Index contains {self.index.ntotal if self.index else 0} vectors."
        )
    
    def _ensure_store_directory(self) -> None:
        self.store_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Storage directory ensured at: {self.store_path}")
    
    def _initialize_index(self) -> None:
        index_path = self.store_path / self.INDEX_FILENAME
        metadata_path = self.store_path / self.METADATA_FILENAME
        
        if index_path.exists() and metadata_path.exists():
            try:
                self.index = faiss.read_index(str(index_path))
                with open(metadata_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.metadata = saved_data['metadata']
                    self.id_to_idx = saved_data['id_to_idx']
                    self.idx_to_id = saved_data['idx_to_id']
                
                if self.index.d != self.dimension:
                    logger.warning(
                        f"Index dimension ({self.index.d}) doesn't match config "
                        f"({self.dimension}). Rebuilding index."
                    )
                    self._invalidate_embeddings()
                    self._create_new_index()
                else:
                    logger.info(f"Loaded existing index with {self.index.ntotal} vectors")
            except Exception as e:
                logger.warning(f"Failed to load existing index: {e}. Creating new one.")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = {}
        self.id_to_idx = {}
        self.idx_to_id = {}
        
        logger.info(f"Created new FAISS index with dimension {self.dimension}")

    def _invalidate_embeddings(self) -> None:
        for content in self.metadata.values():
            content.embedding = None
        self.id_to_idx = {}
        self.idx_to_id = {}
        logger.warning("Cleared stored embeddings due to dimension mismatch.")
    
    def save(self) -> None:
        if self.index is None:
            logger.warning("No index to save")
            return
        
        try:
            index_path = self.store_path / self.INDEX_FILENAME
            metadata_path = self.store_path / self.METADATA_FILENAME
            
            faiss.write_index(self.index, str(index_path))
            with open(metadata_path, 'wb') as f:
                pickle.dump({
                    'metadata': self.metadata,
                    'id_to_idx': self.id_to_idx,
                    'idx_to_id': self.idx_to_id
                }, f)
            
            logger.info(f"Saved index with {self.index.ntotal} vectors to {self.store_path}")
        
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise RuntimeError(f"Failed to save vector store: {e}")
    
    async def add_content(self, content: MarketingContent) -> MarketingContent:
        if content.id is None:
            content.id = uuid4()
        
        text_to_embed = f"{content.title}\n\n{content.content}"
        
        try:
            embedding = await self.embedding_service.embed_document(text_to_embed)
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Failed to embed content: {e}")
        
        content.embedding = embedding
        embedding_array = np.array([embedding], dtype=np.float32)
        faiss.normalize_L2(embedding_array)
        
        idx = self.index.ntotal
        self.index.add(embedding_array)
        
        content_id = str(content.id)
        self.id_to_idx[content_id] = idx
        self.idx_to_id[idx] = content_id
        self.metadata[content_id] = content
        
        self.save()
        
        logger.info(f"Added content '{content.title}' with ID {content.id}")
        return content
    
    async def search(
        self,
        query: str,
        k: int = 10,
        content_type: Optional[ContentType] = None
    ) -> List[RetrievedContent]:
        if self.index is None or self.index.ntotal == 0:
            logger.warning("Search called on empty index")
            return []
        
        try:
            query_embedding = await self.embedding_service.embed_query(query)
        except Exception as e:
            logger.error(f"Failed to embed query: {e}")
            raise RuntimeError(f"Failed to embed search query: {e}")
        
        query_array = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_array)
        
        search_k = min(k * 3, self.index.ntotal)
        distances, indices = self.index.search(query_array, search_k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            content_id = self.idx_to_id.get(int(idx))
            if content_id is None:
                continue
            content = self.metadata.get(content_id)
            if content is None:
                continue
            if content_type and content.content_type != content_type:
                continue
            
            similarity = float(max(0, min(1, distance)))
            results.append(RetrievedContent(
                content=content,
                similarity_score=similarity
            ))
            
            if len(results) >= k:
                break
        
        logger.debug(f"Search returned {len(results)} results for query: {query[:50]}...")
        return results
    
    async def get_content(self, content_id: UUID) -> Optional[MarketingContent]:
        return self.metadata.get(str(content_id))
    
    async def update_content(
        self,
        content_id: UUID,
        updates: dict
    ) -> Optional[MarketingContent]:
        content_id_str = str(content_id)
        if content_id_str not in self.metadata:
            logger.warning(f"Content not found for update: {content_id}")
            return None
        
        content = self.metadata[content_id_str]
        
        needs_reembedding = (
            'content' in updates and updates['content'] != content.content or
            'title' in updates and updates['title'] != content.title
        )
        
        for key, value in updates.items():
            if hasattr(content, key) and value is not None:
                setattr(content, key, value)
        
        content.updated_at = datetime.utcnow()
        
        if needs_reembedding:
            text_to_embed = f"{content.title}\n\n{content.content}"
            new_embedding = await self.embedding_service.embed_document(text_to_embed)
            content.embedding = new_embedding
            
            embedding_array = np.array([new_embedding], dtype=np.float32)
            faiss.normalize_L2(embedding_array)
            await self._rebuild_index()
        
        self.save()
        logger.info(f"Updated content: {content_id}")
        return content
    
    async def delete_content(self, content_id: UUID) -> bool:
        content_id_str = str(content_id)
        if content_id_str not in self.metadata:
            logger.warning(f"Content not found for deletion: {content_id}")
            return False
        
        del self.metadata[content_id_str]
        idx = self.id_to_idx.pop(content_id_str, None)
        if idx is not None:
            self.idx_to_id.pop(idx, None)
        
        await self._rebuild_index()
        self.save()
        logger.info(f"Deleted content: {content_id}")
        return True
    
    async def _rebuild_index(self) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        self.id_to_idx = {}
        self.idx_to_id = {}
        
        for idx, (content_id, content) in enumerate(self.metadata.items()):
            if content.embedding:
                embedding_array = np.array([content.embedding], dtype=np.float32)
                faiss.normalize_L2(embedding_array)
                self.index.add(embedding_array)
                
                self.id_to_idx[content_id] = idx
                self.idx_to_id[idx] = content_id
        
        logger.info(f"Rebuilt index with {self.index.ntotal} vectors")
    
    async def list_content(
        self,
        content_type: Optional[ContentType] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[MarketingContent], int]:
        filtered = [
            content for content in self.metadata.values()
            if content_type is None or content.content_type == content_type
        ]
        
        filtered.sort(key=lambda x: x.created_at, reverse=True)
        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = filtered[start:end]
        
        return paginated, total
    
    def get_stats(self) -> dict:
        type_counts = {}
        for content in self.metadata.values():
            type_name = content.content_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_documents": len(self.metadata),
            "index_size": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "content_type_counts": type_counts,
            "store_path": str(self.store_path)
        }


# =============================================================================
# Module-level singleton
# =============================================================================

_vector_store: Optional[VectorStoreService] = None


def get_vector_store() -> VectorStoreService:
    """Get or create the singleton vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStoreService()
    return _vector_store
