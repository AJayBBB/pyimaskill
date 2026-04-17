"""Custom exceptions for IMA OpenAPI errors."""

from __future__ import annotations

from typing import Dict, Type

__all__ = [
    "ImaAuthError",
    "ImaError",
    "ImaNotFoundError",
    "ImaPermissionError",
    "ImaRateLimitError",
    "ImaServerError",
    "ImaValidationError",
]


class ImaError(Exception):
    """Base exception for all IMA API errors."""

    def __init__(self, retcode: int, errmsg: str) -> None:
        self.retcode = retcode
        self.errmsg = errmsg
        super().__init__(f"[{retcode}] {errmsg}")


class ImaAuthError(ImaError):
    """Authentication failed — invalid or expired credentials."""


class ImaNotFoundError(ImaError):
    """Resource not found — note deleted, notebook doesn't exist, etc."""


class ImaRateLimitError(ImaError):
    """Rate limit exceeded — API key frequency limit reached."""


class ImaPermissionError(ImaError):
    """Permission denied — not the note author or no access."""


class ImaValidationError(ImaError):
    """Validation error — invalid parameters or size limits."""


class ImaServerError(ImaError):
    """Server error — internal server error or downstream failure."""


# Error code mapping
_ERROR_MAP: Dict[int, Type[ImaError]] = {
    # Auth errors
    20004: ImaAuthError,
    100002: ImaAuthError,
    # Not found
    100006: ImaNotFoundError,
    310001: ImaNotFoundError,
    # Rate limit
    20002: ImaRateLimitError,
    110021: ImaRateLimitError,
    # Permission
    100005: ImaPermissionError,
    110030: ImaPermissionError,
    # Validation
    100001: ImaValidationError,
    100004: ImaValidationError,
    100009: ImaValidationError,
    110001: ImaValidationError,
    110002: ImaValidationError,
    # Server errors
    100003: ImaServerError,
    110010: ImaServerError,
    110011: ImaServerError,
    110012: ImaServerError,
    110013: ImaServerError,
    110020: ImaServerError,
}


def raise_for_retcode(retcode: int, errmsg: str) -> None:
    """Raise appropriate exception based on retcode.

    Args:
        retcode: API return code (0 = success).
        errmsg: Error message from API.

    Raises:
        ImaError: Subclass matching the error code.
    """
    if retcode == 0:
        return
    exc_class = _ERROR_MAP.get(retcode, ImaError)
    raise exc_class(retcode, errmsg)
