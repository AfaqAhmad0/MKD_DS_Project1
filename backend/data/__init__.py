# =============================================================================
# Marketing Assistant AI - Data Package
# =============================================================================

# Brand components
from backend.data.brand import (
    BRAND_VOICE,
    BrandVoiceConfig,
    get_brand_voice_prompt,
    TONE_GUIDELINES,
    CONTENT_TYPE_GUIDELINES,
    get_guidelines_for_content_type,
    POWER_WORDS,
    PHRASES_TO_USE,
    PHRASES_TO_AVOID,
    EMOTIONAL_TRIGGERS,
    TARGET_PERSONAS,
    get_persona_context,
)

# Templates
from backend.data.templates import (
    EMAIL_TEMPLATES,
    SOCIAL_MEDIA_TEMPLATES,
    AD_COPY_TEMPLATES,
    WEBSITE_TEMPLATES,
    FUNNEL_TEMPLATES,
    BLOG_TEMPLATES,
)

# Samples for seeding
from backend.data.samples import SAMPLE_MARKETING_CONTENT

__all__ = [
    # Brand
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
    # Templates
    "EMAIL_TEMPLATES",
    "SOCIAL_MEDIA_TEMPLATES",
    "AD_COPY_TEMPLATES",
    "WEBSITE_TEMPLATES",
    "FUNNEL_TEMPLATES",
    "BLOG_TEMPLATES",
    # Samples
    "SAMPLE_MARKETING_CONTENT",
]
