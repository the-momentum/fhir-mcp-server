import requests
import chardet
import io
import csv
import json
import fitz

from functools import lru_cache
from llama_index.core.node_parser import SemanticSplitterNodeParser
from app.services.rag.pinecone_client import pinecone_client
from llama_index.core.schema import Document


@lru_cache(maxsize=1)
def get_text_splitter() -> SemanticSplitterNodeParser:
    return SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=95,
        embed_model=pinecone_client.embedder.model,
    )


def download_bytes(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def detect_encoding(byte_data: bytes) -> str:
    result = chardet.detect(byte_data)
    return result["encoding"] or "utf-8"


def bytes_to_text(file_bytes: bytes, filetype: str | None = None) -> str:
    if filetype == "pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join([page.get_text() for page in doc])

    elif filetype == "txt":
        encoding = detect_encoding(file_bytes)
        return file_bytes.decode(encoding)

    elif filetype == "csv":
        encoding = detect_encoding(file_bytes)
        f = io.StringIO(file_bytes.decode(encoding))
        reader = csv.reader(f)
        return "\n".join([", ".join(row) for row in reader])

    elif filetype == "json":
        encoding = detect_encoding(file_bytes)
        data = json.loads(file_bytes.decode(encoding))
        return json.dumps(data, indent=2, ensure_ascii=False)

    raise ValueError("Filetype is required")


def chunk_text(text: str) -> list[str]:
    text_splitter = get_text_splitter()
    nodes = text_splitter.get_nodes_from_documents([Document(text=text)])
    return [node.get_content() for node in nodes]
