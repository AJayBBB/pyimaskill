"""Pagination utilities for cursor-based APIs."""

from __future__ import annotations

from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


def paginate(
    fetch_fn: Callable[..., T],
    *,
    cursor_key: str = "cursor",
    limit: int = 20,
    max_pages: int | None = None,
    **kwargs,
) -> Iterator[T]:
    """Sync pagination helper for cursor-based APIs.

    Args:
        fetch_fn: Function to fetch a page. Must accept cursor and limit params.
        cursor_key: Name of cursor parameter in fetch_fn.
        limit: Number of items per page.
        max_pages: Maximum number of pages to fetch (None for unlimited).
        **kwargs: Additional arguments passed to fetch_fn.

    Yields:
        Result objects from each page.

    Example:
        for result in paginate(
            client.notes.list_folders,
            cursor_key="cursor",
            limit=20,
        ):
            for folder in result.note_book_folders:
                print(folder.folder.basic_info.name)
    """
    cursor = ""
    page_count = 0

    while True:
        if max_pages is not None and page_count >= max_pages:
            break

        page_kwargs = {cursor_key: cursor, "limit": limit, **kwargs}
        result = fetch_fn(**page_kwargs)

        yield result

        if result.is_end:
            break

        next_cursor = getattr(result, "next_cursor", None)
        if next_cursor is None or next_cursor == cursor:
            break
        cursor = next_cursor
        page_count += 1


class Paginator:
    """Stateful paginator for cursor-based APIs."""

    def __init__(
        self,
        fetch_fn: Callable[..., T],
        *,
        cursor_key: str = "cursor",
        limit: int = 20,
    ) -> None:
        self._fetch_fn = fetch_fn
        self._cursor_key = cursor_key
        self._limit = limit
        self._cursor = ""
        self._exhausted = False

    @property
    def is_exhausted(self) -> bool:
        """Check if all pages have been fetched."""
        return self._exhausted

    def fetch_next(self) -> T | None:
        """Fetch the next page.

        Returns:
            Next page result, or None if exhausted.
        """
        if self._exhausted:
            return None

        result = self._fetch_fn(
            **{self._cursor_key: self._cursor, "limit": self._limit}
        )

        if result.is_end:
            self._exhausted = True
        else:
            next_cursor = getattr(result, "next_cursor", None)
            if next_cursor is None or next_cursor == self._cursor:
                self._exhausted = True
            else:
                self._cursor = next_cursor

        return result

    def reset(self) -> None:
        """Reset pagination state to beginning."""
        self._cursor = ""
        self._exhausted = False
