# =============================================================================
# Marketing Assistant AI - Pydantic Schemas
# =============================================================================
# This module defines all data models used throughout the application.
# Each model is thoroughly documented to explain its purpose and usage.
#
# Schema Categories:
# 1. Enums: Predefined choices (content types)
# 2. Base Models: Shared fields across multiple schemas
# 3. Request Models: Input validation for API endpoints
# 4. Response Models: Output structure for API responses
# 5. Internal Models: Data structures used within services
# =============================================================================

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# =============================================================================
# Enums - Predefined Content Categories
# =============================================================================

class ContentType(str, Enum):
    """
    Enumeration of supported marketing content types.
    
    This enum defines the categories of marketing content that the AI can
    generate. Each type has different structural and tonal requirements.
    
    Types:
        EMAIL: Email campaigns, newsletters, promotional emails
        SOCIAL_MEDIA: Posts for platforms like Instagram, LinkedIn, Twitter
        WEBSITE_COPY: Landing pages, about pages, product descriptions
        FUNNEL_PAGE: Sales funnels, opt-in pages, checkout pages
        AD_COPY: Paid advertisements (Facebook, Google, etc.)
        BLOG_POST: Long-form blog content
        CAMPAIGN: Full marketing campaigns with multiple touchpoints
    
    Example:
        >>> content_type = ContentType.EMAIL
        >>> print(content_type.value)
        'email'
    """
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    WEBSITE_COPY = "website_copy"
    FUNNEL_PAGE = "funnel_page"
    AD_COPY = "ad_copy"
    BLOG_POST = "blog_post"
    CAMPAIGN = "campaign"


# =============================================================================
# Request Models - API Input Validation
# =============================================================================

class GenerationRequest(BaseModel):
    """
    Request model for generating marketing copy.
    
    This model validates the input when a user requests new marketing content.
    It captures all the information the AI needs to generate relevant,
    brand-aligned copy.
    
    Attributes:
        prompt: The user's request describing what content they need.
                Example: "Create an email campaign for our spring sale"
        content_type: The category of content to generate (from ContentType enum)
        target_audience: Description of who the content is for.
                        Helps AI tailor tone and messaging.
        key_points: Specific points or features to include in the content.
                   Optional but helps ensure important info is included.
        tone_override: Optional override for the default Adriana James tone.
                      Use sparingly as brand consistency is important.
        max_length: Approximate maximum length in words.
                   Helps control output size for different use cases.
    
    Example:
        {
            "prompt": "Write a welcome email for new subscribers",
            "content_type": "email",
            "target_audience": "Women interested in personal development",
            "key_points": ["Free ebook offer", "Weekly newsletter benefits"],
            "max_length": 300
        }
    """
    prompt: str = Field(
        ...,  # Required field (no default)
        min_length=10,  # Ensure meaningful input
        max_length=2000,  # Prevent abuse
        description="Description of the marketing content to generate",
        examples=["Create an email campaign for our new product launch"]
    )
    
    content_type: ContentType = Field(
        ...,
        description="Type of marketing content to generate"
    )
    
    target_audience: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of the target audience for this content",
        examples=["Women aged 25-45 interested in personal transformation"]
    )
    
    key_points: Optional[List[str]] = Field(
        default=None,
        max_length=10,  # Limit number of key points
        description="Key points or features to include in the content",
        examples=[["Limited time offer", "Free shipping", "Money-back guarantee"]]
    )
    
    tone_override: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional tone override (default: Adriana James brand voice)",
        examples=["More urgent and action-oriented"]
    )
    
    max_length: Optional[int] = Field(
        default=500,
        ge=50,  # Minimum 50 words
        le=5000,  # Maximum 5000 words
        description="Approximate maximum length in words"
    )


class SimpleGenerationRequest(BaseModel):
    """
    Simplified request model for generation (compatibility with /generate-copy).
    
    This model allows content_type to be omitted, defaulting to CAMPAIGN.
    """
    prompt: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Description of the marketing content to generate",
        examples=["Write a social media post for our new product launch"]
    )
    
    content_type: Optional[ContentType] = Field(
        default=ContentType.CAMPAIGN,
        description="Optional content type (defaults to campaign)"
    )
    
    target_audience: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of the target audience for this content"
    )
    
    key_points: Optional[List[str]] = Field(
        default=None,
        max_length=10,
        description="Key points or features to include in the content"
    )
    
    tone_override: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional tone override (default: Adriana James brand voice)"
    )
    
    max_length: Optional[int] = Field(
        default=500,
        ge=50,
        le=5000,
        description="Approximate maximum length in words"
    )


class TrainingDataCreate(BaseModel):
    """
    Request model for adding new training data (marketing content).
    
    Training data is used to teach the AI about the brand voice and
    provide examples for retrieval-augmented generation (RAG).
    
    Attributes:
        title: A descriptive title for the content piece
        content: The actual marketing content text
        content_type: Category of this content
        metadata: Additional information (campaign name, date, etc.)
        tags: Keywords for easier retrieval and categorization
    
    Example:
        {
            "title": "Spring Sale Email - March 2024",
            "content": "Dear friend, Spring is here and so are amazing deals...",
            "content_type": "email",
            "tags": ["sale", "spring", "promotion"]
        }
    """
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Title or name for this marketing content"
    )
    
    content: str = Field(
        ...,
        min_length=50,  # Meaningful content minimum
        description="The marketing content text"
    )
    
    content_type: ContentType = Field(
        ...,
        description="Type/category of this content"
    )
    
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata (campaign info, dates, etc.)"
    )
    
    tags: Optional[List[str]] = Field(
        default=None,
        description="Tags for categorization and retrieval"
    )


class TrainingDataUpdate(BaseModel):
    """
    Request model for updating existing training data.
    
    All fields are optional - only provided fields will be updated.
    This follows the PATCH semantics for partial updates.
    
    Attributes:
        title: New title (optional)
        content: New content text (optional)
        content_type: New content type (optional)
        metadata: New metadata (optional, replaces existing)
        tags: New tags (optional, replaces existing)
    """
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=200
    )
    
    content: Optional[str] = Field(
        default=None,
        min_length=50
    )
    
    content_type: Optional[ContentType] = None
    
    metadata: Optional[dict] = None
    
    tags: Optional[List[str]] = None


# =============================================================================
# Response Models - API Output Structure
# =============================================================================

class GenerationResponse(BaseModel):
    """
    Response model for generated marketing copy.
    
    This model structures the output when the AI generates new content.
    It includes the generated copy plus metadata about the generation process.
    
    Attributes:
        generated_content: The AI-generated marketing copy
        content_type: Type of content that was generated
        prompt_used: The original prompt (for reference)
        similar_content_used: Titles of retrieved content used as context
        generation_metadata: Information about the generation process
    
    Example Response:
        {
            "generated_content": "Subject: Spring into Savings! ...",
            "content_type": "email",
            "prompt_used": "Create a spring sale email",
            "similar_content_used": ["Past Spring Sale 2023", "Summer Promo"],
            "generation_metadata": {"model": "gpt-4", "tokens_used": 456}
        }
    """
    generated_content: str = Field(
        ...,
        description="The AI-generated marketing copy"
    )
    
    content_type: ContentType = Field(
        ...,
        description="Type of content generated"
    )
    
    prompt_used: str = Field(
        ...,
        description="The original generation prompt"
    )
    
    similar_content_used: List[str] = Field(
        default=[],
        description="Titles of similar content retrieved for context"
    )
    
    generation_metadata: dict = Field(
        default={},
        description="Metadata about the generation process"
    )


class TrainingDataResponse(BaseModel):
    """
    Response model for a single training data item.
    
    Used when creating, retrieving, or updating training data.
    Includes all fields plus system-generated fields like ID and timestamps.
    
    Attributes:
        id: Unique identifier for this content
        title: Content title
        content: The marketing content text
        content_type: Category of the content
        metadata: Additional metadata
        tags: Associated tags
        created_at: When this content was added
        updated_at: When this content was last modified
    """
    id: UUID = Field(
        ...,
        description="Unique identifier"
    )
    
    title: str = Field(
        ...,
        description="Content title"
    )
    
    content: str = Field(
        ...,
        description="Marketing content text"
    )
    
    content_type: ContentType = Field(
        ...,
        description="Content category"
    )
    
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata"
    )
    
    tags: Optional[List[str]] = Field(
        default=None,
        description="Content tags"
    )
    
    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp"
    )


class TrainingDataListResponse(BaseModel):
    """
    Response model for listing multiple training data items.
    
    Used for pagination and bulk retrieval of training data.
    
    Attributes:
        items: List of training data items
        total: Total number of items (for pagination)
        page: Current page number
        page_size: Number of items per page
    """
    items: List[TrainingDataResponse] = Field(
        default=[],
        description="List of training data items"
    )
    
    total: int = Field(
        ...,
        ge=0,
        description="Total number of items"
    )
    
    page: int = Field(
        default=1,
        ge=1,
        description="Current page number"
    )
    
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Items per page"
    )


# =============================================================================
# Internal Models - Used Within Services
# =============================================================================

class MarketingContent(BaseModel):
    """
    Internal model representing a piece of marketing content.
    
    This model is used within the application to represent stored content.
    It includes all data needed for storage, retrieval, and display.
    
    Attributes:
        id: Unique identifier
        title: Content title
        content: The marketing text
        content_type: Category
        metadata: Additional info
        tags: Keywords
        embedding: Vector embedding (for similarity search)
        created_at: Creation time
        updated_at: Last modification time
    """
    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    content_type: ContentType
    metadata: Optional[dict] = None
    tags: Optional[List[str]] = None
    embedding: Optional[List[float]] = None  # Vector embedding
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration for this model."""
        # Allow arbitrary types (needed for some internal use cases)
        arbitrary_types_allowed = True


class RetrievedContent(BaseModel):
    """
    Model for content retrieved from the vector store.
    
    When we search for similar content, this model represents
    each retrieved item along with its relevance score.
    
    Attributes:
        content: The marketing content object
        similarity_score: How similar this is to the query (0-1)
        rerank_score: Score after re-ranking (if applied)
    """
    content: MarketingContent = Field(
        ...,
        description="The retrieved marketing content"
    )
    
    similarity_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Similarity score from vector search (0-1)"
    )
    
    rerank_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Re-ranking score (if re-ranking was applied)"
    )
