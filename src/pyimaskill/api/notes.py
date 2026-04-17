"""Notes API wrapper — all 6 note endpoints."""

from __future__ import annotations

from pyimaskill.models import ContentFormat, SearchType, SortType
from pyimaskill.models.notes import ListFolderResult, ListNotesResult, SearchNoteResult


class NotesAPI:
    def __init__(self, client) -> None:
        self._client = client
        self._base = "openapi/note/v1"

    def search(
        self,
        query: str = "",
        *,
        search_type: SearchType = SearchType.TITLE,
        sort_type: SortType = SortType.MODIFY_TIME,
        start: int = 0,
        end: int = 20,
    ) -> SearchNoteResult:
        body: dict = {
            "search_type": int(search_type),
            "sort_type": int(sort_type),
            "start": start,
            "end": end,
        }
        if query:
            key = "title" if search_type == SearchType.TITLE else "content"
            body["query_info"] = {key: query}
        data = self._client.request(f"{self._base}/search_note_book", body)
        return SearchNoteResult(**data)

    def list_folders(
        self,
        cursor: str = "0",
        limit: int = 20,
    ) -> ListFolderResult:
        data = self._client.request(
            f"{self._base}/list_notebook",
            {"cursor": cursor, "limit": limit},
        )
        return ListFolderResult(**data)

    def list_notes(
        self,
        folder_id: str = "",
        *,
        sort_type: SortType | None = None,
        cursor: str = "",
        limit: int = 20,
    ) -> ListNotesResult:
        body: dict = {"cursor": cursor, "limit": limit}
        if folder_id:
            body["folder_id"] = folder_id
        if sort_type is not None:
            body["sort_type"] = int(sort_type)
        data = self._client.request(f"{self._base}/list_note", body)
        return ListNotesResult(**data)

    def import_doc(
        self,
        content: str,
        *,
        folder_id: str | None = None,
    ) -> str:
        body: dict = {
            "content_format": int(ContentFormat.MARKDOWN),
            "content": content,
        }
        if folder_id is not None:
            body["folder_id"] = folder_id
        data = self._client.request(f"{self._base}/import_doc", body)
        return data["doc_id"]

    def append_doc(self, doc_id: str, content: str) -> str:
        body = {
            "doc_id": doc_id,
            "content_format": int(ContentFormat.MARKDOWN),
            "content": content,
        }
        data = self._client.request(f"{self._base}/append_doc", body)
        return data["doc_id"]

    def get_content(self, doc_id: str) -> str:
        data = self._client.request(
            f"{self._base}/get_doc_content",
            {"doc_id": doc_id, "target_content_format": 0},
        )
        return data["content"]
