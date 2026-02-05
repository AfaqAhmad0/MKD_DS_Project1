# =============================================================================
# Marketing Assistant AI - Configuration Module (Cohere + HF Version)
# =============================================================================
# All configuration is managed through environment variables.
# This version uses Cohere for embeddings/rerank (API key required).
# =============================================================================

import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# =============================================================================
# Find project root and .env file
# =============================================================================
# This ensures .env is found regardless of where the script is run from

def _find_env_file() -> Optional[Path]:
    """
    Find the .env file by searching from this file's location upward.
    
    Returns:
        Path to .env file if found, None otherwise
    """
    # Start from this file's directory
    current = Path(__file__).resolve().parent
    
    # Search up to 3 levels (backend/ -> project root)
    for _ in range(3):
        env_path = current / ".env"
        if env_path.exists():
            return env_path
        current = current.parent
    
    return None


# Resolve .env path once at module load
_ENV_FILE = _find_env_file()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses hosted + local models:
    - Cohere for embeddings and re-ranking (API key required)
    - FAISS for vector search (local)
    - Hugging Face Transformers for LLM (local)
    
    Settings are loaded in this priority order:
    1. Environment variables (highest priority)
    2. .env file
    3. Default values (lowest priority)
    """
    
    # -------------------------------------------------------------------------
    # Application Settings
    # -------------------------------------------------------------------------
    app_name: str = "Marketing Assistant AI"
    app_env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # -------------------------------------------------------------------------
    # Vector Store Configuration
    # -------------------------------------------------------------------------
    vector_store_path: str = "./data/vector_store"
    
    # Embedding dimension - must match the Cohere model
    # embed-english-v3.0 = 1024 dimensions
    embedding_dimension: int = 1024
    
    # -------------------------------------------------------------------------
    # Cohere Configuration (Embeddings + Re-ranking)
    # -------------------------------------------------------------------------
    cohere_api_key: Optional[str] = None
    cohere_embed_model: str = "embed-english-v3.0"
    cohere_rerank_model: str = "rerank-english-v3.0"
    
    # -------------------------------------------------------------------------
    # Open Source LLM (Hugging Face Transformers)
    # -------------------------------------------------------------------------
    # Model options (by RAM requirement):
    # - TinyLlama/TinyLlama-1.1B-Chat-v1.0: ~4GB RAM, fast
    # - microsoft/phi-2: ~6GB RAM, good quality  
    # - Qwen/Qwen2-1.5B-Instruct: ~4GB RAM, good quality
    # - mistralai/Mistral-7B-Instruct-v0.2: ~16GB RAM, best quality
    huggingface_model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    # Generation parameters
    max_generation_tokens: int = 512
    generation_temperature: float = 0.7
    
    # -------------------------------------------------------------------------
    # Re-ranking Configuration (Cohere)
    # -------------------------------------------------------------------------
    rerank_top_n: int = 5
    
    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------
    
    @field_validator("api_port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Ensure port is in valid range."""
        if not 1 <= v <= 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {v}")
        return v
    
    @field_validator("generation_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Ensure temperature is in valid range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError(f"Temperature must be between 0.0 and 2.0, got {v}")
        return v
    
    @field_validator("embedding_dimension")
    @classmethod
    def validate_dimension(cls, v: int) -> int:
        """Ensure embedding dimension is positive."""
        if v <= 0:
            raise ValueError(f"Embedding dimension must be positive, got {v}")
        return v
    
    # -------------------------------------------------------------------------
    # Pydantic Settings Configuration
    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,  # Use resolved absolute path
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Settings: Validated settings instance
        
    Note:
        Settings are cached after first load. Call get_settings.cache_clear()
        to reload settings (useful for testing).
    """
    return Settings()


def validate_env_file() -> dict:
    """
    Validate that .env file exists and return status info.
    
    Returns:
        dict: Status information about .env file
    """
    if _ENV_FILE is None:
        return {
            "found": False,
            "path": None,
            "message": "No .env file found. Using defaults and environment variables."
        }
    
    return {
        "found": True,
        "path": str(_ENV_FILE),
        "message": f"Using .env from: {_ENV_FILE}"
    }


# =============================================================================
# Convenience access
# =============================================================================
# Create settings instance at module load for easy import

settings = get_settings()

# Print .env status on first import (only in debug mode)
if settings.debug:
    _env_status = validate_env_file()
    if not _env_status["found"]:
        print(f"[config] Warning: {_env_status['message']}", file=sys.stderr)
    if not settings.cohere_api_key:
        print(
            "[config] Warning: COHERE_API_KEY is not set. "
            "Embeddings and re-ranking will fail until it is provided.",
            file=sys.stderr
        )


__all__ = ["Settings", "get_settings", "settings", "validate_env_file"]
