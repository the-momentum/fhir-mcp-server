import sys
from pinecone import Pinecone

from app.config import settings
from app.services.rag.utils import convert_pinecone_response_to_json
from app.services.rag.pinecone_initializer import create_index_if_not_exists
from app.schemas.vector_store_schemas import (
    PineconeSearchResponse,
    PineconeSearchRequest,
    PineconeUpsertRequest,
    PineconeError,
)
from app.services.rag.semantic_embedder import SemanticEmbedder


class PineconeClient:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.embedder = SemanticEmbedder(model_name=settings.EMBEDDING_MODEL)
        self.index = create_index_if_not_exists(
            pc=self.pc,
            index_name=settings.PINECONE_INDEX_NAME,
            dimension=settings.VECTOR_DIMENSION,
            metric=settings.EMBED_METRIC,
            cloud=settings.PINECONE_CLOUD,
            region=settings.PINECONE_REGION,
        )

    def upsert_vectors(
        self,
        upsert_request: PineconeUpsertRequest,
    ) -> None | PineconeError:
        try:
            self.index.upsert(
                namespace=upsert_request.namespace,
                vectors=[
                    (vector.id, vector.values, vector.metadata) for vector in upsert_request.vector
                ],
            )
            return None
        except Exception as e:
            return PineconeError(error_message=str(e))

    def search(
        self,
        embedded_query: PineconeSearchRequest,
        fhir_document_id: str,
        top_k: int = settings.TOP_K_RETRIEVAL_RESULTS,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> list[PineconeSearchResponse] | PineconeError:
        try:
            results = self.index.query(
                namespace=namespace,
                vector=embedded_query.embedded_query,
                top_k=top_k,
                filter={"fhir_document_id": fhir_document_id},
                include_metadata=True,
            )
            return convert_pinecone_response_to_json(results)
        except Exception as e:
            return PineconeError(error_message=str(e))

    def check_if_document_exists(
        self, fhir_document_id: str, namespace: str = settings.PINECONE_NAMESPACE
    ) -> bool | PineconeError:
        """
        Checks if a document exists in the Pinecone index.
        """
        try:
            fetched_vec = self.index.fetch(namespace=namespace, ids=[f"0-{fhir_document_id}"])

            return len(fetched_vec.vectors) > 0
        except Exception as e:
            return PineconeError(error_message=str(e))


try:
    pinecone_client: PineconeClient | None = PineconeClient()
except Exception as e:
    print(f"Error initializing Pinecone client: {e}", file=sys.stderr)
    pinecone_client = None
