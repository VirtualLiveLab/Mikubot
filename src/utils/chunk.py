from collections.abc import Generator
from typing import TypeVar

_T = TypeVar("_T")


def chunks(iterable: list[_T], size: int) -> Generator[list[_T], None, None]:
    """Yield successive chunks from iterable of size."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def chunk_str_iter_with_max_str_length(iterable: list[str], max_str_length: int) -> Generator[list[str], None, None]:
    """Yield successive chunks from iterable of size."""
    while iterable:
        chunk = []
        while iterable and len("\n".join(chunk)) + len(iterable[0]) <= max_str_length:
            chunk.append(iterable.pop(0))
        yield chunk
