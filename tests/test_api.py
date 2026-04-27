"""
Integration tests for ElectionGuide AI API endpoints.
Uses FastAPI TestClient for endpoint validation without needing a running server.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set required env vars before importing app
os.environ.setdefault("GEMINI_API_KEY", "test-key-for-testing")
os.environ.setdefault("GOOGLE_API_KEY", "test-key-for-testing")

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Test the /api/health endpoint."""

    def test_health_returns_200(self):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_has_status(self):
        response = client.get("/api/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_has_service_name(self):
        response = client.get("/api/health")
        data = response.json()
        assert data["service"] == "ElectionGuide AI"

    def test_health_has_model(self):
        response = client.get("/api/health")
        data = response.json()
        assert "model" in data


class TestTopicsEndpoint:
    """Test the /api/topics endpoint."""

    def test_topics_returns_200(self):
        response = client.get("/api/topics")
        assert response.status_code == 200

    def test_topics_has_list(self):
        response = client.get("/api/topics")
        data = response.json()
        assert "topics" in data
        assert isinstance(data["topics"], list)

    def test_topics_has_six_entries(self):
        response = client.get("/api/topics")
        data = response.json()
        assert len(data["topics"]) == 6

    def test_each_topic_has_required_fields(self):
        response = client.get("/api/topics")
        data = response.json()
        for topic in data["topics"]:
            assert "id" in topic
            assert "title" in topic
            assert "query" in topic


class TestCacheStatsEndpoint:
    """Test the /api/cache-stats endpoint."""

    def test_cache_stats_returns_200(self):
        response = client.get("/api/cache-stats")
        assert response.status_code == 200

    def test_cache_stats_has_fields(self):
        response = client.get("/api/cache-stats")
        data = response.json()
        assert "size" in data
        assert "hits" in data
        assert "misses" in data


class TestChatValidation:
    """Test input validation on the /api/chat endpoint."""

    def test_empty_message_rejected(self):
        response = client.post("/api/chat", json={"message": ""})
        assert response.status_code == 422  # Validation error

    def test_missing_message_rejected(self):
        response = client.post("/api/chat", json={})
        assert response.status_code == 422


class TestSecurityHeaders:
    """Test that security headers are present on responses."""

    def test_x_content_type_options(self):
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_x_frame_options(self):
        response = client.get("/api/health")
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_x_xss_protection(self):
        response = client.get("/api/health")
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_referrer_policy(self):
        response = client.get("/api/health")
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
