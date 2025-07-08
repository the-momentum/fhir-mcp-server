import hashlib


def convert_pinecone_response_to_json(pinecone_response) -> list[dict]:
    hits = pinecone_response.get("result", {}).get("hits", [])
    converted = []
    for hit in hits:
        converted.append(
            {
                "id": hit.get("_id"),
                "score": hit.get("_score"),
                "category": (hit["fields"].get("category") if "fields" in hit else None),
                "chunk_text": (hit["fields"].get("chunk_text") if "fields" in hit else None),
            }
        )
    return converted


def generate_id(source_url: str) -> str:
    return hashlib.md5(source_url.encode()).hexdigest()
