.PHONY: help install run dev test clean docker-build docker-run

help:
	@echo "RepoAsk - Professional Code Auditor & RAG Engine"
	@echo ""
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  run         Start production server"
	@echo "  dev         Start development server with hot reload"
	@echo "  test        Run tests"
	@echo "  clean       Clean cache and storage"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run Docker container"
	@echo ""

install:
	pip install -r requirements.txt

run:
	python run.py

dev:
	python -c "import os; os.environ['DEBUG']='true'; exec(open('run.py').read())"

test:
	python -m pytest tests/ -v --tb=short

clean:
	@echo "Cleaning cache files..."
	@python -c "import shutil; from pathlib import Path; [shutil.rmtree(p, ignore_errors=True) for p in ['__pycache__', 'storage', 'src/__pycache__', 'tests/__pycache__']]; [f.unlink() for f in Path('.').rglob('*.pyc') if f.is_file()]"
	@echo "Clean complete!"

docker-build:
	docker build -t repoask:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env repoask:latest
