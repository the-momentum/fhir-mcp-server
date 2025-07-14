from app.config import settings
from app.services.rag.pinecone_client import pinecone_client
from app.schemas.vector_store_schemas import PineconeUpsertRequest, Embeddings, Vector


def get_chunks_embeddings(chunks: list[str]) -> Embeddings:
    if not pinecone_client:
        raise ValueError("Pinecone client is not initialized")
    return pinecone_client.embedder.embed_texts(texts=chunks)


def upload_embeddings(
    embeddings: Embeddings,
    chunks: list[str],
    source_url: str,
    fhir_document_id: str,
    batch_size: int = settings.EMBED_BATCH_SIZE,
    namespace: str = settings.PINECONE_NAMESPACE,
) -> None:
    vectors = []
    if not pinecone_client:
        raise ValueError("Pinecone client is not initialized")

    for i, (embedding, chunk) in enumerate(zip(embeddings.vectors, chunks)):
        vectors.append(
            Vector(
                id=f"{i}-{fhir_document_id}",
                values=embedding,
                metadata={
                    "chunk_text": chunk,
                    "source_url": source_url,
                    "chunk_index": i,
                    "fhir_document_id": fhir_document_id,
                },
            )
        )

        if len(vectors) >= batch_size:
            pinecone_client.upsert_vectors(
                upsert_request=PineconeUpsertRequest(vector=vectors, namespace=namespace)
            )
            vectors = []

    if vectors:
        pinecone_client.upsert_vectors(
            upsert_request=PineconeUpsertRequest(vector=vectors, namespace=namespace)
        )
