from typing import TYPE_CHECKING, Generic, LiteralString, TypeVar

from .interface import IUrlExtractorPlugin

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from re import Pattern


_K = TypeVar("_K", bound=LiteralString)
_PLUGIN = TypeVar("_PLUGIN", bound=IUrlExtractorPlugin)


class UrlExtractor(Generic[_K, _PLUGIN]):
    def __init__(self, plugins: dict[_K, _PLUGIN], /) -> None:
        self.__plugins = plugins

    def extract(self, url: str) -> dict[_K, str]:  # noqa: ARG002
        return {}


class ExamplePlugin(IUrlExtractorPlugin):
    def get_url_pattern(self) -> "Pattern[str] | str":
        return r"https://www.google.com"

    def extract(self, url: str) -> "str | Awaitable[str]":  # noqa: ARG002
        return "Google"


class ExamplePluginB(IUrlExtractorPlugin):
    def get_url_pattern(self) -> "Pattern[str] | str":
        return r"https://www.google.com"

    def extract(self, url: str) -> "str | Awaitable[str]":  # noqa: ARG002
        return "Google"


a = UrlExtractor({"a": ExamplePlugin(), "b": ExamplePluginB()})

aa = a.extract("https://www.google.com")
aaa = aa["a"]  # a, b will be inferred
