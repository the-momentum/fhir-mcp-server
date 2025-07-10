import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

dotenv_path = "config/.env"

load_dotenv(dotenv_path)

embedding_model_name = os.getenv("EMBEDDING_MODEL")

if not embedding_model_name:
    embedding_model_name = "NeuML/pubmedbert-base-embeddings"

model = HuggingFaceEmbedding(model_name=embedding_model_name)
