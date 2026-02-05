# =============================================================================
# Marketing Assistant AI - Tone Guidelines
# =============================================================================

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ToneGuideline:
    """Individual tone guideline with examples."""
    name: str
    description: str
    do_examples: List[str]
    dont_examples: List[str]


@dataclass
class ContentTypeGuideline:
    """Guidelines specific to a content type."""
    content_type: str
    description: str
    structure: List[str]
    tone_notes: str
    length_guide: str
    key_elements: List[str]
    example_opening: str


TONE_GUIDELINES: Dict[str, ToneGuideline] = {
    "empowerment": ToneGuideline(
        name="Empowerment Over Pressure",
        description="Make readers feel capable, not pressured or anxious",
        do_examples=[
            "You have everything you need to start this journey.",
            "This is your moment to step into your power.",
            "Imagine waking up feeling confident and unstoppable.",
        ],
        dont_examples=[
            "If you don't act now, you'll miss out forever!",
            "Don't be left behind while others succeed.",
            "You're running out of time to change your life.",
        ],
    ),
    "authenticity": ToneGuideline(
        name="Authentic Connection",
        description="Be genuine and relatable, not corporate or fake",
        do_examples=[
            "Here's the truth: I've been exactly where you are.",
            "Can I share something personal with you?",
            "Let me be real with you for a moment.",
        ],
        dont_examples=[
            "As a leading industry expert with proprietary methods...",
            "Our revolutionary system will transform your life!",
            "We leverage cutting-edge methodologies for synergy.",
        ],
    ),
    "transformation": ToneGuideline(
        name="Transformation Focus",
        description="Always paint the picture of positive change",
        do_examples=[
            "Picture yourself six months from now...",
            "The woman you're becoming is already within you.",
            "Every small step brings you closer to your breakthrough.",
        ],
        dont_examples=[
            "Our product has 15 features including...",
            "We've been in business for 20 years.",
            "Buy this course to learn marketing.",
        ],
    ),
    "direct_warmth": ToneGuideline(
        name="Direct Yet Warm",
        description="Be clear and direct while maintaining warmth",
        do_examples=[
            "Let's cut through the noise. Here's what actually works.",
            "I won't waste your time with fluff. Let's dive in.",
            "Real talk: this won't be easy, but it will be worth it.",
        ],
        dont_examples=[
            "In this comprehensive guide, we shall endeavor to...",
            "Perhaps you might consider possibly exploring...",
            "It could potentially be beneficial if you maybe...",
        ],
    ),
    "action_oriented": ToneGuideline(
        name="Action-Oriented",
        description="Inspire action, not just inspiration",
        do_examples=[
            "Here's your first step: [specific action]",
            "Try this today: [concrete activity]",
            "Take 5 minutes right now and [do this].",
        ],
        dont_examples=[
            "Think positive thoughts and good things will happen.",
            "Just believe in yourself!",
            "The universe will provide if you want it enough.",
        ],
    ),
}


CONTENT_TYPE_GUIDELINES: Dict[str, ContentTypeGuideline] = {
    "email": ContentTypeGuideline(
        content_type="Email",
        description="Personal, direct communication that builds relationship",
        structure=[
            "Subject line (curiosity or benefit-driven)",
            "Personal greeting",
            "Opening hook (1-2 sentences)",
            "Body (short paragraphs, 2-3 sentences each)",
            "Single clear call-to-action",
            "Warm sign-off",
            "P.S. (optional, for important secondary point)",
        ],
        tone_notes="Write like you're emailing a friend who you respect professionally. Warm but purposeful.",
        length_guide="150-400 words for promotional, 100-200 for transactional",
        key_elements=[
            "Compelling subject line",
            "Personal greeting (use 'friend' or first name)",
            "One main message per email",
            "Clear CTA button or link",
            "Signature with personal touch",
        ],
        example_opening="Subject: This changed everything for me\n\nDear friend,\n\nI need to share something with you that I wish someone had told me years ago...",
    ),
    "social_media": ContentTypeGuideline(
        content_type="Social Media",
        description="Thumb-stopping, engaging content that sparks conversation",
        structure=[
            "Hook (first line must stop the scroll)",
            "Value/Story (2-4 short paragraphs)",
            "Call to action or question",
            "Hashtags (3-5 relevant ones)",
        ],
        tone_notes="More casual and conversational. Use line breaks liberally. Write for the scroll.",
        length_guide="100-300 words for LinkedIn, 50-150 for Instagram",
        key_elements=[
            "Strong opening hook",
            "Line breaks for readability",
            "Emoji use (sparingly, purposefully)",
            "Engagement prompt (question or CTA)",
            "Strategic hashtags",
        ],
        example_opening="The question isn't 'Can I do this?'\n\nThe question is 'What's stopping me from trying?'\n\nEvery woman I've worked with started with the same doubts you have right now...",
    ),
    "website_copy": ContentTypeGuideline(
        content_type="Website Copy",
        description="Clear, benefit-focused copy that guides visitors to action",
        structure=[
            "Headline (main benefit or transformation)",
            "Subheadline (supporting detail)",
            "Problem acknowledgment",
            "Solution introduction",
            "Benefits (bullet points)",
            "Social proof",
            "Call to action",
        ],
        tone_notes="Clear and scannable. Lead with benefits. Make every word earn its place.",
        length_guide="Varies by page type - headlines short, about pages longer",
        key_elements=[
            "Clear value proposition",
            "Benefit-focused headlines",
            "Scannable bullet points",
            "Trust elements (testimonials, credentials)",
            "Clear navigation to next step",
        ],
        example_opening="# Transform Your Potential Into Reality\n\nYou know you're capable of more. Let's unlock it together.",
    ),
    "funnel_page": ContentTypeGuideline(
        content_type="Funnel/Landing Page",
        description="Focused, conversion-optimized copy with single goal",
        structure=[
            "Headline addressing core desire",
            "Problem agitation",
            "Solution reveal",
            "Benefits and features",
            "Objection handling",
            "Social proof",
            "Risk reversal",
            "Strong CTA",
            "Urgency (if genuine)",
        ],
        tone_notes="More persuasive but still authentic. Build desire through transformation, not manipulation.",
        length_guide="Long-form for cold traffic, shorter for warm",
        key_elements=[
            "Single focused offer",
            "Transformation-focused headline",
            "Before/after contrast",
            "Specific outcomes and benefits",
            "Testimonials with results",
            "Clear, repeated CTA",
        ],
        example_opening="# Finally... A Proven Path to [Desired Outcome]\n\n**Without** [pain point they want to avoid]\n\nYou've tried everything. The courses. The books. The podcasts...",
    ),
    "ad_copy": ContentTypeGuideline(
        content_type="Ad Copy",
        description="Attention-grabbing, concise copy that drives clicks",
        structure=[
            "Hook (first 3 words critical)",
            "Problem or desire",
            "Solution hint",
            "CTA",
        ],
        tone_notes="Punchy and direct. Every word must work hard. Create curiosity.",
        length_guide="Primary text: 50-125 words. Headline: 5-10 words.",
        key_elements=[
            "Pattern interrupt opening",
            "Single clear benefit",
            "Curiosity gap",
            "Action-oriented CTA",
            "Congruent with landing page",
        ],
        example_opening="🛑 Stop scrolling. This is for you.\n\nYou've tried the productivity hacks. The morning routines.\n\nBut you're still stuck.\n\nHere's what no one tells you...",
    ),
    "blog_post": ContentTypeGuideline(
        content_type="Blog Post",
        description="Educational, value-packed content that builds authority",
        structure=[
            "Compelling headline",
            "Hook opening paragraph",
            "Introduction to problem/topic",
            "Main content (with subheadings)",
            "Actionable takeaways",
            "Conclusion with CTA",
        ],
        tone_notes="Educational but still personal. Share insights and stories. Be generous with value.",
        length_guide="800-2000 words depending on topic depth",
        key_elements=[
            "SEO-friendly headline",
            "Subheadings every 200-300 words",
            "Bullet points and lists",
            "Personal stories/examples",
            "Actionable advice",
            "Internal/external links",
        ],
        example_opening="# Why Your Goals Aren't Working (And What to Do Instead)\n\nEvery January, millions of people set goals. By February, most have given up.\n\nIf this sounds familiar, I want you to know: it's not your fault...",
    ),
    "campaign": ContentTypeGuideline(
        content_type="Campaign",
        description="Multi-piece content with unified theme and journey",
        structure=[
            "Campaign theme/concept",
            "Awareness phase content",
            "Consideration phase content",
            "Decision phase content",
            "Post-purchase/engagement content",
        ],
        tone_notes="Consistent voice across all pieces. Build momentum. Tell a cohesive story.",
        length_guide="Varies by piece - see individual content types",
        key_elements=[
            "Unified campaign theme",
            "Consistent messaging",
            "Strategic sequencing",
            "Cross-piece callbacks",
            "Clear journey progression",
            "Coordinated CTAs",
        ],
        example_opening="CAMPAIGN: Spring Renewal\n\nTheme: 'Spring Into the New You'\n\nMessage: Use spring's energy of renewal for personal transformation...",
    ),
}


def get_guidelines_for_content_type(content_type: str) -> Optional[ContentTypeGuideline]:
    """Get the writing guidelines for a specific content type."""
    return CONTENT_TYPE_GUIDELINES.get(content_type.lower())


def format_guidelines_for_prompt(content_type: str) -> str:
    """Format content type guidelines as a prompt section."""
    guideline = get_guidelines_for_content_type(content_type)
    if not guideline:
        return ""
    
    structure_list = "\n".join(f"  {i+1}. {item}" for i, item in enumerate(guideline.structure))
    elements_list = "\n".join(f"  - {item}" for item in guideline.key_elements)
    
    return f"""
## Content Type: {guideline.content_type}

{guideline.description}

### Structure
{structure_list}

### Tone Notes
{guideline.tone_notes}

### Length Guide
{guideline.length_guide}

### Key Elements
{elements_list}

### Example Opening
{guideline.example_opening}
"""
