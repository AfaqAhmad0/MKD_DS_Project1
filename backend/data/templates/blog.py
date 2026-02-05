# =============================================================================
# Marketing Assistant AI - Blog Post Templates
# =============================================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BlogTemplate:
    """Template for blog post type."""
    name: str
    post_type: str
    purpose: str
    structure: List[str]
    example_outline: str
    seo_tips: List[str]


BLOG_TEMPLATES: Dict[str, BlogTemplate] = {
    "how_to": BlogTemplate(
        name="How-To Guide",
        post_type="Educational",
        purpose="Teach a specific skill or process",
        structure=[
            "Headline with benefit",
            "Introduction (problem + promise)",
            "Why this matters",
            "Step-by-step instructions",
            "Common mistakes to avoid",
            "Pro tips",
            "Conclusion with CTA",
        ],
        example_outline="""# How to [Achieve Desired Outcome] in [Timeframe]

## Introduction
- Hook: The struggle your reader faces
- Promise: What they'll learn
- Why you're qualified to teach this

## Why [Topic] Matters
- The cost of not doing this
- The benefits of getting it right

## Step 1: [First Step]
- What to do
- How to do it
- Example

## Step 2: [Second Step]
[Continue pattern...]

## Common Mistakes to Avoid
- Mistake 1 and how to fix it
- Mistake 2 and how to fix it
- Mistake 3 and how to fix it

## Pro Tips
- Advanced tip for better results
- Time-saving hack
- What experts do differently

## Conclusion
- Recap key points
- Encouragement
- CTA to related resource/program""",
        seo_tips=[
            "Include primary keyword in headline",
            "Use numbered steps for featured snippets",
            "Add internal links to related content",
            "Include images for each major step",
            "Target long-tail question keywords",
        ],
    ),
    "listicle": BlogTemplate(
        name="Listicle",
        post_type="Educational/Entertainment",
        purpose="Provide value in scannable format",
        structure=[
            "Headline with number",
            "Introduction",
            "List items (each with subheading)",
            "Bonus item (optional)",
            "Conclusion",
        ],
        example_outline="""# [Number] [Topic] That Will [Benefit]

## Introduction
- Why this list matters
- How to use it

## 1. [First Item]
- Explanation
- Example
- How to implement

## 2. [Second Item]
[Continue pattern...]

## Bonus: [Extra Item]
- Why it's a bonus
- Implementation

## Conclusion
- Key takeaway
- CTA""",
        seo_tips=[
            "Odd numbers perform better (7, 9, 11)",
            "Include the number in the title",
            "Make items scannable with bold text",
            "Each item should stand alone",
            "Link to detailed posts for each item",
        ],
    ),
    "personal_story": BlogTemplate(
        name="Personal Story/Lesson",
        post_type="Connection Building",
        purpose="Build trust through vulnerability and shared experience",
        structure=[
            "Headline (curiosity or outcome)",
            "Scene-setting opening",
            "The story (challenge/conflict)",
            "The turning point",
            "Lessons learned",
            "How this applies to reader",
            "CTA",
        ],
        example_outline="""# [Curiosity-Driving Headline]

## The Scene
- Set up the situation
- Create vivid imagery
- Make it relatable

## The Challenge
- What happened
- How you felt
- The struggle

## The Turning Point
- What changed
- The realization
- The decision

## What I Learned
- Lesson 1
- Lesson 2
- Lesson 3

## What This Means for You
- How this applies to reader
- Action they can take
- Permission or encouragement

## Conclusion
- Wrap up the story
- Inspiring close
- CTA""",
        seo_tips=[
            "Optimize for emotional keywords",
            "Include the lesson in meta description",
            "Use story keywords people search",
            "Add relevant images",
            "Link to related actionable content",
        ],
    ),
    "comparison": BlogTemplate(
        name="Comparison/Versus Post",
        post_type="Decision Support",
        purpose="Help readers make decisions by comparing options",
        structure=[
            "Headline (X vs Y)",
            "Introduction (why this comparison matters)",
            "Quick answer (for those in a hurry)",
            "Overview of Option A",
            "Overview of Option B",
            "Detailed comparison",
            "Recommendation by use case",
            "Conclusion",
        ],
        example_outline="""# [Option A] vs [Option B]: Which Is Right for You?

## Introduction
- Why you're making this comparison
- Who this is for

## Quick Answer
- TL;DR recommendation
- Table summary

## What Is [Option A]?
- Overview
- Key features
- Best for

## What Is [Option B]?
- Overview
- Key features
- Best for

## Head-to-Head Comparison

### [Criterion 1]
- Option A: [Rating/Analysis]
- Option B: [Rating/Analysis]
- Winner: [Which and why]

[Continue for each criterion...]

## The Verdict

### Choose [Option A] if:
- Bullet points

### Choose [Option B] if:
- Bullet points

## Conclusion
- Final recommendation
- CTA""",
        seo_tips=[
            "Target 'vs' and 'versus' keywords",
            "Include comparison tables",
            "Answer the question early for featured snippets",
            "Be fair and balanced",
            "Include affiliate links if relevant",
        ],
    ),
    "problem_solution": BlogTemplate(
        name="Problem-Solution",
        post_type="Educational",
        purpose="Address a specific pain point and provide solution",
        structure=[
            "Headline (problem-focused)",
            "Problem description (empathy)",
            "Why common solutions don't work",
            "The real solution",
            "How to implement",
            "Results to expect",
            "CTA",
        ],
        example_outline="""# Why [Problem] Happens (And How to Fix It)

## Introduction
- Acknowledge the problem
- Show you understand the frustration

## Why [Problem] Is So Common
- Root causes
- What makes it worse
- Why it persists

## What Most People Try (And Why It Doesn't Work)
- Common approach 1 - why it fails
- Common approach 2 - why it fails
- Common approach 3 - why it fails

## The Real Solution
- Core insight
- Why this works
- Overview of approach

## How to Implement This

### Step 1
[Details]

### Step 2
[Details]

### Step 3
[Details]

## What to Expect
- Timeline
- Signs of progress
- What success looks like

## Conclusion
- Encouragement
- CTA""",
        seo_tips=[
            "Target problem-focused keywords",
            "Include 'why' and 'how to fix'",
            "Address related problems",
            "Link to deeper resources",
            "Include success indicators",
        ],
    ),
}
