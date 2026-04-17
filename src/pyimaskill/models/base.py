"""Base models and enums shared across modules."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, ConfigDict


class ImaModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class ContentFormat(IntEnum):
    PLAINTEXT = 0
    MARKDOWN = 1
    JSON = 2


class SearchType(IntEnum):
    TITLE = 0
    CONTENT = 1


class SortType(IntEnum):
    MODIFY_TIME = 0
    CREATE_TIME = 1
    TITLE = 2
    SIZE = 3


class FolderType(IntEnum):
    USER_CREATED = 0
    ALL_NOTES = 1
    UNCATEGORIZED = 2


class MediaType(IntEnum):
    PDF = 1
    WEBPAGE = 2
    WORD = 3
    PPT = 4
    EXCEL = 5
    WECHAT = 6
    MARKDOWN = 7
    IMAGE = 9
    NOTE = 11
    AI_SESSION = 12
    TXT = 13
    XMIND = 14
    AUDIO = 15
    VIDEO = 16
