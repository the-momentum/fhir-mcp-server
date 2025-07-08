from app.config import settings
from app.services.rag.document_service import (
    download_pdf_bytes,
    bytes_to_text,
    chunk_text,
)
from app.services.rag.vector_store_service import upload_chunks


class DocumentProcessor:
    def process_pdf(
        self,
        url: str,
        fhir_document_id: str,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> None:
        pdf_bytes = download_pdf_bytes(url=url)
        text = bytes_to_text(bytes=pdf_bytes)
        chunks = chunk_text(text)
        upload_chunks(
            chunks=chunks,
            source_url=url,
            fhir_document_id=fhir_document_id,
            namespace=namespace,
        )


document_processor = DocumentProcessor()
