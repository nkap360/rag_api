#1. Importation des bibliothèques et modules nécessaires

# Importation des modules FastAPI et Pydantic pour la création de l'API et la validation des données.
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel, Field

# Importation des modules pour la gestion asynchrone des fichiers et la configuration.
import yaml
import aiofiles

# Importation des utilitaires personnalisés pour le téléversement et la recherche de fichiers.
from utils.indexer import FileUploader as FU
from utils.retriever import FileSearcher as FS
from typing import Optional

# Importation de Ollama pour l'utilisation du modèle de langage et des embeddings.
from llama_index.llms.ollama import Ollama


#2. Initialisation de l'API FastAPI et configuration
app = FastAPI()

# Chargement de la configuration à partir du fichier YAML.
with open("config.yml", "r") as conf:
    config = yaml.safe_load(conf)
    
# Initialisation de Ollama avec la configuration chargée.
llm = Ollama(model=config["llm"], url=config["qdrant_local"])


#3. Point d'entrée de l'API
@app.get("/")
def root():
    return {"message": "Research RAG"}

#4. Téléversement de fichiers
file_uploader = FU(config=config, llm=llm)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    try:
        await file_uploader.save_file(file)
        return {"message": f"File '{file.filename}' saved successfully"}
    except Exception as e:
        return {"error": f"An error occurred while saving the file: {str(e)}"}

#5. Définition des modèles Pydantic pour la validation des données
class Query(BaseModel):
    query: str
    similarity_top_k: Optional[int] = Field(default=1, ge=1, le=5)

class Response(BaseModel):
    search_result: str 
    source: str


#6. Recherche de fichiers
file_searcher = FS(config=config, llm=llm)
index = file_searcher.qdrant_index()

@app.post("/search/", response_model=Response, status_code=200)
def search(query: Query):
    query_engine = index.as_query_engine(similarity_top_k=query.similarity_top_k, output=Response, response_mode="tree_summarize", verbose=True)
    response = query_engine.query(query.query)
    response_object = Response(
        search_result=str(response).strip(), source=[response.metadata[k]["file_path"] for k in response.metadata.keys()][0]
    )
    return response_object


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)