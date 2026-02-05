# =============================================================================
# Marketing Assistant AI - Email Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EmailTemplate:
    """Template for a specific email type."""
    name: str
    purpose: str
    subject_line_formulas: List[str]
    structure: List[str]
    example: str
    tips: List[str]


EMAIL_TEMPLATES: Dict[str, EmailTemplate] = {
    "welcome": EmailTemplate(
        name="Welcome Email",
        purpose="Greet new subscribers and set expectations",
        subject_line_formulas=[
            "Welcome to [community name] 💜",
            "You're in! Here's what's next...",
            "So glad you're here, [name]",
            "Your journey starts now",
        ],
        structure=[
            "Warm greeting acknowledging their decision",
            "Set expectations for what they'll receive",
            "Deliver promised lead magnet (if applicable)",
            "Quick personal introduction",
            "Single CTA for next step",
            "Warm sign-off with invitation to reply",
        ],
        example="""Subject: Welcome to the family 💜 Your transformation starts now

Dear friend,

I'm so glad you're here.

You know that feeling when something just clicks? When you realize you're exactly where you need to be? That's what I hope you're feeling right now.

Here's the truth: you didn't find this community by accident. Something within you is ready for change—ready to step into a bigger, bolder version of yourself.

And I'm honored to be part of your journey.

Over the coming weeks, I'll be sharing my most valuable insights on transformation, growth, and creating a life that truly lights you up. These aren't just theories—they're strategies that have helped thousands of women just like you.

To get us started, I have a gift for you: my "5 Pillars of Personal Transformation" guide.

[Download Your Free Guide →]

Remember: the woman you're becoming is already within you. My role is simply to help you see her more clearly.

Here's to your transformation,

Adriana

P.S. I read every reply. Tell me—what brought you here today?""",
        tips=[
            "Make them feel special for joining",
            "Deliver value immediately",
            "Set expectations for future emails",
            "Invite engagement (reply)",
            "Keep it warm but not overwhelming",
        ],
    ),
    "nurture": EmailTemplate(
        name="Nurture/Value Email",
        purpose="Build relationship by providing value without selling",
        subject_line_formulas=[
            "The one thing that changed everything for me",
            "[Name], I noticed something...",
            "A question I keep getting asked",
            "What I wish I knew sooner",
        ],
        structure=[
            "Hook that creates curiosity",
            "Story or insight",
            "Key lesson or takeaway",
            "How they can apply it",
            "Soft CTA (reply, read more, reflect)",
            "Sign-off",
        ],
        example="""Subject: The question I ask myself every morning

Friend,

Can I share something that completely changed my mornings?

For years, I'd wake up and immediately check my phone. Emails. Social media. Everyone else's priorities flooding my brain before I'd even gotten out of bed.

Sound familiar?

Then I learned this one question that changed everything:

"What would make today meaningful?"

Not productive. Not successful. Meaningful.

It's a small shift, but it changed how I approach each day. Instead of reacting to the world's demands, I start by connecting with what matters to me.

Here's my challenge for you: Tomorrow morning, before you reach for your phone, ask yourself this question. 

Then let it guide your first hour.

I'd love to hear what comes up for you—hit reply and let me know.

In your corner,

Adriana""",
        tips=[
            "Lead with value, not sales",
            "Share personal stories that relate",
            "Give actionable takeaways",
            "Keep the conversation going",
            "Build trust through consistency",
        ],
    ),
    "launch": EmailTemplate(
        name="Launch/Sales Email",
        purpose="Announce and sell a product or program",
        subject_line_formulas=[
            "It's finally here...",
            "Doors are open (but not for long)",
            "[Name], your invitation inside",
            "I made something for you",
        ],
        structure=[
            "Story or hook",
            "Problem acknowledgment",
            "Solution introduction",
            "What's included (benefits, not just features)",
            "Who it's for / Who it's not for",
            "Social proof",
            "Clear CTA",
            "Urgency (if authentic)",
        ],
        example="""Subject: She did it. So can you.

Let me tell you about Sarah.

Six months ago, she was where you might be right now—feeling stuck, watching others succeed, wondering if it would ever be "her turn."

She had all the knowledge. Read all the books. Taken all the free courses. But something was missing.

That something? A proven system and someone who believed in her enough to hold her accountable.

Sarah joined my Breakthrough Blueprint program, and within 90 days, she had:
• Launched her dream project
• 3x'd her income  
• Built confidence she never knew she had

Today, I'm opening doors to a new cohort of Breakthrough Blueprint.

This is for you if:
✓ You're tired of going in circles
✓ You know you're capable of more
✓ You're ready to invest in yourself

This is NOT for you if:
✗ You're looking for overnight success
✗ You're not willing to do the work

I only open this program twice a year.

[Learn More About Breakthrough Blueprint →]

What would your life look like in 90 days if you took this step?

Believing in your potential,

Adriana

P.S. Early bird pricing ends Friday. The best time to start was yesterday—the next best time is now.""",
        tips=[
            "Lead with transformation, not features",
            "Use specific testimonials",
            "Be clear about who it's for",
            "Create urgency through opportunity",
            "Don't apologize for selling",
        ],
    ),
    "cart_abandonment": EmailTemplate(
        name="Cart Abandonment Email",
        purpose="Re-engage someone who started but didn't complete purchase",
        subject_line_formulas=[
            "Did something come up?",
            "Your spot is waiting...",
            "A quick question for you",
            "Don't let this slip away",
        ],
        structure=[
            "Acknowledge they were interested",
            "Ask if something came up (without pressure)",
            "Address common objections",
            "Remind of key benefits",
            "Offer help or answers",
            "Clear CTA to return",
        ],
        example="""Subject: Did something come up?

Hey there,

I noticed you were checking out [Program Name] but didn't complete your enrollment.

No pressure—I just wanted to make sure nothing got in the way.

Sometimes life happens. Sometimes we need a moment to think. Sometimes there's a question that needs answering first.

If you have questions, just hit reply. I'm here to help you make the right decision for you—whether that's joining us or not.

A few things that might help:

→ Not sure if it's right for you? Here's who thrives in this program...
→ Worried about the time commitment? Here's what students say...
→ Need a payment plan? We've got options.

Your spot is still available, but enrollment closes [date].

[Complete Your Enrollment →]

Whatever you decide, I'm cheering for you.

Adriana""",
        tips=[
            "Be helpful, not pushy",
            "Address likely objections",
            "Offer genuine support",
            "Remind of deadline without being aggressive",
            "Make it easy to get answers",
        ],
    ),
}
