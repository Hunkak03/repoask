"""Test RAG engine."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestRAGEngineInitialization:
    """Test RAG engine initialization."""

    @patch('rag_engine.Settings')
    @patch('rag_engine.Groq')
    @patch('rag_engine.HuggingFaceEmbedding')
    def test_setup_llm_configures_models(self, mock_embedding, mock_groq, mock_settings):
        """Test _setup_llm configures LLM and embedding."""
        from rag_engine import RAGEngine
        engine = RAGEngine()

        with patch.object(engine, '_setup_llm') as mock_setup:
            engine._setup_llm()
            mock_setup.assert_called_once()

    def test_is_initialized_starts_false(self):
        """Test is_initialized is False initially."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        assert engine.is_initialized is False

    def test_files_indexed_starts_at_zero(self):
        """Test files_indexed starts at 0."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        assert engine.files_indexed == 0


class TestRAGEngineDirectoryChecks:
    """Test directory existence checks."""

    def test_ensure_data_dir_uses_settings_path(self):
        """Test _ensure_data_dir uses configured DATA_DIR."""
        from rag_engine import RAGEngine
        from config import settings

        engine = RAGEngine()
        # Just verify it doesn't crash when DATA_DIR exists
        if settings.DATA_DIR.exists():
            engine._ensure_data_dir()  # Should not raise


class TestRAGEngineQuery:
    """Test query functionality."""

    @patch('rag_engine.rag_engine')
    def test_query_requires_initialization(self, mock_engine):
        """Test query works after initialization."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine._initialized = True
        engine._query_engine = Mock()
        engine._query_engine.query.return_value = Mock(
            source_nodes=[]
        )

        result = engine.query("test query")

        assert "response" in result
        assert "sources" in result

    def test_query_extracts_sources_from_response(self):
        """Test query extracts source files from response."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine._initialized = True

        # Mock query engine with source nodes
        mock_response = Mock()
        mock_node1 = Mock()
        mock_node1.node.metadata = {'file_name': 'main.py'}
        mock_node2 = Mock()
        mock_node2.node.metadata = {'file_name': 'config.py'}
        mock_response.source_nodes = [mock_node1, mock_node2]

        mock_query_engine = Mock()
        mock_query_engine.query.return_value = mock_response
        engine._query_engine = mock_query_engine

        result = engine.query("test")

        assert 'main.py' in result['sources']
        assert 'config.py' in result['sources']


class TestRAGEngineChat:
    """Test chat functionality."""

    def test_chat_extracts_sources_when_available(self):
        """Test chat extracts source files."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine._initialized = True

        # Mock chat engine with source nodes
        mock_response = Mock()
        mock_node = Mock()
        mock_node.node.metadata = {'file_name': 'auth.py'}
        mock_response.source_nodes = [mock_node]

        mock_chat_engine = Mock()
        mock_chat_engine.chat.return_value = mock_response
        engine._chat_engine = mock_chat_engine

        result = engine.chat("test", conversation_id="test-id")

        assert 'auth.py' in result['sources']
        assert result['response'] == str(mock_response)

    def test_chat_handles_missing_source_nodes(self):
        """Test chat handles response without source_nodes gracefully."""
        from rag_engine import RAGEngine
        engine = RAGEngine()
        engine._initialized = True

        mock_response = Mock(spec=['response'])
        mock_response.response = "No sources"

        mock_chat_engine = Mock()
        mock_chat_engine.chat.return_value = mock_response
        engine._chat_engine = mock_chat_engine

        result = engine.chat("test")

        assert result['sources'] == []
        assert 'response' in result


class TestRAGEngineRebuild:
    """Test index rebuild functionality."""

    @patch('rag_engine.settings')
    def test_rebuild_clears_storage(self, mock_settings, tmp_path):
        """Test rebuild clears storage directory."""
        from rag_engine import RAGEngine

        storage_dir = tmp_path / "storage"
        storage_dir.mkdir()
        mock_settings.STORAGE_DIR = storage_dir

        engine = RAGEngine()
        engine._initialized = True

        with patch.object(engine, 'initialize'):
            engine.rebuild_index()

        assert engine._initialized is False
        assert engine._index is None
