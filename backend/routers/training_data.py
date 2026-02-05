# =============================================================================
# Marketing Assistant AI - Training Data Router
# =============================================================================

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    MarketingContent,
    TrainingDataCreate,
    TrainingDataUpdate,
    TrainingDataResponse,
    TrainingDataListResponse,
    ContentType
)
from backend.services.vector_store import get_vector_store
from backend.services.local_storage import save_campaign_content
from backend.data.samples import SAMPLE_MARKETING_CONTENT

# Configure logging
logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/v1/training-data",
    tags=["Training Data"],
    responses={
        404: {"description": "Training data not found"},
        500: {"description": "Internal server error"}
    }
)


@router.post(
    "",
    response_model=TrainingDataResponse,
    status_code=201,
    summary="Add Training Data",
    description="""
    Add new marketing content to the training data.
    """
)
async def create_training_data(data: TrainingDataCreate) -> TrainingDataResponse:
    """Create a new training data entry."""
    try:
        logger.info(f"Creating training data: {data.title}")
        
        vector_store = get_vector_store()
        
        content = MarketingContent(
            title=data.title,
            content=data.content,
            content_type=data.content_type,
            metadata=data.metadata,
            tags=data.tags
        )
        
        added = await vector_store.add_content(content)
        
        try:
            save_campaign_content(added)
        except Exception as storage_error:
            logger.warning(f"Failed to store campaign content: {storage_error}")
        
        logger.info(f"Training data created with ID: {added.id}")
        
        return TrainingDataResponse(
            id=added.id,
            title=added.title,
            content=added.content,
            content_type=added.content_type,
            metadata=added.metadata,
            tags=added.tags,
            created_at=added.created_at,
            updated_at=added.updated_at
        )
    
    except Exception as e:
        logger.error(f"Failed to create training data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create training data: {str(e)}"
        )


@router.get(
    "",
    response_model=TrainingDataListResponse,
    summary="List Training Data",
    description="List all training data with optional filtering and pagination."
)
async def list_training_data(
    content_type: Optional[ContentType] = Query(
        default=None,
        description="Filter by content type"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
) -> TrainingDataListResponse:
    """List all training data with pagination."""
    try:
        vector_store = get_vector_store()
        items, total = await vector_store.list_content(
            content_type=content_type,
            page=page,
            page_size=page_size
        )
        
        return TrainingDataListResponse(
            items=[TrainingDataResponse(**item.model_dump()) for item in items],
            total=total,
            page=page,
            page_size=page_size
        )
    
    except Exception as e:
        logger.error(f"Failed to list training data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list training data: {str(e)}"
        )


@router.get(
    "/stats",
    summary="Get Training Data Statistics",
    description="Get statistics about the training data and vector store."
)
async def get_stats() -> dict:
    """Get vector store statistics."""
    try:
        vector_store = get_vector_store()
        return vector_store.get_stats()
    
    except Exception as e:
        logger.error(f"Failed to get stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.get(
    "/{training_data_id}",
    response_model=TrainingDataResponse,
    summary="Get Training Data by ID",
    description="Retrieve a specific training data entry by its ID."
)
async def get_training_data(training_data_id: UUID) -> TrainingDataResponse:
    """Get a training data entry by ID."""
    vector_store = get_vector_store()
    content = await vector_store.get_content(training_data_id)
    
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Training data not found: {training_data_id}"
        )
    
    return TrainingDataResponse(**content.model_dump())


@router.put(
    "/{training_data_id}",
    response_model=TrainingDataResponse,
    summary="Update Training Data",
    description="Update an existing training data entry."
)
async def update_training_data(
    training_data_id: UUID,
    data: TrainingDataUpdate
) -> TrainingDataResponse:
    """Update a training data entry."""
    try:
        vector_store = get_vector_store()
        
        updates = {}
        if data.title is not None:
            updates["title"] = data.title
        if data.content is not None:
            updates["content"] = data.content
        if data.content_type is not None:
            updates["content_type"] = data.content_type
        if data.metadata is not None:
            updates["metadata"] = data.metadata
        if data.tags is not None:
            updates["tags"] = data.tags
        
        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No fields to update"
            )
        
        updated = await vector_store.update_content(training_data_id, updates)
        
        if updated is None:
            raise HTTPException(
                status_code=404,
                detail=f"Training data not found: {training_data_id}"
            )
        
        logger.info(f"Training data updated: {training_data_id}")
        
        try:
            save_campaign_content(updated)
        except Exception as storage_error:
            logger.warning(f"Failed to store campaign content: {storage_error}")
        
        return TrainingDataResponse(
            id=updated.id,
            title=updated.title,
            content=updated.content,
            content_type=updated.content_type,
            metadata=updated.metadata,
            tags=updated.tags,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update training data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update training data: {str(e)}"
        )


@router.delete(
    "/{training_data_id}",
    status_code=204,
    summary="Delete Training Data",
    description="Delete a training data entry by ID."
)
async def delete_training_data(training_data_id: UUID) -> None:
    """Delete a training data entry."""
    try:
        vector_store = get_vector_store()
        deleted = await vector_store.delete_content(training_data_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Training data not found: {training_data_id}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete training data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete training data: {str(e)}"
        )


@router.post(
    "/seed",
    summary="Seed Sample Data",
    description="Seed the vector store with sample marketing content."
)
async def seed_sample_data() -> dict:
    """Seed the vector store with sample data."""
    try:
        vector_store = get_vector_store()
        
        added_count = 0
        errors = []
        
        for sample in SAMPLE_MARKETING_CONTENT:
            try:
                content = MarketingContent(**sample)
                await vector_store.add_content(content)
                added_count += 1
            except Exception as e:
                errors.append(str(e))
        
        return {
            "message": "Sample data seeded successfully",
            "added_count": added_count,
            "total_samples": len(SAMPLE_MARKETING_CONTENT),
            "errors": errors if errors else None
        }
    
    except Exception as e:
        logger.error(f"Failed to seed sample data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to seed sample data: {str(e)}"
        )


@router.post(
    "/search",
    summary="Search Training Data",
    description="Search training data by semantic similarity."
)
async def search_training_data(
    query: str = Query(..., description="Search query"),
    k: int = Query(5, ge=1, le=50, description="Number of results"),
    content_type: Optional[ContentType] = Query(None, description="Filter by content type")
) -> list:
    """Search training data."""
    try:
        vector_store = get_vector_store()
        results = await vector_store.search(query=query, k=k, content_type=content_type)
        
        return [
            {
                "id": str(r.content.id),
                "title": r.content.title,
                "content_type": r.content.content_type.value,
                "similarity_score": r.similarity_score,
                "content_preview": r.content.content[:200],
                "tags": r.content.tags
            }
            for r in results
        ]
    
    except Exception as e:
        logger.error(f"Failed to search training data: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search training data: {str(e)}"
        )
