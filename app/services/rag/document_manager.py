import requests
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings
from app.services.rag.pinecone_client import pinecone_client


class DocumentManager:
    def __init__(self):
        self.pinecone_client = pinecone_client
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

    def download_pdf_bytes(self, url: str) -> bytes:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def bytes_to_text(self, bytes: bytes) -> str:
        doc = fitz.open(stream=bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def chunk_text(self, text: str) -> list[str]:
        return self.text_splitter.split_text(text)

    def prepare_and_upload(
        self,
        chunks: list[str],
        source_url: str,
        fhir_document_id: str,
        batch_size: int = 96,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> None:
        vectors = []

        for i, chunk in enumerate(chunks):
            record = {
                "id": f"{i}-{fhir_document_id}",
                "chunk_text": chunk,
                "source_url": source_url,
                "chunk_index": i,
                "fhir_document_id": fhir_document_id,
            }
            vectors.append(record)

            if len(vectors) >= batch_size:
                self.pinecone_client.upsert(vectors=vectors, namespace=namespace)
                vectors = []

        if vectors:
            self.pinecone_client.upsert(vectors=vectors, namespace=namespace)

    def process_pdf(
        self,
        url: str,
        fhir_document_id: str,
        namespace: str = settings.PINECONE_NAMESPACE,
    ) -> None:
        pdf_bytes = self.download_pdf_bytes(url=url)
        text = self.bytes_to_text(bytes=pdf_bytes)
        chunks = self.chunk_text(text)
        self.prepare_and_upload(
            chunks=chunks,
            source_url=url,
            fhir_document_id=fhir_document_id,
            namespace=namespace,
        )


document_manager = DocumentManager()
