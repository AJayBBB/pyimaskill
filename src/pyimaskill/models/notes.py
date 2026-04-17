"""Note-related models."""

from __future__ import annotations

from typing import Dict, List

from pydantic import Field

from pyimaskill.models.base import FolderType, ImaModel


class DocBasic(ImaModel):
    docid: str = ""
    title: str = ""
    summary: str = ""
    create_time: int = 0
    modify_time: int = 0
    status: int = 0
    folder_id: str = ""
    folder_name: str = ""


class DocBasicInfo(ImaModel):
    basic_info: DocBasic = Field(default_factory=DocBasic)


class NoteBookFolderBasic(ImaModel):
    folder_id: str = ""
    name: str = ""
    status: int = 0
    create_time: int = 0
    modify_time: int = 0
    note_number: int = 0
    folder_type: FolderType = FolderType.USER_CREATED


class NoteBookFolderBasicInfo(ImaModel):
    basic_info: NoteBookFolderBasic = Field(default_factory=NoteBookFolderBasic)


class NoteBookFolder(ImaModel):
    folder: NoteBookFolderBasicInfo = Field(default_factory=NoteBookFolderBasicInfo)


class NoteBookInfo(ImaModel):
    basic_info: DocBasicInfo = Field(default_factory=DocBasicInfo)


class SearchedDoc(ImaModel):
    doc: DocBasicInfo = Field(default_factory=DocBasicInfo)
    highlight_info: Dict[str, str] = Field(default_factory=dict)


class SearchNoteResult(ImaModel):
    docs: List[SearchedDoc] = Field(default_factory=list)
    is_end: bool = True
    total_hit_num: int = 0


class ListFolderResult(ImaModel):
    note_book_folders: List[NoteBookFolder] = Field(default_factory=list)
    next_cursor: str = ""
    is_end: bool = True


class ListNotesResult(ImaModel):
    note_book_list: List[NoteBookInfo] = Field(default_factory=list)
    next_cursor: str = ""
    is_end: bool = True
