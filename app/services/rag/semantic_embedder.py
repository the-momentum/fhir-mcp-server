from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from app.schemas.vector_store_schemas import Embeddings


class SemanticEmbedder:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._model: HuggingFaceEmbedding | None = None

    # Lazy loading of the model
    @property
    def model(self) -> HuggingFaceEmbedding:
        if self._model is None:
            self._model = HuggingFaceEmbedding(model_name=self.model_name)
        return self._model

    def embed_texts(self, texts: list[str]) -> Embeddings:
        return Embeddings(vectors=self.model.get_text_embedding_batch(texts))
