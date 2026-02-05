# =============================================================================
# Marketing Assistant AI - Routers Package
# =============================================================================

from backend.routers.generation import router as generation_router, public_router as generation_public_router
from backend.routers.training_data import router as training_data_router

__all__ = [
    "generation_router",
    "generation_public_router",
    "training_data_router",
]
