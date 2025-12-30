import faiss
import numpy as np
import os
from worker.settings import settings
from worker.chroma_client import chroma_client

class FaissIndexManager:
    def __init__(self):
        self.index = None
        self.index_path = settings.FAISS_INDEX_PATH
        self.doc_map = [] # Mapping of index to {id, document, metadata}
        self.load_or_rebuild()

    def load_or_rebuild(self):
        # We always rebuild if doc_map is empty because we need the mapping
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                # We still need the doc_map from Chroma to associate indices with text
                print(f"Loaded FAISS index from {self.index_path}. Fetching mapping...")
            except Exception as e:
                print(f"Failed to load FAISS index: {e}")
        
        self.rebuild()

    def rebuild(self):
        print("Rebuilding FAISS index from ChromaDB...")
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
        
        # Store mapping
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
        if self.index is None or not self.doc_map:
            return []
            
        vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(vector, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.doc_map):
                results.append(self.doc_map[idx])
        return results

faiss_manager = FaissIndexManager()
