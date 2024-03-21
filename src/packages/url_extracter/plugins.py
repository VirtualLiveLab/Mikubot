import re

from .internal import IUrlExtractorPlugin

regex_discord_message_url = re.compile(
    "(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/"
    "(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})(?!>)"
)


class DiscordPlugin(IUrlExtractorPlugin):
    def url_pattern(self) -> re.Pattern[str]:
        return regex_discord_message_url


class NotionPlugin(IUrlExtractorPlugin):
    def __init__(self, workspace: str = ".*") -> None:
        super().__init__()
        self.__workspace = workspace

    def url_pattern(self) -> re.Pattern[str]:
        return re.compile(f"https://www.notion.so/{self.__workspace}/[a-f0-9]{32}")
