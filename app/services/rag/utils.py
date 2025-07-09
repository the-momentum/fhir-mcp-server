import hashlib
from app.schemas.vector_store_schemas import PineconeSearchResponse


def convert_pinecone_response_to_json(
    pinecone_response,
) -> list[PineconeSearchResponse]:
    hits = pinecone_response.get("result", {}).get("hits", [])
    converted = []
    for hit in hits:
        converted.append(
            PineconeSearchResponse(
                fhir_document_id=hit.get("fhir_document_id"),
                score=hit.get("_score"),
                chunk_text=hit.get("fields", {}).get("chunk_text"),
            )
        )
    return converted


def generate_id(source_url: str) -> str:
    return hashlib.md5(source_url.encode()).hexdigest()
