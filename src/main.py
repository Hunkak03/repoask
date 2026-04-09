"""RepoAsk: Professional Code Auditor & RAG Engine."""

import logging
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
import sys

# Add src/ to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from models import ChatRequest, ChatResponse, HealthResponse, ErrorResponse, RepositoryRequest, RepositoryResponse
from rag_engine import rag_engine
from git_utils import repo_manager
import __init__ as pkg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("repoask.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    logger.info("Starting RepoAsk server...")
    try:
        settings.validate()
        rag_engine.initialize()
        logger.info("RepoAsk server started successfully")
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise
    yield
    logger.info("Shutting down RepoAsk server...")


app = FastAPI(
    title="RepoAsk",
    description="Professional Code Auditor & RAG Engine",
    version=pkg.__version__,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if rag_engine.is_initialized else "initializing",
        version=pkg.__version__,
        model_loaded=rag_engine.is_initialized,
        files_indexed=rag_engine.files_indexed
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with conversation history support."""
    try:
        # Use chat engine for conversation history
        result = rag_engine.chat(
            message=request.message,
            conversation_id=str(uuid.uuid4())
        )

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            conversation_id=str(uuid.uuid4())
        )

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/rebuild-index")
async def rebuild_index():
    """Force rebuild the RAG index."""
    try:
        rag_engine.rebuild_index()
        return {"status": "success", "message": "Index rebuilt successfully"}
    except Exception as e:
        logger.error(f"Rebuild error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/repository", response_model=RepositoryResponse)
async def add_repository(request: RepositoryRequest):
    """Clone a repository from URL and load it into RAG engine."""
    try:
        # Clone repository
        repo_info = repo_manager.clone_repository(request.url)
        
        # Get code files
        code_files = repo_manager.get_code_files(repo_info['path'])
        file_count = len(code_files)
        
        # Update RAG engine to use this repository
        rag_engine.load_repository(repo_info['path'])
        
        return RepositoryResponse(
            status="success",
            message=f"Successfully cloned and indexed {repo_info['name']} ({file_count} files)",
            repository={
                **repo_info,
                'files_indexed': file_count
            }
        )
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Repository error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/repositories", response_model=RepositoryResponse)
async def list_repositories():
    """List all cloned repositories."""
    try:
        repos = repo_manager.list_repositories()
        return RepositoryResponse(
            status="success",
            message=f"Found {len(repos)} repositories",
            repositories=repos
        )
    except Exception as e:
        logger.error(f"List repositories error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/repository/{repo_name}")
async def delete_repository(repo_name: str):
    """Delete a cloned repository."""
    try:
        success = repo_manager.delete_repository(repo_name)
        if not success:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        return {"status": "success", "message": f"Deleted repository: {repo_name}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete repository error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Mount frontend (must be last to avoid route conflicts)
if settings.FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(settings.FRONTEND_DIR), html=True),
        name="frontend"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
