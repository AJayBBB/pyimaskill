"""Knowledge base models."""

from __future__ import annotations

from pydantic import Field

from pyimaskill.models.base import ImaModel


class KnowledgeBaseInfo(ImaModel):
    id: str = ""
    name: str = ""
    cover_url: str = ""
    description: str = ""
    recommended_questions: list[str] = Field(default_factory=list)


class KnowledgeInfo(ImaModel):
    media_id: str = ""
    title: str = ""
    parent_folder_id: str = ""


class FolderInfo(ImaModel):
    folder_id: str = ""
    name: str = ""
    file_number: int = 0
    folder_number: int = 0
    parent_folder_id: str = ""
    is_top: bool = False


class AddableKnowledgeBaseInfo(ImaModel):
    id: str = ""
    name: str = ""


class SearchedKnowledgeBaseInfo(ImaModel):
    id: str = ""
    name: str = ""
    cover_url: str = ""


class SearchedKnowledgeInfo(ImaModel):
    media_id: str = ""
    title: str = ""
    parent_folder_id: str = ""
    highlight_content: str = ""


class FileInfo(ImaModel):
    cos_key: str = ""
    file_size: int = 0
    file_name: str = ""
    last_modify_time: int = 0
    password: str = ""


class Credential(ImaModel):
    token: str = ""
    secret_id: str = ""
    secret_key: str = ""
    start_time: int = 0
    expired_time: int = 0
    appid: str = ""
    bucket_name: str = ""
    region: str = ""
    custom_domain: str = ""
    cos_key: str = ""


class ImportURLData(ImaModel):
    url: str = ""
    ret_code: int = 0
    media_id: str = ""


class CheckRepeatedNamesParam(ImaModel):
    name: str = ""
    media_type: int = 0


class CheckRepeatedNamesResult(ImaModel):
    name: str = ""
    is_repeated: bool = False


class CreateMediaResult(ImaModel):
    media_id: str = ""
    cos_credential: Credential = Field(default_factory=Credential)


class AddKnowledgeResult(ImaModel):
    media_id: str = ""


class GetKnowledgeBaseResult(ImaModel):
    infos: dict[str, KnowledgeBaseInfo] = Field(default_factory=dict)


class GetKnowledgeListResult(ImaModel):
    knowledge_list: list[KnowledgeInfo] = Field(default_factory=list)
    is_end: bool = True
    next_cursor: str = ""
    current_path: list[FolderInfo] = Field(default_factory=list)


class SearchKnowledgeResult(ImaModel):
    info_list: list[SearchedKnowledgeInfo] = Field(default_factory=list)
    is_end: bool = True
    next_cursor: str = ""


class SearchKnowledgeBaseResult(ImaModel):
    info_list: list[SearchedKnowledgeBaseInfo] = Field(default_factory=list)
    is_end: bool = True
    next_cursor: str = ""


class GetAddableKBListResult(ImaModel):
    addable_knowledge_base_list: list[AddableKnowledgeBaseInfo] = Field(default_factory=list)
    next_cursor: str = ""
    is_end: bool = True


class CheckRepeatedNamesResultWrapper(ImaModel):
    results: list[CheckRepeatedNamesResult] = Field(default_factory=list)


class ImportURLsResult(ImaModel):
    results: dict[str, ImportURLData] = Field(default_factory=dict)
