# 🤖 RepoAsk: AI-Powered Repository Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-7fff9a.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-4f9eff.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-7fff9a.svg)](https://fastapi.tiangolo.com/)

**RepoAsk** is a high-performance RAG (Retrieval-Augmented Generation) engine designed to transform your local source code into a searchable, conversational database. Stop reading thousands of lines; start asking.

---

## 🇺🇸 English Guide

### 🚀 Key Capabilities
- **Local Neural Indexing:** Utilizes `BAAI/bge-small-en-v1.5` embeddings for zero-cost, private document vectorization.
- **Ultra-Fast Inference:** Integrated with **Groq Llama 3** for near-instant contextual responses.
- **Persistent Knowledge Base:** Automatic storage in `./storage` to avoid re-indexing overhead.
- **Modern Developer UI:** A sleek, JetBrains-inspired dashboard built with FastAPI and asynchronous JavaScript.

### 🛠️ Quick Start

1. **System Requirements**
   ```bash
   pip install -r requirements.txt
Environment Configuration
Create a .env file in the root directory:

Fragmento de código
GROQ_API_KEY=your_groq_api_key_here
Execution

Place your source files in /codigo_a_analizar.

Start the engine: python main.py

Access the UI: http://localhost:8000

🇪🇸 Guía en Español
🚀 Capacidades Clave
Indexación Neuronal Local: Utiliza embeddings BAAI/bge-small-en-v1.5 para una vectorización privada y gratuita.

Inferencia Ultra-Rápida: Integración con Groq Llama 3 para obtener respuestas contextuales instantáneas.

Base de Conocimiento Persistente: Almacenamiento automático en ./storage para evitar re-indexar en cada inicio.

Interfaz para Desarrolladores: Dashboard moderno inspirado en JetBrains, construido con FastAPI y JavaScript asíncrono.

🛠️ Inicio Rápido
Requisitos del Sistema

Bash
pip install -r requirements.txt
Configuración de Entorno
Crea un archivo .env en la raíz del proyecto:

Fragmento de código
GROQ_API_KEY=tu_clave_de_groq_aqui
Ejecución

Coloca tus archivos fuente en /codigo_a_analizar.

Arranca el motor: python main.py

Accede a la interfaz: http://localhost:8000

⚙️ Technical Architecture
RepoAsk operates on a Vector-Store RAG architecture:

Ingestion: Documents are parsed from the local directory.

Embedding: Local models transform code blocks into high-dimensional vectors.

Retrieval: Semantic search identifies relevant code context based on user queries.

Generation: Groq LLM synthesizes an answer using only the retrieved context.

Developed by Hunkak03