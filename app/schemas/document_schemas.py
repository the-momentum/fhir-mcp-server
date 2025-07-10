from typing import Literal
from pydantic import BaseModel

type DocumentFormat = Literal["pdf", "txt", "csv", "json"]


class Document(BaseModel):
    url: str
    fhir_document_id: str
    format: DocumentFormat | None = None
