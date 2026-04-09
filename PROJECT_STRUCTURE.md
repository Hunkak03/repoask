# 📁 RepoAsk Project Structure

## Clean Organization

```
repoask/
│
├── 📄 Configuration Files (root)
│   ├── .env                 # Your API keys (git-ignored)
│   ├── .env.example         # Template for setup
│   ├── .gitignore           # Git exclusions
│   ├── .dockerignore        # Docker exclusions
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Container config
│   ├── Makefile             # Build commands
│   └── LICENSE              # MIT license
│
├── 📖 Documentation (root)
│   ├── README.md            # Main documentation
│   └── QUICKSTART.md        # Quick start guide
│
├── 🚀 Entry Point
│   └── run.py               # Double-click to start!
│
├── 🐍 Source Code (src/)
│   ├── __init__.py          # Package init
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings & config
│   ├── models.py            # Data validation
│   ├── rag_engine.py        # AI RAG engine
│   └── git_utils.py         # Git cloning utils
│
├── 🎨 Frontend (frontend/)
│   └── index.html           # Web UI
│
├── 📊 Data (data/) - Auto-generated
│   ├── codigo_a_analizar/   # Local code to analyze
│   └── repositories/        # Cloned Git repos
│
├── 🧪 Tests (tests/)
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_models.py
│   └── test_api.py
│
└── 💾 Storage (storage/) - Auto-generated
    └── vector index files
```

## 🎯 Quick Navigation

| What you need | Where to find it |
|---------------|------------------|
| **Start the app** | `run.py` (root) |
| **API keys** | `.env` (root) |
| **Server code** | `src/main.py` |
| **Web UI** | `frontend/index.html` |
| **Clone repos** | `data/repositories/` (auto-created) |
| **Config** | `src/config.py` |
| **AI engine** | `src/rag_engine.py` |

## 🚀 How to Run

### Option 1: Double-click (Easiest)
```bash
python run.py
```

### Option 2: Use Makefile
```bash
make run
```

### Option 3: Direct
```bash
cd src
python main.py
```

## 📝 Development

### Add new feature
1. Create file in `src/`
2. Import in `main.py`
3. Add endpoint

### Add tests
1. Create file in `tests/`
2. Run: `make test`

### Update dependencies
1. Edit `requirements.txt`
2. Run: `make install`

## 🗂️ File Categories

**Root Level** - Only essential files
- Entry points (`run.py`)
- Documentation (`README.md`, `QUICKSTART.md`)
- Build config (`Makefile`, `Dockerfile`, `requirements.txt`)
- User config (`.env`, `.env.example`)

**src/** - All application code
- Each file has single responsibility
- Imports use relative paths
- No business logic in `main.py`

**data/** - User data only
- Auto-generated
- Can be safely deleted
- Git-ignored

**frontend/** - Web interface
- Single HTML file
- All CSS inline
- All JS inline

**tests/** - Test suite
- Mirror src/ structure
- Independent modules
- Mock external services

## ✨ Design Principles

1. **Root is clean** - Only files you interact with regularly
2. **src/ has code** - All Python source in one place
3. **data/ is temporary** - Safe to delete anytime
4. **Clear separation** - Config, code, data, UI, tests
5. **Easy navigation** - Know exactly where to look

---

**Total files in root: 11** (down from 20+) 🎉
