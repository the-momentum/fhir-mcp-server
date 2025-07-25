from app.config import settings
from app.schemas.document_schemas import Document
from app.services.rag.document_service import (
    bytes_to_text,
    chunk_text,
    download_bytes,
)
from app.services.rag.vector_store_service import (
    get_chunks_embeddings,
    upload_embeddings,
)


class DocumentProcessor:
    def process_document(
        self,
        document: Document,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> None:
        pdf_bytes = download_bytes(url=document.url)
        text = bytes_to_text(file_bytes=pdf_bytes, filetype=document.format)
        chunks = chunk_text(text)
        embeddings = get_chunks_embeddings(chunks)

        upload_embeddings(
            embeddings=embeddings,
            chunks=chunks,
            source_url=document.url,
            fhir_document_id=document.fhir_document_id,
            namespace=namespace,
        )


document_processor = DocumentProcessor()
