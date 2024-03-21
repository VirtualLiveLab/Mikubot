from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from re import Pattern


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
