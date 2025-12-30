import chromadb
import time
from worker.settings import settings
from worker.embeddings import embeddings_manager

class ChromaClient:
    def __init__(self):
        max_retries = 15
        retry_interval = 2
        
        self.client = None
        self.collection = None
        
        for i in range(max_retries):
            try:
                self.client = chromadb.HttpClient(
                    host=settings.CHROMA_HOST, 
                    port=settings.CHROMA_PORT
                )
                # Test connection by fetching identity or collection
                self.collection = self.client.get_or_create_collection(
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

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        embeddings = embeddings_manager.get_embeddings(documents)
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, text: str, n_results: int = 5):
        query_embedding = embeddings_manager.get_embedding(text)
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_all_data(self):
        return self.collection.get(include=['embeddings', 'metadatas', 'documents'])

chroma_client = ChromaClient()
