# =============================================================================
# Marketing Assistant AI - Social Media Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SocialTemplate:
    """Template for a social media post type."""
    name: str
    platform: str
    purpose: str
    structure: List[str]
    example: str
    hashtag_suggestions: List[str]


SOCIAL_MEDIA_TEMPLATES: Dict[str, SocialTemplate] = {
    "linkedin_story": SocialTemplate(
        name="LinkedIn Personal Story",
        platform="LinkedIn",
        purpose="Build authority and connection through personal narrative",
        structure=[
            "Hook (surprising statement or question)",
            "Setup (the before/context)",
            "Conflict/challenge",
            "Resolution/lesson",
            "Takeaway for audience",
            "Engagement prompt",
        ],
        example="""I got fired at 28. It was the best thing that ever happened to me.

At the time, I thought my world was ending. My identity was wrapped up in that job title, that paycheck, that daily routine.

But losing everything forced me to ask: Who am I without this?

The answer changed my life.

I realized I'd been playing small. Following someone else's script. Living for validation instead of purpose.

15 years later, I've built a business that impacts thousands of women. Not despite getting fired—because of it.

If you're going through a professional setback right now, here's what I want you to know:

This is not the end of your story. It's the beginning of a better chapter.

What setback turned into a setup for you? I'd love to hear in the comments.

#CareerAdvice #Resilience #ProfessionalDevelopment #WomenInBusiness""",
        hashtag_suggestions=[
            "#CareerAdvice",
            "#ProfessionalGrowth",
            "#WomenInBusiness",
            "#Leadership",
            "#PersonalBranding",
        ],
    ),
    "instagram_motivation": SocialTemplate(
        name="Instagram Motivational Post",
        platform="Instagram",
        purpose="Inspire and engage through relatable motivation",
        structure=[
            "Hook (first line stops the scroll)",
            "Expand on the hook",
            "Personal touch or story",
            "Call to action or question",
            "Hashtags",
        ],
        example="""The question isn't "Can I do this?"

The question is "What's stopping me from trying?"

Every woman I've worked with who achieved extraordinary things started with the same doubts you have right now.

The difference? They moved forward anyway.

Today, I challenge you: identify ONE thing you've been putting off because of fear. Then take ONE small step toward it.

That's it. One step.

You might surprise yourself. 💜

Drop a 🙋‍♀️ if you're ready to take that step today.

#TransformationTuesday #PersonalGrowth #WomenEmpowerment #MindsetShift #MotivationDaily""",
        hashtag_suggestions=[
            "#PersonalGrowth",
            "#WomenEmpowerment",
            "#Motivation",
            "#MindsetMatters",
            "#SelfDevelopment",
        ],
    ),
    "instagram_educational": SocialTemplate(
        name="Instagram Educational Carousel",
        platform="Instagram",
        purpose="Provide value through educational content",
        structure=[
            "Cover slide with curiosity hook",
            "Problem statement",
            "Solution/framework intro",
            "Step-by-step breakdown (3-7 slides)",
            "Summary slide",
            "CTA slide",
        ],
        example="""[SLIDE 1 - COVER]
5 Reasons Your Goals Fail
(And what to do instead)

[SLIDE 2]
Setting goals isn't the problem.

The problem is HOW most people set them.

Here's what's actually sabotaging your success...

[SLIDE 3]
❌ Mistake #1: Too vague

"I want to be healthier" gives your brain nothing to work with.

✅ Instead: "I will walk for 20 minutes every morning"

[SLIDE 4]
❌ Mistake #2: No emotional connection

If you don't feel it, you won't do it.

✅ Instead: Connect to WHY this matters to you

[SLIDE 5]
❌ Mistake #3: All or nothing thinking

One missed day doesn't mean failure.

✅ Instead: Plan for setbacks in advance

[SLIDE 6]
❌ Mistake #4: No environment design

Willpower always loses to environment.

✅ Instead: Make the right choice the easy choice

[SLIDE 7]
❌ Mistake #5: Going alone

You need support and accountability.

✅ Instead: Find your people

[SLIDE 8]
Save this post for your next goal-setting session.

And if you want my complete goal-setting framework, link in bio 🔗""",
        hashtag_suggestions=[
            "#GoalSetting",
            "#ProductivityTips",
            "#SelfImprovement",
            "#SuccessMindset",
            "#PersonalDevelopment",
        ],
    ),
    "twitter_thread": SocialTemplate(
        name="Twitter/X Thread",
        platform="Twitter/X",
        purpose="Share insights in a digestible thread format",
        structure=[
            "Hook tweet (curiosity or bold statement)",
            "Context/setup",
            "Main points (one per tweet)",
            "Summary/conclusion",
            "CTA",
        ],
        example="""🧵 I've helped 1000+ women build their businesses.

Here are 7 lessons I wish I could tell my younger self:

(Thread)

1/ Start before you're ready.

There will never be a "perfect" time. The best time to start is always now, even if you're scared.

2/ Your first version will be terrible.

And that's okay. Ship it anyway. You can't iterate on something that doesn't exist.

3/ Charge more than you think you should.

Women consistently undercharge. Your expertise has value. Price accordingly.

4/ Your network is your net worth.

Invest in relationships. Help others generously. The opportunities that change your life come from people.

5/ Rest is productive.

Burnout is not a badge of honor. The best ideas come when you're rested, not running on empty.

6/ Not everyone will like you.

That's a sign you're doing something meaningful. Don't dilute your message to please everyone.

7/ Trust your gut.

You know more than you think. Stop waiting for permission. You are the expert of your own life.

Which of these resonates most? Reply and let me know 👇""",
        hashtag_suggestions=[
            "#Entrepreneurship",
            "#WomenInBusiness",
            "#StartupAdvice",
            "#BusinessTips",
        ],
    ),
    "facebook_community": SocialTemplate(
        name="Facebook Community Post",
        platform="Facebook",
        purpose="Foster engagement and discussion in groups/pages",
        structure=[
            "Relatable opening",
            "Story or observation",
            "Question or discussion prompt",
            "Invitation to share",
        ],
        example="""Real talk for a minute...

I was coaching a client yesterday and she said something that stopped me:

"I feel like I'm the only one who doesn't have it together."

I hear this SO often. And here's what I told her:

Nobody has it all together. Not me. Not the people you admire on social media. Nobody.

We're all figuring it out as we go. Some of us are just better at hiding the mess. 😅

So today, I want to normalize this:

What's ONE thing you're currently figuring out? No judgment, just honesty.

I'll go first: I'm figuring out how to set better boundaries with my time. Still a work in progress.

Your turn 👇""",
        hashtag_suggestions=[
            "#RealTalk",
            "#CommunitySupport",
            "#WomenSupportingWomen",
        ],
    ),
}
