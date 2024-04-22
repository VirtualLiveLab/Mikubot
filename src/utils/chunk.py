from collections.abc import Generator, Iterable
from typing import LiteralString, TypeVar

_T = TypeVar("_T")


def chunks(iterable: list[_T], *, size: int) -> Generator[list[_T], None, None]:
    """Yield successive chunks from iterable of size."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


class InvalidMaxLengthError(ValueError):
    def __init__(self, max_length: int) -> None:
        super().__init__(f"max_length must be greater than 0, but got {max_length}")


class InvalidIterableLengthError(ValueError):
    def __init__(self, length: int) -> None:
        super().__init__(f"length of the iterable must be greater than 0, but got {length}")


class FragmentTooLargeError(ValueError):
    def __init__(self, fragment: str, max_length: int) -> None:
        super().__init__(f"fragment is too large: {fragment} (got: {len(fragment)}, max_length: {max_length})")


def chunk_str_iter_with_max_length(
    iterable: Iterable[str],
    *,
    max_length: int,
    separator: LiteralString,
    ignore_oversize_fragment: bool = True,
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
    ignore_oversize_fragment: `bool`, optional, default is `True`
        If `True`, ignore the fragment that exceeds the `max_length`.
        If `False`, raise `FragmentTooLargeError` when the fragment exceeds the `max_length`.

    Yields
    ------
    `Generator[str, None, None]`
        Chunked strings with a maximum length. joined by the specified separator.

    Raises
    ------
    `InvalidMaxLengthError`
        If `max_length` is less than or equal to 0.
    `InvalidIterableLengthError`
        If the length of the `iterable` is 0.
    `FragmentTooLargeError`
        If the fragment exceeds the `max_length` and `ignore_oversize_fragment` is `False`.
    """
    if max_length <= 0:
        raise InvalidMaxLengthError(max_length)

    def safe_len(iterable: Iterable) -> int:
        try:
            return iterable.__len__()  # type: ignore[attr-defined]
        except AttributeError:
            return sum(1 for _ in iterable)

    if (length := safe_len(iterable)) == 0:
        raise InvalidIterableLengthError(length)

    # chunkをstrにして毎回文字列結合をすると、Pythonの言語仕様上遅いので、
    # 配列で保存してyieldするタイミングで結合する
    # 参考1: https://nixeneko.hatenablog.com/entry/2021/07/29/143621
    # 参考2: https://dev.to/fayomihorace/python-how-simple-string-concatenation-can-kill-your-code-performance-2636
    chunk_fragment: list[str] = []
    chunk_length: int = 0
    separator_len: int = len(separator)

    for i in iterable:
        fragment_len = len(i)

        # chunkが初期状態の場合
        if chunk_fragment == []:
            # 一つの文字列がmax_lengthを超えている場合
            if (fragment_len) > max_length:
                if ignore_oversize_fragment:
                    continue
                else:
                    raise FragmentTooLargeError(fragment=i, max_length=max_length)

            # next: 'fragment'
            chunk_fragment.append(i)
            chunk_length += fragment_len
            continue

        # これ以上文字列を追加できないので、今までの文字列を結合してyieldする
        if (next_length := chunk_length + fragment_len + separator_len) > max_length:
            yield separator.join(chunk_fragment)
            # その後chunkを初期化
            chunk_fragment.clear()
            chunk_length = 0
            continue

        # next: '...current + separator + fragment'
        chunk_fragment.append(i)
        chunk_length = next_length
        continue

    # 最後のchunkをyieldする
    yield separator.join(chunk_fragment)
