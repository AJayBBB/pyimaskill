from unittest.mock import MagicMock, Mock

import pytest

from pyimaskill.client import ImaClient


@pytest.fixture
def mock_client():
    """Create a mock ImaClient with a mocked HTTP transport."""
    client = MagicMock(spec=ImaClient)
    client.request = Mock()
    client.notes = MagicMock()
    client.knowledge = MagicMock()
    return client


@pytest.fixture
def success_response():
    """Standard success API response."""
    return {
        "retcode": 0,
        "errmsg": "成功",
        "data": {"doc_id": "test_doc_123"},
    }


@pytest.fixture
def error_response():
    """Standard error API response."""
    return {
        "retcode": 100001,
        "errmsg": "参数错误",
        "data": {},
    }
