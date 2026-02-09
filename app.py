"""
Entry point for deployment platforms (e.g. Hugging Face Spaces, Render)
that expect `app` at the project root.

This simply re-exports the FastAPI application defined in `backend.main`.
"""

from backend.main import app  # noqa: F401

