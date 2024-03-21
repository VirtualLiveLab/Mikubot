from typing import TYPE_CHECKING, Generic, LiteralString, TypeVar

from asyncer import asyncify
from result import Err, Ok

from src.utils.logger import get_my_logger

from .internal import InternalPlugin, IUrlExtractorPlugin

if TYPE_CHECKING:
    from re import Match, Pattern

    from result import Result

_K = TypeVar("_K", bound=LiteralString)
_PLUGIN = TypeVar("_PLUGIN", bound=IUrlExtractorPlugin)


class UrlExtractor(Generic[_K, _PLUGIN]):
    """A class for extracting URLs using plugins."""

    def __init__(self, plugins: dict[_K, _PLUGIN], /) -> None:
        self.__plugins = {k: InternalPlugin(k, p, index=i) for i, (k, p) in enumerate(plugins.items())}
        self.__logger = get_my_logger(self.__class__.__name__)

    def find_all(self, string: str) -> "dict[_K, set[Match[str]] | None]":
        """Find all occurrences of URLs in the given string using the registered plugins.

        Args:
            string `str`: The input string to search for URLs.

        Returns:
            `dict[_K, set[Match[str]] | None]`: A dictionary containing the plugin keys as keys and
                a set of matches or None as values. Each set of matches represents the URLs found
                by the corresponding plugin.
        """
        return {
            k: self._safe_match_iter(pattern=plugin.pattern, string=string).unwrap_or(None)
            for k, plugin in self.__plugins.items()
        }

    async def find_all_async(self, string: str) -> "dict[_K, set[Match[str]] | None]":
        """Find all occurrences of URLs in the given string using the registered plugins asynchronously.

        Args:
            string `str`: The input string to search for URLs.

        Returns:
            `dict[_K, set[Match[str]] | None]`: A dictionary containing the plugin keys as keys and
                a set of matches or None as values. Each set of matches represents the URLs found
                by the corresponding plugin.
        """
        return await asyncify(self.find_all)(string=string)

    def _safe_match_iter(self, /, *, pattern: "Pattern[str]", string: str) -> "Result[set[Match[str]] | None, Exception]":
        """Safely perform a regex finditer operation on the given string.

        Args:
            pattern `Pattern[str]`: The regex pattern to match.
            string `str`: The input string to search for matches.

        Returns:
            `Result[set[Match[str]] | None, Exception]`: A Result object containing a set of matches
                or None if no matches were found. If an exception occurs during the operation, an
                Err object containing the exception is returned.
        """
        try:
            found_iter = set(pattern.finditer(string=string))
            if len(found_iter) == 0:
                self.__logger.debug("No matches found.")
                return Ok(None)
            return Ok(found_iter)
        except Exception as e:
            self.__logger.exception("An error occurred while searching for matches.")
            return Err(e)

    def _safe_match_first(self, /, *, pattern: "Pattern[str]", string: str) -> "Result[Match[str] | None, Exception]":
        """Safely perform a regex search operation on the given string.

        Args:
            pattern `Pattern[str]`: The regex pattern to match.
            string `str: The input string to search for a match.

        Returns:
            `Result[Match[str] | None, Exception]`: A Result object containing the first match found
                or None if no match was found. If an exception occurs during the operation, an Err
                object containing the exception is returned.
        """
        try:
            return Ok(pattern.search(string=string))
        except Exception as e:
            self.__logger.exception("An error occurred while searching for a match.")
            return Err(e)
