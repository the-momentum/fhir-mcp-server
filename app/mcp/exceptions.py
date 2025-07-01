from typing import Any, LiteralString, Sequence

from fastapi import status
from pydantic import BaseModel, field_serializer

from app.schemas.error_codes import ErrorCode

Loc = tuple[int | str, ...] | None


class APICustomError(Exception):
    def __init__(
        self,
        status: int,
        code: LiteralString,
        message: str,
        ctx: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.code = code
        self.message = message
        self.ctx = ctx


class APIErrorDetail(BaseModel):
    code: str | None = None
    message: str
    path: list[str | int]
    ctx: dict[str, Any] | None = None

    @field_serializer("path")
    def rewrite_body_path(self, path: list[str | int], _info) -> list[str | int]:
        if path == ["body"]:
            return ["_base"]

        return path


class APIError(BaseModel):
    code: ErrorCode
    details: list[APIErrorDetail]


class APIErrorResponse(BaseModel):
    error: APIError


class APIValidationError(APICustomError):
    def __init__(
        self,
        code: LiteralString,
        message: str,
        ctx: dict[str, Any] | None = None,
        loc: Loc = None,
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.loc = loc

        super().__init__(status, code, message, ctx)


class APIMultiValidationError(Exception):
    def __init__(
        self,
        errors: Sequence[APIValidationError],
        status: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.status = status
        self.errors = errors

        super().__init__(errors, self.status)
