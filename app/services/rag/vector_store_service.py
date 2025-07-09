from app.config import settings
from app.services.rag.pinecone_client import pinecone_client
from app.schemas.vector_store_schemas import PineconeUpsertRequest


def upload_chunks(
    chunks: list[str],
    source_url: str,
    fhir_document_id: str,
    batch_size: int = settings.PINECONE_BATCH_SIZE,
    namespace: str = settings.PINECONE_NAMESPACE,
) -> None:
    vectors = []
    for i, chunk in enumerate(chunks):
        vectors.append(
            {
                "id": f"{i}-{fhir_document_id}",
                "chunk_text": chunk,
                "source_url": source_url,
                "chunk_index": i,
                "fhir_document_id": fhir_document_id,
            }
        )

        if len(vectors) >= batch_size:
            pinecone_client.upsert(
                upsert_request=PineconeUpsertRequest(vectors=vectors, namespace=namespace)
            )
            vectors = []

    if vectors:
        pinecone_client.upsert(
            upsert_request=PineconeUpsertRequest(vectors=vectors, namespace=namespace)
        )
