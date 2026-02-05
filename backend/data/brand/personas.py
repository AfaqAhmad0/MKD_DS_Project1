# =============================================================================
# Marketing Assistant AI - Target Personas
# =============================================================================

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Persona:
    """Detailed definition of a target audience persona."""
    name: str
    demographic: str
    description: str
    goals: List[str]
    pain_points: List[str]
    desires: List[str]
    objections: List[str]
    motivators: List[str]
    content_preferences: List[str]
    tone_adjustments: str


TARGET_PERSONAS: Dict[str, Persona] = {
    "aspiring_entrepreneur": Persona(
        name="The Aspiring Entrepreneur",
        demographic="Women 28-45, professional background, considering or starting a business",
        description="She's successful in her career but feels unfulfilled. She has a business idea or side hustle she's been thinking about but hasn't taken the leap. She's smart, capable, but held back by fear of failure and imposter syndrome.",
        goals=[
            "Start her own business or scale her side hustle",
            "Achieve financial independence",
            "Create work that aligns with her values",
            "Build something she's proud of",
            "Have flexibility and freedom in her schedule",
        ],
        pain_points=[
            "Imposter syndrome - 'Who am I to do this?'",
            "Fear of failure and judgment",
            "Overwhelmed by where to start",
            "Lack of support from friends/family who don't understand",
            "Feeling stuck between security and dreams",
            "Information overload - too many courses, conflicting advice",
        ],
        desires=[
            "Confidence to take the leap",
            "A clear roadmap to follow",
            "Proof that people like her can succeed",
            "A supportive community of like-minded women",
            "Permission to prioritize her dreams",
        ],
        objections=[
            "I don't have enough time",
            "I don't have enough money to invest",
            "I'm not ready yet - I need to learn more first",
            "What if it doesn't work?",
            "My situation is different/harder",
        ],
        motivators=[
            "Success stories of women who started where she is",
            "Practical, actionable steps (not just theory)",
            "Quick wins to build momentum",
            "Recognition that her fears are normal",
            "Vision of the life she could have",
        ],
        content_preferences=[
            "How-to guides and frameworks",
            "Behind-the-scenes and real talk",
            "Success stories and case studies",
            "Bite-sized, actionable content",
            "Longer deep-dive content for serious learning",
        ],
        tone_adjustments="Balance inspiration with practicality. Address imposter syndrome directly. Emphasize that starting messy is better than not starting.",
    ),
    "burnt_out_professional": Persona(
        name="The Burnt Out Professional",
        demographic="Women 35-55, established career, feeling exhausted and unfulfilled",
        description="She's achieved success by external measures but feels empty. She's exhausted from climbing a ladder that might be against the wrong wall. She's questioning everything and looking for meaning and balance.",
        goals=[
            "Find fulfillment and purpose",
            "Achieve work-life balance",
            "Reconnect with herself and what she actually wants",
            "Make a change without losing everything she's built",
            "Find energy and joy again",
        ],
        pain_points=[
            "Constant exhaustion and burnout",
            "Golden handcuffs - good salary but soul-sucking job",
            "Identity wrapped up in work",
            "Guilt about wanting more when she 'should' be grateful",
            "Fear of starting over at this age",
            "Feeling invisible and undervalued",
        ],
        desires=[
            "Permission to want more",
            "A path to change that doesn't require blowing everything up",
            "Energy and enthusiasm again",
            "Alignment between values and daily life",
            "To feel like herself again",
        ],
        objections=[
            "I've invested too much to change now",
            "I have too many responsibilities",
            "This is just how life is at this stage",
            "It's too late for me",
            "I can't afford to take risks",
        ],
        motivators=[
            "Stories of mid-career transformations",
            "Evidence that it's never too late",
            "Strategies that work within constraints",
            "Focus on small shifts with big impact",
            "Validation that her feelings are valid",
        ],
        content_preferences=[
            "Thoughtful, nuanced content",
            "Evidence-based approaches",
            "Strategies that respect her experience",
            "Content she can consume during commute or lunch",
            "Community of peers at similar life stage",
        ],
        tone_adjustments="Acknowledge her accomplishments. Don't be patronizing - she's smart and experienced. Focus on optimization and alignment rather than starting from scratch.",
    ),
    "growth_seeker": Persona(
        name="The Growth Seeker",
        demographic="Women 25-40, always learning, invested in personal development",
        description="She's a perpetual student of life. She reads the books, takes the courses, listens to the podcasts. She's growth-minded but sometimes struggles to implement what she learns.",
        goals=[
            "Continuous self-improvement",
            "Turn knowledge into results",
            "Develop mastery in her chosen areas",
            "Build a life designed on her terms",
            "Help others on their journey too",
        ],
        pain_points=[
            "Shiny object syndrome - too many interests",
            "Gap between knowing and doing",
            "Overwhelm from too much information",
            "Perfectionism preventing progress",
            "Comparing herself to others ahead of her",
            "Feeling like she's always almost there",
        ],
        desires=[
            "A framework to focus her energy",
            "Accountability to take action",
            "Depth over breadth",
            "Real transformation, not just information",
            "To be in a room with people playing at a higher level",
        ],
        objections=[
            "I've already tried so many things",
            "What makes this different?",
            "I already know this stuff",
            "I just need to implement what I already know",
            "Is this going to be another course that sits unused?",
        ],
        motivators=[
            "Novel perspectives and frameworks",
            "Implementation-focused content",
            "Challenges and accountability",
            "Community of action-takers",
            "Tangible progress metrics",
        ],
        content_preferences=[
            "Frameworks and systems",
            "Advanced/nuanced content",
            "Challenges and sprints",
            "Community interaction",
            "Quick-hit content that's still substantive",
        ],
        tone_adjustments="Respect her existing knowledge. Focus on implementation and action. Challenge her to go deeper rather than wider. Call out analysis paralysis kindly.",
    ),
    "new_chapter": Persona(
        name="The New Chapter Woman",
        demographic="Women 45-60, major life transition, redefining identity",
        description="She's navigating a significant life change and ready to write the next chapter of her life on her own terms.",
        goals=[
            "Reinvent herself for this next phase",
            "Discover who she is outside of her previous roles",
            "Create meaning and purpose",
            "Build new connections and community",
            "Leave a legacy she's proud of",
        ],
        pain_points=[
            "Identity crisis - who am I now?",
            "Loss of purpose when previous roles end",
            "Invisibility in society that values youth",
            "Starting over when she thought she'd be settled",
            "Fear of the unknown",
            "Grief for the life she had or expected",
        ],
        desires=[
            "A vision for an exciting next chapter",
            "Proof that her best years aren't behind her",
            "Community of women in similar transitions",
            "Practical guidance for reinvention",
            "To be seen and valued for who she is now",
        ],
        objections=[
            "I'm too old to start over",
            "My best years are behind me",
            "I don't know how to do things differently",
            "The world has changed too much",
            "This is for younger women",
        ],
        motivators=[
            "Stories of women thriving in their 50s+",
            "Celebration of wisdom and experience",
            "Focus on the advantages of this life stage",
            "Practical, respectful guidance",
            "Community of peers",
        ],
        content_preferences=[
            "Thoughtful, inspiring content",
            "Stories of reinvention",
            "Practical how-tos for modern challenges",
            "Longer-form content",
            "Community connection",
        ],
        tone_adjustments="Celebrate her experience and wisdom. Never be condescending or ageist. Focus on the freedom and power of this life stage. Be sensitive to grief while being hopeful about the future.",
    ),
}


def get_persona(name: str) -> Optional[Persona]:
    """Get a specific persona by name."""
    return TARGET_PERSONAS.get(name.lower().replace(" ", "_"))


def get_persona_context(persona_name: str) -> str:
    """Generate context about a persona for the LLM."""
    persona = get_persona(persona_name)
    if not persona:
        return ""
    
    return f"""
## Target Audience: {persona.name}

**Demographic**: {persona.demographic}

**Description**: {persona.description}

**Goals**:
{chr(10).join(f"- {goal}" for goal in persona.goals[:3])}

**Pain Points**:
{chr(10).join(f"- {pain}" for pain in persona.pain_points[:3])}

**What They Want to Hear**:
{chr(10).join(f"- {desire}" for desire in persona.desires[:3])}

**Tone Adjustment**: {persona.tone_adjustments}
"""


def get_all_personas_summary() -> str:
    """Get a brief summary of all personas."""
    summaries = []
    for key, persona in TARGET_PERSONAS.items():
        summaries.append(f"- **{persona.name}**: {persona.demographic}")
    return "\n".join(summaries)
