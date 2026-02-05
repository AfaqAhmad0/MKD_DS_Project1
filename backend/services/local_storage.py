# =============================================================================
# Marketing Assistant AI - Local Storage Helpers
# =============================================================================

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from backend.config import settings
from backend.models.schemas import GenerationRequest, GenerationResponse, MarketingContent, ContentType


def _data_root() -> Path:
    """Resolve the data directory root."""
    return Path(settings.vector_store_path).resolve().parent


def _write_json(directory: Path, payload: dict) -> Path:
    """Write payload to a JSON file and return the path."""
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    file_path = directory / f"{timestamp}_{uuid4().hex}.json"
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path


def save_user_query(request: GenerationRequest, response: GenerationResponse) -> Optional[Path]:
    """
    Save user query + response to local storage (data/user_queries).
    """
    payload = {
        "prompt": request.prompt,
        "content_type": request.content_type.value,
        "target_audience": request.target_audience,
        "key_points": request.key_points,
        "tone_override": request.tone_override,
        "max_length": request.max_length,
        "generated_content": response.generated_content,
        "similar_content_used": response.similar_content_used,
        "generation_metadata": response.generation_metadata,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    return _write_json(_data_root() / "user_queries", payload)


def save_campaign_content(content: MarketingContent) -> Optional[Path]:
    """
    Save campaign content to local storage (data/past_campaigns).
    """
    if content.content_type != ContentType.CAMPAIGN:
        return None
    
    payload = {
        "id": str(content.id),
        "title": content.title,
        "content": content.content,
        "content_type": content.content_type.value,
        "metadata": content.metadata,
        "tags": content.tags,
        "created_at": content.created_at.isoformat() + "Z",
        "updated_at": content.updated_at.isoformat() + "Z"
    }
    return _write_json(_data_root() / "past_campaigns", payload)
