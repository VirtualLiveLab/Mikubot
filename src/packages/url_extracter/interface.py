from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from re import Pattern


class IUrlExtractorPlugin(ABC):
    """
    Interface for URL extractor plugins.
    """

    @abstractmethod
    def get_url_pattern(self) -> "Pattern[str] | str":
        """
        Returns the regular expression pattern used to match URLs.
        """
        raise NotImplementedError

    @abstractmethod
    def extract(self, url: str) -> "str | Awaitable[str]":
        """
        Extracts relevant information from the given URL and returns it as a string.
        """
        raise NotImplementedError
