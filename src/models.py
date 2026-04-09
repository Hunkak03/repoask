"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class RepositoryRequest(BaseModel):
    """Repository clone request model."""

    url: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Git repository URL (HTTPS)",
        examples=["https://github.com/username/repository"]
    )


class RepositoryResponse(BaseModel):
    """Repository response model."""

    status: str
    message: str
    repository: Optional[dict] = None
    repositories: Optional[list[dict]] = None


class ChatRequest(BaseModel):
    """Chat message request model."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question or command",
        examples=["Audit this code for security vulnerabilities"]
    )


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str = Field(..., description="AI response text")
    sources: list[str] = Field(default_factory=list, description="Source files referenced")
    conversation_id: Optional[str] = Field(None, description="Conversation session ID")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    model_loaded: bool
    files_indexed: int


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
