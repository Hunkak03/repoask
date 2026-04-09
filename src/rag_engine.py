"""RAG engine with lazy initialization and conversation history."""

import os
import logging
from pathlib import Path
from typing import Optional
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.chat_engine import ContextChatEngine

from config import settings

logger = logging.getLogger(__name__)


class RAGEngine:
    """Retrieval-Augmented Generation engine with lazy initialization."""

    def __init__(self):
        self._index = None
        self._query_engine = None
        self._chat_engine = None
        self._initialized = False
        self._files_indexed = 0

    def _setup_llm(self):
        """Configure LLM and embedding model."""
        Settings.llm = Groq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            system_prompt=settings.get_system_prompt()
        )
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=settings.EMBEDDING_MODEL
        )
        logger.info(f"LLM configured: {settings.GROQ_MODEL}")

    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        if not settings.DATA_DIR.exists():
            settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created data directory: {settings.DATA_DIR}")

    def _count_files(self) -> int:
        """Count files in data directory."""
        if not settings.DATA_DIR.exists():
            return 0
        return len([
            f for f in settings.DATA_DIR.iterdir()
            if f.is_file() and f.name != '.gitkeep'
        ])

    def _build_index_from_dir(self, directory: Path) -> None:
        """Build index from a directory of files."""
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            self._index = VectorStoreIndex.from_documents([])
            return

        # Check if directory has any files (excluding .gitkeep)
        try:
            documents = SimpleDirectoryReader(
                str(directory),
                recursive=True,
                required_exts=None  # Don't filter extensions
            ).load_data()
        except ValueError as e:
            if "No files found" in str(e):
                logger.info(f"No files in {directory}, starting with empty index")
                self._index = VectorStoreIndex.from_documents([])
                return
            raise

        if not documents:
            logger.warning(f"No documents found in {directory}")
            self._index = VectorStoreIndex.from_documents([])
        else:
            self._index = VectorStoreIndex.from_documents(documents)
            settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            self._index.storage_context.persist(
                persist_dir=str(settings.STORAGE_DIR)
            )
            logger.info(f"Index built and persisted with {len(documents)} documents")

    def load_repository(self, repo_path: str):
        """Load a specific repository into the RAG engine."""
        logger.info(f"Loading repository: {repo_path}")
        path = Path(repo_path)
        
        if not path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        # Reinitialize LLM if needed
        if not self._initialized:
            self._setup_llm()

        # Build index from repository
        self._build_index_from_dir(path)
        
        self._files_indexed = len(list(path.rglob('*')))
        
        # Initialize engines
        self._query_engine = self._index.as_query_engine(
            similarity_top_k=settings.SIMILARITY_TOP_K
        )
        self._chat_engine = self._index.as_chat_engine(
            chat_mode="context",
            similarity_top_k=settings.SIMILARITY_TOP_K,
            system_prompt=settings.get_system_prompt()
        )
        
        self._initialized = True
        logger.info(f"Repository loaded successfully: {repo_path}")

    def initialize(self):
        """Initialize the RAG engine (lazy loading)."""
        if self._initialized:
            return

        logger.info("Initializing RAG engine...")
        self._setup_llm()
        self._ensure_data_dir()

        try:
            # Try to load existing index
            if settings.STORAGE_DIR.exists() and (settings.STORAGE_DIR / "docstore.json").exists():
                logger.info("Loading existing index from storage...")
                storage_context = StorageContext.from_defaults(
                    persist_dir=str(settings.STORAGE_DIR)
                )
                self._index = load_index_from_storage(storage_context)
                logger.info("Index loaded successfully")
            else:
                logger.info("Building new index from documents...")
                self._build_index_from_dir(settings.DATA_DIR)

            self._files_indexed = self._count_files()

            # Initialize query engine
            self._query_engine = self._index.as_query_engine(
                similarity_top_k=settings.SIMILARITY_TOP_K
            )

            # Initialize chat engine with conversation history
            self._chat_engine = self._index.as_chat_engine(
                chat_mode="context",
                similarity_top_k=settings.SIMILARITY_TOP_K,
                system_prompt=settings.get_system_prompt()
            )

            self._initialized = True
            logger.info("RAG engine initialization complete")

        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}", exc_info=True)
            raise

    def query(self, message: str) -> dict:
        """Execute a query (single-turn)."""
        if not self._initialized:
            self.initialize()

        response = self._query_engine.query(message)

        # Extract unique source files
        sources = set()
        for node in response.source_nodes:
            fname = node.node.metadata.get('file_name', 'Unknown')
            sources.add(fname)

        return {
            "response": str(response),
            "sources": sorted(list(sources))
        }

    def chat(self, message: str, conversation_id: Optional[str] = None) -> dict:
        """Execute a chat message (with conversation history)."""
        if not self._initialized:
            self.initialize()

        # Reset chat history if needed (conversation_id could be used for session management)
        response = self._chat_engine.chat(message)

        # Extract unique source files
        sources = set()
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                fname = node.node.metadata.get('file_name', 'Unknown')
                sources.add(fname)

        return {
            "response": str(response),
            "sources": sorted(list(sources))
        }

    def rebuild_index(self):
        """Force rebuild the index from scratch."""
        logger.info("Rebuilding index...")
        self._initialized = False
        self._index = None
        self._query_engine = None
        self._chat_engine = None

        # Clear storage
        if settings.STORAGE_DIR.exists():
            import shutil
            shutil.rmtree(settings.STORAGE_DIR)
            logger.info("Cleared storage directory")

        self.initialize()
        logger.info("Index rebuilt successfully")

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def files_indexed(self) -> int:
        return self._files_indexed


# Singleton instance
rag_engine = RAGEngine()
