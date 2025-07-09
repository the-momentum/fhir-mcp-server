from app.services.rag.pinecone_client import pinecone_client
from app.schemas.vector_store_schemas import (
    PineconeSearchResponse,
    PineconeSearchRequest,
    PineconeError,
)


class SearchQueryProcessor:
    def process_query(
        self, query: str, fhir_document_id: str, top_k: int = 10
    ) -> list[PineconeSearchResponse] | PineconeError:
        embedded_query = pinecone_client.embedder.embed_texts(texts=[query]).vectors[0]
        return pinecone_client.search(
            embedded_query=PineconeSearchRequest(embedded_query=embedded_query),
            fhir_document_id=fhir_document_id,
            top_k=top_k,
        )


search_query_processor = SearchQueryProcessor()
