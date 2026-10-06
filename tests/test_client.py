import pytest
import responses

from pyimaskill.client import ImaClient
from pyimaskill.exceptions import ImaError


@responses.activate
def test_search_notes():
    responses.post(
        "https://ima.qq.com/openapi/note/v1/search_note",
        json={
            "code": 0,
            "msg": "成功",
            "data": {
                "search_note_infos": [
                    {
                        "note_book_info": {
                            "note_id": "note_1",
                            "title": "Test Note",
                            "summary": "A test note",
                        },
                        "highlightInfo": {},
                    }
                ],
                "is_end": True,
                "total_hit_num": 1,
            },
        },
    )

    with ImaClient(client_id="test_id", api_key="test_key") as client:
        result = client.notes.search(query="Test")
        assert len(result.search_note_infos) == 1
        assert result.search_note_infos[0].note_book_info.note_id == "note_1"


@responses.activate
def test_import_doc():
    responses.post(
        "https://ima.qq.com/openapi/note/v1/import_doc",
        json={
            "code": 0,
            "msg": "成功",
            "data": {"note_id": "new_note_123"},
        },
    )

    with ImaClient(client_id="test_id", api_key="test_key") as client:
        note_id = client.notes.import_doc(content="# Test\n\nContent")
        assert note_id == "new_note_123"


@responses.activate
def test_error_handling():
    responses.post(
        "https://ima.qq.com/openapi/note/v1/search_note",
        json={
            "code": 210001,
            "msg": "参数错误",
            "data": {},
        },
    )

    with ImaClient(client_id="test_id", api_key="test_key") as client:
        with pytest.raises(ImaError) as exc_info:
            client.notes.search(query="Test")
        assert exc_info.value.code == 210001


@responses.activate
def test_search_knowledge_base():
    responses.post(
        "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base",
        json={
            "code": 0,
            "msg": "成功",
            "data": {
                "info_list": [
                    {"id": "kb_1", "name": "Test KB", "cover_url": ""}
                ],
                "is_end": True,
                "next_cursor": "",
            },
        },
    )

    with ImaClient(client_id="test_id", api_key="test_key") as client:
        result = client.knowledge.search_knowledge_base(query="Test")
        assert len(result.info_list) == 1
        assert result.info_list[0].name == "Test KB"


@responses.activate
def test_import_urls():
    responses.post(
        "https://ima.qq.com/openapi/wiki/v1/import_urls",
        json={
            "code": 0,
            "msg": "成功",
            "data": {
                "results": {
                    "https://example.com": {
                        "url": "https://example.com",
                        "ret_code": 0,
                        "media_id": "media_1",
                    }
                }
            },
        },
    )

    with ImaClient(client_id="test_id", api_key="test_key") as client:
        result = client.knowledge.import_urls(
            knowledge_base_id="kb_1",
            urls=["https://example.com"],
        )
        assert "https://example.com" in result.results
