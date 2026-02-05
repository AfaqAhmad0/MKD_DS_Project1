# =============================================================================
# Marketing Assistant AI - Brand Vocabulary
# =============================================================================

from typing import List, Dict
from dataclasses import dataclass


POWER_WORDS: Dict[str, List[str]] = {
    "transformation": [
        "transform",
        "breakthrough",
        "unlock",
        "discover",
        "awaken",
        "evolve",
        "become",
        "emerge",
        "shift",
        "elevate",
    ],
    "empowerment": [
        "empower",
        "capable",
        "confident",
        "unstoppable",
        "powerful",
        "strong",
        "bold",
        "fearless",
        "resilient",
        "determined",
    ],
    "action": [
        "start",
        "begin",
        "launch",
        "create",
        "build",
        "take",
        "move",
        "step",
        "commit",
        "decide",
    ],
    "connection": [
        "together",
        "community",
        "support",
        "join",
        "belong",
        "share",
        "connect",
        "tribe",
        "sisterhood",
        "ally",
    ],
    "positive_outcome": [
        "freedom",
        "clarity",
        "peace",
        "joy",
        "success",
        "abundance",
        "fulfillment",
        "growth",
        "progress",
        "achievement",
    ],
    "urgency_positive": [
        "now",
        "today",
        "moment",
        "ready",
        "time",
        "opportunity",
        "chance",
        "finally",
        "already",
        "waiting",
    ],
}


PHRASES_TO_USE: Dict[str, List[str]] = {
    "openings": [
        "Here's the truth...",
        "What if I told you...",
        "Let me share something with you...",
        "Can I be honest with you?",
        "Imagine this...",
        "Picture yourself...",
        "You know that feeling when...",
        "I've been where you are...",
    ],
    "empowerment": [
        "You deserve...",
        "You're capable of...",
        "This is your moment to...",
        "You have everything you need to...",
        "The woman you're becoming...",
        "You're closer than you think...",
        "Trust yourself to...",
        "Give yourself permission to...",
    ],
    "connection": [
        "Together, we can...",
        "You're not alone in this...",
        "I believe in you...",
        "I see you, and I understand...",
        "We're in this together...",
        "I'm here with you...",
        "Join me in...",
        "Let's do this together...",
    ],
    "transition": [
        "Here's what I've learned...",
        "The real question is...",
        "But here's the thing...",
        "What changed everything was...",
        "The secret is...",
        "What most people miss is...",
        "Here's what actually works...",
        "Let me break this down...",
    ],
    "call_to_action": [
        "Take the first step...",
        "Start your journey...",
        "Claim your spot...",
        "Join us today...",
        "Ready to transform?",
        "Your next step is...",
        "Let's begin...",
        "Say yes to yourself...",
    ],
    "closing": [
        "Believing in your potential,",
        "Here's to your transformation,",
        "With you every step,",
        "In your corner,",
        "Cheering you on,",
        "To your success,",
        "With belief in you,",
        "Onward and upward,",
    ],
}


PHRASES_TO_AVOID: Dict[str, List[str]] = {
    "pushy_sales": [
        "Buy now!",
        "Limited time only!",
        "Act fast!",
        "Don't miss out!",
        "Only X spots left!",
        "This won't last!",
        "Exclusive offer expires...",
        "You'd be crazy not to...",
    ],
    "fear_based": [
        "You'll regret not...",
        "Don't be left behind...",
        "You're running out of time...",
        "If you don't do this, you'll...",
        "Don't make this mistake...",
        "You're failing because...",
        "What's wrong with you is...",
        "Your problem is...",
    ],
    "corporate_jargon": [
        "Leverage synergies...",
        "Paradigm shift...",
        "Move the needle...",
        "Circle back...",
        "Low-hanging fruit...",
        "Best-in-class...",
        "Industry-leading...",
        "Revolutionary system...",
    ],
    "condescending": [
        "It's simple, just...",
        "Obviously you should...",
        "Anyone can do this...",
        "If you really wanted it...",
        "You're doing it wrong...",
        "Let me explain this simply...",
        "You don't understand...",
        "That's not how it works...",
    ],
    "vague_inspiration": [
        "Just believe in yourself!",
        "Follow your dreams!",
        "You can do anything!",
        "Think positive!",
        "The universe will provide...",
        "Manifest your destiny...",
        "Everything happens for a reason...",
        "Just be grateful...",
    ],
}


@dataclass
class EmotionalTrigger:
    """Defines an emotional trigger with examples."""
    emotion: str
    description: str
    trigger_phrases: List[str]
    use_when: str


EMOTIONAL_TRIGGERS: Dict[str, EmotionalTrigger] = {
    "hope": EmotionalTrigger(
        emotion="Hope",
        description="A feeling that positive change is possible",
        trigger_phrases=[
            "Imagine waking up feeling...",
            "Picture yourself six months from now...",
            "What would your life look like if...",
            "The transformation is possible...",
        ],
        use_when="Opening messages, painting the vision of transformation",
    ),
    "belonging": EmotionalTrigger(
        emotion="Belonging",
        description="A sense of community and not being alone",
        trigger_phrases=[
            "You're not alone in this...",
            "Join thousands of women who...",
            "We're in this together...",
            "Welcome to a community that...",
        ],
        use_when="Community building, program enrollment, support offers",
    ),
    "validation": EmotionalTrigger(
        emotion="Validation",
        description="Feeling seen and understood",
        trigger_phrases=[
            "I see you...",
            "Your feelings are valid...",
            "It's okay to feel...",
            "You're not crazy for wanting...",
        ],
        use_when="Acknowledging struggles, building rapport, showing empathy",
    ),
    "confidence": EmotionalTrigger(
        emotion="Confidence",
        description="Belief in one's ability to succeed",
        trigger_phrases=[
            "You have everything you need...",
            "You're more ready than you think...",
            "Trust yourself to...",
            "You've already proven you can...",
        ],
        use_when="Calls to action, overcoming objections, motivating action",
    ),
    "curiosity": EmotionalTrigger(
        emotion="Curiosity",
        description="A desire to learn more",
        trigger_phrases=[
            "What if I told you...",
            "Here's what no one tells you...",
            "The real secret is...",
            "Have you ever wondered why...",
        ],
        use_when="Headlines, hooks, ad copy, email subject lines",
    ),
    "urgency": EmotionalTrigger(
        emotion="Positive Urgency",
        description="Motivation to act now (opportunity-based, not fear-based)",
        trigger_phrases=[
            "This is your moment...",
            "The time is now...",
            "You're ready for this...",
            "Why wait for someday when...",
        ],
        use_when="Calls to action, closing arguments, launch content",
    ),
}


def get_power_words_for_context(context: str) -> List[str]:
    """Get relevant power words for a specific context."""
    return POWER_WORDS.get(context.lower(), [])


def get_all_power_words() -> List[str]:
    """Get all power words as a flat list."""
    all_words = []
    for words in POWER_WORDS.values():
        all_words.extend(words)
    return list(set(all_words))


def format_vocabulary_for_prompt() -> str:
    """Format vocabulary guidelines for LLM prompt."""
    power_words_str = ", ".join(get_all_power_words()[:20])
    phrases_use = PHRASES_TO_USE.get("openings", [])[:5]
    phrases_avoid = PHRASES_TO_AVOID.get("pushy_sales", [])[:5]
    
    return f"""
## Vocabulary Guidelines

### Power Words to Use
{power_words_str}

### Signature Phrases
{chr(10).join(f'- "{p}"' for p in phrases_use)}

### Phrases to Avoid
{chr(10).join(f'- "{p}"' for p in phrases_avoid)}
"""
