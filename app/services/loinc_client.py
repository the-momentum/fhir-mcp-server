import requests
from requests.auth import HTTPBasicAuth

from app.config import settings


class LoincClient:
    def __init__(self):
        self.base_url = settings.LOINC_ENDPOINT
        self.auth = HTTPBasicAuth(
            settings.LOINC_USERNAME, settings.LOINC_PASSWORD.get_secret_value()
        )
        self.code_record_url = f"{self.base_url}?query="

    def _get_loinc_code(
        self,
        component_name: str,
        max_codes: int = 5,
        max_fetch: int = 50,
        sort_order: str = "common_test_rank asc",  # lower rank = more common
    ) -> list[dict]:
        url = self.code_record_url + component_name
        params = {
            "query": str(component_name),
            "rows": str(max_fetch),
            "sortorder": str(sort_order),
        }
        try:
            response = requests.get(
                url, auth=self.auth, params=params, timeout=settings.LOINC_TIMEOUT
            )
            data = response.json()
        except requests.exceptions.RequestException as e:
            return [{"Error": f"Request failed: {str(e)}"}]
        except ValueError as e:
            return [{"Error": f"Invalid JSON response: {str(e)}"}]

        records_found = data.get("ResponseSummary", {}).get("RecordsFound", 0)

        if records_found == 0:
            return [{"RecordsFound": 0, "Error": "No LOINC codes found"}]

        # get only active codes
        active_codes = []

        if "Results" in data and data["Results"]:
            active_codes = [item for item in data["Results"] if item.get("STATUS") == "ACTIVE"]

        # No active codes found
        if not active_codes:
            return [
                {
                    "AllRecordsFound": records_found,
                    "Error": "No active LOINC codes found in current fetch",
                }
            ]

        return active_codes[:max_codes]

    def get_common_loinc_codes(
        self, component_name: str, max_codes: int = 5, max_fetch: int = 50
    ) -> list[dict]:
        return self._get_loinc_code(
            component_name, max_codes, max_fetch, sort_order="common_test_rank asc"
        )


loinc_client = LoincClient()
