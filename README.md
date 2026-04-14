# 🤖 RepoAsk — AI Code Auditor & Repository Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-7fff9a.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-4f9eff.svg?style=flat-square)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg?style=flat-square)](https://fastapi.tiangolo.com/)
[![LLM: Groq](https://img.shields.io/badge/LLM-Groq-F5A623.svg?style=flat-square)](https://console.groq.com/)
[![RAG: LlamaIndex](https://img.shields.io/badge/RAG-LlamaIndex-ff6b6b.svg?style=flat-square)](https://docs.llamaindex.ai/)
[![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat-square)](https://www.docker.com/)

**RepoAsk** is an enterprise-grade AI-powered code analysis platform that combines **Retrieval-Augmented Generation (RAG)** with advanced LLM capabilities to deliver automated code auditing, intelligent documentation, and conversational code exploration. Clone any Git repository via URL and receive instant, context-aware technical insights with full source traceability.

---

## 🚀 Key Features

- **⚡ Instant Repository Loading** — Paste any GitHub/GitLab URL to analyze code within seconds
- **🔒 Security-First Auditing** — Automated vulnerability detection, OWASP compliance checks, and logic flaw identification
- **📝 Technical Documentation Generator** — Generate structured READMEs, API docs, and architecture diagrams
- **🧠 Multi-Turn Conversational AI** — Context-aware chat with persistent session history
- **🎯 Source-Cited Responses** — Every AI response includes linked file references for verification
- **🏠 Privacy-Preserving Embeddings** — Local vector indexing using `BAAI/bge-small-en-v1.5` (zero data leakage)
- **🌐 Multi-Language Support** — Configurable AI response language (English/Spanish)
- **📦 Repository Management UI** — Clone, switch, and delete repositories from the dashboard
- **🔌 RESTful API** — Full programmatic access to all features via documented endpoints

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Docker Deployment](#-docker-deployment)
- [Development](#-development)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔧 Prerequisites

Before installation, ensure your system meets the following requirements:

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Python** | 3.11 | 3.12+ |
| **RAM** | 8 GB | 16 GB+ (for embedding models) |
| **Disk Space** | 2 GB | 5 GB+ (for model caching) |
| **Git** | 2.0+ | Latest |
| **Groq API Key** | Required | [Get one here](https://console.groq.com/) |

---

## 📦 Installation

Choose one of the following installation methods:

### Option 1: Standard Installation (Recommended)

**1. Clone the repository**
```bash
git clone https://github.com/Hunkak03/repoask.git
cd repoask
```

**2. Create a virtual environment (recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
# Using Make (cross-platform)
make install

# Or directly with pip
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```ini
GROQ_API_KEY=your_actual_api_key_here
```

**5. Start the server**
```bash
make run
# or: python run.py
```

**6. Access the dashboard**

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

### Option 2: Docker Installation

**1. Clone the repository**
```bash
git clone https://github.com/Hunkak03/repoask.git
cd repoask
```

**2. Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

**3. Build and run**
```bash
# Build image
make docker-build

# Run container
make docker-run
```

The server will be available at [http://localhost:8000](http://localhost:8000).

---

## 🎯 Quick Start

### Step 1: Load a Repository

1. Open [http://localhost:8000](http://localhost:8000)
2. Paste a repository URL in the left panel:
   ```
   https://github.com/pallets/flask
   ```
3. Click **🔄 Clone Repository**
4. Wait for the indexing to complete (status indicator turns green)

### Step 2: Start Analyzing

Use the quick action buttons or type custom queries:

| Button | Purpose | Example Query |
|--------|---------|---------------|
| **🔍 AUDIT** | Security & quality review | "Find all SQL injection vulnerabilities" |
| **📄 DOCS** | Documentation generation | "Create API documentation for all endpoints" |
| **💡 EXPLAIN** | Code comprehension | "How does the authentication middleware work?" |
| **⚡ OPTIMIZE** | Performance improvement | "Identify N+1 query problems in database calls" |

---

## 📖 Usage Guide

### Common Analysis Prompts

#### 🔐 Security Audit
```
Perform a comprehensive security audit focusing on:
- OWASP Top 10 vulnerabilities
- Input validation gaps
- Authentication/authorization flaws
- Secrets or hardcoded credentials
```

#### 📚 Generate Documentation
```
Generate comprehensive technical documentation including:
- Architecture overview
- API endpoint descriptions
- Database schema
- Deployment instructions
```

#### 🔍 Code Review
```
Review this codebase for:
- Error handling completeness
- Logging consistency
- Test coverage gaps
- Code duplication
```

#### ⚙️ Architecture Analysis
```
Explain the system architecture:
- Entry points and main flows
- Design patterns used
- External dependencies
- Scalability bottlenecks
```

### Managing Repositories

**List all loaded repositories:**
```bash
curl http://localhost:8000/api/repositories
```

**Delete a repository:**
```bash
curl -X DELETE http://localhost:8000/api/repository/<repo_name>
```

**Rebuild the index:**
```bash
curl -X POST http://localhost:8000/api/rebuild-index
```

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through the `.env` file in the project root:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Groq API authentication key | — | ✅ Yes |
| `GROQ_MODEL` | LLM model identifier | `llama-3.3-70b-versatile` | No |
| `SYSTEM_LANGUAGE` | AI response language (`en`/`es`) | `en` | No |
| `HOST` | Server bind address | `0.0.0.0` | No |
| `PORT` | Server port number | `8000` | No |
| `DEBUG` | Enable development mode with hot reload | `false` | No |
| `SIMILARITY_TOP_K` | Number of context chunks to retrieve | `5` | No |
| `EMBEDDING_MODEL` | HuggingFace embedding model name | `BAAI/bge-small-en-v1.5` | No |

### Advanced Configuration

To customize the system prompt, modify `src/config.py`:

```python
@classmethod
def get_system_prompt(cls) -> str:
    return """Your custom system prompt here..."""
```

---

## 📡 API Reference

Full API documentation with interactive testing is available at `/docs` when the server is running.

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server health and status check |
| `POST` | `/api/chat` | Send a message to the AI assistant |
| `POST` | `/api/repository` | Clone and index a Git repository |
| `GET` | `/api/repositories` | List all cloned repositories |
| `DELETE` | `/api/repository/{name}` | Delete a cloned repository |
| `POST` | `/api/rebuild-index` | Force rebuild of the vector index |

### Example: Chat Request

**Request:**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What are the main security concerns in this codebase?"
}
```

**Response:**
```json
{
  "response": "Based on my analysis, the main security concerns are:\n\n1. **SQL Injection**: Raw queries in database.py...",
  "sources": ["database.py", "auth.py", "config.py"],
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Example: Clone Repository

**Request:**
```http
POST /api/repository
Content-Type: application/json

{
  "url": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully cloned and indexed repository (42 files)",
  "repository": {
    "name": "repository",
    "url": "https://github.com/username/repository.git",
    "path": "/path/to/data/repositories/repository",
    "branch": "main",
    "commit": "abc12345",
    "files_indexed": 42
  }
}
```

---

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build with production optimizations
docker build -t repoask:latest .

# Run with resource limits
docker run -d \
  --name repoask \
  -p 8000:8000 \
  --memory=4g \
  --cpus=2 \
  --env-file .env \
  -v repoask-data:/app/data \
  repoask:latest
```

### Docker Compose (Recommended for Production)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  repoask:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - repoask-data:/app/data
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'

volumes:
  repoask-data:
```

Run with:
```bash
docker-compose up -d
```

---

## 💻 Development

### Development Setup

```bash
# Install dependencies
make install

# Start with hot reload (auto-restart on file changes)
make dev

# Run tests
make test

# Clean build artifacts
make clean
```

### Project Structure

```
repoask/
├── src/                      # Application source code
│   ├── __init__.py           # Package version
│   ├── main.py               # FastAPI application & routes
│   ├── config.py             # Configuration management
│   ├── models.py             # Pydantic data models
│   ├── rag_engine.py         # RAG indexing & query engine
│   └── git_utils.py          # Git repository management
├── frontend/                 # Web interface
│   └── index.html            # Single-page application
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_models.py
│   └── test_api.py
├── data/                     # Data directory (auto-generated)
│   ├── codigo_a_analizar/    # Legacy code folder
│   └── repositories/         # Cloned Git repositories
├── storage/                  # Vector index cache (auto-generated)
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
├── Makefile                  # Build automation
├── run.py                    # Application entry point
└── README.md                 # This file
```

---

## 🧠 Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          RepoAsk Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Web UI     │◄────►│   FastAPI    │◄────►│  Git Manager │  │
│  │  (Browser)   │      │   Server     │      │  (Cloning)   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                               │                                 │
│                               ▼                                 │
│                      ┌──────────────────┐                      │
│                      │    RAG Engine    │                      │
│                      │  (LlamaIndex)    │                      │
│                      └────────┬─────────┘                      │
│                               │                                 │
│              ┌────────────────┼────────────────┐               │
│              ▼                ▼                ▼               │
│     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│     │   Embedding  │ │ Vector Store │ │  LLM Client  │        │
│     │ (Local HF)   │ │  (In-Memory) │ │  (Groq API)  │        │
│     └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Repository Ingestion**
   - User provides Git URL → Server clones repository
   - Smart file filtering excludes binaries, dependencies, caches
   - Documents are chunked and embedded locally
   - Vectors are stored in persistent index

2. **Query Processing**
   - User submits question → Embedding model converts to vector
   - Top-K similar chunks are retrieved from index
   - Context + prompt are sent to Groq LLM
   - Response with source citations is returned

3. **Conversation Management**
   - Each chat session maintains context history
   - Subsequent questions build on previous answers
   - Source tracking enables verification of claims

---

## ⚠️ Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **`GROQ_API_KEY is not configured`** | Missing API key | Add `GROQ_API_KEY=your_key` to `.env` |
| **`Model not found (400 Error)`** | Invalid model name | Set `GROQ_MODEL=llama-3.3-70b-versatile` |
| **`Port 8000 already in use`** | Port conflict | Change `PORT` in `.env` or kill process |
| **`No files indexed`** | Empty repository | Ensure repo has supported file types |
| **`ImportError: No module named 'src'`** | Incorrect installation | Run `pip install -r requirements.txt` |
| **`Permission denied` on Windows** | Read-only `.git` files | Server handles this automatically now |
| **`CUDA out of memory`** | Insufficient GPU RAM | Use CPU-only mode or reduce model size |

### Logs & Debugging

**Enable debug logging:**
```bash
# Set DEBUG=true in .env
make dev
```

**View server logs:**
```bash
# Logs are written to repoask.log
tail -f repoask.log
```

**Test connectivity:**
```bash
# Check server health
curl http://localhost:8000/health

# Test API key
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

---

## 🧪 Testing

Run the full test suite:
```bash
make test
```

Run specific test files:
```bash
python -m pytest tests/test_api.py -v
python -m pytest tests/test_config.py -v
```

Generate coverage report:
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 🔐 Security Best Practices

- **Never commit `.env` files** — They contain sensitive API keys
- **Rotate exposed keys immediately** — Regenerate any leaked credentials
- **Local embeddings** — All vector embeddings are generated locally (zero data exfiltration)
- **Rate limiting** — Implement your own rate limiting for production deployments
- **HTTPS** — Use a reverse proxy (nginx, traefik) for TLS termination in production

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Hunkak03

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Community

- **Issues:** [GitHub Issues](https://github.com/Hunkak03/repoask/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Hunkak03/repoask/discussions)
- **Documentation:** [Wiki](https://github.com/Hunkak03/repoask/wiki)

---

<div align="center">

**Developed by [Hunkak03](https://github.com/Hunkak03)**

⭐ Star this repo if you find it helpful!

[![GitHub stars](https://img.shields.io/github/stars/Hunkak03/repoask?style=social)](https://github.com/Hunkak03/repoask/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Hunkak03/repoask?style=social)](https://github.com/Hunkak03/repoask/network/members)

</div>
