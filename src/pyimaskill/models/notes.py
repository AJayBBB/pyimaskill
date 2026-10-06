from __future__ import annotations

from typing import Dict, List

from pydantic import Field

from pyimaskill.models.base import FolderType, ImaModel


class NoteExtinfo(ImaModel):
    folder_id: str = ""
    folder_name: str = ""


class NoteBookInfo(ImaModel):
    note_id: str = ""
    title: str = ""
    summary: str = ""
    create_time: int = 0
    modify_time: int = 0
    cover_image: str = ""
    note_ext_info: NoteExtinfo = Field(default_factory=NoteExtinfo)


class NoteFolderInfo(ImaModel):
    folder_id: str = ""
    name: str = ""
    create_time: int = 0
    modify_time: int = 0
    note_number: int = 0
    parent_folder_id: str = ""
    folder_type: FolderType = FolderType.USER_CREATE


class SearchNoteInfo(ImaModel):
    note_book_info: NoteBookInfo = Field(default_factory=NoteBookInfo)
    highlightInfo: Dict[str, str] = Field(default_factory=dict)


class SearchNoteResult(ImaModel):
    search_note_infos: List[SearchNoteInfo] = Field(default_factory=list)
    is_end: bool = True
    total_hit_num: int = 0


class ListFolderResult(ImaModel):
    note_folder_infos: List[NoteFolderInfo] = Field(default_factory=list)
    next_cursor: str = ""
    is_end: bool = True
    next_version: str = ""
    need_update: bool = False


class ListNotesResult(ImaModel):
    note_book_list: List[NoteBookInfo] = Field(default_factory=list)
    is_end: bool = True


class GetContentResult(ImaModel):
    content: str = ""


class ImportNoteResult(ImaModel):
    note_id: str = ""


class AppendNoteResult(ImaModel):
    note_id: str = ""
