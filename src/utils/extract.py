import re

import discord
from discord import Client, Message

from .finder import Finder

regex_discord_message_url = (
    "(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/"
    "(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})(?!>)"
)
regex_extra_url = (
    r"\?base_aid=(?P<base_author_id>[0-9]{17,20})&aid=(?P<author_id>[0-9]{17,20})&extra=(?P<extra_messages>(|[0-9,]+))"
)


class DiscordExtractor:
    def __init__(self, client: Client) -> None:
        self._client = client
        self._finder = Finder(client)

    async def from_matches(self, matches: set[re.Match[str]]) -> list[Message]:
        messages: list[Message] = []
        for ids in matches:
            if int(ids["guild"]) not in [g.id for g in self._client.guilds]:
                continue

            fetched_message = await self._fetch_message_from_id(
                channel_id=int(ids["channel"]),
                message_id=int(ids["message"]),
            )
            if fetched_message is not None:
                messages.append(fetched_message)
        return messages

    async def _fetch_message_from_id(self, *, channel_id: int, message_id: int) -> Message | None:
        channel = await self._finder.find_channel(channel_id)
        if not isinstance(channel, discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread):
            return None

        try:
            return await channel.fetch_message(message_id)
        except Exception:  # noqa: BLE001
            return None
