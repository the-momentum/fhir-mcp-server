from fastmcp import FastMCP

from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError
from app.services.rag.pinecone_client import pinecone_client
from app.services.rag.document_manager import document_manager

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


@document_reference_router.tool
async def check_if_pinecone_document_exists(fhir_document_id: str) -> bool:
    """
    Checks if a document exists in the Pinecone index by FHIR DocumentReference ID.

    Args:
        fhir_document_id: ID of the FHIR DocumentReference resource

    Returns:
        True if the document exists, False otherwise
    """
    return pinecone_client.check_if_document_exists(fhir_document_id=fhir_document_id)


@document_reference_router.tool
async def search_pinecone(query: str, fhir_document_id: str, top_k: int = 10) -> list[dict]:
    """
    Searches the Pinecone index for the given query by FHIR DocumentReference ID.
    Use this tool to search the Pinecone index for the given query by FHIR DocumentReference ID.
    Rules:
        - First check if the document exists in the Pinecone index using the check_if_pinecone_document_exists tool.
        - If the document exists, use this tool to search the Pinecone index for the given query.
        - If the document does not exist, use the add_pdf_to_pinecone tool to add the PDF file to the Pinecone index.

    Args:
        query: Query to search for
        fhir_document_id: ID of the FHIR DocumentReference resource
        top_k: Number of results to return
    """
    return pinecone_client.search(query=query, fhir_document_id=fhir_document_id, top_k=top_k)


@document_reference_router.tool
async def add_pdf_to_pinecone(url: str, fhir_document_id: str):
    """
    Adds a PDF file to the Pinecone index.
    Use this tool to add a PDF file to the Pinecone index.
    Rules:
        - First check if the document exists in the Pinecone index using the check_if_pinecone_document_exists tool.
        - If the document does not exist, use this tool to add the PDF file to the Pinecone index, otherwise say that the document already exists.

    Args:
        url: URL of the PDF file
        fhir_document_id: ID of the FHIR DocumentReference resource
    """
    document_manager.process_pdf(url=url, fhir_document_id=fhir_document_id)
