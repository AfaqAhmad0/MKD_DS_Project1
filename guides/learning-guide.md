# Marketing Assistant AI - Student Learning Guide

This guide is a deep, end-to-end explanation of every major concept used in this
project. It is written so a motivated student can learn the ideas, understand
the design decisions, compare alternatives, and build a similar system on their
own.

If you are new to any topic, read in order. If you are experienced, jump to the
sections you need. All references to code paths use the actual files in this
repository.

---------------------------------------------------------------------------
Table of Contents
---------------------------------------------------------------------------

1. Project Overview
2. Architecture at a Glance
3. The End-to-End Request Flow
4. Core Concepts and Why They Were Chosen
   4.1 FastAPI and the Web Layer
   4.2 Data Validation with Pydantic
   4.3 Configuration and Environment Management
   4.4 Retrieval-Augmented Generation (RAG)
   4.5 Embeddings and Vector Search
   4.6 Re-ranking
   4.7 LLM Text Generation
   4.8 Prompt Engineering with Brand Voice
   4.9 Asynchronous I/O and Lazy Loading
   4.10 Singleton Services
   4.11 Local Storage for Audit and Learning
5. Data Model Design (Schemas)
6. Services Layer Design
7. API Design and Routing
8. Storage Design: FAISS Index + Metadata
9. Brand Data: Voice, Guidelines, Templates, Samples
10. Decisions and Alternatives (Trade-offs)
11. Testing and Quality
12. How to Extend the Project
13. Security, Privacy, and Reliability Notes
14. Deployment and Operations
15. Glossary

---------------------------------------------------------------------------
1. Project Overview
---------------------------------------------------------------------------

This project is a marketing copy generator aligned with a specific brand voice
(Adriana James). It combines:

- A REST API (FastAPI)
- Retrieval (FAISS vector search)
- External embedding and re-ranking (Cohere)
- Local LLM text generation (Hugging Face Transformers)
- Structured brand guidance (voice, tone, templates, vocabulary)

The system is designed to:

- Accept a structured prompt and content type
- Retrieve similar examples from a vector store
- Re-rank those examples for relevance
- Generate new marketing copy using a local LLM
- Return a response that includes the copy and metadata

Key documentation files:

- `README.md`
- `docs/DOCUMENTATION.md`
- `docs/API_DOCUMENTATION.md`

Primary code lives under `backend/`.

---------------------------------------------------------------------------
2. Architecture at a Glance
---------------------------------------------------------------------------

High-level layers:

1) API Layer
   - `backend/main.py`
   - `backend/routers/generation.py`
   - `backend/routers/training_data.py`

2) Domain Models
   - `backend/models/schemas.py`

3) Services (Business Logic)
   - `backend/services/embeddings.py`
   - `backend/services/vector_store.py`
   - `backend/services/reranker.py`
   - `backend/services/llm_service.py`
   - `backend/services/local_storage.py`

4) Brand Data and Templates
   - `backend/data/brand/*`
   - `backend/data/templates/*`
   - `backend/data/samples/marketing_samples.py`

5) Storage
   - `data/vector_store/` (FAISS index and metadata)
   - `data/user_queries/` and `data/past_campaigns/` (JSON logs)

The project follows a clean layering approach:

- API depends on services
- Services depend on models and config
- Models are pure schema definitions

This reduces coupling and makes the system easier to test and extend.

---------------------------------------------------------------------------
3. The End-to-End Request Flow
---------------------------------------------------------------------------

The main generation flow uses the endpoint in `backend/routers/generation.py`.
Here is the precise sequence:

1) Request arrives at `POST /api/v1/generate`.
2) FastAPI validates the body against `GenerationRequest`.
3) The router retrieves service singletons:
   - Vector store
   - Reranker
   - LLM service
4) If RAG is enabled:
   - Create query embedding using Cohere
   - Search FAISS for nearest neighbors
   - Re-rank results via Cohere
5) Build a full prompt:
   - Brand voice
   - Content-type guidelines
   - Vocabulary and do/dont rules
   - User prompt and optional audience details
   - Retrieved examples
6) Generate text with Hugging Face model locally.
7) Clean the output to remove prompt artifacts.
8) Save user query and response to `data/user_queries/`.
9) Return `GenerationResponse`.

This flow is classic Retrieval-Augmented Generation:

User prompt -> Retrieve similar content -> Re-rank -> Generate with context

Why this design matters:

- The LLM sees grounded examples, improving relevance and consistency.
- The vector store allows the system to learn from past content without full
  fine-tuning.
- The API keeps responsibilities separate and testable.

---------------------------------------------------------------------------
4. Core Concepts and Why They Were Chosen
---------------------------------------------------------------------------

4.1 FastAPI and the Web Layer
--------------------------------

Files: `backend/main.py`, `backend/routers/*`

What FastAPI provides:

- ASGI-based async web server
- Automatic validation through Pydantic models
- Automatic OpenAPI documentation at `/docs`
- Dependency injection (not used heavily here but available)

Why FastAPI was chosen:

- Fast to develop and easy to reason about
- Strong typing and validation
- Great developer experience and documentation

Alternatives:

- Flask: simpler but lacks built-in async and validation
- Django: heavier framework with ORM and templating
- Express (Node): good ecosystem, but different language

Why FastAPI here:

- We want fast iteration, robust schemas, and clear request/response types.

4.2 Data Validation with Pydantic
-----------------------------------

File: `backend/models/schemas.py`

Pydantic enforces:

- Required fields and types
- Min/max lengths and ranges
- Clear, structured models for API input/output

Why it matters:

- Prevents invalid input from causing failures downstream
- Creates self-documenting API contracts

Alternatives:

- Manual validation (error prone)
- Marshmallow or Cerberus (less integrated with FastAPI)

Why Pydantic here:

- Native to FastAPI and very ergonomic for typed schemas.

4.3 Configuration and Environment Management
----------------------------------------------

File: `backend/config.py`

Key decisions:

- Use `pydantic-settings` to load `.env` and env vars
- Validate configs (port range, temperature, embedding dimension)
- Cache settings for reuse

Why:

- Keeps secrets out of source control
- Provides safe defaults
- Validates at startup to fail early

Alternatives:

- Plain `os.environ` lookups (no validation)
- Dynaconf or dotenv only (less structure)

Why this approach:

- We need reliable configuration with validation and clear defaults.

4.4 Retrieval-Augmented Generation (RAG)
-----------------------------------------

Files:

- `backend/routers/generation.py`
- `backend/services/vector_store.py`
- `backend/services/reranker.py`

RAG is the idea of retrieving relevant examples and feeding them into the LLM.

Why:

- Improves factual consistency and brand voice alignment
- Reduces hallucinations by grounding output in known samples
- Allows updating knowledge without retraining the LLM

Alternatives:

- Fine-tuning (expensive, less flexible)
- Prompt-only generation (less grounded, less consistent)

Why RAG here:

- The project needs to reflect a specific brand voice and past examples.

4.5 Embeddings and Vector Search
----------------------------------

Files:

- `backend/services/embeddings.py`
- `backend/services/vector_store.py`

Embeddings convert text into dense vectors. FAISS performs similarity search.

Why:

- Allows semantic search (meaning-based), not just keyword matching.
- Enables retrieving content that "feels" similar, even if worded differently.

Alternatives:

- Keyword search (BM25) only
- Vector databases like Pinecone, Weaviate, Milvus

Why Cohere embeddings:

- High quality and easy to use
- Consistent dimensionality (1024 for embed-english-v3.0)
- Good English performance without hosting your own embedding model

Why FAISS:

- Local, fast, and easy to persist
- No extra infrastructure required for a project of this size

Trade-offs:

- FAISS lacks features like metadata filtering at scale and distributed search.
- Managed vector DBs give better scaling but cost more and require deployment.

4.6 Re-ranking
----------------

File: `backend/services/reranker.py`

Why re-rank:

- Vector search returns "similar" results, not always the most relevant.
- Re-ranking uses a cross-encoder model to score relevance more precisely.

Alternatives:

- Skip re-ranking for speed
- Use an open-source re-ranker (e.g., cross-encoder from SentenceTransformers)

Why Cohere re-rank:

- Strong performance with simple API
- Good quality without hosting your own model

Trade-offs:

- Adds external API cost and latency
- Requires API key

4.7 LLM Text Generation
-------------------------

File: `backend/services/llm_service.py`

Uses Hugging Face Transformers to run the LLM locally.

Why local LLM:

- No per-request API cost for generation
- Keeps brand data on local machine
- Works offline after model download

Alternatives:

- OpenAI, Anthropic, Cohere generation APIs
- Self-hosted inference servers (vLLM, TGI)

Why this approach:

- Good for a local or small team environment
- Easy to switch models via `.env`

Trade-offs:

- Requires local RAM and GPU (or slower CPU)
- Model downloads can be large

4.8 Prompt Engineering with Brand Voice
-----------------------------------------

Files:

- `backend/data/brand/voice.py`
- `backend/data/brand/tone_guidelines.py`
- `backend/data/brand/vocabulary.py`
- `backend/services/llm_service.py`

The prompt includes:

- Brand identity and values
- Tone guidelines by content type
- Vocabulary rules and examples
- Optional retrieved content examples

Why:

- Models are general-purpose and need clear guidance
- Brand voice consistency is critical in marketing

Alternatives:

- Use few-shot examples only
- Use fine-tuned LLM

Why this approach:

- Flexible, editable in plain Python data files
- Easier to maintain than model fine-tuning

4.9 Asynchronous I/O and Lazy Loading
--------------------------------------

FastAPI is async-friendly. Services use async methods, even though some calls
are actually synchronous. The model is lazily loaded:

- `_load_model()` only runs on first request
- Cohere API calls happen only when needed

Why:

- Faster startup
- Avoids memory cost if generation is not used immediately

Alternatives:

- Eager model load at startup (simpler but slow)
- Background task to warm up the model

4.10 Singleton Services
-------------------------

Each service provides `get_*()` singleton getters:

- `get_embedding_service()`
- `get_vector_store()`
- `get_reranker_service()`
- `get_llm_service()`

Why:

- Ensures consistent configuration
- Reuses heavy objects like LLMs and FAISS index
- Avoids repeatedly creating API clients

Trade-offs:

- Global state can make testing harder
- In a multi-worker setup, each process has its own singleton

4.11 Local Storage for Audit and Learning
-------------------------------------------

File: `backend/services/local_storage.py`

The system writes JSON files for:

- User queries + outputs (`data/user_queries/`)
- Campaign content (`data/past_campaigns/`)

Why:

- Simple audit log
- Useful for analysis and learning
- Lightweight, no database required

Alternatives:

- Relational DB (Postgres, SQLite)
- Document DB (MongoDB)
- Cloud storage

Why local JSON:

- Low setup overhead and easy for a student project

---------------------------------------------------------------------------
5. Data Model Design (Schemas)
---------------------------------------------------------------------------

File: `backend/models/schemas.py`

Key models:

- `ContentType` enum defines supported output types.
- `GenerationRequest` and `SimpleGenerationRequest` define input.
- `GenerationResponse` defines output.
- `TrainingDataCreate/Update/Response` define CRUD for training data.
- `MarketingContent` is internal storage representation.
- `RetrievedContent` stores search results and scores.

Why enums:

- Prevent invalid content types.
- Central source of truth used across API and services.

Why separate request and response models:

- Control exactly what data is accepted and returned.
- Avoid leaking internal fields like embeddings.

Alternative approach:

- A single schema for everything (simpler but less safe).

---------------------------------------------------------------------------
6. Services Layer Design
---------------------------------------------------------------------------

The services are explicit modules with clear responsibilities:

1) EmbeddingService:
   - Calls Cohere embed API
   - Provides query and document embeddings
   - Validates embedding dimension

2) VectorStoreService:
   - Stores embeddings in FAISS
   - Stores metadata in pickle
   - Handles CRUD and search
   - Normalizes vectors for cosine similarity

3) RerankerService:
   - Calls Cohere rerank API
   - Returns improved relevance order

4) LLMService:
   - Loads HF model and tokenizer
   - Builds prompts with brand voice and examples
   - Generates, cleans output, returns metadata

5) LocalStorage:
   - Writes JSON logs for queries and campaigns

This design is clean because:

- Each module has a single responsibility
- You can swap a service without changing routers

---------------------------------------------------------------------------
7. API Design and Routing
---------------------------------------------------------------------------

File: `backend/routers/generation.py`

Endpoints:

- `POST /api/v1/generate`
- `POST /generate-copy` (spec-compatible)
- `POST /api/v1/generate/refine`
- `GET /api/v1/generate/content-types`

Why a public spec endpoint:

- The task spec expects `/generate-copy`.
- This allows simple usage while preserving a richer endpoint.

File: `backend/routers/training_data.py`

Endpoints:

- CRUD for training data
- `/seed` to load sample data
- `/search` to query with semantic search
- `/stats` for diagnostics

Why CRUD:

- Training data is core to RAG quality.
- Users need to add their own brand examples.

Validation:

- Ensures no empty prompt, no too-short content, etc.

Error handling:

- Global handler in `backend/main.py`
- Explicit HTTP errors in routers

---------------------------------------------------------------------------
8. Storage Design: FAISS Index + Metadata
---------------------------------------------------------------------------

File: `backend/services/vector_store.py`

Storage is split:

- FAISS index for fast vector search
- Metadata dictionary (pickled) for content details

How it works:

- Add content: embed text -> normalize -> add to index -> store metadata
- Search: embed query -> normalize -> FAISS search -> map IDs -> filter

Why normalize:

- FAISS uses dot product; normalized vectors approximate cosine similarity.

Why pickle:

- Quick, simple, Python-native
- Works for a student project

Alternatives:

- SQLite + separate index (more durable)
- Full vector DB with metadata filtering (scales better)

Trade-offs:

- Pickle is not cross-language friendly.
- Concurrent writes can be tricky in multi-process setups.

---------------------------------------------------------------------------
9. Brand Data: Voice, Guidelines, Templates, Samples
---------------------------------------------------------------------------

Brand voice drives style and consistency.

Key files:

- `backend/data/brand/voice.py`
  - Defines brand values, traits, tone, communication style
  - Builds a complete system prompt

- `backend/data/brand/tone_guidelines.py`
  - Defines general tone rules
  - Defines per-content-type structures and examples

- `backend/data/brand/vocabulary.py`
  - Defines power words, phrases to use, phrases to avoid
  - Defines emotional triggers

- `backend/data/brand/personas.py`
  - Defines target audience personas
  - Provides structured persona contexts

- `backend/data/templates/*`
  - Contains template structures and examples

- `backend/data/samples/marketing_samples.py`
  - Sample data used for seeding

Why separate these into data modules:

- Brand voice can be updated without changing code logic.
- It is testable and editable by non-engineers.

Alternative:

- Keep brand voice hardcoded in prompts directly (less maintainable).

---------------------------------------------------------------------------
10. Decisions and Alternatives (Trade-offs)
---------------------------------------------------------------------------

This section explains key choices and viable alternatives.

1) Cohere for embeddings and re-ranking
   - Why: strong quality, easy API, consistent dimensions
   - Alternatives: OpenAI embeddings, SentenceTransformers, BGE models
   - Trade-off: external API cost, dependency on network

2) FAISS for vector storage
   - Why: local, fast, no infrastructure
   - Alternatives: Pinecone, Weaviate, Milvus, Chroma
   - Trade-off: less scalable and fewer metadata query features

3) Hugging Face local LLM
   - Why: no per-request cost, privacy, flexible
   - Alternatives: OpenAI API, Anthropic, Cohere, local vLLM server
   - Trade-off: needs local RAM and compute; slower without GPU

4) Prompt-based brand voice instead of fine-tuning
   - Why: easier to iterate, less cost, more flexible
   - Alternatives: fine-tuning or LoRA
   - Trade-off: prompt engineering needs careful design

5) JSON file logging instead of database
   - Why: easy and minimal setup
   - Alternatives: SQLite, Postgres, MongoDB
   - Trade-off: limited query and reporting capabilities

6) Singleton services
   - Why: reuse heavy resources, reduce setup costs
   - Alternatives: dependency injection per request
   - Trade-off: more global state, harder to test in isolation

7) No authentication in the API
   - Why: simplified development
   - Alternative: OAuth2, API keys, JWT
   - Trade-off: not suitable for public deployment

8) CORS open to all origins
   - Why: simplify frontend testing
   - Alternative: restrict origins
   - Trade-off: potential security risks

---------------------------------------------------------------------------
11. Testing and Quality
---------------------------------------------------------------------------

Tests live in `tests/`.

- `tests/test_api.py` checks core endpoints.
- Use `pytest` to run tests.

What you should test:

- Generation endpoint for valid and invalid inputs
- Training data CRUD operations
- Search returns expected structure
- Stats endpoint returns counts

Future improvements:

- Mock Cohere calls (avoid API dependency in tests)
- Snapshot tests for generated output
- Load tests for performance

---------------------------------------------------------------------------
12. How to Extend the Project
---------------------------------------------------------------------------

Add a new content type:

1) Add to `ContentType` in `backend/models/schemas.py`
2) Add guidelines in `backend/data/brand/tone_guidelines.py`
3) Add templates (optional) in `backend/data/templates/`
4) Add sample data in `backend/data/samples/marketing_samples.py`

Swap embedding provider:

- Replace `EmbeddingService` with a different client
- Update `embedding_dimension` in `.env`

Use a different vector store:

- Replace `VectorStoreService` with Pinecone or Weaviate wrapper
- Update search and add methods accordingly

Add authentication:

- Use FastAPI dependencies for auth middleware
- Add API key checks or JWT validation

Add a frontend:

- Build a UI that calls `/api/v1/generate`
- Use `/api/v1/generate/content-types` for UI dropdowns

---------------------------------------------------------------------------
13. Security, Privacy, and Reliability Notes
---------------------------------------------------------------------------

Current state:

- No auth: anyone can call endpoints
- CORS wide open
- API keys live in `.env`
- No rate limiting

Improvements:

- Add API key or OAuth-based auth
- Restrict CORS
- Add request rate limiting
- Use structured logging and monitoring

Privacy considerations:

- User prompts are stored locally in JSON
- If privacy is needed, disable storage or encrypt logs

---------------------------------------------------------------------------
14. Deployment and Operations
---------------------------------------------------------------------------

For local development:

- `python run.py`

Production considerations:

- Use `uvicorn` or `gunicorn` with multiple workers
- Disable reload and debug
- Use a process manager (systemd, Docker)
- Set API keys via environment variables

Scaling:

- With more traffic, move FAISS to a hosted vector DB
- Use a dedicated inference server for the LLM
- Cache embeddings and generated outputs

---------------------------------------------------------------------------
15. Glossary
---------------------------------------------------------------------------

API: Application Programming Interface, how systems communicate.
ASGI: Async Server Gateway Interface, async web server standard.
Embedding: Numeric vector representation of text meaning.
FAISS: Facebook AI Similarity Search, library for vector search.
LLM: Large Language Model, generates text.
RAG: Retrieval-Augmented Generation, combines retrieval and generation.
Re-ranking: Sorting retrieved items for relevance with a stronger model.
Prompt: The input text given to the LLM.
Schema: Data structure definition for validation and documentation.
Vector DB: Database optimized for storing and searching embeddings.

---------------------------------------------------------------------------
End of Guide
---------------------------------------------------------------------------
