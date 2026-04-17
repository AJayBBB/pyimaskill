from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests

from pyimaskill.api.knowledge import KnowledgeAPI
from pyimaskill.api.notes import NotesAPI
from pyimaskill.config import Config, load_config
from pyimaskill.exceptions import raise_for_retcode

__all__ = ["ImaClient"]


class ImaClient:
    """Sync client for IMA OpenAPI.

    Usage:
        client = ImaClient(client_id="xxx", api_key="xxx")
        results = client.notes.search(query="Python")
        client.close()

    Or with context manager:
        with ImaClient(client_id="xxx", api_key="xxx") as client:
            results = client.notes.search(query="Python")
    """

    def __init__(
        self,
        client_id: str,
        api_key: str,
        api_key_expires_at: Optional[Union[str, datetime]] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        expiry_warning_window: Optional[int] = None,
        config: Optional[Config] = None,
    ) -> None:
        self._config = config or load_config(
            client_id=client_id,
            api_key=api_key,
            api_key_expires_at=api_key_expires_at,
            base_url=base_url,
            timeout=timeout,
            expiry_warning_window=expiry_warning_window,
        )
        self._config.emit_runtime_warnings()
        self._http = requests.Session()
        self._http.headers.update(self._config.build_headers())
        self._base_url = self._config.base_url
        self._timeout = self._config.timeout
        self.notes = NotesAPI(self)
        self.knowledge = KnowledgeAPI(self)

    def validate_credentials(self) -> List[str]:
        return self._config.validate_credentials()

    def request(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._http.post(
            f"{self._base_url}/{path}",
            json=body,
            timeout=self._timeout,
        )
        resp.raise_for_status()
        payload = resp.json()
        retcode = payload.get("code", payload.get("retcode", -1))
        errmsg = payload.get("msg", payload.get("errmsg", "Unknown error"))
        raise_for_retcode(retcode, errmsg)
        return payload.get("data", {})

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> ImaClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
