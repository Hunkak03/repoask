import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, StorageContext, 
    load_index_from_storage, Settings
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de IA
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# Cargar índice
PERSIST_DIR = "./storage"
REPO_PATH = "./codigo_a_analizar"

if not os.path.exists(PERSIST_DIR):
    if not os.path.exists(REPO_PATH): os.makedirs(REPO_PATH)
    documents = SimpleDirectoryReader(REPO_PATH).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = query_engine.query(request.message)
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir Frontend
if os.path.exists("./frontend"):
    app.mount("/", StaticFiles(directory="./frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Servidor en http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)