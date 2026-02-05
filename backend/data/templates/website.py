# =============================================================================
# Marketing Assistant AI - Website Copy Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class WebsiteTemplate:
    """Template for website copy."""
    name: str
    page_type: str
    purpose: str
    sections: List[str]
    example: str


WEBSITE_TEMPLATES: Dict[str, WebsiteTemplate] = {
    "homepage_hero": WebsiteTemplate(
        name="Homepage Hero Section",
        page_type="Homepage",
        purpose="Capture attention and communicate core value proposition",
        sections=[
            "Headline (main benefit/transformation)",
            "Subheadline (supporting detail)",
            "Primary CTA button",
            "Secondary CTA (optional)",
            "Trust indicators (optional)",
        ],
        example="""# Transform Your Potential Into Reality

You know you're capable of more. Let's unlock it together.

[Start Your Journey →]

*Join 10,000+ women who've already transformed their lives*""",
    ),
    "about_page": WebsiteTemplate(
        name="About Page",
        page_type="About",
        purpose="Build connection and establish credibility",
        sections=[
            "Opening hook (relatable statement)",
            "Personal story (struggle to success)",
            "Mission and values",
            "Credentials/experience",
            "Who I help",
            "CTA to take next step",
        ],
        example="""# Hi, I'm Adriana.

## And I believe you're capable of more than you know.

For the past 15 years, I've dedicated my life to one mission: helping women transform their potential into reality.

Not through empty motivation. Not through wishful thinking. Through proven systems, genuine support, and the kind of accountability that actually works.

### My Story

I didn't always have this figured out.

At 28, I was burnt out, broke, and questioning everything. The corporate career I'd worked so hard for felt meaningless. My relationships were suffering. My health was declining.

Something had to change.

What followed was a five-year journey of discovery—studying psychology, working with mentors, and testing everything I learned on myself first.

The transformation wasn't overnight. But it was real.

### What I Do

I help ambitious women who are:
- Stuck in careers that don't fulfill them
- Struggling to balance success and wellbeing
- Ready for a breakthrough but don't know where to start

Through my programs, speaking, and content, I provide:
- **Proven frameworks** that create lasting change
- **Supportive community** of like-minded women
- **Accountability systems** that keep you moving forward

### Ready to Begin?

Your transformation starts with a single step.

[Explore My Programs →]""",
    ),
    "services_page": WebsiteTemplate(
        name="Services/Programs Page",
        page_type="Services",
        purpose="Showcase offerings and guide visitors to right option",
        sections=[
            "Introduction (who you help)",
            "Program 1 overview",
            "Program 2 overview",
            "Comparison/guide to choosing",
            "Testimonials",
            "FAQ",
            "CTA",
        ],
        example="""# Programs Designed for Your Transformation

Everyone's journey is different. That's why I offer multiple ways to work together—so you can choose what fits your life, goals, and budget.

---

## Breakthrough Blueprint
**For women ready to go all-in on transformation**

A 12-week intensive program that gives you the framework, support, and accountability to create lasting change.

✓ Weekly group coaching calls
✓ Step-by-step curriculum
✓ Private community access
✓ Personalized support

**Investment:** $1,997 or 3 payments of $697

[Learn More →]

---

## The Inner Circle
**For women who want ongoing support**

Monthly membership with continuous access to coaching, community, and resources.

✓ Monthly group coaching
✓ Resource library
✓ Community forum
✓ Member-only events

**Investment:** $97/month

[Join Now →]

---

## Not sure which is right for you?

**Choose Breakthrough Blueprint if:** You're ready for intensive transformation and want a structured program with clear milestones.

**Choose The Inner Circle if:** You want flexible, ongoing support and prefer to go at your own pace.

[Still unsure? Book a free call →]""",
    ),
    "testimonials_section": WebsiteTemplate(
        name="Testimonials Section",
        page_type="Any",
        purpose="Build trust through social proof",
        sections=[
            "Section headline",
            "Featured testimonials (3-5)",
            "Mix of text and video if available",
            "Specific results mentioned",
            "CTA",
        ],
        example="""## What Our Community Says

---

> "I went from feeling completely stuck to launching my dream business in 90 days. Adriana's framework gave me the clarity and confidence I needed. I can't believe how much has changed."

**Sarah M.** — Entrepreneur | 3x'd her income

---

> "This program changed how I show up in every area of my life. The community alone is worth it—finally being around women who get it."

**Jennifer K.** — Marketing Director | Found work-life balance

---

> "I was skeptical at first. I'd tried so many things. But this was different. Adriana actually gets it, and her methods actually work."

**Maria L.** — Coach | Built her first $10K month

---

[Start Your Own Transformation →]""",
    ),
    "contact_page": WebsiteTemplate(
        name="Contact Page",
        page_type="Contact",
        purpose="Make it easy to get in touch",
        sections=[
            "Warm greeting",
            "What to expect",
            "Contact form",
            "Alternative contact methods",
            "FAQ for common questions",
        ],
        example="""# Let's Connect

Have a question? Want to explore working together? I'd love to hear from you.

## Get in Touch

Fill out the form below and I'll get back to you within 2 business days.

[Contact Form]
- Name
- Email
- What can I help you with?
- Message

---

## Other Ways to Reach Me

📧 **Email:** hello@adrianajames.com
📱 **Instagram:** @adrianajames

---

## Quick Answers

**Q: Do you offer 1:1 coaching?**
A: Currently, I focus on group programs which provide both personalized support and community connection. [Learn about my programs →]

**Q: Can I hire you to speak at my event?**
A: I love speaking! [Fill out this form →] with details about your event.

**Q: I'm a member of a program and need support.**
A: Please reach out in the member community or email support@adrianajames.com.""",
    ),
}
