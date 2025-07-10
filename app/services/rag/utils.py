import hashlib
from app.schemas.vector_store_schemas import PineconeSearchResponse


def convert_pinecone_response_to_json(
    pinecone_response,
) -> list[PineconeSearchResponse]:
    matches = pinecone_response.get("matches", [])
    converted = []
    for match in matches:
        converted.append(
            PineconeSearchResponse(
                chunk_text=match.get("metadata", {}).get("chunk_text"),
                chunk_index=match.get("metadata", {}).get("chunk_index"),
                fhir_document_id=match.get("metadata", {}).get("fhir_document_id"),
                source_url=match.get("metadata", {}).get("source_url"),
                score=match.get("score"),
            )
        )
    return converted


def generate_id(source_url: str) -> str:
    return hashlib.md5(source_url.encode()).hexdigest()
