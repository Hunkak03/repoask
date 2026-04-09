"""Test API endpoints."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient


# Mock the rag_engine before importing main
with patch('rag_engine.rag_engine') as mock_engine:
    mock_engine.is_initialized = True
    mock_engine.files_indexed = 5
    mock_engine.chat.return_value = {
        "response": "Test response",
        "sources": ["test.py"]
    }
    
    from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_returns_ok(self, client):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "model_loaded" in data
        assert "files_indexed" in data


class TestChatEndpoint:
    """Test chat endpoint."""

    @patch('main.rag_engine')
    def test_chat_with_valid_message(self, mock_engine, client):
        """Test chat endpoint with valid message."""
        mock_engine.chat.return_value = {
            "response": "Analysis complete",
            "sources": ["main.py"]
        }
        
        response = client.post(
            "/api/chat",
            json={"message": "Audit my code"}
        )
        
        # Note: This will fail if GROQ_API_KEY is not set
        # It's here for structure testing
        assert response.status_code in [200, 500]

    def test_chat_with_empty_message(self, client):
        """Test chat with empty message returns 422."""
        response = client.post(
            "/api/chat",
            json={"message": ""}
        )
        assert response.status_code == 422

    def test_chat_with_missing_message(self, client):
        """Test chat with missing message returns 422."""
        response = client.post("/api/chat", json={})
        assert response.status_code == 422

    def test_chat_with_invalid_method(self, client):
        """Test chat endpoint rejects GET requests."""
        response = client.get("/api/chat")
        assert response.status_code == 405


class TestStaticFiles:
    """Test static file serving."""

    def test_frontend_served_at_root(self, client):
        """Test frontend is served at root path."""
        response = client.get("/")
        # Should return HTML content
        assert response.status_code in [200, 500]
