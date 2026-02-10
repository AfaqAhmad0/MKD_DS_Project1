# =============================================================================
# Marketing Assistant AI - API Tests
# =============================================================================
# Basic tests to verify the API is working correctly.
# Run with: pytest tests/test_api.py -v
# =============================================================================

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.schemas import (
    ContentType,
    GenerationResponse,
    MarketingContent,
    RetrievedContent,
)


# Create test client
client = TestClient(app)


# =============================================================================
# Test doubles (avoid external services in CI)
# =============================================================================

class DummyLLMService:
    async def generate(self, request, retrieved_content=None):
        return GenerationResponse(
            generated_content="Test output",
            content_type=request.content_type,
            prompt_used=request.prompt,
            similar_content_used=[
                r.content.title for r in (retrieved_content or [])
            ],
            generation_metadata={
                "model": "dummy",
                "device": "cpu",
                "temperature": 0.1,
            },
        )

    async def refine_content(self, original_content, feedback, content_type):
        return f"{original_content}\n\n[Refined: {feedback}]"


class DummyReranker:
    async def rerank(self, query, results, top_n=None):
        return results[: top_n or len(results)]


class DummyVectorStore:
    def __init__(self):
        self._items = {}

    async def add_content(self, content):
        self._items[str(content.id)] = content
        return content

    async def list_content(self, content_type=None, page=1, page_size=10):
        items = list(self._items.values())
        if content_type is not None:
            items = [i for i in items if i.content_type == content_type]
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        return items[start:end], total

    async def get_content(self, content_id):
        return self._items.get(str(content_id))

    async def update_content(self, content_id, updates):
        key = str(content_id)
        item = self._items.get(key)
        if item is None:
            return None
        updated = item.model_copy(update=updates)
        self._items[key] = updated
        return updated

    async def delete_content(self, content_id):
        return self._items.pop(str(content_id), None) is not None

    async def search(self, query, k=10, content_type=None):
        items = list(self._items.values())
        if content_type is not None:
            items = [i for i in items if i.content_type == content_type]
        results = [
            RetrievedContent(
                content=i,
                similarity_score=0.9,
                rerank_score=0.9,
            )
            for i in items[:k]
        ]
        return results

    def get_stats(self):
        return {
            "total_documents": len(self._items),
            "dimension": 1024,
        }


@pytest.fixture(autouse=True)
def stub_services(monkeypatch):
    """Stub external services to keep tests fast and deterministic."""
    dummy_store = DummyVectorStore()
    seed_content = MarketingContent(
        title="Seed Email",
        content="Welcome to our community.",
        content_type=ContentType.EMAIL,
        metadata={"seeded": True},
        tags=["welcome"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    dummy_store._items[str(seed_content.id)] = seed_content

    monkeypatch.setattr(
        "backend.routers.generation.get_llm_service",
        lambda: DummyLLMService(),
    )
    monkeypatch.setattr(
        "backend.routers.generation.get_vector_store",
        lambda: dummy_store,
    )
    monkeypatch.setattr(
        "backend.routers.generation.get_reranker_service",
        lambda: DummyReranker(),
    )
    monkeypatch.setattr(
        "backend.routers.training_data.get_vector_store",
        lambda: dummy_store,
    )
    return dummy_store


class TestRootEndpoints:
    """Tests for root-level API endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["name"] == "Marketing Assistant AI"
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify health check structure
        assert "status" in data
        assert "services" in data
        assert data["status"] in ["healthy", "degraded"]

    def test_playground_endpoint(self):
        """Ensure the demo UI is available."""
        response = client.get("/playground")
        assert response.status_code == 200
        assert "Marketing Assistant AI" in response.text


class TestGenerationEndpoints:
    """Tests for content generation endpoints."""
    
    def test_list_content_types(self):
        """Test listing available content types."""
        response = client.get("/api/v1/generate/content-types")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify we have content types
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify each type has required fields
        for content_type in data:
            assert "value" in content_type
            assert "name" in content_type
            assert "description" in content_type
    
    def test_generate_requires_prompt(self):
        """Test that generation requires a valid prompt."""
        # Empty request should fail validation
        response = client.post(
            "/api/v1/generate",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_generate_requires_content_type(self):
        """Test that generation requires a content type."""
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Write a test email"
            }
        )
        
        assert response.status_code == 422  # Validation error

    def test_generate_copy_public_endpoint(self):
        """Spec-compatible endpoint should return generated content."""
        response = client.post(
            "/generate-copy",
            json={"prompt": "Write a welcome email"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "generated_content" in data
        assert data["content_type"] == ContentType.CAMPAIGN.value

    def test_generate_endpoint_returns_metadata(self):
        response = client.post(
            "/api/v1/generate",
            json={
                "prompt": "Write a test email",
                "content_type": "email",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["generation_metadata"]["model"] == "dummy"


class TestTrainingDataEndpoints:
    """Tests for training data CRUD endpoints."""
    
    def test_list_training_data(self):
        """Test listing training data."""
        response = client.get("/api/v1/training-data")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
    
    def test_get_stats(self):
        """Test getting training data statistics."""
        response = client.get("/api/v1/training-data/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify stats structure
        assert "total_documents" in data
        assert "dimension" in data

    def test_create_training_data(self):
        response = client.post(
            "/api/v1/training-data",
            json={
                "title": "Launch Email",
                "content": "We are live.",
                "content_type": "email",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Launch Email"

    def test_update_training_data_not_found(self):
        response = client.put(
            "/api/v1/training-data/00000000-0000-0000-0000-000000000000",
            json={"title": "Updated"},
        )
        assert response.status_code == 404

    def test_delete_training_data_not_found(self):
        response = client.delete(
            "/api/v1/training-data/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code == 404
    
    def test_training_data_pagination(self):
        """Test pagination parameters are accepted."""
        response = client.get(
            "/api/v1/training-data",
            params={"page": 1, "page_size": 5}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["page"] == 1
        assert data["page_size"] == 5
    
    def test_training_data_content_type_filter(self):
        """Test filtering by content type."""
        response = client.get(
            "/api/v1/training-data",
            params={"content_type": "email"}
        )
        
        assert response.status_code == 200
    
    def test_create_training_data_validation(self):
        """Test training data creation validation."""
        # Missing required fields
        response = client.post(
            "/api/v1/training-data",
            json={}
        )
        
        assert response.status_code == 422  # Validation error


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_not_found_training_data(self):
        """Test 404 response for non-existent training data."""
        # Using a random UUID that shouldn't exist
        response = client.get(
            "/api/v1/training-data/00000000-0000-0000-0000-000000000000"
        )
        
        assert response.status_code == 404
    
    def test_invalid_content_type(self):
        """Test validation for invalid content type."""
        response = client.get(
            "/api/v1/training-data",
            params={"content_type": "invalid_type"}
        )
        
        assert response.status_code == 422


# =============================================================================
# Run tests when executed directly
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
