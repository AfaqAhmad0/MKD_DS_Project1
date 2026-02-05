# =============================================================================
# Marketing Assistant AI - Generation Router
# =============================================================================
# This module defines the API endpoints for generating marketing copy.
# =============================================================================

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    GenerationRequest,
    SimpleGenerationRequest,
    GenerationResponse,
    ContentType
)
from backend.services.vector_store import get_vector_store
from backend.services.reranker import get_reranker_service
from backend.services.llm_service import get_llm_service
from backend.services.local_storage import save_user_query

# Configure logging for this module
logger = logging.getLogger(__name__)

# Create the router with prefix and tags for OpenAPI documentation
router = APIRouter(
    prefix="/api/v1/generate",
    tags=["Generation"],
    responses={
        500: {"description": "Internal server error during generation"}
    }
)

# Public compatibility router (matches task spec)
public_router = APIRouter(
    tags=["Generation"]
)


@router.post(
    "",
    response_model=GenerationResponse,
    summary="Generate Marketing Copy",
    description="""
    Generate marketing copy aligned with Adriana James' brand voice.
    
    This endpoint uses Retrieval-Augmented Generation (RAG) to create content:
    1. Searches for similar past content in the vector store
    2. Re-ranks results for optimal relevance
    3. Uses retrieved content as context for the LLM
    4. Generates new content matching the brand voice
    """
)
async def generate_copy(
    request: GenerationRequest,
    use_rag: bool = Query(
        default=True,
        description="Whether to use retrieved content for context (RAG)"
    ),
    num_examples: int = Query(
        default=3,
        ge=0,
        le=10,
        description="Number of similar examples to retrieve for context"
    )
) -> GenerationResponse:
    """Generate marketing copy based on the provided request."""
    try:
        logger.info(
            f"Generation request received: content_type={request.content_type.value}, "
            f"use_rag={use_rag}, num_examples={num_examples}"
        )
        
        vector_store = get_vector_store()
        reranker = get_reranker_service()
        llm = get_llm_service()
        
        retrieved_content = None
        if use_rag and num_examples > 0:
            search_results = await vector_store.search(
                query=request.prompt,
                k=num_examples * 2,
                content_type=request.content_type
            )
            
            if search_results:
                reranked_results = await reranker.rerank(
                    query=request.prompt,
                    results=search_results,
                    top_n=num_examples
                )
                retrieved_content = reranked_results
        
        response = await llm.generate(
            request=request,
            retrieved_content=retrieved_content
        )
        
        try:
            save_user_query(request, response)
        except Exception as storage_error:
            logger.warning(f"Failed to store user query: {storage_error}")
        
        return response
    
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content: {str(e)}"
        )


@public_router.post(
    "/generate-copy",
    response_model=GenerationResponse,
    summary="Generate Marketing Copy (Spec-Compatible)",
    description="""
    Generate marketing copy using the simplified /generate-copy endpoint.
    
    This matches the task spec and accepts a minimal payload with `prompt`.
    """
)
async def generate_copy_public(
    request: SimpleGenerationRequest
) -> GenerationResponse:
    """
    Spec-compatible endpoint for content generation.
    
    Defaults content_type to CAMPAIGN when omitted.
    """
    full_request = GenerationRequest(
        prompt=request.prompt,
        content_type=request.content_type or ContentType.CAMPAIGN,
        target_audience=request.target_audience,
        key_points=request.key_points,
        tone_override=request.tone_override,
        max_length=request.max_length
    )
    return await generate_copy(full_request, use_rag=True, num_examples=3)


@router.post(
    "/refine",
    response_model=dict,
    summary="Refine Existing Content",
    description="""
    Refine existing marketing content based on feedback.
    """
)
async def refine_content(
    original_content: str,
    feedback: str,
    content_type: ContentType
) -> dict:
    """Refine existing content based on feedback."""
    if not original_content or len(original_content) < 10:
        raise HTTPException(
            status_code=400,
            detail="Original content must be at least 10 characters"
        )
    
    if not feedback or len(feedback) < 5:
        raise HTTPException(
            status_code=400,
            detail="Feedback must be at least 5 characters"
        )
    
    try:
        logger.info(f"Refine request: content_type={content_type.value}")
        
        llm = get_llm_service()
        refined = await llm.refine_content(
            original_content=original_content,
            feedback=feedback,
            content_type=content_type
        )
        
        return {
            "refined_content": refined,
            "content_type": content_type.value,
            "feedback_applied": feedback
        }
        
    except Exception as e:
        logger.error(f"Refinement failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refine content: {str(e)}"
        )


@router.get(
    "/content-types",
    response_model=list,
    summary="List Available Content Types",
    description="Get a list of all supported content types for generation."
)
async def list_content_types() -> list:
    """List all available content types."""
    content_types = [
        {
            "value": ContentType.EMAIL.value,
            "name": "Email",
            "description": "Email campaigns, newsletters, promotional emails"
        },
        {
            "value": ContentType.SOCIAL_MEDIA.value,
            "name": "Social Media",
            "description": "Posts for Instagram, LinkedIn, Twitter, Facebook"
        },
        {
            "value": ContentType.WEBSITE_COPY.value,
            "name": "Website Copy",
            "description": "Landing pages, about pages, product descriptions"
        },
        {
            "value": ContentType.FUNNEL_PAGE.value,
            "name": "Funnel Page",
            "description": "Sales funnels, opt-in pages, checkout pages"
        },
        {
            "value": ContentType.AD_COPY.value,
            "name": "Ad Copy",
            "description": "Paid advertisements (Facebook, Google, etc.)"
        },
        {
            "value": ContentType.BLOG_POST.value,
            "name": "Blog Post",
            "description": "Long-form blog content and articles"
        },
        {
            "value": ContentType.CAMPAIGN.value,
            "name": "Campaign",
            "description": "Full marketing campaigns with multiple touchpoints"
        }
    ]
    
    return content_types
