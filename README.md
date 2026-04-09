# 🤖 RepoAsk: AI Code Auditor & Repository Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-7fff9a.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-4f9eff.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**RepoAsk** is an advanced AI-driven tool designed for automated code auditing, technical documentation, and repository intelligence. By leveraging **Retrieval-Augmented Generation (RAG)**, it allows developers to interact with any Git repository through a simple URL paste, getting instant code analysis, reviews, and documentation.

---

## 🚀 Key Features

- **🔗 Instant Repository Cloning** — Paste any GitHub/GitLab URL to analyze code instantly
- **🔒 Automated Security Audit** — Identify vulnerabilities, logic flaws, and OWASP risks
- **📄 Instant Documentation** — Generate structured technical READMEs and module descriptions
- **🧠 Contextual Conversations** — Multi-turn chat with persistent conversation history
- **🎯 Neural Source Tracking** — Every AI response includes metadata-linked source citations
- **🏠 Local Embedding Engine** — Uses `BAAI/bge-small-en-v1.5` for private, high-accuracy indexing
- **🌐 Bilingual Support** — Configurable system language (English/Spanish)
- **📦 Repository Management** — Clone, switch, and delete repositories from the UI

---

## 📦 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git installed and in PATH
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd repoask
   ```

2. **Install dependencies**
   ```bash
   make install
   # or: pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy the example environment file
   copy .env.example .env   # Windows
   # cp .env.example .env   # Linux/Mac
   
   # Edit .env and add your Groq API key
   ```

4. **Start the server**
   ```bash
   make run
   # or: python main.py
   ```

5. **Access the dashboard**
   
   Open http://localhost:8000 in your browser

6. **Paste a repository URL**
   
   Enter any public GitHub repository URL in the left panel and click "Clone Repository"

---

## 🎯 Usage Examples

### Clone a Repository
1. Open http://localhost:8000
2. Paste URL: `https://github.com/username/repository`
3. Click **🔄 Clone Repository**
4. Wait for indexing to complete

### Analyze Code
Once a repository is loaded, you can ask:

**Security Audit:**
> "Perform a complete technical audit. Identify vulnerabilities, logic errors, and improvement suggestions."

**Generate Documentation:**
> "Generate comprehensive technical documentation in Markdown format."

**Explain Architecture:**
> "Explain how this codebase works, including the architecture and key components."

**Optimize Code:**
> "Suggest performance optimizations, better design patterns, and code quality improvements."

**Specific Questions:**
> "How does the authentication flow work?"
> "What database queries are used?"
> "Are there any memory leaks?"

---

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | *(required)* |
| `GROQ_MODEL` | LLM model to use | `llama-3.3-70b-versatile` |
| `SYSTEM_LANGUAGE` | Response language (`en`/`es`) | `en` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable hot reload | `false` |
| `SIMILARITY_TOP_K` | Number of similar docs to retrieve | `5` |
| `EMBEDDING_MODEL` | Embedding model name | `BAAI/bge-small-en-v1.5` |

---

## 📡 API Documentation

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "model_loaded": true,
  "files_indexed": 42
}
```

### Chat Endpoint

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Audit this code for security vulnerabilities"
}
```

**Response:**
```json
{
  "response": "Security audit results: ...",
  "sources": ["main.py", "config.py", "auth.py"],
  "conversation_id": "uuid-string"
}
```

### Clone Repository

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
    "path": "/path/to/repositories/repository",
    "branch": "main",
    "commit": "abc12345",
    "files_indexed": 42
  }
}
```

### List Repositories

```http
GET /api/repositories
```

**Response:**
```json
{
  "status": "success",
  "message": "Found 3 repositories",
  "repositories": [
    {
      "name": "repository1",
      "path": "/path/to/repositories/repository1",
      "url": "https://github.com/user/repo1.git",
      "branch": "main"
    }
  ]
}
```

### Delete Repository

```http
DELETE /api/repository/{repo_name}
```

### Rebuild Index

```http
POST /api/rebuild-index
```

Forces a complete rebuild of the RAG index from scratch.

---

## 🧠 Technical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        RepoAsk System                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐ │
│  │   Frontend   │────▶│   FastAPI    │────▶│  Git Utils   │ │
│  │  (Web UI)    │◀────│    Server    │◀────│  (Cloning)   │ │
│  └──────────────┘     └──────────────┘     └──────────────┘ │
│                            │                         │        │
│                            │                         ▼        │
│                            │              GitHub/GitLab API   │
│                            │                                   │
│                            ▼                         │        │
│                   ┌──────────────┐                  │        │
│                   │   RAG        │◀─────────────────┘        │
│                   │   Engine     │                            │
│                   └──────────────┘                            │
│                            │                                   │
│                            ▼                                   │
│                   ┌──────────────────┐                         │
│                   │  Vector Store    │                         │
│                   │  (HuggingFace)   │                         │
│                   └──────────────────┘                         │
│                            │                                   │
│                            ▼                                   │
│                   ┌──────────────────┐                         │
│                   │  Groq LLM        │                         │
│                   │  (Llama 3.3 70B) │                         │
│                   └──────────────────┘                         │
└──────────────────────────────────────────────────────────────┘
```

### Workflow

1. **URL Input** — User pastes a Git repository URL in the web interface
2. **Cloning** — Repository is cloned locally with shallow clone (fast)
3. **Smart Filtering** — Only code files are included (excludes node_modules, vendor, etc.)
4. **Vectorization** — Text converted to high-dimensional vectors via HuggingFace
5. **Indexing** — Files are indexed and stored in vector database
6. **Ready to Query** — User can now ask questions about the codebase
7. **Contextual Querying** — User prompts retrieve relevant code snippets
8. **LLM Synthesis** — Groq's Llama 3.3 synthesizes expert-level technical responses
9. **Source Citation** — Original file sources are attached to each response

---

## 💡 Usage Examples

### Security Audit
Click the **🔍 SECURITY AUDIT** button or ask:
> "Perform a complete technical audit. Identify vulnerabilities, logic errors, and OWASP risks."

### Generate Documentation
Click the **📄 GENERATE DOCS** button or ask:
> "Generate comprehensive technical documentation in Markdown format."

### Code Optimization
Click the **⚡ OPTIMIZE CODE** button or ask:
> "Suggest performance optimizations and better design patterns."

### Custom Questions
Ask anything about your codebase:
> "How does the authentication flow work?"
> "What are the main entry points?"
> "Explain the database schema."

---

## 🐳 Docker Deployment

### Build Image
```bash
make docker-build
# or: docker build -t repoask:latest .
```

### Run Container
```bash
make docker-run
# or: docker run -p 8000:8000 --env-file .env repoask:latest
```

---

## ⚠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"GROQ_API_KEY is not configured"** | Add your API key to `.env` file |
| **Model not found (400 Error)** | Ensure `GROQ_MODEL=llama-3.3-70b-versatile` in `.env` |
| **AI not seeing new files** | Run `make clean` or delete `./storage` folder and restart |
| **Port 8000 in use** | Change `PORT` in `.env` or kill existing processes |
| **Import errors** | Run `make install` to ensure all dependencies are installed |

### Development Mode

Enable hot reloading for development:
```bash
make dev
# Sets DEBUG=true for automatic restart on file changes
```

### Clean Cache

Remove all cached files and rebuild index:
```bash
make clean
# Removes __pycache__, *.pyc, and storage/
```

---

## 🧪 Testing

Run the test suite:
```bash
make test
# or: python -m pytest tests/ -v
```

---

## 📁 Project Structure

```
repoask/
├── codigo_a_analizar/   # Local code to analyze (legacy)
├── repositories/        # Cloned Git repositories (auto-generated)
├── frontend/            # Web UI
│   └── index.html
├── storage/             # Cached vector index (auto-generated)
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_models.py
│   └── test_api.py
├── .env                 # Environment variables (git-ignored)
├── .env.example         # Environment template
├── .gitignore
├── config.py            # Configuration management
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic data models
├── rag_engine.py        # RAG engine with lazy loading
├── git_utils.py         # Git repository cloning utilities
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
├── .dockerignore
├── Makefile             # Build automation
└── LICENSE
```

---

## 🔐 Security Notes

- **Never commit `.env` files** — Contains sensitive API keys
- **Rotate exposed keys immediately** — If keys are leaked, regenerate them
- **Local embeddings** — All vector embeddings are generated locally (no data leaves your machine)
- **Rate limiting** — Add your own rate limiting for production deployments

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Developed by Hunkak03** | [GitHub](https://github.com/Hunkak03)
