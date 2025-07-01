from requests import PreparedRequest
from requests.auth import AuthBase


class BearerAuth(AuthBase):
    """Attaches HTTP Bearer Authentication to the given Request object."""

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r