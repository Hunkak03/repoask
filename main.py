import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

load_dotenv()

app = FastAPI()

# Configuración de Modelos
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

PERSIST_DIR = "./storage"
DATA_DIR = "./codigo_a_analizar"

# Crear carpeta de datos si no existe
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
query_engine = index.as_query_engine(similarity_top_k=3)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = query_engine.query(request.message)
        
        # Extraer fuentes únicas de los metadatos
        sources = set()
        for node in response.source_nodes:
            # LlamaIndex guarda el nombre del archivo en metadata['file_name']
            fname = node.node.metadata.get('file_name', 'Archivo desconocido')
            sources.add(fname)
        
        source_list = list(sources)
        
        return {
            "response": str(response),
            "sources": source_list
        }
    except Exception as e:
        return {"response": f"Error del servidor: {str(e)}", "sources": []}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)