import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface import IUrlExtractorPlugin, PluginConfig


class InternalPlugin:
    def __init__(self, key: str, plugin: "IUrlExtractorPlugin", /, *, index: int) -> None:
        self.__config = plugin.config
        self.__key = key
        self.__index = index
        self.__pattern = self.__compile_pattern(plugin.url_pattern())

    @property
    def key(self) -> str:
        return self.__key

    @property
    def index(self) -> int:
        return self.__index

    @property
    def config(self) -> "PluginConfig":
        return self.__config

    @property
    def pattern(self) -> re.Pattern[str]:
        return self.__pattern

    def __compile_pattern(self, pattern: re.Pattern[str], /) -> re.Pattern[str]:
        if self.__config["auto_escape"]:
            return re.compile(re.escape(pattern.pattern))
        return re.compile(pattern.pattern)
