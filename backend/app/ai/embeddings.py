from app.core.config import settings

class EmbeddingsManager:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        return self._model

    def get_embedding(self, text: str):
        return self.model.encode(text).tolist()

    def get_embeddings(self, texts: list[str]):
        return self.model.encode(texts).tolist()

embeddings_manager = EmbeddingsManager()
