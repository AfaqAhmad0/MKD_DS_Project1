# =============================================================================
# Marketing Assistant AI - Sample Marketing Content
# =============================================================================

from backend.models.schemas import ContentType


SAMPLE_MARKETING_CONTENT = [
    {
        "title": "Welcome Email - New Subscriber",
        "content": """Subject: Welcome to the family 💜 Your transformation starts now

Dear friend,

I'm so glad you're here.

You know that feeling when something just clicks? When you realize you're exactly where you need to be? That's what I hope you're feeling right now.

Here's the truth: you didn't find this community by accident. Something within you is ready for change—ready to step into a bigger, bolder version of yourself.

And I'm honored to be part of your journey.

Over the coming weeks, I'll be sharing my most valuable insights on transformation, growth, and creating a life that truly lights you up.

To get us started, I have a gift for you: my "5 Pillars of Personal Transformation" guide.

[Download Your Free Guide →]

Remember: the woman you're becoming is already within you. My role is simply to help you see her more clearly.

Here's to your transformation,

Adriana

P.S. I read every reply. If there's something specific you're working through, hit reply and tell me.""",
        "content_type": ContentType.EMAIL,
        "tags": ["welcome", "onboarding", "introduction"],
        "metadata": {"email_type": "welcome", "sequence": "onboarding"}
    },
    {
        "title": "Nurture Email - Morning Routine Tip",
        "content": """Subject: The question I ask myself every morning

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
        "content_type": ContentType.EMAIL,
        "tags": ["nurture", "value", "morning routine", "mindset"],
        "metadata": {"email_type": "nurture", "topic": "productivity"}
    },
    {
        "title": "Launch Email - Course Announcement",
        "content": """Subject: She did it. So can you.

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

I only open this program twice a year.

[Learn More About Breakthrough Blueprint →]

What would your life look like in 90 days if you took this step?

Believing in your potential,

Adriana""",
        "content_type": ContentType.EMAIL,
        "tags": ["launch", "sales", "course", "testimonial"],
        "metadata": {"email_type": "launch", "product": "Breakthrough Blueprint"}
    },
    {
        "title": "Instagram - Motivation Monday",
        "content": """The question isn't "Can I do this?"

The question is "What's stopping me from trying?"

Every woman I've worked with who achieved extraordinary things started with the same doubts you have right now.

The difference? They moved forward anyway.

Today, I challenge you: identify ONE thing you've been putting off because of fear. Then take ONE small step toward it.

That's it. One step.

You might surprise yourself. 💜

Drop a 🙋‍♀️ if you're ready to take that step today.

#TransformationTuesday #PersonalGrowth #WomenEmpowerment #MindsetShift""",
        "content_type": ContentType.SOCIAL_MEDIA,
        "tags": ["instagram", "motivation", "engagement"],
        "metadata": {"platform": "Instagram", "post_type": "motivational"}
    },
    {
        "title": "LinkedIn - Professional Story",
        "content": """I got fired at 28. It was the best thing that ever happened to me.

At the time, I thought my world was ending. My identity was wrapped up in that job title, that paycheck, that daily routine.

But losing everything forced me to ask: Who am I without this?

The answer changed my life.

I realized I'd been playing small. Following someone else's script. Living for validation instead of purpose.

15 years later, I've built a business that impacts thousands of women. Not despite getting fired—because of it.

If you're going through a professional setback right now, here's what I want you to know:

This is not the end of your story. It's the beginning of a better chapter.

What setback turned into a setup for you?

#CareerAdvice #Resilience #ProfessionalDevelopment #WomenInBusiness""",
        "content_type": ContentType.SOCIAL_MEDIA,
        "tags": ["linkedin", "story", "professional", "resilience"],
        "metadata": {"platform": "LinkedIn", "post_type": "personal_story"}
    },
    {
        "title": "Homepage Hero Section",
        "content": """# Transform Your Potential Into Reality

You know you're capable of more. Let's unlock it together.

For the past 15 years, I've helped thousands of women break through their limitations and create lives they love.

Not through wishful thinking. Through proven systems, genuine support, and the kind of accountability that actually works.

[Start Your Journey →]

*Join 10,000+ women who've already transformed their lives*""",
        "content_type": ContentType.WEBSITE_COPY,
        "tags": ["homepage", "hero", "value proposition"],
        "metadata": {"page": "homepage", "section": "hero"}
    },
    {
        "title": "About Page - Full",
        "content": """# Hi, I'm Adriana.

## And I believe you're capable of more than you know.

For the past 15 years, I've dedicated my life to one mission: helping women transform their potential into reality.

### My Story

I didn't always have this figured out.

At 28, I was burnt out, broke, and questioning everything. The corporate career I'd worked so hard for felt meaningless.

Something had to change.

What followed was a five-year journey of discovery—studying psychology, working with mentors, and testing everything I learned on myself first.

The transformation wasn't overnight. But it was real.

### What I Do

I help ambitious women who are:
- Stuck in careers that don't fulfill them
- Struggling to balance success and wellbeing
- Ready for a breakthrough but don't know where to start

Through my programs, I provide:
- **Proven frameworks** that create lasting change
- **Supportive community** of like-minded women
- **Accountability systems** that keep you moving forward

### Ready to Begin?

[Explore My Programs →]""",
        "content_type": ContentType.WEBSITE_COPY,
        "tags": ["about", "bio", "story"],
        "metadata": {"page": "about", "section": "main"}
    },
    {
        "title": "Lead Magnet Landing Page",
        "content": """# 5 Pillars of Personal Transformation
## The Framework That Changed Everything

**Free guide reveals the exact system I used to go from burnt out to thriving.**

---

You're working hard. Doing "all the right things." But something still feels... off.

Here's the truth: it's not about working harder. It's about working smarter.

### Inside This Free Guide:

✓ **Pillar 1: Clarity** — How to identify exactly what you want

✓ **Pillar 2: Strategy** — The framework for reverse-engineering any goal

✓ **Pillar 3: Environment** — Why willpower fails and what to do instead

✓ **Pillar 4: Accountability** — The support that actually works

✓ **Pillar 5: Momentum** — How to maintain progress when motivation fades

### Get Instant Access

[Email Address]
[Send Me the Guide →]

*Join 50,000+ women committed to transformation*""",
        "content_type": ContentType.FUNNEL_PAGE,
        "tags": ["lead magnet", "opt-in", "landing page"],
        "metadata": {"funnel_stage": "top", "offer": "free guide"}
    },
    {
        "title": "Facebook Ad - Lead Gen",
        "content": """🛑 Stop scrolling. This is for you.

You've tried the productivity hacks. The morning routines. The vision boards.

But you're still not where you want to be.

Here's the thing no one tells you: transformation isn't about adding more. It's about doing the RIGHT things in the RIGHT order.

I've helped 10,000+ women break through—and I put my entire framework in a free guide.

No fluff. Just the 5 pillars that actually create change.

🎁 Grab your free copy below.

#PersonalGrowth #WomenEmpowerment #FreeGuide""",
        "content_type": ContentType.AD_COPY,
        "tags": ["facebook", "lead gen", "free offer"],
        "metadata": {"platform": "Facebook", "objective": "lead_generation"}
    },
    {
        "title": "Blog Post - Why Goals Fail",
        "content": """# Why Your Goals Aren't Working (And What to Do Instead)

Every January, millions of people set goals. By February, most have given up.

If this sounds familiar, I want you to know: it's not your fault.

The problem isn't your willpower. It's the goal-setting advice you've been following.

## The Traditional Approach Is Broken

We've been taught to set SMART goals—Specific, Measurable, Achievable, Relevant, Time-bound.

Sounds logical, right?

But here's what that approach misses: human beings aren't logical. We're emotional.

## What Actually Works

### 1. Connect to the Feeling

Instead of "I want to lose 20 pounds," try "I want to wake up feeling energized and confident."

The feeling pulls you forward when motivation fades.

### 2. Design Your Environment

Willpower is limited. Make the right choice the easy choice.

### 3. Build Identity, Not Just Habits

Ask "Who do I need to become?" not just "What should I do?"

## Your Next Step

Take ONE goal you've been struggling with and apply these three shifts.

[Download my free goal-setting framework →]

What goal are you going to transform? Let me know in the comments.""",
        "content_type": ContentType.BLOG_POST,
        "tags": ["goals", "productivity", "mindset", "how-to"],
        "metadata": {"category": "Personal Development", "word_count": 300}
    },
    {
        "title": "Spring Renewal Campaign - Email Sequence",
        "content": """# Spring Renewal Campaign

## Campaign Overview
7-day campaign encouraging women to embrace spring as a time for personal transformation.

## Theme: "Spring Into the New You"

---

## Email 1: Awareness (Day 1)
Subject: Spring is here. Are you?

Spring doesn't just happen to flowers. It can happen to you, too.

After the heaviness of winter, there's something powerful about this season of renewal.

This week, I'm sharing my Spring Renewal framework. Stay tuned.

---

## Email 2: Education (Day 3)
Subject: The 3 areas to focus on this spring

My Spring Renewal Framework:
1. Clear the clutter
2. Plant new seeds
3. Nurture growth

[Learn More →]

---

## Email 3: Social Proof (Day 5)
Subject: "This changed my spring—and my year."

[Success story from Maria]

---

## Email 4: Offer (Day 6)
Subject: Doors are open (48 hours only)

Spring Renewal enrollment is now open.

---

## Email 5: Last Chance (Day 7)
Subject: Final hours

Enrollment closes tonight.""",
        "content_type": ContentType.CAMPAIGN,
        "tags": ["campaign", "email sequence", "launch", "seasonal"],
        "metadata": {"campaign_name": "Spring Renewal", "duration": "7 days"}
    },
]
