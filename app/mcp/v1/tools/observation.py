from fastmcp import FastMCP

from app.config import settings
from app.services.medplum.medplum_client import medplum_client
from app.schemas.fhir_schemas import FhirQueryResponse, FhirQueryRequest, FhirError
from app.services.loinc_client import loinc_client


observation_router = FastMCP(name="Observation Request MCP")


@observation_router.tool
async def get_loinc_codes(
    component_name: str,
    max_codes: int = settings.LOINC_MAX_CODES,
    max_fetch: int = settings.LOINC_MAX_FETCH,
) -> list[dict]:
    """
    Get the most relevant LOINC codes for a given observation name.

    The function automatically:
    - Filters for STATUS="ACTIVE" codes only
    - Sorts by COMMON_TEST_RANK (lower rank = more commonly used)
    - Returns codes in popularity order (most common first)

    Your job is to:
    1. Analyze returned codes for semantic relevance to the search query
    2. Balance clinical popularity with semantic matching
    3. Select codes that best match the intended observation

    Strategy:
    1. Start with default parameters (max_codes=5, max_fetch=50)
    2. Check if result contains "Error" key in first element
    3. If "Authentication failed" or "Authorization" error:
        - STOP using this tool immediately.
        - Do not retry with different parameters.
        - Report the authentication error to the user.
        - Suggest they check their LOINC API credentials.
        - Ask the user if they want to use your knowledge to find a LOINC code and wait for the confirmation.
          Add warning that this may cause wrong results.
    3. If "No active LOINC codes found in current fetch":
        - Increase max_fetch progressively (50→100→200→RecordsFound).
        - Keep trying until max_fetch >= RecordsFound or you find active codes.
    4. If "No LOINC codes found": Try alternative search terms or report failure.
    5. If you get codes but they don't semantically match your query:
        - Increase max_codes to see more options.
        - Look for better matches in COMPONENT, SHORTNAME, LONG_COMMON_NAME fields.

    Rules:
    - Function returns codes sorted by popularity - YOU decide which are most relevant.
    - Don't automatically pick the first (most common) codes.
    - Prioritize semantic relevance: exact matches in COMPONENT > SHORTNAME > partial matches.
    - Balance popularity with relevance (very rare codes might not be clinically useful).
    - Keep increasing max_fetch until you exhaust all available records (max_fetch >= RecordsFound).
    - Increase max_codes only when you need more options to find better semantic matches.

    Args:
        component_name: The name of the observation to get the LOINC code for (i.e. "glucose").
        max_codes: The maximum number of LOINC codes to return.
        max_fetch: The maximum number of LOINC codes to fetch from the API.
    Returns:
        LOINC codes sorted by popularity - you must select the most semantically relevant ones.
    """

    return loinc_client.get_common_loinc_codes(
        component_name, max_codes=max_codes, max_fetch=max_fetch
    )


@observation_router.tool
async def request_observation_resource(
    request: FhirQueryRequest,
) -> FhirQueryResponse | FhirError:
    """
    Makes an HTTP request to the FHIR server.
    Use this tool to perform CRUD operations only on the FHIR Observation resource.

    IMPORTANT: Before fetching observations that require LOINC codes:
    1. First use get_loinc_code() tool to find appropriate LOINC codes
    2. Then use this tool to fetch the observation with the LOINC code

    Rules:
        - When creating or updating an observation, use only the data explicitly provided by the user.
        - Do not guess, auto-fill, or assume any missing data.
        - When deleting an observation, ask the user for confirmation with details of the observation and wait for the user's confirmation.
        - Provide links to the app (not api) observation resource in the final response.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: Resource path (e.g., "/Observation?subject:Patient.name=Homer%20Simpson")
        body: Optional JSON data for POST/PUT requests)

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
