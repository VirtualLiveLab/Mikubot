from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface import IUrlExtractorPlugin


class UrlExtractor:
    def __init__(self) -> None:
        self.__plugins: "list[IUrlExtractorPlugin]" = []

    def use(self, plugin: "IUrlExtractorPlugin") -> None:
        self.__plugins.append(plugin)
