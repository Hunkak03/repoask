"""Test configuration and settings."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Settings


class TestSettings:
    """Test configuration management."""

    def test_settings_has_required_attributes(self):
        """Verify Settings class has all required attributes."""
        assert hasattr(Settings, 'GROQ_API_KEY')
        assert hasattr(Settings, 'GROQ_MODEL')
        assert hasattr(Settings, 'PORT')
        assert hasattr(Settings, 'DATA_DIR')
        assert hasattr(Settings, 'STORAGE_DIR')

    def test_default_values(self):
        """Test default configuration values."""
        assert Settings.GROQ_MODEL == "llama-3.3-70b-versatile"
        assert Settings.PORT == 8000
        assert Settings.SIMILARITY_TOP_K == 5

    def test_validate_raises_error_for_missing_key(self, monkeypatch):
        """Test validation raises error for missing API key."""
        monkeypatch.setenv("GROQ_API_KEY", "")
        # Reload settings to pick up new env var
        import importlib
        import config
        importlib.reload(config)
        from config import Settings as TestSettings
        
        with pytest.raises(ValueError, match="GROQ_API_KEY"):
            TestSettings.validate()

    def test_get_system_prompt_returns_string(self):
        """Test system prompt returns non-empty string."""
        prompt = Settings.get_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0
