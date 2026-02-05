# =============================================================================
# Marketing Assistant AI - Ad Copy Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AdTemplate:
    """Template for an ad type."""
    name: str
    platform: str
    objective: str
    structure: List[str]
    primary_text: str
    headline: str
    description: str
    tips: List[str]


AD_COPY_TEMPLATES: Dict[str, AdTemplate] = {
    "lead_gen_problem": AdTemplate(
        name="Lead Gen - Problem Aware",
        platform="Facebook/Instagram",
        objective="Collect leads through free resource offer",
        structure=[
            "Hook (call out the problem)",
            "Agitate (make it relatable)",
            "Solution hint",
            "Offer (free resource)",
            "CTA",
        ],
        primary_text="""🛑 Stop scrolling. This is for you.

You've tried the productivity hacks. The morning routines. The vision boards.

But you're still not where you want to be.

Here's the thing no one tells you: transformation isn't about adding more. It's about doing the RIGHT things in the RIGHT order.

I've helped 10,000+ women break through—and I put my entire framework in a free guide.

No fluff. Just the 5 pillars that actually create change.

🎁 Grab your free copy below.""",
        headline="Free: 5 Pillars of Transformation Guide",
        description="The framework that's helped 10,000+ women. Download now.",
        tips=[
            "Call out the target audience in the hook",
            "Acknowledge what they've already tried",
            "Keep primary text under 125 words",
            "Make the offer irresistible",
            "Use emojis strategically (not excessively)",
        ],
    ),
    "lead_gen_desire": AdTemplate(
        name="Lead Gen - Desire Focused",
        platform="Facebook/Instagram",
        objective="Collect leads by speaking to aspirations",
        structure=[
            "Paint the picture (desired state)",
            "Bridge (this is possible for you)",
            "Method (hint at how)",
            "Offer",
            "CTA",
        ],
        primary_text="""Imagine waking up excited for your day.

Not dreading your to-do list. Not feeling behind before you even start.

Just... clear. Energized. Ready.

This isn't a fantasy. It's what happens when you stop trying harder and start working smarter.

I've put my entire transformation framework into a free guide—the same one I use with my private clients.

Inside you'll discover:
✅ The #1 reason you feel stuck (it's not what you think)
✅ A simple shift that changes everything
✅ How to create momentum that lasts

🎁 Download free below.""",
        headline="Wake Up Excited Again",
        description="Free guide: The 5 Pillars of Personal Transformation",
        tips=[
            "Focus on the emotional outcome",
            "Use sensory language",
            "Make it feel achievable",
            "Be specific about what's inside",
        ],
    ),
    "webinar_registration": AdTemplate(
        name="Webinar/Event Registration",
        platform="Facebook/Instagram",
        objective="Drive registrations for live event",
        structure=[
            "Hook (big promise or curiosity)",
            "What they'll learn",
            "Why now",
            "Who it's for",
            "CTA",
        ],
        primary_text="""FREE MASTERCLASS 🎯

"How to Finally Stop Self-Sabotaging and Start Making Real Progress"

Join me LIVE this Thursday at 7pm ET.

In 60 minutes, you'll discover:

🔹 The hidden pattern keeping you stuck (most women don't even realize they're doing it)

🔹 A simple reframe that instantly changes how you approach challenges

🔹 The 3-step system I use with private clients to create lasting change

This isn't theory. It's the exact process that's helped thousands of women break through.

Spots are limited. Save yours now 👇""",
        headline="Free Masterclass: Stop Self-Sabotaging",
        description="Thursday 7pm ET. Limited spots. Register free.",
        tips=[
            "Create urgency with date/time",
            "List specific takeaways",
            "Mention it's live (increases perceived value)",
            "Keep it focused on one main promise",
        ],
    ),
    "product_launch": AdTemplate(
        name="Product/Program Launch",
        platform="Facebook/Instagram",
        objective="Drive sales for paid offering",
        structure=[
            "Hook (transformation or result)",
            "Story/proof",
            "What's included",
            "Who it's for",
            "Urgency/scarcity (if real)",
            "CTA",
        ],
        primary_text=""""6 months ago, I was exactly where you are. Today, everything is different."

That's what Sarah told me after completing Breakthrough Blueprint.

She went from:
❌ Stuck and spinning her wheels
❌ Doubting herself daily
❌ Watching others succeed

To:
✅ Launched her dream project
✅ 3x'd her income
✅ Confidence she never knew she had

The program that made it possible is open NOW—but only until Friday.

Inside Breakthrough Blueprint:
📚 12 weeks of guided curriculum
💬 Weekly group coaching calls
👥 Private community of action-takers
🎯 Personalized accountability

This is for you if you're ready to stop dabbling and start committing.

Doors close Friday. Will you be inside?""",
        headline="Breakthrough Blueprint Is OPEN",
        description="12-week program. Doors close Friday. Learn more.",
        tips=[
            "Lead with results/transformation",
            "Use specific testimonials",
            "List what's included clearly",
            "Only use scarcity if it's real",
            "Qualify your audience",
        ],
    ),
    "retargeting_reminder": AdTemplate(
        name="Retargeting - Reminder",
        platform="Facebook/Instagram",
        objective="Re-engage warm audience who didn't convert",
        structure=[
            "Acknowledge their interest",
            "Address potential objection",
            "Remind of key benefit",
            "CTA",
        ],
        primary_text="""Still thinking about it?

I get it. Big decisions deserve thoughtful consideration.

But here's what I've learned: the women who transform aren't the ones who wait until they're "ready."

They're the ones who take the leap and figure it out along the way.

If fear is what's holding you back, that's exactly why you need this.

Doors close soon. Your future self will thank you for taking action today.

[Link to program]""",
        headline="Your Spot Is Still Waiting",
        description="Don't let fear make this decision for you.",
        tips=[
            "Be understanding, not pushy",
            "Address the likely objection",
            "Remind of deadline",
            "Keep it short—they already know the offer",
        ],
    ),
}
