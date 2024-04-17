from collections.abc import Generator, Iterable
from typing import LiteralString, TypeVar

_T = TypeVar("_T")


def chunks(iterable: list[_T], *, size: int) -> Generator[list[_T], None, None]:
    """Yield successive chunks from iterable of size."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def chunk_str_iter_with_max_length(
    iterable: Iterable[str], *, max_length: int, separator: LiteralString
) -> Generator[str, None, None]:
    """
    Chunk the iterable of strings into strings with a maximum length.

    Parameters
    ----------
    iterable : `Iterable[str]`
         Iterable of strings to be chunked.
    max_length : `int`
        Maximum length of the chunked strings.
    separator : `LiteralString`
        Separator to join the strings.

    Yields
    ------
    `Generator[str, None, None]`
        Chunked strings with a maximum length. joined by the specified separator.
    """
    # chunkをstrにして毎回文字列結合をすると、Pythonの言語仕様上遅いので、
    # 配列で保存してyieldするタイミングで結合する
    # 参考1: https://nixeneko.hatenablog.com/entry/2021/07/29/143621
    # 参考2: https://dev.to/fayomihorace/python-how-simple-string-concatenation-can-kill-your-code-performance-2636
    chunk_fragment: list[str] = []
    chunk_length: int = 0
    for i in iterable:
        if (chunk_length + (new_fragment_len := len(separator) + len(i))) > max_length:
            # これ以上文字列を追加できないので、今までの文字列を結合してyieldする
            yield separator.join(chunk_fragment)
            # その後、chunkを初期化
            chunk_fragment.clear()
            chunk_length = 0
        chunk_fragment.append(i)
        chunk_length += new_fragment_len
