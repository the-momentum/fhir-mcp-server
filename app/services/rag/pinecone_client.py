from pinecone import Pinecone
from app.config import settings
from app.services.rag.utils import convert_pinecone_response_to_json
from app.services.rag.pinecone_initializer import create_index_if_not_exists


class PineconeClient:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY.get_secret_value())
        self.index = create_index_if_not_exists(
            pc=self.pc,
            index_name=settings.PINECONE_INDEX_NAME,
            embed_model=settings.EMBEDDING_MODEL,
            dimension=settings.PINECONE_DIMENSION,
            metric=settings.PINECONE_METRIC,
            cloud=settings.PINECONE_CLOUD,
            region=settings.PINECONE_REGION,
            field_map={"text": "chunk_text"},
        )

    def upsert(self, vectors: list[dict], namespace: str = settings.PINECONE_NAMESPACE):
        self.index.upsert_records(namespace=namespace, records=vectors)

    def search(
        self,
        query: str,
        fhir_document_id: str,
        top_k: int = 10,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> list[dict]:
        results = self.index.search(
            namespace=namespace,
            query={
                "top_k": top_k,
                "inputs": {"text": query},
                "filter": {"fhir_document_id": fhir_document_id},
            },  # type: ignore
        )

        return convert_pinecone_response_to_json(results)

    def check_if_document_exists(
        self, fhir_document_id: str, namespace: str = settings.PINECONE_NAMESPACE
    ) -> bool:
        """
        Checks if a document exists in the Pinecone index.
        """
        fetched_vec = self.index.fetch(namespace=namespace, ids=[f"0-{fhir_document_id}"])

        return len(fetched_vec.vectors) > 0


pinecone_client = PineconeClient()
