import requests
import fitz
from llama_index.core.node_parser import SemanticSplitterNodeParser
from app.services.rag.pinecone_client import pinecone_client
from llama_index.core.schema import Document


text_splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=95,
    embed_model=pinecone_client.embedder.model,
)


def download_pdf_bytes(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def bytes_to_text(bytes: bytes) -> str:
    doc = fitz.open(stream=bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text: str) -> list[str]:
    nodes = text_splitter.get_nodes_from_documents([Document(text=text)])
    return [node.get_content() for node in nodes]
