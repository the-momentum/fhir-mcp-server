from typing import Any
from pydantic import BaseModel


class PineconeSearchResponse(BaseModel):
    chunk_text: str | None = None
    chunk_index: int | None = None
    fhir_document_id: str | None = None
    source_url: str | None = None
    score: float | None = None


class PineconeSearchRequest(BaseModel):
    embedded_query: list[float]


class Vector(BaseModel):
    id: str
    values: list[float]
    metadata: dict[str, Any]


class PineconeUpsertRequest(BaseModel):
    vector: list[Vector]
    namespace: str


class Embeddings(BaseModel):
    vectors: list[list[float]]


class PineconeError(BaseModel):
    error_message: str
