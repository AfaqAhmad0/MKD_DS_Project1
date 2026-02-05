# =============================================================================
# Marketing Assistant AI - Copywriter Module (Spec-Compatible)
# =============================================================================

from backend.models.schemas import GenerationRequest, GenerationResponse
from backend.services.llm_service import get_llm_service
from backend.services.reranker import get_reranker_service
from backend.services.vector_store import get_vector_store


async def generate_copy(
    request: GenerationRequest,
    use_rag: bool = True,
    num_examples: int = 3
) -> GenerationResponse:
    """
    Generate marketing copy using the same pipeline as the API.
    
    Args:
        request: GenerationRequest with prompt and content_type
        use_rag: Whether to use retrieval-augmented generation
        num_examples: Number of examples to retrieve
    """
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
            retrieved_content = await reranker.rerank(
                query=request.prompt,
                results=search_results,
                top_n=num_examples
            )

    return await llm.generate(
        request=request,
        retrieved_content=retrieved_content
    )
