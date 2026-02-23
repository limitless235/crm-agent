from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingsManager:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def get_embedding(self, text: str):
        return self.model.encode(text).tolist()

    def get_embeddings(self, texts: list[str]):
        return self.model.encode(texts).tolist()

embeddings_manager = EmbeddingsManager()
