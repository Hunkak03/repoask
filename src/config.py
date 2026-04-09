"""Application configuration management."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of src/)
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings:
    """Centralized configuration manager."""

    # API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    SYSTEM_LANGUAGE: str = os.getenv("SYSTEM_LANGUAGE", "en")

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # RAG Configuration
    SIMILARITY_TOP_K: int = int(os.getenv("SIMILARITY_TOP_K", "5"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent  # Go up one level from src/
    DATA_DIR: Path = BASE_DIR / "data" / "codigo_a_analizar"
    REPO_DIR: Path = BASE_DIR / "data" / "repositories"
    STORAGE_DIR: Path = BASE_DIR / "storage"
    FRONTEND_DIR: Path = BASE_DIR / "frontend"

    # Validation
    MAX_QUERY_LENGTH: int = 5000
    MAX_CONVERSATION_HISTORY: int = 20

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GROQ_API_KEY or cls.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Please set it in your .env file. "
                "Get one at https://console.groq.com/"
            )

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get system prompt based on configured language."""
        if cls.SYSTEM_LANGUAGE.lower() == "es":
            return """Eres un Ingeniero de Software Senior y Auditor de Seguridad.
Tu objetivo es analizar el código proporcionado con precisión técnica.

- Si te piden DOCUMENTACIÓN: Genera un README técnico estructurado (Arquitectura, Funciones, Instalación).
- Si te piden AUDITORÍA: Busca errores de lógica, fallos de seguridad (OWASP) y falta de manejo de excepciones.
- Siempre cita los archivos fuente al final de tu respuesta.
- Responde en español."""
        else:
            return """You are a Senior Software Engineer and Security Auditor.
Your objective is to analyze provided code with technical precision.

- When asked for DOCUMENTATION: Generate a structured technical README (Architecture, Functions, Installation).
- When asked for AUDIT: Search for logic errors, security flaws (OWASP), and missing exception handling.
- Always cite source files at the end of your response.
- Respond in English."""


settings = Settings()
