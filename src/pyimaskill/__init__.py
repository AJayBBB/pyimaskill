"""pyimaskill — Python SDK for IMA OpenAPI."""

from __future__ import annotations

__version__ = "1.1.3"
__all__ = ["Config", "ImaClient", "ImaError", "KnowledgeAPI", "NotesAPI"]

from pyimaskill.api.knowledge import KnowledgeAPI
from pyimaskill.api.notes import NotesAPI
from pyimaskill.client import ImaClient
from pyimaskill.config import Config
from pyimaskill.exceptions import ImaError
