from __future__ import annotations

import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
__all__ = ["Config", "load_config"]

_DEFAULT_BASE_URL = "https://ima.qq.com"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_EXPIRY_WARNING_WINDOW = 24 * 60 * 60
SKILL_VERSION = "1.1.3"


@dataclass(frozen=True)
class Config:
    client_id: str
    api_key: str
    api_key_expires_at: datetime | None = None
    base_url: str = _DEFAULT_BASE_URL
    timeout: float = _DEFAULT_TIMEOUT
    expiry_warning_window: int = _DEFAULT_EXPIRY_WARNING_WINDOW

    def __post_init__(self) -> None:
        if not self.client_id or not self.api_key:
            raise ValueError("client_id and api_key are required")

        if self.expiry_warning_window < 0:
            raise ValueError("expiry_warning_window must be >= 0")

    def build_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "ima-openapi-ctx": f"skill_version={SKILL_VERSION}",
        }

    def validate_credentials(self, *, now: datetime | None = None) -> list[str]:
        current_time = now or datetime.now(timezone.utc)
        warnings_list: list[str] = []

        if self.api_key_expires_at and current_time >= self.api_key_expires_at:
            raise ValueError(
                "api_key expired. "
                f"Expiry time: {self._format_dt(self.api_key_expires_at)}"
            )

        expiry_warning = self._build_expiry_warning(
            expires_at=self.api_key_expires_at,
            now=current_time,
        )
        if expiry_warning:
            warnings_list.append(expiry_warning)

        return warnings_list

    def emit_runtime_warnings(self) -> None:
        for message in self.validate_credentials():
            warnings.warn(message, stacklevel=2)

    def _build_expiry_warning(
        self,
        *,
        expires_at: datetime | None,
        now: datetime,
    ) -> str | None:
        if expires_at is None:
            return None

        remaining = (expires_at - now).total_seconds()
        if remaining < 0 or remaining > self.expiry_warning_window:
            return None

        return f"api_key expires in {int(remaining / 3600)} hours"

    @staticmethod
    def _format_dt(value: datetime | None) -> str:
        if value is None:
            return "unknown"
        return value.astimezone(timezone.utc).isoformat()


def _parse_datetime(value: str | datetime | None) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if not value:
        return None

    text = value.strip()
    if not text:
        return None

    if text.isdigit():
        return datetime.fromtimestamp(int(text), tz=timezone.utc)

    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            "Invalid api_key expiry time. Use ISO8601 or unix timestamp, "
            f"got: {value!r}"
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def load_config(
    client_id: str,
    api_key: str,
    api_key_expires_at: str | datetime | None = None,
    base_url: str | None = None,
    timeout: float | None = None,
    expiry_warning_window: int | None = None,
) -> Config:
    parsed_api_key_expires = _parse_datetime(api_key_expires_at)

    return Config(
        client_id=client_id,
        api_key=api_key,
        api_key_expires_at=parsed_api_key_expires,
        base_url=base_url if base_url is not None else _DEFAULT_BASE_URL,
        timeout=timeout if timeout is not None else _DEFAULT_TIMEOUT,
        expiry_warning_window=(
            expiry_warning_window
            if expiry_warning_window is not None
            else _DEFAULT_EXPIRY_WARNING_WINDOW
        ),
    )
