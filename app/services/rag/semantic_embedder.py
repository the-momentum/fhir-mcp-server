from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.schemas.vector_store_schemas import Embeddings


class SemanticEmbedder:
    def __init__(self, model_name: str):
        self.model = HuggingFaceEmbedding(model_name=model_name)

    def embed_texts(self, texts: list[str]) -> Embeddings:
        return Embeddings(vectors=self.model.get_text_embedding_batch(texts))
