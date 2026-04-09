"""Test API models."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic import ValidationError
from models import ChatRequest, ChatResponse, HealthResponse


class TestChatRequest:
    """Test ChatRequest model."""

    def test_valid_request(self):
        """Test valid chat request."""
        request = ChatRequest(message="Audit this code")
        assert request.message == "Audit this code"

    def test_empty_message_raises_error(self):
        """Test empty message raises validation error."""
        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_too_long_message_raises_error(self):
        """Test message over 5000 chars raises validation error."""
        with pytest.raises(ValidationError):
            ChatRequest(message="a" * 5001)


class TestChatResponse:
    """Test ChatResponse model."""

    def test_valid_response(self):
        """Test valid chat response."""
        response = ChatResponse(
            response="Analysis complete",
            sources=["main.py", "config.py"]
        )
        assert response.response == "Analysis complete"
        assert len(response.sources) == 2

    def test_response_with_empty_sources(self):
        """Test response with no sources."""
        response = ChatResponse(response="No sources")
        assert response.sources == []


class TestHealthResponse:
    """Test HealthResponse model."""

    def test_healthy_response(self):
        """Test healthy status response."""
        response = HealthResponse(
            status="healthy",
            version="2.0.0",
            model_loaded=True,
            files_indexed=10
        )
        assert response.status == "healthy"
        assert response.files_indexed == 10
