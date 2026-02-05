# =============================================================================
# Marketing Assistant AI - Models Package
# =============================================================================
# This package contains Pydantic models (schemas) for data validation.
# =============================================================================

from backend.models.schemas import (
    # Request models
    GenerationRequest,
    SimpleGenerationRequest,
    TrainingDataCreate,
    TrainingDataUpdate,
    
    # Response models
    GenerationResponse,
    TrainingDataResponse,
    TrainingDataListResponse,
    
    # Internal models
    MarketingContent,
    RetrievedContent,
    
    # Enums
    ContentType,
)

__all__ = [
    "GenerationRequest",
    "SimpleGenerationRequest",
    "TrainingDataCreate",
    "TrainingDataUpdate",
    "GenerationResponse",
    "TrainingDataResponse",
    "TrainingDataListResponse",
    "MarketingContent",
    "RetrievedContent",
    "ContentType",
]
