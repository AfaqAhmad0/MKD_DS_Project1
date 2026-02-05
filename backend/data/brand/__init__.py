# =============================================================================
# Marketing Assistant AI - Brand Package
# =============================================================================

from backend.data.brand.voice import (
    BRAND_VOICE,
    BrandVoiceConfig,
    get_brand_voice_prompt,
)

from backend.data.brand.tone_guidelines import (
    TONE_GUIDELINES,
    CONTENT_TYPE_GUIDELINES,
    get_guidelines_for_content_type,
)

from backend.data.brand.vocabulary import (
    POWER_WORDS,
    PHRASES_TO_USE,
    PHRASES_TO_AVOID,
    EMOTIONAL_TRIGGERS,
)

from backend.data.brand.personas import (
    TARGET_PERSONAS,
    get_persona_context,
)

__all__ = [
    "BRAND_VOICE",
    "BrandVoiceConfig",
    "get_brand_voice_prompt",
    "TONE_GUIDELINES",
    "CONTENT_TYPE_GUIDELINES",
    "get_guidelines_for_content_type",
    "POWER_WORDS",
    "PHRASES_TO_USE",
    "PHRASES_TO_AVOID",
    "EMOTIONAL_TRIGGERS",
    "TARGET_PERSONAS",
    "get_persona_context",
]
