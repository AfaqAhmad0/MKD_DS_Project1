# =============================================================================
# Marketing Assistant AI - Main Application (Cohere + HF Version)
# =============================================================================
# Cohere is used for embeddings/rerank (API key required).
#
# Tech Stack:
# - Cohere for embeddings (API)
# - FAISS for vector search (local)
# - Cohere for re-ranking (API)
# - Hugging Face Transformers for LLM (local)
#
# To run: python main.py
# API Docs: http://localhost:8000/docs
# =============================================================================

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.routers import generation_router, generation_public_router, training_data_router

# =============================================================================
# Logging Configuration
# =============================================================================

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


# =============================================================================
# Application Lifespan
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name}")
    logger.info("=" * 60)
    logger.info("Cohere API is required for embeddings and re-ranking.")
    logger.info("=" * 60)
    logger.info(f"Embedding model: {settings.cohere_embed_model}")
    logger.info(f"LLM model: {settings.huggingface_model}")
    logger.info(f"Re-rank model: {settings.cohere_rerank_model}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title=settings.app_name,
    description="""
## Marketing Assistant AI

AI-powered marketing copy generation aligned with **Adriana James' brand voice**.

**Cohere API key required** for embeddings and re-ranking.

### Tech Stack
- **Embeddings**: Cohere (API)
- **Vector DB**: FAISS (local)
- **Re-ranking**: Cohere (API)
- **LLM**: Hugging Face Transformers (local)

### Quick Start
1. Seed sample data: `POST /api/v1/training-data/seed`
2. Generate content: `POST /generate-copy`
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Exception Handler
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
        }
    )


# =============================================================================
# Routers
# =============================================================================

app.include_router(generation_router)
app.include_router(generation_public_router)
app.include_router(training_data_router)


# =============================================================================
# Root Endpoints
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "AI-powered marketing copy generation",
        "stack": {
            "embeddings": f"Cohere ({settings.cohere_embed_model})",
            "vector_db": "FAISS",
            "reranking": f"Cohere ({settings.cohere_rerank_model})",
            "llm": f"Hugging Face ({settings.huggingface_model})"
        },
        "docs": "/docs",
        "cohere_required": True,
        "endpoints": {
            "generate_copy": "/generate-copy",
            "generate": "/api/v1/generate",
            "refine": "/api/v1/generate/refine",
            "content_types": "/api/v1/generate/content-types",
            "training_data": "/api/v1/training-data",
            "training_data_seed": "/api/v1/training-data/seed"
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "embeddings": "cohere",
            "vector_store": "local", 
            "reranker": "cohere",
            "llm": "local (huggingface)"
        },
        "note": "Cohere API key required for embeddings and reranking."
    }


# =============================================================================
# Run directly
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.api_host, port=settings.api_port, reload=settings.debug)
