import requests
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)


def download_pdf_bytes(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def bytes_to_text(bytes: bytes) -> str:
    doc = fitz.open(stream=bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()  # type: ignore
    doc.close()
    return text


def chunk_text(text: str) -> list[str]:
    return text_splitter.split_text(text)
