from pydantic import BaseModel


class PineconeSearchResponse(BaseModel):
    fhir_document_id: str | None = None
    score: float | None = None
    chunk_text: str | None = None


class PineconeSearchRequest(BaseModel):
    query: str


class PineconeUpsertRequest(BaseModel):
    vectors: list[dict]
    namespace: str


class PineconeError(BaseModel):
    error_message: str
