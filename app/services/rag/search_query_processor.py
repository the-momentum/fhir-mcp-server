from app.config import settings
from app.schemas.vector_store_schemas import (
    PineconeError,
    PineconeSearchRequest,
    PineconeSearchResponse,
)
from app.services.rag.pinecone_client import pinecone_client


class SearchQueryProcessor:
    def process_query(
        self,
        query: str,
        fhir_document_id: str,
        top_k: int = settings.TOP_K_RETRIEVAL_RESULTS,
    ) -> list[PineconeSearchResponse] | PineconeError:
        if not pinecone_client:
            raise ValueError("Pinecone client is not initialized")
        embedded_query = pinecone_client.embedder.embed_texts(texts=[query]).vectors[0]
        return pinecone_client.search(
            embedded_query=PineconeSearchRequest(embedded_query=embedded_query),
            fhir_document_id=fhir_document_id,
            top_k=top_k,
        )


search_query_processor = SearchQueryProcessor()
