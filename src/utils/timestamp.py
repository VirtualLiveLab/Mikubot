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
    """
    Utility class for Discord timestamp.

    ref: https://discord.com/developers/docs/reference#message-formatting-timestamp-styles
    """

    def __init__(self, posix_timestamp: str) -> None:
        self.posix_timestamp = posix_timestamp

    @classmethod
    def from_datetime(cls, dt: datetime, tz: timezone) -> Self:
        """
        initialize with datetime object.

        Parameters
        ----------
        dt : `datetime.datetime`
        tz : `datetime.timezone`

        Returns
        -------
        Self
            DiscordTimestamp object.
        """
        return cls(str(int(dt.astimezone(tz).timestamp())))

    def export_with_style(self, style: DiscordTimestampStyle = DiscordTimestampStyle.LONG_DATE_WITH_SHORT_TIME) -> str:
        """
        export timestamp with style for sending to Discord.
        default style is `LONG_DATE_WITH_SHORT_TIME`.

        Parameters
        ----------
        style : `DiscordTimestampStyle`, optional
            Timestamp Style. by default DiscordTimestampStyle.LONG_DATE_WITH_SHORT_TIME

        Returns
        -------
        str
            formatted timestamp string.
        """
        return f"<t:{self.posix_timestamp}:{style}>"
