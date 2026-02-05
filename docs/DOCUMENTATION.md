# Marketing Assistant AI - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Configuration Files](#configuration-files)
4. [Application Core](#application-core)
5. [Models (Schemas)](#models-schemas)
6. [Services](#services)
7. [API Routers](#api-routers)
8. [Brand Data](#brand-data)
9. [Templates](#templates)
10. [Sample Content](#sample-content)
11. [How-To Guides](#how-to-guides)

---

## Project Overview

**Marketing Assistant AI** is an AI-powered tool for generating marketing copy aligned with Adriana James' brand voice. It uses:

- **FastAPI** for the REST API backend
- **FAISS** for vector similarity search
- **Cohere** for embeddings and re-ranking
- **Hugging Face Transformers** for LLM text generation

**Key Feature**: Cohere API key required for embeddings and re-ranking.

---

## Directory Structure

```
Project 1_C/
│
├── backend/                    # Core application package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration settings
│   ├── main.py                # FastAPI application entry point
│   │
│   ├── models/                # Pydantic data models
│   │   ├── __init__.py
│   │   └── schemas.py         # Request/response schemas
│   │
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── embeddings.py      # Text embedding service
│   │   ├── vector_store.py    # FAISS vector database
│   │   ├── reranker.py        # Search result re-ranking
│   │   ├── llm_service.py     # LLM text generation
│   │   └── local_storage.py   # Local storage helpers
│   │
│   ├── routers/               # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── generation.py      # Content generation endpoints
│   │   └── training_data.py   # CRUD endpoints
│   │
│   └── data/                  # Brand data and content
│       ├── __init__.py
│       ├── brand/             # Brand voice components
│       ├── templates/         # Content templates
│       └── samples/           # Sample marketing content
│
├── data/                      # Runtime data storage
│   ├── vector_store/          # FAISS index files
│   ├── past_campaigns/        # Past marketing campaigns (spec)
│   ├── user_queries/          # Stored user queries (spec)
│   └── style_guidelines/      # Brand style references (spec)
│
├── tests/                     # Test files
│   ├── __init__.py
│   └── test_api.py
│
├── docs/                      # Documentation
│   └── DOCUMENTATION.md       # This file
│
├── .env                       # Environment configuration
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── run.py                     # Application runner
└── README.md                  # Quick start guide
```

---

## Configuration Files

### `.env`

**Purpose**: Environment configuration for the application.

**Location**: Project root

**Key Settings**:

```env
# Application
APP_ENV=development          # Environment mode
DEBUG=true                   # Enable debug logging
API_HOST=0.0.0.0            # Server host
API_PORT=8000               # Server port

# Vector Store
VECTOR_STORE_PATH=./data/vector_store    # Where FAISS index is stored
EMBEDDING_DIMENSION=1024                 # Must match Cohere model

# Cohere
COHERE_API_KEY=your_key_here
COHERE_EMBED_MODEL=embed-english-v3.0
COHERE_RERANK_MODEL=rerank-english-v3.0

# LLM
# Either a remote model ID or a local fine-tuned folder
# HUGGINGFACE_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
HUGGINGFACE_MODEL=./backend/models/finetuned-merged

# Generation
MAX_GENERATION_TOKENS=512    # Max output length
GENERATION_TEMPERATURE=0.7   # Creativity (0-1)
RERANK_TOP_N=5              # Results after re-ranking
```

**How to Use**:
```bash
# Copy template
copy .env.example .env

# Edit values as needed
notepad .env
```

---

### `requirements.txt`

**Purpose**: Python package dependencies.

**Key Packages**:

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pydantic` | Data validation |
| `faiss-cpu` | Vector database |
| `cohere` | Embeddings & rerank |
| `transformers` | Hugging Face models |
| `torch` | Deep learning framework |

**How to Use**:
```bash
pip install -r requirements.txt
```

---

### `run.py`

**Purpose**: Convenience script to start the application.

**Functions**:

```python
def main():
    """
    Parse command-line arguments and start the uvicorn server.
    
    Arguments:
        --host: Server host (default: 0.0.0.0)
        --port: Server port (default: 8000)
        --reload: Enable auto-reload (default: True in debug)
        --workers: Number of workers (default: 1)
    """
```

**How to Use**:
```bash
# Basic start
python run.py

# Custom port
python run.py --port 8080

# Production mode
python run.py --reload=false --workers 4
```

---

## Application Core

### `backend/config.py`

**Purpose**: Centralized configuration management using Pydantic Settings.

**Classes**:

```python
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        app_name: str - Application display name
        app_env: str - Environment (development/production)
        debug: bool - Debug mode flag
        api_host: str - Server host address
        api_port: int - Server port number
        
        vector_store_path: str - Path for FAISS index
        embedding_dimension: int - Embedding vector size
        
        cohere_api_key: str - Cohere API key
        cohere_embed_model: str - Cohere embedding model name
        cohere_rerank_model: str - Cohere rerank model name
        huggingface_model: str - LLM model name
        
        max_generation_tokens: int - Max generation length
        generation_temperature: float - Creativity level
        rerank_top_n: int - Top N after re-ranking
    """
```

**Functions**:

```python
def get_settings() -> Settings:
    """
    Get cached application settings (singleton pattern).
    
    Returns:
        Settings: Validated settings instance
    
    Example:
        settings = get_settings()
        print(settings.api_port)  # 8000
    """
```

**How to Use**:
```python
from backend.config import settings

# Access any setting
print(settings.huggingface_model)
print(settings.api_port)
```

---

### `backend/main.py`

**Purpose**: FastAPI application entry point with all configurations.

**Components**:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    
    Startup:
        - Logs configuration
        - Initializes services
    
    Shutdown:
        - Cleanup resources
    """

app = FastAPI(...)  # Main application instance

@app.get("/")
async def root():
    """
    Root endpoint returning API information.
    
    Returns:
        dict: API name, version, stack info, endpoints
    """

@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns:
        dict: Service status for monitoring
    """
```

**How to Use**:
```python
# Run directly
python -m backend.main

# Or via run.py
python run.py
```

---

## Models (Schemas)

### `backend/models/schemas.py`

**Purpose**: Pydantic models for request/response validation.

---

#### Enums

```python
class ContentType(str, Enum):
    """
    Supported marketing content types.
    
    Values:
        EMAIL = "email"              # Email campaigns
        SOCIAL_MEDIA = "social_media"  # Social posts
        WEBSITE_COPY = "website_copy"  # Website pages
        FUNNEL_PAGE = "funnel_page"    # Sales funnels
        AD_COPY = "ad_copy"            # Advertisements
        BLOG_POST = "blog_post"        # Blog articles
        CAMPAIGN = "campaign"          # Full campaigns
    """
```

**How to Use**:
```python
from backend.models.schemas import ContentType

content_type = ContentType.EMAIL
print(content_type.value)  # "email"
```

---

#### Request Models

```python
class GenerationRequest(BaseModel):
    """
    Request model for generating marketing copy.
    
    Attributes:
        prompt: str - Description of content to generate (required)
        content_type: ContentType - Type of content (required)
        target_audience: str - Who the content is for (optional)
        key_points: List[str] - Points to include (optional)
        tone_override: str - Custom tone adjustment (optional)
        max_length: int - Approximate word count (optional, default 500)
    
    Example:
        {
            "prompt": "Write a welcome email for new subscribers",
            "content_type": "email",
            "target_audience": "Women aged 25-45",
            "key_points": ["Free ebook", "Weekly tips"],
            "max_length": 300
        }
    """

class TrainingDataCreate(BaseModel):
    """
    Request model for adding training data.
    
    Attributes:
        title: str - Content title (required)
        content: str - The marketing content (required)
        content_type: ContentType - Category (required)
        metadata: dict - Additional info (optional)
        tags: List[str] - Keywords (optional)
    """

class TrainingDataUpdate(BaseModel):
    """
    Request model for updating training data (partial update).
    All fields are optional - only provided fields are updated.
    """
```

---

#### Response Models

```python
class GenerationResponse(BaseModel):
    """
    Response model for generated content.
    
    Attributes:
        generated_content: str - The AI-generated copy
        content_type: ContentType - Type that was generated
        prompt_used: str - Original prompt
        similar_content_used: List[str] - Titles of retrieved examples
        generation_metadata: dict - Model info, tokens, etc.
    """

class TrainingDataResponse(BaseModel):
    """
    Response model for training data items.
    
    Attributes:
        id: UUID - Unique identifier
        title: str - Content title
        content: str - Marketing content
        content_type: ContentType - Category
        metadata: dict - Additional info
        tags: List[str] - Keywords
        created_at: datetime - Creation time
        updated_at: datetime - Last update time
    """

class TrainingDataListResponse(BaseModel):
    """
    Response model for paginated training data list.
    
    Attributes:
        items: List[TrainingDataResponse] - Content items
        total: int - Total count
        page: int - Current page
        page_size: int - Items per page
    """
```

---

#### Internal Models

```python
class MarketingContent(BaseModel):
    """
    Internal model for stored marketing content.
    
    Includes embedding vector for similarity search.
    
    Attributes:
        id: UUID - Unique identifier
        title: str - Content title
        content: str - Marketing text
        content_type: ContentType - Category
        metadata: dict - Additional info
        tags: List[str] - Keywords
        embedding: List[float] - Vector embedding (1024 dims)
        created_at: datetime - Creation time
        updated_at: datetime - Last update time
    """

class RetrievedContent(BaseModel):
    """
    Model for content retrieved from vector search.
    
    Attributes:
        content: MarketingContent - The content
        similarity_score: float - FAISS similarity (0-1)
        rerank_score: float - Cohere rerank score (0-1)
    """
```

---

## Services

### `backend/services/embeddings.py`

**Purpose**: Convert text to vector embeddings using Cohere.

```python
class EmbeddingService:
    """
    Service for generating text embeddings.
    
    Uses Cohere embeddings via API.
    
    Attributes:
        client: cohere.Client - The API client
        model_name: str - Model identifier
        dimension: int - Output vector dimension
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the embedding service.
        
        Args:
            model_name: Model to use (default: from settings)
        """
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            List[float]: 1024-dimensional vector
        
        Example:
            embedding = await service.embed_text("Hello world")
        """
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch).
        
        More efficient than calling embed_text multiple times.
        
        Args:
            texts: List of texts
        
        Returns:
            List of embedding vectors
        """
    
    async def embed_query(self, query: str) -> List[float]:
        """Embed a search query."""
    
    async def embed_document(self, document: str) -> List[float]:
        """Embed a document for indexing."""
    
    def cosine_similarity(self, emb1, emb2) -> float:
        """Calculate similarity between two embeddings."""

def get_embedding_service() -> EmbeddingService:
    """Get singleton embedding service instance."""
```

**How to Use**:
```python
from backend.services.embeddings import get_embedding_service

service = get_embedding_service()
embedding = await service.embed_text("Marketing copy example")
print(len(embedding))  # 1024
```

---

### `backend/services/vector_store.py`

**Purpose**: FAISS-based vector database for semantic search.

```python
class VectorStoreService:
    """
    FAISS vector store for marketing content retrieval.
    
    Stores content embeddings for semantic similarity search.
    Persists to disk automatically.
    
    Attributes:
        embedding_service: EmbeddingService - For generating embeddings
        index: faiss.IndexFlatIP - FAISS index
        metadata: Dict - Content metadata storage
        store_path: Path - Disk storage location
    """
    
    def __init__(self, embedding_service=None, store_path=None):
        """
        Initialize vector store.
        
        Loads existing index from disk or creates new one.
        """
    
    async def add_content(self, content: MarketingContent) -> MarketingContent:
        """
        Add marketing content to the store.
        
        1. Generates embedding for the content
        2. Adds to FAISS index
        3. Stores metadata
        4. Saves to disk
        
        Args:
            content: MarketingContent to add
        
        Returns:
            MarketingContent with ID and embedding
        
        Example:
            content = MarketingContent(
                title="Welcome Email",
                content="Dear friend...",
                content_type=ContentType.EMAIL
            )
            added = await store.add_content(content)
        """
    
    async def search(
        self,
        query: str,
        k: int = 10,
        content_type: Optional[ContentType] = None
    ) -> List[RetrievedContent]:
        """
        Search for similar content.
        
        Uses semantic similarity, not keyword matching.
        
        Args:
            query: Search query (natural language)
            k: Max results to return
            content_type: Optional filter
        
        Returns:
            List of RetrievedContent sorted by similarity
        
        Example:
            results = await store.search(
                "email for product launch",
                k=5,
                content_type=ContentType.EMAIL
            )
        """
    
    async def get_content(self, content_id: UUID) -> Optional[MarketingContent]:
        """Get content by ID."""
    
    async def update_content(self, content_id: UUID, updates: dict) -> Optional[MarketingContent]:
        """Update content (re-embeds if text changes)."""
    
    async def delete_content(self, content_id: UUID) -> bool:
        """Delete content and rebuild index."""
    
    async def list_content(
        self,
        content_type: Optional[ContentType] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[MarketingContent], int]:
        """List content with pagination."""
    
    def get_stats(self) -> dict:
        """Get store statistics."""
    
    def save(self) -> None:
        """Persist index to disk."""

def get_vector_store() -> VectorStoreService:
    """Get singleton vector store instance."""
```

**How to Use**:
```python
from backend.services.vector_store import get_vector_store
from backend.models.schemas import MarketingContent, ContentType

store = get_vector_store()

# Add content
content = MarketingContent(
    title="Test Email",
    content="Dear friend, welcome to our community...",
    content_type=ContentType.EMAIL
)
await store.add_content(content)

# Search
results = await store.search("welcome email", k=5)
for r in results:
    print(f"{r.content.title}: {r.similarity_score:.3f}")
```

---

### `backend/services/reranker.py`

**Purpose**: Re-rank search results for better relevance using Cohere.

```python
class RerankerService:
    """
    Re-ranking service using Cohere Rerank API.
    
    Attributes:
        client: cohere.Client - The API client
        model_name: str - Model identifier
        top_n: int - Default number of results
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize re-ranker (requires COHERE_API_KEY)."""
    
    async def rerank(
        self,
        query: str,
        results: List[RetrievedContent],
        top_n: Optional[int] = None
    ) -> List[RetrievedContent]:
        """
        Re-rank search results for improved relevance.
        
        Args:
            query: Original search query
            results: Initial search results
            top_n: Number of results to return
        
        Returns:
            Re-ranked results with rerank_score added
        
        Example:
            initial = await vector_store.search("email", k=20)
            reranked = await reranker.rerank("welcome email", initial, top_n=5)
        """
    
    async def rerank_with_scores(
        self,
        query: str,
        texts: List[str],
        top_n: Optional[int] = None
    ) -> List[dict]:
        """Re-rank arbitrary texts and return scores."""

def get_reranker_service() -> RerankerService:
    """Get singleton reranker instance."""
```

**How to Use**:
```python
from backend.services.reranker import get_reranker_service

reranker = get_reranker_service()

# After initial search
initial_results = await store.search("marketing email", k=20)

# Re-rank for better relevance
reranked = await reranker.rerank(
    query="welcome email for new customers",
    results=initial_results,
    top_n=5
)
```

---

### `backend/services/llm_service.py`

**Purpose**: Generate marketing copy using Hugging Face LLM.

```python
class LLMService:
    """
    LLM service for marketing copy generation.
    
    Uses Hugging Face Transformers with brand voice prompting.
    Model downloads on first use (~2GB for TinyLlama).
    
    Attributes:
        model_name: str - Hugging Face model ID
        max_tokens: int - Max generation length
        temperature: float - Creativity level
        device: str - "cuda" or "cpu"
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize LLM service (lazy loads model)."""
    
    async def generate(
        self,
        request: GenerationRequest,
        retrieved_content: Optional[List[RetrievedContent]] = None
    ) -> GenerationResponse:
        """
        Generate marketing copy.
        
        Process:
        1. Builds prompt with brand voice
        2. Adds content-type guidelines
        3. Includes retrieved examples (RAG)
        4. Generates with LLM
        5. Cleans output
        
        Args:
            request: Generation request
            retrieved_content: Examples for context (RAG)
        
        Returns:
            GenerationResponse with content and metadata
        
        Example:
            request = GenerationRequest(
                prompt="Write a welcome email",
                content_type=ContentType.EMAIL
            )
            response = await llm.generate(request, similar_content)
        """
    
    async def refine_content(
        self,
        original_content: str,
        feedback: str,
        content_type: ContentType
    ) -> str:
        """
        Refine existing content based on feedback.
        
        Args:
            original_content: Content to refine
            feedback: What to change
            content_type: Content category
        
        Returns:
            Refined content string
        """

def get_llm_service() -> LLMService:
    """Get singleton LLM service instance."""
```

**How to Use**:
```python
from backend.services.llm_service import get_llm_service
from backend.models.schemas import GenerationRequest, ContentType

llm = get_llm_service()

request = GenerationRequest(
    prompt="Write a promotional email for our spring sale",
    content_type=ContentType.EMAIL,
    target_audience="Women aged 25-45",
    key_points=["30% off", "Free shipping"],
    max_length=300
)

response = await llm.generate(request)
print(response.generated_content)
```

---

## API Routers

### `backend/routers/generation.py`

**Purpose**: API endpoints for content generation.

#### Endpoints

```
POST /api/v1/generate
```
**Generate Marketing Copy**

Request:
```json
{
    "prompt": "Write a welcome email for new subscribers",
    "content_type": "email",
    "target_audience": "Women interested in personal development",
    "key_points": ["Free ebook", "Weekly tips"],
    "max_length": 300
}
```

Query Parameters:
- `use_rag`: bool (default: true) - Use retrieved content for context
- `num_examples`: int (default: 3) - Number of examples to retrieve

Response:
```json
{
    "generated_content": "Subject: Welcome to the family...",
    "content_type": "email",
    "prompt_used": "Write a welcome email...",
    "similar_content_used": ["Welcome Email - New Subscriber"],
    "generation_metadata": {"model": "TinyLlama...", "temperature": 0.7}
}
```

---

```
POST /api/v1/generate/refine
```
**Refine Existing Content**

Request:
```json
{
    "original_content": "The generated email content...",
    "feedback": "Make it more urgent",
    "content_type": "email"
}
```

---

```
GET /api/v1/generate/content-types
```
**List Available Content Types**

Response:
```json
[
    {"value": "email", "name": "Email", "description": "Email campaigns..."},
    {"value": "social_media", "name": "Social Media", "description": "..."}
]
```

---

### `backend/routers/training_data.py`

**Purpose**: CRUD endpoints for managing training data.

#### Endpoints

```
POST /api/v1/training-data
```
**Add Training Data**

Request:
```json
{
    "title": "Summer Sale Email",
    "content": "Dear friend, Summer is here...",
    "content_type": "email",
    "tags": ["summer", "sale"]
}
```

---

```
GET /api/v1/training-data
```
**List Training Data**

Query Parameters:
- `content_type`: Filter by type (optional)
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)

---

```
GET /api/v1/training-data/{id}
```
**Get Specific Training Data**

---

```
PUT /api/v1/training-data/{id}
```
**Update Training Data**

---

```
DELETE /api/v1/training-data/{id}
```
**Delete Training Data**

---

```
POST /api/v1/training-data/seed
```
**Seed Sample Data**

Seeds the database with example marketing content.
Call this on first setup.

---

```
POST /api/v1/training-data/search
```
**Search Training Data**

Query Parameters:
- `query`: Search query (required)
- `k`: Number of results (default: 5)
- `content_type`: Filter by type (optional)

---

```
GET /api/v1/training-data/stats
```
**Get Statistics**

Returns counts by content type and total documents.

---

## Brand Data

### `backend/data/brand/voice.py`

**Purpose**: Core brand voice definition.

```python
@dataclass
class BrandVoiceConfig:
    """
    Brand voice configuration.
    
    Attributes:
        name: str - Brand name ("Adriana James")
        tagline: str - Brand tagline
        core_values: List[str] - Brand values
        personality_traits: List[str] - Voice characteristics
        communication_style: Dict - Style guidelines
        emotional_tone: List[str] - Emotional register
    """

BRAND_VOICE = BrandVoiceConfig(...)  # Pre-configured instance

def get_brand_voice_prompt() -> str:
    """
    Generate the complete brand voice prompt for LLM.
    
    Returns:
        str: Formatted system prompt with all brand guidelines
    """
```

---

### `backend/data/brand/tone_guidelines.py`

**Purpose**: Detailed writing guidelines by content type.

```python
@dataclass
class ToneGuideline:
    """
    Individual tone guideline.
    
    Attributes:
        name: str - Guideline name
        description: str - What it means
        do_examples: List[str] - Good examples
        dont_examples: List[str] - Bad examples
    """

@dataclass
class ContentTypeGuideline:
    """
    Guidelines for a content type.
    
    Attributes:
        content_type: str - Type name
        description: str - Purpose
        structure: List[str] - Content structure
        tone_notes: str - Tone guidance
        length_guide: str - Length recommendations
        key_elements: List[str] - Must-have elements
        example_opening: str - Example start
    """

TONE_GUIDELINES: Dict[str, ToneGuideline]  # General guidelines
CONTENT_TYPE_GUIDELINES: Dict[str, ContentTypeGuideline]  # By type

def get_guidelines_for_content_type(content_type: str) -> ContentTypeGuideline:
    """Get guidelines for a specific content type."""

def format_guidelines_for_prompt(content_type: str) -> str:
    """Format guidelines as LLM prompt section."""
```

---

### `backend/data/brand/vocabulary.py`

**Purpose**: Power words and phrases for the brand.

```python
POWER_WORDS: Dict[str, List[str]] = {
    "transformation": ["transform", "breakthrough", "unlock", ...],
    "empowerment": ["empower", "capable", "confident", ...],
    "action": ["start", "begin", "launch", ...],
    "connection": ["together", "community", "support", ...],
    ...
}

PHRASES_TO_USE: Dict[str, List[str]] = {
    "openings": ["Here's the truth...", "What if I told you...", ...],
    "empowerment": ["You deserve...", "You're capable of...", ...],
    "call_to_action": ["Take the first step...", ...],
    ...
}

PHRASES_TO_AVOID: Dict[str, List[str]] = {
    "pushy_sales": ["Buy now!", "Limited time only!", ...],
    "fear_based": ["You'll regret not...", ...],
    ...
}

EMOTIONAL_TRIGGERS: Dict[str, EmotionalTrigger]  # Emotions to evoke

def get_power_words_for_context(context: str) -> List[str]:
    """Get power words for a context (transformation, action, etc.)"""

def format_vocabulary_for_prompt() -> str:
    """Format vocabulary as LLM prompt section."""
```

---

### `backend/data/brand/personas.py`

**Purpose**: Target audience persona definitions.

```python
@dataclass
class Persona:
    """
    Target audience persona.
    
    Attributes:
        name: str - Persona name
        demographic: str - Age, background
        description: str - Who they are
        goals: List[str] - What they want
        pain_points: List[str] - Their struggles
        desires: List[str] - What they need to hear
        objections: List[str] - Common objections
        motivators: List[str] - What moves them
        content_preferences: List[str] - How they consume content
        tone_adjustments: str - How to adjust tone
    """

TARGET_PERSONAS: Dict[str, Persona] = {
    "aspiring_entrepreneur": Persona(...),
    "burnt_out_professional": Persona(...),
    "growth_seeker": Persona(...),
    "new_chapter": Persona(...),
}

def get_persona(name: str) -> Optional[Persona]:
    """Get persona by name."""

def get_persona_context(persona_name: str) -> str:
    """Format persona as LLM context."""
```

---

## Templates

### `backend/data/templates/email.py`

**Purpose**: Email content templates.

```python
@dataclass
class EmailTemplate:
    """
    Email template.
    
    Attributes:
        name: str - Template name
        purpose: str - When to use
        subject_line_formulas: List[str] - Subject patterns
        structure: List[str] - Email structure
        example: str - Full example
        tips: List[str] - Writing tips
    """

EMAIL_TEMPLATES: Dict[str, EmailTemplate] = {
    "welcome": EmailTemplate(...),
    "nurture": EmailTemplate(...),
    "launch": EmailTemplate(...),
    "cart_abandonment": EmailTemplate(...),
}
```

### Other Template Files

- `social_media.py` - LinkedIn, Instagram, Twitter, Facebook templates
- `ad_copy.py` - Lead gen, retargeting, webinar ad templates
- `website.py` - Homepage, about, services page templates
- `funnel.py` - Lead magnet, sales page, thank you templates
- `blog.py` - How-to, listicle, story, comparison templates

---

## Sample Content

### `backend/data/samples/marketing_samples.py`

**Purpose**: Sample marketing content for seeding the database.

```python
SAMPLE_MARKETING_CONTENT: List[dict] = [
    {
        "title": "Welcome Email - New Subscriber",
        "content": "Subject: Welcome to the family...",
        "content_type": ContentType.EMAIL,
        "tags": ["welcome", "onboarding"],
        "metadata": {"email_type": "welcome"}
    },
    # ... more samples for each content type
]
```

**How to Use**:
```bash
# Via API
POST http://localhost:8000/api/v1/training-data/seed

# Response
{"message": "Sample data seeded successfully", "added_count": 10}
```

---

## How-To Guides

### Starting the Application

```bash
# 1. Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Start the server
python -m backend.main

# 3. Open browser
http://localhost:8000/docs  # Swagger UI
```

### Generating Content

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-copy",
    json={
        "prompt": "Write a welcome email for new subscribers"
    }
)

print(response.json()["generated_content"])
```

### Adding Custom Training Data

```python
import requests

# Add new content
response = requests.post(
    "http://localhost:8000/api/v1/training-data",
    json={
        "title": "My Custom Email",
        "content": "Dear friend, this is my custom marketing email...",
        "content_type": "email",
        "tags": ["custom", "example"]
    }
)

print(response.json()["id"])  # UUID of created content
```

### Searching Training Data

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/training-data/search",
    params={
        "query": "welcome email new subscribers",
        "k": 5
    }
)

for item in response.json():
    print(f"{item['title']}: {item['similarity_score']}")
```

### Changing the LLM Model

1. Edit `.env`:
```env
HUGGINGFACE_MODEL=microsoft/phi-2
```

2. Restart the server:
```bash
python run.py
```

3. First generation will download the new model.

### Adding a New Content Type

1. Add to `backend/models/schemas.py`:
```python
class ContentType(str, Enum):
    # ... existing types
    PODCAST_SCRIPT = "podcast_script"  # Add new type
```

2. Add guidelines in `backend/data/brand/tone_guidelines.py`:
```python
CONTENT_TYPE_GUIDELINES["podcast_script"] = ContentTypeGuideline(...)
```

3. Add template in `backend/data/templates/` (create new file if needed)

4. Add sample in `backend/data/samples/marketing_samples.py`

---

## Error Handling

### Common Errors

**"Model not found"**
- First run downloads models automatically
- Check internet connection
- Check disk space (~3GB needed)

**"CUDA out of memory"**
- Use smaller model in `.env`
- Set `device = "cpu"` explicitly

**"Connection refused"**
- Server not running
- Check port availability
- Run `python run.py`

---

## Performance Tips

1. **First request is slow** - Models load on first use
2. **Use batch operations** - `embed_texts()` over multiple `embed_text()`
3. **Seed data once** - Don't re-seed repeatedly
4. **Adjust `max_tokens`** - Lower = faster generation
5. **Use GPU** - 10x faster if CUDA available

---

## Version History

- **1.0.0** - Initial release with full feature set
