"""Knowledge API wrapper — all 9 knowledge endpoints + file upload."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests

from pyimaskill.models.knowledge import (
    AddKnowledgeResult,
    CheckRepeatedNamesResultWrapper,
    CreateMediaResult,
    GetAddableKBListResult,
    GetKnowledgeBaseResult,
    GetKnowledgeListResult,
    ImportURLsResult,
    SearchKnowledgeBaseResult,
    SearchKnowledgeResult,
)


class KnowledgeAPI:
    def __init__(self, client) -> None:
        self._client = client
        self._base = "openapi/wiki/v1"

    def create_media(
        self,
        file_name: str,
        file_size: int,
        content_type: str,
        knowledge_base_id: str,
        file_ext: str,
    ) -> CreateMediaResult:
        body = {
            "file_name": file_name,
            "file_size": file_size,
            "content_type": content_type,
            "knowledge_base_id": knowledge_base_id,
            "file_ext": file_ext,
        }
        data = self._client.request(f"{self._base}/create_media", body)
        return CreateMediaResult(**data)

    def add_knowledge(
        self,
        media_type: int,
        title: str,
        knowledge_base_id: str,
        *,
        media_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        file_info: Optional[Dict[str, Any]] = None,
        web_info: Optional[Dict[str, Any]] = None,
        note_info: Optional[Dict[str, Any]] = None,
        session_info: Optional[Dict[str, Any]] = None,
    ) -> AddKnowledgeResult:
        body: Dict[str, Any] = {
            "media_type": media_type,
            "title": title,
            "knowledge_base_id": knowledge_base_id,
        }
        if media_id:
            body["media_id"] = media_id
        if folder_id:
            body["folder_id"] = folder_id
        if file_info:
            body["file_info"] = file_info
        if web_info:
            body["web_info"] = web_info
        if note_info:
            body["note_info"] = note_info
        if session_info:
            body["session_info"] = session_info
        data = self._client.request(f"{self._base}/add_knowledge", body)
        return AddKnowledgeResult(**data)

    def get_knowledge_base(self, ids: List[str]) -> GetKnowledgeBaseResult:
        data = self._client.request(
            f"{self._base}/get_knowledge_base", {"ids": ids}
        )
        return GetKnowledgeBaseResult(infos=data.get("infos", {}))

    def get_knowledge_list(
        self,
        knowledge_base_id: str,
        cursor: str = "",
        limit: int = 20,
        folder_id: Optional[str] = None,
    ) -> GetKnowledgeListResult:
        body: Dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "cursor": cursor,
            "limit": limit,
        }
        if folder_id:
            body["folder_id"] = folder_id
        data = self._client.request(f"{self._base}/get_knowledge_list", body)
        return GetKnowledgeListResult(**data)

    def search_knowledge(
        self,
        query: str,
        knowledge_base_id: str,
        cursor: str = "",
    ) -> SearchKnowledgeResult:
        body = {
            "query": query,
            "knowledge_base_id": knowledge_base_id,
            "cursor": cursor,
        }
        data = self._client.request(f"{self._base}/search_knowledge", body)
        return SearchKnowledgeResult(**data)

    def search_knowledge_base(
        self,
        query: str,
        cursor: str = "",
        limit: int = 20,
    ) -> SearchKnowledgeBaseResult:
        body = {
            "query": query,
            "cursor": cursor,
            "limit": limit,
        }
        data = self._client.request(f"{self._base}/search_knowledge_base", body)
        return SearchKnowledgeBaseResult(**data)

    def get_addable_knowledge_base_list(
        self,
        cursor: str = "",
        limit: int = 20,
    ) -> GetAddableKBListResult:
        body = {"cursor": cursor, "limit": limit}
        data = self._client.request(
            f"{self._base}/get_addable_knowledge_base_list", body
        )
        return GetAddableKBListResult(**data)

    def check_repeated_names(
        self,
        knowledge_base_id: str,
        params: List[Dict[str, Any]],
        folder_id: Optional[str] = None,
    ) -> CheckRepeatedNamesResultWrapper:
        body: Dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "params": params,
        }
        if folder_id:
            body["folder_id"] = folder_id
        data = self._client.request(f"{self._base}/check_repeated_names", body)
        return CheckRepeatedNamesResultWrapper(**data)

    def import_urls(
        self,
        knowledge_base_id: str,
        urls: List[str],
        folder_id: Optional[str] = None,
    ) -> ImportURLsResult:
        body: Dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "urls": urls,
        }
        if folder_id:
            body["folder_id"] = folder_id
        data = self._client.request(f"{self._base}/import_urls", body)
        return ImportURLsResult(results=data.get("results", {}))

    def upload_file(
        self,
        file_path: Union[str, Path],
        knowledge_base_id: str,
        folder_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> AddKnowledgeResult:
        file_path = Path(file_path)
        file_name = file_path.name
        file_ext = file_path.suffix.lstrip(".")
        file_size = file_path.stat().st_size

        content_type = self._guess_content_type(file_ext)
        media_type = self._guess_media_type(file_ext)

        media_result = self.create_media(
            file_name=file_name,
            file_size=file_size,
            content_type=content_type,
            knowledge_base_id=knowledge_base_id,
            file_ext=file_ext,
        )

        cred = media_result.cos_credential
        self._upload_to_cos(file_path, cred)

        return self.add_knowledge(
            media_type=media_type,
            media_id=media_result.media_id,
            title=title or file_name,
            knowledge_base_id=knowledge_base_id,
            folder_id=folder_id,
            file_info={
                "cos_key": cred.cos_key,
                "file_size": file_size,
                "file_name": file_name,
            },
        )

    def _upload_to_cos(self, file_path: Path, cred) -> None:
        import time

        key_time_start = str(int(time.time()))
        key_time_end = str(int(time.time()) + 3600)

        import hashlib
        import hmac

        def hmac_sha1(key: str, data: str) -> str:
            return hmac.new(
                key.encode(), data.encode(), hashlib.sha1
            ).hexdigest()

        def sha1_hex(data: str) -> str:
            return hashlib.sha1(data.encode()).hexdigest()

        hostname = f"{cred.bucket_name}.cos.{cred.region}.myqcloud.com"
        pathname = f"/{cred.cos_key}"

        file_content = file_path.read_bytes()
        content_length = str(len(file_content))

        header_list = "content-length;host"
        http_headers = (
            f"content-length={content_length}&host={hostname}"
        )
        http_string = f"put\n{pathname}\n\n{http_headers}\n"
        key_time = f"{key_time_start};{key_time_end}"
        sign_key = hmac_sha1(cred.secret_key, key_time)
        string_to_sign = f"sha1\n{key_time}\n{sha1_hex(http_string)}\n"
        signature = hmac_sha1(sign_key, string_to_sign)

        authorization = (
            f"q-sign-algorithm=sha1&q-ak={cred.secret_id}"
            f"&q-sign-time={key_time}&q-key-time={key_time}"
            f"&q-header-list={header_list}&q-url-param-list="
            f"&q-signature={signature}"
        )

        resp = requests.put(
            f"https://{hostname}{pathname}",
            data=file_content,
            headers={
                "Content-Type": self._guess_content_type(
                    file_path.suffix.lstrip(".")
                ),
                "Content-Length": content_length,
                "Authorization": authorization,
                "x-cos-security-token": cred.token,
            },
        )
        resp.raise_for_status()

    @staticmethod
    def _guess_content_type(ext: str) -> str:
        return {
            "pdf": "application/pdf",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "ppt": "application/vnd.ms-powerpoint",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "xls": "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "csv": "text/csv",
            "md": "text/markdown",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
            "txt": "text/plain",
            "mp3": "audio/mpeg",
            "m4a": "audio/x-m4a",
            "wav": "audio/wav",
            "aac": "audio/aac",
        }.get(ext, "application/octet-stream")

    @staticmethod
    def _guess_media_type(ext: str) -> int:
        return {
            "pdf": 1,
            "doc": 3,
            "docx": 3,
            "ppt": 4,
            "pptx": 4,
            "xls": 5,
            "xlsx": 5,
            "csv": 5,
            "md": 7,
            "png": 9,
            "jpg": 9,
            "jpeg": 9,
            "webp": 9,
            "txt": 13,
            "mp3": 15,
            "m4a": 15,
            "wav": 15,
            "aac": 15,
        }.get(ext, 1)
