"""
RepoAsk - AI Code Auditor & Repository Assistant
Run this file to start the server.
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to Python path so src/ is importable
sys.path.insert(0, str(Path(__file__).parent))

# Import and run
from src.main import app
from src.config import settings
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 RepoAsk - AI Code Auditor & Repository Assistant")
    print("="*60)
    print(f"\n📡 Server starting at: http://{settings.HOST}:{settings.PORT}")
    print(f"📊 Health check: http://{settings.HOST}:{settings.PORT}/health")
    print(f"🎯 Dashboard: http://localhost:{settings.PORT}")
    print("\n" + "="*60 + "\n")

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
