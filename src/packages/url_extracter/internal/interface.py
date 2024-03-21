from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, ClassVar, TypedDict

if TYPE_CHECKING:
    from re import Pattern


class PluginConfig(TypedDict):
    auto_escape: Annotated[bool, True]


class IUrlExtractorPlugin(ABC):
    """
    Interface for URL extractor plugins.
    """

    config: ClassVar[PluginConfig] = {"auto_escape": True}

    @abstractmethod
    def url_pattern(self) -> "Pattern[str]":
        """
        Returns the regular expression pattern used to match URLs.
        """
        raise NotImplementedError
