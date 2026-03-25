import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

app = FastAPI()

# --- CONFIGURACIÓN DE IA ---
# Usamos el modelo más reciente llama-3.3 y definimos su comportamiento
Settings.llm = Groq(
    model="llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY"),
    system_prompt="""Eres un Ingeniero de Software Senior y Auditor de Seguridad. 
    Tu objetivo es analizar el código proporcionado con precisión técnica.
    - Si te piden DOCUMENTACIÓN: Genera un README técnico estructurado (Arquitectura, Funciones, Instalación).
    - Si te piden AUDITORÍA: Busca errores de lógica, fallos de seguridad (OWASP) y falta de manejo de excepciones.
    - Siempre cita los archivos fuente al final de tu respuesta."""
)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

PERSIST_DIR = "./storage"
DATA_DIR = "./codigo_a_analizar"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_index():
    if os.path.exists(PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        return index

index = get_index()
query_engine = index.as_query_engine(similarity_top_k=5)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = query_engine.query(request.message)
        
        # Extraer nombres de archivos únicos de los metadatos
        sources = set()
        for node in response.source_nodes:
            fname = node.node.metadata.get('file_name', 'Desconocido')
            sources.add(fname)
        
        return {
            "response": str(response),
            "sources": list(sources)
        }
    except Exception as e:
        return {"response": f"Error: {str(e)}", "sources": []}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)