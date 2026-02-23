import faiss
import numpy as np
import logging
import os
from app.core.config import settings
from app.ai.chroma_client import chroma_client

class FaissIndexManager:
    def __init__(self):
        self.index = None
        self.index_path = settings.FAISS_INDEX_PATH
        self.doc_map = [] 
        self._initialized = False
        
    def _initialize(self):
        if self._initialized: return
        self._initialized = True
        self.load_or_rebuild()

    def get_index(self):
        if not self._initialized:
            self._initialize()
        return self.index
        
    def get_doc_map(self):
        if not self._initialized:
            self._initialize()
        return self.doc_map

    def load_or_rebuild(self):
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print(f"Loaded FAISS index from {self.index_path}. Fetching mapping...")
            except Exception as e:
                print(f"Failed to load FAISS index: {e}")
        self.rebuild()

    def rebuild(self):
        print("Rebuilding FAISS index from ChromaDB...")
        from app.ai.chroma_client import chroma_client
        data = chroma_client.get_all_data()
        
        if data is None or 'embeddings' not in data or data['embeddings'] is None or len(data['embeddings']) == 0:
            print("No data in ChromaDB to build FAISS index.")
            self.doc_map = []
            return

        embeddings = np.array(data['embeddings']).astype('float32')
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
            
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(embeddings)
        
        self.doc_map = []
        for i in range(len(data['ids'])):
            self.doc_map.append({
                "id": data['ids'][i],
                "document": data['documents'][i],
                "metadata": data['metadatas'][i]
            })
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        print(f"FAISS index and mapping for {len(self.doc_map)} docs rebuilt.")

    def search(self, query_vector: list, k: int = 3):
        idx = self.get_index()
        dmap = self.get_doc_map()
        if idx is None or not dmap:
            return []
            
        vector = np.array([query_vector]).astype('float32')
        distances, indices = idx.search(vector, k)
        
        results = []
        for i, idx_res in enumerate(indices[0]):
            if idx_res != -1 and idx_res < len(dmap):
                results.append(dmap[idx_res])
        return results

faiss_manager = FaissIndexManager()
