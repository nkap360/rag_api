### Loading the embedder

from llama_index.core import VectorStoreIndex,ServiceContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import qdrant_client


class FileSearcher:
    def __init__(self, config, llm):
        self.config = config
        self.llm = llm  # ollama llm
        self.qdrant_client = qdrant_client.QdrantClient(
            url=self.config['qdrant_local'],
            timeout=self.config["qdrant_timeout"]
        )
        self.embedder = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=self.config["embedding"])
        )
    

    def qdrant_index(self):
        # Create a QdrantVectorStore
        qdrant_vector_store = QdrantVectorStore(
            client=self.qdrant_client, collection_name=self.config['collection_name']
        )
        # Create a ServiceContext
        service_context = ServiceContext.from_defaults(
            llm=self.llm, embed_model=self.embedder, chunk_size=self.config["chunk_size"]
        )
        # Create a VectorStoreIndex
        index = VectorStoreIndex.from_vector_store(
            vector_store=qdrant_vector_store, service_context=service_context
        )
        return index
