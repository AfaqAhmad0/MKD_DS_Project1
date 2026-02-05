# Marketing Assistant AI

AI-powered marketing copy generation aligned with Adriana James' brand voice. **Cohere API key required** for embeddings and re-ranking.

## Features

- Generate marketing copy in Adriana James' brand voice
- Supports: emails, social media, ads, blogs, campaigns, and more
- RAG-powered (uses past content for better generation)
- CRUD for managing training data
- Semantic search

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Embeddings | Cohere |
| Vector DB | FAISS |
| Re-ranking | Cohere |
| LLM | Hugging Face Transformers |

---

## Quick Start

### 1. Install Dependencies

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install packages (root)
pip install -r requirements.txt
```

### 2. Configure API Key

Add your Cohere API key to `.env`:
```
COHERE_API_KEY=your_cohere_api_key_here
```

### 3. Run

```powershell
# Recommended (project root)
python run.py

# Or explicit module
python -m backend.main
```

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### 4. First Time Setup

**Seed sample data:**
```bash
curl -X POST http://localhost:8000/api/v1/training-data/seed
```

**Generate content (spec endpoint):**
```bash
curl -X POST http://localhost:8000/generate-copy \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a welcome email"}'
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md) | Complete technical documentation |
| [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) | API reference with examples |

---

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI backend (spec entrypoint)
│   ├── copywriter.py        # Copy generation module (wrapper)
│   ├── vector_store.py      # Vector store wrapper
│   ├── embeddings.py        # Cohere embeddings wrapper
│   ├── brand_style.py       # Brand tone helpers
│   ├── config.py            # Configuration wrapper
│   └── requirements.txt     # Backend dependencies
├── docs/                    # Documentation
├── requirements.txt
├── .env
└── run.py
```

---

## Content Types

| Type | Description |
|------|-------------|
| `email` | Email campaigns, newsletters |
| `social_media` | Social posts (LinkedIn, Instagram, etc.) |
| `website_copy` | Landing pages, about pages |
| `funnel_page` | Sales funnels, opt-in pages |
| `ad_copy` | Facebook, Google ads |
| `blog_post` | Blog articles |
| `campaign` | Full marketing campaigns |

---

## LLM Model Options

Edit `HUGGINGFACE_MODEL` in `.env`:

| Model | RAM | Quality |
|-------|-----|---------|
| `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | ~4GB | Good |
| `microsoft/phi-2` | ~6GB | Better |
| `mistralai/Mistral-7B-Instruct-v0.2` | ~16GB | Best |

---

## API Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate-copy` | POST | Generate content (spec endpoint) |
| `/api/v1/generate` | POST | Generate content |
| `/api/v1/training-data` | GET/POST | List/Add training data |
| `/api/v1/training-data/{id}` | GET/PUT/DELETE | CRUD by ID |
| `/api/v1/training-data/seed` | POST | Seed sample data |
| `/api/v1/training-data/search` | POST | Semantic search |

See [API Documentation](docs/API_DOCUMENTATION.md) for full details.

---

## License

MIT License
