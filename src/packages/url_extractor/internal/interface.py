from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from re import Match, Pattern


class IUrlExtractorPlugin(ABC):
    """
    Interface for URL extractor plugins.
    """

    @abstractmethod
    def url_pattern(self) -> "Pattern[str] | str":
        """
        Returns the regular expression pattern used to match URLs.
        """
        raise NotImplementedError


class IUrlSyncProcessor[R](ABC):
    """
    Interface for URL processors.
    """

    @abstractmethod
    def from_matches_sync(self, matches: "Iterable[Match[str]]") -> list[R]:
        """
        Extracts information from the given matches.
        """
        raise NotImplementedError


class IUrlAsyncProcessor[R](ABC):
    """
    Interface for URL processors. For asynchronous processing.
    """

    @abstractmethod
    async def from_matches_async(self, matches: "Iterable[Match[str]]") -> list[R]:
        """
        Extracts information from the given matches.
        """
        raise NotImplementedError
