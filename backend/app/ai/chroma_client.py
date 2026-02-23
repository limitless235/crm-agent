import chromadb
from chromadb.config import Settings
from app.core.config import settings
from app.ai.embeddings import embeddings_manager

import time

class ChromaClient:
    def __init__(self):
        self._client = None
        self._collection = None
        self._initialized = False

    def _initialize(self):
        if self._initialized: return
        self._initialized = True
        max_retries = 15
        retry_interval = 2
        
        for i in range(max_retries):
            try:
                self._client = chromadb.HttpClient(
                    host=settings.CHROMA_HOST, 
                    port=settings.CHROMA_PORT
                )
                self._collection = self._client.get_or_create_collection(
                    name=settings.CHROMA_COLLECTION_NAME
                )
                print(f"Connected to Chroma successfully.")
                break
            except Exception as e:
                if i == max_retries - 1:
                    print(f"FAILED to connect to Chroma after {max_retries} attempts.")
                    raise e
                print(f"Chroma not ready (attempt {i+1}/{max_retries}). Retrying in {retry_interval}s...")
                time.sleep(retry_interval)

    @property
    def collection(self):
        if not self._initialized:
            self._initialize()
        return self._collection

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        if not self.collection: return
        from app.ai.embeddings import embeddings_manager
        embeddings = embeddings_manager.get_embeddings(documents)
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, text: str, n_results: int = 5):
        if not self.collection: return []
        from app.ai.embeddings import embeddings_manager
        query_embedding = embeddings_manager.get_embedding(text)
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_all_data(self):
        if not self.collection: return None
        return self.collection.get(include=['embeddings', 'metadatas', 'documents'])

chroma_client = ChromaClient()
