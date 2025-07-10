from app.config import settings
from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError
from app.services.rag.pinecone_client import pinecone_client
from app.services.rag.document_processor import document_processor
from app.schemas.vector_store_schemas import (
    PineconeSearchResponse,
    PineconeError,
)
from app.services.rag.search_query_processor import search_query_processor

document_reference_router = FastMCP(name="Document Reference Request MCP")


@document_reference_router.tool
async def request_document_reference_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR DocumentReference resource.
    Rules:
        - When creating or updating a document reference, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting a document reference, ask the user for confirmation with details of the document and wait for the user's confirmation.
        - Provide links to the app (not api) document reference resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/DocumentReference", "/DocumentReference?patient=Patient/123")
        body: Optional JSON data for POST/PUT requests

    Returns:
        JSON response from the FHIR server

    """

    try:
        response = medplum_client.request(
            method=request.method,
            path=request.path,
            json=request.body,
        )
    except Exception as e:
        return FhirError(
            error_message=str(e),
            method=request.method,
            path=request.path,
            body=request.body,
        )

    return response


@document_reference_router.tool
async def add_document_to_pinecone(url: str, fhir_document_id: str) -> str | PineconeError:
    """
    IMPORTANT: Always inform the user at the beginning of your response that this search operation may take some time because the embedding model will be loaded into cache.
    Adds a document to the Pinecone vector index for the specified FHIR DocumentReference ID.

    This tool should be used to ingest new documents into the Pinecone index.

    Rules:
        - After adding the document, the Pinecone index may take up to 1 minute to update before the document is searchable.

    Args:
        url (str): The URL of the document to be added.
        fhir_document_id (str): The ID of the FHIR DocumentReference resource corresponding to the document.

    Returns:
        str: Confirmation message that the document was added or already exists.
        PineconeError: Error object with a message if the operation fails.
    """
    try:
        if not pinecone_client.check_if_document_exists(fhir_document_id=fhir_document_id):
            document_processor.process_document(url=url, fhir_document_id=fhir_document_id)
            return "Document added to Pinecone index"
        return "Document already exists in Pinecone index"
    except Exception as e:
        return PineconeError(error_message=str(e))


@document_reference_router.tool
async def search_pinecone(
    query: str, fhir_document_id: str, top_k: int = settings.TOP_K_RETRIEVAL_RESULTS
) -> list[PineconeSearchResponse] | PineconeError:
    """
    IMPORTANT: Always inform the user at the beginning of your response that this search operation may take some time because the embedding model will be loaded into cache.
    Searches the Pinecone vector index for information related to the given document by FHIR DocumentReference ID.

    Use this tool when the user requests information from the documents, notes, etc.

    Rules:
        - Firstly, prepare fhir_document_id by running the appropriate tool.
        - If the error message "Document does not exist in Pinecone index" is returned, automatically trigger the 'add_document_to_pinecone' tool to add the missing document to the index.
        - Translate the user's query into the language of the document before performing the search.
        - Base all answers strictly on the content found in the Pinecone index documents.
        - If the user's question is unrelated to the indexed documents, respond that the information is not available in the documents.
        - If the query is unclear or ambiguous, ask the user to clarify or provide more details.
        - You can modify the query to make it more specific and relevant to the document.

    Args:
        query (str): The user's search query.
        fhir_document_id (str): The ID of the FHIR DocumentReference resource to search within - it is the same as the FHIR ID of the document.
        top_k (int, optional): The maximum number of search results to return. Defaults to 10.

    Returns:
        list[PineconeSearchResponse]: List of search results matching the query.
        PineconeError: Error object with a message if the search fails.
    """
    try:
        if not pinecone_client.check_if_document_exists(fhir_document_id=fhir_document_id):
            return PineconeError(error_message="Document does not exist in Pinecone index")

        return search_query_processor.process_query(
            query=query, fhir_document_id=fhir_document_id, top_k=top_k
        )
    except Exception as e:
        return PineconeError(error_message=str(e))


# @document_reference_router.tool
# async def fetch_pdf(url: str) -> str:
#     """
#     Fetches a PDF file from the given URL and returns the text content.
#     """
#     response = requests.get(url)

#     response.raise_for_status()
#     pdf_file = BytesIO(response.content)
#     reader = PdfReader(pdf_file)

#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() or ""

#     return text


# @document_reference_router.tool
# async def check_if_pinecone_document_exists(
#     fhir_document_id: str,
# ) -> bool | PineconeError:
#     """
#     Checks if a document exists in the Pinecone index by FHIR DocumentReference ID.

#     Args:
#         fhir_document_id: ID of the FHIR DocumentReference resource

#     Returns:
#         True if the document exists, False otherwise
#     """
#     try:
#         return pinecone_client.check_if_document_exists(
#             fhir_document_id=fhir_document_id
#         )
#     except Exception as e:
#         return PineconeError(error_message=str(e))
