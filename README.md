# 🤖 RepoAsk: Professional Code Auditor & RAG Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-7fff9a.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-4f9eff.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

**RepoAsk** is an advanced AI-driven tool designed for automated code auditing, technical documentation, and repository intelligence. By leveraging **Retrieval-Augmented Generation (RAG)**, it allows developers to interact with their local codebase through a high-performance neural interface.

---

## 🇺🇸 English Guide

### 🚀 Key Functionalities
- **Automated Security Audit:** Identify vulnerabilities, logic flaws, and OWASP risks.
- **Instant Documentation:** Generate structured technical READMEs and module descriptions.
- **Neural Source Tracking:** Every AI response includes metadata-linked source citations.
- **Local Embedding Engine:** Uses `BAAI/bge-small-en-v1.5` for private, high-accuracy indexing.

### 🛠️ Installation & Setup
1. **Environment Setup**
   ```bash
   pip install -r requirements.txt
API Configuration
Create a .env file in the root directory:

Fragmento de código
GROQ_API_KEY=your_api_key_here
Execution

Place source files in /codigo_a_analizar.

Run the engine: python main.py

Access the dashboard: http://localhost:8000

⚠️ Troubleshooting (Common Errors)
"Model Decommissioned" (400 Error): Ensure main.py uses llama-3.3-70b-versatile.

IA Not "Seeing" New Files: Delete the ./storage folder and restart the server to force re-indexing.

Port 8000 in Use: Terminate existing Python processes or change the port in uvicorn.run().

🇪🇸 Guía en Español
🚀 Funcionalidades Clave
Auditoría de Seguridad Automatizada: Identificación de vulnerabilidades, fallos lógicos y riesgos OWASP.

Documentación Instantánea: Generación de READMEs técnicos estructurados y descripciones de módulos.

Rastreo de Fuentes Neuronal: Cada respuesta de la IA incluye citas de los archivos fuente originales.

Motor de Embeddings Local: Utiliza BAAI/bge-small-en-v1.5 para una indexación privada de alta precisión.

🛠️ Instalación y Configuración
Preparación del Entorno

Bash
pip install -r requirements.txt
Configuración de API
Crea un archivo .env en el directorio raíz:

Fragmento de código
GROQ_API_KEY=tu_clave_aqui
Ejecución

Coloca los archivos fuente en /codigo_a_analizar.

Inicia el motor: python main.py

Accede al dashboard: http://localhost:8000

⚠️ Resolución de Problemas (Errores Comunes)
"Model Decommissioned" (Error 400): Verifica que main.py utilice el modelo llama-3.3-70b-versatile.

La IA no detecta archivos nuevos: Elimina la carpeta ./storage y reinicia el servidor para forzar la re-indexación.

Puerto 8000 ocupado: Finaliza procesos de Python previos o cambia el puerto en uvicorn.run().

🧠 Technical Architecture
RepoAsk follows a Semantic Retrieval Workflow:

Parsing: Local files are ingested and cleaned.

Vectorization: Text is converted into high-dimensional vectors via HuggingFace.

Contextual Querying: User prompts retrieve the most relevant code snippets.

LLM Synthesis: Groq's Llama 3.3 synthesizes an expert-level technical response.

Developed by Hunkak03
Developed by Hunkak03