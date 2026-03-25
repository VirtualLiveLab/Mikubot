from typing import TypeVar, overload

import discord
from discord import Thread
from discord.abc import GuildChannel, PrivateChannel

from src.const import literal

from .logger import get_my_logger
from .validator import validate

T = TypeVar("T", bound=GuildChannel | PrivateChannel | Thread)


class Finder:
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.logger = get_my_logger("Finder")

    @overload
    async def find_channel(
        self,
        channel_id: int,
        expected_type: None = None,
    ) -> GuildChannel | PrivateChannel | Thread: ...

    @overload
    async def find_channel(self, channel_id: int, expected_type: type[T]) -> T: ...

    async def find_channel(
        self,
        channel_id: int,
        expected_type: type[T] | None = None,
    ) -> GuildChannel | PrivateChannel | Thread:
        channel = self.bot.get_channel(channel_id)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except Exception as e:
                self.logger.exception(literal.CHANNEL_NOT_FOUND, exc_info=e)
                raise

        if not expected_type:
            return channel

        return validate(channel, expected_type)

    async def find_guild(self, guild_id: int) -> discord.Guild:
        guild = self.bot.get_guild(guild_id)
        if not guild:
            try:
                guild = await self.bot.fetch_guild(guild_id)
            except Exception as e:
                self.logger.exception(literal.CHANNEL_NOT_FOUND, exc_info=e)
                raise
        return guild
