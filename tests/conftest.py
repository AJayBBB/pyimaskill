from unittest.mock import MagicMock, Mock

import pytest

from pyimaskill.client import ImaClient


@pytest.fixture
def mock_client():
    client = MagicMock(spec=ImaClient)
    client.request = Mock()
    client.notes = MagicMock()
    client.knowledge = MagicMock()
    return client


@pytest.fixture
def success_response():
    return {
        "code": 0,
        "msg": "成功",
        "data": {"note_id": "test_note_123"},
    }


@pytest.fixture
def error_response():
    return {
        "code": 210001,
        "msg": "参数错误",
        "data": {},
    }
