# =============================================================================
# Marketing Assistant AI - Brand Style Helpers (Spec-Compatible)
# =============================================================================

from backend.data.brand import (
    get_brand_voice_prompt,
    format_guidelines_for_prompt,
    format_vocabulary_for_prompt,
    get_persona_context
)

__all__ = [
    "get_brand_voice_prompt",
    "format_guidelines_for_prompt",
    "format_vocabulary_for_prompt",
    "get_persona_context"
]
