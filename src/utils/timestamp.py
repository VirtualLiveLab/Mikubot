from datetime import datetime, timezone
from enum import StrEnum
from typing import Self


# https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
class DiscordTimestampStyle(StrEnum):
    SHORT_TIME = "t"
    LONG_TIME = "T"
    SHORT_DATE = "d"
    LONG_DATE = "D"
    LONG_DATE_WITH_SHORT_TIME = "f"
    LONG_DATE_WITH_DAY_OF_WEEK_AND_SHORT_TIME = "F"
    RELATIVE = "R"


class DiscordTimestamp:
    def __init__(self, posix_timestamp: str) -> None:
        self.posix_timestamp = posix_timestamp

    @classmethod
    def from_datetime(cls, dt: datetime, tz: timezone) -> Self:
        return cls(str(int(dt.astimezone(tz).timestamp())))

    def to_discord_timestamp(self, style: DiscordTimestampStyle = DiscordTimestampStyle.LONG_DATE_WITH_SHORT_TIME) -> str:
        return f"<t:{self.posix_timestamp}:{style}>"
