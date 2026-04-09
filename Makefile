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
	set DEBUG=true && python run.py

test:
	python -m pytest tests/ -v --tb=short

clean:
	@echo "Cleaning cache files..."
	if exist __pycache__ rd /s /q __pycache__
	if exist storage rd /s /q storage
	for /r %%i in (*.pyc) do del "%%i"
	@echo "Clean complete!"

docker-build:
	docker build -t repoask:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env repoask:latest
