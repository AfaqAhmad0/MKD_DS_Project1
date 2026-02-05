# =============================================================================
# Marketing Assistant AI - API Tests
# =============================================================================
# Basic tests to verify the API is working correctly.
# Run with: pytest tests/test_api.py -v
# =============================================================================

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.schemas import ContentType


# Create test client
client = TestClient(app)


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
