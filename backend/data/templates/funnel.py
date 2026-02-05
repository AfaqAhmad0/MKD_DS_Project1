# =============================================================================
# Marketing Assistant AI - Funnel Page Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class FunnelTemplate:
    """Template for funnel page."""
    name: str
    funnel_stage: str
    purpose: str
    sections: List[str]
    example: str


FUNNEL_TEMPLATES: Dict[str, FunnelTemplate] = {
    "lead_magnet_optin": FunnelTemplate(
        name="Lead Magnet Opt-in Page",
        funnel_stage="Top of Funnel",
        purpose="Capture email in exchange for free resource",
        sections=[
            "Headline (benefit-driven)",
            "Subheadline (what they get)",
            "Bullet points (specific benefits)",
            "Opt-in form",
            "Trust elements",
            "About the author (brief)",
        ],
        example="""# 5 Pillars of Personal Transformation
## The Framework That Changed Everything

**Free guide reveals the exact system I used to go from burnt out to thriving—and how you can too.**

---

You're working hard. Doing "all the right things." But something still feels... off.

Here's the truth: it's not about working harder. It's about working smarter.

### Inside This Free Guide, You'll Discover:

✓ **Pillar 1: Clarity** — How to cut through confusion and identify exactly what you want

✓ **Pillar 2: Strategy** — The simple framework for reverse-engineering any goal

✓ **Pillar 3: Environment** — Why willpower always fails (and what to do instead)

✓ **Pillar 4: Accountability** — The type of support that actually works

✓ **Pillar 5: Momentum** — How to maintain progress even when motivation fades

---

### Get Instant Access

[Email Address]
[Send Me the Guide →]

*Join 50,000+ women committed to transformation*

---

**About Adriana James**

Adriana has helped over 10,000 women transform their lives through her proven frameworks. Featured in Forbes, Entrepreneur, and The Today Show.

*"This guide was the starting point of everything for me."* — Sarah M.""",
    ),
    "webinar_registration": FunnelTemplate(
        name="Webinar Registration Page",
        funnel_stage="Middle of Funnel",
        purpose="Get registrations for live training",
        sections=[
            "Headline (big promise)",
            "Date/time prominently displayed",
            "What they'll learn (3-5 points)",
            "Who this is for",
            "About the host",
            "Registration form",
            "Urgency element",
        ],
        example="""# FREE MASTERCLASS

## How to Finally Break Free From Self-Sabotage and Create the Life You Actually Want

**Live Training: Thursday, March 15th at 7pm ET**

[Reserve My Spot →]

---

### In This 60-Minute Training, You'll Discover:

🎯 **The Hidden Pattern** — Why you keep getting in your own way (and how to stop)

🎯 **The Clarity Method** — A simple process to know exactly what you want and how to get it

🎯 **The Action Framework** — How to take consistent action without burning out

🎯 **The Support System** — Why you can't do this alone and how to build your team

---

### This Masterclass Is For You If:

✓ You feel stuck and don't know why
✓ You've tried "everything" but nothing sticks
✓ You know you're capable of more
✓ You're ready to stop dreaming and start doing

---

### Meet Your Host

**Adriana James** has helped over 10,000 women transform their lives through her proven frameworks and supportive programs.

After burning out in corporate America, Adriana discovered the principles she now teaches. Today, she's dedicated to helping other women avoid the same mistakes she made.

---

### Save Your Spot Now

This training is FREE but space is limited.

[Your Name]
[Your Email]
[Reserve My Spot →]

**Can't make it live?** Register anyway and we'll send you the replay.""",
    ),
    "sales_page_long": FunnelTemplate(
        name="Long-Form Sales Page",
        funnel_stage="Bottom of Funnel",
        purpose="Convert warm leads to buyers",
        sections=[
            "Headline (transformation)",
            "Opening story/hook",
            "Problem agitation",
            "Solution introduction",
            "What's included",
            "Bonuses",
            "Who it's for / not for",
            "Testimonials",
            "About the creator",
            "FAQ",
            "Guarantee",
            "Final CTA",
            "P.S.",
        ],
        example="""# Finally... A Proven Path to Breaking Through

## Without the overwhelm, confusion, or going it alone

[Enroll Now →]

---

Let me guess...

You've read the books. Taken the courses. Made the vision boards.

But somehow, you're still stuck.

Still watching others succeed while you spin your wheels.

Still wondering if it will ever be "your turn."

I get it. I was there too.

---

## Here's What Nobody Tells You

The problem isn't information. You have plenty of that.

The problem is **implementation**.

You need a system. A community. And someone who's been where you're going to show you the way.

That's exactly why I created...

---

# Breakthrough Blueprint

## The 12-Week Transformation Program

A step-by-step system to finally break through your blocks and create the life you've been dreaming about.

[Enroll Now — Doors Close Friday →]

---

## Here's What You Get Inside:

### Module 1: Clarity
Define exactly what you want and why it matters

### Module 2: Mindset
Rewire the beliefs holding you back

### Module 3: Strategy
Create your personalized action plan

[... additional modules ...]

---

## Plus These Bonuses (Worth $2,000+)

🎁 **BONUS 1:** Private Podcast Feed ($297 value)
🎁 **BONUS 2:** Quarterly Planning Workshop ($497 value)
🎁 **BONUS 3:** Resource Library Access ($297 value)

---

## This Is For You If:

✓ You're done with dabbling and ready to commit
✓ You know you're capable of more
✓ You want structure AND flexibility
✓ You thrive with community support

## This Is NOT For You If:

✗ You're looking for a magic pill
✗ You're not willing to do the work
✗ You expect overnight results

---

## What Past Students Say

[Testimonials section]

---

## Your Investment

**Breakthrough Blueprint**

$1,997 one-time
or 3 payments of $697

[Enroll Now →]

---

## 30-Day Money-Back Guarantee

Try the program risk-free. If you do the work and don't see results within 30 days, I'll refund your investment. No questions asked.

---

## Frequently Asked Questions

**Q: How much time does this require?**
A: Plan for 3-5 hours per week...

**Q: What if I fall behind?**
A: You have lifetime access...

---

[Final CTA]

P.S. — A year from now, you'll wish you had started today. This is your moment. Don't let it pass.""",
    ),
    "thank_you_page": FunnelTemplate(
        name="Thank You / Confirmation Page",
        funnel_stage="Post-Conversion",
        purpose="Confirm action and set up next step",
        sections=[
            "Confirmation message",
            "What to expect next",
            "Next step CTA",
            "Share buttons (optional)",
            "Additional resource (optional)",
        ],
        example="""# You're In! 🎉

## Check your inbox for your free guide.

While you wait, here's something else I think you'll love...

---

### Your Next Step

Join me for a FREE live training where I'll walk you through how to implement everything in the guide.

**"How to Finally Break Free From Self-Sabotage"**

Thursday, March 15th at 7pm ET

[Save My Spot →]

---

### Spread the Word

Know someone who needs this? Share the guide:

[Facebook] [Twitter] [Email]

---

### Connect With Me

📧 Email: hello@adrianajames.com
📱 Instagram: @adrianajames

See you inside!

Adriana""",
    ),
}
