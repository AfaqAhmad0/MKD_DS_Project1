# Test Guide

This project uses **pytest** and FastAPI’s TestClient for API tests. External
services (Cohere + vector store + LLM) are stubbed in tests to keep runs fast
and deterministic.

## How to Run

```bash
pytest -q
```

For verbose output:

```bash
pytest -v
```

## Test Coverage (What is Verified)

- **Root endpoints**: `/` and `/health`
- **UI endpoint**: `/playground`
- **Generation**:
  - Validation errors for missing fields
  - Spec-compatible `/generate-copy` endpoint
  - Metadata and content fields in responses
- **Training data**:
  - List, stats, pagination
  - Create
  - Update/delete not found

## Why We Stub External Services

The API depends on:

- **Cohere** (embeddings + reranking)
- **FAISS** (vector store)
- **HF models** (generation)

To avoid network calls and model downloads in CI, the tests monkeypatch:

- `get_llm_service`
- `get_vector_store`
- `get_reranker_service`

This keeps CI stable and prevents failing tests when API keys are missing.

## Extending Tests

If you add new endpoints:

1. Add a new test class in `tests/test_api.py`.
2. Cover both success and failure cases.
3. If the endpoint touches external services, add a dummy stub or mock.

## CI Notes

GitHub Actions runs:

```bash
pytest -q
```

If you want live integration tests (real Cohere + real model), add a separate
workflow/job and mark it as optional.

