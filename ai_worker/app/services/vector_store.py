import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from app.core.config import settings

class VectorStoreService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST, 
            port=settings.CHROMA_PORT
        )
        self.collection = self.chroma_client.get_or_create_collection(name="knowledge_base")
        self.faiss_index = None
        self.metadata_map = {} # Maps FAISS index to Chroma IDs

    def _get_embedding(self, text: str):
        return self.model.encode(text).tolist()

    def add_documents(self, documents: list, metadatas: list, ids: list):
        embeddings = self.model.encode(documents).tolist()
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        # Invalidate FAISS index to trigger rebuild
        self.faiss_index = None

    def query(self, text: str, n_results: int = 5):
        # Always use Chroma as source of truth for the final results
        # but can use FAISS for the heavy lifting if the index is built.
        query_embedding = self._get_embedding(text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    def trigger_rebuild_faiss(self):
        """Manual trigger to rebuild FAISS from ChromaDB source of truth."""
        print("Triggering FAISS rebuild...")
        self.export_to_faiss()

    def export_to_faiss(self, path: str = "data/faiss_index"):
        # Rebuild FAISS index from ChromaDB data
        all_data = self.collection.get(include=['embeddings', 'metadatas', 'documents'])
        if not all_data or not all_data.get('embeddings') or len(all_data['embeddings']) == 0:
            print("No data in ChromaDB to export to FAISS.")
            return

        embeddings = np.array(all_data['embeddings']).astype('float32')
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
            
        d = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(d)
        self.faiss_index.add(embeddings)
        
        # Save FAISS index
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        faiss.write_index(self.faiss_index, path)
        print(f"FAISS index exported to {path}")

vector_service = VectorStoreService()
