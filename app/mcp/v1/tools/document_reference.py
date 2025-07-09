from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError
from app.services.rag.pinecone_client import pinecone_client
from app.services.rag.document_processor import document_processor
from app.schemas.vector_store_schemas import (
    PineconeSearchResponse,
    PineconeSearchRequest,
    PineconeError,
)

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


@document_reference_router.tool
async def search_pinecone(
    query: PineconeSearchRequest, fhir_document_id: str, top_k: int = 10
) -> list[PineconeSearchResponse] | PineconeError:
    """
    Searches the Pinecone index for the given query by FHIR DocumentReference ID.
    Use this tool when the user asks for information from the documents.
    Rules:
        - if the error says "Document does not exist in Pinecone index", use appropriate tool to add the PDF file to the Pinecone index.

    Args:
        query: Query to search for
        fhir_document_id: ID of the FHIR DocumentReference resource
        top_k: Number of results to return

    Returns:
        List of PineconeSearchResponse objects
    """
    try:
        if not pinecone_client.check_if_document_exists(fhir_document_id=fhir_document_id):
            return PineconeError(error_message="Document does not exist in Pinecone index")
        return pinecone_client.search(
            query=query,
            fhir_document_id=fhir_document_id,
            top_k=top_k,
        )
    except Exception as e:
        return PineconeError(error_message=str(e))


@document_reference_router.tool
async def add_pdf_to_pinecone(url: str, fhir_document_id: str) -> bool | PineconeError:
    """
    Adds a PDF file to the Pinecone index.
    Use this tool to add a PDF file to the Pinecone index.

    Args:
        url: URL of the PDF file
        fhir_document_id: ID of the FHIR DocumentReference resource

    Returns:
        True if the PDF file is added to the Pinecone index, False if the document already exists
    """
    try:
        if not pinecone_client.check_if_document_exists(fhir_document_id=fhir_document_id):
            document_processor.process_pdf(url=url, fhir_document_id=fhir_document_id)
            return True
        return False
    except Exception as e:
        return PineconeError(error_message=str(e))
