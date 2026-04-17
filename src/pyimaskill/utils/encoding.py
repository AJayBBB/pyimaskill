"""UTF-8 encoding utilities for note content."""

from __future__ import annotations

import codecs
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def ensure_utf8(text: str) -> str:
    """Ensure text is valid UTF-8.

    This function validates and cleans text to ensure it's valid UTF-8.
    Use this before writing note content to IMA.

    Args:
        text: Input text that may contain invalid UTF-8 bytes.

    Returns:
        Valid UTF-8 text.

    Example:
        content = ensure_utf8(user_input)
        client.notes.import_doc(content=content)
    """
    # Encode to bytes and decode back to UTF-8, replacing invalid sequences
    return text.encode("utf-8", errors="replace").decode("utf-8")


def detect_encoding(data: bytes) -> str:
    """Detect the encoding of byte data.

    Tries common encodings in order: UTF-8, GBK, GB2312, Big5, Latin-1.

    Args:
        data: Raw byte data.

    Returns:
        Detected encoding name.

    Raises:
        ValueError: If encoding cannot be detected.
    """
    # Try UTF-8 first (most common)
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # Try other common encodings
    for encoding in ("gbk", "gb2312", "big5", "latin-1"):
        try:
            data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue

    raise ValueError("Unable to detect encoding")


def convert_to_utf8(data: bytes, source_encoding: Optional[str] = None) -> str:
    """Convert bytes to UTF-8 string.

    Args:
        data: Raw byte data.
        source_encoding: Source encoding. If None, auto-detect.

    Returns:
        UTF-8 decoded string.

    Example:
        with open("notes.txt", "rb") as f:
            content = convert_to_utf8(f.read())
    """
    if source_encoding is None:
        source_encoding = detect_encoding(data)

    return data.decode(source_encoding).encode("utf-8").decode("utf-8")


def sanitize_text(text: str) -> str:
    """Sanitize text by removing common problem characters.

    Removes:
    - BOM (Byte Order Mark)
    - Zero-width characters
    - Invalid control characters

    Args:
        text: Input text.

    Returns:
        Sanitized text.
    """
    # Remove BOM if present
    if text.startswith("\ufeff"):
        text = text[1:]

    # Remove zero-width characters
    zero_width_chars = [
        "\u200b",  # Zero Width Space
        "\u200c",  # Zero Width Non-Joiner
        "\u200d",  # Zero Width Joiner
        "\ufeff",  # Zero Width No-Break Space (BOM)
    ]
    for char in zero_width_chars:
        text = text.replace(char, "")

    # Remove invalid control characters (keep only valid Unicode categories)
    # Keep: tab (9), newline (10), carriage return (13)
    result = []
    for char in text:
        code = ord(char)
        # Allow printable characters, tabs, newlines
        if code >= 32 or char in "\t\n\r":
            result.append(char)
    return "".join(result)


class UTF8Validator:
    """Utility class for validating UTF-8 text."""

    @staticmethod
    def is_valid(text: str) -> bool:
        """Check if text is valid UTF-8."""
        try:
            text.encode("utf-8")
            return True
        except UnicodeEncodeError:
            return False

    @staticmethod
    def validate_or_raise(text: str) -> str:
        """Validate text is valid UTF-8, raise if not."""
        if not UTF8Validator.is_valid(text):
            raise ValueError("Text contains invalid UTF-8 characters")
        return text


def with_utf8_validation(
    func: Callable[[str], T]
) -> Callable[[str], T]:
    """Decorator to validate UTF-8 before function call.

    Use on functions that process note content.

    Example:
        @with_utf8_validation
        def process_content(content: str) -> dict:
            ...
    """
    def wrapper(text: str) -> T:
        validated = ensure_utf8(sanitize_text(text))
        return func(validated)
    return wrapper
