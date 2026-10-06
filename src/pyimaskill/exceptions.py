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
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class ImaAuthError(ImaError):
    pass


class ImaNotFoundError(ImaError):
    pass


class ImaRateLimitError(ImaError):
    pass


class ImaPermissionError(ImaError):
    pass


class ImaValidationError(ImaError):
    pass


class ImaServerError(ImaError):
    pass


_ERROR_MAP: Dict[int, Type[ImaError]] = {
    20004: ImaAuthError,
    210002: ImaAuthError,
    210006: ImaNotFoundError,
    210035: ImaNotFoundError,
    210012: ImaNotFoundError,
    20002: ImaRateLimitError,
    110021: ImaRateLimitError,
    210005: ImaPermissionError,
    210034: ImaPermissionError,
    210011: ImaPermissionError,
    110030: ImaPermissionError,
    210001: ImaValidationError,
    210004: ImaValidationError,
    210009: ImaValidationError,
    210030: ImaValidationError,
    210031: ImaValidationError,
    110001: ImaValidationError,
    110002: ImaValidationError,
    210003: ImaServerError,
    210007: ImaServerError,
    210008: ImaServerError,
    210032: ImaServerError,
    210033: ImaServerError,
    210036: ImaServerError,
    110010: ImaServerError,
    110011: ImaServerError,
    110012: ImaServerError,
    110013: ImaServerError,
    110020: ImaServerError,
}


def raise_for_retcode(code: int, msg: str) -> None:
    if code == 0:
        return
    exc_class = _ERROR_MAP.get(code, ImaError)
    raise exc_class(code, msg)
