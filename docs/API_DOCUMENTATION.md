# Marketing Assistant AI - API Documentation

**Base URL**: `http://localhost:8000`

**API Version**: v1

**Content-Type**: `application/json`

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Root Endpoints](#root-endpoints)
4. [Generation Endpoints](#generation-endpoints)
5. [Training Data Endpoints](#training-data-endpoints)
6. [Error Handling](#error-handling)
7. [Examples](#examples)

---

## Overview

The Marketing Assistant AI API provides endpoints for:

- **Content Generation**: Generate marketing copy using AI
- **Training Data Management**: CRUD operations for marketing examples
- **Semantic Search**: Find similar content by meaning

### Quick Links

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/generate-copy` | POST | Generate content (spec endpoint) |
| `/api/v1/generate` | POST | Generate content |
| `/api/v1/generate/refine` | POST | Refine content |
| `/api/v1/generate/content-types` | GET | List content types |
| `/api/v1/training-data` | GET | List training data |
| `/api/v1/training-data` | POST | Add training data |
| `/api/v1/training-data/{id}` | GET | Get by ID |
| `/api/v1/training-data/{id}` | PUT | Update by ID |
| `/api/v1/training-data/{id}` | DELETE | Delete by ID |
| `/api/v1/training-data/seed` | POST | Seed sample data |
| `/api/v1/training-data/search` | POST | Search content |
| `/api/v1/training-data/stats` | GET | Get statistics |

---

## Authentication

**No authentication required**, but **Cohere API key is required** for embeddings and re-ranking.

For production deployment, implement authentication middleware.

---

## Root Endpoints

### Get API Information

```
GET /
```

Returns basic information about the API.

**Response** `200 OK`
```json
{
    "name": "Marketing Assistant AI",
    "version": "1.0.0",
    "description": "AI-powered marketing copy generation",
    "stack": {
        "embeddings": "Cohere (embed-english-v3.0)",
        "vector_db": "FAISS",
        "reranking": "Cohere (rerank-english-v3.0)",
        "llm": "Hugging Face (TinyLlama/TinyLlama-1.1B-Chat-v1.0)"
    },
    "docs": "/docs",
    "cohere_required": true
}
```

---

### Health Check

```
GET /health
```

Check if all services are operational.

**Response** `200 OK`
```json
{
    "status": "healthy",
    "services": {
        "api": "running",
        "embeddings": "cohere",
        "vector_store": "local",
        "reranker": "cohere",
        "llm": "local (huggingface)"
    },
    "note": "Cohere API key required for embeddings and reranking."
}
```

---

## Generation Endpoints

### Generate Marketing Copy (Spec Endpoint)

```
POST /generate-copy
```

Generate marketing content using the spec-compatible endpoint.

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Description of content to generate |
| `content_type` | string | No | Optional (defaults to `campaign`) |

**Example Request**
```json
{
    "prompt": "Write a social media post for our new product launch"
}
```

---

### Generate Marketing Copy

```
POST /api/v1/generate
```

Generate marketing content aligned with the brand voice.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_rag` | boolean | `true` | Use retrieved content for context |
| `num_examples` | integer | `3` | Number of examples to retrieve (1-10) |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Description of content to generate (10-2000 chars) |
| `content_type` | string | Yes | Type of content (see Content Types) |
| `target_audience` | string | No | Who the content is for |
| `key_points` | array[string] | No | Points to include (max 10) |
| `tone_override` | string | No | Custom tone adjustment |
| `max_length` | integer | No | Approximate word count (50-5000, default: 500) |

**Content Types**

| Value | Description |
|-------|-------------|
| `email` | Email campaigns, newsletters |
| `social_media` | Social media posts |
| `website_copy` | Website pages |
| `funnel_page` | Sales funnels, landing pages |
| `ad_copy` | Advertisements |
| `blog_post` | Blog articles |
| `campaign` | Full marketing campaigns |

**Example Request**
```json
{
    "prompt": "Write a welcome email for new subscribers to our wellness newsletter",
    "content_type": "email",
    "target_audience": "Women aged 25-45 interested in personal development",
    "key_points": ["Free ebook offer", "Weekly tips", "Community access"],
    "max_length": 300
}
```

**Response** `200 OK`
```json
{
    "generated_content": "Subject: Welcome to the family 💜\n\nDear friend,\n\nI'm so glad you're here...",
    "content_type": "email",
    "prompt_used": "Write a welcome email for new subscribers...",
    "similar_content_used": [
        "Welcome Email - New Subscriber",
        "Nurture Email - Morning Routine Tip"
    ],
    "generation_metadata": {
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "device": "cpu",
        "temperature": 0.7
    }
}
```

**Error Responses**

| Status | Description |
|--------|-------------|
| `422` | Validation error (invalid request body) |
| `500` | Generation failed |

---

### Refine Content

```
POST /api/v1/generate/refine
```

Refine existing content based on feedback.

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `original_content` | string | Yes | Content to refine |
| `feedback` | string | Yes | What to change |
| `content_type` | string | Yes | Content type |

**Example Request**
```
POST /api/v1/generate/refine?content_type=email
```

Body (form data or JSON):
```json
{
    "original_content": "Subject: Welcome!\n\nHi there...",
    "feedback": "Make it more personal and add urgency",
    "content_type": "email"
}
```

**Response** `200 OK`
```json
{
    "refined_content": "Subject: Welcome to your transformation journey 💜\n\nDear friend...",
    "content_type": "email",
    "feedback_applied": "Make it more personal and add urgency"
}
```

---

### List Content Types

```
GET /api/v1/generate/content-types
```

Get all available content types with descriptions.

**Response** `200 OK`
```json
[
    {
        "value": "email",
        "name": "Email",
        "description": "Email campaigns, newsletters, promotional emails"
    },
    {
        "value": "social_media",
        "name": "Social Media",
        "description": "Posts for Instagram, LinkedIn, Twitter, Facebook"
    },
    {
        "value": "website_copy",
        "name": "Website Copy",
        "description": "Landing pages, about pages, product descriptions"
    },
    {
        "value": "funnel_page",
        "name": "Funnel Page",
        "description": "Sales funnels, opt-in pages, checkout pages"
    },
    {
        "value": "ad_copy",
        "name": "Ad Copy",
        "description": "Paid advertisements (Facebook, Google, etc.)"
    },
    {
        "value": "blog_post",
        "name": "Blog Post",
        "description": "Long-form blog content and articles"
    },
    {
        "value": "campaign",
        "name": "Campaign",
        "description": "Full marketing campaigns with multiple touchpoints"
    }
]
```

---

## Training Data Endpoints

### List Training Data

```
GET /api/v1/training-data
```

Get paginated list of training data.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content_type` | string | - | Filter by content type |
| `page` | integer | `1` | Page number |
| `page_size` | integer | `10` | Items per page (1-100) |

**Example Request**
```
GET /api/v1/training-data?content_type=email&page=1&page_size=5
```

**Response** `200 OK`
```json
{
    "items": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Welcome Email - New Subscriber",
            "content": "Subject: Welcome to the family...",
            "content_type": "email",
            "metadata": {"email_type": "welcome"},
            "tags": ["welcome", "onboarding"],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 10,
    "page": 1,
    "page_size": 5
}
```

---

### Create Training Data

```
POST /api/v1/training-data
```

Add new marketing content to the training data.

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Content title (3-200 chars) |
| `content` | string | Yes | Marketing content (min 50 chars) |
| `content_type` | string | Yes | Content type |
| `metadata` | object | No | Additional information |
| `tags` | array[string] | No | Keywords for categorization |

**Example Request**
```json
{
    "title": "Summer Sale Email",
    "content": "Subject: Summer is here! ☀️\n\nDear friend,\n\nSummer is finally here, and so are incredible savings...",
    "content_type": "email",
    "metadata": {
        "campaign": "Summer 2024",
        "version": 1
    },
    "tags": ["summer", "sale", "promotion"]
}
```

**Response** `201 Created`
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Summer Sale Email",
    "content": "Subject: Summer is here! ☀️\n\nDear friend...",
    "content_type": "email",
    "metadata": {"campaign": "Summer 2024", "version": 1},
    "tags": ["summer", "sale", "promotion"],
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}
```

---

### Get Training Data by ID

```
GET /api/v1/training-data/{id}
```

Get a specific training data item.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Training data ID |

**Response** `200 OK`
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Welcome Email - New Subscriber",
    "content": "Subject: Welcome to the family...",
    "content_type": "email",
    "metadata": {"email_type": "welcome"},
    "tags": ["welcome", "onboarding"],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**Response** `404 Not Found`
```json
{
    "detail": "Training data not found: 550e8400-e29b-41d4-a716-446655440999"
}
```

---

### Update Training Data

```
PUT /api/v1/training-data/{id}
```

Update an existing training data item (partial update).

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Training data ID |

**Request Body** (all fields optional)

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | New title |
| `content` | string | New content (triggers re-embedding) |
| `content_type` | string | New content type |
| `metadata` | object | New metadata (replaces existing) |
| `tags` | array[string] | New tags (replaces existing) |

**Example Request**
```json
{
    "title": "Updated Welcome Email",
    "tags": ["welcome", "onboarding", "updated"]
}
```

**Response** `200 OK`
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Updated Welcome Email",
    "content": "Subject: Welcome to the family...",
    "content_type": "email",
    "metadata": {"email_type": "welcome"},
    "tags": ["welcome", "onboarding", "updated"],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### Delete Training Data

```
DELETE /api/v1/training-data/{id}
```

Delete a training data item.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Training data ID |

**Response** `204 No Content`

(No response body)

**Response** `404 Not Found`
```json
{
    "detail": "Training data not found: 550e8400-e29b-41d4-a716-446655440999"
}
```

---

### Seed Sample Data

```
POST /api/v1/training-data/seed
```

Seed the database with sample marketing content.

**Note**: Intended to be called once during setup. Each call adds another copy
of the same sample items (useful for demos, but can duplicate data).

**Response** `200 OK`
```json
{
    "message": "Sample data seeded successfully",
    "added_count": 10,
    "total_samples": 10,
    "errors": null
}
```

---

### Search Training Data

```
POST /api/v1/training-data/search
```

Semantic search across training data.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | - | Search query (required) |
| `k` | integer | `5` | Number of results (1-50) |
| `content_type` | string | - | Filter by type |

**Example Request**
```
POST /api/v1/training-data/search?query=welcome%20email%20new%20customers&k=5
```

**Response** `200 OK`
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Welcome Email - New Subscriber",
        "content_type": "email",
        "similarity_score": 0.8542,
        "content_preview": "Subject: Welcome to the family 💜\n\nDear friend,\n\nI'm so glad you're here...",
        "tags": ["welcome", "onboarding"]
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "title": "Nurture Email - Morning Routine",
        "content_type": "email",
        "similarity_score": 0.6234,
        "content_preview": "Subject: The question I ask myself every morning...",
        "tags": ["nurture", "value"]
    }
]
```

---

### Get Statistics

```
GET /api/v1/training-data/stats
```

Get statistics about training data.

**Response** `200 OK`
```json
{
    "total_documents": 10,
    "index_size": 10,
    "dimension": 1024,
    "content_type_counts": {
        "email": 3,
        "social_media": 2,
        "website_copy": 2,
        "funnel_page": 1,
        "ad_copy": 1,
        "blog_post": 1
    },
    "store_path": "./data/vector_store"
}
```

---

## Error Handling

### Error Response Format

All errors return JSON with this structure:

```json
{
    "detail": "Error message describing what went wrong"
}
```

Or for validation errors:

```json
{
    "detail": [
        {
            "loc": ["body", "prompt"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request (invalid parameters) |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

---

## Examples

### cURL Examples

**Generate Content (Spec Endpoint)**
```bash
curl -X POST "http://localhost:8000/generate-copy" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a welcome email for new subscribers"
  }'
```

**Seed Sample Data**
```bash
curl -X POST "http://localhost:8000/api/v1/training-data/seed"
```

**Search Training Data**
```bash
curl -X POST "http://localhost:8000/api/v1/training-data/search?query=welcome%20email&k=5"
```

**Add Training Data**
```bash
curl -X POST "http://localhost:8000/api/v1/training-data" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Custom Email",
    "content": "Subject: Hello!\n\nDear friend, this is my custom marketing email that demonstrates the brand voice...",
    "content_type": "email",
    "tags": ["custom"]
  }'
```

### Python Examples

```python
import requests

BASE_URL = "http://localhost:8000"

# Generate content (spec endpoint)
response = requests.post(
    f"{BASE_URL}/generate-copy",
    json={
        "prompt": "Write a promotional email for our spring sale"
    }
)
print(response.json()["generated_content"])

# Search training data
response = requests.post(
    f"{BASE_URL}/api/v1/training-data/search",
    params={"query": "welcome email", "k": 5}
)
for item in response.json():
    print(f"{item['title']}: {item['similarity_score']:.2f}")

# Add custom training data
response = requests.post(
    f"{BASE_URL}/api/v1/training-data",
    json={
        "title": "Custom Email Template",
        "content": "Subject: Big news!\n\nDear friend...",
        "content_type": "email",
        "tags": ["custom", "template"]
    }
)
print(f"Created: {response.json()['id']}")
```

### JavaScript Examples

```javascript
const BASE_URL = "http://localhost:8000";

// Generate content (spec endpoint)
async function generateContent() {
    const response = await fetch(`${BASE_URL}/generate-copy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            prompt: "Write a welcome email for new subscribers"
        })
    });
    const data = await response.json();
    console.log(data.generated_content);
}

// Search training data
async function searchContent(query) {
    const response = await fetch(
        `${BASE_URL}/api/v1/training-data/search?query=${encodeURIComponent(query)}&k=5`,
        { method: "POST" }
    );
    const results = await response.json();
    results.forEach(item => {
        console.log(`${item.title}: ${item.similarity_score.toFixed(2)}`);
    });
}
```

---

## Interactive Documentation

Swagger UI is available at:
```
http://localhost:8000/docs
```

ReDoc is available at:
```
http://localhost:8000/redoc
```

These provide interactive API exploration with request/response examples.
