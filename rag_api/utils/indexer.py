
from fastapi import UploadFile, HTTPException, File
import aiofiles
import  os
import re
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from tqdm import tqdm
import qdrant_client
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from fastembed.embedding import TextEmbedding


class FileUploader:
    def __init__(self,config,llm):
        self.config = config
        self.qdrant_client = qdrant_client.QdrantClient(
            url=self.config['qdrant_local'],
            timeout=self.config["qdrant_timeout"]
        )
        self.llm = llm
        os.makedirs(self.config['upload_dir'], exist_ok=True)



    def remove_non_alphanumeric(input_string):
        # Replace non-alphanumeric characters with an empty string
        cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
        return cleaned_string
        
    async def save_file(self, file: UploadFile):
        """
        Save the uploaded file based on its type.
        """
        file_path = os.path.join(self.config['upload_dir'], file.filename)
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension == ".pdf":
            await self.save_pdf(file, file_path)
        elif file_extension == ".csv":
            await self.save_csv(file, file_path)
        elif file_extension == ".txt":
            await self.save_text(file, file_path)
        elif file_extension == ".json":
            await self.save_json(file, file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        print("Loading Embedder...")
        data = FileUploader(self.config,self.llm)
        
        print("Embedder Loaded",)
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=self.config['embedding'])
        )
        
        
        
        print("Embedder modelled")
 
    
        await data.ingest(embedder=embed_model, llm=self.llm)



    async def save_pdf(self, file: UploadFile, file_path: str):
        # Implement PDF file saving logic here
        # Example: Save the PDF to the specified path
        async with aiofiles.open(file_path, "wb") as saved_file:
            await saved_file.write(await file.read())

    async def save_csv(self, file: UploadFile, file_path: str):
        # Implement CSV file saving logic here
        # Example: Save the CSV to the specified path
        async with aiofiles.open(file_path, "wb") as saved_file:
            await saved_file.write(await file.read())

    async def save_text(self, file: UploadFile, file_path: str):
        # Implement text file saving logic here
        # Example: Save the text file to the specified path
        async with aiofiles.open(file_path, "wb") as saved_file:
            await saved_file.write(await file.read())

    async def save_json(self, file: UploadFile, file_path: str):
        # Implement JSON file saving logic here
        # Example: Save the JSON file to the specified path
        async with aiofiles.open(file_path, "wb") as saved_file:
            await saved_file.write(await file.read())


    async def ingest(self, embedder, llm):
        print("Indexing data...")
        documents = SimpleDirectoryReader(self.config['upload_dir']).load_data()
        documents_with_progress = tqdm(documents, desc="Indexing Documents")

        #print(documents)
        qdrant_vector_store = QdrantVectorStore(
                client= self.qdrant_client , collection_name=self.config['collection_name']
            )
        storage_context = StorageContext.from_defaults(vector_store=qdrant_vector_store)
        service_context = ServiceContext.from_defaults(
                llm=llm, embed_model=embedder, chunk_size=self.config['chunk_size']
            )
        print(service_context)
        index = VectorStoreIndex.from_documents(
            documents_with_progress, storage_context=storage_context, service_context=service_context
        )
        #print(index)
        print(
            f"Data indexed successfully to Qdrant. Collection: {self.config['collection_name']}"
        )
        return index